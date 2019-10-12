from bs4 import BeautifulSoup
import requests
import csv


def get_html(url):
    """Return html code, if 200 has been returned."""
    r = requests.get(url)
    return r.text if r.status_code == 200 else "Error"


def get_DOM(url):
    """Return all tr from the page."""
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    # return soup.find('table', class_='stats-table')
    return soup.find_all('tr')


def get_all_elements(url):
    """Write all tr in massive."""
    tbl = get_DOM(url)
    tbl.pop(0)
    elements = []
    for tr in tbl:
        elements.append(tr)
    return elements


def get_data(url):  # rename later
    """####"""
    elements = get_all_elements(url)
    data = []
    for element in elements:
        teams = []
        score = []
        date = element.find("div", class_="time").text.replace('/', '-')
        teams_ = element.find_all("td", class_="team-col")        
        for t in teams_:
            teams.append(t.find("a").text)
            score.append(t.find("span", class_ = "score").text.strip().replace(')', '').replace('(', '')) 
        # score = element.find_all("td", class_="score")
        playedMap = element.find("div", class_="dynamic-map-name-full").text
        event = element.find("td", class_="event-col").text
        data.append([date, str(teams), str(score), playedMap, event])
    return data
    # тут выделение каждого элемента из массива элементс
    # сделать компановку по матчам
    #
    #
    #

# def create_csv(url):
    ###
    ###


url = "https://www.hltv.org/stats/matches?startDate=2018-10-09&endDate=2019-10-09&offset=100"

print(get_data(url))


# html_doc = urlopen('http://otus.ru').read()
# soup = BeautifulSoup(html_doc)
# print soup
