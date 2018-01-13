from TICalculations import TI
from Lineair_regression import Regression
import glob

myTI = TI()
myRegression = Regression()
number_of_samples = 15
days  = 1

dict_weights = {}

#Make a list of all the data files and iterate over them
datafiles =  glob.glob("datasets/*/*.csv")
for file_name in datafiles:
    print(file_name)
    with open(file_name, "r") as f:
        open_prices = []
        high_prices = []
        low_prices = []
        close_prices = []
        time_stamp = []

        #parse the data file
        for row in f:
            row = row.strip()
            row = row.split(",")
            open_prices.append(row[1])
            high_prices.append(row[2])
            low_prices.append(row[3])
            close_prices.append(row[4])
            time_stamp.append(row[0])

        #remove the headers
        del open_prices[0]
        del high_prices[0]
        del low_prices[0]
        del close_prices[0]
        del time_stamp[0]

        #Convert the lists to the right type
        open_prices = list(map(float, open_prices))
        high_prices = list(map(float, high_prices))
        low_prices = list(map(float, low_prices))
        close_prices = list(map(float, close_prices))

        #Changes the lists so that you can specify an interval for the data
        temp_close = []
        temp_open = []
        temp_low = []
        temp_high = []

        for i in range(len(close_prices)-1):
            if i % days == 0:
                temp_close.append(close_prices[i])
                temp_open.append(open_prices[i])
                temp_high.append(high_prices[i])
                temp_low.append(low_prices[i])
            else:
                continue

        close_prices = temp_close
        open_prices = temp_open
        low_prices = temp_low
        high_prices = temp_high

        #Making lists containing the technical indicators
        SMA = []
        EMA = []
        GROW = []
        MACD = []
        STOCH = []
        RSI = []
        AROONUP = []
        AROONDOWN = []
        BBRAND = []

        for i in range(len(close_prices)-number_of_samples -1):
            SMA.append(TI.SMA(myTI, close_prices[i:i+number_of_samples]))

        for i in range(len(close_prices)-number_of_samples -1):
            EMA.append(TI.EMA(myTI, close_prices[i:i+number_of_samples]))

        for i in range(len(close_prices)-number_of_samples -1):
            GROW.append(TI.GROW(myTI, close_prices[i:i+number_of_samples]))

        for i in range(len(close_prices)-number_of_samples -1):
            MACD.append(TI.MACD(myTI, close_prices[i:i+number_of_samples]))

        for i in range(len(close_prices)-number_of_samples -1):
            STOCH.append(TI.STOCH(myTI, low_prices[i:i+number_of_samples], high_prices[i:i+number_of_samples], close_prices[i:i+number_of_samples]))

        for i in range(len(close_prices)-number_of_samples -1):
            RSI.append(TI.RSI(myTI, close_prices[i:i+number_of_samples]))

        for i in range(len(close_prices)-number_of_samples -1):
            AROONUP.append(TI.AROONUP(myTI, close_prices[i:i+number_of_samples]))

        for i in range(len(close_prices)-number_of_samples -1):
            AROONDOWN.append(TI.AROONDOWN(myTI, close_prices[i:i+number_of_samples]))

        for i in range(len(close_prices)-number_of_samples -1):
            BBRAND.append(TI.BBRAND(myTI, close_prices[i:i+number_of_samples], low_prices[i:i+number_of_samples], high_prices[i:i+number_of_samples]))

        #Makes a list containing the grow of a stock over a certain period
        periodical_grow = []

        for i in range(len(close_prices)-number_of_samples-2):
            periodical_grow.append(close_prices[i]-close_prices[i+1])

        #Combine the periodical grow and the technical indicators in one list of lists
        all_data = []

        for i in range(len(close_prices)-number_of_samples-2):
            all_data.append([periodical_grow[i], EMA[i+1]-SMA[i+1], GROW[i+1], MACD[i+1], STOCH[i+1], RSI[i+1], AROONDOWN[i+1], AROONUP[i+1]])

        #Makes a dictionary containing the best weights for every stock
        dict_weights["{0}".format(file_name)], count = Regression.regression(myRegression, all_data)
        print(count)
print(dict_weights)
