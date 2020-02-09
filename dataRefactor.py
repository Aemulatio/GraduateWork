import sqlite3


def printAll(list):
    for i in list:
        print(i)


# region connecting
connection = sqlite3.connect('DataBase/DataBase.sqlite')
cursor = connection.cursor()
# endregion

# region reading data base
cursor.execute('''select * from rawData''')
raw_data = cursor.fetchall()
local_data = list()
for line in raw_data:  # считываем базу данных и суем все в list()
    local_data.append(
        (line[1],
         line[2].replace('[\'', '').replace("'", '').replace("'", '').replace('\'', '').replace(']', '').split(','),
         line[3].replace('[\'', '').replace('\'', '').replace('\'', '').replace('\'', '').replace(']', '').split(','),
         line[4], line[5], line[0]))

for ld in local_data:  # Удаляем лишние пробелы
    for ld_line in ld[1:3]:
        ld_line[0] = ld_line[0].strip()
        ld_line[1] = ld_line[1].strip()

printAll(local_data)  # test only
# endregion

# ('8-2-20', ['1WIN', 'EveryBodyDance'], ['16', '5'], 'Dust2', 'CIS Minor Open Qualifier 2 - ESL One Rio 2020', 23)
# ('8-2-20', ['EveryBodyDance', '1WIN'], ['16', '9'], 'Train', 'CIS Minor Open Qualifier 2 - ESL One Rio 2020', 23)
# ('8-2-20', ['EveryBodyDance', '1WIN'], ['12', '16'], 'Overpass', 'CIS Minor Open Qualifier 2 - ESL One Rio 2020', 23)

refactored_data = list()
matches = {}
# date, team1, win/lose, team2, win/lose, map, event
# TODO:Думаю нужно переделать чуток парсер.
#  Крч, надо сделать чтобы игры были обозначены по сериям игр. ВОТ! DONE!
# TODO: Более лучшее распределение по сериям

for line in local_data:
    matches[line[-1]] = {
        'teams': line[1][0] + '-' + line[1][1],
        'score': line[2][0] + '-' + line[2][0],
    }  # Сюда можно засунуть игры по их сериям, т.е. номер_серии {teams: t1-t2, score:t1score-t2score}

printAll(matches)

# region close_connection
connection.commit()
cursor.close()
connection.close()
# endregion
