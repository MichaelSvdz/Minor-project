stock = input("What Stock?")
number_of_samples = int(input("How much samples?"))
file_name = "datasets/financials/{0}.csv".format(stock)

f = open(file_name, "r")
close_prices = []

for row in f:
    row = row.strip()
    row = row.split(",")
    close_prices.append(row[3])
    if len(close_prices) == number_of_samples + 1:
        break

del close_prices[0]
close_prices = list(map(float, close_prices))

new_price = (close_prices[0]-close_prices[len(close_prices)-1])/number_of_samples + close_prices[0]


print(close_prices[0],close_prices[9])
print(price())