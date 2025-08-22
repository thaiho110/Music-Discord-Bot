import discord
from discord.ext import commands
import yt_dlp
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

music_queue = []
is_playing = False
now_playing_message = None


class PlayerView(discord.ui.View):
    def __init__(self, ctx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.timeout = None # View does not time out

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.secondary, emoji="⏸️")
    async def pause_resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.ctx.voice_client
        if not vc:
            return await interaction.response.send_message("I'm not connected.", ephemeral=True)

        if vc.is_playing():
            vc.pause()
            button.label = "Resume"
            button.emoji = "▶️"
            await interaction.response.edit_message(view=self)
        elif vc.is_paused():
            vc.resume()
            button.label = "Pause"
            button.emoji = "⏸️"
            await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.secondary, emoji="⏭️")
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.ctx.voice_client
        if not vc or not (vc.is_playing() or vc.is_paused()):
            return await interaction.response.send_message("I'm not playing anything.", ephemeral=True)
        vc.stop()
        await interaction.response.send_message("Skipped!", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger, emoji="⏹️")
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        global music_queue, is_playing, now_playing_message
        vc = self.ctx.voice_client
        if not vc:
            return await interaction.response.send_message("I'm not connected.", ephemeral=True)
            
        music_queue.clear()
        is_playing = False
        vc.stop()
        
        if now_playing_message:
            await now_playing_message.edit(content="Player stopped, queue cleared.", embed=None, view=None)
        self.stop()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

async def play_next(ctx):
    global is_playing, music_queue, now_playing_message
    if len(music_queue) > 0:
        is_playing = True
        song_info = music_queue.pop(0)
        url, title = song_info['url'], song_info['title']
        
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
        
        embed = discord.Embed(title="Now Playing", description=f"**{title}**", color=discord.Color.green())
        view = PlayerView(ctx=ctx)
        now_playing_message = await ctx.send(embed=embed, view=view)
    else:
        is_playing = False
        if now_playing_message:
            await now_playing_message.edit(content="Queue finished!", embed=None, view=None)

@bot.command(name='play', help='Adds a song to the queue.')
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        return await ctx.send("You need to be in a voice channel to play music.")
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': True, 'default_search': 'auto'}
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        except Exception:
            return await ctx.send("Sorry, I could not find that song.")
            
    song_info = {'title': info.get('title'), 'url': info.get('url')}
    music_queue.append(song_info)
    await ctx.send(f"✅ Added to queue: **{song_info['title']}**")
    
    if not is_playing:
        await play_next(ctx)
        
@bot.command(name='skip', help='Skips the current song.')
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped current song.")
    else:
        await ctx.send("I'm not playing anything right now.")

@bot.command(name='queue', help='Displays the current music queue.')
async def queue(ctx):
    if len(music_queue) == 0:
        await ctx.send("The music queue is currently empty.")
        return
    queue_list = ""
    for i, song in enumerate(music_queue):
        queue_list += f"{i+1}. {song['title']}\n"
    
    embed = discord.Embed(title="Music Queue", description=queue_list, color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command(name='stop', help='Stops the music and clears the queue.')
async def stop(ctx):
    global music_queue, is_playing
    if ctx.voice_client:
        music_queue = []
        is_playing = False
        ctx.voice_client.stop()
        await ctx.send("⏹️ Stopped the music and cleared the queue.")
    else:
        await ctx.send("I'm not connected to a voice channel.")

print("Token loaded. Starting bot...")
bot.run(TOKEN)