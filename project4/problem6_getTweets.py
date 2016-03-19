import json
import datetime, time

def getTweets():
    tags = ['tweets_#gohawks', 'tweets_#gopatriots', 'tweets_#nfl', \
    'tweets_#patriots', 'tweets_#sb49', 'tweets_#superbowl']
    #f = open('data/tweet_data/tweets_#gopatriots.txt')
    # The time is from the 2 weeks before the game to a week after the game
    start_date = datetime.datetime(2015,01,16, 12,0,0)
    end_date = datetime.datetime(2015,02,07, 15,0,0)
    mintime = int(time.mktime(start_date.timetuple()))
    maxtime = int(time.mktime(end_date.timetuple()))
    hours = (maxtime - mintime) // 3600
    lookup = {}
    total = 0
    for tag in tags:
        lookup[tag] = [0 for i in range(hours)]
        print("start read data of " + tag)
        #i is the hours after start time
        f = open('data/tweet_data/' + tag + '.txt')
        line = f.readline()  
        count = 0
        while len(line) != 0:
            tweet = json.loads(line)
            if mintime < tweet['firstpost_date'] < maxtime:                        
                hour = (tweet['firstpost_date'] - mintime) // 3600
                lookup[tag][hour] += 1                
            count += 1
            if count % 50000 == 0:
                print("Have read " + str(count) + " tweets")
            line = f.readline() 
        f.close()
        total += count
        print("Finish preparing data for " + tag)
    print("Finish preparing all data! The number of total tweets is " + str(total) + "!")
    return lookup
    
if __name__ == "__main__":
    lookup = getTweets()



