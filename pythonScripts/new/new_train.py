from pymongo import MongoClient
import pandas as pd
import numpy as np
from time import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn import ensemble
import pickle
from db import connectionString


def getAllData():
    """
    Получает всю таблицу статы
    :return:
    """
    collection = db.Prepare_01
    data = list()
    # data.append([
    #     'winner',
    #     'team1',
    #     'team1_p1',
    #     'team1_p2',
    #     'team1_p3',
    #     'team1_p4',
    #     'team1_p5',
    #     'team2',
    #     'team2_p1',
    #     'team2_p2',
    #     'team2_p3',
    #     'team2_p4',
    #     'team2_p5',
    #     'map'
    # ])
    for obj in collection.find():
        data.append(
            [obj['winner'],
             # obj['team1'],
             obj['t1_rating'],
             obj['t1_dpr'],
             obj['t1_kast'],
             obj['t1_impact'],
             obj['t1_adr'],
             obj['t1_kpr'],
             # obj['team2'],
             obj['t2_rating'],
             obj['t2_dpr'],
             obj['t2_kast'],
             obj['t2_impact'],
             obj['t2_adr'],
             obj['t2_kpr'],
             # obj['map'],
             ]
        )
    # [winner, team1['name'], team1['player1'], team1['player2'], team1['player3'], team1['player4'],
    #  team1['player5'], team2['name'], team2['player1'], team2['player2'], team2['player3'],
    #  team2['player4'], team2['player5'], map]
    return data


if __name__ == "__main__":
    client = MongoClient(connectionString)
    db = client.Diploma
    allData = getAllData()
    data = pd.DataFrame(allData, columns=[
        'winner',
        # 'team1',
        'team1_p1',
        'team1_p2',
        'team1_p3',
        'team1_p4',
        'team1_p5',
        'team1_p6',
        # 'team2',
        'team2_p1',
        'team2_p2',
        'team2_p3',
        'team2_p4',
        'team2_p5',
        'team2_p6',
        # 'map'
    ])
    # print(type(allData))
    # data = pd.read_csv(getAllData())
    print(data)
    # Получаем все команды
    # UniqueTeams = pd.Series(np.unique(np.concatenate((data['team1'].unique(), data['team2'].unique()))))
    # Получаем все карты, на которых играли команды
    # UniqueMaps = pd.Series(np.unique(data['map'].unique()))

    X_all = data.drop(['winner'], 1)
    y_all = data['winner']

    cols = [['team1', 'team1_p1', 'team1_p2', 'team1_p3', 'team1_p4', 'team1_p5', 'team1_p6', 'team2_p1', 'team2_p2',
             'team2_p3', 'team2_p4', 'team2_p5', "team2_p6"]]


    def preprocess_features(X):
        ''' Preprocesses the data and converts catagorical variables into dummy variables. '''

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


    print(X_all)
    X_all = preprocess_features(X_all)
    print(X_all)

    # Shuffle and split the dataset into training and testing set.
    X_train, X_test, y_train, y_test = train_test_split(X_all, y_all,
                                                        test_size=0.28,
                                                        random_state=42, )


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
        from sklearn.metrics import max_error
        from sklearn.metrics import explained_variance_score
        from sklearn.metrics import r2_score

        # Start the clock, make predictions, then stop the clock
        start = time()
        y_pred = clf.predict(features)

        end = time()
        # Print and return results
        print("Made predictions in {:.4f} seconds.".format(end - start))

        # return f1_score(target, y_pred, average="macro"), sum(target == y_pred) / float(len(y_pred))
        # return max_error(target, y_pred), sum(target == y_pred) / float(len(y_pred))
        # return explained_variance_score(target, y_pred), sum(target == y_pred) / float(len(y_pred))
        return r2_score(target, y_pred), sum(target == y_pred) / float(len(y_pred))
        # return f1_score(target, y_pred, average="micro"), sum(target == y_pred) / float(len(y_pred))
        # return f1_score(target, y_pred, average="weighted"), sum(target == y_pred) / float(len(y_pred))
        # return f1_score(target, y_pred, pos_label='Team1'), sum(target == y_pred) / float(len(y_pred))


    def pred_prob(clf, obj):
        # Проверить дома
        return clf.predict_proba([obj])


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


    rf = ensemble.RandomForestClassifier(n_estimators=5000, random_state=11, n_jobs=-1)
    # print(rf.max_depth)
    # train_predict(rf, X_train, y_train, X_test, y_test)
    # print(pred_prob(rf, X_test.iloc[0, :]), rf.classes_)
    # print(rf.predict([X_test.iloc[0, :]]))

    gbr = ensemble.GradientBoostingRegressor(n_estimators=5000, random_state=11, )
    # train_predict(gbr, X_train, y_train, X_test, y_test)
    start1 = time()
    gbr.fit(X_train, y_train)
    end1 = time()
    print("Trained in {:.4f} seconds.".format(end1 - start1))

    # clf_A = LogisticRegression(random_state=42, penalty='l2')
    # clf_B = SVC(random_state=912, kernel='rbf')
    # clf_C = SVR()
    # clf_C.fit(X_train, y_train)
    # print(clf_C.predict([X_test.iloc[0, :]]))
    # print([X_test.iloc[0, :]])
    #
    # train_predict(clf_A, X_train, y_train, X_test, y_test)
    # print("")
    # train_predict(clf_B, X_train, y_train, X_test, y_test)
    print("")
    # train_predict(clf_C, X_train, y_train, X_test, y_test)
    print("")
