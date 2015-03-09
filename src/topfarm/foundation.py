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

from numpy import array, isnan
from openmdao.main.component import Component
from openmdao.main.datatypes.array import Array
from openmdao.main.datatypes.float import Float
from scipy.interpolate.interpnd import LinearNDInterpolator
from tlib import TopfarmComponent


class FoundationLength(TopfarmComponent):
    wt_positions = Array([], unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')
    ##wt_layout = VarTree(GenericWindFarmTurbineLayout(), iotype='in', desc='wind turbine properties and layout')
    borders = Array(iotype='in', desc='The polygon defining the borders ndarray([n_bor,2])', unit='m')
    depth = Array(iotype='in', desc='An array of depth ndarray([n_d, 2])', unit='m')
    foundation_length = Float(iotype='out', desc='The total foundation length of the wind farm')
    foundations = Array(iotype='out', desc='The foundation length ofeach wind turbine')
    scaling = Float(1.0, iotype='in', desc='scaling of the foundation')
    inc = 0



    def execute(self):
        foundation_func = LinearNDInterpolator(self.depth[:,0:2],self.depth[:,2])
        self.foundations = array([foundation_func(self.wt_positions[i,0],self.wt_positions[i,1]) for i in range(self.wt_positions.shape[0])])
        #dist = DistFromBorders()(wt_positions=self.wt_positions, borders=self.borders).dist
        min_depth = self.depth[:,2].min()
        self.foundations[isnan(self.foundations)] = min_depth

        if self.scaling == 0.0:
            # Using the baseline for scaling
            self.scaling = sum(self.foundations)

        self.foundation_length = sum(self.foundations)/self.scaling
        # print 'foundations:', self.foundation_length
