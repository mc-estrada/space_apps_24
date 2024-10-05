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

def populate_plane(ax):
    #read from database and create initial data-points

    #create test object (0,0,0)
    points = [(0, 0, 0)]

    plot_point(ax, points)

    return

def update_plane():

    return


def next_position(object):
    #read current position:

    return


def main():
    ax = create_base_plane()
    populate_plane(ax)
    update_plane()

    plt.show()
    return

if __name__ == "__main__":
    main()
