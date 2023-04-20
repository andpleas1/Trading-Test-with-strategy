import csv
import math
import datetime

#eliminate record in arr by index
def find_and_remove(arr, record, index):
    for i in range(len(arr)):
        if record[index] == record[index]:
            arr.pop(i)
            # print(record[4], i)
            break
    return arr


# Calculate volatility by hour
def getVolatilityByHour(arr, duration, last):
    # blockTime
    lastRec = last[0]

    #Calculate AverPrice
    averPrice = 0
    cnt = 0
    for i in reversed(range(len(arr))):
        averPrice += float(arr[i][4])
        cnt += 1
        if int(arr[i][0]) <= (int(lastRec) - duration):
            break
    averPrice = averPrice / cnt

    # calculate volatility
    volatility = 0
    for i in reversed(range(len(arr))):
        volatility = volatility + (float(arr[i][4]) - averPrice) ** 2
        if int(arr[i][0]) <= (int(lastRec) - duration):
            break
    # print(averPrice, cnt, volatility)
    volatility = volatility / cnt

    return math.sqrt(volatility)


# Convert time stamp to Date String
def convertTimeStampToDateStr(timestamp):
    # Convert timestamp to datetime object
    dt_object = datetime.datetime.fromtimestamp(int(timestamp))

    # Format datetime object as string
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')


# Open and read the data For Test Part1.csv
file = open("Data For Test Part 1.csv")
# file = open("test.csv")
type(file)
csvreader = csv.reader(file)

header = []
header = next(csvreader)
# rows = []
records = []


# Define arrays for Trx, sellers, bidders
buyNowArr = [] # Trx' order array
listArr = [] # Sellers' order array
bidArr = [] # Bidders order array

# Define tradePrice variable
tradePrice = 0

# Reading file by record
for row in csvreader:
    records.append(row)

# Looping Records from oldest one to latest
for i in reversed(range(len(records))):
    row = records[i]
    match row[10]:
        case "buyNow":
            buyNowArr.append(row)
            find_and_remove(listArr, row, 4)
            find_and_remove(bidArr, row, 4)
            tradePrice = row[4]
            # print("here we are", row[4])
        case "list":
            listArr.append(row) 
        case "bid":
            bidArr.append(row)
        case "cancelBid":
            # print(len(bidArr), "Bidding ------------")
            find_and_remove(bidArr, row, 1)
            # print(len(bidArr), "Bidding ------------")
        case "delist":
            # print(len(listArr), "Delist ------------")
            find_and_remove(listArr, row, 1)
            # print(len(listArr), "Delist ------------")


# Print Records, buyNowArr, ListArr, bidArr counts
# print(len(records), len(buyNowArr), len(listArr), len(bidArr))



# Print trade Price and also timestamp by following csv file
print ("Timestamp ", convertTimeStampToDateStr(records[0][0]))
tradePrice = round(float(tradePrice), 2)
print ("Trading Price (market price) is ", tradePrice)


# Get the best offer and bid by following csv file
bestOffer = listArr[0][4]
for record in listArr:
    if bestOffer > record[4]:
        bestOffer = record[4]

bestBid = bidArr[0][4]
for record in bidArr:
    if bestBid < record[4]:
        bestBid = record[4]

bestBid = round(float(bestBid), 2)
bestOffer = round(float(bestOffer), 2)

print ("Best Bid (buyer)", bestBid)
print ("Best Offer (seller)", bestOffer)

# print (records[0], len(buyNowArr))

# Calculate volitality for one, six, twentyfour hours by following csv file
volitality1 = getVolatilityByHour(buyNowArr, 3600, records[0])
volitality6 = getVolatilityByHour(buyNowArr, 3600 * 6, records[0])
volitality24 = getVolatilityByHour(buyNowArr, 3600 * 24, records[0])

print ("Volitality for 1 hour : ", round(volitality1,2))
print ("Volitality for 6 hour : ", round(volitality6,2))
print ("Volitality for 24 hour : ", round(volitality24,2))
# print(rows)


# Logging files on logMetrics.txt

logFile = open("logMetrics.txt", 'w')

line = "Timestamp " + convertTimeStampToDateStr(records[0][0]) + "\n"
logFile.write (line)

line = "Trading Price (market price) is " + str(tradePrice) + "\n"
logFile.write (line)

line = "Best Bid (buyer)" + str(bestBid) + "\n"
logFile.write (line)

line = "Best Offer (seller)" + str(bestOffer) + "\n"
logFile.write (line)

line = "Volitality for 1 hour : " + str(round(volitality1,2)) + "\n"
logFile.write (line)

line = "Volitality for 6 hour : " + str(round(volitality6,2)) + "\n"
logFile.write (line)

line = "Volitality for 24 hour : " + str(round(volitality24,2)) + "\n"
logFile.write (line)

logFile.close ()