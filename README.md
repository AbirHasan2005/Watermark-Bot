# Watermark-Bot
A Telegram Video Watermark Adder Bot by [@AbirHasan2005](https://github.com/AbirHasan2005)

## Features:
- Save Custom Watermark Image.
- Auto Resize Watermark According to Video quality.
- Easy Apply saved watermark to video.
- Progress of all tasks.
- Can Choose [FFMPEG](https://www.ffmpeg.org/) Process Preset.
- Can Cancel Process. *(Beta)*
- Any Channel or Group Force Sub.
- Logs Process in any channel.
- Broadcast Feature.
- Can Save Watermark Position for users.
- Can Save Watermark Size for users.
- Can Upload to [Streamtape](https://streamtape.com/) if File Size is more than 2GB.

### Demo Bot:
<a href="https://t.me/VideoWatermark_Bot"><img src="https://img.shields.io/badge/Demo-Telegram%20Bot-blue.svg?logo=telegram"></a>

## Configs:
- `API_ID` - Get this from [@TeleORG_Bot](https://t.me/TeleORG_Bot)
- `API_HASH` - Get this from [@TeleORG_Bot](https://t.me/TeleORG_Bot)
- `BOT_TOKEN` - Get this from [@BotFather](https://t.me/BotFather)
- `BOT_USERNAME` - You Bot Username. *(Without [@])*
- `LOG_CHANNEL` - Logs Channel ID
- `OWNER_ID` - Bot Owner UserID
- `DATABASE_URL` - MongoDB Database URI
- `UPDATES_CHANNEL` - Force Sub Channel ID *(Optional)*
- `PRESET` - Video Encoding Preset Type *(Optional)*
	- Better put `ultrafast` or `superfast` or `veryfast`
- `STREAMTAPE_API_PASS` - Get this from [Here](https://streamtape.com/accpanel#collapseThree).
	- For Uploading to Streamtape if File Size is more than 2GB.
- `STREAMTAPE_API_USERNAME` - Get this from [Here](https://streamtape.com/accpanel#collapseThree).
	- For Uploading to Streamtape if File Size is more than 2GB.

## BotFather Commands:
```
start - start the bot
status - Show number of users in DB & Bot Status
broadcast - Broadcast replied message to DB Users
cancel - Cancel Current Task
settings - User Settings Panel
reset - Reset all settings to default
```

### Support Group:
<a href="https://t.me/DevsZone"><img src="https://img.shields.io/badge/Telegram-Join%20Telegram%20Group-blue.svg?logo=telegram"></a>

## Deploy:

#### Easiest Way [Deploy To Heroku] 😪

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/AbirHasan2005/Watermark-Bot)

#### Video Tutorial:
[![YouTube](https://img.shields.io/badge/YouTube-Video%20Tutorial-red?logo=youtube)](https://www.youtube.com/watch?v=A7wnaKMHpvU&t)

#### The Hard Way 🤕
```sh
git clone https://github.com/AbirHasan2005/Watermark-Bot
cd Watermark-Bot
virtualenv -p python3 VENV
. ./VENV/bin/activate
pip3 install -r requirements.txt
--- EDIT configs.py values appropriately ---
python3 bot.py
```

### Follow on:
<p align="left">
<a href="https://github.com/AbirHasan2005"><img src="https://img.shields.io/badge/GitHub-Follow%20on%20GitHub-inactive.svg?logo=github"></a>
</p>
<p align="left">
<a href="https://twitter.com/AbirHasan2005"><img src="https://img.shields.io/badge/Twitter-Follow%20on%20Twitter-informational.svg?logo=twitter"></a>
</p>
<p align="left">
<a href="https://facebook.com/AbirHasan2005"><img src="https://img.shields.io/badge/Facebook-Follow%20on%20Facebook-blue.svg?logo=facebook"></a>
</p>
<p align="left">
<a href="https://instagram.com/AbirHasan2005"><img src="https://img.shields.io/badge/Instagram-Follow%20on%20Instagram-important.svg?logo=instagram"></a>
</p>
