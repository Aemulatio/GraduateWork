import csv
import collections
import pandas as pd
from IPython.display import display
import numpy as np


def csv_reader(path):
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


if __name__ == "__main__":
    data = pd.read_csv("Data/results2.csv")
    display(data.head())
    # Получаем все команды
    UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
    # UT = pd.Series(UniqueTeams, index=(range(1, len(UniqueTeams) + 1)))
    # print(UniqueTeams)
    # # Тоже самое только долгим путем
    # Team1 = data['Team1']
    # Team2 = data['Team2']
    # Team1_unique = Team1.unique()  # , name='Team1'
    # Team2_unique = Team2.unique()  # , name='Team2'
    # T = np.concatenate((Team1_unique, Team2_unique))
    # T1 = np.unique(T)
    # data
    # temp = data
    for id, team in UniqueTeams.items():
        data = data.replace(team, id)

    print("DATA:")
    print(data)

    # Total number of matches.
    # n_matches = data.shape[0]

    # matches = {}
    # for team in UniqueTeams:
    #     matches[team] = \
    #         {
    #             'Wins': len(data[data.Winner == team]),
    #             'Matches': len(data[data.Team1 == team]) + len(data[data.Team2 == team]),
    #             # 'Maps': [].append(data[data.Map])
    #             # 'PlayedMaps': [].append(data[data['Map']])
    #         }

    # df = pd.DataFrame(matches).T
    # print(df.Matches > 5)

    # print(type(UniqueTeams[0]))
    # TTTT = pd.DataFrame(index=UniqueTeams)
    # print(TTTT)
    # print(UT)
    # for id, team in UT.items():
    # TTTT[team].append("123")
    # print(id)
    # print(data.any(axis='columns'))
    # matches1[str(id)] = {
    #     id: data[data['Team1'].str.contains(team)],
    # }
    # pass

    # print("Matches:")
    # print(matches)

    # Calculate number of features. -1 because we are saving one as the target variable (win/lose/draw)
    # n_features = data.shape[1] - 1
    # # Calculate matches won by home team.
    # n_homewins = len(data[data.Winner == 'Team2'])
    # # Calculate win rate for home team.
    # win_rate = (float(n_homewins) / (n_matches)) * 100
    # print(n_matches)
    # print(n_features)
    # print(n_homewins)
    # print(win_rate)

    X_all = data.drop(['Winner'], 1)
    y_all = data['Winner']

    display(X_all.head())
    print("\n")
    display(y_all.head())
    # print(X_all)
    # print(y_all)

    # Standardising the data.
    from sklearn.preprocessing import scale

    # # Center to the mean and component wise scale to unit variance.
    cols = [['Team1', 'Team2', 'Team1_Score', 'Team2_Score']]
    for col in cols:
        X_all[col] = scale(X_all[col])


    # last 3 wins for both sides
    # X_all.HM1 = X_all.HM1.astype('str')
    # X_all.HM2 = X_all.HM2.astype('str')
    # X_all.HM3 = X_all.HM3.astype('str')
    # X_all.AM1 = X_all.AM1.astype('str')
    # X_all.AM2 = X_all.AM2.astype('str')
    # X_all.AM3 = X_all.AM3.astype('str')

    # we want continous vars that are integers for our input data, so lets remove any categorical vars
    def preprocess_features(X):
        ''' Preprocesses the football data and converts catagorical variables into dummy variables. '''

        # Initialize new output DataFrame
        output = pd.DataFrame(index=X.index)

        # Investigate each feature column for the data
        for col, col_data in X.iteritems():

            # If data type is categorical, convert to dummy variables
            if col_data.dtype == object:
                col_data = pd.get_dummies(col_data, prefix=col)

            # Collect the revised columns
            output = output.join(col_data)

        return output


    from sklearn.model_selection import train_test_split

    # Shuffle and split the dataset into training and testing set.
    X_train, X_test, y_train, y_test = train_test_split(X_all, y_all,
                                                        test_size=50,
                                                        random_state=2, )
    # stratify = y_all)

    print(X_train)
    print(X_test)
    print(y_train)
    print(y_test)

    from time import time
    from sklearn.metrics import f1_score


    def train_classifier(clf, X_train, y_train):
        ''' Fits a classifier to the training data. '''

        # Start the clock, train the classifier, then stop the clock
        start = time()
        clf.fit(X_train, y_train)
        end = time()

        # Print the results
        print("Trained model in {:.4f} seconds".format(end - start))


    def predict_labels(clf, features, target):
        ''' Makes predictions using a fit classifier based on F1 score. '''

        # Start the clock, make predictions, then stop the clock
        start = time()
        y_pred = clf.predict(features)

        end = time()
        # Print and return results
        print("Made predictions in {:.4f} seconds.".format(end - start))

        return f1_score(target, y_pred, pos_label='Team1'), sum(target == y_pred) / float(len(y_pred))


    def train_predict(clf, X_train, y_train, X_test, y_test):
        ''' Train and predict using a classifer based on F1 score. '''

        # Indicate the classifier and the training set size
        print("Training a {} using a training set size of {}. . .".format(clf.__class__.__name__, len(X_train)))

        # Train the classifier
        train_classifier(clf, X_train, y_train)

        # Print the results of prediction for both training and testing
        f1, acc = predict_labels(clf, X_train, y_train)
        print(f1, acc)
        print("F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1, acc))

        f1, acc = predict_labels(clf, X_test, y_test)
        print("F1 score and accuracy score for test set: {:.4f} , {:.4f}.".format(f1, acc))


    # produces a prediction model in the form of an ensemble of weak prediction models, typically decision tree

    # the outcome (dependent variable) has only a limited number of possible values.
    # Logistic Regression is used when response variable is categorical in nature.
    from sklearn.linear_model import LogisticRegression
    # A random forest is a meta estimator that fits a number of decision tree classifiers
    # on various sub-samples of the dataset and use averaging to improve the predictive
    # accuracy and control over-fitting.
    from sklearn.ensemble import RandomForestClassifier
    # a discriminative classifier formally defined by a separating hyperplane.
    from sklearn.svm import SVC

    # Initialize the three models (XGBoost is initialized later)
    clf_A = LogisticRegression(random_state=42)
    clf_B = SVC(random_state=912, kernel='rbf')

    train_predict(clf_A, X_train, y_train, X_test, y_test)
    print()
    clf_A.predict(X_test[2])

    print()
    train_predict(clf_B, X_train, y_train, X_test, y_test)
    print()

    from sklearn.model_selection import GridSearchCV
    from sklearn.metrics import make_scorer

    # TODO: Create the parameters list you wish to tune
    parameters = {'learning_rate': [0.1],
                  'n_estimators': [40],
                  'max_depth': [3],
                  'min_child_weight': [3],
                  'gamma': [0.4],
                  'subsample': [0.8],
                  'colsample_bytree': [0.8],
                  'scale_pos_weight': [1],
                  'reg_alpha': [1e-5]
                  }

    # TODO: Initialize the classifier
    clf = LogisticRegression(random_state=42)
    print(clf.get_params().keys())
    # print(clf.estimator.get_params().keys())
    # TODO: Make an f1 scoring function using 'make_scorer'
    f1_scorer = make_scorer(f1_score, pos_label='Team1')
    print(f1_scorer)

    # TODO: Perform grid search on the classifier using the f1_scorer as the scoring method
    grid_obj = GridSearchCV(clf,
                            scoring=f1_scorer,
                            param_grid=parameters,
                            cv=5)

    # TODO: Fit the grid search object to the training data and find the optimal parameters
    grid_obj = grid_obj.fit(X_train, y_train)

    # Get the estimator
    clf = grid_obj.best_estimator_

    # Report the final F1 score for training and testing after parameter tuning
    f1, acc = predict_labels(clf, X_train, y_train)
    print("F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1, acc))

    f1, acc = predict_labels(clf, X_test, y_test)
    print("F1 score and accuracy score for test set: {:.4f} , {:.4f}.".format(f1, acc))

    # data = csv_reader('refactoredData.csv')[1:]
    #
    # # region test
    # wins = collections.defaultdict(int)
    # matches = collections.defaultdict(int)
    # maps = collections.defaultdict(int)
    # tt = collections.defaultdict(list)
    # index = round(len(data) / 5)
    # # print(index)
    # # ['KOVA', 'l', 'LDLC', 'w', '11-5-20 ', 'Dust2', 'Home Sweet Home Cup 5 Closed Qualifier']
    #
    # for row in data[:index]:
    #     # for t1 in [*row]:
    #     #     print(t1)
    #     tt[row[0].strip()].append((row[5].strip(), row[2].strip(), row[1].strip()))
    #     matches[row[0].strip()] += 1
    #     matches[row[2].strip()] += 1
    #     maps[row[-2].strip()] += 1
    #     if row[1].strip() == 'l':
    #         wins[row[2].strip()] += 1
    #     else:
    #         wins[row[0].strip()] += 1
    #
    # # print(row)
    # # print(data[0])
    # # for team, m in matches.items():
    # #     print(team, m)
    # print(matches)
    # # print(wins['KOVA'])
    # print(wins)
    # print(maps)
    # print(tt)
    # # endregion
