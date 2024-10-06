import csv

def datareader():
    with open('NEO_PHA_Database.cvs', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            print(row)
    
    with open('Near_Earth_Comet_Database.cvs', 'r') as file:
        csv_reader2 = csv.reader(file)
        for row in csv_reader2:
            print(row)
    
    with open('Planets_Database.cvs', 'r') as file:
        csv_reader3 = csv.reader(file)
        for row in csv_reader3:
            print(row)

datareader()
