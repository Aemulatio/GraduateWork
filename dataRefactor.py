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
        (line[0],
         line[1].replace('[\'', '').replace("'", '').replace("'", '').replace('\'', '').replace(']', '').split(','),
         line[2].replace('[\'', '').replace('\'', '').replace('\'', '').replace('\'', '').replace(']', '').split(','),
         line[3], line[4]))

for ld in local_data:  # Удаляем лишние пробелы
    for ld_line in ld[1:3]:
        ld_line[0] = ld_line[0].strip()
        ld_line[1] = ld_line[1].strip()

printAll(local_data)  # test only
# endregion

# ('8-2-20', ['EveryBodyDance', '1WIN'], ['12', '16'], 'Overpass', 'CIS Minor Open Qualifier 2 - ESL One Rio 2020')
# ('8-2-20', ['Astralis', 'Complexity'], ['11', '16'], 'Dust2', 'BLAST Premier Spring Series 2020')
# ('8-2-20', ['Astralis', 'Complexity'], ['12', '16'], 'Vertigo', 'BLAST Premier Spring Series 2020')
# ('8-2-20', ['DivisionX', 'SHIFT'], ['16', '5'], 'Vertigo', 'Vietnam Pro League Season 3')

refactored_data = list()
# date, team1, win/lose, team2, win/lose, map, event
# Думаю нужно переделать чуток парсер. Крч, надо сделать чтобы игры были обозначены по сериям игр. ВОТ!
for line in local_data:
    print('')

# region close_connection
connection.commit()
cursor.close()
connection.close()
# endregion
