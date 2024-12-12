import os
from datetime import datetime, date
from dotenv import load_dotenv
from atproto import Client
import requests
from bs4 import BeautifulSoup

load_dotenv()


def get_celebrity_birthdays():
    today = date.today()
    month = today.strftime('%B').lower()
    day = str(today.day)
    url = f"https://www.famousbirthdays.com/{month}{day}.html"

    print(f"URL accessed: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        celebrity_tiles = soup.find_all("div", class_="tile__item")

        if not celebrity_tiles:
            return None

        celebrities = []
        for tile in celebrity_tiles[:3]:
            name_elem = tile.find("p", class_="type-16-18-small")
            profession_elem = tile.find("p", class_="tile__description")

            if name_elem:
                name = name_elem.text.strip()
                profession = profession_elem.text.strip() if profession_elem else ""
                celebrities.append(f"{name} ({profession})")

        if celebrities:
            birthday_text = ", \n• ".join(celebrities)
            return f"🎂Happy birthday to \n• {birthday_text}"

        return None

    except Exception as e:
        print(f"Error fetching birthdays: {e}")
        return None


def post_to_bluesky():
    username = os.getenv('BLUESKY_USERNAME')
    password = os.getenv('BLUESKY_PASSWORD')

    client = Client()
    client.login(username, password)

    day_of_year = datetime.now().timetuple().tm_yday
    birthday_celebs_elem = get_celebrity_birthdays()


    if birthday_celebs_elem:
        full_post = f"(Today is the {day_of_year} day of the year.)\n{birthday_celebs_elem}"
    else:
        full_post = f"(Today is the {day_of_year} day of the year)\n\n"

    try:
        response = client.send_post(text=full_post)
        print("posting successful!")
        print(f"post URI: {response.uri}")
        if birthday_celebs_elem:
            print(f"successfully added birthdays to post:")
            print(birthday_celebs_elem)
    except Exception as e:
        print(f"Error posting: {e}")


if __name__ == "__main__":
    birthdays = get_celebrity_birthdays()
    if birthdays:
        print("\n birthday message posted to feed:")
        print(birthdays)
    else:
        print("no celebrity birthdays found for today")

    post_to_bluesky()
