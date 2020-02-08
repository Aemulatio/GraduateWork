from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sqlite3


def parse(url):
    """DOCUMENTE THIS"""
    r = requests.get(url)
    if r.status_code == 200:
        driver = webdriver.Chrome()
        driver.get(url)
        pagesSrc = list()
        while True:
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            pagesSrc.append(soup.find('table',
                                      class_='stats-table matches-table no-sort').find('tbody'))
            go_right = driver.find_element_by_class_name("pagination-next")

            if not soup.find('div', class_='pagination-component pagination-top with-stats-table') \
                    .find('a', class_='pagination-next').has_attr('href'):
                # if pagination-next то сначала в конец, если pagination-prev то с конца в начало
                driver.quit()
                break
            go_right.send_keys(Keys.RETURN)

        data = list()
        for pageSrc in pagesSrc:
            for tr in pageSrc.find_all('tr'):  # reversed(....) сзаду-наперед
                """Get data about each game."""
                teams = []
                score = []
                date = tr.find('div', class_='time').text.replace('/', '-')
                teams_ = tr.find_all("td", class_="team-col")
                for t in teams_:
                    teams.append(t.find("a").text)
                    score.append(t.find("span", class_="score").text.strip().replace(
                        ')', '').replace('(', ''))
                played_map = tr.find("div", class_="dynamic-map-name-full").text
                event = tr.find("td", class_="event-col").text
                data.append((date, teams, score, played_map, event))

        # """Create a .csv file."""
        # with open('1234.csv', "w", newline='', encoding='utf-8') as csv_file:
        #     writer = csv.writer(csv_file, delimiter=',')
        #     writer.writerow(['Date', 'Teams', 'Score', 'Map', 'Event'])
        #     for line in data:
        #         writer.writerow(line)

        data = list(reversed(data))  # reverse data, from old to new, instead of new-old

        """Insert it all in DB instead of .csv file"""
        conn = sqlite3.connect('DataBase/DataBase.sqlite')
        c = conn.cursor()

        # Create table
        if c.execute('''SELECT count(*) FROM rawData''') != 0:
            c.execute('''DELETE FROM rawData''')
        c.execute('''CREATE TABLE IF NOT EXISTS rawData
                     (date text, teams text,score text, map text,event text)''')
        # Insert a row of data
        for line in data:
            c.execute('''INSERT INTO rawData(date, teams, score, map, event) VALUES (?,?,?,?,?)''',
                      (str(line[0]), str(line[1]), str(line[2]), str(line[3]), str(line[4])))
        # Save (commit) the changes
        conn.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()


url = 'https://www.hltv.org/stats/matches?startDate=2019-01-01&endDate=2020-12-31'
# url = 'https://www.hltv.org/stats/matches?startDate=2019-01-01&endDate=2019-02-31' #temp line, delete later. It just for tests

parse(url)
