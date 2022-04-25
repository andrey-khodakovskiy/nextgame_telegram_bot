import asyncio
from aiogram import Dispatcher, types
from decouple import config
from prometheus_client import Counter

from app.functions.functions import get_info, get_text, create_session

ADMIN = config("ADMIN", cast=int)
requests_total = Counter(
    "nextgame_requests_counter", "Nextgame requests counter", ["method"]
)
requests_total.labels("human")
requests_total.labels("auto")


async def nextgame(message: types.Message) -> None:
    result = get_info()
    requests_total.labels("human").inc(1)

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
        await message.answer(
            "Извините, вы не можете выполнить данную команду.\nВоспользуйтесь командой /nextgame"
        )
        return

    times = 0
    old_result = {}
    while True:
        if times == 48:
            create_session()
            times = 0

        result = get_info()
        requests_total.labels("auto").inc(1)

        if (
            result
            and result != "Exception"
            and result != old_result
            and result["time"] != "00:01"
        ):
            old_result = result
            text = get_text(result)
            text = "<u>ОБНОВЛЕНИЕ:</u>\n" + text
            await message.answer(text)

        times += 1
        await asyncio.sleep(1800)


def register_handlers_common(dp: Dispatcher) -> None:
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(nextgame, commands="nextgame")
