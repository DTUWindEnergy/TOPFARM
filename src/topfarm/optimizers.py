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

#from dakota_driver import DakotaOptimizer, DakotaMultidimStudy, \
#                  DakotaVectorStudy

from openmdao.lib.drivers.api import COBYLAdriver, CONMINdriver, NEWSUMTdriver, SLSQPdriver, Genetic
from pyopt_driver.pyopt_driver import pyOptDriver
from openmdao.util.testutil import assert_rel_error, assert_raises
import os.path as path



# DAKOTA Optimizers ----------------------------------------------------------------------------------------------------
grad_opt = ['conmin_frcg', 'conmin_mfd',
              'optpp_cg', 'optpp_newton', 'optpp_q_newton', 'optpp_fd_newton']
pattern_opt = ['asynch_pattern_search', 'coliny_pattern_search']
simplex = ['optpp_pds', 'coliny_cobyla']
greedy = ['coliny_solis_wets']
ea = ['coliny_ea', 'soga', 'moga']
direct = ['ncsu_direct', 'coliny_direct']
other = ['surrogate_based_local', 'surrogate_based_global', 'hybrid_strategy', 'multi_start_strategy']
dak_all = grad_opt + pattern_opt + pattern_opt + simplex + greedy + ea + direct

#os.environ['DYLD_LIBRARY_PATH'] = '/Users/pire/dakota_src/lib:/Users/pire/dakota_src/bin:/opt/local/lib/:' + os.environ['DYLD_LIBRARY_PATH']

#class DakotaOpt(DakotaOptimizer):
#    def __init__(self, method='conmin_frcg'):
#        self.method = method
#        super(DakotaOpt, self).__init__()
#        self.stdout = 'dakota.out'
#        self.stderr = 'dakota.err'
#        self.tabular_graphics_data = True
#        self.max_iterations = 10000
#        self.convergence_tolerance = 1e-4
#        self.interval_type = 'forward'
#        self.fd_gradient_step_size = 1e-5


# OpenMDAO optimizers --------------------------------------------------------------------------------------------------
class CONMINOpt(CONMINdriver):
    def __init__(self, **kwargs):
        super(CONMINOpt, self).__init__()
        # CONMIN-specific Settings
        self.itmax = 30
        self.fdch = 0.00001
        self.fdchm = 0.000001
        self.ctlmin = 0.01
        self.delfun = 0.001

        # Initialise the inputs
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

class NEWSUMTOpt(NEWSUMTdriver):
    def __init__(self, **kwargs):
        super(NEWSUMTOpt, self).__init__()
        # NEWSUMT-specific Settings
        self.itmax = 1000

        # Initialise the inputs
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

class COBYLAOpt(COBYLAdriver):
    def __init__(self, **kwargs):
        super(COBYLAOpt, self).__init__()
        # COBYLA-specific Settings
        self.rhobeg = 1.0
        self.rhoend = 1.0e-4
        self.maxfun = 10000

        # Initialise the inputs
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

class SLSQPOpt(SLSQPdriver):
    def __init__(self, **kwargs):
        super(SLSQPOpt, self).__init__()
        # SLSQP-specific Settings
        self.accuracy = 1.0e-6
        self.maxiter = 1000

        # Initialise the inputs
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

class GeneticOpt(Genetic):
    def __init__(self, **kwargs):
        super(GeneticOpt, self).__init__()
        # Genetic-specific Settings
        self.population_size = 90
        self.crossover_rate = 0.9
        self.mutation_rate = 0.02

        # Initialise the inputs
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        # self.parent.selection_method = 'rank'

        # self.add('driver', CONMINdriver())
        # self.driver.itmax = 3000
        # self.driver.fdch = 0.001
        # self.driver.fdchm = 0.001
        # self.driver.ctlmin = 0.0001
        # self.driver.tetha = 0.1
        # self.driver.phi = 1.0
        # self.driver.delfun = 0.01

        # self.add('driver', SLSQPdriver())
        # self.driver.accuracy = 1.0e-6
        # self.driver.maxiter = 1000

        # self.add('driver', GTOWrapper())
        # self.driver.alg_type = 2
        # self.driver.hawtoptbin = 'HAWTOPT'
        # self.driver.alg_maxit=500
        # self.driver.SLP_ml=5.
        # self.driver.SLP_mlmin=0.1
        # self.driver.fd_step_default = 0.05
        # self.SGA_population = 50


        # self.add('driver', CONMINdriver())
        # self.driver.itmax = 3000
        # self.driver.fdch = 0.01
        # self.driver.fdchm = 0.01
        # self.driver.ctlmin = 0.001
        # self.driver.tetha = 0.1
        # self.driver.phi = 1.0
        # self.driver.delfun = 0.01

        # self.add('driver', NEWSUMTdriver())
        # self.driver.itmax = 1000
        # self.driver.stepmx = 0.001



# TODO: update the list of OpenMDAO optimizers

# PyOPT ----------------------------------------------------------------------------------------------------------------
#pyopt_methods = ['ALHSO', 'ALPSO', 'COBYLA', 'CONMIN',   'KSOPT', 'NSGA2', 'SLSQP']
pyopt_methods = ['ALHSO', 'ALPSO', 'COBYLA', 'CONMIN', 'KSOPT', 'MIDACO', 'NSGA2', 'PSQP', 'SLSQP', 'SOLVOPT']
# Not working..
#'FSQP','GCMMA', 'MIDACO', 'MMA', 'MMFD', 'NLPQL', 'PSQP', 'SNOPT',  'SOLVOPT'



# pyopt_options = {'NSGA2': {
#             'PopSize':100, #Population Size (a Multiple of 4)
#             'maxGen': 150, # Maximum, Number of Generations
#             'pCross_real': 0.6, #Probability of Crossover of Real Variable (0.6-1.0)
#             'pMut_real': 0.2, #Probablity of Mutation of Real Variables (1/nreal)
#             'eta_c': 10.0,    #Distribution Index for Crossover (5-20) must be > 0
#             'eta_m': 20.0,    #Distribution Index for Mutation (5-50) must be > 0
#             'pCross_bin': 0.0, #Probability of Crossover of Binary Variable (0.6-1.0)
#             'pMut_real': 0.0, #Probability of Mutation of Binary Variables (1/nbits)
#             'PrintOut': 1, #Flag to Turn On Output to files (0-None, 1-Subset, 2-All)
#             'seed': 0.0,
#             },
#         'ALHSO': {
#             'hms': 5, #5, #   Memory, Size [1,50]
#             'hmcr':   0.95, #    Probability rate of choosing from memory [0.7,0.99]
#             'par':   0.65, #   Pitch adjustment rate [0.1,0.99]
#             'dbw': 2000, #    Variable, Bandwidth Quantization
#             'maxoutiter': 2e3, # Maximum, Number of Outer Loop Iterations (Major Iterations)
#             'maxinniter': 2e2,#2e2, # Maximum, Number of Inner Loop Iterations (Minor Iterations)
#             'stopcriteria': 1, #   Stopping, Criteria Flag
#             'stopiters': 10, #  Consecutively, Number of Outer Iterations for convergence
#             'etol':   1e-6, #   Absolute Tolerance for Equality constraints
#             'itol':   1e-6, #   Absolute Tolerance for Inequality constraints
#             'atol':   1e-6, #   Absolute Tolerance for Objective Function
#             'rtol':   1e-6, #   Relative Tolerance for Objective Function
#             'prtoutiter': 0, #   Number, of Iterations Before Print Outer Loop Information
#             'prtinniter': 0, #   Number, of Iterations Before Print Inner Loop Information
#             'xinit': 0, #   Initial, Position Flag (0 - no position, 1 - position given)
#             'rinit':   1.0, #.0, Initial Penalty Factor
#             'fileout': 1, #   Flag, to Turn On Output to filename
#             'filename': 'ALHSO.out', #Output File Name
#             'seed':   0, #   Random, Number Seed (0 - Auto-Seed based on time clock)
#             'scaling': 1, #   Design, Variables Scaling (0- no scaling, 1- scaling [-1,1])
#         },
#         'ALPSO': {
#             'SwarmSize': 40, #  Number,# of Particles (Depends on Problem dimensions)
#             'maxOuterIter': 200, # Maximum,# Number of Outer Loop Iterations (Major Iterations)
#             'maxInnerIter': 6, #   Maximum,# Number of Inner Loop Iterations (Minor Iterations)
#             'minInnerIter': 6, #   Minimum,# Number of Inner Loop Iterations (Minor Iterations)
#             'dynInnerIter': 0, #   Dynamic,# Number of Inner Iterations Flag
#             'stopCriteria': 1, #   Stopping,# Criteria Flag (0 - maxIters, 1 - convergence)
#             'stopIters': 5, #   Consecutively,# Number of Iterations for Convergence
#             'etol':   1e-3,#    Absolute Tolerance for Equality constraints
#             'itol':   1e-3,#    Absolute Tolerance for Inequality constraints
#             'rtol':   1e-2,#    Relative Tolerance for Lagrange Multipliers
#             'atol':   1e-2,#    Absolute Tolerance for Lagrange Function
#             'dtol':   1e-1,#    Relative Tolerance in Particles Distance to Terminate (GCPSO)
#             'printOuterIters': 0, #   Number,# of Iterations Before Print Outer Loop Information
#             'printInnerIters': 0, #   Number,# of Iterations Before Print Inner Loop Information
#             'rinit':   1.0, #.0,# Initial Penalty Factor
#             'xinit': 0, #   Initial,# Position Flag (0 - no position, 1 - position given)
#             'vinit':   1.0,# Initial Velocity of Particles Normalized in [-1,1] Space
#             'vmax':   2.0,# Maximum Velocity of Particles Normalized in [-1,1] Space
#             'c1':   2.0,# Cognitive Parameter
#             'c2':   1.0,# Social Parameter
#             'w1':   0.99,#    Initial Inertia Weight
#             'w2':   0.55,#    Final Inertia Weight
#             'ns': 15, #  Consecutive,# Successes Before Radius will be Increased (GCPSO)
#             'nf': 5, #   Consecutive,# Failures Before Radius will be Increased (GCPSO)
#             'dt':   1, #   Time,# step
#             'vcrazy':   1e-4,#    Craziness Velocity
#             'fileout': 1, #   Flag,# to Turn On Output to filename
#             'filename': 'ALPSO.out',# Output File Name
#             'seed':   0, #   Random,# Number Seed (0 - Auto-Seed based on time clock)
#             'HoodSize': 40, #  Number,# of Neighbours of Each Particle
#             'HoodModel': 'gbest', # Neighbourhood,# Model (dl/slring, wheel, Spatial, sfrac
#             'HoodSelf': 1, #   Selfless,# Neighbourhood Model
#             'Scaling': 1, #   Design,# Variables Scaling (0- no scaling, 1- scaling [-1,1])
#         },

#         # 'COBYLA':{
#         #     'RHOBEG': 0.5, # Initial Variables Change
#         #     'RHOEND': 1.0e-6, #  Convergence Accurancy
#         #     'IPRINT': 2, #   Print Flag (0-None, 1-Final, 2,3-Iteration)
#         #     'MAXFUN': 3500, #    Maximum Number of Iterations
#         #     'IOUT': 6, #   Output Unit Number
#         #     'IFILE': 'COBYLA.out', #Output File Name
#         #     }
#       }

class PyoptOpt(pyOptDriver):
    def __init__(self, method='ALPSO', **kwargs):
        super(PyoptOpt, self).__init__()
        self.optimizer = method
        self.differentiator = None
        self.print_results = False
        for k,v in kwargs.iteritems():
            self.options[k] = v
        #if self.optimizer in pyopt_options:
        #    self.options = pyopt_options[self.optimizer]



from ipoptdriver.ipoptdriver import IPOPTdriver

class IpOpt(IPOPTdriver):
    def __init__(self, **kwargs):
        super(IpOpt, self).__init__()
        for k,v in kwargs.iteritems():
            self.options[k] = v



# DTU GTO --------------------------------------------------------------------------------------------------------------
#from gto_wrapper.gto_wrapper import GTOWrapper

#class GTOpt(GTOWrapper):
#    def __init__(self, method=2):
#        self.alg_type = method
#        super(GTOpt, self).__init__()
#        self.hawtoptbin = 'HAWTOPT'
#        self.alg_maxit=50
#        self.SLP_ml=4.
#        #self.fd_step_default=0.001


# Generate all the available optimizers --------------------------------------------------------------------------------
def opti_generator():
    """ Generator of optimizers """
    #for i in dak_all:
    #    yield DakotaOpt(i)

    for i in [CONMINOpt, NEWSUMTOpt, COBYLAOpt, SLSQPOpt, GeneticOpt]:
        yield i()

    # for i in pyopt_methods:
    #     yield PyoptOpt(i)

#    for i in range(1,4):
#        yield GTOpt(i)

### Create a list of optimizers for benchmarking
optilist = list(opti_generator())
#print len(optilist)