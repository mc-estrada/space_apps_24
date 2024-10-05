import csv

with open('NEO PHA Database.cvs', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)
