"""
Task requirements:

    Create a command line program to check the search results for the page:
    https://yousician.com/songs

    ● The program should take a string to search with as an input argument.
    ● The program should then use the search with the given string, and get all the search results (a list of songs with song and artist name).
    ● It should then print all the found songs in alphabetical order, sorted primarily by the artist name, and then by the song name.
    ● If any error is encountered (e.g., the user does not have an internet connection), the program should print an error message instead and exit.


"""

from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def accept_cookies():
    sleep(10)
    try:
        driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
    except NoSuchElementException:
        pass


def find_song(query: str):
    search_string = driver.find_element(
        By.XPATH, '//*[@class="SearchInput__Input-sc-1o849ds-2 gmQnaU"]'
    )
    search_string.clear()
    search_string.send_keys(query)
    search_string.send_keys(Keys.ENTER)
    sleep(5)

    return driver.find_elements(
        By.XPATH,
        '//*[@class="TableCell-sc-4sgq1o-0 align-left SongsTable__SongCell-sc-1fm48ej-1 iJEBjs"]',
    )


def retrieve_data(result_of_search: List) -> List[Tuple]:
    songs, artists = [], []

    for i in range(0, len(result_of_search), 2):
        if result_of_search[i].text != "Song":
            songs.append(result_of_search[i].text)

    for i in range(1, len(result_of_search), 2):
        if result_of_search[i].text != "Made Famous By":
            artists.append(result_of_search[i].text)

    zipped = zip(songs, artists)
    sorted_list = sorted(zipped, key=lambda t: t[1])

    return sorted_list


def has_connection(url):
    try:
        requests.get(url, timeout=5, verify=False)
        return True
    except (requests.ConnectionError, requests.Timeout) as e:
        return False


if __name__ == "__main__":
    url = "https://yousician.com/songs"
    driver = webdriver.Chrome()
    if not has_connection(url):
        print("Check your internet connection")
        driver.quit()
        exit(1)
    else:
        while True:
            driver.get(url)
            accept_cookies()
            search_query = input("Please enter the name of the song or artist: \n")
            print(f"You entered {search_query}")
            print("--------Searching--------")
            raw_result = find_song(search_query)
            if raw_result:
                result = retrieve_data(raw_result)
                print(f"{len(result)} songs found !")
                for song, artist in result:
                    print(f"Artist: {artist} ---> song: {song}")
            else:
                print("There are no results.")
            _ = input("Enter any key for a new search and 'n' for exit: \n")
            if _ == "n":
                print("Have a good day.")
                break
