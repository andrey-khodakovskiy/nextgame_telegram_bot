FROM python:3.8.6
WORKDIR /nextgame-bot
COPY . .
RUN pip install -r requirements.txt
CMD python nextgame_bot.py