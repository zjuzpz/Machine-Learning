import json
import matplotlib.pyplot as plt
import datetime, time


def solution1():
    print("Start problem1")
    tags = ['tweets_#gohawks', 'tweets_#gopatriots', 'tweets_#nfl', \
    'tweets_#patriots', 'tweets_#sb49', 'tweets_#superbowl']
    #f = open('data/tweet_data/tweets_#gopatriots.txt')
    
    res = {tag : {} for tag in tags}
    nfl, uniqueNfl = [], set()
    superbowl, uniqueSuperbowl = [], set()
    # The time is from the 2 weeks before the game to a week after the game
    start_date = datetime.datetime(2015,01,16, 12,0,0)
    end_date = datetime.datetime(2015,02,07, 15,0,0)
    mintime = int(time.mktime(start_date.timetuple()))
    maxtime = int(time.mktime(end_date.timetuple()))
    
    for tag in tags:
        print("start read data of " + tag)
        f = open('data/tweet_data/' + tag + '.txt')
        line = f.readline()
        count = 0
        users = set()
        followers = 0
        retweet = 0
        while len(line) != 0:
            tweet = json.loads(line)
            #deal with superbowl and nfl
            if mintime < tweet['firstpost_date'] < maxtime:
                if tag == 'tweets_#nfl':
                    h = (tweet['firstpost_date'] - mintime) // 3600
                    nfl.append(h)
                    uniqueNfl.add(h)
                if tag == 'tweets_#superbowl':
                    h = (tweet['firstpost_date'] - mintime) // 3600
                    superbowl.append(h)
                    uniqueSuperbowl.add(h)
                count += 1
                user = tweet['tweet']['user']
                if user['id'] not in users:
                    users.add(user['id'])
                    followers += user['followers_count']
                retweet += tweet["metrics"]["citations"]["total"]
                if count % 50000 == 0:
                    print("Have read " + str(count) + " tweets")
            line = f.readline()
        res[tag]['totalNumber'] = count
        res[tag]['follower'] = followers * 1.0 / len(users)
        res[tag]['retweet'] = retweet * 1.0 / count
        f.close()
    hours = (maxtime - mintime) / 3600
    print("Finish read all data!")
    print("Results: ")
    for tag in res:
        print(tag + ": Average number of tweets per hour :" + str(res[tag]['totalNumber'] / hours))
        print(tag + ": Average number of followers of users posting the tweets: " + str(res[tag]['follower']))
        print(tag + ": Average number of retweets: " + str(res[tag]['retweet']))
    
    plt.hist(nfl, bins = len(uniqueNfl))
    plt.title("NFL")
    plt.xlabel("Time(hour)")
    plt.ylabel("Number of tweets per hour")
    plt.show()  
    plt.hist(superbowl, len(uniqueSuperbowl))
    plt.title("Superbowl")
    plt.xlabel("Time(hour)")
    plt.ylabel("Number of tweets per hour")  
    plt.show()
    
if __name__ == "__main__":
    solution1()



