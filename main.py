from distutils.filelist import findall
from tkinter import Menu
import requests
from bs4 import BeautifulSoup
import re
url = "https://www.sio.no/mat-og-drikke/spisesteder-og-kaffebarer"

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
    # find the title of the restaurant
    header = place.find("div", {"class": "panel-heading tableview"})
    title_span = header.find("span", {"class": "maintitle"})
    title = re.findall(r'<.*?\>(.+)<\/span>', str(title_span))[0]

    # dictinary of heading and contents
    menu_book = {}
    restaurants[title] = menu_book

    # find the menu
    body = place.find("div", {"class": "panel-body"})
    menu_div = body.find("div", {"class": "dagensmiddag"})
    if menu_div == None:
        continue

    # find heading
    headers = menu_div.findAll("h4")
    header_titles = []
    for h in headers:
        header_titles.append(re.findall(r'\<h4\>(.+)?\<\/h4\>', str(h))[0])
    # header_titles = map(lambda x: print("x er", x) and
    #                     re.findall(r'\<h4\>(.+)?\<\/h4\>', str(x))[0], headers)

    # find content
    menus = menu_div.find_all("ul")
    menu_titles = []
    for m in menus:
        m_title = re.findall(r'<li>(.+?)\<\/li\>', str(m))[0]
        menu_titles.append(m_title)

    # TODO: convert to map
    # menu_titles = map(re.findall(r'<li>(.+?)\<\/li\>',
    #                   str(menus[0])), list(menus))

    # add combination of heading and contents to menu_book
    for pair in zip(header_titles, menu_titles):
        menu_book[pair[0]] = pair[1]


print(restaurants)
