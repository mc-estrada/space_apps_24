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


def calculate_position(a, e, i, om, w, ma):
    # Convert degrees to radians
    i = np.radians(i)
    om = np.radians(om)
    w = np.radians(w)
    ma = np.radians(ma)

    # Calculate the eccentric anomaly (E) using Kepler's equation
    E = ma + (e * np.sin(ma))  # First approximation

    # Iterate to find a more accurate E
    for _ in range(10):  # 10 iterations for convergence
        E = ma + e * np.sin(E)

    # Calculate the true anomaly (ν)
    ν = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))

    # Distance from the Sun
    r = a * (1 - e * np.cos(E))

    # Heliocentric coordinates
    x = r * (np.cos(om) * np.cos(w + ν) - np.sin(om) * np.sin(w + ν) * np.cos(i))
    y = r * (np.sin(om) * np.cos(w + ν) + np.cos(om) * np.sin(w + ν) * np.cos(i))
    z = r * (np.sin(w + ν) * np.sin(i))

    return x, y, z



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

    #print all data
    print("Planets:")
    for planet in planets:
        print(f"Name: {planet.full_name}, Eccentricity: {planet.orbit.e}, "
              f"Semi-major axis: {planet.orbit.a} AU, "
              f"Diameter: {planet.physical.diameter} km")

    print("\nNEOs:")
    for neo in neos:
        print(f"Name: {neo.full_name}, Eccentricity: {neo.orbit.e}, "
              f"Semi-major axis: {neo.orbit.a} AU, "
              f"Diameter: {neo.physical.diameter} km, "
              f"NEO: {neo.neo}, PHA: {neo.pha}")

    print("\nComets:")
    for comet in comets:
        print(f"Name: {comet.full_name}, Eccentricity: {comet.orbit.e}, "
              f"Semi-major axis: {comet.orbit.a} AU, "
              f"Diameter: {comet.physical.diameter} km, "
              f"H: {comet.comet_params.H}")


    #set up initial position
    populate_plane(ax, planets, neos, comets)
    plt.show()
    #calculate orbits and position changes
    update_plane()


if __name__ == "__main__":
    main()
