import statsmodels.api as sm
from problem2_data_preparation import dataPreparation

def solution2():
    print("Start problem 2")
    print("Start data preparation for problem 2")
    dataPreparation()
    print("Results: ")
    tags = ['tweets_#gohawks', 'tweets_#gopatriots', 'tweets_#nfl', \
    'tweets_#patriots', 'tweets_#sb49', 'tweets_#superbowl']
    #tweets, retweets, sum of followers, maximum followers, time of the day
    for tag in tags:
        tweets, parameters = [], []
        f = open('problem 2 ' + tag + ' data.txt')
        line = f.readline()
        while len(line):
            p = line.split()
            tweets.append(float(p[0]))
            parameters.append([float(p[i]) for i in range(len(p))])
            line = f.readline()
        del(tweets[0])
        next_hour_tweets = tweets
        parameters.pop()
        res = sm.OLS(next_hour_tweets, parameters).fit()
        print("Result of " + tag)
        print(res.summary())
        f.close()
        
if __name__ == "__main__":
    solution2()