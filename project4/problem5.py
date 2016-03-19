from problem5_data_preparation import dataPreparation_for_5
import os
from models import getModels

def solution5():
    print("Start problem 5")
    print("Start data preparation for problem 5")
    dataPreparation_for_5()
    print("Results: ")
    
    
    model=getModels()
    
    for i in range(1,11):
        for j in range(1,4):
            filename='problem 5 sample'+str(i)+'_period'+str(j)+'.txt'
            tweets,parameters=[],[]
            prediction=[]
            #f = open('problem 5 sample'+str(i)+'_period'+'j'+'.txt')
            if os.path.isfile('problem 5 sample'+str(i)+'_period'+str(j)+'.txt'):
                print filename,'problem 5 sample'+str(i)+'_period'+str(j)+'.txt'
                f = open('problem 5 sample'+str(i)+'_period'+str(j)+'.txt')
                line = f.readline()
                while len(line):
                    p = line.split()
                    tweets.append(float(p[0]))
                    parameters.append([float(p[i]) for i in range(len(p))])
                    line = f.readline()
    
                    # del(tweets[0])
                    # next_hour_tweets = tweets
                    # parameters.pop()
                    #print parameters, tweets
                # X=[1,1,1,1,1]
                # y=[1]
                # model=[]
                # for i in range(3):
                #     clf=linear_model.LinearRegression()
                #     clf.fit(X,y)
                #     model.append(clf)
    
                clf=model[j-1]
                prediction=clf.predict(parameters)
                #print parameters, tweets
                print "prediction of tweets in next hour of "+filename
                print prediction[-1]
                f.close()

if __name__ == "__main__":
    solution5()
