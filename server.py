# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

from flask import Flask, Response, render_template_string
from pyrogram import Client
from database import get_file, get_subtitles
import config

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024 * 1024

tg = Client(
    "stream",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

tg.start()

@app.route("/stream/<key>")
def stream(key):

    file = get_file(key)

    if not file:
        return "Invalid"

    video_url = f"/video/{key}"

    subs = get_subtitles(key)

    tracks = ""

    for i, (lang, _) in enumerate(subs.items()):
        tracks += f'''
        <track kind="subtitles"
        src="/sub/{key}/{lang}"
        srclang="{lang}"
        label="{lang.upper()}"
        {"default" if i == 0 else ""}
        >
        '''

    return render_template_string(f"""

<html>

<head>

<meta name="viewport" content="width=device-width">

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
width="100%"
height="240"
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

</body>
</html>

""")

@app.route("/video/<key>")
async def video(key):

    file = get_file(key)

    if not file:
        return "Invalid File"

    async def generate():

        async for chunk in tg.stream_media(file["file_id"]):
            yield chunk

    return Response(
        generate(),
        content_type="video/mp4",
        headers={
            "Accept-Ranges": "bytes"
        }
    )

@app.route("/sub/<key>/<lang>")
def sub(key, lang):

    subs = get_subtitles(key)

    if lang not in subs:
        return "No subtitle"

    return Response(
        subs[lang],
        content_type="text/vtt"
    )

# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #
