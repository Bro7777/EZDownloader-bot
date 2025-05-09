# EZDownloader 🎧📥

**EZDownloader** is a feature-rich Discord bot that allows users to download videos and audio directly from a URL inside Discord. It supports both MP4 (video) and MP3 (audio) formats and provides a secure Gofile link for easy sharing.

---

## 🚀 Features

- 🎬 Download videos in MP4 format
- 🎵 Extract audio in MP3 format
- 🔗 Uploads to [Gofile.io](https://gofile.io) and returns a download link
- ⏳ Automatic cleanup (optional scheduling support)
- 🔐 Secure handling of environment variables via `.env`
- 🛠 Powered by `yt-dlp`, `ffmpeg`, and `aiohttp`

---

## 📦 Requirements

- Python 3.10+
- A Discord bot token
- yt-dlp
- ffmpeg
- A Gofile API token

---

## 🛠 Installation

1. Clone the repo:

    ```bash
    git clone https://github.com/Bro7777/EZDownloader-bot.git
    cd EZDownloader-bot
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file:

    ```env
    DISCORD_TOKEN=your_discord_bot_token
    GOFILE_API=your_gofile_api_token
    ```

4. Run the bot:

    ```bash
    python main.py
    ```

---

## 💬 Usage

In Discord, use the following command:

```bash
/download <url> <format>
```

- `url`: Link to the media
- `format`: `mp4` or `mp3`

Example:
```
/download https://youtu.be/dQw4w9WgXcQ mp3
```

The bot will upload the file to Gofile and send you a private download link.

---

## ℹ️ Info Command

You can also use the `/info` command in Discord to get a brief summary of what the bot does and who created it.

---

## 👨‍💻 Developer

Developed by **@Bro7777**  
Feel free to contribute or suggest improvements!

