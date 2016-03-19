# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 21:41:45 2016

@author: Yu
"""

import statsmodels.api as sm
import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import RandomForestRegressor

def solution4():
    tags = ['tweets_#gohawks', 'tweets_#gopatriots', 'tweets_#nfl', \
    'tweets_#patriots', 'tweets_#sb49', 'tweets_#superbowl']
    
    # row index for Feb 1st, 8:00am, 8:00 pm
    before_active = 380
    after_active = 392
    
    for tag in tags:
        tweets, parameters = [], []
        f = open('problem 3 ' + tag + ' data.txt')
        line = f.readline()
        while len(line):
            p = line.split()
            tweets.append(float(p[0]))
            parameters.append([float(p[i]) for i in range(len(p))])
            line = f.readline()
        del(tweets[0])
        parameters.pop()
        # generate training data X, y
        X = np.matrix(parameters)
        y = np.array(tweets)

        
        # split 3 periods 
        X_before_active = X[0:before_active,:]
        y_before_active = y[0:before_active]
        X_active = X[before_active:after_active+1, :]
        y_active = y[before_active:after_active+1]
        X_after_active = X[after_active+1:530, :]
        y_after_active = y[after_active+1:530]
        
        # training model before Feb.1, 8:00am
        errors = []
        test_data_x, test_data_y = [],[]
        train_data_x, train_data_y = [],[]
        print("average score for " + tag)
        for i in range(10):
            test_data_x = X_before_active[i*38 : (i+1)*38]
            test_data_y = y_before_active[i*38 : (i+1)*38]
            for j in range(i*38, (i+1)*38):
                train_data_x = np.delete(X_before_active, j, axis=0)
                train_data_y = np.delete(y_before_active, j, axis=0)
            res = sm.OLS(train_data_y, train_data_x).fit()
            predicted = res.predict(test_data_x)
            sum_error = 0
            for idx in range(0, 38):
                sum_error += abs(test_data_y[idx]-predicted[idx])
            errors.append(sum_error*1.0/38)
        print "before active: %.3f" % np.mean(errors)
        
        # training model during Feb.1, 8:00am - 8:00pm
        scores_active = cross_validation.cross_val_score(RandomForestRegressor(n_estimators = 50, max_depth = 30), X_active, y_active, cv=10, scoring='mean_absolute_error')
        ave_score_active = np.average(np.abs(scores_active))
        print "during active: %.3f" % ave_score_active
        
        # training model after Feb.1, 8:00pm
        errors = []
        test_data_x, test_data_y = [],[]
        train_data_x, train_data_y = [],[]
        for i in range(10):
            test_data_x = X_after_active[i*13 : (i+1)*13]
            test_data_y = y_after_active[i*13 : (i+1)*13]
            for j in range(i*13, (i+1)*13):
                train_data_x = np.delete(X_after_active, j, axis=0)
                train_data_y = np.delete(y_after_active, j, axis=0)
            res = sm.OLS(train_data_y, train_data_x).fit()
            predicted = res.predict(test_data_x)
            sum_error = 0
            for idx in range(0, 13):
                sum_error += abs(test_data_y[idx]-predicted[idx])
            errors.append(sum_error*1.0/13)
        print "after active: %.3f" % np.mean(errors)
        f.close()
        
if __name__ == "__main__":
    solution4()