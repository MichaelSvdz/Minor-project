import numpy as np
from scipy.optimize import minimize
import math
import glob

stocks = ["AAL","ALK","ALLE"]

def getData(stocks):
    files = []
    for s in stocks:
        files.append("datasets/*/" + s + ".csv")
    for f in files:
        with open(f, "r") as f:
            close_prices = []
            for row in f:
                row = row.strip()
                row = row.split(",")
                close_prices.append(row[3])
            del close_prices[0]
            close_prices = list(map(float, close_prices))
    print(close_prices)

getData(stocks)

def unsystematicRisk(cov_matrix, x):
    return np.dot(np.dot(x.T,np.transpose(cov_matrix)),x)       # unsystematic risk

def totalExpectedReturn(weights,expected_returns):              # total Expected Return of portfolio
    return np.dot(weights,expected_returns)

def negativeSharpeRatio(weights,returns,risk_free_rate,cov_matrix):
    return -(totalExpectedReturn(weights,returns)-risk_free_rate)/ math.sqrt(unsystematicRisk(cov_matrix, weights))

def weightsCalculator(returnsStocks, risk_free_rate, allow_short = False):
    cov_matrix = np.cov(returnsStocks)
    weights = [1/len(returnsStocks)]*len(returnsStocks)                     # initial_weights
    returns = [0.089083,0.213667,0.23458]  #TODO get these from Koen
    if not allow_short:
        bounds = [(0, None,) for i in range(len(weights))]              # boundaries for the weights
    else:
        bounds = None                                                   # there are no boundaries
    cons = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}) # sum of weights must be 1



    minimum = minimize(negativeSharpeRatio, weights, args=(returns,risk_free_rate,cov_matrix),
                       bounds=bounds, constraints = cons)                                       # Maximize SharpeRatio
    return [-minimum.fun, minimum.x]

returnsStocks = [
    [0.3,0.103,0.216,-0.046,-0.071,0.056,0.038,0.089,0.09,0.083,0.035,0.176],
    [0.225,0.29,0.216,-0.272,0.144,0.107,0.321,0.305,0.195,0.39,-0.072,0.715],
    [0.149,0.260,0.419,-0.078,0.169,-0.035,0.133,0.732,0.021,0.131,0.006,0.908]
    ]         #list of stocks containing the stockprices

gewichten = weightsCalculator(returnsStocks,0.05, True)
print(gewichten)

