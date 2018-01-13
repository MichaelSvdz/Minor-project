import random

class Regression:
    def regression(self, data):
        alfa = 0.02
        weights = []
        for i in range(1,len(data[0])):
            weights.append(random.random()*2-1)
        count_good = 0
        count_wrong = 0
        for day in data:
            grow = float(day[0])
            indicators = day[1:]
            weighted_indicators = []
            for i in range(len(indicators)):
                weighted_indicators.append(weights[i] * indicators [i])
            predicted_grow = sum(weighted_indicators)
            error = grow - predicted_grow
            indicators_sum = sum(abs(w) for w in indicators)
            for i in range(len(weights)):
                weights[i] = weights[i] + (alfa * indicators[i]/indicators_sum * error)

            if predicted_grow > 0 and grow > 0:
                count_good += 1
            elif predicted_grow < 0 and grow < 0:
                count_good += 1
            else:
                count_wrong += 1


        print(count_good, count_wrong)

        return weights
