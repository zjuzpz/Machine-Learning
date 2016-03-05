import matplotlib.pyplot as plt
#Read actual data
f1 = open('problem5data/actualData.txt')
data = f1.readlines()
f1.close()
v = [d.split() for d in data]
print(len(v))
print(len(v[0]))
print(v[0].count("0"))

#Read predicted data k = 10
f1 = open('problem5data/predictedR1.txt')
data = f1.readlines()
f1.close()
def getResults(data, L = 5, nums = [1.0]):
    data = [d.split() for d in data]
    predict = []
    for i in range(len(data)):
        cur = []
        for j in range(len(data[i])):
            num = float(data[i][j])
            cur.append((num, j))
        cur.sort(reverse = True)
        predict.append(cur)
    
    precision, nums, totalHit, total = 0, [1.0], 0, 0
    for threshold in nums:
        hit, count, res = 0, 0, []
        for i in range(len(predict)):
            tem = L
            for j in range(len(predict[i])):
                movieId = predict[i][j][1]
                if int(v[i][movieId]) > 3:
                    total += 1
                if predict[i][j][0] <= threshold and tem:
                    if v[i][movieId] != "0":
                        tem -= 1
                        if int(v[i][movieId]) > 3:
                            hit += 1
                        else:
                            res.append(v[i][movieId])
                    else:
                        count += 1
        totalHit += hit
        precision = max(precision, hit / (L * len(predict)))      
        print("L = {}, Precision = {}".format(L, precision))
    far = 1 - precision
    hitRate = totalHit / total
    return far, hitRate

if __name__ == "__main__":
    #Read predicted data k = 10
    f1 = open('problem5data/predictedR1.txt')
    data = f1.readlines()
    f1.close()
    getResults(data)
    x1, y1 = [], []
    for L in range(1, 150):
        far, hitRate = getResults(data, L, nums = [1.3])
        x1.append(far)
        y1.append(hitRate)
    
    #Read predicted data k = 50
    f1 = open('problem5data/predictedR2.txt')
    data = f1.readlines()
    f1.close()
    getResults(data)
    x2, y2 = [], []
    for L in range(1, 150):
        far, hitRate = getResults(data, L, nums = [1.3])
        x2.append(far)
        y2.append(hitRate)
    
    #Read predicted data k = 100
    f1 = open('problem5data/predictedR3.txt')
    data = f1.readlines()
    f1.close()
    getResults(data)
    x3, y3 = [], []
    for L in range(1, 150):
        far, hitRate = getResults(data, L, nums = [1.3])
        x3.append(far)
        y3.append(hitRate)
        
    plt.plot(x1, y1, x2, y2, x3, y3)
    plt.legend(['k = 10', 'k = 50', 'k = 100'], loc = 0) 
    plt.xlabel('False alarm rate')
    plt.ylabel('hit rate)')
    plt.title('False-alarm rate VS hit rate with different k')    
    plt.show()
