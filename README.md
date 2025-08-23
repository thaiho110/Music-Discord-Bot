# 🎵 MelodyBot: A Lavalink-Powered Discord Music Bot
A feature-rich, asynchronous music bot for Discord, built with Python using **discord.py**. It supports a full music queue system, interactive button controls, scheduled playback, and is optimized for performance.
This project is designed to be a robust starting point for anyone looking to create their own Discord music bot or learn more about the discord.py library and its advanced features.
# ✨ Features
**High-Performance Audio:** Powered by Lavalink, audio processing is offloaded from the bot to a separate server, resulting in smooth, lag-free playback even in busy servers.

**Multi-Source Streaming:** Plays music from YouTube (via URL or search query) and can be extended to support other sources like SoundCloud.

**Advanced Queue System:** Add multiple songs or entire playlists to a queue. The bot automatically plays the next song and gracefully handles the end of the queue.

**Interactive UI Controls:** A clean "Now Playing" message with buttons for Pause/Resume, Skip, and Stop. No need to type commands for basic controls!

**Auto Disconnect:** To save resources, the bot will automatically leave the voice channel after a period of inactivity once the queue has finished.

**Comprehensive Commands:** Includes text commands for playing music, managing the queue, and controlling playback (!play, !skip, !queue, !stop, !pause, !resume, !disconnect).

**Secure and Configurable:** Keeps your bot token and Lavalink password safe using a .env file for easy configuration.

# 🔧 Prerequisites

Before you begin, ensure you have the following installed on your system:

Python 3.8 or higher: Download [Python](www.python.org)

Java 17 or higher: Lavalink is a Java application and requires a modern [Java](https://www.java.com/en/) runtime.

Check your version with 
```bash
java -version
```

Lavalink Server: You need the [Lavalink.jar](https://github.com/lavalink-devs/Lavalink) file.

Download the latest Lavalink.jar from the official GitHub releases.

# A Discord Bot Application:

Create a new application on the [Discord Developer Portal](https://discord.com/developers).

In the "Bot" tab, create a bot user and enable the MESSAGE CONTENT INTENT.

# 🚀 Setup and Installation

Follow these steps to get your instance of MelodyBot up and running.

# 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/YourBotRepository.git
cd YourBotRepository
```

# 2. Create a Virtual Environment
   
It's highly recommended to use a virtual environment to manage dependencies.

Windows
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

# 4. Install Dependencies

Create a file named requirements.txt in your project root with the following content:

```txt
# requirements.txt

discord.py
python-dotenv
lavalink
```

Then, install the packages using pip:
```bash
pip install -r requirements.txt
```

# 4. Configure the Application

You will need to configure both the Lavalink server and the Python bot.

**A. Configure Lavalink Server**

Create a folder named lavalink-server (or similar) on your machine. It can be outside of your bot's project folder.

Place the Lavalink.jar file you downloaded inside it.

In the same folder, create a file named application.yml and paste the following:

```
server:
  port: 2333
lavalink:
  server:
    password: "YourSecurePasswordHere" # Choose a strong password
```
**B. Configure the Bot**

In the root of your bot's project directory, create a file named .env.

Add your secret tokens and passwords to this file. It must match your application.yml.

```
# .env file content

# Your secret bot token from the Discord Developer Portal
DISCORD_TOKEN=YourActualBotTokenGoesHere

# The password you set in application.yml
LAVALINK_PASSWORD=YourSecurePasswordHere
```
# 5. Running the Application

The bot requires two separate processes to be running: the Lavalink server and the Python bot itself. You will need two separate terminal windows.

**Terminal 1: Start the Lavalink Server**
```
# Navigate to your lavalink-server directory
cd path/to/your/lavalink-server
```
```
# Run the jar file
java -jar Lavalink.jar
```
You should see log output indicating Lavalink is ready to accept connections. Keep this terminal open.

**Terminal 2: Run the Bot**
```
# Navigate to your bot's project directory (if you're not already there)
cd path/to/your/YourBotRepository
```
```
# Run the main bot file (assuming it's named main.py)
python main.py
```

If everything is set up correctly, you will see a confirmation message in this terminal, and the bot will appear as "online" in Discord.

# 🎶 Bot Usage

Invite the bot to your server using the OAuth2 URL generated from the Discord Developer Portal. Make sure to grant it the bot and applications.commands scopes, along with permissions to View Channels, Send Messages, Connect, and Speak.

# Main Commands

!play <song name or URL>: Searches for a song on YouTube and adds it to the queue. If the queue is empty, it starts playing immediately.

!queue: Displays the list of songs currently in the queue.

!skip: Skips the currently playing song and moves to the next one in the queue.

!stop: Stops the music, clears the entire queue, and removes the player message.

!join: Makes the bot join the voice channel you are currently in.

!leave: Disconnects the bot from its current voice channel.

# Button Controls

When a song starts playing, the bot will post a "Now Playing" message with interactive buttons:

⏸️ Pause / ▶️ Resume: Toggles playback.

⏭️ Skip: Skips to the next song.

⏹️ Stop: Stops the music and clears the queue.

# ☁️ Hosting

To make the bot available 24/7, you need to host it on a server.

# ⚠️ Important Disclaimer

This bot is designed to stream audio from sources like YouTube for personal use. The act of streaming copyrighted material may violate the Terms of Service of both the streaming platform (YouTube) and the hosting provider.
The developers of this project are not responsible for how it is used.
Running a large, public music bot that streams from YouTube is against their ToS and will likely result in a shutdown.
Use at your own risk. This project is intended for educational and small-scale personal use.
Please update this readme for me please
