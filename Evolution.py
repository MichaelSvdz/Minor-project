import random

class Regression:

    def regression(self, data):

        #Creating training and test data
        data_test = data[0:200]
        data_training = data[200:1000]

        weights = []
        count_good = 0
        count_wrong = 0

        #Creating 50 sets of weights
        for i in range(50):
            weights_one = []
            for i in range(1, len(data[0])):
                weights_one.append(random.random() * 5 - 2.5)
            weights.append(weights_one)

        #Recursive function to test the weights and create new ones by changing the best sets
        def train_weights(weights, data, count=0):
            count += 1
            all_error = []

            #Iterate over the weight sets
            for element in weights:
                error = 0

                #Iterate over the training data
                for day in data:
                    grow = float(day[0])
                    indicators = day[1:]
                    weighted_indicators = []
                    for i in range(len(indicators)):
                        weighted_indicators.append(element[i] * indicators[i])
                    predicted_grow = sum(weighted_indicators)

                    #Summing the error the weight set makes each period in the training data
                    error += (grow - predicted_grow)**3
                all_error.append(error)

            #Isolate the best weight sets
            best_weight_sets = []
            for i in range(10):
                best_weight_sets.append(weights[all_error.index(min(all_error))])
                del all_error[all_error.index(min(all_error))]

            #Making new weight sets from the best weight sets
            new_weights = best_weight_sets
            for i in range(len(best_weight_sets)):
                for j in range(4):
                    new_weights.append([k*((random.random()/5 - 0.1)/count) for k in best_weight_sets[i]])

            #Repeat the process until the recursion has been done a certain amount of times
            if count < 100:
                return train_weights(new_weights, data_training, count)
            else:
                return best_weight_sets[0]

        #Get the best weight set by calling the training function
        best_weights = train_weights(weights,data_training)
        print(best_weights)

        #See how good the best weight set does on the test data
        for day in data_test:
            grow = float(day[0])
            indicators = day[1:]
            weighted_indicators = []
            for i in range(len(indicators)):
                weighted_indicators.append(best_weights[i] * indicators[i])
            predicted_grow = sum(weighted_indicators)


        #Adding one to count_good for every time the grow and the predicted grow have the same sign
        #Adding one to count_wrong for every time the grow and the predicted grow have a different sign
            if predicted_grow > 0 and grow > 0:
                count_good += 1
            elif predicted_grow < 0 and grow < 0:
                count_good += 1
            else:
                count_wrong += 1
        count_count = count_good / count_wrong
        return best_weights, count_count
