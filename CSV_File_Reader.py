import csv

def read_csv(file_name):
    try:
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                print(row)
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
    except Exception as e:
        print(f"An error occurred while reading {file_name}: {e}")

def datareader():
    read_csv('NEO_PHA_Database.csv')
    read_csv('Near_Earth_Comet_Database.csv')
    read_csv('Planets_Database.csv')

datareader()
