import csv
import os
import json
import matlab.engine
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_base_plane():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = np.linspace(-10, 10, 10)
    y = np.linspace(-10, 10, 10)
    x, y = np.meshgrid(x, y)
    z = np.zeros_like(x)

    ax.plot_surface(x, y, z, alpha=0.5, rstride=100, cstride=100)

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-5, 5])

    return ax

def plot_point(ax, points):
    x, y, z = zip(*points)
    ax.scatter(x, y, z, c='r', marker='o')

def read_neo_pha_database(filename):
    neo_pha_data = []

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {
                'full_name': row['full_name'].strip(),
                'diameter': float(row['diameter']) if row['diameter'] else None,
                'epoch': float(row['epoch']),
                'e': float(row['e']),
                'a': float(row['a']),
                'q': float(row['q']),
                'i': float(row['i']),
            }
            neo_pha_data.append(data)

    return neo_pha_data

def read_near_earth_comet_database(filename):
    near_earth_comet_data = []

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {
                'full_name': row['full_name'].strip(),
                'H': float(row['H']) if row['H'] else None,
                'G': float(row['G']) if row['G'] else None,
                'epoch': float(row['epoch']),
                'e': float(row['e']),
                'a': float(row['a']),
                'q': float(row['q']),
                'i': float(row['i']),
            }
            near_earth_comet_data.append(data)

    return near_earth_comet_data

def populate_plane(ax, neo_pha_data, near_earth_comet_data):
    neo_points = [
        (
            data['a'] * np.cos(np.radians(data['i'])),  # x
            data['a'] * np.sin(np.radians(data['i'])),  # y
            data['q']                                    # z
        )
        for data in neo_pha_data if data['a'] is not None and data['i'] is not None and data['q'] is not None
    ]

    comet_points = [
        (
            data['a'] * np.cos(np.radians(data['i'])),  # x
            data['a'] * np.sin(np.radians(data['i'])),  # y
            data['q']                                    # z
        )
        for data in near_earth_comet_data if data['a'] is not None and data['i'] is not None and data['q'] is not None
    ]

    plot_point(ax, neo_points)
    plot_point(ax, comet_points)

def load_data():
    # Load the data from the files
    neo_pha_data = read_neo_pha_database('NEO PHA Database.csv')
    near_earth_comet_data = read_near_earth_comet_database('Near Earth Comet Database.csv')
    
    return neo_pha_data, near_earth_comet_data



def update_plane():

    return


def next_position(object):
    #read current position:

    return


def main():
    # Create base 3D plane
    ax = create_base_plane()
    
    # Load the data from the CSV files
    neo_pha_data, near_earth_comet_data = load_data()
    
    # Populate the plane with data from both databases
    populate_plane(ax, neo_pha_data, near_earth_comet_data)

    # Update the plane (this is a placeholder)
    update_plane()

    # Display the plot
    plt.show()

    return

if __name__ == "__main__":
    main()