import os
import csv
#import json #not sure if still needed
#import matlab.engine //not needed anymore
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from space_data import load_files

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

"""
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
"""

def populate_plane(ax, planets, neos, comets):
    # planets, blue
    for planet in planets:
        x = planet.orbit.a * np.cos(np.radians(planet.orbit.L)) if planet.orbit.L is not None else 0
        y = planet.orbit.a * np.sin(np.radians(planet.orbit.L)) if planet.orbit.L is not None else 0
        z = 0
    ax.scatter(x, y, z, c='b', marker='o', label=planet.full_name)

    # NEOs, red
    for neo in neos:
        if neo.orbit.L is not None:  # Check if L is not None
            x = neo.orbit.a * np.cos(np.radians(neo.orbit.L))
            y = neo.orbit.a * np.sin(np.radians(neo.orbit.L))
        else:
            x, y = 0, 0
        z = 0
    ax.scatter(x, y, z, c='r', marker='^', label=neo.full_name)

    # comets, greem
    for comet in comets:
        if comet.orbit.L is not None:  # Check if L is not None
            x = comet.orbit.a * np.cos(np.radians(comet.orbit.L))
            y = comet.orbit.a * np.sin(np.radians(comet.orbit.L))
        else:
            x, y = 0, 0
        z = 0
        
        ax.scatter(x, y, z, c='g', marker='s', label=comet.full_name)

    return



"""
def load_data():
    # Load the data from the files
    neo_pha_data = read_neo_pha_database('NEO PHA Database.csv')
    near_earth_comet_data = read_near_earth_comet_database('Near Earth Comet Database.csv')
    
    return neo_pha_data, near_earth_comet_data
"""


def update_plane():

    return


def next_position(object):
    #read current position:

    return


def main():
    
    #set up space
    ax = create_base_plane()
    #load data
    planets, neos, comets = load_files()
    #set up initial position
    populate_plane(ax, planets, neos, comets)
    plt.show()



if __name__ == "__main__":
    main()