import csv


with open('report_csv.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar=' ')
    i=0
    for row in spamreader:
        print(str(i.__str__()+" ")+' | '.join(row))
        i=i+1