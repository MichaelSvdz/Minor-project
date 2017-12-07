import statistics

def SMA(Lijst):
    return sum(Lijst)/len(Lijst)

def EMA(Lijst):
    K = 2 / (len(Lijst) + 1)
    print(K)
    ema = Lijst[len(Lijst)-1]
    print(ema)
    for i in range(len(Lijst)-2, -1, -1):
        ema += K * (Lijst[i] - ema)
        print(ema)
    return ema

def MACD(Lijst):
    K1 = 0.15
    shortema = Lijst[len(Lijst)-1]
    print(shortema)
    for i in range(len(Lijst)-2, -1, -1):
        shortema += K1 * (Lijst[i] - shortema)
    K2 = 0.075
    longema = Lijst[len(Lijst)-1]
    print(longema)
    for i in range(len(Lijst)-2, -1, -1):
        longema += K2 * (Lijst[i] - longema)
    return shortema - longema

#not sure if complete
def STOCH(lijst_lowest, lijst_highest, close):
    lowest_low = min(lijst_lowest)
    highest_high = max(lijst_highest)
    return (close - lowest_low)/(highest_high-lowest_low)

def RSI(lijst_close):
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
    RMI = upavg / (upavg + dnavg)
    return RMI

def AROONUP(lijst_close):
    n = len(lijst_close)
    highest_close = lijst_close.index(max(lijst_close))
    return (n - highest_close) / n

def ARRONDOWN(lijst_close):
    n = len(lijst_close)
    lowest_close = lijst_close.index(min(lijst_close))
    return (n - lowest_close) / n

def BBRAND(lijst_close, lijst_lowest, lijst_highest, number_of_standard_deviations = 2):
    TP = []
    for i in range(len(lijst_close)):
        TP.append((lijst_close[i]+lijst_lowest[i]+lijst_highest[i])/3)
    mid_band = SMA(TP)
    upper_band = mid_band + number_of_standard_deviations * statistics.stdev(TP)
    lower_band = mid_band - number_of_standard_deviations * statistics.stdev(TP)
    return [lower_band, mid_band, upper_band]

def OBV(lijst_close):
    obv = 0
    for i in range(len(lijst_close) - 1):
        if lijst_close[i] > lijst_close[i+1]:
            obv += lijst_close[i]
        elif lijst_close[i] < lijst_close[i+1]:
            obv -= lijst_close[i]
        else:
            continue
    return obv

