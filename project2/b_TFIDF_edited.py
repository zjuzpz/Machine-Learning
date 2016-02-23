# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 21:54:48 2016
 
@author: Peizhe
"""
 
from sklearn.datasets import fetch_20newsgroups
from nltk.tokenize import word_tokenize 
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction import text
import pandas as pd

def initializeData(data): 
#    graphics_train = fetch_20newsgroups(subset = dataSet,\
#    categories = categories, shuffle = True, random_state = 42)
     
    wnl = WordNetLemmatizer()
    stop_words = text.ENGLISH_STOP_WORDS
     
    data = data 
    #List of dicts, each element represents word to number mapping for each document
    termDictList = []
    #Dictionary for each term which stores the number of documents that contains this term
    termDocCountDict = {}
    # set of term 
    termSet = set()
    # list of int, each element represents total number of terms in each tokenlized documment
    termCountList = []    
     
    # get focument frequency for each term
    for i in range(len(data)):
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
    for i in range(len(data)):
        termDict = {}
        termCount = 0
        document = data[i].lower()
        words = word_tokenize(document)
        for word in words:
            if word.isalpha():
                term = wnl.lemmatize(word)
                if term not in stop_words:
                    if term in termDocCountDict:
                        if termDocCountDict[term] >= 110 and termDocCountDict[term] <= 11000:
                            termSet.add(term)
                            termCount += 1
                            # fill in termDict
                            if term not in termDict:
                                termDict[term] = 0
                            termDict[term] += 1
                        else:
                            del termDocCountDict[term]
        termDictList.append(termDict)
        termCountList.append(termCount)
         
    return (termDictList, termCountList, termDocCountDict, termSet)
 
# function
def computeTF(termDict, termCount):
    tfDict = {}
    for term, count in termDict.iteritems():
        tfDict[term] = count / float(termCount)
    return tfDict

 # computeIDF function
def computeIDF(N, termDocCountDict):
    import math
                 
    for word, val in termDocCountDict.iteritems():
        termDocCountDict[word] = math.log(N / float(val))
         
    return termDocCountDict

# computeTFIDF function: compute tfidt for each document
def computeTFIDF(tfDict, idfs, termSet):
    tfidf = {}
    for term in termSet:
        if term in tfDict:
            tfidf[term] = tfDict[term] * idfs[term]
        else:
            tfidf[term] = 0
             
    return tfidf

def solution(data):
    tfDictList = []
    termDictList, termCountList, termDocCountDict, termSet = initializeData(data)
    
# compute TF for each tokenized document
    for i in range(len(termDictList)):
        tfDictList.append(computeTF(termDictList[i], termCountList[i]))
    # compute IDF
    idfs = computeIDF(len(termDictList), termDocCountDict)

    # tfidf list
    tfidfList = []
    for i in range(len(termDictList)):
        tfidfList.append(computeTFIDF(tfDictList[i], idfs, termSet))
             
     
    # create tfidf matrix
    matrix = pd.DataFrame(tfidfList)
    return matrix

 
if __name__ == "__main__":
    newsgroups_train = fetch_20newsgroups(subset='train')
    categories = list(newsgroups_train.target_names)
    graphics_train = fetch_20newsgroups(subset = "train",\
    categories = categories, shuffle = True, random_state = 42)
    matrix = solution(graphics_train.data)
    x, y = matrix.shape
    print("final number of terms extracted", y)
    print("total Documents", x)