# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

from flask import Flask, Response, render_template_string, request
from pyrogram import Client
from database import get_file, get_subtitles
import config
import asyncio

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024 * 1024

tg = Client(
    "stream",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

tg.start()

# ========================= STREAM PAGE ========================= #

@app.route("/stream/<key>")
def stream(key):

    file = get_file(key)

    if not file:
        return "Invalid File"

    video_url = f"/video/{key}"

    subs = get_subtitles(key)

    tracks = ""

    for i, (lang, _) in enumerate(subs.items()):

        tracks += f"""
        <track
            kind="subtitles"
            src="/sub/{key}/{lang}"
            srclang="{lang}"
            label="{lang.upper()}"
            {"default" if i == 0 else ""}
        >
        """

    return render_template_string(f"""

<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet"/>
<script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>

<style>

body {{
    background: #0d0d0d;
    color: white;
    margin: 0;
    font-family: sans-serif;
}}

.top {{
    background: #111;
    padding: 15px;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
}}

.banner img {{
    width: 100%;
}}

.container {{
    padding: 10px;
}}

.btn {{
    display: block;
    background: #00c853;
    padding: 12px;
    margin-top: 10px;
    color: white;
    text-align: center;
    text-decoration: none;
    border-radius: 8px;
    font-weight: bold;
}}

.footer {{
    margin-top: 20px;
}}

video {{
    width: 100%;
    border-radius: 10px;
}}

</style>

</head>

<body>

<div class="top">
📺 {config.CHANNEL_USERNAME}
</div>

<div class="banner">
<img src="{config.THUMB_URL}">
</div>

<div class="container">

<video
id="player"
class="video-js vjs-default-skin"
controls
preload="auto"
playsinline
data-setup='{{}}'>

<source src="{video_url}" type="video/mp4">

{tracks}

</video>

<a class="btn" href="{video_url}">
⬇️ Download
</a>

<div class="footer">

<a class="btn" href="{config.CHANNEL_LINK}">
📢 Updates Channel
</a>

<a class="btn" href="{config.DEV_LINK}">
👨‍💻 Developer
</a>

</div>

</div>

<script>
var player = videojs('player');
</script>

</body>
</html>

""")

# ========================= VIDEO STREAM ========================= #

@app.route("/video/<key>")
def video(key):

    file = get_file(key)

    if not file:
        return "Invalid File"

    range_header = request.headers.get("Range", None)

    file_size = file.get("file_size", 0)

    start = 0
    end = file_size - 1

    if range_header:

        range_value = range_header.replace("bytes=", "")

        start = int(range_value.split("-")[0])

        if "-" in range_value:
            end_part = range_value.split("-")[1]
            if end_part:
                end = int(end_part)

    chunk_size = end - start + 1

    async def stream_generator():

        async for chunk in tg.stream_media(
            file["file_id"],
            offset=start
        ):
            yield chunk

    def generate():

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        agen = stream_generator()

        while True:

            try:
                chunk = loop.run_until_complete(
                    agen.__anext__()
                )

                yield chunk

            except StopAsyncIteration:
                break

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(chunk_size),
        "Content-Type": "video/mp4"
    }

    return Response(
        generate(),
        status=206,
        headers=headers
    )

# ========================= SUBTITLE ========================= #

@app.route("/sub/<key>/<lang>")
def sub(key, lang):

    subs = get_subtitles(key)

    if lang not in subs:
        return "No Subtitle"

    return Response(
        subs[lang],
        content_type="text/vtt"
    )

# ========================= HOME ========================= #

@app.route("/")
def home():
    return "Anime Updates AU Stream Bot Running"

# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #
