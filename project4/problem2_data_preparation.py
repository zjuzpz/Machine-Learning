import json
import datetime, time

def dataPreparation():
    tags = ['tweets_#gohawks', 'tweets_#gopatriots', 'tweets_#nfl', \
    'tweets_#patriots', 'tweets_#sb49', 'tweets_#superbowl']
    #f = open('data/tweet_data/tweets_#gopatriots.txt')
    # The time is from the 2 weeks before the game to a week after the game
    start_date = datetime.datetime(2015,01,16, 12,0,0)
    end_date = datetime.datetime(2015,02,07, 15,0,0)
    mintime = int(time.mktime(start_date.timetuple()))
    maxtime = int(time.mktime(end_date.timetuple()))
    hours = (maxtime - mintime) // 3600
    
    total = 0
    for tag in tags:
        print("start read data of " + tag)
        #i is the hours after start time
        lookup = [{"tweets" : 0, "retweets" : 0, "followers": 0, "maxFollowers" : 0, "time": (i + 12) % 24} for i in range(hours)]
        f = open('data/tweet_data/' + tag + '.txt')
        line = f.readline()  
        count = 0
        while len(line) != 0:
            tweet = json.loads(line)
            if mintime < tweet['firstpost_date'] < maxtime:                        
                hour = (tweet['firstpost_date'] - mintime) // 3600
                lookup[hour]["tweets"] += 1
                lookup[hour]["retweets"] += tweet["metrics"]["citations"]["total"]
                lookup[hour]["followers"] += tweet["author"]["followers"]
                lookup[hour]["maxFollowers"] = max(lookup[hour]["maxFollowers"], tweet["author"]["followers"])
            count += 1
            if count % 50000 == 0:
                print("Have read " + str(count) + " tweets")
            line = f.readline() 
        f.close()
        fw = open("problem 2 " + tag + " data.txt", "w")
        for hour in range(len(lookup)):
            fw.write(str(lookup[hour]["tweets"]) + " " + str(lookup[hour]["retweets"]) \
            + " " + str(lookup[hour]["followers"]) + " " + str(lookup[hour]["maxFollowers"]) \
            + " " + str(lookup[hour]["time"]) + "\n")
        fw.close()
        total += count
        print("Finish preparing data for " + tag)
    print("Finish preparing all data! The number of total tweets is " + str(total) + "!")
    




