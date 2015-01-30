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
from fusedwind.plant_flow.vt import GenericWindFarmTurbineLayout, WTPC

__author__ = 'Pierre-Elouan Rethore'
__email__ = "pire@dtu.dk"
__version__ = '0.01a'
__copyright__ = "Copyright 2015, DTU Wind Energy, TOPFARM Development Team"
__license__ = "AGPL v3"
__status__ = "Alpha"

import unittest
from numpy import loadtxt, linspace, meshgrid, array
from gclarsen.fusedwasp import PlantFromWWH, WTDescFromWTG
from topfarm.topfarm import Topfarm


class TopfarmTestCase(unittest.TestCase):

    def setUp(self):

        case = 0


        self.case_dicts = [{'Dir' : 'VesterhavnSyd',
                       'wwh_file' : 'VesterhavnSyd_3MW_delivery1.wwh',
                       'wake_decay':0.075},
                      {'Dir' : 'VesterhavnSyd',
                       'wwh_file' : 'VesterhavnSyd_10MW_delivery1.wwh',
                       'wake_decay':0.1165},
                      {'Dir' : 'VesterhavnNord',
                       'wwh_file' : 'VesterhavnNord_3MW_delivery1.wwh',
                       'wake_decay':0.075},
                      {'Dir' : 'VesterhavnNord',
                       'wwh_file' : 'VesterhavnNord_10MW_delivery1.wwh',
                       'wake_decay':0.05}]



        
    def tearDown(self):
        pass

    def test_all_cases(self):
        #for i in range(4):
        #    self._run_case(i)
        pass

    def _run_case(self, case):
        print self.case_dicts[case]['wwh_file']

        Dir = '/Users/pire/Projects/201312_EnergiNet/' + self.case_dicts[case]['Dir']
        wwh_file = Dir+'/'+ self.case_dicts[case]['wwh_file']
        depth = loadtxt(Dir+'/depth.xyz')
        borders = loadtxt(Dir+'/borders.xyz', usecols=(0,1))

        t = Topfarm(
            baseline_layout = PlantFromWWH(filename=wwh_file).wt_layout,
            borders = borders,
            depth_map = depth,
            dist_WT_D = 5.0,
            distribution='spiral',
            wind_speeds=[4., 8., 20.],
            wind_directions=linspace(0., 360., 36)[:-1]
        )
        t.run()

        
    # add some tests here...
    
    #def test_Topfarm(self):
        #pass

# Functional tests

# Load a turbine from WAsP library file WTG

# Test outputing a new WAsP workspace from a TOPFARM assembly
class TestSaveWWH(unittest.TestCase):
    def test_writing_WWH(self):
        self.fail('make save WWH function')


# Test writing a standard TOPFARM input file (JSON format)

class TestWriting(unittest.TestCase):
    def test_writing_outputs(self):
        self.fail('make save function')


# Test reading a standard TOPFARM input file (JSON)

class TestReading(unittest.TestCase):
    def test_reading_inputs(self):
        self.fail('make read function')

# Test the 2x3 test case
class Test2x3(unittest.TestCase):
    def test_2x3(self):
        # Loading the water depth map
        dat = loadtxt('data/WaterDepth1.dat')
        X, Y = meshgrid(linspace(0., 1000., 50), linspace(0., 1000., 50))
        depth = array(zip(X.flatten(), Y.flatten(), dat.flatten()))
        borders = array([[200, 200], [150, 500], [200, 800], [600, 900], [700, 700], [900, 500], [800, 200], [500, 100], [200, 200]])
        baseline = array([[587.5, 223.07692308], [525., 346.15384615], [837.5, 530.76923077], [525., 530.76923077], [525., 838.46153846], [837.5, 469.23076923]])

        wt_desc = WTDescFromWTG('data/V80-2MW-offshore.wtg').wt_desc
        wt_layout = GenericWindFarmTurbineLayout([WTPC(wt_desc=wt_desc, position=pos) for pos in baseline])

        t = Topfarm(
            baseline_layout = wt_layout,
            borders = borders,
            depth_map = depth,
            dist_WT_D = 5.0,
            distribution='spiral',
            wind_speeds=[4., 8., 20.],
            wind_directions=linspace(0., 360., 36)[:-1]
        )

        t.run()

        self.fail('make save function')
        t.save()
        
if __name__ == "__main__":
    unittest.main()
    