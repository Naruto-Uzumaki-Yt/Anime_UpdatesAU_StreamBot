# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD gunicorn server:app --bind 0.0.0.0:$PORT & python bot.py

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
