# -*- coding: utf-8 -*-
"""
    Created on Wed Feb 20 23:54:48 2016
    
    @author: Peizhe
    """
from d_truncated_SVD import getSVD
from sklearn.datasets import fetch_20newsgroups
from sklearn.svm import SVC
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from sklearn.cross_validation import KFold
import numpy
from sklearn.grid_search import GridSearchCV

#newsgroups_train = fetch_20newsgroups(subset='train')
#categories = list(newsgroups_train.target_names)
categories_computer = ["comp.graphics", "comp.os.ms-windows.misc", \
                       "comp.sys.ibm.pc.hardware", "comp.sys.mac.hardware"]
categories_recreation = ["rec.autos", "rec.motorcycles", \
                         "rec.sport.baseball", "rec.sport.hockey"]

train_data = fetch_20newsgroups(subset = 'train', categories = categories_computer + \
                                categories_recreation, shuffle = True, random_state = 42)

test_data = fetch_20newsgroups(subset = 'test', categories = categories_computer + \
                               categories_recreation, shuffle = True, random_state = 42)

total_data = fetch_20newsgroups(subset = 'all', categories = categories_computer + \
                                categories_recreation, shuffle = True, random_state = 42)

#1 for computer, -1 for recreation
for i in range(len(train_data.target)):
    if train_data.target[i] <= 3:
        train_data.target[i] = 1
    else:
        train_data.target[i] = -1

for i in range(len(test_data.target)):
    if test_data.target[i] <= 3:
        test_data.target[i] = 1
    else:
        test_data.target[i] = -1

def draw(name, y_true, y_score):
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    plt.plot(fpr, tpr)
    plt.grid()
    plt.title(name + "ROC curve")
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.show()
    
"""
Problem e: SVM Classifier
"""
#svm = sklearn.LinearSVC()
svm = SVC(kernel = "linear", probability = True, verbose = True, random_state = 42)
categories = categories_computer + categories_recreation

SVD_train = getSVD(train_data.data)
svm_fitted = svm.fit(SVD_train, train_data.target)
SVD_test = getSVD(test_data.data)
predicted = svm_fitted.predict(SVD_test)

print("Results for problem e - SVM classifier :")
print(metrics.classification_report(test_data.target, predicted))
print(metrics.confusion_matrix(test_data.target, predicted))
print(metrics.accuracy_score(test_data.target, predicted))
    
draw("SVM Classifier ", test_data.target, svm_fitted.predict_proba(SVD_test)[:, 1])


"""
Problem f: Soft margin SVM
"""
estimator = svm
param = {"range" : [1e-3, 1e3]}
svmSoft = GridSearchCV(estimator = estimator, param_grid = param, cv= 5)
SVD_train = getSVD(train_data.data)
svmSoft_fitted = svm.fit(SVD_train, train_data.target)
SVD_test = getSVD(test_data.data)
predicted = svmSoft_fitted.predict(SVD_test)

print("Results for problem f - Soft margin SVM classifier :")
print(metrics.classification_report(test_data.target, predicted))
print(metrics.confusion_matrix(test_data.target, predicted))
print(metrics.accuracy_score(test_data.target, predicted))
draw("Soft margin SVM", test_data.target, svm_fitted.predict_proba(SVD_test)[:, 1])

#"""
#Soft margin SVM
#"""
#SVD_total = getSVD(categories, dataSet = "all")
#SVD_target = total_data.target
#print(len(SVD_total), len(SVD_total[0]))
#print(len(SVD_target), SVD_target[0])
#distance = len(SVD_total) // 5
#cc = [0.01, 0.1, 1, 10, 100]
#bestScore, bestC = -float("inf"), None
#for c in [1, 10, 100, 1000]:
#    score = 0
#    svm = SVC(kernel = "linear", probability = True, \
#    verbose = True, random_state = 42, C = c)
#    for i in range(5):
#        train_data = list(SVD_total[0 : i * distance]) + list(SVD_total[(i + 1) * distance : ])
#        train_target = list(SVD_target[0 : i * distance]) + list(SVD_target[(i + 1) * distance : ])
#        test_data = list(SVD_total[i * distance : (i + 1) * distance])
#        test_target = list(SVD_target[i * distance : (i + 1) * distance])
#        svm_fitted = svm.fit(train_data, train_target)
#        predicted = svm_fitted.predict(test_data)
#        score += metrics.accuracy_score(test_target, predicted)
##        print(score / (i + 1))
#    if score > bestScore:
#        bestScore, bestC = score, c
#    print(c, score / 5)
#print(bestScore * 0.2, bestC)


"""
Problem g: Naive Bayes Classifier
"""
from sklearn.naive_bayes import GaussianNB
naive_clf = GaussianNB()
naive_clf.fit(SVD_train, train_data.target)
nb_predicted = naive_clf.predict(SVD_test)
print("Results for problem g - Naive Bayes Classifier: ")
print(metrics.classification_report(test_data.target, nb_predicted))
print(metrics.confusion_matrix(test_data.target, nb_predicted))
print(metrics.accuracy_score(test_data.target, nb_predicted))
draw("Naive Bayes Classifier ", test_data.target, naive_clf.predict_proba(SVD_test)[:, 1])


"""
Problem h: Logistic Regressional Classifier
"""
from sklearn import linear_model
logreg = linear_model.LogisticRegression(C=1e5)
logreg.fit(SVD_train, train_data.target)
lr_predicted = logreg.predict(SVD_test)
print("Results for problem h - Logistic Regressional Classifier: ")
print(metrics.classification_report(test_data.target, lr_predicted))
print(metrics.confusion_matrix(test_data.target, lr_predicted))
print(metrics.accuracy_score(test_data.target, lr_predicted))
draw("Logistic Regressional Classifier ", test_data.target, logreg.predict_proba(SVD_test)[:, 1])
