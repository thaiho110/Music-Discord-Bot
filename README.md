🎵 MelodyBot: A Python Discord Music Bot
A feature-rich, asynchronous music bot for Discord, built with Python using discord.py. It supports a full music queue system, interactive button controls, scheduled playback, and is optimized for performance.
This project is designed to be a robust starting point for anyone looking to create their own Discord music bot or learn more about the discord.py library and its advanced features.
✨ Features
High-Quality Audio Streaming: Plays music from YouTube (via URL or search query) directly into a voice channel.
Advanced Queue System: Add multiple songs to a queue. The bot will automatically play the next song when the current one finishes.
Interactive UI Controls: A clean "Now Playing" message with buttons for Pause/Resume, Skip, and Stop. No need to type commands for basic controls!
Lag-Free Performance: Uses asynchronous programming and runs blocking tasks in a separate thread to keep the bot responsive at all times.
Scheduled Playback: Configure the bot to automatically join a specific voice channel at a set time each day and play a "wake-up" song, but only if members are present.
Standard Commands: Includes text commands for managing the queue (!play, !skip, !queue, !stop) and voice connection (!join, !leave).
Secure and Configurable: Keeps your bot token safe using a .env file and allows for easy configuration of all features.
🔧 Prerequisites
Before you begin, ensure you have the following installed on your system:
Python 3.8 or higher: Download Python
FFmpeg: A required library for processing audio.
Windows: Download FFmpeg and add the bin folder to your system's PATH.
macOS (via Homebrew): brew install ffmpeg
Linux (Debian/Ubuntu): sudo apt install ffmpeg
A Discord Bot Application:
Create a new application on the Discord Developer Portal.
In the "Bot" tab, create a bot user and enable the MESSAGE CONTENT INTENT and SERVER MEMBERS INTENT under "Privileged Gateway Intents".
🚀 Setup and Installation
Follow these steps to get your instance of MelodyBot up and running.
1. Clone the Repository
code
Bash
git clone https://github.com/YourUsername/YourBotRepository.git
cd YourBotRepository
2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.
code
Bash
# For Windows
python -m venv .venv
.\.venv\Scripts\activate

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
Create a requirements.txt file with the following content:
code
Txt
# requirements.txt
discord.py
python-dotenv
yt-dlp
PyNaCl
```Then, install the packages using pip:
```bash
pip install -r requirements.txt
4. Configure the Bot
Create a file named .env in the root of your project directory. This is where you will store your secret token and other settings.
Copy the contents of .env.example below into your .env file and fill in the values.
code
Ini
# .env.example - Copy this into a new .env file

# Your secret bot token from the Discord Developer Portal
DISCORD_TOKEN=YourActualBotTokenGoesHere

# --- Scheduled Song Configuration ---
# The ID of the voice channel for the scheduled task.
# To get this, enable Developer Mode in Discord, right-click the channel, and "Copy Channel ID".
TARGET_CHANNEL_ID=123456789012345678

# The time to play the scheduled song (24-hour format)
SCHEDULED_HOUR=8
SCHEDULED_MINUTE=0

# The YouTube URL of the song you want to play automatically
SONG_URL="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
5. Run the Bot!
Once configured, you can start the bot with:
code
Bash
python music_bot.py
If everything is set up correctly, you will see a confirmation message in your terminal, and the bot will appear as "online" in Discord.
🎶 Bot Usage
Invite the bot to your server using the OAuth2 URL generated from the Discord Developer Portal. Make sure to grant it the bot and applications.commands scopes, along with permissions to View Channels, Send Messages, Connect, and Speak.
Main Commands
!play <song name or URL>: Searches for a song on YouTube and adds it to the queue. If the queue is empty, it starts playing immediately.
!queue: Displays the list of songs currently in the queue.
!skip: Skips the currently playing song and moves to the next one in the queue.
!stop: Stops the music, clears the entire queue, and removes the player message.
!join: Makes the bot join the voice channel you are currently in.
!leave: Disconnects the bot from its current voice channel.
Button Controls
When a song starts playing, the bot will post a "Now Playing" message with interactive buttons:
⏸️ Pause / ▶️ Resume: Toggles playback.
⏭️ Skip: Skips to the next song.
⏹️ Stop: Stops the music and clears the queue.
☁️ Hosting
To make the bot available 24/7, you need to host it on a server.
Recommended: A Virtual Private Server (VPS) from providers like DigitalOcean, Vultr, or Linode offers the best performance and reliability for audio streaming.
Alternative: Platform as a Service (PaaS) providers like Railway can offer an easier setup with a free tier, but may have resource limitations.
⚠️ Important Disclaimer
This bot is designed to stream audio from sources like YouTube for personal use. The act of streaming copyrighted material may violate the Terms of Service of both the streaming platform (YouTube) and the hosting provider.
The developers of this project are not responsible for how it is used.
Running a large, public music bot that streams from YouTube is against their ToS and will likely result in a shutdown.
Use at your own risk. This project is intended for educational and small-scale personal use.
