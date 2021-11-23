import cloudscraper
from bs4 import BeautifulSoup
import requests
import emoji


EXCLAMATION = emoji.emojize(":red_exclamation_mark:")


def get_info():
    # with open(
    #     "test_pages/game_no.html", "r", encoding="windows-1251", errors="ignore"
    # ) as f:
    #     data = f.read()

    try:
        keys = ["tour", "date", "home", "time", "guest", "stadium"]
        scraper = cloudscraper.create_scraper()
        data = scraper.get("https://lfl.ru/club5").text
        data.encoding = "windows-1251"
        soup = BeautifulSoup(data, "lxml")
        print(soup)
        result = soup.find("h3", string="Ближайшие матчи")
        print(result)
        result = result.find_parent("div", class_="cont fortable")
        result = list(result.stripped_strings)
        result_dict = {key: value for key, value in zip(keys, result[2:8])}
    except Exception as ex:
        print(ex)
        result_dict = "Exception"

    return result_dict


def get_text(result):
    text = f"{result['tour']}: {result['home']} - {result['guest']}\n{result['time']} {result['date']}\n"
    if not "Октябрь" in result["stadium"]:
        text += f"{EXCLAMATION} "
    text += f"{result['stadium']}"

    return text
