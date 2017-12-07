import glob
import csv
import os

dirs = os.walk('.').next()[1]
for d in dirs:
    with open(d + ".csv", 'w+') as csvfile
    urlfiles =  glob.glob(d + "/*.csv")
    for u in urlfiles:
        print u
        with open(u, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            #for row in reader:
            #print(row[1])
