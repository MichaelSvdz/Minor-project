import glob
import csv
import os

test = {'2017-10-1': {'AES': {'open': '83'}}}

dirs = os.walk('.').next()[1]
for d in dirs:
    with open(d + ".csv", 'w+') as output:
        urlfiles =  glob.glob(d + "/*.csv")
        for u in urlfiles:
            with open(u, 'rb') as csvfile:
                reader = csv.reader(csvfile)
                #for row in reader:
                #print(row[1])
