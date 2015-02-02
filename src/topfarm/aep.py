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


# OpenMDAO imports
from openmdao.main.datatypes.array import Array
from openmdao.main.datatypes.float import Float
from openmdao.main.datatypes.list import List
from openmdao.main.component import Component


# FUSED-Wind imports
from fusedwind.plant_flow.asym import AEPMultipleWindRoses, BaseAEPModel
from fusedwind.interface import InterfaceSlot, implement_base
from fusedwind.plant_flow.comp import GenericWindFarm

# GCLarsen import
#from gclarsen.fused import FGCLarsen

# Other
import numpy as np
from scipy.interpolate import interp1d


#
# class TopFGCLarsen(FGCLarsen):
#     """
#     Calculate the wind turbine power using the GCLarsen model.
#     This version gives the standard FGCLarsen interfaces, but replace the wt_layout.wt_positions by the input
#     wt_positions. This is done to speed-up the variable copy in openMDAO. The idea is that at each iteration, it's not
#     necessary to copy arround wt_layout.
#     """
#     wt_positions = Array([], unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')
#
#     def execute(self):
#         self.wt_layout.wt_positions = self.wt_positions
#         super(TopFGCLarsen, self).execute()
#
# class TopAEP(AEPMultipleWindRoses):
#     """
#     Calculate the AEP of a wind farm. Provide the standard AEPMultipleWindRoses interfaces, with in addition the
#     possibility to change the layout of the windfarm using wt_positions as an interface.
#     """
#     wt_positions = Array([], unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')
#
#     def __init__(self, wake_model=TopFGCLarsen()):
#         """
#         :param wake_model: A GenericWindFarm compatible model
#         """
#         super(TopAEP, self).__init__()
#         self.add('wf', wake_model)
#
#
#     def configure(self):
#         """
#         Configure the assembly.
#         :param wake_model: The wake model
#         :return:
#         """
#
#         super(TopAEP, self).configure()
#         self.connect('wt_positions', 'wf.wt_positions')


def weibullCDF(x,A,k):
    """
    Returns the CDF of a weibull distribution over a vector x

    :param x: ndarray[n]
    :param A: Weibull coefficient A
    :param k: Weibull coefficient k
    :return: CDF
    """
    return 1.0 - np.exp(-(x/A)**k)

class AEP(Component):

    wf = InterfaceSlot(GenericWindFarm,
        desc='A wind farm assembly or component')

    # Inputs
    wind_speeds = List([], iotype='in', units='m/s',
        desc='The different wind speeds to run [nWS]')

    wind_directions = List([], iotype='in', units='deg',
        desc='The different wind directions to run [nWD]')

    wt_positions = Array(iotype='in')


    # Outputs
    array_aep = Array([], iotype='out', units='kW*h',
        desc='The energy production per sector [nWD, nWS]')

    gross_aep = Float(iotype='out', units='kW*h',
        desc='Gross Annual Energy Production before availability and loss impacts')

    net_aep = Float(iotype='out', units='kW*h',
        desc='Net Annual Energy Production after availability and loss impacts')

    capacity_factor = Float(0.0, iotype='out',
        desc='Capacity factor for wind plant')


    def __init__(self, wt_layout, wind_rose, wf):
        """

        :param wt_layout: GenericWindFarmTurbineLayout()
        :param wind_rose: WeibullWindRoseVT()
        :param wf: GenericWindFarm()
        """
        self.wf = wf
        self.wf.wt_layout = wt_layout
        self.wf.wt_layout.wind_roses = [wind_rose] * self.wf.wt_layout.n_wt

    def execute(self):
        power_curve = interp1d(self.wf.wt_layout.wt_list[0].power_curve[:,0],
                               self.wf.wt_layout.wt_list[0].power_curve[:,1])(self.wind_speeds)
        net_aep = 0.0
        gross_aep = 0.0
        for iwd, wd in enumerate(self.wind_directions):
            powers = np.zeros([len(self.wind_speeds)])
            for iws, ws in enumerate(self.wind_speeds):
                self.wf.wt_layout.wt_positions=self.wt_positions
                self.wf.wind_speed=ws
                self.wf.wind_direction=wd
                self.wf.run(force=True)
                powers[iws] = self.wf.power
            cdf = weibullCDF(self.wind_speeds, self.wind_rose.A[iwd], self.wind_rose.k[iwd])
            net_aep += np.trapz(powers, cdf) * 365.0 * 24.0
            gross_aep += np.trapz(power_curve, cdf) * 365.0 * 24.0

        self.net_aep = net_aep
        self.gross_aep = gross_aep
        self.capacity_factor = net_aep / gross_aep

