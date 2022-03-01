from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient


def getPlayers(url: str):
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

        if soup.find('table', class_='stats-table player-ratings-table') is not None:
            for href in soup.select("td.playerCol a"):
                user_id = str(href['href']).split("/")[3]
                nickName = str(href['href']).split("/")[-1]
                print(nickName)
                new_url = "https://www.hltv.org" + href['href']
                r2 = requests.get(new_url, headers=headers)
                if (r2.status_code == 200):  # если страничка загрузилась, то ок
                    html_new = r2.text  # код текущей страницы в переменную
                    soup2 = BeautifulSoup(html_new, features='html.parser')  # объект BS
                    current_team = soup2.select("div.SummaryTeamname")[0].get_text()
                    stats = soup2.select("div.summaryStatBreakdownDataValue")
                    rating = stats[0].get_text()
                    dpr = stats[1].get_text()
                    kast = stats[2].get_text()
                    impact = stats[3].get_text()
                    adr = stats[4].get_text()
                    kpr = stats[5].get_text()
                    collection.insert_one({
                        'user_id': user_id,
                        'nickName': nickName,
                        'current_team': current_team,
                        'rating': rating,
                        'dpr': dpr,
                        'kast': kast,
                        'impact': impact,
                        'adr': adr,
                        'kpr': kpr,
                    })
    else:
        print(r.status_code)


if __name__ == '__main__':
    url = 'https://www.hltv.org/stats/players/'
    client = MongoClient(
        "mongodb+srv://new:oIGh34Xd8010lrgj@cluster0.rg6wi.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = client.Diploma
    collection = db.Players
    print("Соединено")
    for obj in collection.find():
        collection.delete_many(obj)
    print("Удалено все")
    getPlayers(url)
