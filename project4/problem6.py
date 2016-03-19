from scipy.stats.stats import pearsonr
from problem6_getTweets import getTweets

tags = ['tweets_#gohawks', 'tweets_#gopatriots', 'tweets_#nfl', \
'tweets_#patriots', 'tweets_#sb49', 'tweets_#superbowl']
#f = open('data/tweet_data/tweets_#gopatriots.txt')

def solution6():
    lookup = getTweets()
    for i in tags:
        for j in tags:
            print (pearsonr(lookup[i],lookup[j]))
            
if __name__ == "__main__":
    solution6()

