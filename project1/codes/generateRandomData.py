import random
f1 = open('network_backup_dataset.csv')
l = f1.readlines()
f1.close()
header = l[0]
data = l[1:]
data[-1] += "\n"
random.shuffle(data)
f2 = open('random_data_backup_dataset.csv', 'w')
f2.write(header)
for i in range(len(data)):
    f2.write(data[i])
f2.close()
