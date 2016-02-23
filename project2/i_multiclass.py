# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 11:22:35 2016

@author: Yu
"""
from d_truncated_SVD import getSVD
from sklearn.datasets import fetch_20newsgroups
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.pipeline import Pipeline
import string
from sklearn import feature_extraction
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier

def print_helper(expected, predicted, model):
    # summarize the fit of the model
    print('Classification report for: %s\n'%model)
    print(metrics.classification_report(expected, predicted))
    print('Confusion matrix for: %s\n'%model)
    print(metrics.confusion_matrix(expected, predicted))
    print('Accuracy for: %s\n'%model)
    print(metrics.accuracy_score(expected, predicted))
    print '\n'

def clean_word(s):
    cleaned = ""    
    if s is not None:
        for w in nltk.tokenize.word_tokenize(s.lower()):
            if w is not None and w not in feature_extraction.text.ENGLISH_STOP_WORDS and w not in string.punctuation:
                cleaned += " " + nltk.stem.LancasterStemmer().stem(w)
    return cleaned


def pipeline_setup(model):
    tf_idf = TfidfVectorizer(preprocessor=clean_word, use_idf=True)
    svd = TruncatedSVD(n_components=50, n_iter=5)
    pipeline = Pipeline([('tf_idf', tf_idf), ('svd', svd), ('model', model)])
    return pipeline

categories = ['comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'misc.forsale', 'soc.religion.christian']

train_data = fetch_20newsgroups(subset = 'train', categories = categories, shuffle = True, random_state = 42)
test_data = fetch_20newsgroups(subset = 'test', categories = categories, shuffle = True, random_state = 42)

#svd_train = getSVD(train_data.data)
#svd_test = getSVD(test_data.data)

########################    naive bayes multiclass       ######################
#### Fit using truncated_svd_matrix #######
#nb_model = GaussianNB()
#nb_model.fit(svd_train, train_data.target)
#nb_predicted = nb_model.predict(svd_test)
#nb_expected = test_data.target
#print_helper(nb_expected, nb_predicted, "naive bayes multiclass")

########## Fit using pipeline ##############
nb_model = pipeline_setup(GaussianNB())
nb_model.fit(train_data.data, train_data.target)

nb_expected = test_data.target
nb_predicted = nb_model.predict(test_data.data)
print_helper(nb_expected, nb_predicted, "naive bayes multiclass")

########################    svm one vs rest multiclass       ######################
#### Fit using truncated_svd_matrix 0.08... #######
#svm = SVC(kernel = "linear", probability = True, verbose = True, random_state = 42)
#svm_onevsrest = OneVsRestClassifier(svm)
#svm_onevsrest.fit(svd_train, train_data.target)
#svm_predicted = svm_onevsrest.predict(svd_test)
#svm_expected = test_data.target
#print_helper(svm_expected, svm_predicted, "SVM one vs rest")

########## Fit using pipeline ##############
svm = SVC(kernel = "linear", probability = True, verbose = True, random_state = 42)
svm_onevsrest = OneVsRestClassifier(svm)
svm_model_onevsrest = pipeline_setup(svm_onevsrest)
svm_model_onevsrest.fit(train_data.data, train_data.target)
# print(model)
# make predictions
svm_expected = test_data.target
svm_predicted = svm_model_onevsrest.predict(test_data.data)
print_helper(svm_expected, svm_predicted, "SVM one vs rest")

#########################    svm one vs one multiclass       ######################
svm = SVC(kernel = "linear", probability = True, verbose = True, random_state = 42)
svm_onevsone = OneVsOneClassifier(svm)
svm_model_onevsone = pipeline_setup(svm_onevsone)
svm_model_onevsone.fit(train_data.data, train_data.target)
svm_expected = test_data.target
svm_predicted = svm_model_onevsone.predict(test_data.data)
print_helper(svm_expected, svm_predicted, "SVM one vs one")