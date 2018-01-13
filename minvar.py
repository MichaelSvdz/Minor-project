import numpy as np
from scipy.optimize import minimize
import math
import glob

stocks = ["GOOGL","MSFT","AAPL","ACN","ADBE","ADP", "ADS", "ADSK", "AKAM","AMAT","AMD","APH","AVGO","CA","CDNS","CSCO","EBAY"]

def getDataClosed(stocks):
    files = []
    data = []
    for s in stocks:
        files.append("datasets/information_technology/" + s + ".csv")
    for f in files:
        with open(f, "r") as f:
            close_prices = []
            for row in f:
                row = row.strip()
                row = row.split(",")
                close_prices.append(row[4])
            del close_prices[0]
            close_prices = list(map(float, close_prices))
            data.append(close_prices)
    return data

def calculateReturns(stocks):
    data = getDataClosed(stocks)
    num_stocks= len(data)
    min_values = min({len(i) for i in data})
    for lijst in data:
        lijst = lijst[0:min_values]
    Totalreturns = []
    days = 120
    for j in range(num_stocks):
        returns = []
        for i in range(math.floor(min_values/days)-1):
            returns.append((data[j][days*i]-data[j][days*i+days])/data[j][days*i+days])
        Totalreturns.append(returns)
    return Totalreturns

def getMeanReturns(returns):
    mean_returns = []
    for i in range(len(returns)):
        mean_returns.append(np.mean(returns[i]))
    return mean_returns

def unsystematicRisk(cov_matrix, weights):
    risk = np.dot(np.dot(weights.T,np.transpose(cov_matrix)),weights)# unsystematic risk
    print("Risk: ")
    print(risk)
    return risk

def totalExpectedReturn(weights,expected_returns):              # total Expected Return of portfolio
    return np.dot(weights,expected_returns)

def negativeSharpeRatio(weights,returns,risk_free_rate,cov_matrix):
    return -(totalExpectedReturn(weights,returns)-risk_free_rate)/ math.sqrt(unsystematicRisk(cov_matrix, weights))

def weightsCalculator(returnsStocks, risk_free_rate, allow_short = False):
    cov_matrix = np.cov(returnsStocks)
    #print(cov_matrix)
    weights = [1/len(returnsStocks)]*len(returnsStocks)                     # initial_weights
    returns = getMeanReturns(returnsStocks)
    #print(returns)
    if not allow_short:
        bounds = [(0, None,) for i in range(len(weights))]              # boundaries for the weights
    else:
        bounds = None                                                   # there are no boundaries
    cons = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}) # sum of weights must be 1


    #negativeSharpeRatio
    minimum = minimize(unsystematicRisk, weights, args=(cov_matrix),
                       bounds=bounds, constraints = cons)                                       # Maximize SharpeRatio
    return minimum
'''
returnsStocks = [
    [0.3,0.103,0.216,-0.046,-0.071,0.056,0.038,0.089,0.09,0.083,0.035,0.176],
    [0.225,0.29,0.216,-0.272,0.144,0.107,0.321,0.305,0.195,0.39,-0.072,0.715],
    [0.149,0.260,0.419,-0.078,0.169,-0.035,0.133,0.732,0.021,0.131,0.006,0.908]
    ]         #list of stocks containing the stockprices
'''

returnsStocks = calculateReturns(stocks)
weights = [1/len(returnsStocks)]*len(returnsStocks)
print(unsystematicRisk(np.cov(returnsStocks),array(weights)))

#print(type(returnsStocks[0]))
#gewichten = weightsCalculator(returnsStocks,0.05)
#print(gewichten)

