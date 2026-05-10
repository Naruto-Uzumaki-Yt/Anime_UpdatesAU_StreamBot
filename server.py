# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

from flask import Flask, Response, render_template_string, request
from pyrogram import Client
from database import get_file, get_subtitles
import config
import os

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

<title>Anime_UpdatesAU Stream</title>

</head>

<body>

<!-- ========================= HEADER ========================= -->

<div class="topbar">

    <div class="logo">
        Anime_UpdatesAU
    </div>

    <div class="menu-btn">
        ☰
    </div>

</div>

<!-- ========================= HERO TEXT ========================= -->

<div class="hero">

    <h1>
        Stream Effortlessly,
        <span>Anytime, Anywhere</span>
    </h1>

</div>

<!-- ========================= VIDEO PLAYER ========================= -->

<div class="player-box">

    <video
        id="player"
        class="video-js vjs-default-skin"
        controls
        preload="auto"
        playsinline
        width="100%"
        height="240"
        data-setup='{{}}'>

        <source src="{video_url}">

        {tracks}

    </video>

</div>

<!-- ========================= FILE CARD ========================= -->

<div class="card">

    <h2>{file["file_name"]}</h2>

    <div class="streaming">
        🔴 Now Streaming
    </div>

    <!-- DOWNLOAD -->

    <a class="download-btn" href="{video_url}">
        ⬇️ Download
    </a>

    <!-- VLC -->

    <a class="player-btn"
       href="vlc://{config.BASE_URL}/video/{key}">
       🟠 VLC Player
    </a>

    <!-- MX PLAYER -->

    <a class="player-btn"
       href="intent:{config.BASE_URL}/video/{key}#Intent;package=com.mxtech.videoplayer.ad;end">
       🔵 MX Player
    </a>

    <!-- PLAYit -->

    <a class="player-btn"
       href="intent:{config.BASE_URL}/video/{key}#Intent;package=com.playit.videoplayer;end">
       ▶️ PLAYit
    </a>

    <!-- KM PLAYER -->

    <a class="player-btn"
       href="intent:{config.BASE_URL}/video/{key}#Intent;package=com.kmplayer;end">
       🟣 KMPlayer
    </a>

</div>

<!-- ========================= WARNING ========================= -->

<div class="warning">

⚠️ Browser may not support some MKV audio codecs.<br>
Use VLC or MX Player for best experience.

</div>

<!-- ========================= CHANNELS ========================= -->

<div class="section">

    <h1>Explore Our Universe</h1>

    <p>
        Discover our channels and intelligent bots
    </p>

</div>

<div class="card">

    <h2>Our Channels</h2>

    <a class="player-btn"
       href="{config.CHANNEL_LINK}">
       📢 Anime_UpdatesAU
    </a>

</div>

<!-- ========================= BOTS ========================= -->

<div class="card">

    <h2>Our Bots</h2>

    <a class="player-btn"
       href="{config.DEV_LINK}">
       🤖 Stream Bot
    </a>

</div>

<!-- ========================= FOOTER ========================= -->

<div class="footer">

© 2026 Anime_UpdatesAU. All Rights Reserved.

</div>

<!-- ========================= CSS ========================= -->

<style>

body{
    background:#050816;
    color:white;
    font-family:sans-serif;
    margin:0;
    padding:0;
}

.topbar{
    background:#020617;
    padding:18px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.logo{
    font-size:32px;
    font-weight:bold;
    color:#ff6b57;
}

.menu-btn{
    font-size:30px;
}

.hero{
    padding:20px;
}

.hero h1{
    font-size:32px;
    line-height:1.3;
}

.hero span{
    color:#ff7b00;
}

.player-box{
    padding:15px;
}

video{
    width:100%;
    border-radius:20px;
}

.card{
    background:#091227;
    margin:15px;
    padding:20px;
    border-radius:20px;
}

.card h2{
    font-size:26px;
    word-break:break-word;
}

.streaming{
    background:#2a1020;
    color:#ff4f7b;
    padding:12px;
    border-radius:12px;
    display:inline-block;
    margin-bottom:20px;
}

.download-btn{
    display:block;
    text-decoration:none;
    background:#ff1654;
    color:white;
    text-align:center;
    padding:16px;
    border-radius:14px;
    margin-top:15px;
    font-size:22px;
    font-weight:bold;
}

.player-btn{
    display:block;
    text-decoration:none;
    background:#1c2740;
    color:white;
    padding:16px;
    border-radius:14px;
    margin-top:15px;
    font-size:22px;
    text-align:center;
}

.warning{
    color:#ffd54f;
    padding:20px;
    font-size:20px;
    text-align:center;
}

.section{
    padding:20px;
}

.section h1{
    font-size:40px;
    color:#ff6b57;
}

.section p{
    font-size:22px;
    color:#ccc;
}

.footer{
    text-align:center;
    padding:30px;
    color:#aaa;
    font-size:18px;
}

</style>

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

    file_path = tg.download_media(file["file_id"])

    def generate():

        with open(file_path, "rb") as f:

            while True:

                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                yield chunk

    return Response(
        generate(),
        headers={
            "Content-Type": "video/x-matroska",
            "Accept-Ranges": "bytes",
            "Content-Disposition": f'inline; filename="{file["file_name"]}"'
        }
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
