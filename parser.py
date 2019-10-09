from bs4 import BeautifulSoup
import requests
import csv


def get_html(url):
    r = requests.get(url)
    return r.text if r.status_code == 200 else "Error"

def get_DOM(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    # return soup.find('table', class_='stats-table')
    return soup.find_all('tr')

def get_all_elements(url):
    tbl = get_DOM(url)
    tbl.pop(0)
    elements = []    
    for tr in tbl:
        elements.append(tr)
    return elements

def get_data(url):  #rename later
     # тут выделение каждого элемента из массива элементс
     #
     #
     #
     #

# def create_csv(url):
    ###
    ###


url = "https://www.hltv.org/stats/matches?startDate=2018-10-09&endDate=2019-10-09&offset=100"

print(get_all_elements(url))


# html_doc = urlopen('http://otus.ru').read()
# soup = BeautifulSoup(html_doc)
# print soup
