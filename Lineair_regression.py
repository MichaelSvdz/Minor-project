import random

class Regression:
    def regression(self, data):
        alfa = 0.1
        weight = random.uniform(0.0, 1.0)

        for i in range(0, 500):
            growth = float(data[i][0])
            indicator = data[i][2]

<<<<<<< HEAD

        print(count_good, count_wrong)
=======
            predicted_growth = weight * indicator
            error = growth - predicted_growth
            print("i, growth, indicator, weight, error")
            print(i, growth, indicator, weight, error)
>>>>>>> 2c7d0e8f7aa804d2bcfd01133fe9625f98322a0e

            weight += (alfa * indicator * error)

        return weight
