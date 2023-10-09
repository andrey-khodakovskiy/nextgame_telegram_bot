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


EXCLAMATION = emoji.emojize(":red_exclamation_mark:")
nextgame_url = "https://lfl.ru/club5"


def get_info():
    try:
        keys = ["tour", "date", "home", "time", "guest", "stadium"]
        data = requests.get(nextgame_url, verify=False)
        data.encoding = "Windows-1251"

        soup = BeautifulSoup(data.text, "lxml")
        result = soup.find("h3", string="Ближайшие матчи")
        result = result.find_parent("div", class_="cont fortable")
        result = list(result.stripped_strings)
        result_dict = {key: value for key, value in zip(keys, result[2:8])}
        print(result_dict)
    except Exception as ex:
        logger.error(ex)
        result_dict = "Exception"

    return result_dict


def get_text(result):
    text = f"{result['tour']}: {result['home']} - {result['guest']}\n{result['time']} {result['date']}\n"
    if (not "Октябрь" in result["stadium"]) or ("Красный" in result["stadium"]):
        text += f"{EXCLAMATION} "
    text += f"{result['stadium']}"

    return text
