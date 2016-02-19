# -*- coding: utf-8 -*-
"""
@author: Yu
"""

import numpy
from sklearn import linear_model, cross_validation


data = numpy.genfromtxt('random_housing_data.csv', delimiter=',', skip_header=1)
alphas = [0.1, 0.01, 0.001]
others = data[:, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)]
medv = data[:, 13]
rmse = []

tenfold = cross_validation.KFold(len(others), 10, True)   
lasso = linear_model.LassoCV(0.001, 3, alphas, True, False, 'auto', 100, 0.0001, True, tenfold, False, -1, False, None, 'cyclic')
lasso.fit(others, medv)

predicted = lasso.predict(others)

rmse.append(numpy.sqrt(((predicted - medv) ** 2).mean()))

print 'RMSE: \n', rmse
print 'Alpha: \n', lasso.alpha_