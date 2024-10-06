import csv

def read_csv(file_name):
    new_name = file_name.replace(".csv","")
    try:
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)
            print(f"{new_name}")
            for row in csv_reader:
                print(f" {row}\n \n")
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
    except Exception as e:
        print(f"An error occurred while reading {file_name}: {e}")

def datareader():
    read_csv('NEO PHA Database.csv')
    read_csv('Near Earth Comet Database.csv')
    read_csv('Planets Database.csv')

datareader()
