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


from numpy import argmin, array, sqrt
from openmdao.main.component import Component
from openmdao.main.datatypes.array import Array
from openmdao.main.datatypes.dict import Dict
from openmdao.main.datatypes.float import Float



class ElNetLayout(Component):
    wt_positions = Array([], unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')
    ##wt_layout = VarTree(GenericWindFarmTurbineLayout(), iotype='in', desc='wind turbine properties and layout')
    #elnet_layout = VarTree(GenericWindTurbineCableLayout(), iotype='out')

    elnet_layout = Dict(iotype='out', desc='The keys are tuples of connected wind turbine indices, the values are the cable length')

    def execute(self):
        self.elnet_layout = elnet(self.wt_positions)

class ElNetLength(Component):
    wt_positions = Array([], unit='m', iotype='in', desc='Array of wind turbines attached to particular positions')
    #wt_layout = VarTree(GenericWindFarmTurbineLayout(), iotype='in', desc='wind turbine properties and layout')
    elnet_layout = Dict(iotype='out') #VarTree(GenericWindTurbineCableLayout(), iotype='out')
    elnet_length = Float(iotype='out', desc='The total inner cable length', unit='m')
    scaling = Float(1.0, iotype='in', desc='')

    def execute(self):
        elnet_layout = elnet(self.wt_positions)
        self.elnet_length = sum(elnet_layout.values()) / self.scaling
        self.elnet_layout = elnet_layout


def elnet(positions):
    """
    Calculate the minimum distance grid connection for a given wind farm

    Parameters
    ----------
     positions:  ndarray([n_wt,2]): X,Y positions of the wind turbines

    Returns
    -------
     connections: dict of keys (i_wt, j_wt) and value the distance between the two wind turbine index

    the total cable length is simply sum(connections.values())
    """
    n_wt = positions.shape[0]
    X, Y = positions[:,0], positions[:,1]
    dist = lambda i, j: sqrt((X[i] - X[j])**2.0 + (Y[i] - Y[j])**2.0)

    turblist = range(n_wt)
    connections = {}
    islands = []
    ### Look for the smallest connections, and cluster them together.
    for i_wt in turblist:
        not_i_wt = filter(lambda x: x != i_wt, turblist)
        distances = sqrt((X[not_i_wt] - X[i_wt])**2.0 + (Y[not_i_wt] - Y[i_wt])**2.0)
        id = argmin(distances)
        closest_wt = not_i_wt[id]

        ### Add the connection to the structure
        connections[(i_wt,closest_wt)] = distances[id]
        #
        #   connections{closest_wt}(end+1) = i_wt

        ### Add the turbine to an island
        found = False
        for iIS, island in enumerate(islands):
            ### Check if it's nearest turbine is already in an island
            if closest_wt in island or i_wt in island:
                if found:
                    ### Those two islands are connected (iIs & id_island)
                    ### let's merge them
                    island += filter(lambda x: x != i_wt and x != closest_wt, islands[id_island])
                    del islands[id_island]

                found = True
                id_island = iIS
                if  i_wt not in island:
                    ### Add it to the island
                    island.append(i_wt)

                if  closest_wt not in island:
                    ### Add it to the island
                    island.append(closest_wt)

        if not found:
            ### Creat a new island
            islands.append([i_wt,closest_wt])


    ### Connect the islands

    while len(islands)>1:
        ### Look for the closest turbine that is not in the island
        dist_list = array([[dist(i_wt, j_wt), i_wt, j_wt] for i_wt in islands[0]
                                                              for j_wt in turblist
                                                                  if j_wt not in islands[0]])
        amin = argmin(dist_list[:,0])
        i_wt = int(dist_list[amin, 1])
        j_wt = int(dist_list[amin, 2])

        ### Add the connection to the structure
        if (i_wt, j_wt) not in connections and (j_wt, i_wt) not in connections:
            connections[(i_wt,j_wt)] = dist_list[amin,0]
        #if i_wt not in connections[j_wt]:
        #    connections[j_wt].append(i_wt)

        for i, island in enumerate(islands):
            if j_wt in island:
                islands[0] += island
                del islands[i]

    return connections
