# (c) @AbirHasan2005

# Don't Forget That I Made This!
# So Give Credtis!


import os

class Config(object):
	BOT_TOKEN = os.environ.get("BOT_TOKEN")
	API_ID = int(os.environ.get("API_ID", 12345))
	API_HASH = os.environ.get("API_HASH")
	LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))
	DOWN_PATH = os.environ.get("DOWN_PATH", "./downloads")
	OWNER_ID = int(os.environ.get("OWNER_ID", 1445283714))
	CAPTION = "By @AHToolsBot"
	SESSION_NAME = os.environ.get("SESSION_NAME", "VidWatermarkBot")
	USAGE_WATERMARK_ADDER = """
Hi, I am Video Watermark Adder Bot!

**How to Added Watermark to a Video?**
**Usage:** First Send a JPG Image/Logo, then send any Video. Better add watermark to a MP4 or MKV Video.

__Note: I can only process one video at a time. As my server is Heroku, my health is not good. If you have any issues with Adding Watermark to a Video, then please Report at [Support Group](https://t.me/linux_repo).__

Desgined by @AbirHasan2005
"""
	PROGRESS = """
Percentage : {0}%
Done ✅: {1}
Total 🌀: {2}
Speed 🚀: {3}/s
ETA 🕰: {4}
"""