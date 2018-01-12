import re
import csv
import glob
import random
from programming import Fitness as fit

# Set limitations
popSize = 10 # Size of population
numOfGens = 100 # Amount of generation
minSIP = 2 # Minimum amount of stocks in portfolio
maxSIP = 6 # Maximum amount of stocks in portfolio
bestWeights = []

# Classes
class Chromosome:
    def __init__(self, chrom, fitness):
        self.chrom = chrom
        self.fitness = fitness

# Functions
def getRandomChromosome():
    array = [0] * chrLngth
    c = Chromosome(array, 0.01)
    stocks = random.sample(range(chrLngth), random.randint(minSIP, maxSIP))
    for stock in stocks:
        c.chrom[stock] = 1
    return c

def getStocknames(chrom):
    global stocks
    stks = []
    for i in range(len(chrom)):
        if (chrom[i] == 1):
            stks.append(stocks[i])
    return(stks)

def determineFitness(chrom):
    stks = getStocknames(chrom)
    ftns, weights = fit.fitness(stks)
    return(ftns, weights)

def roulettewheelselection(population):
    max = sum(p.fitness for p in population)
    pick = random.uniform(0, max)
    current = 0
    for p in population:
        current += p.fitness
        if current > pick:
            return p

def mutate(chrom):
    if (sum(j for j in chrom) < (maxSIP - 1) and sum(j for j in chrom) > (minSIP + 1)):
        i = random.randint(0, chrLngth - 1)
        if (chrom[i] == 0):
            chrom[i] = 1
        else:
            chrom[i] = 0

# Genetic Algorithm
def genAlg(stocks):
    global chrLngth
    chrLngth = len(stocks)

    # Make random population
    population = []
    for i in range(popSize):
        population.append(getRandomChromosome())

    for i in range(numOfGens):
        # Make new population
        newpopulation = []

        # Elitism 2 chromosomes
        newpopulation.append(population[0])
        newpopulation.append(population[1])
        del population[0]
        del population[1]

        for i in range(0, popSize - 2, 2):
            # Roulette wheel selection
            parent1 = roulettewheelselection(population)
            parent2 = roulettewheelselection(population)
            while (parent1.chrom == parent2.chrom):
                parent2 = roulettewheelselection(population)

            # Crossover
            child1 = [0] * chrLngth
            child2 = [0] * chrLngth
            copoint = random.randint(0, chrLngth)
            for i in range(0, chrLngth):
                if(i < copoint):
                    child1[i] = parent1.chrom[i]
                    child2[i] = parent2.chrom[i]
                else:
                    child1[i] = parent2.chrom[i]
                    child2[i] = parent1.chrom[i]

            newpopulation.append(Chromosome(child1, 0))
            newpopulation.append(Chromosome(child2, 0))

        population = newpopulation

        # Mutation
        mutProb = 0.005
        for p in population:
            if (random.uniform(0.0, 0.1) > mutProb):
                mutate(p.chrom)

        # Determine fitness
        for p in population:
            ftns, weights = determineFitness(p.chrom)
            p.fitness = ftns
        population.sort(key=lambda x: x.fitness, reverse=True)

        bestChrom = population[0]
        bestWeights = weights

    print(getStocknames(bestChrom.chrom))
    print(bestChrom.fitness)
    print(bestWeights)

for i in range(10):
    stocks = []
    datafiles =  glob.glob("datasets/*/*.csv")
    for f in datafiles:
        stocks.append(re.split('\/(.*?\/.*?).csv', f)[1])
    genAlg(stocks)

#fit.getDataClosed(population)























'''
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

def pertubate()

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
    pfRandom = pertubate(pfCurrent)

    # Compute the probability of moving, P(S <-- S')


    # If the condition for moving is satisfied:


        # Update the current solution, S <-- S'


        # If the fitness of S is greater than S*:


            # Update the best found solution, S* <-- S


# Return the best found solution, S*
'''
