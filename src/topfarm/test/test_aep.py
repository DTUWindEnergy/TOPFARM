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
from numpy import linspace
from gclarsen.fusedwasp import PlantFromWWH

__author__ = 'Pierre-Elouan Rethore'
__email__ = "pire@dtu.dk"
__version__ = '0.01a'
__copyright__ = "Copyright 2015, DTU Wind Energy, TOPFARM Development Team"
__license__ = "AGPL v3"
__status__ = "Alpha"

from unittest import TestCase

class TopFGCLarsen(TestCase):
    pass

class TestTopAEP(TestCase):
    pass


class TestAEP(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_HR(self):
        """Testing that the AEP class performs identically to the AEPSingleWindRose class"""
        HR = [AEP(), AEPSingleWindRose()]

        for h in HR:
            h.wf = FGCLarsen()
            h.wind_speeds = linspace(4.,25.,10)
            h.wind_directions = linspace(0., 360., 36 )[:-1]
            h.wf.wt_layout = PlantFromWWH(filename='data/hornsrev1_turbine_nodescription.wwh').wt_layout

        HR[1].wind_rose = HR[1].wf.wt_layout.wt_wind_roses[0].weibull_array

