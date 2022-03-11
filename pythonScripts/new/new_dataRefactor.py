import csv
import pandas as pd
from itertools import groupby
import numpy as np
import ast
import json


def printAll(list):
    print(list.__class__.__name__)
    for i in list:
        print(i)


def csv_reader(path):
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


def csv_writer(filename: str, data: list):
    with open(filename, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(
            ['Winner',
             'Team1', "T1_Player1", "T1_Player2", "T1_Player3", "T1_Player4", "T1_Player5",
             'Team2', "T2_Player1", "T2_Player2", "T2_Player3", "T2_Player4", "T2_Player5",
             'Map'])
        for line in data:
            writer.writerow(line)


def unite(files: list, output_filename: str):
    """
    Объединяет файлы .csv в один

    :param files: Массив файлов для объединения
    :param output_filename: Имя выходного файла
    :return:
    """
    pd.concat([pd.read_csv(f, delimiter=',', encoding='UTF-8') for f in files]).to_csv("../Data/New/" + output_filename)


def refactor(input_file: str, output_file: str):
    """
Приводит к заданному виду файлы
    :param input_file:
    :param output_file:
    :return:
    """
    data = csv_reader(input_file)[1:]
    refactored = list()
    for row in data:
        print(row)
        print(row[1])
        print(row[2])
        t1 = ast.literal_eval(row[2])
        t2 = ast.literal_eval(row[3])
        if len(t1) == 6 and len(t2) == 6:
            score = ast.literal_eval(row[4])
            map = row[5]
            team1 = {
                "name": t1[0],
                "player1": t1[1],
                "player2": t1[2],
                "player3": t1[3],
                "player4": t1[4],
                "player5": t1[5],
            }
            team2 = {
                "name": t2[0],
                "player1": t2[1],
                "player2": t2[2],
                "player3": t2[3],
                "player4": t2[4],
                "player5": t2[5],
            }

            # Получаем победителя
            if score[0] > score[1]:
                # winner = "Team1"
                winner = team1['name']
            else:
                # winner = "Team2"
                winner = team2['name']

            refactored.append(
                [winner, team1['name'], team1['player1'], team1['player2'], team1['player3'], team1['player4'],
                 team1['player5'], team2['name'], team2['player1'], team2['player2'], team2['player3'],
                 team2['player4'], team2['player5'], map])

    csv_writer(output_file, refactored)


def delete_teams(input_file: str, output_file: str, teams: str):
    f = open(teams, 'r', encoding='utf-8')
    teams_list = json.loads(f.read()).keys()
    f.close()
    data = csv_reader(input_file)
    refactored = list()

    for row in data:
        if row[1] in teams_list or row[7] in teams_list:
            refactored.append(row)

    csv_writer(output_file, refactored)


def get_unique_maps(input_file: str, output_file: str):
    """
    Получает уникальный список карт

    :param input_file:
    :param output_file:
    :return:
    """
    data = csv_reader(input_file)
    # print(data)
    UniqueMap = np.unique(np.array(data)[:, -1])
    maps = {}
    for map in UniqueMap:
        maps[map] = {"mapName": map}

    endFile = open(output_file, 'w', encoding='utf-8')
    endFile.write(json.dumps(maps))


def team_by_team_csv(list, ids, name):
    try:  # Менять в зависимости от нужды либо море либо тимс
        with open("Data/More/" + name + ".csv", "w", newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['Winner', 'Team1', 'Team2', 'Team1_Score', 'Team2_Score', 'Map'])
            for id in ids:
                writer.writerow(list[id])
    except:
        print("Nu ok", name)


def split_by_teams(files: list[str]):
    """
    Разбивает данные по командам

    :type files: object
    """
    output_filename = ""
    data = list()
    for file in files:
        data.append(csv_reader(file)[1:])

    refactored_data = list()
    table = str.maketrans("[]", "  ")
    for year in data:
        for match in year:
            # Заменяем [ ] из строки на пробелы, заменяем " на ' и разбираем ее на 2, тк имеем дело с строками
            teams = match[1].translate(table).replace("\"", "'").split(',')
            # Разбиваем полученный массив на отдельные переменные убирая ' и лишние пробелы
            team1, team2 = teams[0].strip()[1:-1], teams[1].strip()[1:-1]

            # Заменяем [ ] из строки на пробелы, заменяем " на ' и разбираем ее на 2, тк имеем дело с строками
            score = match[2].translate(table).replace("\'", "").split(',')
            # Разбиваем полученный массив на отдельные переменные убирая и лишние пробелы
            team1_score, team2_score = score[0].strip(), score[1].strip()

            # Получаем победителя
            winner = str()
            if team1_score > team2_score:
                winner = 'Team1'
            else:
                winner = 'Team2'

            # Получаем карту на которой играли
            map = match[3]

            # Добавляем данные в таком виде
            refactored_data.append([winner, team1, team2, team1_score, team2_score, map])

    rd = list()
    pt1, pt2 = refactored_data[0][1:3]
    for row in refactored_data:
        if pt1 in row and pt2 in row:
            if row[1] == pt1 and row[2] == pt2:
                rd.append(row)
            else:
                if row[3] > row[4]:
                    rd.append([row[0], row[2], row[1], row[4], row[3], row[5]])
                else:
                    if row[0] == 'Team1':
                        rd.append(["Team2", row[2], row[1], row[4], row[3], row[5]])
                    else:
                        rd.append(["Team1", row[2], row[1], row[4], row[3], row[5]])
        else:
            rd.append(row)
        pt1, pt2 = row[1:3]

    rd = sorted(rd)
    del (rd[:3])
    UniqueTeams = np.unique(np.concatenate((np.array(rd)[:, 1], np.array(rd)[:, 2])))

    rd = np.array(rd)
    UniqueTeams = np.delete(UniqueTeams, 0)

    for team in UniqueTeams:
        if team in rd:
            if len(np.where(rd[:, 1] == team)[0]) > 10:  # Пишем только те команды в которых больше 10 игр за 19-20 года
                team_by_team_csv(rd, np.where(rd[:, 1] == team)[0], team)


def delete_garbage(filename, matches_count, output):
    data = pd.read_csv(filename)
    UniqueTeams = np.unique(np.concatenate((np.array(data)[:, 1], np.array(data)[:, 7])))

    for team in UniqueTeams:
        if team in data.values:
            # Пишем только те команды в которых больше 10 игр за 19-20 года
            if data.eq(team).values.sum() < matches_count + 1:
                for row in data.index[data['Team1'] == team]:
                    data = data.drop(row)
                for row in data.index[data['Team2'] == team]:
                    data = data.drop(row)

    # display(data.head())
    # printAll(data)
    data.to_csv('../Data/' + output, index=False)
    # csv_writer(output, data)


if __name__ == '__main__':
    # refactor_data_from_csvs_to_csv(['../Data/rawData20.csv', '../Data/rawData19.csv', '../Data/rawData20.csv'],
    #                                'results11_TN.csv')
    # refactor_data_from_csvs_to_csv(['../Data/rawData20.csv'],
    #                                'results12_TN.csv')
    # delete_garbage('../Data/results11_TN.csv', 50, 'results8_wo_garbage_NTN.csv')
    # delete_garbage('../Data/results12_TN.csv', 20, 'results111_wo_garbage_NTN.csv')
    print('done')
    # split_by_teams(['Data/rawData19.csv', 'Data/rawData20.csv'])
    # printAll(data)
    # 'Data/rawData18.csv',

    # unite(['../Data/New/rawData18_newFormat.csv', '../Data/New/rawData19_newFormat.csv',
    #        '../Data/New/rawData20_newFormat.csv', '../Data/New/rawData21_newFormat.csv',], "csgo18-21.csv")
    # refactor("../Data/New/csgo18-21.csv", "../Data/New/refactored_csgo_18-21.csv")
    delete_teams("../../Data/New/refactored_csgo_18-21.csv", "../Data/New/refactored_goodTeams_csgo_18-21.csv",
                 "../Data/New/teams.json")

    # get_unique_maps("../Data/New/refactored_goodTeams18-20.csv", "../Data/New/maps.json")

    # data = pd.read_csv("../Data/New/refactored18-20.csv")
    # print(np.array(data)[:, 1])
    # print(np.array(data)[:])
    # UniqueTeams = np.unique(np.concatenate((np.array(data)[:, 1], np.array(data)[:, 7])))
    # print(UniqueTeams)
