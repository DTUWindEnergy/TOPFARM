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

from unittest import TestCase
from topfarm.elnet import ElNetLength, ElNetLayout


class TestElNetLayout(TestCase):
    def setUp(self):
        self.enl = ElNetLayout()

    # TODO: check that elnet() is called successfully


class TestElNetLength(TestCase):
    def setUp(self):
        self.enl = ElNetLength()

    # TODO: check that the total length is calculated correctly

class TestElnet(TestCase):
    def test_elnet(self):
        # TODO: check that some basic layout look rational
        pass