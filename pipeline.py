import matplotlib.pyplot as plt
import ssl
import alpha_vantage.alpha_vantage.techindicators as av

stocks = ["MSFT", "GOOGL", "RHT"]
for s in stocks:
    ts = av.techindicators(key='OJGCX4Y5UT2YRRKY', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=s,interval='1min', outputsize='full')
    data['close'].plot()
    plt.title('Intraday Times Series for the MSFT stock (1 min)')
    plt.show()
