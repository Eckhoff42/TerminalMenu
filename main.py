import argparse
from termcolor import colored
import requests
from bs4 import BeautifulSoup
import re


def get_menu_from_restaurant(place):
    # dictinary of heading and contents
    menu_book = {}

    # find the title of the restaurant
    header = place.find("div", {"class": "panel-heading tableview"})
    title_span = header.find("span", {"class": "maintitle"})
    title = re.findall(r'<.*?\>(.+)<\/span>', str(title_span))[0]

    # find the menu
    body = place.find("div", {"class": "panel-body"})
    menu_div = body.find("div", {"class": "dagensmiddag"})
    if menu_div == None:
        return title, {}

    # find heading
    headers = menu_div.findAll("h4")
    header_titles = []
    header_titles = list(map(lambda x: re.findall(
        r'\<h4\>(.+)?\<\/h4\>', str(x))[0], headers))

    # find content
    menus = menu_div.find_all("ul")
    menu_titles = list(map(lambda x: re.findall(
        r'<li>(.+?)\<\/li\>', str(x))[0], menus))

    # add combination of heading and contents to menu_book
    for pair in zip(header_titles, menu_titles):
        menu_book[pair[0]] = pair[1]

    return title, menu_book


def get_menus(url):
    # GET the page
    result = requests.get(url)
    assert result.status_code == 200

    # create BeautifulSoup with the result
    src = result.content
    document = BeautifulSoup(src, 'lxml')

    # get list of all restaurant-divs
    panel_container = document.find("div", {"id": "ptaccordion"})
    panels = panel_container.find_all("div", {"class": "panel panel-default"})

    # dictionary of results: {restauntName: {heading1: "description", heading2: "description"}, ....}
    restaurants = {}

    for place in panels:
        title, book = get_menu_from_restaurant(place)
        restaurants[title] = book

    return restaurants


def printRestaurants(res):
    print(f'|{"Name": <48}|{"Menu": <11}|')
    print(f'|{"****": <48}|{"****": <11}|')
    for title in res.keys():
        hasMenu = colored("No menu", 'red')
        if (res[title] != {}):
            hasMenu = colored("Found menu", "blue")

        print(f'|{title: <48}|{hasMenu: <20}|')


def printMenu(title, menu):
    print("****", title, "****")
    if (menu == {}):
        print("There is no menu")
    else:
        for heading in menu.keys():
            print(heading, ":", menu[heading])


if __name__ == "__main__":
    url = "https://www.sio.no/mat-og-drikke/spisesteder-og-kaffebarer"
    res = get_menus(url)

    parser = argparse.ArgumentParser(
        description='Get todays menu at a SiO restaurants',
        usage="python3 main.py <'restaurant name'>")

    # Add the arguments
    parser.add_argument('Restaurant',
                        metavar='restaurant',
                        type=str,
                        nargs='?',
                        help='name of restaurant')
    parser.add_argument('-l', '--list', action='store_true',
                        help="list all restaurants")

    args = parser.parse_args()
    if (args.list):
        printRestaurants(res)
    elif (args.Restaurant != None and args.Restaurant in res):
        printMenu(args.Restaurant, res[args.Restaurant])
    else:
        print("Restaurant does not exist. Try 'python3 main.py -l' to see a list of restaurants")
