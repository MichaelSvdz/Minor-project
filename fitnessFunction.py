import numpy as np
x = np.array([0.25,0.25,0.25,0.25])                                     #weights of the stocks


stockprices = [[2,2,2,2,5],[1,2,6,1,3],[1,2,3,4,3],[5,2,3,4,8]]         #list of stocks containing the stockprices

cov_matrix = np.cov(stockprices)
#print(corr_matrix)

def fitnessFunction(cov_matrix, x):
    return np.dot(np.dot(x.T,np.transpose(cov_matrix)),x)               # unsystematic risk

print(fitFunction(cov_matrix, x))

