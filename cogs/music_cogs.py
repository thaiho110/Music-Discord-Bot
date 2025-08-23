import re
import os
import asyncio # Import asyncio for the auto-disconnect delay
from dotenv import load_dotenv

import discord
import lavalink
from discord.ext import commands
from lavalink.events import TrackStartEvent, QueueEndEvent
from lavalink.errors import ClientError, AuthenticationError
from lavalink.server import LoadType

load_dotenv()
LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD")

url_rx = re.compile(r'https?://(?:www\.)?.+')

class PlayerView(discord.ui.View):
    def __init__(self, player: lavalink.DefaultPlayer):
        super().__init__(timeout=None)
        self.player = player

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not interaction.user.voice or interaction.user.voice.channel.id != int(self.player.channel_id):
            await interaction.response.send_message("You must be in the same voice channel to use this.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Pause/Resume", style=discord.ButtonStyle.primary, emoji="⏯️", row=0)
    async def pause_resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.player.paused:
            await self.player.set_pause(False)
            await interaction.response.send_message("Resumed!", ephemeral=True)
        else:
            await self.player.set_pause(True)
            await interaction.response.send_message("Paused!", ephemeral=True)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.secondary, emoji="⏭️", row=0)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.player.skip()
        await interaction.response.send_message("Skipped!", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger, emoji="⏹️", row=1)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player.queue.clear()
        await self.player.stop()
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(content="⏹️ Playback stopped and queue cleared.", view=self)
        self.stop()

    @discord.ui.button(label="Queue", style=discord.ButtonStyle.success, emoji="🎵", row=1)
    async def queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if not self.player.queue:
            return await interaction.response.send_message("The queue is empty.", ephemeral=True)

        queue_list = "\n".join(f"{i+1}. [{track.title}]({track.uri})" for i, track in enumerate(self.player.queue))
        embed = discord.Embed(title="Music Queue", description=queue_list, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, ephemeral=True)


class LavalinkVoiceClient(discord.VoiceProtocol):
    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        self.client = client
        self.channel = channel
        self.guild_id = channel.guild.id
        self._destroyed = False

        if not hasattr(self.client, 'lavalink'):
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(host='localhost', port=2333, password=LAVALINK_PASSWORD,
                                          region='us', name='default-node')
        self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        lavalink_data = {'t': 'VOICE_SERVER_UPDATE', 'd': data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        channel_id = data['channel_id']
        if not channel_id:
            await self._destroy()
            return
        self.channel = self.client.get_channel(int(channel_id))
        lavalink_data = {'t': 'VOICE_STATE_UPDATE', 'd': data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool, self_deaf: bool = False, self_mute: bool = False) -> None:
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel, self_mute=self_mute, self_deaf=self_deaf)

    async def disconnect(self, *, force: bool = False) -> None:
        player = self.lavalink.player_manager.get(self.channel.guild.id)
        if not force and not player.is_connected:
            return
        await self.channel.guild.change_voice_state(channel=None)
        player.channel_id = None
        await self._destroy()

    async def _destroy(self):
        self.cleanup()
        if self._destroyed: return
        self._destroyed = True
        try:
            await self.lavalink.player_manager.destroy(self.guild_id)
        except ClientError:
            pass


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, 'lavalink'):
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node(host='localhost', port=2333, password=LAVALINK_PASSWORD,
                                  region='us', name='default-node')
        self.lavalink: lavalink.Client = bot.lavalink
        self.lavalink.add_event_hooks(self)

    def cog_unload(self):
        self.lavalink._event_hooks.clear()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
        elif isinstance(error, AuthenticationError):
            await ctx.send("Authentication failed. Please check your Lavalink password.")

    async def ensure_voice(ctx: commands.Context):
        player = ctx.bot.lavalink.player_manager.create(ctx.guild.id)
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Join a voice channel first.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError("I'm not connected.")
            permissions = ctx.author.voice.channel.permissions_for(ctx.me)
            if not permissions.connect or not permissions.speak:
                raise commands.CommandInvokeError('I need `CONNECT` and `SPEAK` permissions.')
            
            # Store the text channel for future messages
            player.store('channel', ctx.channel.id) 
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voice channel.')
        return True

    # --- MODIFIED: Event Listeners ---

    @lavalink.listener(TrackStartEvent)
    async def on_track_start(self, event: TrackStartEvent):
        player = event.player
        channel_id = player.fetch('channel')
        channel = self.bot.get_channel(channel_id)
        
        # Clean up the previous 'Now Playing' message if it exists
        if player.fetch('now_playing_message'):
            try:
                old_message = await channel.fetch_message(player.fetch('now_playing_message'))
                await old_message.delete()
            except discord.NotFound:
                pass # Message was already deleted

        embed = discord.Embed(title="Now Playing",
                              description=f"[{event.track.title}]({event.track.uri})",
                              color=discord.Color.green())
        
        # Send the new message with the PlayerView
        message = await channel.send(embed=embed, view=PlayerView(player))
        # Store the message ID on the player
        player.store('now_playing_message', message.id)

    @lavalink.listener(QueueEndEvent)
    async def on_queue_end(self, event: QueueEndEvent):
        player = event.player
        guild_id = player.guild_id
        guild = self.bot.get_guild(guild_id)

        channel_id = player.fetch('channel')
        channel = self.bot.get_channel(channel_id)

        # Clean up the final 'Now Playing' message
        if player.fetch('now_playing_message'):
            try:
                old_message = await channel.fetch_message(player.fetch('now_playing_message'))
                await old_message.edit(content="Queue has finished.", embed=None, view=None)
            except discord.NotFound:
                pass

        # Wait for 60 seconds before disconnecting
        await asyncio.sleep(60)

        # Check if the player is still connected and not playing
        if player.is_connected and not player.is_playing:
            if guild and guild.voice_client:
                await channel.send("Queue has ended. Leaving voice channel.")
                await guild.voice_client.disconnect(force=True)

    # --- Commands ---

    @commands.command(aliases=['p'])
    @commands.check(ensure_voice)
    async def play(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)

        embed = discord.Embed(color=discord.Color.blurple())
        if not results or not results.tracks:
            return await ctx.send("Couldn't find anything!")
        
        if results.load_type == LoadType.PLAYLIST:
            tracks = results.tracks
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results.playlist_info.name} - {len(tracks)} tracks'
        else:
            track = results.tracks[0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track.title}]({track.uri})'
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['s', 'skip'])
    @commands.check(ensure_voice)
    async def fskip(self, ctx):
        """ Skips the current track. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send("I'm not playing anything.")
            
        await player.skip()
        await ctx.send('⏭️ | Skipped the current track.')
    
    @commands.command()
    @commands.check(ensure_voice)
    async def stop(self, ctx):
        """ Stops the player and clears the queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send("I'm not playing anything.")

        player.queue.clear()
        await player.stop()

        # Clean up the 'Now Playing' message
        if player.fetch('now_playing_message'):
            channel = self.bot.get_channel(player.fetch('channel'))
            try:
                message = await channel.fetch_message(player.fetch('now_playing_message'))
                await message.edit(content="⏹️ Playback stopped and queue cleared.", embed=None, view=None)
            except discord.NotFound:
                pass

        await ctx.send('⏹️ | Stopped playback and cleared the queue.')

    @commands.command(aliases=['dc'])
    @commands.check(ensure_voice)
    async def disconnect(self, ctx):
        """ Disconnects the player and clears the queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        player.queue.clear()
        await player.stop()
        await ctx.voice_client.disconnect(force=True)
        await ctx.send('✳️ | Disconnected.')

async def setup(bot):
    await bot.add_cog(Music(bot))