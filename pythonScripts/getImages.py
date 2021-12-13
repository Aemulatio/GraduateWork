from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import base64
import json


def getFullProfile(output_file: str):
    """

    :param output_file:
    :return:
    """
    client = MongoClient(
        "mongodb+srv://new:oIGh34Xd8010lrgj@cluster0.rg6wi.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = client.Diploma
    collection = db.Teams
    data = list()
    for obj in collection.find():
        data.append(obj)

    newData = []
    for d in data[:]:
        teamName = d.get('teamName')
        teamUrl = d.get(teamName).get('teamUrl')
        teamLogo = getTeamLogo(teamUrl)
        name1 = d.get(teamName).get('player1').get('name')
        url1 = d.get(d.get('teamName')).get('player1').get("url")
        p1 = getPlayerImage(url1)
        print(p1)
        name2 = d.get(teamName).get('player2').get('name')
        url2 = d.get(d.get('teamName')).get('player2').get("url")
        p2 = getPlayerImage(url2)
        print(p2)
        name3 = d.get(teamName).get('player3').get('name')
        url3 = d.get(d.get('teamName')).get('player3').get("url")
        p3 = getPlayerImage(url3)
        print(p3)
        name4 = d.get(teamName).get('player4').get('name')
        url4 = d.get(d.get('teamName')).get('player4').get("url")
        p4 = getPlayerImage(url4)
        print(p4)
        name5 = d.get(teamName).get('player5').get('name')
        url5 = d.get(d.get('teamName')).get('player5').get("url")
        p5 = getPlayerImage(url5)
        print(p5)
        newData.append(
            {
                'teamName': teamName,
                teamName:
                    {
                        'teamUrl': teamUrl,
                        'teamLogo': teamLogo,
                        'teamName': teamName,
                        'player1':
                            {
                                "url": url1,
                                'name': name1,
                                'image': p1,
                            },
                        'player2':
                            {
                                "url": url2,
                                'name': name2,
                                'image': p2,
                            },
                        'player3':
                            {
                                "url": url3,
                                'name': name3,
                                'image': p3,
                            },
                        'player4':
                            {
                                "url": url4,
                                'name': name4,
                                'image': p4,
                            },
                        'player5':
                            {
                                "url": url5,
                                'name': name5,
                                'image': p5,
                            },
                    }
            })
        print("-----------------------")

    endFile = open(output_file, 'w', encoding='utf-8')
    endFile.write(json.dumps(newData))


def getPlayerImage(url):
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
        img = soup.select("img[itemprop=image]")
        print(url)
        # print(img)
        src = img[0]['src']
        if "player_silhouette.png" in src:
            src = "https://www.hltv.org" + src
        print(src)
        answ = base64.b64encode(src.encode('ascii')).decode("ascii")
        # print(answ)
        return answ
    else:
        print("err")


def getTeamLogo(url):
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
        img = soup.select(".profile-team-logo-container img.teamlogo")
        print(url)
        # print(img)
        src = img[0]['src']
        # if "player_silhouette.png" in src:
        #     src = "https://www.hltv.org" + src
        print(src)
        answ = base64.b64encode(src.encode('ascii')).decode("ascii")
        # print(answ)
        return answ
    else:
        print("err")


if __name__ == '__main__':
    getFullProfile("../Data/New/teams_from_db_with_logos.json")
