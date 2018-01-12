import statistics
import matplotlib.pyplot as plt

class TI:
    def SMA(self, Lijst):
        return sum(Lijst)/len(Lijst)

    def EMA(self, Lijst,K = 0):
        if K == 0:
            K = 2 / (len(Lijst) + 1)
        ema = TI.SMA(self, Lijst)
        for i in range(len(Lijst)-2, -1, -1):
            ema += K * (Lijst[i] - ema)
        return ema

    def GROW(selfs, Lijst):
        return Lijst[0]-Lijst[len(Lijst)-1]

    def MACD(self, Lijst):
        K1 = 0.15
        shortema = TI.SMA(self, Lijst)
        for i in range(len(Lijst)-2, -1, -1):
            shortema += K1 * (Lijst[i] - shortema)
        K2 = 0.075
        longema = TI.SMA(self, Lijst)
        for i in range(len(Lijst)-2, -1, -1):
            longema += K2 * (Lijst[i] - longema)
        return shortema - longema

    #not sure if complete
    def STOCH(self, lijst_lowest, lijst_highest, close):
        lowest_low = min(lijst_lowest)
        highest_high = max(lijst_highest)
        try:
            return (close[0] - lowest_low)/(highest_high-lowest_low)
        except ZeroDivisionError:
            return None

    def RSI(self, lijst_close):
        up = []
        dn = []
        for i in range(len(lijst_close)-1):
            if lijst_close[i] > lijst_close[i+1]:
                up.append(lijst_close[i] - lijst_close[i+1])
                dn.append(0)
            else:
                up.append(0)
                dn.append(lijst_close[i+1] - lijst_close[i])
        upavg = sum(up) / len(up)
        dnavg = sum(dn) / len(dn)
        try:
            RMI = upavg / (upavg + dnavg)
        except ZeroDivisionError:
            RMI = None
        return RMI

    def AROONUP(self, lijst_close):
        n = len(lijst_close)
        highest_close = lijst_close.index(max(lijst_close))
        return (n - highest_close) / n

    def AROONDOWN(self, lijst_close):
        n = len(lijst_close)
        lowest_close = lijst_close.index(min(lijst_close))
        return (n - lowest_close) / n

    def BBRAND(self, lijst_close, lijst_lowest, lijst_highest, number_of_standard_deviations = 2):
        TP = []
        for i in range(len(lijst_close)):
            TP.append((lijst_close[i]+lijst_lowest[i]+lijst_highest[i])/3)
        mid_band = TI.SMA(self, TP)
        upper_band = mid_band + number_of_standard_deviations * statistics.stdev(TP)
        lower_band = mid_band - number_of_standard_deviations * statistics.stdev(TP)
        return [lower_band, mid_band, upper_band]

    def OBV(self, lijst_close):
        obv = 0
        for i in range(len(lijst_close) - 1):
            if lijst_close[i] > lijst_close[i+1]:
                obv += lijst_close[i]
            elif lijst_close[i] < lijst_close[i+1]:
                obv -= lijst_close[i]
            else:
                continue
        return obv
