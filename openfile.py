x = [ 9, 3, 4, 3, 5, 6, 7,4, 2]
y = [ "ja", 5, 8, 10, "nee", 3, 2,3]

zipped = list(zip(x,y))
print(zipped)
print(sorted(zipped, reverse=True))
print(zipped[0:2])