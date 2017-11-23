import urllib
import csv
import glob
import time
import os.path

urlfiles =  glob.glob("stocks/*.csv")
for u in urlfiles:
    with open(u, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not os.path.isfile("datasets/" + u[7:-4] + "/" + row[0] + ".csv"):
                url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + row[0] + "&apikey=OJGCX4Y5UT2YRRKY&outputsize=full&datatype=csv"
                testfile = urllib.URLopener()
                print u[7:-4]
                print row[0]
                try:
                    testfile.retrieve(url, "datasets/" + u[7:-4] + "/" + row[0] + ".csv")
                except:
                    pass
                time.sleep(0.6)
