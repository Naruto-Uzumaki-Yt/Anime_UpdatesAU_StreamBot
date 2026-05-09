
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
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# =========================
# RENDER PORT
# =========================

ENV PORT=10000

# =========================
# START BOT + SERVER
# =========================

CMD gunicorn server:app --workers 1 --threads 1 --bind 0.0.0.0:$PORT & python bot.py

# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #
