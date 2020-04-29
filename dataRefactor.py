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
matches = dict()
# series, date, team1, win/lose, team2, win/lose, map, event
# TODO:Думаю нужно переделать чуток парсер.
#  Крч, надо сделать чтобы игры были обозначены по сериям игр. ВОТ! DONE!
# TODO: Более лучшее распределение по сериям

prev = 1
current = 0
t1 = str()  # left team
t2 = str()  # right team
s1 = str()  # left team score
s2 = str()  # right team score
event = str()  # event
date = str()  # date of match
gMap = str()  # map of the game

ref_data = list()

for line in reversed(local_data):
    # matches[line[-1]] = {
    #     'teams': str(line[1][0]) + '/' + str(line[1][1]),
    #     'score': str(line[2][0]) + '-' + str(line[2][1]),
    # }  # Сюда можно засунуть игры по их сериям, т.е. номер_серии {teams: t1-t2, score:t1score-t2score}
    # if refactored_data[-1][0] == line[-1]:

    # ('8-2-20', ['1WIN', 'EveryBodyDance'], ['16', '5'], 'Dust2',
    #                                   'CIS Minor Open Qualifier 2 - ESL One Rio 2020', 23)
    if prev != current:
        t1 = line[1][0]  # left team
        t2 = line[1][1]  # right team
        s1 = 0  # left team score to 0
        s2 = 0  # right team score to 0
        event = line[-2]
        date = line[0]
        gMap = line[3]
    current = line[-1]
    if prev == current:  # if prev id == cur id
        if t1 == line[1][0]:  # if teams doesnt switch sides in statistic
            if int(line[2][0]) > int(line[2][1]):  # if t1 > t2
                s1 = 'w'
                s2 = 'l'
            else:  # if t2 > t1
                s2 = 'w'
                s1 = 'l'
        else:
            if int(line[2][1]) > int(line[2][0]):  # if t2 > t1
                s1 = 'w'
                s2 = 'l'
            else:  # if t1 > t2
                s2 = 'w'
                s1 = 'l'
        # print([t1, s1, t2, s2, date, event])
    else:
        t1 = line[1][0]  # left team
        t2 = line[1][1]  # right team
        s1 = 0  # left team score to 0
        s2 = 0  # right team score to 0
        event = line[-2]
        date = line[0]
        gMap = line[3]
        prev = current
        if prev == current:  # if prev id == cur id
            if t1 == line[1][0]:  # if teams doesnt switch sides in statistic
                if int(line[2][0]) > int(line[2][1]):  # if t1 > t2
                    s1 = 'w'
                    s2 = 'l'
                else:  # if t2 > t1
                    s2 = 'w'
                    s1 = 'l'
            else:
                if int(line[2][1]) > int(line[2][0]):  # if t2 > t1
                    s1 = 'w'
                    s2 = 'l'
                else:  # if t1 > t2
                    s2 = 'w'
                    s1 = 'l'

    # for match in local_data:
    #     if prev != current:
    #         t1 = match[1][0]  # left team
    #         t2 = match[1][1]  # right team
    #         s1 = 0  # left team score to 0
    #         s2 = 0  # right team score to 0
    #         event = match[-2]
    #         date = match[0]
    #     current = match[-1]
    #     if prev == current:  # if prev id == cur id
    #         if t1 == match[1][0]:  # if teams doesnt switch sides in statistic
    #             if int(match[2][0]) > int(match[2][1]):  # if t1 > t2
    #                 s1 = 'w'
    #                 s2 = 'l'
    #             else:  # if t2 > t1
    #                 s2 = 'w'
    #                 s1 = 'l'
    #         else:
    #             if int(match[2][1]) > int(match[2][0]):  # if t2 > t1
    #                 s1 = 'w'
    #                 s2 = 'l'
    #             else:  # if t1 > t2
    #                 s2 = 'w'
    #                 s1 = 'l'
    #     else:
    #         print([t1, s1, t2, s2, date, event])
    #         refactored_data.append([t1, s1, t2, s2, date, event])
    #         t1 = match[1][0]  # left team
    #         t2 = match[1][1]  # right team
    #         s1 = 0  # left team score to 0
    #         s2 = 0  # right team score to 0
    #         event = match[-2]
    #         date = match[0]
    #         prev = current
    #         if prev == current:  # if prev id == cur id
    #             if t1 == match[1][0]:  # if teams doesnt switch sides in statistic
    #                 if int(match[2][0]) > int(match[2][1]):  # if t1 > t2
    #                     s1 = 'w'
    #                     s2 = 'l'
    #                 else:  # if t2 > t1
    #                     s2 = 'w'
    #                     s1 = 'l'
    #             else:
    #                 if int(match[2][1]) > int(match[2][0]):  # if t2 > t1
    #                     s1 = 'w'
    #                     s2 = 'l'
    #                 else:  # if t1 > t2
    #                     s2 = 'w'
    #                     s1 = 'l'
    ref_data.append([t1, s1, t2, s2, date, gMap, event])
    # print([t1, s1, t2, s2, date, event])

    # Create table

print(len(ref_data))
try:
    if cursor.execute('''SELECT count(*) FROM refactoredData''') != 0:
        cursor.execute('''DELETE FROM refactoredData''')
except sqlite3.OperationalError:
    cursor.execute('''CREATE TABLE IF NOT EXISTS refactoredData
                                 (id integer PRIMARY KEY AUTOINCREMENT, team1 text, team1_Status text, team2 text, team2_Status text, date text, map text, event text)''')

try:
    # Insert a row of data
    for line in ref_data:
        cursor.execute(
            '''INSERT INTO refactoredData(team1, team1_Status, team2, team2_Status,date, map, event) VALUES (?,?,?,?,?,?,?)''',
            (str(line[0]), str(line[1]), str(line[2]), str(line[3]), str(line[4]), str(line[5]), str(line[6])))
        # print(line[0])
except sqlite3.OperationalError:
    print("123")
    # Save (commit) the changes

# refactored_data.append([t1, s1, t2, s2, date, event])
#     refactored_data.append((line[-1], line[0], t1,  ))

# for i,v in matches.items():
#     print(i,v)

# region close_connection
connection.commit()
cursor.close()
connection.close()
# endregion
