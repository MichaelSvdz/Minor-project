import numpy as np
from scipy.optimize import minimize
import math
import glob

stocks = ["GOOGL","MSFT","AAPL","ACN","ADBE","ADP", "ADS", "ADSK", "AKAM","AMAT","AMD","APH","AVGO","CA","CDNS","CSCO","EBAY"]
class Fitness:
    def getDataClosed(stocks):
        files = []
        data = []
        for s in stocks:
            files.append("datasets/" + s + ".csv")
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
        data = Fitness.getDataClosed(stocks)
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

    def unsystematicRisk(cov_matrix, x):
        return np.dot(np.dot(x.T,np.transpose(cov_matrix)),x)       # unsystematic risk

    def totalExpectedReturn(weights,expected_returns):              # total Expected Return of portfolio
        return np.dot(weights,expected_returns)

    def negativeSharpeRatio(weights,returns,risk_free_rate,cov_matrix):
        return -(Fitness.totalExpectedReturn(weights,returns)-risk_free_rate)/ math.sqrt(Fitness.unsystematicRisk(cov_matrix, weights))

    def weightsCalculator(returnsStocks, risk_free_rate, allow_short = False):
        cov_matrix = np.cov(returnsStocks)
        weights = [1/len(returnsStocks)]*len(returnsStocks)                     # initial_weights
        returns = Fitness.getMeanReturns(returnsStocks)
        if not allow_short:
            bounds = [(0, None,) for i in range(len(weights))]              # boundaries for the weights
        else:
            bounds = None                                                   # there are no boundaries
        cons = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}) # sum of weights must be 1

        minimum = minimize(Fitness.negativeSharpeRatio, weights, args=(returns,risk_free_rate,cov_matrix),
                           bounds=bounds, constraints = cons)                                       # Maximize SharpeRatio
        return minimum

    def fitness (stocks):
        #returnstocks
        returnsStocks = Fitness.calculateReturns(stocks)
        gewichten = Fitness.weightsCalculator(returnsStocks,0.05)
        portfolioReturn = np.dot(Fitness.getMeanReturns(returnsStocks), gewichten.x)
        return(portfolioReturn, gewichten)
