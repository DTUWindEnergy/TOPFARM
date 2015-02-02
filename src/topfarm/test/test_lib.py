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


from unittest import TestCase
from topfarm.lib import PolyFill
import numpy as np

__author__ = 'pire'


class TestConverHullArea(TestCase):
    pass


class TestDistFromBorders(TestCase):
    pass


class TestDistFromTurbines(TestCase):
    pass


class Test_points_in_poly(TestCase):
    pass


class Test_point_in_poly(TestCase):
    pass


class Test_dist_from_poly(TestCase):
    pass


class Test_dist_from_segment(TestCase):
    pass


class Test_wt_dist(TestCase):
    pass


class Test_polygon_area(TestCase):
    pass


class Test_segments(TestCase):
    pass


class Test_polygon(TestCase):
    pass


class TestPolyFill(TestCase):
    def setUp(self):
        borders = np.array([[200, 200], [150, 500], [200, 800], [600, 900], [700, 700], [900, 500], [800, 200], [500, 100], [200, 200]])
        self.pf = PolyFill(borders, 20, 20)

        
    def test_init_values(self):
        pass

    def test_fill(self):
        pass

    def test_plot(self):
        pass

    def test_is_in(self):
        pass

    def test_is_in_id(self):
        pass

    def test_locate_ij(self):
        pass

    def test_locate_xy(self):
        pass

    def test_move(self):
        pass

    def test_valid_move(self):
        pass

    def test_update(self):
        pass

    def test_in_positions(self):
        self.assertEqual(self.pf.in_positions.shape[1], 2)
        self.assertGreater(self.pf.in_positions.shape[0], 2)