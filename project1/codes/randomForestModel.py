# -*- coding: utf-8 -*-
"""
@author: Peizhe
"""

from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

#Read data
f1 = open('random_data_backup_dataset.csv')
header = f1.readline()
d = f1.readlines()
f1.close()
data = [d[i].split(",") for i in range(len(d))]
portionLength = len(data) // 10

def convert(l):
    weekdayMap = {"Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4, "Friday":5, "Saturday":6,"Sunday":7}
    res = []
    res.append(l[0])
    res.append(weekdayMap[l[1]])
    res.append(l[2])
    res.append(l[3].split("_")[-1])
    res.append(l[4].split("_")[-1])
    res.append(l[6][0])
    return res

def calRMSE(yReal, yPredict):
    res = 0
    for i in range(len(yReal)):
        res += (float(yReal[i]) - float(yPredict[i])) ** 2
    return (res * 1.0 / len(yReal)) ** 0.5

model= RandomForestRegressor(n_estimators = 20, max_depth = 12, max_features = 6)

# Convert the data and partition the data into 10 parts (Last (len(data) % 10) data will be lost)
xData, yData, temXData, temYData, count = [], [], [], [], 0
for d in data:
    count += 1
    if count == portionLength:
        count = 0
        xData.append(temXData)
        yData.append(temYData)
        temXData, temYData = [], []
    temXData.append(convert(d))
    temYData.append(d[5])    

#10 test, every test use 90% data to train, and 10% data to test
res = []
RMSE = []
for i in range(10):
    xTrain, yTrain = [], []
    for j in range(10):
#Predict data        
        if j == i:
            xTest = xData[j]
            yReal = yData[j]
        else:
            xTrain += xData[j]
            yTrain += yData[j]
    model.fit(xTrain, yTrain)
    predicted = model.predict(xTest)
    curRMSE = calRMSE(yReal, predicted)
    res += list(predicted)
    print(curRMSE)
    RMSE.append(curRMSE)
    plt.scatter(range(len(xTest)), yReal,  color='black')
    plt.scatter(range(len(xTest)), predicted, color='blue')
    plt.show()

#Use all predicted data to replace the real data
for i in range(len(res)):
    data[i][5] = str(res[i])
#Write the predicted data to file
f1 = open('predicted network_backup_dataset.csv', 'w')
f1.write(header)
for i in range(len(data)):
    f1.write(",".join(data[i]))
f1.close()

print("RMSE =", RMSE)
print("Average RMSE = ", sum(RMSE) / len(RMSE))