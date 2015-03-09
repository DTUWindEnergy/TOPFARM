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
__version__ = '0.1.0'
__copyright__ = "Copyright 2015, DTU Wind Energy, TOPFARM Development Team"
__license__ = "AGPL v3"
__status__ = "Alpha"

from openmdao.lib.datatypes.api import VarTree, Float, Slot, Array, List, Int, Str, Dict, Enum
from openmdao.main.api import Component
from numpy import zeros

from tlib import point_in_poly, PolyFill, TopfarmComponent
import numpy as np

spiral = lambda t_, a_, x_: [a_*t_**(1./x_) * np.cos(t_), a_*t_**(1./x_) * np.sin(t_)]

class DistributeSpiral(TopfarmComponent):
    borders = Array(iotype='in', desc='The polygon defining the borders ndarray([n_bor,2])', unit='m')
    spiral_param = Float(5.0, iotype='in', desc='spiral parameter')
    wt_positions = Array([], unit='m', iotype='out', desc='Array of wind turbines attached to particular positions')

    inc = 0

    def __init__(self, wt_layout, **kwargs):
        """
        baseline =  Array(unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')
        pos = Array(iotype='in', desc='[n_wt]')

        :param wt_layout:
        :param borders:
        :param spiral_param:
        :return:
        """
        super(DistributeSpiral, self).__init__(**kwargs)

        self.original_wt_layout = wt_layout
        self.wt_names = wt_layout.wt_names
        self.baseline = wt_layout.wt_positions

        for wt_name in self.wt_names:
            self.add(wt_name, Float(0.0, iotype='in'))


    def list_design_variables(self):
        return [{'name': wt_name, 'start': 0.0, 'low': 0.0, 'high': 1.0, 'fd_step':0.005}
                for wt_name in self.wt_names]
      
    def execute(self):
        #if self.inc == 0:
        #   self.polyfill = PolyFill(self.borders, 100, 100)
        #   self.old_positions = self.baseline
        #self.wt_layout = self.baseline
        #self.wt_layout.wt_positions += self.pos * scaling
        #new_positions = self.baseline + self.pos * scaling_dist
        new_positions = self.baseline.copy()
        for i, wt_name in enumerate(self.wt_names):
            opos = getattr(self.original_wt_layout, wt_name).position
            parameter = getattr(self, wt_name)
            new_positions[i,:] = opos +  spiral(parameter *10*np.pi, self.spiral_param, 1.)
            inc = 0.0
            while not point_in_poly(new_positions[i,0], new_positions[i,1], self.borders):
                inc += 0.01 
                new_positions[i,:] = opos + spiral((parameter+inc) *10*np.pi, self.spiral_param, 1.)

        self.wt_positions =  new_positions
        #self.wt_positions =  self.polyfill.update(self.old_positions, new_positions)
        self.old_positions = self.wt_positions.copy()
        self.inc += 1


class DistributeXY(TopfarmComponent):
    borders = Array(iotype='in', desc='The polygon defining the borders ndarray([n_bor,2])', unit='m')
    baseline =  Array(unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')

    wt_positions = Array([], unit='m', iotype='out', desc='Array of wind turbines attached to particular positions')


    def __init__(self, wt_layout, **kwargs):
        super(DistributeXY, self).__init__(**kwargs)
        self.baseline = wt_layout.wt_positions
        self.wt_names = wt_layout.wt_names
        for wt_name in self.wt_names:
            self.add(wt_name+'_x', Float(0.0, iotype='in'))
            self.add(wt_name+'_y', Float(0.0, iotype='in'))


    def scale(self, x):
        return ((x[0]-self.borders[:,0].min())/(self.borders[:,0].max()-self.borders[:,0].min()),
                (x[1]-self.borders[:,1].min())/(self.borders[:,1].max()-self.borders[:,1].min()))

    def unscale(self, x):
        return (x[0] * (self.borders[:,0].max()-self.borders[:,0].min()) + self.borders[:,0].min(),
                x[1] * (self.borders[:,1].max()-self.borders[:,1].min()) + self.borders[:,1].min())


    def list_design_variables(self):
        return [{'name': wt_name+'_x', 'start': self.scale(self.baseline[i,:])[0], 'low': 0.0, 'high': 1.0, 'fd_step':0.005}
                for i, wt_name in enumerate(self.wt_names)] + \
               [{'name': wt_name+'_y', 'start': self.scale(self.baseline[i,:])[1], 'low': 0.0, 'high': 1.0, 'fd_step':0.005}
                for i, wt_name in enumerate(self.wt_names)]

    def execute(self):
        #if self.inc == 0:
        #   self.polyfill = PolyFill(self.borders, 100, 100)
        #   self.old_positions = self.baseline

        new_positions = np.array([self.unscale([getattr(self, wt_name+'_x'), getattr(self, wt_name+'_y')]) for wt_name in self.wt_names])
        #self.wt_positions =  self.polyfill.update(self.old_positions, new_positions)
        self.wt_positions =  new_positions
        self.old_positions = self.wt_positions.copy()
        #self.inc += 1



class DistributeFilledPolygon(DistributeXY):
    borders = Array(iotype='in', desc='The polygon defining the borders ndarray([n_bor,2])', unit='m')
    baseline =  Array(unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')

    wt_positions = Array([], unit='m', iotype='out', desc='Array of wind turbines attached to particular positions')

    def __init__(self, **kwargs):
        super(DistributeFilledPolygon, self).__init__(**kwargs)
        self.polyfill = PolyFill(self.borders, 100, 100)
        self.old_positions = self.baseline

    def execute(self):
        new_positions = np.array([self.unscale([getattr(self, wt_name+'_x'), getattr(self, wt_name+'_y')]) for wt_name in self.wt_names])
        self.wt_positions =  self.polyfill.update(self.old_positions, new_positions)
        self.old_positions = self.wt_positions.copy()


