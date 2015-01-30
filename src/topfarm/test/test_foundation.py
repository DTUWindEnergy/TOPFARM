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


from numpy import loadtxt
from unittest import TestCase
from topfarm.foundation import FoundationLength
from numpy.testing import assert_almost_equal

class TestFoundationLength(TestCase):
    def setUp(self):
        self.fl = FoundationLength()

    # TODO: Test that the foundation length is calculated correctly

    def test_ref_waterdetpth(self):
        dat = loadtxt('data/WaterDepth1.dat')
        assert_almost_equal(dat.shape, [50, 50])