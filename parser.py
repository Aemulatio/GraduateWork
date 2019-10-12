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
    id = 0
    for element in elements:
        """Get data about each game."""
        if "first" in element["class"]:
            id = id + 1
        teams = []
        score = []
        date = element.find("div", class_="time").text.replace('/', '-')
        teams_ = element.find_all("td", class_="team-col")
        for t in teams_:
            teams.append(t.find("a").text)
            score.append(t.find("span", class_="score").text.strip().replace(
                ')', '').replace('(', ''))
        # score = element.find_all("td", class_="score")
        playedMap = element.find("div", class_="dynamic-map-name-full").text
        event = element.find("td", class_="event-col").text
        data.append([id, date, teams, score, playedMap, event])

    prev = 1
    current = 0
    finalData = []
    t1 = str()  # left team
    t2 = str()  # right team
    s1 = int()  # left team score
    s2 = int()  # right team score

    for match in data:
        if prev != current:
            t1 = match[2][0]  # left team
            t2 = match[2][1]  # right team
            s1 = 0  # left team score to 0
            s2 = 0  # right team score to 0

        current = match[0]

        if prev == current:  # if prev id == cur id
            if t1 == match[2][0]:  # if teams doesnt switch sides in statistic
                if match[3][0] > match[3][1]:  # if t1 > t2
                    s1 = s1 + 1
                else:   # if t2 > t1
                    s2 = s2 + 1
            else:
                if match[3][1] > match[3][0]:  # if t2 > t1
                    s2 = s2 + 1
                else:   # if t1 > t2
                    s1 = s1 + 1
        else:
            prev = current
    return data[0][3]
    # сделать счет
    # сделать компановку по матчам
    #
    #
    #

# def create_csv(url):
    ###
    ###


url = "https://www.hltv.org/stats/matches?startDate=2018-10-09&endDate=2019-10-09&offset=100"

# print(len(get_all_elements(url)))
print(get_data(url))
