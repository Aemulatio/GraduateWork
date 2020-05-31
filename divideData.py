import csv
import collections
import pandas as pd
from IPython.display import display
import numpy as np
import os
import time
import category_encoders as ce
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder


def csv_reader(path):
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


if __name__ == "__main__":

    # files = os.listdir("Data/More/")
    # print(files)
    # for file in files:
    #     print(pd.read_csv("Data/More/"+file))
    data = pd.read_csv("Data/results1_wo_garbage_NTN.csv")
    display(data.head())
    # Получаем все команды
    UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
    print(pd.Index(UniqueTeams).get_loc('LDLC'))
    # print(UniqueTeams.get("LDLC"))
    # print(pd.g)

    # Получаем все карты, на которых играли команды
    UniqueMaps = pd.Series(np.unique(data['Map'].unique()))

    # Создаем энкодер
    enc_map = OrdinalEncoder()
    # Кодируем названия Карт
    Map = pd.DataFrame(data['Map'])
    Map = enc_map.fit_transform(Map)
    data = data.drop(['Map'], 1)
    data.insert(5, "Map", Map, True)

    for id, team in UniqueTeams.items():
        data = data.replace(team, id)

    data = data.drop(['Team1_Score', 'Team2_Score'], 1)

    X_all = data.drop(['Winner'], 1)
    y_all = data['Winner']

    # Standardising the data.
    from sklearn.preprocessing import scale

    # # Center to the mean and component wise scale to unit variance.
    # cols = [['Team1', 'Team2', 'Team1_Score', 'Team2_Score']]
    # cols = [['Team1', 'Team2', 'Team1_Score', 'Team2_Score', 'Map']]
    cols = [['Team1', 'Team2', 'Map']]


    # for col in cols:
    #     X_all[col] = scale(X_all[col])

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


    X_all = preprocess_features(X_all)

    from sklearn.model_selection import train_test_split

    # Shuffle and split the dataset into training and testing set.
    X_train, X_test, y_train, y_test = train_test_split(X_all, y_all,
                                                        test_size=0.28,  # ПОЧИТАТЬ
                                                        random_state=42, )
    # stratify=y_all)

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
    clf_A = LogisticRegression(random_state=42, penalty='l2')
    clf_B = SVC(random_state=912, kernel='rbf')

    train_predict(clf_A, X_train, y_train, X_test, y_test)
    print()
    print(type(X_test))
    # print(clf_A.predict([["London", 'PACT', 'Mirage']]))
    # print(clf_A.predict(X_test[1, :]))

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
    # ['C', 'class_weight', 'dual', 'fit_intercept', 'intercept_scaling', 'l1_ratio', 'max_iter', 'multi_class',
    # 'n_jobs', 'penalty', 'random_state', 'solver', 'tol', 'verbose', 'warm_start']
    # TODO: Initialize the classifier
    clf = LogisticRegression(random_state=42)
    from sklearn import ensemble

    # ------------------------
    rf = ensemble.RandomForestClassifier(n_estimators=1000, random_state=11)
    rf.fit(X_train, y_train)

    err_train = np.mean(y_train != rf.predict(X_train))
    err_test = np.mean(y_test != rf.predict(X_test))
    print(err_train, err_test)
    print(type(X_test))
    # TEST = pd.DataFrame({
    #     "Team1": ["SKADE"],
    #     "Team2": ["Brute"],
    #     "Map": ["Dust2"]
    # })
    TEST = pd.DataFrame({
        "Team1": 1,
        "Team2": 257,
        "Map": 3  # t2
    }, index=[0])
    TEST1 = pd.DataFrame({
        "Team1": 30,
        "Team2": 84,
        "Map": 5
    }, index=[0])
    print("Введите название команды")
    t1 = input()
    print("Введите название команды")
    t2 = input()
    print(UniqueMaps)
    print("Введите название карты")
    m = input()
    print(pd.Index(UniqueTeams).get_loc(t1))
    print(pd.Index(UniqueTeams).get_loc(t2))
    print(pd.Index(UniqueMaps).get_loc(m))

    vvod = pd.DataFrame({
        "Team1": pd.Index(UniqueTeams).get_loc(t1),
        "Team2": pd.Index(UniqueTeams).get_loc(t2),
        "Map": pd.Index(UniqueMaps).get_loc(m),
    }, index=[0])
    print("ВВЕДЕННЫЕ: ")
    print(vvod)

    print(rf.predict(vvod))
    print(clf_A.predict(vvod))
    print(clf_B.predict(vvod))


    print(TEST)
    print(rf.predict(TEST))
    print(rf.predict(TEST1))

    print(clf_A.predict(TEST))
    print(clf_A.predict(TEST1))
    print(clf_B.predict(TEST))
    print(clf_B.predict(TEST1))
