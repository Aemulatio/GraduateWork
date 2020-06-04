from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
import re
import urllib.request
import shutil


# from urllib import request


def csv_reader(path):
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


def lets_parse(files):
    data = pd.read_csv("Data/results1_wo_garbage_NTN.csv")
    UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
    del data
    html = ''
    for file in files:
        f = open(file, "r", encoding="UTF-8")
        html += f.read()
        f.close()
    soup = BeautifulSoup(html, 'lxml')
    del html
    teams_logo = list()
    for team in UniqueTeams[1:]:
        print(team)
        # print(soup.find_all('a', href=re.compile(team.replace(' ', '%20'))))
        if len(soup.find_all('a', href=re.compile(team.replace(' ', '%20')))) > 0:
            for match in soup.find_all('a', href=re.compile(team.replace(' ', '%20'))):
                print(match)
                # matches.append("https://www.hltv.org" + match.attrs['href'])
                # print(match.attrs['href'])
                # print("https://www.hltv.org" + match.attrs['href'])
                r = requests.get("https://www.hltv.org" + match.attrs['href'])
                print(r.url)
                # match_to_open = request.urlopen("https://www.hltv.org" + match.attrs['href'])
                nested_soup = BeautifulSoup(r.text, 'lxml')
                # print(nested_soup)

                if nested_soup.find('div', {'class': 'match-info-box'}):
                    match_info_block = nested_soup.find('div', {'class': 'match-info-box'})
                    for img in match_info_block.find_all('img', {'class': 'team-logo'}):
                        if img.attrs['alt'] == team:
                            print(img.attrs['src'])
                            resp = requests.get(img.attrs['src'], stream=True)
                            local_file = open('static/imgs/logos/' + team + '.jpg', 'wb')
                            resp.raw.decode_content = True
                            shutil.copyfileobj(resp.raw, local_file)
                            del resp
                            local_file.close()
                else:
                    img = nested_soup.find('img', {'class': 'context-item-image'})
                    print(img)
                    if img.attrs['alt'] == team:
                        print(img.attrs['src'])
                        resp = requests.get(img.attrs['src'], stream=True)
                        local_file = open('static/imgs/logos/' + team + '.jpg', 'wb')
                        resp.raw.decode_content = True
                        shutil.copyfileobj(resp.raw, local_file)
                        del resp
                        local_file.close()

                        # teams_logo.append(img.attrs['src'])
                        # urllib.request.urlretrieve(img.attrs['src'], 'static/imgs/logos/' + team + ".webp")
                    # print(img)
                break
                # continue
                # if 'href' in match:
                #     print(match)

    # for img in soup.find_all('img'):
    #     print(img)


if __name__ == '__main__':
    lets_parse(['Data/pages19-20.html', 'Data/pages20.html'])

    pass
