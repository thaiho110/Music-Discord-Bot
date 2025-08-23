import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
LAVALINK_PASSWORD = os.getenv('LAVALINK_PASSWORD')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """
    Called when the bot is ready and has successfully connected to Discord.
    """
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('-------------------------------------------')
    
    try:
        await bot.load_extension('cogs.music_cogs')
        print('Successfully loaded the music cog.')
    except Exception as e:
        print(f'Failed to load music cog: {e}')

bot.run(TOKEN)