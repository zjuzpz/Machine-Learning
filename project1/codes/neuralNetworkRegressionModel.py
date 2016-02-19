# -*- coding: utf-8 -*-
"""
@author: Peizhe
"""
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
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

input_size, hidden, output = len(xData[0][0]), 3, 1
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
    ds = SupervisedDataSet(input_size, output)
    for k in range(len(xTrain)):
        ds.addSample(xTrain[k], yTrain[k])

    net = buildNetwork(input_size, hidden, output, bias = True)
#    trainer = BackpropTrainer(net, ds)
 #   trainer = BackpropTrainer(net, ds, momentum = 0.1, verbose = True, weightdecay =0.01)
 #   trainer.trainUntilConvergence()    
 #   trainer.trainEpochs(epochs = 500)   
#    trainer.trainUntilConvergence(maxEpochs = 500)
#    trainer.train()
    trainer = BackpropTrainer(net, ds, learningrate = 0.001, verbose = True, momentum = 0)
#    trainer.trainUntilConvergence(dataset=ds, maxEpochs=500)
    trainer.trainEpochs(epochs = 500)
    predicted = []
    for test in xTest:
        predicted.append(net.activate(test))
    """
    out = SupervisedDataSet(input_size, output)
    for i in range(len(xTest)):
        temp = [0]
        out.addSample(xTest[i], temp)
    predicted = net.activateOnDataset(out) 
    """ 
    curRMSE = calRMSE(yReal, predicted)
    res += list(predicted)
    RMSE.append(curRMSE)
    print(sum(RMSE) * 1.0 / len(RMSE))
   
"""   

for i in range(len(xTrain)):
    ds.addSample(xTrain[i], yTrain[i])
trainer = BackpropTrainer(net, ds, momentum = 0.1, verbose = True, weightdecay =0.01)
#trainer.trainEpochs(epochs = 100)
out = SupervisedDataSet(input_size, output)
for i in range(len(xTest)):
    temp = [0]
    out.addSample(xTest[i], temp)
out = net.activateOnDataset(out)
print(out)
"""