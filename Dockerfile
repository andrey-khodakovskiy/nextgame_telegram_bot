FROM python:3.8.6
WORKDIR /nextgame-bot
COPY ./requirements.txt .
RUN pip install -r requirements.txt
ENV ADMIN="<>"
ENV BOT_TOKEN="<>"
COPY . .
CMD python nextgame_bot.py
