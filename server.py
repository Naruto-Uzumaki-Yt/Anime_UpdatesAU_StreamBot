# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

from flask import Flask, Response, request, render_template_string
from pyrogram import Client
from database import get_file
import config

app = Flask(__name__)

tg = Client("stream",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN)
tg.start()

@app.route("/stream/<key>")
def stream(key):
    file = get_file(key)
    if not file:
        return "Invalid"

    video_url = f"/video/{key}"

    lang_btn = ""
    for l in file["langs"]:
        lang_btn += f'<a class="btn" href="/play/{key}/{l}">{l.upper()}</a>'

    tracks = ""
    for i, (lang, _) in enumerate(file["subs"].items()):
        tracks += f'<track kind="subtitles" src="/sub/{key}/{lang}" srclang="{lang}" label="{lang.upper()}" {"default" if i==0 else ""}>'

    return render_template_string(f"""
<html>
<head>
<meta name="viewport" content="width=device-width">

<link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet"/>
<script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>

<style>
body {{background:#0d0d0d;color:white;margin:0}}
.top {{background:#111;padding:10px}}
.btn {{display:block;background:#00c853;padding:10px;margin:5px;color:white;text-align:center;text-decoration:none}}
</style>

</head>
<body>

<div class="top">📺 {config.CHANNEL_USERNAME}</div>

<video id="player" class="video-js" controls preload="metadata" width="100%">
<source src="{video_url}" type="video/mp4">
{tracks}
</video>

<a class="btn" href="{video_url}">⬇️ Download</a>

<div>
<h3>🎧 Languages</h3>
{lang_btn}
</div>

<div>
<a class="btn" href="{config.CHANNEL_LINK}">Updates</a>
<a class="btn" href="{config.DEV_LINK}">Developer</a>
</div>

</body>
</html>
""")

@app.route("/video/<key>")
def video(key):
    file = get_file(key)
    range_header = request.headers.get('Range')

    async def gen(start=0):
        async for chunk in tg.stream_media(file["file_id"], offset=start):
            yield chunk

    if range_header:
        start = int(range_header.replace("bytes=", "").split("-")[0])
        return Response(gen(start), status=206,
                        content_type="video/mp4",
                        headers={"Accept-Ranges": "bytes"})
    else:
        return Response(gen(),
                        content_type="video/mp4",
                        headers={"Accept-Ranges": "bytes"})

@app.route("/play/<key>/<lang>")
def play(key, lang):
    file = get_file(key)
    if lang in file["langs"]:
        file["file_id"] = file["langs"][lang]
    return stream(key)

@app.route("/sub/<key>/<lang>")
def sub(key, lang):
    file = get_file(key)
    if lang not in file["subs"]:
        return "No subtitle"
    return Response(file["subs"][lang], content_type="text/vtt")

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
