import csv
def datareader():
    with open('NEO PHA Database.cvs', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            print(row)
    with open('Near Earth Comet Database.cvs', 'r') as file:
        csv_reader2 = csv.reader(file)
        for row in csv_reader2:
            print(row)
    with open('Planets Database.cvs', 'r') as file:
        csv_reader3 = csv.reader(file)
        for row in csv_reader3:
            print(row)

datareader()
