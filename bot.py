# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
import config
import uuid
from database import (
    save_file,
    add_subtitle
)

app = Client(
    "bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# STORE LAST FILE KEY
LAST_FILES = {}

# ================= FORCE SUB ================= #

async def check_join(client, user_id):

    try:
        member = await client.get_chat_member(
            config.CHANNEL_USERNAME,
            user_id
        )

        return True

    except UserNotParticipant:
        return False

    except:
        return True

# ================= START ================= #

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):

    await message.reply_text(f"""
👋 Welcome to {config.CHANNEL_USERNAME}

📥 Send Video/File
🎬 Get Stream Link
🌐 Watch Online
⬇️ Download Directly

📢 Updates:
{config.CHANNEL_LINK}
""")

# ================= FILE HANDLER ================= #

@app.on_message(
    filters.private &
    (filters.video | filters.document)
)
async def file_handler(client, message):

    if not await check_join(client, message.from_user.id):

        return await message.reply(
            f"🚫 Join Updates Channel First:\n{config.CHANNEL_LINK}"
        )

    file = message.video or message.document

    if not file.file_name:
        return await message.reply("❌ File name missing")

    key = str(uuid.uuid4())[:8]

    save_file(
        key,
        file.file_id,
        file.file_name,
        file.file_size
    )

    # SAVE LAST FILE
    LAST_FILES[message.from_user.id] = key

    size = round(file.file_size / (1024 ** 3), 2)

    stream_link = f"{config.BASE_URL}/stream/{key}"
    download_link = f"{config.BASE_URL}/video/{key}"

    await message.reply_text(f"""
📁 {file.file_name}

📦 Size: {size} GB

🎬 Stream Link:
{stream_link}

⬇️ Download Link:
{download_link}
""")

# ================= SUBTITLE HANDLER ================= #

@app.on_message(
    filters.private &
    filters.document
)
async def subtitle_handler(client, message):

    file = message.document

    if not file.file_name:
        return

    name = file.file_name.lower()

    if not (
        name.endswith(".srt") or
        name.endswith(".vtt")
    ):
        return

    key = LAST_FILES.get(message.from_user.id)

    if not key:
        return await message.reply(
            "❌ Send video first"
        )

    path = await message.download()

    def srt_to_vtt(text):

        lines = text.splitlines()

        out = ["WEBVTT\n"]

        for line in lines:

            if "-->" in line:
                line = line.replace(",", ".")

            out.append(line)

        return "\n".join(out)

    with open(
        path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        content = f.read()

    if name.endswith(".srt"):
        content = srt_to_vtt(content)

    # DETECT SUBTITLE LANGUAGE
    if "eng" in name:
        lang = "en"

    elif "hin" in name:
        lang = "hi"

    elif "jap" in name:
        lang = "jp"

    else:
        lang = "sub"

    add_subtitle(
        key,
        lang,
        content
    )

    await message.reply(
        "✅ Subtitle Added Successfully"
    )

# ================= RUN ================= #

app.run()

# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #
