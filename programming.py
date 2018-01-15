import math
import glob
import numpy as np
from scipy.optimize import minimize
from make_expected_return import Evostrat

class Fitness:
    # Takes a list of stocks and returns the daily close prices
    def getDataClosed(stocks):
        # Initialise variables
        data = []   # return variable
        files = []  # path to files variable

        # Build path to stocks
        for s in stocks:
            files.append("datasets/" + s + ".csv")

        # Read files and append to 'data'
        for f in files:
            with open(f, "r") as f:
                close_prices = []
                for row in f:
                    row = row.strip()
                    row = row.split(",")
                    close_prices.append(row[4])
                del close_prices[0]
                close_prices = list(map(float, close_prices)) # map to floats
                data.append(close_prices)

        return data

    # Calculates return on stock per [amount of days]
    # Returned list has length of shortest stock on market
    def calculateReturns(stocks):
        days = 5                                    # Calculate returns over x days (5 = weekly)
        Totalreturns = []
        realReturns = []
        data = Fitness.getDataClosed(stocks)        # get data
        num_stocks= len(data)
        min_values = min(min({len(i) for i in data}), 365)    # set length
        for d in data:                              # shorten data
            d = d[0:min_values]

        for j in range(num_stocks):
            returns = []
            for i in range(math.floor(min_values/days)-1):
                returns.append((data[j][days*i]-data[j][days*i+days])/data[j][days*i+days]) # add return over rest of periods of days
            Totalreturns.append(returns)

        for t in Totalreturns:
            realReturns.append(t[0])
            t = t[1:]

        return Totalreturns, realReturns

    # Returns mean return of each set in returns
    def getMeanReturns(returns):
        mean_returns = []
        for i in range(len(returns)):
            mean_returns.append(np.mean(returns[i]))
        return mean_returns

    #def unsystematicRisk(cov_matrix, x):
    #    return np.dot(np.dot(x.T,np.transpose(cov_matrix)),x)       # unsystematic risk

    def unsystematicRisk(weights,cov_matrix):
        return np.dot(np.dot(weights.T,np.transpose(cov_matrix)),weights)       # unsystematic risk

    def totalExpectedReturn(weights,expected_returns):              # total Expected Return of portfolio
        return np.dot(weights,expected_returns)

    def negativeSharpeRatio(weights,returns,risk_free_rate,cov_matrix):
        zero = math.sqrt(Fitness.unsystematicRisk(weights, cov_matrix))
        return -(Fitness.totalExpectedReturn(weights,returns)-risk_free_rate)/ zero

    # Calculates optimal weigths of stock in portfolio
    # using a minimize model with constraints
    def weightsCalculator(returnsStocks, risk_free_rate, stocks, wantedReturn, sharpe, evo, allow_short):
        # Set variables for model
        cov_matrix = np.cov(returnsStocks)
        weights = [1/len(returnsStocks)]*len(returnsStocks)                 # initial_weights
        #weights = np.ones(len(returnsStocks)) #minvariance
        if evo:     # Use evoluotionary strategy to calculate expected future returns
            returns = Evostrat.evostrat(stocks)
        else:   # Use mean returns as expected future return
            returns = Fitness.getMeanReturns(returnsStocks)

        # Set bounds
        if not allow_short:
            bounds = [(0.05, None,) for i in range(len(weights))]              # boundaries for the weights
        else:
            bounds = None                                                   # there are no boundaries

        # Splitted on either Sharpe ratio or minimize variance
        if sharpe:
            # Set constraints
            cons = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}) # sum of weights must be 1


            return minimize(Fitness.negativeSharpeRatio,                        # maximize SharpeRatio
                                weights,
                                args=(returns,risk_free_rate,cov_matrix),
                                bounds=bounds,
                                constraints = cons)
        else:
            cons = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
                    {'type': 'ineq', 'fun':lambda weights: np.dot(weights,returns)-wantedReturn}) # sum of weights must be 1

            return minimize(Fitness.unsystematicRisk,
                                weights,
                                args=(cov_matrix),
                                bounds=bounds,
                                constraints = cons)

    def fitness (stocks, wantedReturn, sharpe, evo, allow_short):
        # Get past returns on stocks
        returnsStocks, realReturn = Fitness.calculateReturns(stocks)
        # Get optimal weights of specific fortfolio
        gewichten = Fitness.weightsCalculator(returnsStocks,0.05, stocks, wantedReturn, sharpe, evo, allow_short)
        # Calculate expected return of total portfolio
        portfolioReturn = np.dot(Fitness.getMeanReturns(returnsStocks), gewichten.x)
        # Return in last period
        realReturn = np.dot(realReturn, gewichten.x)

        return(portfolioReturn, gewichten.x, realReturn)
