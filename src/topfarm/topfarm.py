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

__all__ = ['Topfarm']
__author__ = 'Pierre-Elouan Rethore'
__email__ = "pire@dtu.dk"
__version__ = '0.1.0'
__copyright__ = "Copyright 2015, DTU Wind Energy, TOPFARM Development Team"
__license__ = "AGPL v3"
__status__ = "Alpha"




from numpy import zeros
# OpenMDAO imports
from openmdao.main.api import Assembly
from openmdao.lib.datatypes.api import VarTree, Float, Slot, Array, List, Int, Str, Dict, Enum

# FUSEDWind imports
from fusedwind.interface import implement_base, InterfaceSlot
from fusedwind.plant_flow.comp import GenericWindFarm
from fusedwind.plant_flow.vt import GenericWindFarmTurbineLayout


# Topfarm lib imports
from aep import AEP
from layout_distribution import spiral, DistributeSpiral, DistributeXY
from plot import OffshorePlot
from tlib import DistFromTurbines
#from tlib import ConverHullArea,
from foundation import FoundationLength
from elnet import ElNetLength, elnet
#from optimizers import *


from openmdao.main.api import Assembly


class Topfarm(Assembly):
    def __init__(self, components={}, workflows={}, objectives={}, constraints={}, design_variables={}, connections={}, input_parameters={}):
        """

        :param components: dict
        :param workflows: dict
        :param objectives: dict
        :param constraints: dict
        :param design_variables: dict
        :param connections: list(tuple)
        :param input_parameters: dict
        :return:
        """
        self._components = components
        self._workflows = workflows
        self._objectives = objectives
        self._constraints = constraints
        self._design_variables = design_variables
        self._connections = connections
        self._input_parameters = input_parameters

        self._output_configure = True
        self._logconf = []
        super(Topfarm, self).__init__()



    def configure(self):
        self.add_components(self._components)
        self.add_workflows(self._workflows)
        self.add_design_variables(self._design_variables)
        self.add_objectives(self._objectives)
        self.add_constraints(self._constraints)
        self.add_connections(self._connections)
        self.initialise_parameters(self._input_parameters)

        if self._output_configure:
            self.print_logconf()


    def add_components(self, components):

        self.logconf('\n# Add the components')
        for k, v in components.iteritems():
            self.add(k,v)
            self.logconf("self.add('%s', %s)"%(k, v))

    def add_workflows(self, workflows):
        self.logconf('\n# Add the workflows')
        for d, w in workflows.iteritems():
            getattr(self,d).workflow.add(w)
            self.logconf("self.%s.workflow.add(%s)"%(d, ", ".join(["'%s'"%(i) for i in w])))

    def add_design_variables(self, design_variables):
        """Get all the design variables automatically from a component that has list_design_variables
        """
        self.logconf('\n# Add the design variables')
        for d, v in design_variables.iteritems():
            for dv in getattr(self, v).list_design_variables():
                getattr(self, d).add_parameter(v + '.' + dv['name'],
                                               start=dv['start'],
                                               low=dv['low'],
                                               high=dv['high'],
                                               fd_step=dv['fd_step'])
                self.logconf("self.%s.add_parameter('%s', start=%s, low=%s, high=%s, fd_step=%s)"%(
                        d, v + '.' + dv['name'], dv['start'], dv['low'], dv['high'], dv['fd_step']))

    def add_objectives(self, objectives):
        self.logconf('\n# Add the objectives')
        for d, o in objectives.iteritems():
            getattr(self,d).add_objective(o)
            self.logconf("self.%s.add_objective('%s')"%(d, o))

    def add_constraints(self, constraints):
        self.logconf('\n# Add the constraints')
        for d, cons in constraints.iteritems():
            for c in cons:
                print c
                if '.' in c:
                    getattr(self, d).add_constraint(c)
                    self.logconf("self.%s.add_constraint('%s')"%(d, c))
                else:
                    # Automatically get the constraints from a the component method list_constraints
                    for c2 in getattr(self,c).list_constraints():
                        getattr(self, d).add_constraint(c+'.'+c2)
                        self.logconf("self.%s.add_constraint('%s')"%(d, c+'.'+c2))


    def add_connections(self, connections):
        self.logconf('\n# Connect the components together')
        for k, v in connections.iteritems():
            self.connect(k, v)
            if isinstance(v, list):
                self.logconf("self.connect('%s', %s)"%(k, v))
            else:
                self.logconf("self.connect('%s', '%s')"%(k, v))


    def initialise_parameters(self, parameters):
        self.logconf('\n# Initialize the input parameters')
        for v, p in parameters.iteritems():
            hops = v.split('.')
            # Travel through the assembly to get the right object
            obj = self
            for h in hops[:-1]:
                if not h == '.' and not h == '':
                    obj = getattr(obj, h)
            setattr(obj, hops[-1], p)
            self.logconf('self.%s = %s'%(v, str(p)))

    def logconf(self, string):
        self._logconf.append(string)

    def print_logconf(self):
        print '\n'.join(self._logconf)


class TopfarmClassic(Assembly):
    """
    dist_WT_D = Float(3.0, iotype='in', desc='The minimum admissible distance between turbines')
    depth_map = Array(iotype='in', desc='The depth map of the offshore region')
    borders = Array(iotype='in', desc='The border of the admissible wind farm')
    baseline_layout = VarTree(GenericWindFarmTurbineLayout(), iotype='in', desc='The baseline wind farm layout')
    distribution = Enum('spiral', ['spiral', 'xy'], iotype='in', desc='The type of wind turbine layout distribution to use')
    """

    def __init__(self, **kwargs):
        """
        Parameters:
            dist_WT_D = Float(3.0, iotype='in', desc='The minimum admissible distance between turbines')
            depth_map = Array(iotype='in', desc='The depth map of the offshore region ndarray([n_d, 3])', units='m')
            borders = Array(iotype='in', desc='The border of the admissible wind farm')
            baseline_layout = VarTree(GenericWindFarmTurbineLayout(), iotype='in', desc='The baseline wind farm layout')
            distribution = Enum('spiral', ['spiral', 'xy'], iotype='in', desc='The type of wind turbine layout distribution to use')
            wind_speeds = List([], iotype='in', units='m/s',
                desc='The different wind speeds to run [nWS]')
            wind_directions = List([], iotype='in', units='deg',
                desc='The different wind directions to run [nWD]')
        """
        # Initialise the inputs
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        super(Topfarm, self).__init__()


    def configure(self):
        # 1.) Adding objective components ------------------------------------------------------------------------------
        # Load the electrical net
        self.add('elnet', ElNetLength())
        # Load the foundation length calculator
        self.add('foundation', FoundationLength())
        # Load the AEP calculator
        self.add('aep', AEP())

        # 2.) Adding constraints components ----------------------------------------------------------------------------
        # Load the area constraint calculator
        #self.add('area', ConverHullArea())
        # Load the wind turbine distance calculator
        self.add('wt_dist', DistFromTurbines())
        # self.add('border_dist', DistFromBorders())

        # 3.) Design variable component --------------------------------------------------------------------------------
        if self.distribution == 'spiral':
            self.add('distribute', DistributeSpiral())
        elif self.distribution == 'xy':
            self.add('distribute', DistributeXY())

        # 4.) Visualization component [Optional] -----------------------------------------------------------------------
        self.add('plotting', OffshorePlot())

        # 5.) Optimizer ------------------------------------------------------------------------------------------------
        self.add('driver', NEWSUMTOpt())

        # 6.) Workflow definition --------------------------------------------------------------------------------------
        #self.driver.workflow.add(['distribute', 'elnet', 'foundation', 'area', 'wt_dist', 'border_dist'])
        self.driver.workflow.add(['distribute', 'foundation', 'elnet', 'aep', 'wt_dist', 'plotting'])

        # 7.) Objective function ---------------------------------------------------------------------------------------
        self.driver.add_objective('-aep.net_aep')

        #self.driver.add_objective('-foundation.foundation_length')
        #self.driver.add_objective('-wt_dist.mean_dist')
        #self.driver.add_objective('-foundation.foundation_length')
        #self.driver.add_objective('elnet.elnet_length')

        # 8.) Constraints definitions ----------------------------------------------------------------------------------
        self.driver.add_constraint('foundation.foundation_length<1.2')
        self.driver.add_constraint('elnet.elnet_length<1.2')
        self.driver.add_constraint('wt_dist.min_dist>0.8')
        #for i in range(baseline.wt_layout.wt_positions.shape[0]):
        #    for j in range(borders.shape[0]):
        #        self.driver.add_constraint('border_dist.dist[%d,%d]>0.0'%(i,j))


        # for i in range(n_wt):
        #     for j in range(n_wt):
        #         if i!=j:
        #             self.driver.add_constraint('wt_dist.dist[%d,%d]>1.0'%(i,j))

        #for i in range(n_wt):
        #    self.driver.add_constraint('wt_dist.dist[%d]>1.0'%(i))

        # 9.) Design Variable configuration ---------------------------------------------------------------------------
        n_wt = self.baseline_layout.n_wt
        if self.distribution == 'spiral':
            # With DistributeSpiral
            self.distribute.pos = zeros([n_wt])
            for i in range(n_wt):
                self.driver.add_parameter('distribute.pos[%d]' % (i), start=0.0, low=0., high=1., fd_step=0.005)
        elif self.distribution == 'xy':
            self.distribute.pos = zeros([n_wt,2])
            ### With DistributeXY
            ###self.driver.add_parameter('distribute.pos', low=-1., high=1.)
            for i in range(n_wt):
                self.driver.add_parameter('distribute.pos[%d,0]' % (i), start=0.0, low=-1., high=1., fd_step=0.005)
                self.driver.add_parameter('distribute.pos[%d,1]' % (i), start=0.0, low=-1., high=1., fd_step=0.005)

        # 10.) Connection of the components together -------------------------------------------------------------------
        #self.connect('wwh.wt_layout', 'distribute.baseline')
        self.connect('distribute.wt_positions', ['foundation.wt_positions',
                                                 'elnet.wt_positions',
                                                 'wt_dist.wt_positions',
                                                 'aep.wt_positions',
                                                 'plotting.wt_positions'])

        self.connect('foundation.foundation_length', 'plotting.foundation_length')
        self.connect('foundation.foundations', 'plotting.foundations')
        self.connect('elnet.elnet_layout', 'plotting.elnet_layout')
        self.connect('elnet.elnet_length', 'plotting.elnet_length')
        self.connect('wt_dist.dist', 'plotting.wt_dist')
        self.connect('aep.net_aep', 'plotting.net_aep')

        # 11.) Initialization ------------------------------------------------------------------------------------------
        basepos = self.baseline_layout.wt_positions
        wt = self.baseline_layout.wt_list[0]

        self.aep.wt_layout = self.baseline_layout
        self.aep.wf.wt_layout = self.baseline_layout #necessary to avoid copying wt_layout at each iteration
        self.aep.wind_speeds = self.wind_speeds
        self.aep.wind_directions = self.wind_directions

        self.distribute.baseline = basepos
        self.plotting.baseline = basepos

        self.distribute.borders = self.borders
        self.foundation.borders = self.borders
        self.plotting.borders = self.borders
        # self.border_dist.borders = self.borders

        self.foundation.depth = self.depth_map
        self.plotting.depth = self.depth_map

        # Definition of the scaling
        self.wt_dist.scaling = wt.rotor_diameter * self.dist_WT_D
        self.elnet.scaling = sum(elnet(basepos).values())
        self.aep.scaling = self.aep(wt_positions=basepos, scaling=1.0).net_aep
        self.foundation.scaling = self.foundation(wt_positions=basepos, scaling=1.0).foundation_length



