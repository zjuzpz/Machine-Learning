# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 15:00:25 2016

@author: Yu
"""
#
#from sklearn.datasets import fetch_20newsgroups
#
#from sklearn.feature_extraction.text import CountVectorizer
#
#from sklearn.feature_extraction.text import TfidfVectorizer
#
#from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
#
#
#
##Applying LSI to the TF-IDF matrix to reduce to 50 features
#
#
#from sklearn.decomposition import TruncatedSVD
#from sklearn.pipeline import Pipeline
#
#vectorizer = TfidfVectorizer()
#svd = TruncatedSVD(n_components=50, n_iter=5, random_state=25)
#svd_transformer = Pipeline([('tfidf', vectorizer),
#                            ('svd', svd)])
#svd_matrix = svd_transformer.fit_transform(matrix)
#
##from sklearn.decomposition import TruncatedSVD
##X = TruncatedSVD(n_components=50)
##LSI = X.fit_transform(matrix)

from sklearn.datasets import fetch_20newsgroups
from b_TFIDF_edited import solution
#Applying LSI to the TF-IDF matrix to reduce to 50 features

from sklearn.decomposition import TruncatedSVD

def getSVD(data):
    svd = TruncatedSVD(n_components=50, n_iter=5)
    matrix = solution(data)
    svd_matrix = svd.fit_transform(matrix)
    return svd_matrix

if __name__ == "__main__":
    categories = ["comp.graphics", "comp.os.ms-windows.misc", \
    "comp.sys.ibm.pc.hardware", "comp.sys.mac.hardware", "rec.autos", "rec.motorcycles", \
    "rec.sport.baseball", "rec.sport.hockey"]
    graphics_train = fetch_20newsgroups(subset = "train",\
    categories = categories, shuffle = True, random_state = 42)
    SVD = getSVD(graphics_train.data)
    print(SVD)
    print(len(SVD))
    print(len(SVD[0]))