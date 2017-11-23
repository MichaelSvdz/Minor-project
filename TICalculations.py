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
