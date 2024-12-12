import requests
from bs4 import BeautifulSoup

#based off of pybirthdayscraper from PyPi but updated solely the getPeople(date) method.

def get_birthday(person):
    name_cleaned = person.lower().replace(" ", "-").replace("'", "-")

    url = "https://www.famousbirthdays.com/people/" + name_cleaned + ".html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    main_div = soup.find("div", {"class": "stat box"})

    try:
        month = main_div.find("span", {"class": "hidden-sm"})
        day = main_div.find("a")
        year = main_div.find_all("a")

        result = person + "'s Birthday is on: " + \
            month.text.strip() + " " + day.text[-2:] + ", " + year[-1].text


        return result
    except:
        error_message = "Sorry! " + person + " is not in our database..."
        return error_message
        #print("Sorry!", person, "is not in our database...")

def get_people(date):
        clean_date = date.lower().replace(" ", "")
        url = "https://www.famousbirthdays.com/" + clean_date + ".html"
        print(f"URL being accessed: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        print(f"Response status code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')

        # Print the first part of the HTML to see the structure
        print("HTML structure:")
        print(soup.prettify()[:1000])  # Print first 1000 characters of HTML

        try:
            # Try finding people cards (adjust these selectors based on the HTML we see)
            people = soup.find_all("div", {"class": ["person-card", "famous-person", "profile-card"]})
            if not people:
                # Try alternative selectors if the above doesn't work
                people = soup.find_all("div", {"data-type": "person"})

            print(f"Number of people found: {len(people) if people else 0}")

            if not people:
                return "Sorry! That does not look like a valid date..."

            result = []
            for person in people:
                # Try different ways to get the name based on the HTML
                name_elem = person.find("div", {"class": "name"}) or \
                            person.find("h2") or \
                            person.find("a", {"class": "name"})

                if name_elem:
                    name = name_elem.text.strip()
                    print(f"Found name: {name}")
                    result.append(name)

            return result
        except Exception as e:
            print(f"Error occurred: {e}")
            return "Sorry! That does not look like a valid date..."

    # Test the function
if __name__ == "__main__":
    date = "December 12"
    print(f"Testing with date: {date}")
    result = get_people(date)
    print("\nResults:")
    print(result)

def search_by_profession(profession, limit=5):
    profession_cleaned = profession.lower().replace(" ", "")
    url = "https://www.famousbirthdays.com/profession/" + profession_cleaned + ".html"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        title = soup.find("title").text
        if "Page Not Found" in title:
            error_message = "Sorry! The profession " + profession + \
                            " is not in our database!"
            return error_message
        else:
            people = soup.find_all("div", {"class": "name"})
            result_list = list()
            for i in range(int(limit)):
                data = people[i].text
                person = data.split(",")[0]
                result = get_birthday(person.strip())
                result_list.append(result)

            return result_list
    except:
        error_message = "Sorry! " + profession + " is not in our database..."
        return error_message
        # print("Sorry!", profession, "is not in our database...")

def search_by_birthsign(birth_sign, limit=5):
    birth_sign_cleaned = birth_sign.lower()
    url = "https://www.famousbirthdays.com/astrology/" + birth_sign_cleaned + ".html"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("title").text
    if "Page Not Found" in title:
        error_message = "Sorry! The birth sign " + birth_sign + \
                        " doesn't exist! Please check if your spelling is correct."
        return error_message
    else:
        people = soup.find_all("div", {"class": "name"})

        result_list = list()

        for i in range(int(limit)):
            try:
                data = people[i].text
            except:
                break
            person = data.split(", ")[0]
            result = get_birthday(person.strip())
            result_list.append(result)

        return result_list

    # def main():

    #     welcome = '''Welcome to pyBirthdays! Select one of the following options:
    #     (1) Enter a famous person's name
    #     (2) Enter a date
    #     (3) Enter a profession and a desired number of records to be returned
    #     (4) Enter a birth sign and a desired number of records to be returned'''

    #     print(welcome)

    #     option = input()

    #     if option == "1":
    #         name = input("Enter a famous person's name to see their birthday: ")
    #         result = get_birthday(name)
    #         return result
    #     elif option == "2":
    #         date = input("Enter a date (Month Day): ")
    #         result = get_people(date)
    #         return result
    #     elif option == "3":
    #         profession = input("Enter a profession: ")
    #         limit = input("Enter the desired number of records: ")
    #         result = search_by_profession(profession, limit)
    #         return result
    #     elif option == "4":
    #         birth_sign = input("Enter a birth sign from the following 12: " +
    #                            "Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius and Pisces.\n")
    #         limit = input("Enter the desired number of records: ")
    #         result = search_by_birthsign(birth_sign, limit)
    #         return result

    # result = main()

    # if isinstance(result, list):
    #     for elem in result:
    #         print(elem)
    # else:
    #     print(result)
