# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 22:49:24 2016

@author: Sarah
"""
from sklearn.datasets import fetch_20newsgroups
from nltk.tokenize import word_tokenize
import string
import nltk

from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction import text

newsgroups_train = fetch_20newsgroups(subset='all')
#categories = list(newsgroups_train.target_names)
#category = ['comp.sys.ibm.pc.hardware']
#category = ['comp.sys.mac.hardware']
#category = ['misc.forsale'] 
category = ['soc.religion.christian']
graphics_train = fetch_20newsgroups(subset = 'train',\
categories = category, shuffle = True, random_state = 42)

C = 20

wnl = WordNetLemmatizer()
stop_words = text.ENGLISH_STOP_WORDS
data = graphics_train.data 

#Dictionary for each term which stores the number of documents that contains this term
termCategorDict = {}

#Dictionary for each term which stores the number of documents that contains this term
termDocCountDict = {}

# set of term 
termSet = set()

# get ocument frequency for each term
totalDocNumber = 0
for i in range(len(data)):
    totalDocNumber += 1
    document = data[i].lower()
    words = set(word_tokenize(document))
    for word in words:
        if word.isalpha():
            term = wnl.lemmatize(word)
            if term not in stop_words:
                if term not in termDocCountDict:
                    termDocCountDict[term] = 0
                termDocCountDict[term] += 1

# get termDict and termSet
totalWordCount = 0
for i in range(len(data)):
    document = data[i].lower()
    words = word_tokenize(document)
    for word in words:
        if word.isalpha():
            term = wnl.lemmatize(word)
            if term not in stop_words:
                if term in termDocCountDict:
                    if termDocCountDict[term] >= 0.01*totalDocNumber and termDocCountDict[term] <= 0.99*totalDocNumber:
                        termSet.add(term)
                        totalWordCount += 1
                        # fill in termCategorDict
                        if term not in termCategorDict:
                            termCategorDict[term] = 0
                        termCategorDict[term] += 1
                    else:
                        del termDocCountDict[term]
    
## final number of terms extracted: 
#print("final number of terms extracted for category: comp.sys.ibm.pc.hardware", len(termSet))

# function
def computeTF(termCategorDict, totalWordCount):
    tfDict = {}
    tfDictNormalized = {}
    tfMax = 0
    for term, count in termCategorDict.iteritems():
        tfDict[term] = count / float(totalWordCount)
        if tfDict[term] > tfMax:
           tfMax = tfDict[term]
           
    for term, count in termCategorDict.iteritems():
        tfDictNormalized[term] = tfDict[term] / tfMax
    
    return tfDictNormalized
    
# compute TF for a given category ()
tfDict = computeTF(termCategorDict, totalWordCount)

 # computeIDF function
def computeIDF():
    import math
        
    return math.log(20)

# compute IDF
idfs = computeIDF()

# computeTFIDF function: compute tfidt for each document
def computeTFIDF(tfDict, idfs):
    tfidf = {}
#    itfidf = {}
    for term in termSet:
        if term in tfDict:
            tfidf[term] = (0.5 + 0.5 * tfDict[term]) * idfs
        else:
            tfidf[term] = 0
    
#    for term in termSet:
#        if term in tfDict:
#            itfidf[tfidf[term]] = term
    return tfidf

# tfidf list
tfidf = computeTFIDF(tfDict, idfs)
from collections import OrderedDict
#OrderedDict(sorted(itfidf.keys(), reverse=True))
#sorted(itfidf.keys())

tfidf_descending = OrderedDict(sorted(tfidf.items(), key = lambda x: (-x[1], x[0])))
print(tfidf_descending)

