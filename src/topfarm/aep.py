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
from gclarsen.fused import FGCLarsen

from tlib import TopfarmComponent

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




class TopFGCLarsen(FGCLarsen):
    """
    Calculate the wind turbine power using the GCLarsen model.
    This version gives the standard FGCLarsen interfaces, but replace the wt_layout.wt_positions by the input
    wt_positions. This is done to speed-up the variable copy in openMDAO. The idea is that at each iteration, it's not
    necessary to copy arround wt_layout.
    """
    wt_positions = Array([], unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')

    def execute(self):
        self.wt_layout.wt_positions = self.wt_positions
        super(TopFGCLarsen, self).execute()

class AEPM(AEPMultipleWindRoses):
    """
    Calculate the AEP of a wind farm. Provide the standard AEPMultipleWindRoses interfaces, with in addition the
    possibility to change the layout of the windfarm using wt_positions as an interface.
    """
    wt_positions = Array([], unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')

    def __init__(self, wake_model=TopFGCLarsen(), **kwargs):
        """
        :param wake_model: A GenericWindFarm compatible model
        """
        self.wake_model = wake_model
        super(TopAEP, self).__init__(**kwargs)




    def configure(self):
        """
        Configure the assembly.
        :param wake_model: The wake model
        :return:
        """
        self.add('wf', self.wake_model)
        super(TopAEP, self).configure()
        self.connect('wt_positions', 'wf.wt_positions')

def weibullCDF(x,A,k):
    """
    Returns the CDF of a weibull distribution over a vector x

    :param x: list or ndarray[n]
    :param A: Weibull coefficient A
    :param k: Weibull coefficient k
    :return: CDF
    """
    return 1.0 - np.exp(-(np.array(x)/A)**k)

class AEP(TopfarmComponent):

    # Inputs
    wind_speeds = List([], iotype='in', units='m/s',
        desc='The different wind speeds to run [nWS]')

    wind_directions = List([], iotype='in', units='deg',
        desc='The different wind directions to run [nWD]')

    wt_positions = Array(iotype='in')

    scaling = Float(1.0, iotype='in', desc='Scaling of the AEP')

    # Outputs
    array_aep = Array([], iotype='out', units='kW*h',
        desc='The energy production per sector [nWD, nWS]')

    gross_aep = Float(iotype='out', units='kW*h',
        desc='Gross Annual Energy Production before availability and loss impacts')

    net_aep = Float(iotype='out', units='kW*h',
        desc='Net Annual Energy Production after availability and loss impacts')

    capacity_factor = Float(0.0, iotype='out',
        desc='Capacity factor for wind plant')


    def __init__(self, wt_layout, wind_rose, wf, **kwargs):
        """

        :param wt_layout: GenericWindFarmTurbineLayout()
        :param wind_rose: WeibullWindRoseVT()
        :param wf: GenericWindFarm()
        :param scaling: float [default = 1.0]
                        The scaling used to calculate the net_aep. If it is set to 0.0, the scaling
                        will be set to the net_aep the first time the simulation is run.
        """
        self.wf = wf
        self.wf.wt_layout = wt_layout
        self.wind_rose = wind_rose
        super(AEP, self).__init__(**kwargs)

    def execute(self):

        # build the cdf vector of the wind speed for each wind rose wind direction sector
        cdfw = []
        for iwd, wd in enumerate(self.wind_rose.wind_directions):
            cdfw.append(weibullCDF(self.wind_speeds, self.wind_rose.A[iwd], self.wind_rose.k[iwd]))

        # calculate the probability in each wind direction sector, using the CDF of the wind rose wind direction
        cdfd0 = [sum(self.wind_rose.frequency[:i]) for i in range(len(self.wind_rose.frequency)+1)]
        wd = np.hstack([self.wind_rose.wind_directions, [360]])
        cdfd1 = interp1d(wd, cdfd0)(self.wind_directions)

        net_aep = 0.0
        gross_aep = 0.0
        cwd = 0
        net_aeps = np.zeros([len(self.wind_directions)])
        gross_aeps = np.zeros([len(self.wind_directions)])
        for iwd, wd in enumerate(self.wind_directions):
            if cwd < len(self.wind_rose.wind_directions):
                while wd >= self.wind_rose.wind_directions[cwd+1] and cwd < len(self.wind_rose.wind_directions)-2:
                    # switching wind rose wind direction sector
                    cwd += 1
            powers = np.zeros([len(self.wind_speeds)])
            for iws, ws in enumerate(self.wind_speeds):
                self.wf.wt_layout.wt_positions=self.wt_positions
                self.wf.wind_speed=ws
                self.wf.wind_direction=wd
                self.wf.run()
                powers[iws] = self.wf.power

            # Integrating over the wind speed CDF
            net_aeps[iwd] = np.trapz(powers, cdfw[cwd]) * 365.0 * 24.0
            for i in range(self.wt_positions.shape[0]):
                power_curve = interp1d(self.wf.wt_layout.wt_list[i].power_curve[:,0],
                               self.wf.wt_layout.wt_list[0].power_curve[:,1])(self.wind_speeds)
                gross_aeps[iwd] += np.trapz(power_curve, cdfw[cwd]) * 365.0 * 24.0

        # Integrating over the wind direction CDF
        net_aep = np.trapz(net_aeps, cdfd1)
        gross_aep = np.trapz(gross_aeps, cdfd1)

        self.capacity_factor = net_aep / gross_aep

        if self.scaling == 0.0:
            # The scaling has to be calculated
            self.scaling = net_aep

        self.net_aep = net_aep / self.scaling
        self.gross_aep = gross_aep
