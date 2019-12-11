from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time


def parse(url):
    '''DOCUMENTE THIS'''
    r = requests.get(url)
    if r.status_code == 200:
        driver = webdriver.Chrome()
        driver.get(url)
        pagesSrc = []
        while True:
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            pagesSrc.append(soup.find('table',
                                      class_='stats-table matches-table no-sort').find('tbody'))
            goLeft = driver.find_element_by_class_name("pagination-prev")  

            if not soup.find('div', class_='pagination-component pagination-top with-stats-table').find('a', class_='pagination-prev').has_attr('href'):
                driver.quit()
                break
            goLeft.send_keys(Keys.RETURN)
        # pageSrc =
        print(pagesSrc)

# def get_html(url):
#     """Return html code, if 200 has been returned."""
#     r = requests.get(url)
#     return r.text if r.status_code == 200 else "Error"


# def get_DOM(url):
#     """Return all tr from the page."""
#     html = get_html(url)
#     soup = BeautifulSoup(html, 'lxml')
#     return soup.find_all('tr')


# def get_all_elements(url):
#     """Write all tr in massive."""
#     tbl = get_DOM(url)
#     tbl.pop(0)
#     elements = []
#     for tr in tbl:
#         elements.append(tr)
#     return elements


# def get_inner_data(url):
#     """Return data of each match."""
#     elements = get_all_elements(url)
#     data = []
#     id = 0
#     for element in elements:
#         """Get data about each game."""
#         if "first" in element["class"]:
#             id = id + 1
#         teams = []
#         score = []
#         date = element.find("div", class_="time").text.replace('/', '-')
#         teams_ = element.find_all("td", class_="team-col")
#         for t in teams_:
#             teams.append(t.find("a").text)
#             score.append(t.find("span", class_="score").text.strip().replace(
#                 ')', '').replace('(', ''))
#         playedMap = element.find("div", class_="dynamic-map-name-full").text
#         event = element.find("td", class_="event-col").text
#         data.append([id, date, teams, score, playedMap, event])
#     return data


# def get_systemized_data(url):
#     """Systemize data of each series."""

#     data = get_inner_data(url)

#     prev = 1
#     current = 0
#     finalData = []
#     t1 = str()  # left team
#     t2 = str()  # right team
#     s1 = int()  # left team score
#     s2 = int()  # right team score
#     event = str()  # event
#     date = str()  # date of match
#     for match in data:
#         if prev != current:
#             t1 = match[2][0]  # left team
#             t2 = match[2][1]  # right team
#             s1 = 0  # left team score to 0
#             s2 = 0  # right team score to 0
#             event = match[-1]
#             date = match[1]

#         current = match[0]
#         if prev == current:  # if prev id == cur id
#             if t1 == match[2][0]:  # if teams doesnt switch sides in statistic
#                 if int(match[3][0]) > int(match[3][1]):  # if t1 > t2
#                     s1 = s1 + 1
#                 else:  # if t2 > t1
#                     s2 = s2 + 1
#             else:
#                 if int(match[3][1]) > int(match[3][0]):  # if t2 > t1
#                     s1 = s1 + 1
#                 else:   # if t1 > t2
#                     s2 = s2 + 1

#         else:
#             finalData.append([t1, s1, t2, s2, date, event])
#             t1 = match[2][0]  # left team
#             t2 = match[2][1]  # right team
#             s1 = 0  # left team score to 0
#             s2 = 0  # right team score to 0
#             event = match[-1]
#             date = match[1]
#             prev = current

#             if prev == current:  # if prev id == cur id
#                 if t1 == match[2][0]:  # if teams doesnt switch sides in statistic
#                     if int(match[3][0]) > int(match[3][1]):  # if t1 > t2
#                         s1 = s1 + 1
#                     else:  # if t2 > t1
#                         s2 = s2 + 1
#                 else:
#                     if int(match[3][1]) > int(match[3][0]):  # if t2 > t1
#                         s1 = s1 + 1
#                     else:   # if t1 > t2
#                         s2 = s2 + 1

#     finalData.append([t1, s1, t2, s2, date, event])
#     return finalData


# def create_csv(url):
#     """Create a .csv file."""
#     data = get_systemized_data(url)
# # normal name
#     with open('123.csv', "w", newline='', encoding='utf-8') as csv_file:
#         writer = csv.writer(csv_file, delimiter=',')
#         writer.writerow(['Team 1', 'Score 1', 'Team 2',
#                          'Score 2', 'Date', 'Event'])
#         for line in data:
#             writer.writerow(line)


url = 'https://www.hltv.org/stats/matches?startDate=2019-01-01&endDate=2019-12-31&offset=14510'

parse(url)
# url = "https://www.hltv.org/stats/matches?startDate=2018-10-09&endDate=2019-10-09&offset=49"

# create_csv(url)
