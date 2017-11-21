import matplotlib.pyplot as plt
import ssl
import alpha_vantage.alpha_vantage.techindicators as ti
import _csv
import time
with open("SP500.csv", "r") as sp500:
    sp_reader = sp500.readlines()

print(sp_reader)

stocks = ["MSFT", "GOOGL", "RHT"]
smaPerDag = [0.0, 0.0, 0.0]
for x in range(3):
    print(x)
for company in sp_reader:
    company = company.strip()
    ts = ti.TechIndicators(key='OJGCX4Y5UT2YRRKY', output_format='pandas')
    data, meta_data = ts.get_sma(company, interval="weekly", time_period=30, series_type='close')
    #data['SMA'].plot()
    needed_sma = data["SMA"][len(data["SMA"])-10:len(data["SMA"])-2]
    print(needed_sma)

    weighted_sma = 0
    for i in range(4,0,-1):
        print(i)
        print(needed_sma[i+1])
        print(needed_sma[i])
        weighted_sma += (needed_sma[i+1]-needed_sma[i])*(0.6+0.1*i)

    print(weighted_sma, company)
    #stock = (data['SMA'][19] - data['SMA'][0]) / 30
    #print("The SMA of {0} is {1}".format(company, last_sma))

    #smaPerDag[i] = stock
#print(smaPerDag)
    #plt.title('Intraday Times Series for the MSFT stock (1 min)')
    #plt.show()
###
