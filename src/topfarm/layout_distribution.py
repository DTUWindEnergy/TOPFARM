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

from openmdao.lib.datatypes.api import VarTree, Float, Slot, Array, List, Int, Str, Dict, Enum
from openmdao.main.api import Component
from numpy import zeros
from lib import *

spiral = lambda t_, a_, x_: [a_*t_**(1./x_) * np.cos(t_), a_*t_**(1./x_) * np.sin(t_)]

class DistributeSpiral(Component):
    borders = Array(iotype='in', desc='The polygon defining the borders ndarray([n_bor,2])', unit='m')
    baseline =  Array(unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')
    pos = Array(iotype='in', desc='[n_wt]')
    spiral_param = Float(5.0, iotype='in', desc='spiral parameter')


    wt_positions = Array([], unit='m', iotype='out', desc='Array of wind turbines attached to particular positions')

    inc = 0

    #VarTree version
    #baseline = VarTree(GenericWindFarmTurbineLayout(), iotype='in', desc='wind turbine properties and layout') 
    #wt_layout = VarTree(GenericWindFarmTurbineLayout(), iotype='out', desc='wind turbine properties and layout') 
      
    def execute(self):
        #if self.inc == 0:
        #   self.polyfill = PolyFill(self.borders, 100, 100)
        #   self.old_positions = self.baseline
        #self.wt_layout = self.baseline
        #self.wt_layout.wt_positions += self.pos * scaling
        #new_positions = self.baseline + self.pos * scaling_dist
        new_positions = self.baseline.copy()
        for i in range(self.baseline.shape[0]):
            new_positions[i,:] = self.baseline[i,:] +  spiral(self.pos[i] *10*np.pi, self.spiral_param, 1.)
            inc = 0.0
            while not point_in_poly(new_positions[i,0], new_positions[i,1], self.borders):
                inc += 0.01 
                new_positions[i,:] = self.baseline[i,:] + spiral((self.pos[i]+inc) *10*np.pi, self.spiral_param, 1.)

        self.wt_positions =  new_positions
        #self.wt_positions =  self.polyfill.update(self.old_positions, new_positions)
        self.old_positions = self.wt_positions.copy()
        self.inc += 1

class DistributeXY(Component):
    borders = Array(iotype='in', desc='The polygon defining the borders ndarray([n_bor,2])', unit='m')
    baseline =  Array(unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')
    pos = Array(iotype='in', desc='[n_wt,2]')
    scaling_dist = Float(1.0, iotype='in', desc='The scaling distance to use')

    wt_positions = Array([], unit='m', iotype='out', desc='Array of wind turbines attached to particular positions')

    inc = 0
      
    def execute(self):
        if self.inc == 0:
           self.polyfill = PolyFill(self.borders, 100, 100)
           self.old_positions = self.baseline
        new_positions = self.baseline.copy() + self.pos * self.scaling_dist
        self.wt_positions =  self.polyfill.update(self.old_positions, new_positions)
        self.old_positions = self.wt_positions.copy()
        self.inc += 1

