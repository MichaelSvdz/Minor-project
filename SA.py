import csv
import glob
import random

# Set limitations
minSIP = 2 # Minimum amount of stocks in portfolio
maxSIP = 3 # Maximum amount of stocks in portfolio
minWeight = 0.01 # Minimum amount of weight per stocks
maxWeight = 0.50 # Maximum amount of weight per stocks

# Functions

# Fills empty portfolio with random solution
def getRandomSolution():
    pf = pfClean
    # Determine amount of active stocks
    stocksInPf = random.randint(minSIP, maxSIP)
    # Randomly select stocks
    stockIndexes = random.sample(range(0, totalStocks - 1), stocksInPf)
    # Assign random weights to active stocks within constraints
    weightSum = 0.0
    for index in stockIndexes:
        pf[index] = random.uniform(minWeight, maxWeight)
        weightSum += pf[index]

    # Scale weights to fill portfolio entirely
    weightUpdate = 1.0 / weightSum
    for index in stockIndexes:
        pf[index] *= weightUpdate

    fitness = getFitness(pf, stockIndexes)

    return(pf, fitness)

# Fitness function for a portfolio
def getFitness(pf, stockIndexes):
    return(random.uniform(0, 1))


# Make sure the portfolio can be filled
if (minSIP * maxWeight < 1.0):
    raise ValueError('The maximum weight times maximum stocks doesn\'t fill the portfolio')

# Form a dict with the stocks and weights initialised at 0.0
pfClean = {} # portfolio dict
urlfiles =  glob.glob("stocks/*.csv")
for u in urlfiles:
    with open(u, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            pfClean[row[0]] = 0.0

# Initialize portfolio dicts
pfBest = pfClean
pfRandom = pfClean
pfCurrent = pfClean
totalStocks = len(pfClean)

# Initialize a random feasible solution, S
pfCurrent, currentFitness = getRandomSolution()

# Initialize the best found solution, S*
pfBest, bestFitness = getRandomSolution()

# Assign S* <-- max( f(S), f(S*) )
bestFitness = getFitness(pfBest)
currentFitness = getFitness(pfCurrent)
if currentFitness > bestFitness:
    pfBest = pfCurrent
    bestFitness = currentFitness

# While the stopping condition is not satisfied:
for i in range(10):

    # Generate a feasible random solution, s'
    # by doing random pertubations to S*
    pertubate()

    # Compute the probability of moving, P(S <-- S')


    # If the condition for moving is satisfied:


        # Update the current solution, S <-- S'


        # If the fitness of S is greater than S*:


            # Update the best found solution, S* <-- S


# Return the best found solution, S*
