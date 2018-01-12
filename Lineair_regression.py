import random

class Regression:
    def regression(self, data):
        alfa = 0.1
        weight = random.uniform(0.0, 1.0)

        for i in range(0, 500):
            growth = float(data[i][0])
            indicator = data[i][2]

            predicted_growth = weight * indicator
            error = growth - predicted_growth
            print("i, growth, indicator, weight, error")
            print(i, growth, indicator, weight, error)

            weight += (alfa * indicator * error)

        return weight
