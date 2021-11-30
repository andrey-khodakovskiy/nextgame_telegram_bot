import logging
from decouple import config
from bs4 import BeautifulSoup
import requests
import emoji


logger = logging.getLogger(__name__)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[console],
)


FLARESOLVERR_SERVICE = config("FLARESOLVERR_SERVICE")
EXCLAMATION = emoji.emojize(":red_exclamation_mark:")

nextgame_request = {
    "cmd": "request.get",
    "url": "https://lfl.ru/club5",
    "session": "100",
    "maxTimeout": 60000,
}

create_session_request = {"cmd": "sessions.create", "session": "100"}
clear_sessions_request = {"cmd": "sessions.destroy", "session": "100"}


def create_session():
    try:
        logger.warning("Clearing sessions")
        result = requests.post(
            f"http://{FLARESOLVERR_SERVICE}:8191/v1", json=clear_sessions_request
        )
        logger.warning(result)
        logger.warning("Creating session")
        result = requests.post(
            f"http://{FLARESOLVERR_SERVICE}:8191/v1", json=create_session_request
        )
        logger.warning(result)

    except Exception as ex:
        logger.error(ex)


def get_info():
    try:
        keys = ["tour", "date", "home", "time", "guest", "stadium"]
        data = requests.post(
            f"http://{FLARESOLVERR_SERVICE}:8191/v1", json=nextgame_request
        )
        data = data.json()
        output = data["solution"]["response"]

        soup = BeautifulSoup(output, "lxml")
        result = soup.find("h3", string="Ближайшие матчи")
        result = result.find_parent("div", class_="cont fortable")
        result = list(result.stripped_strings)
        result_dict = {key: value for key, value in zip(keys, result[2:8])}
    except Exception as ex:
        logger.error(ex)
        result_dict = "Exception"

    return result_dict


def get_text(result):
    text = f"{result['tour']}: {result['home']} - {result['guest']}\n{result['time']} {result['date']}\n"
    if not "Октябрь" in result["stadium"]:
        text += f"{EXCLAMATION} "
    text += f"{result['stadium']}"

    return text
