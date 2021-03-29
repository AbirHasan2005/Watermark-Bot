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
import math
import json
import string
import traceback
import random
import asyncio
import aiofiles
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from datetime import datetime
from random import choice
from core.ffmpeg import vidmark, take_screen_shot
from core.clean import delete_all, delete_trash
from pyrogram import Client, filters
from configs import Config
from core.database import Database
from core.display_progress import progress_for_pyrogram, humanbytes
from humanfriendly import format_timespan
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import InputUserDeactivated, UserIsBlocked
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

AHBot = Client(Config.BOT_USERNAME, bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH)
db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)
broadcast_ids = {}

async def send_msg(user_id, message):
	try:
		await message.forward(chat_id=user_id)
		return 200, None
	except FloodWait as e:
		await asyncio.sleep(e.x)
		return send_msg(user_id, message)
	except InputUserDeactivated:
		return 400, f"{user_id} : deactivated\n"
	except UserIsBlocked:
		return 400, f"{user_id} : blocked the bot\n"
	except PeerIdInvalid:
		return 400, f"{user_id} : user id invalid\n"
	except Exception as e:
		return 500, f"{user_id} : {traceback.format_exc()}\n"


@AHBot.on_message(filters.command(["start", "help"]) & filters.private)
async def HelpWatermark(bot, cmd):
	if not await db.is_user_exist(cmd.from_user.id):
		await db.add_user(cmd.from_user.id)
		await bot.send_message(
			Config.LOG_CHANNEL,
			f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
		)
	if Config.UPDATES_CHANNEL:
		invite_link = None
		try:
			invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
		except FloodWait as e:
			await asyncio.sleep(e.x)
			return
		try:
			user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.from_user.id)
			if user.status == "kicked":
				await bot.send_message(
					chat_id=cmd.from_user.id,
					text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		except UserNotParticipant:
			await bot.send_message(
				chat_id=cmd.from_user.id,
				text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
						],
						[
							InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
						]
					]
				),
				parse_mode="markdown"
			)
			return
		except Exception:
			await bot.send_message(
				chat_id=cmd.from_user.id,
				text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
				parse_mode="markdown",
				disable_web_page_preview=True
			)
			return
	await cmd.reply_text(
		text=Config.USAGE_WATERMARK_ADDER,
		parse_mode="Markdown",
		reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Developer", url="https://t.me/AbirHasan2005"), InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")], [InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")], [InlineKeyboardButton("Source Code", url="https://github.com/AbirHasan2005/Watermark-Bot")]]),
		disable_web_page_preview=True
	)

@AHBot.on_message(filters.photo & filters.private)
async def VidWatermarkSaver(bot, cmd):
	if not await db.is_user_exist(cmd.from_user.id):
		await db.add_user(cmd.from_user.id)
		await bot.send_message(
			Config.LOG_CHANNEL,
			f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
		)
	if Config.UPDATES_CHANNEL:
		invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
		try:
			user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.from_user.id)
			if user.status == "kicked":
				await bot.send_message(
					chat_id=cmd.from_user.id,
					text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		except UserNotParticipant:
			await bot.send_message(
				chat_id=cmd.from_user.id,
				text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
						],
						[
							InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
						]
					]
				),
				parse_mode="markdown"
			)
			return
		except Exception:
			await bot.send_message(
				chat_id=cmd.from_user.id,
				text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
				parse_mode="markdown",
				disable_web_page_preview=True
			)
			return
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
	try:
		image = Image.open(the_media)
		new_image = image.resize((200, 200), Image.ANTIALIAS)
		new_image.save(watermark_path)
	except Exception as err:
		print(err)
		return
	await delete_trash(the_media)
	## --- Done --- ##
	await editable.delete()
	await cmd.reply_text("This Saved as Next Video Watermark!\n\nNow Send any Video to start adding Watermark to the Video!")


@AHBot.on_message(filters.command("settings") & filters.private)
async def SettingsBot(bot, cmd):
	if not await db.is_user_exist(cmd.from_user.id):
		await db.add_user(cmd.from_user.id)
		await bot.send_message(
			Config.LOG_CHANNEL,
			f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
		)
	if Config.UPDATES_CHANNEL:
		invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
		try:
			user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.from_user.id)
			if user.status == "kicked":
				await bot.send_message(
					chat_id=cmd.from_user.id,
					text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		except UserNotParticipant:
			await bot.send_message(
				chat_id=cmd.from_user.id,
				text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
						],
						[
							InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
						]
					]
				),
				parse_mode="markdown"
			)
			return
		except Exception:
			await bot.send_message(
				chat_id=cmd.from_user.id,
				text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
				parse_mode="markdown",
				disable_web_page_preview=True
			)
			return

	position_tag = None
	watermark_position = await db.get_position(cmd.from_user.id)
	if watermark_position == "5:main_h-overlay_h":
		position_tag = "Bottom Left"
	elif watermark_position == "main_w-overlay_w-5:main_h-overlay_h-5":
		position_tag = "Bottom Right"
	elif watermark_position == "main_w-overlay_w-5:5":
		position_tag = "Top Right"
	elif watermark_position == "5:5":
		position_tag = "Top Left"
	await cmd.reply_text(
		text="Here you can set your Watermark Settings:",
		disable_web_page_preview=True,
		parse_mode="Markdown",
		reply_markup=InlineKeyboardMarkup(
			[
				[InlineKeyboardButton(f"Watermark Position - {position_tag}", callback_data="lol")],
				[InlineKeyboardButton("Set Bottom Left", callback_data=f"position_5:main_h-overlay_h"), InlineKeyboardButton("Set Bottom Right", callback_data=f"position_main_w-overlay_w-5:main_h-overlay_h-5")],
				[InlineKeyboardButton("Set Top Right", callback_data=f"position_main_w-overlay_w-5:5"), InlineKeyboardButton("Set Top Left", callback_data=f"position_5:5")]
			]
		)
	)


@AHBot.on_message(filters.document | filters.video & filters.private)
async def VidWatermarkAdder(bot, cmd):
	if not await db.is_user_exist(cmd.from_user.id):
		await db.add_user(cmd.from_user.id)
		await bot.send_message(
			Config.LOG_CHANNEL,
			f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
		)
	if Config.UPDATES_CHANNEL:
		invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
		try:
			user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.from_user.id)
			if user.status == "kicked":
				await bot.send_message(
					chat_id=cmd.from_user.id,
					text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		except UserNotParticipant:
			await bot.send_message(
				chat_id=cmd.from_user.id,
				text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
						],
						[
							InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
						]
					]
				),
				parse_mode="markdown"
			)
			return
		except Exception:
			await bot.send_message(
				chat_id=cmd.from_user.id,
				text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
				parse_mode="markdown",
				disable_web_page_preview=True
			)
			return
	## --- Noobie Process --- ##
	working_dir = Config.DOWN_PATH + "/WatermarkAdder/"
	if not os.path.exists(working_dir):
		os.makedirs(working_dir)
	watermark_path = Config.DOWN_PATH + "/" + str(cmd.from_user.id) + "/thumb.jpg"
	if not os.path.exists(watermark_path):
		await cmd.reply_text("You Didn't Set Any Watermark!\n\nSend any JPG or PNG Picture ...")
		return
	file_type = cmd.video or cmd.document
	if not file_type.mime_type.startswith("video/"):
		await cmd.reply_text("This is not a Video!")
		return
	status = Config.DOWN_PATH + "/WatermarkAdder/status.json"
	if os.path.exists(status):
		await cmd.reply_text("Sorry, Currently I am busy with another Task!\n\nTry Again After Sometime!")
		return
	preset = Config.PRESET
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
	position_tag = None
	watermark_position = await db.get_position(cmd.from_user.id)
	if watermark_position == "5:main_h-overlay_h":
		position_tag = "Bottom Left"
	elif watermark_position == "main_w-overlay_w-5:main_h-overlay_h-5":
		position_tag = "Bottom Right"
	elif watermark_position == "main_w-overlay_w-5:5":
		position_tag = "Top Right"
	elif watermark_position == "5:5":
		position_tag = "Top Left"
	else:
		position_tag = "Top Left"
		watermark_position = "5:5"
	await editable.edit(f"Trying to Add Watermark to the Video at {position_tag} Corner ...\n\nPlease Wait!")
	duration = 0
	metadata = extractMetadata(createParser(the_media))
	if metadata.has("duration"):
		duration = metadata.get('duration').seconds
	the_media_file_name = os.path.basename(the_media)
	main_file_name = os.path.splitext(the_media_file_name)[0]
	output_vid = main_file_name + "_[" + str(cmd.from_user.id) + "]_[" + str(time.time()) + "]_[@AbirHasan2005]" + ".mp4"
	progress = Config.DOWN_PATH + "/WatermarkAdder/" + str(cmd.from_user.id) + "/progress.txt"
	try:
		# WOW! Nice XD
		# Meh Always NOOB
		output_vid = await vidmark(the_media, editable, progress, watermark_path, output_vid, duration, logs_msg, status, preset, watermark_position)
	except Exception as err:
		print(f"Unable to Add Watermark: {err}")
		await editable.edit("Unable to add Watermark!")
		await logs_msg.edit(f"#ERROR: Unable to add Watermark!\n\n**Error:** `{err}`")
		await delete_all()
		return
	if output_vid == None:
		await editable.edit("Something went wrong!")
		await logs_msg.edit("#ERROR: Something went wrong!")
		await delete_all()
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

@AHBot.on_message(filters.command("cancel") & filters.private)
async def CancelWatermarkAdder(bot, cmd):
	if not await db.is_user_exist(cmd.from_user.id):
		await db.add_user(cmd.from_user.id)
		await bot.send_message(
			Config.LOG_CHANNEL,
			f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
		)
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

@AHBot.on_message(filters.private & filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply)
async def broadcast_(c, m):
	all_users = await db.get_all_users()
	broadcast_msg = m.reply_to_message
	while True:
	    broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
	    if not broadcast_ids.get(broadcast_id):
	        break
	out = await m.reply_text(
	    text = f"Broadcast Started! You will be notified with log file when all the users are notified."
	)
	start_time = time.time()
	total_users = await db.total_users_count()
	done = 0
	failed = 0
	success = 0
	broadcast_ids[broadcast_id] = dict(
	    total = total_users,
	    current = done,
	    failed = failed,
	    success = success
	)
	async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
	    async for user in all_users:
	        sts, msg = await send_msg(
	            user_id = int(user['id']),
	            message = broadcast_msg
	        )
	        if msg is not None:
	            await broadcast_log_file.write(msg)
	        if sts == 200:
	            success += 1
	        else:
	            failed += 1
	        if sts == 400:
	            await db.delete_user(user['id'])
	        done += 1
	        if broadcast_ids.get(broadcast_id) is None:
	            break
	        else:
	            broadcast_ids[broadcast_id].update(
	                dict(
	                    current = done,
	                    failed = failed,
	                    success = success
	                )
	            )
	if broadcast_ids.get(broadcast_id):
	    broadcast_ids.pop(broadcast_id)
	completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
	await asyncio.sleep(3)
	await out.delete()
	if failed == 0:
	    await m.reply_text(
	        text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
	        quote=True
	    )
	else:
	    await m.reply_document(
	        document='broadcast.txt',
	        caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
	        quote=True
	    )
	await os.remove('broadcast.txt')

@AHBot.on_message(filters.private & filters.command("status"))
async def sts(c, m):
	msg_text = None
	status = Config.DOWN_PATH + "/WatermarkAdder/status.json"
	if os.path.exists(status):
		msg_text = "Sorry, Currently I am busy with another Task!"
	else:
		msg_text = "I am Free Now!\nSend me any video to add Watermark."
	if int(m.from_user.id) == Config.OWNER_ID:
		total_users = await db.total_users_count()
		msg_text += f"\n\n**Total Users in DB:** `{total_users}`"
	await m.reply_text(text=msg_text, parse_mode="Markdown", quote=True)

@AHBot.on_callback_query()
async def button(bot, cmd: CallbackQuery):
	# Meh Lazy AF ...
	cb_data = cmd.data

	if "refreshmeh" in cb_data:
		if Config.UPDATES_CHANNEL:
			invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
			try:
				user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.message.chat.id)
				if user.status == "kicked":
					await cmd.message.edit(
						text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
						parse_mode="markdown",
						disable_web_page_preview=True
					)
					return
			except UserNotParticipant:
				await cmd.message.edit(
					text="**You Still Didn't Join ☹️, Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
					reply_markup=InlineKeyboardMarkup(
						[
							[
								InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
							],
							[
								InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
							]
						]
					),
					parse_mode="markdown"
				)
				return
			except Exception:
				await cmd.message.edit(
					text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		await cmd.message.edit(
			text=Config.USAGE_WATERMARK_ADDER,
			parse_mode="Markdown",
			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Developer", url="https://t.me/AbirHasan2005"), InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")], [InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")]]),
			disable_web_page_preview=True
		)

	elif "lol" in cb_data:
		await cmd.answer("Sir, that button not works XD\n\nPress Bottom Buttons to Set Position of Watermark!", show_alert=True)

	elif cb_data.startswith("position_"):
		if Config.UPDATES_CHANNEL:
			invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
			try:
				user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.message.chat.id)
				if user.status == "kicked":
					await cmd.message.edit(
						text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
						parse_mode="markdown",
						disable_web_page_preview=True
					)
					return
			except UserNotParticipant:
				await cmd.message.edit(
					text="**You Still Didn't Join ☹️, Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
					reply_markup=InlineKeyboardMarkup(
						[
							[
								InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
							],
							[
								InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
							]
						]
					),
					parse_mode="markdown"
				)
				return
			except Exception:
				await cmd.message.edit(
					text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		await bot.send_message(chat_id=Config.LOG_CHANNEL, text=f"#SETTINGS_SET: [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) Changed Settings!\n\nUser ID: #id{cmd.from_user.id}", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ban User", callback_data=f"ban_{cmd.from_user.id}")]]))
		new_position = cb_data.split("_", 1)[1]
		await db.set_position(cmd.from_user.id, new_position)
		position_tag = None
		watermark_position = await db.get_position(cmd.from_user.id)
		if watermark_position == "5:main_h-overlay_h":
			position_tag = "Bottom Left"
		elif watermark_position == "main_w-overlay_w-5:main_h-overlay_h-5":
			position_tag = "Bottom Right"
		elif watermark_position == "main_w-overlay_w-5:5":
			position_tag = "Top Right"
		elif watermark_position == "5:5":
			position_tag = "Top Left"
		else:
			position_tag = "Top Left"
		await cmd.message.edit(
			text="Here you can set your Watermark Settings:",
			disable_web_page_preview=True,
			parse_mode="Markdown",
			reply_markup=InlineKeyboardMarkup(
				[
					[InlineKeyboardButton(f"Watermark Position - {position_tag}", callback_data="lol")],
					[InlineKeyboardButton("Set Bottom Left", callback_data=f"position_5:main_h-overlay_h"), InlineKeyboardButton("Set Bottom Right", callback_data=f"position_main_w-overlay_w-5:main_h-overlay_h-5")],
					[InlineKeyboardButton("Set Top Right", callback_data=f"position_main_w-overlay_w-5:5"), InlineKeyboardButton("Set Top Left", callback_data=f"position_5:5")]
				]
			)
		)

	elif cb_data.startswith("ban_"):
		if Config.UPDATES_CHANNEL == None:
			await cmd.answer("Sorry Sir, You didn't Set any Updates Channel!", show_alert=True)
			return
		try:
			user_id = cb_data.split("_", 1)[1]
			await bot.kick_chat_member(chat_id=Config.UPDATES_CHANNEL, user_id=int(user_id))
			await cmd.answer("User Banned from Updates Channel!")
		except Exception as e:
			await cmd.answer(f"Can't Ban Him!\n\nError: {e}")

AHBot.run()