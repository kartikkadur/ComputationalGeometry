#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of Graham scan algorithm which finds a convex hull given a set
of points.
Created on Wed Nov 13 15:03:33 2019

@author: karthikkr
"""
import matplotlib.pyplot as plt 
import numpy as np
import math
import argparse

from plyfile import PlyData, PlyElement
from matplotlib import animation

class GrahamScan():

    def __init__(self, plyfile):
        """
        initialization
        """
        self.data = PlyData.read(plyfile)
        self.P = list(zip(self.data.elements[0].data["x"],\
                          self.data.elements[0].data["y"]))

    def delete(self, index, _list):
        """
        delete the element from the list
        """
        for i in index:
            del _list[i]

    def get_angle(self, a, b, c):
        """
        gets the angle between three points
        """
        ang = math.degrees(math.atan2(c[1]-b[1], \
                            c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
        return ang + 360 if ang < 0 else ang

    def upper_hull(self):
        """
        Computes the upper hull of 
        """
        # sort points based on x coordinates
        self.P.sort(key=lambda tup: tup[0])
        l_upper = self.P[:2]
        
        for i in range(3, len(self.P)):
            l_upper.append(self.P[i])

            while((len(l_upper)> 2) and self.get_angle(l_upper[-3], \
                  l_upper[-2], l_upper[-1]) > 180):
                self.delete([-2], l_upper)
        return l_upper

    def lower_hull(self):
        """
        Computes the lower hull of 
        """
        P = list(reversed(self.P))
        l_lower = P[:2]
        for i in range(3, len(P)):
            l_lower.append(P[i])

            while((len(l_lower)> 2) and self.get_angle(l_lower[-3], \
                  l_lower[-2], l_lower[-1]) > 180):
                self.delete([-2], l_lower)

        # delete first and last point in l_lower
        self.delete([0, -1], l_lower)
        return l_lower

    def graham_scan(self):
        """
        complete gramscanalgorithm
        """
        upper_hull = self.upper_hull()
        lower_hull = self.lower_hull()

        return upper_hull + lower_hull


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=\
                            'Graham Scan Algorithm for finding convex hull')
    parser.add_argument('FILE', metavar='FILE', \
                        help='path to the input .ply file.')
    parser.add_argument('-f', metavar='OUTFILE', default = 'output.ply', \
        help='path to the .ply file to which the output has to be written.')
    args = parser.parse_args()
    
    # gramscanalgorithm
    gs = GrahamScan(args.FILE)
    # get the convex hull
    ch = gs.graham_scan()

    x_points = [i[0] for i in ch]
    x_points.append(x_points[0])

    y_points = [i[1] for i in ch]
    y_points.append(y_points[0])

    # save the ply file
    vertex = np.array(ch, dtype=[('x', 'f4'), ('y', 'f4')])
    element = PlyElement.describe(vertex, 'vertex')
    PlyData([element],  text=True).write(args.f)

    # plot the graph
    plt.scatter(gs.data.elements[0].data["x"], gs.data.elements[0].data["y"])
    plt.plot(x_points, y_points, color = "black")
    plt.show()