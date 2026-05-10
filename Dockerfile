# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

FROM python:3.10-slim

# =========================
# WORK DIRECTORY
# =========================

WORKDIR /app

# =========================
# COPY FILES
# =========================

COPY . /app

# =========================
# INSTALL DEPENDENCIES
# =========================

RUN apt-get update && apt-get install -y \
    gcc \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# =========================
# RENDER PORT
# =========================

ENV PORT=10000

# =========================
# START BOT + SERVER
# =========================

CMD python bot.py & gunicorn server:app --worker-class gevent --workers 1 --bind 0.0.0.0:$PORT
# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #
