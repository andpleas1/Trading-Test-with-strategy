import csv
import datetime

def convertTimeStampToDateStr(timestamp):
    # Convert timestamp to datetime object
    dt_object = datetime.datetime.fromtimestamp(int(timestamp))

    # Format datetime object as string
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')

with open('stockData.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(["date", "open", "high", "low", "close"])

    file = open("Data For Test Part 1.csv")
    # file = open("test.csv")
    type(file)
    csvreader = csv.reader(file)

    header = []
    header = next(csvreader)
    # rows = []
    records = []

    for row in csvreader:
        records.append(row)
    
    file.close ()
    
    # candle stick for one hour
    duration = 3600
    startPoint = int(records[len(records) - 1][0])

    close = 0
    open = 0
    high = 0
    low = 0
    
    for i in reversed(range(len(records))):
        if startPoint <= (int(records[i][0]) - duration):
            writer.writerow([
                convertTimeStampToDateStr(records[i][0]),
                open,
                high,
                low,
                close,
            ])
            close = 0
            open = 0
            high = 0
            low = 0
            startPoint = int(records[i][0])

        if records[i][10] == "buyNow":
            close = float(records[i][4])
            print (close)
            if open == 0:
                open = high = low = close
            else:
                if close > high:
                    high = close
                if close < low:
                    low = close
