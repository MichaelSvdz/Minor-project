import glob

from TICalculations import TI

myTI = TI()
days = 5
number_of_samples = 15
grow_dict = {}

with open("weight_dict.txt", "r") as weight_dict:
    weight_dict = eval(weight_dict.read())
    datafiles = glob.glob("datasets/*/*.csv")
    for file in datafiles:
        with open(file, "r") as f:
            open_prices = []
            high_prices = []
            low_prices = []
            close_prices = []
            time_stamp = []

            # parse the data file
            for row in f:
                row = row.strip()
                row = row.split(",")
                open_prices.append(row[1])
                high_prices.append(row[2])
                low_prices.append(row[3])
                close_prices.append(row[4])
                time_stamp.append(row[0])

            # remove the headers
            del open_prices[0]
            del high_prices[0]
            del low_prices[0]
            del close_prices[0]
            del time_stamp[0]

            # Convert the lists to the right type
            open_prices = list(map(float, open_prices))
            high_prices = list(map(float, high_prices))
            low_prices = list(map(float, low_prices))
            close_prices = list(map(float, close_prices))

            # Changes the lists so that you can specify an interval for the data
            temp_close = []
            temp_open = []
            temp_low = []
            temp_high = []

            for i in range(len(close_prices) - 1):
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

            SMA = TI.SMA(myTI, close_prices[0: number_of_samples])
            EMA = TI.EMA(myTI, close_prices[0: number_of_samples])
            GROW = TI.GROW(myTI, close_prices[0: number_of_samples])
            MACD = TI.MACD(myTI, close_prices[0: number_of_samples])
            STOCH = TI.STOCH(myTI, low_prices[0: number_of_samples], high_prices[0: number_of_samples],close_prices[0: number_of_samples])
            RSI = TI.RSI(myTI, close_prices[0: number_of_samples])
            AROONUP = TI.AROONUP(myTI, close_prices[0: number_of_samples])
            AROONDOWN = TI.AROONDOWN(myTI, close_prices[0: number_of_samples])

            indicator_list = [EMA - SMA, GROW, MACD, STOCH, RSI, AROONUP, AROONDOWN]

            stock_name = file.split("\\")[2].split(".")[0]

            weights = weight_dict[stock_name]
            expected_grow = sum([indicator_list[i] * weights[i] for i in range(len(indicator_list))])
            grow_dict[stock_name] = expected_grow
print(grow_dict)