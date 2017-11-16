import matplotlib.pyplot as plt
import ssl
import alpha_vantage.alpha_vantage.techindicators as ti

stocks = ["MSFT", "GOOGL", "RHT"]
for s in stocks:
    ts = ti.TechIndicators(key='OJGCX4Y5UT2YRRKY', output_format='pandas')
    data, meta_data = ts.get_ema(symbol=s)
    data['close'].plot()
    plt.title('Intraday Times Series for the MSFT stock (1 min)')
    plt.show()
