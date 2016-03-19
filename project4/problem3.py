# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 00:45:17 2016

@author: Yu
"""

import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from problem3_data_preparation import data_preparation
   

# the plot function 
def scatterPlot(idx,idx1, idx2, idx3, X, y,tag):
    features = ["tweets", "retweets", "followers", "rankingScore", "friendsCount", "maxFollowers", "time"]

    plt.figure(idx+1)
    plt.title('scatter plot for ' + tag)
    plt.subplot(311)             # the 1st subplot 
    plt.xlabel(features[idx1])
    plt.ylabel('next_hour_tweets')
    plt.plot(X[:,idx1],y,'o')
    
    plt.subplot(312)             # the 2nd subplot 
    plt.xlabel(features[idx2])
    plt.ylabel('next_hour_tweets')
    plt.plot(X[:,idx2],y,'o')
    
    plt.subplot(313)             # the 3rd subplot 
    plt.xlabel(features[idx3])
    plt.ylabel('next_hour_tweets')
    plt.plot(X[:,idx3],y,'o')

    plt.show()
    
    
def solution3():
    print("Start problem 3")
    print("Start data preparation for problem 3")
    # firstly prepare data for problem 3, all text files will be saved at current path
    data_preparation()
    print("Results: ")
    
    tags = ['tweets_#gohawks', 'tweets_#gopatriots', 'tweets_#nfl', \
    'tweets_#patriots', 'tweets_#sb49', 'tweets_#superbowl']
    
    # idx for tag index in tags
    idx=0
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
        next_hour_tweets = np.array(tweets)
        parameters.pop()
        X = np.matrix(parameters)
        res = sm.OLS(next_hour_tweets, X).fit()
        print("Result of " + tag)
        print(res.summary())
        if tag == 'tweets_#gohawks' or tag=='tweets_#nfl' or tag=='tweets_#patriots':
            scatterPlot(idx,0,1,2,X,next_hour_tweets,tag)
        elif tag ==  'tweets_#gopatriots':
            scatterPlot(idx,1,3,4,X,next_hour_tweets, tag)
        elif tag == 'tweets_#sb49':
            scatterPlot(idx,0,1,5,X,next_hour_tweets,tag)
        elif tag == 'tweets_#superbowl':
            scatterPlot(idx,0,2,5,X, next_hour_tweets,tag)
        idx += 1    
        f.close()
        
if __name__ == "__main__":
    solution3()