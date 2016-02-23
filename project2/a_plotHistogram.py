# -*- coding: utf-8 -*-

from sklearn.datasets import fetch_20newsgroups
import matplotlib.pyplot as plt

newsgroups_train = fetch_20newsgroups(subset='train')
categories = list(newsgroups_train.target_names)
graphics_train = fetch_20newsgroups(subset = 'train',\
categories = categories, shuffle = True, random_state = 42)
plt.hist(graphics_train.target, bins = 20)
plt.axis([0, 20, 0, 700])
plt.title("Distribution of Documents")
plt.xlabel("The 20 Different Classes")
plt.ylabel("The Frequency Count")
categories = ["comp.graphics", "comp.os.ms-windows.misc", \
"comp.sys.ibm.pc.hardware", "comp.sys.mac.hardware"]
graphicsComputerTechnology = fetch_20newsgroups(subset = 'train', categories = categories)
print("The number of total documents :", len(graphics_train.target))
print("The number of documents of computer technology :", len(graphicsComputerTechnology.target))
categories = ["rec.autos", "rec.motorcycles", \
"rec.sport.baseball", "rec.sport.hockey"]
graphicsRecreationalActivity = fetch_20newsgroups(subset = 'train',categories = categories)
print("The number of documents of recreational activity :", len(graphicsRecreationalActivity.target))
#plt.hist()