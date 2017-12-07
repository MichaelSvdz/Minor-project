from TICalculations import TI
import glob

myTI = TI()
number_of_samples = 10

datafiles =  glob.glob("datasets/*/*.csv")
for file_name in datafiles:
    print(file_name)
    with open(file_name, "r") as f:
        close_prices = []
        time_stamp = []



        for row in f:
            row = row.strip()
            row = row.split(",")
            close_prices.append(row[3])
            time_stamp.append(row[0])

        del close_prices[0]
        del time_stamp[0]
        close_prices = list(map(float, close_prices))

        SMA = []
        EMA = []
        MACD = []

        for i in range(len(close_prices)-number_of_samples -1):
            SMA.append(TI.SMA(myTI, close_prices[i:i+number_of_samples]))

        for i in range(len(close_prices)-number_of_samples -1):
            EMA.append(TI.EMA(myTI, close_prices[i:i+number_of_samples]))

        for i in range(len(close_prices)-number_of_samples -1):
            MACD.append(TI.MACD(myTI, close_prices[i:i+number_of_samples]))

    print(SMA[0])
    print(EMA[0])
    print(MACD[0])