import csv
import pandas as pd
import numpy as np
import time
from time import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn import ensemble
import pickle

if __name__ == "__main__":
    data = pd.read_csv("../Data/results6_wo_garbage_NTN.csv")
    # Получаем все команды
    UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
    # Получаем все карты, на которых играли команды
    UniqueMaps = pd.Series(np.unique(data['Map'].unique()))

    data = data.drop(['Team1_Score', 'Team2_Score'], 1)

    X_all = data.drop(['Winner'], 1)
    y_all = data['Winner']

    for id, team in UniqueTeams.items():
        X_all = X_all.replace(team, id)
    for id, map in UniqueMaps.items():
        X_all = X_all.replace(map, id)

    print(X_all)

    # Standardising the data.
    from sklearn.preprocessing import scale

    # # Center to the mean and component wise scale to unit variance.
    # cols = [['Team1', 'Team2', 'Team1_Score', 'Team2_Score', 'Map']]
    cols = [['Team1', 'Team2', 'Map']]


    # for col in cols:
    #     X_all[col] = scale(X_all[col])

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

        # Start the clock, make predictions, then stop the clock
        start = time()
        y_pred = clf.predict(features)

        end = time()
        # Print and return results
        print("Made predictions in {:.4f} seconds.".format(end - start))

        # return f1_score(target, y_pred, average="macro"), sum(target == y_pred) / float(len(y_pred))
        # return f1_score(target, y_pred, average="micro"), sum(target == y_pred) / float(len(y_pred))
        # return f1_score(target, y_pred, average="weighted"), sum(target == y_pred) / float(len(y_pred))
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


    clf_A = LogisticRegression(random_state=42, penalty='l2')
    clf_B = SVC(random_state=912, kernel='rbf')
    # #
    # train_predict(clf_A, X_train, y_train, X_test, y_test)
    # print("")
    # train_predict(clf_B, X_train, y_train, X_test, y_test)
    # print("")
    # ------------------------
    # X_train = pd.DataFrame(X_train, dtype='float')
    #
    # X_test = pd.DataFrame(X_test, dtype='float')
    #
    rf = ensemble.RandomForestClassifier(n_estimators=1000, random_state=11, max_features=3, n_jobs=-1)
    print(rf.max_depth)
    train_predict(rf, X_train, y_train, X_test, y_test)

    # rf.fit(X_train, y_train)
    # #
    # err_train = np.mean(y_train != rf.predict(X_train))
    # err_test = np.mean(y_test != rf.predict(X_test))
    # print(err_train, err_test)

    # LR = 'Logistic_regression_model.sav'
    # SVM_model = 'SVM_model.sav'
    RF = 'RANDOM_FOREST.pickle'

    from joblib import dump, load

    # dump(rf, 'Random_forest.joblib')

    # gbt = ensemble.GradientBoostingClassifier(n_estimators=170, random_state=11)
    # print()
    # train_predict(gbt, X_train, y_train, X_test, y_test)

    # from sklearn.neighbors import KNeighborsClassifier
    #
    # knn = KNeighborsClassifier(n_neighbors=1)
    # print()
    # train_predict(knn, X_train, y_train, X_test, y_test)
    #
    # from sklearn.ensemble import ExtraTreesClassifier
    #
    # ETC = ExtraTreesClassifier(n_estimators=170, random_state=11)
    # print()
    # train_predict(ETC, X_train, y_train, X_test, y_test)

    #
    # pickle.dump(knn, open("Models/knn.sav", 'wb'))

    # from sklearn.model_selection import GridSearchCV
    #
    # n_neighbors_array = [1, 3, 5, 7, 10, 15]
    # knn = KNeighborsClassifier()
    # grid = GridSearchCV(knn, param_grid={'n_neighbors': n_neighbors_array})
    # grid.fit(X_train, y_train)
    #
    # best_cv_err = 1 - grid.best_score_
    # best_n_neighbors = grid.best_estimator_.n_neighbors
    # print(best_cv_err, best_n_neighbors)

    # pickle.dump(clf_A, open("Models/" + LR, 'wb'))
    # pickle.dump(clf_B, open("Models/" + SVM_model, 'wb'))
    pickle.dump(rf, open("../Models/" + RF, 'wb'))
