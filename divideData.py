import csv
import collections


def csv_reader(path):
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


if __name__ == "__main__":
    data = csv_reader('refactoredData.csv')[1:]

    # region test
    wins = collections.defaultdict(int)
    matches = collections.defaultdict(int)
    maps = collections.defaultdict(int)
    tt = collections.defaultdict(list)
    index = round(len(data) / 5)
    # print(index)
    # ['KOVA', 'l', 'LDLC', 'w', '11-5-20 ', 'Dust2', 'Home Sweet Home Cup 5 Closed Qualifier']

    for row in data[:index]:
        # for t1 in [*row]:
        #     print(t1)
        tt[row[0].strip()].append((row[5].strip(), row[2].strip(), row[1].strip()))
        matches[row[0].strip()] += 1
        matches[row[2].strip()] += 1
        maps[row[-2].strip()] += 1
        if row[1].strip() == 'l':
            wins[row[2].strip()] += 1
        else:
            wins[row[0].strip()] += 1

    # print(row)
    # print(data[0])
    # for team, m in matches.items():
    #     print(team, m)
    print(matches)
    # print(wins['KOVA'])
    print(wins)
    print(maps)
    print(tt)
    # endregion
