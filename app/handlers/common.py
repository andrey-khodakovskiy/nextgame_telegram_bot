import asyncio
from datetime import datetime, timedelta
from aiogram import Dispatcher, types
from decouple import config

from app.functions.functions import get_info, get_text

ADMIN = config("ADMIN", cast=int)


async def nextgame(message: types.Message) -> None:
    result = get_info()

    if result == "Exception":
        await message.answer("Что-то пошло не так")
        return

    if not result or result["time"] == "00:01":
        text = "Время игры пока неизвестно"
    else:
        text = get_text(result)

    await message.answer(text)


async def start(message: types.Message) -> None:
    if not message.from_user.id == ADMIN:
        await message.answer("Извините, вы не можете выполнить данную команду.\nВоспользуйтесь командой /nextgame")
        return

    old_result = {}
    old_nextgame_text, old_training_text = "", ""
    nextgame_message, training_message = None, None

    while True:
        result = get_info()
        now = datetime.now()
        tomorrow = datetime.today() + timedelta(days=1)
        training_text = f"Тренировка\nчетверг 21:30 {tomorrow.strftime('%d.%m.%y')}"

        if result and result != "Exception" and result != old_result and result["time"] != "00:01":
            nextgame_text = get_text(result)
            old_result = result
            nextgame_text = "<u>ОБНОВЛЕНИЕ:</u>\n" + nextgame_text
            await message.answer(nextgame_text)

        if datetime.weekday(now) == 2 and now.hour > 19:
            if result and result != "Exception" and result["time"] != "00:01":
                nextgame_text = get_text(result)
                if nextgame_text != old_nextgame_text and not "- -" in nextgame_text:
                    if nextgame_message:
                        await nextgame_message.unpin()

                    nextgame_message = await message.answer_poll(
                        question=nextgame_text, options=["Буду", "Не буду", "Приеду посмотреть"], is_anonymous=False
                    )
                    await nextgame_message.pin(disable_notification=False)
                    old_nextgame_text = nextgame_text

            if training_text != old_training_text:
                if training_message:
                    await training_message.unpin()
                training_message = await message.answer_poll(
                    question=training_text,
                    options=["Буду", "Не буду"],
                    is_anonymous=False,
                )
                await training_message.pin(disable_notification=False)
                old_training_text = training_text

        await asyncio.sleep(1800)


def register_handlers_common(dp: Dispatcher) -> None:
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(nextgame, commands="nextgame")
