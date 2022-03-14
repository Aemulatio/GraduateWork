from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time
import hashlib
from datetime import datetime


def setCache(data: str) -> str:
    """
    Хэширует строку data по алгоритму MD5

    :param data: Строка для хэширования
    :return: Захэшированную в MD5 строку
    """
    hash_result = hashlib.md5(data.encode()).hexdigest()
    return hash_result


def getLastDocument() -> str:
    """
    Получает хэш последней обработанной строки

    :return: Хэш полученной строки
    """

    db = client.Diploma
    collection = db.hash
    data = ''
    for obj in collection.find().sort('date', -1).limit(1):
        data = obj['hash']

    client.close()
    return data


def checkHash(hash: str) -> bool:
    """
    Проверяет хэш в БД
    :param hash: Хэш для проверки
    :return: Возвращает True/False если найдет
    """

    db = client.Diploma
    collection = db.hash
    for obj in collection.find({'hash': hash}):
        return True
    return False


def writeHash(hash: str):
    """
    Пишет хэш в БД
    :param hash: Хэш
    :return:
    """
    db = client.Diploma
    collection = db.hash
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    collection.insert_one({
        "hash": hash,
        "dateTime": dt_string
    })


def writeData(
        winner: str,
        team1: str,
        team1_p1: str,
        team1_p2: str,
        team1_p3: str,
        team1_p4: str,
        team1_p5: str,
        team2: str,
        team2_p1: str,
        team2_p2: str,
        team2_p3: str,
        team2_p4: str,
        team2_p5: str,
        map: str,
):
    """
    Запись в таблицу Stats

    :param winner:
    :param team1:
    :param team1_p1:
    :param team1_p2:
    :param team1_p3:
    :param team1_p4:
    :param team1_p5:
    :param team2:
    :param team2_p1:
    :param team2_p2:
    :param team2_p3:
    :param team2_p4:
    :param team2_p5:
    :param map:
    :return:
    """
    db = client.Diploma
    collection = db.Stats  # вроде статс
    collection.insert_one(
        {"winner": winner,
         "team1": team1,
         "team1_p1": team1_p1,
         "team1_p2": team1_p2,
         "team1_p3": team1_p3,
         "team1_p4": team1_p4,
         "team1_p5": team1_p5,
         "team2": team2,
         "team2_p1": team2_p1,
         "team2_p2": team2_p2,
         "team2_p3": team2_p3,
         "team2_p4": team2_p4,
         "team2_p5": team2_p5,
         "map": map})


def autoStart():
    """
    Записывает в БД старт
    :return:
    """
    db = client.Diploma
    collection = db.autoStarts
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    collection.insert_one({
        "start": dt_string
    })


def autoEnd():
    """
    Записывает в БД старт
    :return:
    """
    db = client.Diploma
    collection = db.autoEnd
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    collection.insert_one({
        "end": dt_string
    })


def autoScrapper(url: str, lastHash: str):
    """

    :param lastHash:
    :param url:
    :return:
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "pragma": 'no-cache',
        "cache-control": "no-cache",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "cookie": "CookieConsent={stamp:%27/iFeOz/wnfocVsfOloyCZGDBUppd7M6E1eceKMjQySF6mGHlsx+DGg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cver:1%2Cutc:1616914016722%2Cregion:%27ru%27}; _ga=GA1.2.36646224.1634998534; _gid=GA1.2.2001879148.1634998534; MatchFilter={%22active%22:false%2C%22live%22:false%2C%22stars%22:1%2C%22lan%22:false%2C%22teams%22:[]}; _pbjs_userid_consent_data=6683316680106290; _lr_geo_location=RU; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22d2047997-ef87-4ba1-bed6-b251a4919cab%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-09-23T14%3A15%3A39%22%7D; sharedid=%7B%22id%22%3A%2201FJPR3NAQRENC21NTC8NPJ478%22%2C%22ts%22%3A1634998538926%7D; cto_bundle=zToV4l9uR2xMZlhsRG95ZSUyRkxVTUg5a01Ha0M2SyUyRm4ySmVzTHFKYzNocVFzcHFRU0lRNVliSEhrWWNXc2FQNldvcUNiWHVkVkdPc2FOSXBRc2JLZWFxRVNQWVltVHByUktETTh1YTdBU1I2ODh1MWRUaUJjbG5WJTJGZm1Kc0dDMkM0MmZmUk9QRE10NyUyRlE2NnglMkZpQ3o2ZjdlOSUyRmclM0QlM0Q; _ia__v4=%7B%22v%22%3A3%2C%22r%22%3A%22RU%22%2C%22sportsbook%22%3A%5B0%2C1%5D%7D; pbjs-id5id=%7B%22created_at%22%3A%222021-10-23T14%3A15%3A33Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*rGk8vAlFomWD2PVavpahlzmh0B5vsoNiGC51qQspJqYAAAh3_mOmco5vwuApR3VG%22%2C%22universal_uid%22%3A%22ID5*Hf1nsQVBi-AOQNFLAijbPfC0doYJAyPQgDolhiSFTJcAAF2WidzBTU2HuAAaWPJu%22%2C%22signature%22%3A%22ID5_Abe7-LsG5eqPJjeERPs1m6bkEGXRwEPl3M1muPSevaednZHtjcc106J6mG7SbD1H61VMe0Ebx3G5KJ5fG0vxCGg%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%7D; pbjs-id5id_last=Sun%2C%2024%20Oct%202021%2007%3A29%3A42%20GMT; _lr_retry_request=true; _gat=1; outbrain_cid_fetch=true"
    }

    r = requests.get(url, headers=headers)
    if r.status_code == 200:  # 200 - ok
        html = r.text  # код текущей страницы в переменную
        soup = BeautifulSoup(html, features='html.parser')  # объект BS
        # Если есть таблица с классами
        if soup.find('table', class_='stats-table matches-table no-sort') is not None:
            for tr in soup.find('table', class_='stats-table matches-table no-sort').find('tbody').find_all('tr'):
                """Проходим по строкам таблицы"""
                new_url = 'https://hltv.org' + tr.find('td', class_='date-col').find('a')['href']
                print("new url:")
                print(new_url)
                current_hash = setCache(str(new_url))  # Получаем кэш текущей строки таблицы
                if current_hash != lastHash:  # Если текущий хэш не равен последнему из базы
                    if checkHash(current_hash) is False:  # если такого нет в БД
                        r_new = requests.get(new_url, headers=headers)
                        teamsPlayers = []  # составы команд
                        if (r_new.status_code == 200):  # если страничка загрузилась, то ок
                            html = r_new.text  # код текущей страницы в переменную
                            soup2 = BeautifulSoup(html, features='html.parser')  # объект BS
                            for table in soup2.find_all('table',
                                                        class_='stats-table'):  # обходим все таблички с результатми матча
                                teamPlayers = []
                                teamPlayers.append(
                                    table.find('th', class_='st-teamname').text)  # пишем название команды
                                for player in table.select('tbody tr td.st-player a'):  # обходим всех игроков
                                    teamPlayers.append(player.text)  # пишем ник игрока
                                teamsPlayers.append(teamPlayers)
                                del teamPlayers
                        # print(teamsPlayers)
                        else:
                            print("Вернулась не 200 - матч")
                            print(r_new.status_code)
                            break

                        score = []
                        teams_ = tr.find_all("td", class_="team-col")
                        for t in teams_:
                            if t.find("a") is None:
                                break
                            score.append(t.find("span", class_="score").text.strip().replace(')', '').replace('(', ''))
                        if tr.find("div", class_="dynamic-map-name-full") is None:
                            print(tr)
                            break
                        played_map = tr.find("div", class_="dynamic-map-name-full").text
                        event = tr.find("td", class_="event-col").text
                        print("data:")
                        print(teamsPlayers, score, played_map, event)
                        writeData(winner=teamsPlayers[0][0] if score[0] > score[1] else teamsPlayers[1][0],
                                  team1=teamsPlayers[0][0],
                                  team1_p1=teamsPlayers[0][1],
                                  team1_p2=teamsPlayers[0][2],
                                  team1_p3=teamsPlayers[0][3],
                                  team1_p4=teamsPlayers[0][4],
                                  team1_p5=teamsPlayers[0][5],
                                  team2=teamsPlayers[1][0],
                                  team2_p1=teamsPlayers[1][1],
                                  team2_p2=teamsPlayers[1][2],
                                  team2_p3=teamsPlayers[1][3],
                                  team2_p4=teamsPlayers[1][4],
                                  team2_p5=teamsPlayers[1][5],
                                  map=played_map
                                  )
                        writeHash(current_hash)
                        print(current_hash)
                        ####
                    else:
                        print("Такой уже есть")
                else:  # Если это был последний хэш, то надо прекращать работу
                    print("Текущий и последний были равны")
                    return

                print("-----------------------------------")
        # Если нет ссылки на следующую выборку, то просто закрываем файл
        if not soup.find('div', class_='pagination-component with-stats-table') \
                .find('a', class_='pagination-next').has_attr('href'):
            return
        else:
            # Иначе, закрываем файл, получаем ссылку дальше и делаем рекурсию, через 3 секунды
            href = soup.find('div', class_='pagination-component with-stats-table') \
                .find('a', class_='pagination-next')['href']
            print("Следующая страница")
            print(href)
            time.sleep(3)
            autoScrapper("https://www.hltv.org" + href, getLastDocument())
    else:
        # Отладочный момент, чтобы знать какая ошибка произошла
        print(r.status_code)


if __name__ == '__main__':
    client = MongoClient(
        "mongodb+srv://new:oIGh34Xd8010lrgj@cluster0.rg6wi.mongodb.net/Cluster0?retryWrites=true&w=majority")
    url = "https://www.hltv.org/stats/matches"
    lastHash = getLastDocument()
    autoStart()
    autoScrapper(url, lastHash=lastHash)
    autoEnd()
