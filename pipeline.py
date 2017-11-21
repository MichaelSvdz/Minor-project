import matplotlib.pyplot as plt
import ssl
import alpha_vantage.alpha_vantage.techindicators as ti

stocks = ["MSFT", "GOOGL", "RHT"]
smaPerDag = [0.0, 0.0, 0.0]
for x in range(3):
    print(x)
for i in range(3):
    ts = ti.TechIndicators(key='OJGCX4Y5UT2YRRKY', output_format='pandas')
    data, meta_data = ts.get_sma(stocks[i], interval='daily', time_period=30, series_type='close')
    #data['SMA'].plot()
    stock = (data['SMA'][19] - data['SMA'][0]) / 30
    print(stock)
    smaPerDag[i] = stock
print(smaPerDag)
    #plt.title('Intraday Times Series for the MSFT stock (1 min)')
    #plt.show()
###
