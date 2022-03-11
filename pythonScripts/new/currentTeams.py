import time

from bs4 import BeautifulSoup
import requests
import datetime
import json

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "pragma": 'no-cache',
    "cache-control": "no-cache",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "cookie": "CookieConsent={stamp:%27/iFeOz/wnfocVsfOloyCZGDBUppd7M6E1eceKMjQySF6mGHlsx+DGg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cver:1%2Cutc:1616914016722%2Cregion:%27ru%27}; _ga=GA1.2.36646224.1634998534; _gid=GA1.2.2001879148.1634998534; MatchFilter={%22active%22:false%2C%22live%22:false%2C%22stars%22:1%2C%22lan%22:false%2C%22teams%22:[]}; _pbjs_userid_consent_data=6683316680106290; _lr_geo_location=RU; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22d2047997-ef87-4ba1-bed6-b251a4919cab%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-09-23T14%3A15%3A39%22%7D; sharedid=%7B%22id%22%3A%2201FJPR3NAQRENC21NTC8NPJ478%22%2C%22ts%22%3A1634998538926%7D; cto_bundle=zToV4l9uR2xMZlhsRG95ZSUyRkxVTUg5a01Ha0M2SyUyRm4ySmVzTHFKYzNocVFzcHFRU0lRNVliSEhrWWNXc2FQNldvcUNiWHVkVkdPc2FOSXBRc2JLZWFxRVNQWVltVHByUktETTh1YTdBU1I2ODh1MWRUaUJjbG5WJTJGZm1Kc0dDMkM0MmZmUk9QRE10NyUyRlE2NnglMkZpQ3o2ZjdlOSUyRmclM0QlM0Q; _ia__v4=%7B%22v%22%3A3%2C%22r%22%3A%22RU%22%2C%22sportsbook%22%3A%5B0%2C1%5D%7D; pbjs-id5id=%7B%22created_at%22%3A%222021-10-23T14%3A15%3A33Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*rGk8vAlFomWD2PVavpahlzmh0B5vsoNiGC51qQspJqYAAAh3_mOmco5vwuApR3VG%22%2C%22universal_uid%22%3A%22ID5*Hf1nsQVBi-AOQNFLAijbPfC0doYJAyPQgDolhiSFTJcAAF2WidzBTU2HuAAaWPJu%22%2C%22signature%22%3A%22ID5_Abe7-LsG5eqPJjeERPs1m6bkEGXRwEPl3M1muPSevaednZHtjcc106J6mG7SbD1H61VMe0Ebx3G5KJ5fG0vxCGg%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%7D; pbjs-id5id_last=Sun%2C%2024%20Oct%202021%2007%3A29%3A42%20GMT; _lr_retry_request=true; _gat=1; outbrain_cid_fetch=true"
}


def getTeams(files: list[str]):
    print(datetime.datetime.now())
    html = str()
    for file in files:
        f = open(file, 'r', encoding="UTF-8")
        html = html + f.read()
        f.close()
    soup = BeautifulSoup(html, features='html.parser')
    goodTeams = list()
    gt = {}
    badTeams = list()
    print("start parse")
    for tbody in soup.find_all('tbody'):
        for tr in tbody.find_all('tr'):
            for team_col in tr.select('td.team-col'):
                if team_col.find('a').text in badTeams or team_col.find('a').text in goodTeams:
                    continue
                url = "https://hltv.org" + team_col.find('a')['href'].replace('/stats', '').replace('teams', 'team')
                url = url[:url.find("?")]
                r = requests.get(url, headers=headers)
                if r.status_code == 200:  # r.status
                    soup2 = BeautifulSoup(r.text, features='html.parser')
                    no = soup2.select('#rosterBox .empty-state')
                    if len(no) == 1:
                        badTeams.append(team_col.find('a').text)
                    else:
                        roster = soup2.find("div", class_="bodyshot-team").find_all("a", class_='col-custom')
                        if len(roster) == 5:
                            print(url)
                            logo_container = soup2.find("img", class_="teamlogo")
                            print(logo_container)
                            if logo_container.has_attr("srcset"):
                                logo = soup2.find("img", class_="teamlogo")['srcset'][:-3].replace("amp;", "")
                            else:
                                logo = soup2.find("img", class_="teamlogo")['src'].replace("amp;", "")
                            print(logo)
                            obj = {
                                'teamUrl': url,
                                "teamName": team_col.find('a').text,
                                "teamLogo": logo,
                                'player1': {},
                                'player2': {},
                                'player3': {},
                                'player4': {},
                                'player5': {},
                            }
                            subSoup = [BeautifulSoup(str(roster[0]), features='html.parser'),
                                       BeautifulSoup(str(roster[1]), features='html.parser'),
                                       BeautifulSoup(str(roster[2]), features='html.parser'),
                                       BeautifulSoup(str(roster[3]), features='html.parser'),
                                       BeautifulSoup(str(roster[4]), features='html.parser')]

                            obj['player1']['url'] = 'https://hltv.org' + subSoup[0].find('a')['href']
                            obj['player2']['url'] = 'https://hltv.org' + subSoup[1].find('a')['href']
                            obj['player3']['url'] = 'https://hltv.org' + subSoup[2].find('a')['href']
                            obj['player4']['url'] = 'https://hltv.org' + subSoup[3].find('a')['href']
                            obj['player5']['url'] = 'https://hltv.org' + subSoup[4].find('a')['href']

                            obj['player1']['name'] = subSoup[0].select_one('a span.text-ellipsis').text
                            obj['player2']['name'] = subSoup[1].select_one('a span.text-ellipsis').text
                            obj['player3']['name'] = subSoup[2].select_one('a span.text-ellipsis').text
                            obj['player4']['name'] = subSoup[3].select_one('a span.text-ellipsis').text
                            obj['player5']['name'] = subSoup[4].select_one('a span.text-ellipsis').text

                            # if subSoup[0].select_one('a img.bodyshot-team-img') is not None:
                            print(subSoup[0].select_one('a img'))

                            p1URI = subSoup[0].select_one('a img')['src'].replace("amp;", "")
                            if p1URI[0] == "/":
                                obj['player1']['imgURI'] = 'https://hltv.org' + p1URI
                            else:
                                obj['player1']['imgURI'] = p1URI

                            p2URI = subSoup[1].select_one('a img')['src'].replace("amp;", "")
                            if p2URI[0] == "/":
                                obj['player2']['imgURI'] = 'https://hltv.org' + p2URI
                            else:
                                obj['player2']['imgURI'] = p2URI

                            p3URI = subSoup[2].select_one('a img')['src'].replace("amp;", "")
                            if p3URI[0] == "/":
                                obj['player3']['imgURI'] = 'https://hltv.org' + p3URI
                            else:
                                obj['player3']['imgURI'] = p3URI

                            p4URI = subSoup[3].select_one('a img')['src'].replace("amp;", "")
                            if p4URI[0] == "/":
                                obj['player4']['imgURI'] = 'https://hltv.org' + p4URI
                            else:
                                obj['player4']['imgURI'] = p4URI

                            p5URI = subSoup[4].select_one('a img')['src'].replace("amp;", "")
                            if p5URI[0] == "/":
                                obj['player5']['imgURI'] = 'https://hltv.org' + p5URI
                            else:
                                obj['player5']['imgURI'] = p5URI

                            print(obj)
                            gt[team_col.find('a').text] = obj
                            goodTeams.append(team_col.find('a').text)
                        else:
                            badTeams.append(team_col.find('a').text)
                        pass
                else:  # r.status
                    print("Не 200")
                    print(r.status_code)
                    break
                time.sleep(5)
        print("_------------------------_ end of tbody _------------------------_")

    print(datetime.datetime.now())
    endFile = open("../../Data/New/teams_.json", 'w', encoding='utf-8')
    endFile.write(json.dumps(gt))
    print(datetime.datetime.now())
    endFile.close()


def to_json(input_file: str):
    f = open(input_file, 'r', encoding='utf-8')
    data = f.read()
    f.close()
    f = open("../../Data/New/teams_.json", 'w', encoding='utf-8')
    f.write(data)
    f.close()


if __name__ == '__main__':
    getTeams(["../Data/New/csgo2018.html", "../Data/New/csgo2019.html", "../Data/New/csgo2020.html",
              "../Data/New/csgo2021.html"])  # почти 6 час
    to_json("../Data/New/teams_.txt")
