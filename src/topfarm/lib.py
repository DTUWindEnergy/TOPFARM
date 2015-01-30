# TOPFARM - A Multi-fidelity Wind Farm Layout Optimization Tool
# Copyright (C) 2015  DTU Wind Energy, the TOPFARM development Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Pierre-Elouan Rethore'
__email__ = "pire@dtu.dk"
__version__ = '0.01a'
__copyright__ = "Copyright 2015, DTU Wind Energy, TOPFARM Development Team"
__license__ = "AGPL v3"
__status__ = "Alpha"

from openmdao.main.api import Component, Assembly
from openmdao.lib.datatypes.api import VarTree, Float, Slot, Array, List, Int, Str, Dict
from numpy import sqrt, argmin, array, zeros, isnan, meshgrid, linspace
from scipy.interpolate import RectBivariateSpline, LinearNDInterpolator
from scipy.spatial import ConvexHull
from matplotlib.pyplot import plot


import numpy as np

class ConverHullArea(Component):
    wt_positions = Array([], unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')
    #wt_layout = VarTree(GenericWindFarmTurbineLayout(), iotype='in', desc='wind turbine properties and layout') 
    area = Float(iotype='out', desc='The convex hull area around the wind farm', unit='m*m')

    def execute(self):
        ch = ConvexHull(self.wt_positions)
        area = polygon_area(self.wt_positions[ch.vertices,:])

class DistFromBorders(Component):
    wt_positions = Array([], unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')
    #wt_layout = VarTree(GenericWindFarmTurbineLayout(), iotype='in', desc='wind turbine properties and layout') 
    borders = Array(iotype='in', desc='The polygon defining the borders ndarray([n_bor,2])', unit='m')
    dist = Array(iotype='out', desc="""The distance of each turbine to the borders ndarray([n_wt, n_bor]). 
                                       Positive if inside, negative if outside""", unit='m')
    scaling = Float(1.0, iotype='in', desc='scaling of the dist')

    def execute(self):
        self.dist = array([dist_from_poly(x,y, self.borders) for x, y in self.wt_positions])/self.scaling
        # print 'borders',min(self.dist.flatten())


class DistFromTurbines(Component):
    wt_positions = Array([], unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')
    #wt_layout = VarTree(GenericWindFarmTurbineLayout(), iotype='in', desc='wind turbine properties and layout') 
    threshold = Float(iotype='in', desc='The threshold value the wind turbines should not be under', unit='m')
    dist = Array(iotype='out', desc="""The distance between each turbines ndarray([n_wt]).""", unit='m')
    scaling = Float(1.0, iotype='in', desc='')
    min_dist = Float(iotype='out', desc='')
    mean_dist = Float(iotype='out', desc='')

    def execute(self):
        n_wt = self.wt_positions.shape[0]
        if n_wt>0:
            dist = wt_dist(self.wt_positions, diag=100000.) / self.scaling
            self.dist = np.array([dist[i,:].min() for i in range(n_wt)])
            #print self.dist

            non_diag = np.array([dist[i,range(i)+range(i+1,n_wt)].min() for i in range(n_wt)])
            self.min_dist = non_diag.min()
        else:
            self.min_dist = 0.
            self.mean_dist = 0.
            self.dist = array([])



def points_in_poly(x,y,poly):
    """Helper function to run the point_in_poly using ndarrays(n,m) of point positions. Return an ndarray(n,m) of bools"""
    return array([point_in_poly(x_, y_, poly) for x_, y_ in zip(x.flatten(), y.flatten())]).reshape(x.shape)

def point_in_poly(x,y,poly):
    """
    determine if a point is inside a given polygon or not

    Inputs
    ------
    x: [float] x position of the point in [m]
    y: [float] y position of the point in [m]
    poly: [ndarray(n,2)] position of the polygon points in [m]

    Output
    -------
    inside: [bool]
    """
    n = poly.shape[0]
    inside = False

    p1x,p1y = poly[0,0:2]
    for i in range(n+1):
        p2x,p2y = poly[i % n,0:2]
        if y > min(p1y,p2y) and y <= max(p1y,p2y) and x <= max(p1x,p2x):
            if p1y != p2y:
                xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
            if p1x == p2x or x <= xints:
                inside = not inside
        p1x,p1y = p2x,p2y

    return inside    


def dist_from_poly(x,y, poly):
    """
    Calculate the minimum distance from an edge of the polygon. 
    It's positive if the point is inside the polygon, and negative otherwise.
    
    Inputs
    ------
    x, y: floats the position of the point
    poly: ndarray([n,2]) the points defining the polygon

    Output:
    -------
    dist_from_poly: float
    """
    if point_in_poly(x,y,poly):
        in_ = 1
    else:
        in_ = -1
    disto = zeros([poly.shape[0]])
    for i in range(len(poly)):
        i1 = i
        if i == len(poly) -1:
            i2 = 0
        else:
            i2 = i + 1
        P1 = poly[i1, 0:2]
        P2 = poly[i2, 0:2]
        #print P1, P2, [x,y]
        disto[i] = dist_from_segment(P1, P2, [x,y])
    disto[argmin(disto)] = disto[argmin(disto)] * in_
    #print disto
    return disto

l2_dist = lambda P1, P2: (P1[0] - P2[0])**2. + (P1[1] - P2[1])**2.
dist = lambda P1, P2: sqrt(l2_dist(P1,P2))

def dist_from_segment(P1, P2, P3):
    """ Calculate the distance of a point P3 from a segment defined by [P1,P2]
    Inputs
    ------
    P1: ndarray([2]) or [2]
    P2: ndarray([2]) or [2]
    P3: ndarray([2]) or [2]

    Output:
    -------
    dist: float
    """
    l2P2P1 = l2_dist(P2,P1) 
    if l2P2P1 == 0:
        return dist(P1,P3)
    x1, y1 = P1
    x2, y2 = P2
    x3, y3 = P3
    u = ((x3-x1)*(x2-x1) + (y3-y1)*(y2-y1)) / l2P2P1
    x = x1 + u*(x2-x1)
    y = y1 + u*(y2-y1)
    if u > 1.0: 
        x, y = P2
    if u < 0.0:
        x, y = P1
    #plot([x3, x],[y3, y],'k--')
    return dist([x,y], P3)
    
def wt_dist(wt_positions, diag=None):
    """ Calculate the minimum distance between the wind turbines in a wind farm.

    Input
    -----
    wt_positions: ndarray([n_wt, 2]) the x,y positions of the wind turbines
    diag: float/NaN/inf/None : the value to give the diagonal elements

    Output
    ------
    min_wt_dist: ndarray([n_wt, n_wt]).
    """
    n_wt = wt_positions.shape[0]
    out = array([dist(wt_positions[i,:], wt_positions[j,:]) for i in range(n_wt) for j in range(n_wt)]).reshape([n_wt, n_wt])
    if diag:
        for i in range(n_wt):
            out[i,i] = diag 
    return out

def polygon_area(array2d):
    """ Calculate the polygon_area

    Input
    ------
    array2d: ndarray(n,2) of ordered point positions

    Output
    ------
    area: float
    """
    return 0.5 * abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in segments(polygon(array2d))))

def segments(p):
    return zip(p, p[1:] + [p[0]])

def polygon(array2d):
    """ Return a list of tuples of vertices for a 2d array [n,2] """
    return [(array2d[i,0], array2d[i,1]) for i in range(array2d.shape[0])]


class PolyFill(object):
    """
    Object that takes a border polygon and a discretization, and provides functions to place wind farm layout within
    the borders.
    """

    max_step = 3
    
    def __init__(self, polygon, dx, dy):
        """
        Init the object, and fill the domain with points

        :param polygon: The borders of the domain, polygon array[n,2] [m]
        :param dx: spacing in x direction [m]
        :param dy: spacing in y direction [m]
        """
        self.polygon = polygon
        self.dx = dx
        self.dy = dy
        self.init_values()
        self.fill()
        
    def init_values(self):
        """
        Initialise the basic information about the domain
        """
        self.x_min = self.polygon[:,0].min()
        self.x_max = self.polygon[:,0].max()
        self.y_min = self.polygon[:,1].min()
        self.y_max = self.polygon[:,1].max()        
        self.lx = self.x_max - self.x_min
        self.ly = self.y_max - self.y_min
        self.nx = int(np.ceil(self.lx / self.dx))
        self.ny = int(np.ceil(self.ly / self.dy))
    
    def fill(self):
        """
        Fill the domain with points
        """
        self.xs = np.linspace(self.x_min, self.x_max, self.nx)
        self.ys = np.linspace(self.y_min, self.y_max, self.ny)
        self.X, self.Y = np.meshgrid(self.xs, self.ys)
        self.positions = np.array([[x,y] for x,y in zip(self.X.flatten(), self.Y.flatten())])
        self.In = np.array([points_in_poly(x,y,self.polygon) for x,y in zip(self.X.flatten(), self.Y.flatten())]).reshape(self.X.shape)
        
    def plot(self):
        plot(self.polygon[:,0], self.polygon[:,1], '--')
        plot(self.X[self.In].flatten(), self.Y[self.In].flatten(), 'k.')

    @property
    def in_positions(self):
        """
        returns an array containing all the points inside the polygon

        :return: ndarray[n, 2]
        """
        return np.array(zip(self.X[self.In].flatten(), self.Y[self.In].flatten()))

    def is_in(self, P):
        """
        Inform if the point is inside the borders of the domain

        :param P:   tuple, list or array
                    The point to test

        :return: boolean
                 is the point inside the polygon?
        """
        return point_in_poly(P[0], P[1], self.polygon)
    
    def is_in_id(self, i,j):
        """
        Inform if the indices are inside the acceptable domain

        :param i: int [0,len(self.nx)]
        :param j: int [0,len(self.ny)]
        :return: boolean
        """
        return self.In[i,j]
    
    def locate_ij(self, P):
        """
        Find the closest control point to the reference point P

        :param P: tuple, list or array
                    The reference point
        :return: [i,j]
                 indices in self.positions
        """
        a = np.argmin([(x-P[0])**2 + (y-P[1])**2 for x,y in self.positions])
        return int(np.ceil(a/self.nx)), a % self.nx   
    
    def locate_xy(self, i, j):
        """
        Returns the corresponding point to the indices i,j

        :param i: int
        :param j: int
        :return: array[2]
        """
        return array([self.X[i,j], self.Y[i,j]])
    
    def move(self, P0, P1):
        """
        Move a point P0 to a new legal location

        :param P0: ndarray[2]
        :param P1: ndarray[2]
        :return: ndarray[2]
        """
        x_dist, y_dist = P1 - P0
        tdist = np.sqrt(y_dist**2+x_dist**2)

        if self.is_in(P1):
            return P1
        else:
            x_steps = int(np.sign(x_dist) * np.ceil(abs(x_dist / self.dx)))#, self.max_step
            y_steps = int(np.sign(y_dist) * np.ceil(abs(y_dist / self.dy)))#, self.max_step
            i0, j0 = self.locate_ij(P0)
            P2 = self.locate_xy(i0, j0)
            P_off = P2 - P0
            self.loop_i = 0
            i1, j1 = self.valid_move(i0, j0, x_steps, y_steps, P_off)
            P2 = self.locate_xy(i1, j1) + P_off

            return P2
            
    def valid_move(self, i0, j0, x_steps, y_steps, P_off):
        """
        Function that move one index location to another according to an offset P_off

        :param i0:  int
                    origin index i
        :param j0:  int
                    origin index j
        :param x_steps: int
                        number of steps in x directions
        :param y_steps: int
                        number of steps in y directions
        :param P_off:   array[2]
                        [x,y] offset to displace the point
        :return:
        """
        self.loop_i += 1
        if self.loop_i>10:
            ## Making sure we get somewhere
            self.loop_i = 0
            return self.valid_move(i0, j0, x_steps+1, max(y_steps,1), P_off)
            
        i1 = (i0 + y_steps) % self.ny
        j1 = (j0 + x_steps) % self.nx

        P2 = self.locate_xy(i1, j1) + P_off

        if not self.is_in(P2):
            return self.valid_move(i1, j1, x_steps, y_steps, P_off)
        else:
            return i1, j1

    def update(self, old_positions, new_positions):
        """
        Update a former position to a new one, taking into account the border

        :param old_positions: array[n,2]
        :param new_positions: array[n,2]
        :return: array[n,2]
        """
        return np.array([self.move(P_old, P_new) for P_old, P_new in zip(old_positions, new_positions)])
