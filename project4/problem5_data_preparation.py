import json
import datetime, time
import os

def dataPreparation_for_5():

    for i in range(1,11):
        for j in range(1,4):
            if os.path.isfile('data/test_data/sample' + str(i) + '_period'+str(j)+'.txt'):
                f = open('data/test_data/sample' + str(i) + '_period'+str(j)+'.txt')
                filename='sample' + str(i) + '_period'+str(j)+'.txt'
                line = f.readline()

                start_date = datetime.datetime(2015,01,16, 12,0,0)
                end_date = datetime.datetime(2015,02,07, 15,0,0)
                mintime = int(time.mktime(start_date.timetuple()))
                maxtime = int(time.mktime(end_date.timetuple()))
                hours = (maxtime - mintime) // 3600

                total=0
                #lookup = [{"tweets" : 0, "retweets" : 0, "followers": 0, "maxFollowers" : 0, "time": (k + 12) % 24} for k in range(hours)]
                lookup = [{"tweets" : 0, "retweets" : 0, "followers": 0, "maxFollowers" : 0, "time": (i + 12) % 24, "rankingScore": 0, "friendsCount": 0} for i in range(hours)]

                count = 0
                while len(line) != 0:
                    tweet = json.loads(line)
                    if mintime < tweet['firstpost_date'] < maxtime:
                        hour = (tweet['firstpost_date'] - mintime) // 3600
                        lookup[hour]["tweets"] += 1
                        lookup[hour]["retweets"] += tweet["metrics"]["citations"]["total"]
                        lookup[hour]["followers"] += tweet["author"]["followers"]
                        lookup[hour]["maxFollowers"] = max(lookup[hour]["maxFollowers"], tweet["author"]["followers"])
                        lookup[hour]["rankingScore"] = tweet["metrics"]["ranking_score"]
                        lookup[hour]["friendsCount"] = tweet["tweet"]["user"]["friends_count"]
                    count += 1
                    if count % 50000 == 0:
                        print("Have read " + str(count) + " tweets")
                    line = f.readline()
                f.close()
                fw = open("problem 5 " + filename, "w")
                for hour in range(len(lookup)):
                    if lookup[hour]["tweets"]!=0:
                        fw.write(str(lookup[hour]["tweets"]) + " " + str(lookup[hour]["retweets"]) \
                        + " " + str(lookup[hour]["followers"]) + " " + str(lookup[hour]["rankingScore"])+ " " + str(lookup[hour]["friendsCount"]) \
                        + " " + str(lookup[hour]["maxFollowers"]) + " " + str(lookup[hour]["time"]) + "\n")
                        # fw.write(str(lookup[hour]["tweets"]) + " " + str(lookup[hour]["retweets"]) \
                        # + " " + str(lookup[hour]["followers"]) + " " + str(lookup[hour]["maxFollowers"]) \
                        # + " " + str(lookup[hour]["time"]) + "\n")
                fw.close()
                total += count
                print("Finish preparing data for " + filename)
        print("Finish preparing all data! The number of total tweets is " + str(total) + "!")

#dataPreparation_for_5()



