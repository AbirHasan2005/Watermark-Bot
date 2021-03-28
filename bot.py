# (c) @AbirHasan2005

# This is Telegram Video Watermark Adder Bot's Source Code.
# I Hardly Made This. So Don't Forget to Give Me Credits.
# Done this Huge Task for Free. If you guys not support me,
# I will stop making such things!

# Edit anything at your own risk!

# Don't forget to help me if I done any mistake in the codes.
# Support Group: @linux_repo 
# Bots Channel: @Discovery_Updates

import os
import json
import time
import shutil
import random
import asyncio
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from datetime import datetime
from core.ffmpeg import vidmark, take_screen_shot
from core.clean import delete_all, delete_trash
from pyrogram import Client, filters
from configs import Config
from core.display_progress import progress_for_pyrogram, humanbytes
from humanfriendly import format_timespan
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.flood_420 import FloodWait

AHBot = Client(Config.SESSION_NAME, bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH)

@AHBot.on_message(filters.command(["start", "help"]) & filters.private)
async def HelpWatermark(bot, cmd):
	await cmd.reply_text(
		text=Config.USAGE_WATERMARK_ADDER,
		parse_mode="Markdown",
		reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Developer", url="https://t.me/AbirHasan2005"), InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")], [InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")]]),
		disable_web_page_preview=True
	)

@AHBot.on_message(filters.photo & filters.private)
async def VidWatermarkSaver(bot, cmd):
	editable = await cmd.reply_text("Downloading Image ...")
	dl_loc = Config.DOWN_PATH + "/" + str(cmd.from_user.id) + "/"
	watermark_path = Config.DOWN_PATH + "/" + str(cmd.from_user.id) + "/thumb.jpg"
	await asyncio.sleep(5)
	c_time = time.time()
	the_media = await bot.download_media(
		message=cmd,
		file_name=dl_loc,
		progress=progress_for_pyrogram,
		progress_args=(
			"Downloading Sir ...",
			editable,
			c_time
		)
	)
	## --- Resizer --- ##
	image = Image.open(the_media)
	new_image = image.resize((100, 100), Image.ANTIALIAS)
	new_image.save(watermark_path)
	await delete_trash(the_media)
	## --- Done --- ##
	await editable.delete()
	await cmd.reply_text("This Saved as Next Video Watermark!\n\nNow Send any Video to start adding Watermark to the Video!")


@AHBot.on_message(filters.document | filters.video & filters.private)
async def VidWatermarkAdder(bot, cmd):
	## --- Noobie Process --- ##
	working_dir = Config.DOWN_PATH + "/WatermarkAdder/"
	if not os.path.exists(working_dir):
		os.makedirs(working_dir)
	watermark_path = Config.DOWN_PATH + "/" + str(cmd.from_user.id) + "/thumb.jpg"
	if not os.path.exists(watermark_path):
		await cmd.reply_text("You Didn't Set Any Watermark!\n\nReply to any JPG File with /set_watermark ...")
		return
	file_type = cmd.video or cmd.document
	if not file_type.mime_type.startswith("video/"):
		await cmd.reply_text("This is not a Video!")
		return
	status = Config.DOWN_PATH + "/WatermarkAdder/status.json"
	if os.path.exists(status):
		await cmd.reply_text("Sorry, Currently I am busy with another Task!\n\nTry Again After Sometime!")
		return
	preset = "ultrafast"
	editable = await cmd.reply_text("Downloading Video ...", parse_mode="Markdown")
	with open(status, "w") as f:
		statusMsg = {
			'chat_id': cmd.from_user.id,
			'message': editable.message_id
		}
		json.dump(statusMsg, f, indent=2)
	dl_loc = Config.DOWN_PATH + "/WatermarkAdder/" + str(cmd.from_user.id) + "/"
	if not os.path.isdir(dl_loc):
		os.makedirs(dl_loc)
	the_media = None
	logs_msg = None
	user_info = f"**UserID:** #id{cmd.from_user.id}\n**Name:** [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})"
	## --- Done --- ##
	try:
		forwarded_video = await cmd.forward(Config.LOG_CHANNEL)
		logs_msg = await bot.send_message(chat_id=Config.LOG_CHANNEL, text=f"Download Started!\n\n{user_info}", reply_to_message_id=forwarded_video.message_id, disable_web_page_preview=True, parse_mode="Markdown")
		await asyncio.sleep(5)
		c_time = time.time()
		the_media = await bot.download_media(
			message=cmd,
			file_name=dl_loc,
			progress=progress_for_pyrogram,
			progress_args=(
				"Downloading Sir ...",
				editable,
				c_time
			)
		)
		if (the_media is None):
			await delete_trash(status)
			await delete_trash(the_media)
			print(f"Download Failed: {err}")
			await editable.edit("Unable to Download The Video!")
			return
	except Exception as err:
		await delete_trash(status)
		await delete_trash(the_media)
		print(f"Download Failed: {err}")
		await editable.edit("Unable to Download The Video!")
		return
	await editable.edit("Trying to Add Watermark to the Video at Top Left Corner ...\n\nPlease Wait!")
	duration = 0
	metadata = extractMetadata(createParser(the_media))
	if metadata.has("duration"):
		duration = metadata.get('duration').seconds
	the_media_file_name = os.path.basename(the_media)
	main_file_name = os.path.splitext(the_media_file_name)[0]
	output_vid = main_file_name + "_[" + str(cmd.from_user.id) + "]_[" + str(time.time()) + "]_[@AbirHasan2005]" + ".mp4"
	progress = Config.DOWN_PATH + "/WatermarkAdder/" + str(cmd.from_user.id) + "/progress.txt"
	try:
		output_vid = await vidmark(the_media, editable, progress, watermark_path, output_vid, duration, logs_msg, status, preset)
	except Exception as err:
		print(f"Unable to Add Watermark: {err}")
		await editable.edit("Unable to add Watermark!")
		await logs_msg.edit(f"#ERROR: Unable to add Watermark!\n\n**Error:** `{err}`")
		try:
			await delete_all()
		except:
			pass
		return
	if output_vid == None:
		await editable.edit("Something went wrong!")
		await logs_msg.edit("#ERROR: Something went wrong!")
		try:
			await delete_all()
		except Exception as err:
			print(err)
		return
	await editable.edit("Watermark Added Successfully!\n\nTrying to Upload ...")
	await logs_msg.edit("Watermark Added Successfully!\n\nTrying to Upload ...")
	width = 100
	height = 100
	duration = 0
	metadata = extractMetadata(createParser(output_vid))
	if metadata.has("duration"):
		duration = metadata.get('duration').seconds
	if metadata.has("width"):
		width = metadata.get("width")
	if metadata.has("height"):
		height = metadata.get("height")
	video_thumbnail = None
	try:
		video_thumbnail = Config.DOWN_PATH + "/WatermarkAdder/" + str(cmd.from_user.id) + "/" + str(time.time()) + ".jpg"
		ttl = random.randint(0, int(duration) - 1)
		file_genertor_command = [
			"ffmpeg",
			"-ss",
			str(ttl),
			"-i",
			output_vid,
			"-vframes",
			"1",
			video_thumbnail
		]
		process = await asyncio.create_subprocess_exec(
			*file_genertor_command,
			stdout=asyncio.subprocess.PIPE,
			stderr=asyncio.subprocess.PIPE,
		)
		stdout, stderr = await process.communicate()
		e_response = stderr.decode().strip()
		t_response = stdout.decode().strip()
		print(e_response)
		print(t_response)
		Image.open(video_thumbnail).convert("RGB").save(video_thumbnail)
		img = Image.open(video_thumbnail)
		img.resize((width, height))
		img.save(video_thumbnail, "JPEG")
	except Exception as err:
		print(f"Error: {err}")
	# --- Upload --- #
	sent_vid = None
	file_size = os.path.getsize(output_vid)
	if int(file_size) > 2097152000:
		await editable.edit(f"Sorry Sir,\n\nFile Size Become {humanbytes(file_size)} !!\nI can't Upload to Telegram!")
		await delete_all()
		return
	await asyncio.sleep(5)
	try:
		c_time = time.time()
		sent_vid = await bot.send_video(
			chat_id=cmd.chat.id,
			video=output_vid,
			caption=f"**File Name:** `{output_vid}`\n**Video Duration:** `{format_timespan(duration)}`\n**File Size:** `{humanbytes(file_size)}`\n\n{Config.CAPTION}",
			thumb=video_thumbnail,
			duration=duration,
			width=width,
			height=height,
			reply_to_message_id=cmd.message_id,
			supports_streaming=True,
			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Developer", url="https://t.me/AbirHasan2005")], [InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")], [InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")]]),
			progress=progress_for_pyrogram,
			progress_args=(
				"Uploading, Wait Sir ...",
				editable,
				c_time
			)
		)
	# Any Better Way? :(
	except FloodWait as e:
		print(f"Got FloodWait of {e.x}s ...")
		await asyncio.sleep(e.x)
		await asyncio.sleep(5)
		c_time = time.time()
		sent_vid = await bot.send_video(
			chat_id=cmd.chat.id,
			video=output_vid,
			caption=f"**File Name:** `{output_vid}`\n**Video Duration:** `{format_timespan(duration)}`\n**File Size:** `{humanbytes(file_size)}`\n\n{Config.CAPTION}",
			thumb=video_thumbnail,
			duration=duration,
			width=width,
			height=height,
			reply_to_message_id=cmd.message_id,
			supports_streaming=True,
			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Developer", url="https://t.me/AbirHasan2005")], [InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")], [InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")]]),
			progress=progress_for_pyrogram,
			progress_args=(
				"Uploading, Wait Sir ...",
				editable,
				c_time
			)
		)
	except Exception as err:
		print(f"Unable to Upload Video: {err}")
		await logs_msg.edit(f"#ERROR: Unable to Upload Video!\n\n**Error:** `{err}`")
		await delete_all()
		return
	await delete_all()
	await editable.delete()
	forward_vid = await sent_vid.forward(Config.LOG_CHANNEL)
	await logs_msg.delete()
	await bot.send_message(chat_id=Config.LOG_CHANNEL, text=f"#WATERMARK_ADDED: Video Uploaded!\n\n{user_info}", reply_to_message_id=forward_vid.message_id)

@AHBot.on_message(filters.command("cancel") & filters.private) # Also We Can Use [filters.user()]
async def CancelWatermarkAdder(bot, cmd):
	if not int(cmd.from_user.id) == Config.OWNER_ID:
		await cmd.reply_text("You Can't Use That Command!")
		return

	status = Config.DOWN_PATH + "/WatermarkAdder/status.json"
	with open(status, 'r+') as f:
		statusMsg = json.load(f)
		if 'pid' in statusMsg.keys():
			try:
				os.kill(statusMsg["pid"], 9)
				await delete_trash(status)
			except Exception as err:
				print(err)
		await delete_all()
		await bot.send_message(chat_id=Config.LOG_CHANNEL, text="#WATERMARK_ADDER: Stopped!")
		await cmd.reply_text("Watermark Adding Process Stopped!")
		try:
			await bot.edit_message_text(chat_id=int(statusMsg["chat_id"]), message_id=int(statusMsg["message"]), text="🚦🚦 Last Process Stopped 🚦🚦")
		except:
			pass

AHBot.run()