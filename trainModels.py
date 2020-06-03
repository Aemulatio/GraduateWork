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
    data = pd.read_csv("Data/results1_wo_garbage_NTN.csv")
    # Получаем все команды
    UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
    # Получаем все карты, на которых играли команды
    UniqueMaps = pd.Series(np.unique(data['Map'].unique()))

    for id, team in UniqueTeams.items():
        data = data.replace(team, id)
    for id, map in UniqueMaps.items():
        data = data.replace(map, id)

    data = data.drop(['Team1_Score', 'Team2_Score'], 1)

    X_all = data.drop(['Winner'], 1)
    y_all = data['Winner']

    # Standardising the data.
    from sklearn.preprocessing import scale

    # # Center to the mean and component wise scale to unit variance.
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


    X_all = preprocess_features(X_all)

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

    train_predict(clf_A, X_train, y_train, X_test, y_test)
    train_predict(clf_B, X_train, y_train, X_test, y_test)

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

    # ------------------------
    rf = ensemble.RandomForestClassifier(n_estimators=170, random_state=11)
    rf.fit(X_train, y_train)

    err_train = np.mean(y_train != rf.predict(X_train))
    err_test = np.mean(y_test != rf.predict(X_test))
    print(err_train, err_test)

    LR = 'Logistic_regression_model.sav'
    SVM_model = 'SVM_model.sav'
    RF = 'Random_forest.sav'
    pickle.dump(clf_A, open("Models/" + LR, 'wb'))
    pickle.dump(clf_B, open("Models/" + SVM_model, 'wb'))
    pickle.dump(rf, open("Models/" + RF, 'wb'))
