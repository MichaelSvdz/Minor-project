# -*- coding: utf-8 -*-
import re
import csv
import glob
import random
import datetime
from collections import defaultdict
from programming import Fitness as fit

# Classes
class Chromosome:
    def __init__(self, chrom, fitness, weigths, realReturn, risk):
        self.chrom = chrom
        self.fitness = fitness
        self.weights = weigths
        self.realReturn = realReturn
        self.risk = risk

# Functions
def getRandomChromosome():
    array = [0] * chrLngth
    c = Chromosome(array, 0.01, [], 0.0, 100)
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

def roulettewheelselection(population):
    max = sum(p.fitness for p in population)
    pick = random.uniform(0, max)
    current = 0
    for p in population:
        current += p.fitness
        if current > pick:
            return p

def mutate(chrom):
    activeStocks = sum(j for j in chrom)
    i = random.randint(0, chrLngth - 1)
    if (chrom[i] == 0 and activeStocks < maxSIP):
        chrom[i] = 1
    elif (activeStocks > minSIP):
        chrom[i] = 0

# Genetic Algorithm
def genAlg(stocks):
    # Set lengt of chromosome
    global chrLngth, mutProb, crossProb
    global wantedReturn, sharpe, evo, allow_short
    chrLngth = len(stocks)

    # Make random population
    population = []
    for i in range(popSize):
        population.append(getRandomChromosome())

    # Determine fitness and sort for elitism
    for p in population:
        ftns, weights, realReturn, risk = fit.fitness(getStocknames(p.chrom), wantedReturn, sharpe, evo, allow_short)
        p.fitness = ftns
        p.weights = weights
        p.realReturn = realReturn
        p.risk = risk
        #bestChrom = Chromosome(p.chrom[:], p.fitness)
        #bestWeights = weights
    population.sort(key=lambda x: x.fitness, reverse=True)

    # Run generations
    for i in range(numOfGens):
        if i % 50 == 0:
            print(i, datetime.datetime.now().time())

        global bestChrom
        # Make new population variable
        newpopulation = []

        # Elitism 2 chromosomes
        newpopulation.append(population[0])
        newpopulation.append(population[1])
        population.pop(1)
        population.pop(0)

        # Make rest of new population
        for i in range(0, popSize - 2, 2):
            # Roulette wheel selection
            parent1 = roulettewheelselection(population)
            parent2 = roulettewheelselection(population)
            while (parent1.chrom == parent2.chrom):
                parent2 = roulettewheelselection(population)

            if random.uniform(0.0, 1.0) < crossProb:
                # Crossover
                child1 = [0] * chrLngth
                child2 = [0] * chrLngth
                copoint = random.randint(0, chrLngth)
                stocksLeftOfcopoint = sum(j for j in parent1.chrom[:copoint])
                for i in range(0, chrLngth):
                    if(i < copoint):
                        child1[i] = parent1.chrom[i]
                        child2[i] = parent2.chrom[i]
                    else:
                        child1[i] = parent2.chrom[i]
                        child2[i] = parent1.chrom[i]

                # Put children within 'amount of stock'-constraints
                while(sum(j for j in child1) < minSIP):
                    mutate(child1)
                while(sum(j for j in child1) > maxSIP):
                    mutate(child1)
                while(sum(j for j in child2) < minSIP):
                    mutate(child2)
                while(sum(j for j in child2) > maxSIP):
                    mutate(child2)

                newpopulation.append(Chromosome(child1[:], 0, [], 0.0, 100))
                newpopulation.append(Chromosome(child2[:], 0, [], 0.0, 100))

            else:
                newpopulation.append(Chromosome(parent1.chrom[:], 0, [], 0.0, 100))
                newpopulation.append(Chromosome(parent2.chrom[:], 0, [], 0.0, 100))

        # Switch out population
        population = newpopulation

        # Mutation
        for p in population:
            if (random.uniform(0.0, 1.0) < mutProb):
                mutate(p.chrom)

        # Determine fitness and sort
        for p in population:
            ftns, weights, realReturn, risk = fit.fitness(getStocknames(p.chrom), wantedReturn, sharpe, evo, allow_short)
            p.fitness = ftns
            p.weights = weights
            p.realReturn = realReturn
            p.risk = risk
        population.sort(key=lambda x: x.fitness, reverse=True)

        # Remember best Chromosome
        if population[0].risk < bestChrom.risk:
            bestChrom = Chromosome(population[0].chrom[:], population[0].fitness, population[0].weights, population[0].realReturn, population[0].risk)

    finalPortfolio = defaultdict(list)
    finalStocks = getStocknames(bestChrom.chrom)
    print(('-----EINDE-----\nExpected return:    %s%%\nReal return:        %s%%\nRisk:               %s%%\nPortfolio:') % (round(bestChrom.fitness*100, 2), round(bestChrom.realReturn*100, 2), round(bestChrom.risk*100,2)))
    for i in range(len(finalStocks)):
        finalPortfolio[finalStocks[i]] = round(bestChrom.weights[i], 2)
    for fp in finalPortfolio:
        print(fp, finalPortfolio[fp])


print("Welcome to the portfolio advisor")
print("To advise the optimal portfolio, please answer these questions:")
wantedReturn = (float(input("What is the minimum return you want (higher return, higher risk)?     ")) / 100)
print("Optimize portfolioweigts by Sharpes ratio or minimum variance?")
sharpe = True if input("Type 'sharpe' for Sharpe, or anything else for minimum variance     ").lower() == 'sharpe' else False
print("Calculate expected return by mean or evolutionary strategy?")
evo = False if input("Type 'mean' for mean, or anything else for evolutionary strategy     ").lower() == 'mean' else True
allow_short = True if input("Type '1' for going short on stocks, '0' for otherwise     ").lower() == '1' else False
if evo:
    print("This will take 15 minutes")
else:
    print("This will take 5 minutes")
'''
# input for presentation
wantedReturn = 0.10
sharpe = False
evo = False
allow_short = False
'''
# Get all possible stocks
stocks = []
datafiles =  glob.glob("datasets/*/*.csv")
for f in datafiles:
    stocks.append(re.split('\/(.*?\/.*?).csv', f)[1])

# Set variables
bestChrom = Chromosome([0]*len(stocks), 0.00001, [], 0.0, 100)
bestWeights = []

# Set limitations
mutProb = 0.01
crossProb = 0.7
popSize = 50 # Size of population
numOfGens = 50 # Amount of generation
minSIP = 3 # Minimum amount of stocks in portfolio
maxSIP = 10 # Maximum amount of stocks in portfolio

# Find best portfolio with these stocks
genAlg(stocks)
