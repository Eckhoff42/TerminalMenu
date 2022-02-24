# UiO menu checker 
This is a commandline tool used to check todays menu at all SiO restaurants. The tool should be able to handle restaurants being added/removed as long as they follow the same structure on the page.

## How to run the program
Download the repo:
```Bash
git@github.com:Eckhoff42/TerminalMenu.git
```

Navigate into to the file `main.py`
```bash
cd TerminalMenu
```

Run the program
```bash
python3 main.py "<restaurant name>"
# to se the list of SiO restaurants run 
python3 main.py -l
# to get help use the command
python3 main.py -h
```

## Demo:
[![asciicast](https://asciinema.org/a/88oVkPmHu09XairqPRvdveRtw.svg)](https://asciinema.org/a/88oVkPmHu09XairqPRvdveRtw)

## implementation
The script is written in python using `BeautifulSoup`.
1. The website "https://www.sio.no/mat-og-drikke/spisesteder-og-kaffebarer" is fetched
2. Using BeautifulSoup the each div containing a restaurant is found.
3. Name of restaurant, menu headings and menu is found for each restaurant
4. The result is added to a 2d dictionary. The structure is described below
5. An argparser is used to parse the user-query

*result dictionary structure*
```json
{
  "restaurant_1" : {"title_1" : "text_1", "title_2": "text_2"},
  "restaurant_2" : {"title_3": "text_3"},
  "restaurant_3" : {} //this restaurant has no menu
}
```
