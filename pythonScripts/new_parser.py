from bs4 import BeautifulSoup
import requests
import time
import csv
import hashlib


def setCache(data: str) -> str:
    """
    Хэширует строку data по алгоритму MD5

    :param data: Строка для хэширования
    :return: Захэшированную в MD5 строку
    """
    hash_result = hashlib.md5(data.encode()).hexdigest()
    return hash_result


def parse(url: str, outPutFile: str, attr: str = 'a'):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "pragma": 'no-cache',
        "cache-control": "no-cache",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "cookie": "CookieConsent={stamp:%27/iFeOz/wnfocVsfOloyCZGDBUppd7M6E1eceKMjQySF6mGHlsx+DGg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cver:1%2Cutc:1616914016722%2Cregion:%27ru%27}; _ga=GA1.2.36646224.1634998534; _gid=GA1.2.2001879148.1634998534; MatchFilter={%22active%22:false%2C%22live%22:false%2C%22stars%22:1%2C%22lan%22:false%2C%22teams%22:[]}; _pbjs_userid_consent_data=6683316680106290; _lr_geo_location=RU; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22d2047997-ef87-4ba1-bed6-b251a4919cab%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-09-23T14%3A15%3A39%22%7D; sharedid=%7B%22id%22%3A%2201FJPR3NAQRENC21NTC8NPJ478%22%2C%22ts%22%3A1634998538926%7D; cto_bundle=zToV4l9uR2xMZlhsRG95ZSUyRkxVTUg5a01Ha0M2SyUyRm4ySmVzTHFKYzNocVFzcHFRU0lRNVliSEhrWWNXc2FQNldvcUNiWHVkVkdPc2FOSXBRc2JLZWFxRVNQWVltVHByUktETTh1YTdBU1I2ODh1MWRUaUJjbG5WJTJGZm1Kc0dDMkM0MmZmUk9QRE10NyUyRlE2NnglMkZpQ3o2ZjdlOSUyRmclM0QlM0Q; _ia__v4=%7B%22v%22%3A3%2C%22r%22%3A%22RU%22%2C%22sportsbook%22%3A%5B0%2C1%5D%7D; pbjs-id5id=%7B%22created_at%22%3A%222021-10-23T14%3A15%3A33Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*rGk8vAlFomWD2PVavpahlzmh0B5vsoNiGC51qQspJqYAAAh3_mOmco5vwuApR3VG%22%2C%22universal_uid%22%3A%22ID5*Hf1nsQVBi-AOQNFLAijbPfC0doYJAyPQgDolhiSFTJcAAF2WidzBTU2HuAAaWPJu%22%2C%22signature%22%3A%22ID5_Abe7-LsG5eqPJjeERPs1m6bkEGXRwEPl3M1muPSevaednZHtjcc106J6mG7SbD1H61VMe0Ebx3G5KJ5fG0vxCGg%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%7D; pbjs-id5id_last=Sun%2C%2024%20Oct%202021%2007%3A29%3A42%20GMT; _lr_retry_request=true; _gat=1; outbrain_cid_fetch=true"
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:  # 200 - ok
        # создаем или открываем имеющейся файл для записи/доплнения
        f = open("../Data/New/" + outPutFile, attr, encoding="UTF-8")
        html = r.text  # код текущей страницы в переменную
        soup = BeautifulSoup(html, features='html.parser')  # объект BS
        # Если есть таблица с классами
        if soup.find('table', class_='stats-table matches-table no-sort') is not None:
            # пишем тбоди
            f.write(str(soup.find('table', class_='stats-table matches-table no-sort').find('tbody')))
            f.write("\n")
        # Иначе
        else:
            # Записываем текущую ссылку
            f.write(str(r.url))
        # Если нет ссылки на следующую выборку, то просто закрываем файл
        if not soup.find('div', class_='pagination-component pagination-top with-stats-table') \
                .find('a', class_='pagination-next').has_attr('href'):
            f.close()
        else:
            # Иначе, закрываем файл, получаем ссылку дальше и делаем рекурсию, через 3 секунды
            f.close()
            href = soup.find('div', class_='pagination-component pagination-top with-stats-table') \
                .find('a', class_='pagination-next')['href']
            print(href)
            time.sleep(3)
            parse("https://www.hltv.org" + href, outPutFile, 'a')
    else:
        # Отладочный момент, чтобы знать какая ошибка произошла
        print(r.status_code)


def parseFile(fileName: str, outPutFileName: str, ser: int = 0) -> int:
    pages_src = list()
    f = open("../Data/New/" + fileName, "r", encoding="UTF-8")
    if f:
        soup = BeautifulSoup(f, 'html.parser')
        pages_src.append(soup.find_all('tbody'))
        # print(len(soup.find_all('tbody')))
        data = list()
        series = ser
        for pageSrc in soup.find_all('tbody'):
            # print(str(pageSrc) + "\n")
            for tr in pageSrc.find_all('tr'):  # reversed(....) сзаду-наперед
                """Get data about each game."""
                teams = []
                score = []
                # TODO: надо получать ссылку из первой ячейки, переходить в нее, и получать состав команд на текущий матч
                if "first" in tr["class"]:
                    series = series + 1
                date = tr.find('div', class_='time').text.replace('/', '-')
                teams_ = tr.find_all("td", class_="team-col")
                for t in teams_:
                    if t.find("a") is None:
                        break
                    teams.append(t.find("a").text)
                    score.append(t.find("span", class_="score").text.strip().replace(
                        ')', '').replace('(', ''))
                if tr.find("div", class_="dynamic-map-name-full") is None:
                    print(tr)
                    break
                played_map = tr.find("div", class_="dynamic-map-name-full").text
                event = tr.find("td", class_="event-col").text
                data.append((date, teams, score, played_map, event, series))

        data = list(reversed(data))  # reverse data, from old to new, instead of new-old

        """Create a .csv file."""
        with open("../Data/New/" + outPutFileName, "w", newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['Date', 'Teams', 'Score', 'Map', 'Event', 'Series'])
            for line in data:
                writer.writerow(line)
        print(fileName + " done!")

        return series


def parseFile_new(fileName: str, outPutFileName: str, ser: int = 0) -> int:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "pragma": 'no-cache',
        "cache-control": "no-cache",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "cookie": "CookieConsent={stamp:%27/iFeOz/wnfocVsfOloyCZGDBUppd7M6E1eceKMjQySF6mGHlsx+DGg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cver:1%2Cutc:1616914016722%2Cregion:%27ru%27}; _ga=GA1.2.36646224.1634998534; _gid=GA1.2.2001879148.1634998534; MatchFilter={%22active%22:false%2C%22live%22:false%2C%22stars%22:1%2C%22lan%22:false%2C%22teams%22:[]}; _pbjs_userid_consent_data=6683316680106290; _lr_geo_location=RU; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22d2047997-ef87-4ba1-bed6-b251a4919cab%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-09-23T14%3A15%3A39%22%7D; sharedid=%7B%22id%22%3A%2201FJPR3NAQRENC21NTC8NPJ478%22%2C%22ts%22%3A1634998538926%7D; cto_bundle=zToV4l9uR2xMZlhsRG95ZSUyRkxVTUg5a01Ha0M2SyUyRm4ySmVzTHFKYzNocVFzcHFRU0lRNVliSEhrWWNXc2FQNldvcUNiWHVkVkdPc2FOSXBRc2JLZWFxRVNQWVltVHByUktETTh1YTdBU1I2ODh1MWRUaUJjbG5WJTJGZm1Kc0dDMkM0MmZmUk9QRE10NyUyRlE2NnglMkZpQ3o2ZjdlOSUyRmclM0QlM0Q; _ia__v4=%7B%22v%22%3A3%2C%22r%22%3A%22RU%22%2C%22sportsbook%22%3A%5B0%2C1%5D%7D; pbjs-id5id=%7B%22created_at%22%3A%222021-10-23T14%3A15%3A33Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*rGk8vAlFomWD2PVavpahlzmh0B5vsoNiGC51qQspJqYAAAh3_mOmco5vwuApR3VG%22%2C%22universal_uid%22%3A%22ID5*Hf1nsQVBi-AOQNFLAijbPfC0doYJAyPQgDolhiSFTJcAAF2WidzBTU2HuAAaWPJu%22%2C%22signature%22%3A%22ID5_Abe7-LsG5eqPJjeERPs1m6bkEGXRwEPl3M1muPSevaednZHtjcc106J6mG7SbD1H61VMe0Ebx3G5KJ5fG0vxCGg%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%7D; pbjs-id5id_last=Sun%2C%2024%20Oct%202021%2007%3A29%3A42%20GMT; _lr_retry_request=true; _gat=1; outbrain_cid_fetch=true"
    }
    pages_src = list()
    f = open("../Data/New/" + fileName, "r", encoding="UTF-8")
    if f:
        print("opened")
        soup = BeautifulSoup(f, 'html.parser')
        # print('souped')
        # pages_src.append(soup.find_all('tbody')) #мб нужно, но не понять зачем
        # print(len(soup.find_all('tbody')))
        data = list()
        series = ser
        for pageSrc in soup.find_all('tbody'):
            # print(str(pageSrc) + "\n")
            for tr in pageSrc.find_all('tr'):  # reversed(....) сзаду-наперед
                """Get data about each game."""
                url = 'https://hltv.org' + tr.find('td', class_='date-col').find('a')['href']
                print(url)
                r = requests.get(url, headers=headers)
                teamsPlayers = []  # составы команд
                if (r.status_code == 200):  # если страничка загрузилась, то ок
                    html = r.text  # код текущей страницы в переменную
                    soup2 = BeautifulSoup(html, features='html.parser')  # объект BS
                    for table in soup2.find_all('table',
                                                class_='stats-table'):  # обходим все таблички с результатми матча
                        teamPlayers = []
                        teamPlayers.append(table.find('th', class_='st-teamname').text)  # пишем название команды
                        for player in table.select('tbody tr td.st-player a'):  # обходим всех игроков
                            teamPlayers.append(player.text)  # пишем ник игрока
                        teamsPlayers.append(teamPlayers)
                        del teamPlayers
                # print(teamsPlayers)
                else:
                    print("Вернулась не 200")
                    print(r.status_code)
                    break
                print("-----------------------------------")

                # print(tr)
                # print(tr.find('td', class_='date-col').find('a')['href'])
                # time.sleep(1)
                # teams = []
                score = []
                if "first" in tr["class"]:
                    series = series + 1
                date = tr.find('div', class_='time').text.replace('/', '-')
                teams_ = tr.find_all("td", class_="team-col")
                for t in teams_:
                    if t.find("a") is None:
                        break
                    # teams.append(t.find("a").text)
                    score.append(t.find("span", class_="score").text.strip().replace(')', '').replace('(', ''))
                if tr.find("div", class_="dynamic-map-name-full") is None:
                    print(tr)
                    break
                played_map = tr.find("div", class_="dynamic-map-name-full").text
                event = tr.find("td", class_="event-col").text
                data.append((date, teamsPlayers[0], teamsPlayers[-1], score, played_map, event, series))
        #
        data = list(reversed(data))  # reverse data, from old to new, instead of new-old

        # """Create a .csv file."""
        with open("../Data/New/" + outPutFileName, "w", newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['Date', 'Team1', 'Team2', 'Score', 'Map', 'Event', 'Series'])
            for line in data:
                writer.writerow(line)
        print(fileName + " done!")

        return series


def first_preps():
    """Первичный парсинг"""
    print("-----------------")
    url = 'https://www.hltv.org/stats/matches?startDate=2018-01-01&endDate=2018-12-31'
    parse(url, 'csgo2018.html', "w")
    print("-----------------")
    url = 'https://www.hltv.org/stats/matches?startDate=2019-01-01&endDate=2019-12-31'
    parse(url, 'csgo2019.html', "w")
    print("-----------------")
    url = 'https://www.hltv.org/stats/matches?startDate=2020-01-01&endDate=2020-12-31'
    parse(url, 'csgo2020.html', "w")
    print("-----------------")
    url = 'https://www.hltv.org/stats/matches?startDate=2021-01-01&endDate=2021-12-31'
    parse(url, 'csgo2021.html', "w")
    print("-----------------")


if __name__ == '__main__':
    # first_preps()
    # url = 'https://www.hltv.org/stats/matches?startDate=2019-01-01&endDate=2019-12-31'
    # parse(url, 'csgo2019.html', "w")
    # ser = parseFile("csgo2018.html", 'rawData18.csv')
    # ser = parseFile("csgo2019.html", 'rawData19.csv', ser)
    # parseFile("csgo2020.html", 'rawData20.csv', ser)
    # print(setCache("123"))

    # parseFile_new("csgo2018.html", 'rawData18_newFormat.csv')
    # print("file done")
    # parseFile_new("csgo2019.html", 'rawData19_newFormat.csv')
    # print("file done")
    # parseFile_new("csgo2020.html", 'rawData20_newFormat.csv')
    # print("file done")

    url = 'https://www.hltv.org/stats/matches?startDate=2021-01-01&endDate=2021-12-31'
    parse(url, 'csgo2021.html', "w")
    print("-----------------")
    parseFile_new("csgo2021.html", 'rawData21_newFormat.csv')
    print("file done")

