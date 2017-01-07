"""
Right now this is a naive simulation for the problem we could run into.
"""
from copy import copy, deepcopy
from graphviz import *
from Player import Player
import numpy as np


class node():
    def __init__(self, shopping_list, player,  west, east, meta={}, payments_west=0, payments_east=0, smart_prune=True):
        self.shopping_list = shopping_list
        self.edges = []
        self.west = west
        self.east = east
        self.meta = meta
        self.player = player
        self.payments_west = payments_west
        self.payments_east = payments_east
        WEST_IDX = 0
        EAST_IDX = 1
        self.shopping_list.clip(min=0)

        self.names = ["gold/currency", "brick" ,"stone" ,"ore", "wood", "glass","paper", "silk"]

        if sum(self.shopping_list) == 0: #is terminal sounds to general
            return
        else:
            #cloning should be done before or after. not both. clone everything.
            # need to handle marketplace cards from neighbors (cannot buy from them!)
            
            search_objs = [deepcopy(player), deepcopy(west), deepcopy(east)]
            #################
            # HANDLES XOR RESOURCES for US AND NEIGHBORS
            #################
            for k, p in enumerate(search_objs):
                #k is the player
                for i, options in enumerate(p.xor_resources): 
                    for j, option in enumerate(options):
                        if option == 0: continue
                        if self.shopping_list[j] == 0: continue
                        if k > 0 and player.resources[0] <= 0: continue # cannot afford other players resources
                        p_clone = deepcopy(p)
                        p_clone.xor_resources.pop(i)
                        shopping_list_clone = deepcopy(shopping_list)

                        shopping_list_clone[j] -= 1
                        search_copy = deepcopy(search_objs) 
                        search_copy[k] = p_clone

                        #check if next node is probably legal
                        #skip = probably_terminal(p_clone, search_objects[0], search_objects[1])
                        #code for probably terminal?

                        if smart_prune: #so we are pruning edjes that have no terminal node
                            #we can predcit this
                            if sum(shopping_list_clone) > 0:
                                total = np.asarray(deepcopy(shopping_list_clone))
                                for s in search_objs: #these are adjacent players
                                    if len(s.xor_resources) == 0:
                                        total -= s.resources
                                    else:
                                        total -= s.resources + np.sum(s.xor_resources, dtype='int32',axis=0)
                                if max(total) > 0: 
                                    #prune because not possible to acquire resources
                                    continue 



                        new_node = node(shopping_list_clone, *search_copy,      \
                                        meta={"label": "person: " + ["player","west","east"][k]\
                                              +" optional " + str_options(options)}, \
                                              smart_prune = smart_prune, \
                                              payments_west = self.payments_west, \
                                              payments_east = self.payments_east)
                        self.edges.append(new_node)
                if len(self.edges) > 0: return #first only consider our options

            ######################
            # HANDLE NEIGHBOR PURCHASING
            ######################
            neighbors = (deepcopy(west), deepcopy(east)) #make player objects copy be deepcopy by default.
            for k, neighbor in enumerate(neighbors):
                if player.resources[0] <= 0: break #player cannot buy.
                for i, resource in enumerate( neighbor.resources ):
                    if i == 0: continue #cannot trade for gold (trading takes gold...)
                    if resource == 0: continue #player doesnt have that resource
                    if self.shopping_list[i] == 0: continue #do not need that resource
                    shopping_list_clone = deepcopy(shopping_list)
                    neighbor_clone = deepcopy(neighbors) 
                    shopping_list_clone[i] -= 1
                    neighbor_clone[k].resources[i] -= 1 

                    if smart_prune:
                        """ 
                        Basically, ask if the next node is legal, if it is, compute its subgraph
                        """
    
                        if sum(shopping_list_clone) > 0:
                            total = np.asarray(deepcopy(shopping_list_clone))
                            for s in (player, neighbor_clone[0], neighbor_clone[1]):
                                if len(s.xor_resources) == 0:
                                    total -= s.resources
                                else:
                                    total -= s.resources + np.sum(s.xor_resources, dtype='int32',axis=0)
                            if max(total) > 0: continue
                    
                    new_node = node(shopping_list_clone, player, *neighbor_clone,\
                                 meta={"label":"Purchase " + ["west","east"][k] \
                                 + " resource: " + self.names[i]}, smart_prune=smart_prune,\
                                 payments_west = self.payments_west + (k == WEST_IDX),\
                                 payments_east = self.payments_east + (k == EAST_IDX) ) 
                    self.edges.append( new_node ) 
   

    def is_terminal(self):
        return sum(self.shopping_list) == 0

  
    def get_nodes(self, call_num=0):
        if len(self.edges) == 0:
            return [self]

        to_ret = [self]
        for e in self.edges:
            to_ret += get_nodes(e, call_num+1)
        return to_ret
  
    def get_terminal_nodes(self):
        return [ n for n in self.get_nodes() if n.is_terminal() ]


    def __str__(self):
        #b s o w
        names = ["brick" ,"stone" ,"ore", "wood", "glass","paper", "silk"]
        _str = ""
        if self.is_terminal(): return _str + "None"
        #_str = "need: "
        for name, resource in zip(names, self.shopping_list):
            if resource > 0:
                _str += str(resource) + " " +  name + " " 
        #un comment for detailed state
        #_str += ",".join(map(str, self.west.resources)) + " " + ",".join(map(str,self.east.resources))
        #one thing that's interesting, by not including the ID we get collapsed
        # nodes but not edges.
        return _str.strip() + " " + str(id(self))

def generate_build_actions(graph):
    """
    Generates the appropriate build actions from the passed graph (node object)

    returns tuple of unique payments which re legal that we can make
    """
    pay_poss = set()
    for t in graph.get_terminal_nodes():
        pay_poss.add(str(t.payments_west) + "-" + str(t.payments_east))

    final = []
    for poss in pay_poss:
      final.append(map(int, poss.split("-")))
    return final

  

def str_options(options):
    names = ["brick" ,"stone" ,"ore", "wood", "glass","paper", "silk"]
    _str = ""
    for name,resource in zip(names, options):
        if resource > 0:
            _str += name  + "/"
    return _str[:-1]
            
        

def resource_helper(indicies):
    resource = [0] * 7
    for idx in indicies:
        resource[idx] += 1
    return resource

def test_generator(filename="Cards.csv"):
    for line in open(filename, 'r'):
        if "#" in line[0]: continue
        if line.strip() == "": continue     
        name,cardtype,age,c_gold,c_brick,c_stone,c_ore,c_wood,c_glass,c_paper,c_silk,c_text,\
             upgrades,players,meta = line.strip().split(",")
        if int(age) != 3: continue
        costs = map(int, [c_gold, c_brick, c_stone, c_ore, c_wood, c_glass, c_paper, c_silk])
        yield (name, costs)

def get_nodes(node, call_num=0):
    if len(node.edges) == 0:
        return [node]

    to_ret = [node]
    for e in node.edges:
        to_ret += get_nodes(e, call_num+1)

    return to_ret

def get_edges(node):
    if len(node.edges) == 0:
        return []    

    pairs = []
    for edge in node.edges:
        pairs.append(((node, edge), edge.meta))
        pairs += get_edges(edge)

    return pairs
    
def add_nodes(graph, nodes): #graph object, then this list, tuple dictionary thing.
    """
    n in nodes should be a tuple or a string. If it is a typle, 
    """
    for n in nodes:
        graph.node(str(n))
    return graph

def add_edges(graph, edges):
    (('A', 'B'), {'label': 'Edge 1'}),
    for e in edges:
        if isinstance(e[0], tuple):
            #if we want to add a label, we need ((A, B), {}) label
            graph.edge(str(e[0][0]), str(e[0][1]), **e[1])
        else:
            graph.edge(str(e[0]), str(e[1]))
    return graph

def example_graph():
    add_edges(
    add_nodes(Digraph(), ['A', 'B', 'C']),\
                         [('A', 'B'), ('A', 'C'), ('B', 'C')]\
             ).render('img/g4')

def test_xor_me():

    #scales exponentially by the number of non-zeroes in our need
    # i think its sublinear slowdown when you increase one dimension
    # if you add a nonzero you get exponential slowdown (2^n)

    # anyway now we should see how this works with the game itself
    need = [3,2,3,4,1,1,1] 
    need = np.asarray([0,0,2,0,0,0,0,1])
    p1resources = np.asarray([21,1,0,1,1,1,1])
    p1xor_resources = [ [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0] ]
    west_resources = np.asarray([1,1,0,1,1,1,1,1] )
    east_resources = np.asarray([1,1,2,1,1,1,1,0]) 

    """
    need = [0,0,0,0,0,0,4] 
    p1xor_resources = [ [0,0,0,0,1,0,1] ]
    west_resources = [0,0,0,0,0,0,4] 
    east_resources = [0,0,0,0,0,0,0] 
    """

    cur_player, west, east = Player(xor_resources = p1xor_resources), \
                         Player(resources=west_resources ),       \
                         Player(resources=east_resources)
    import time

    for _ in range(1):
        start = time.time()
        graph = node(shopping_list=need, player=cur_player, west=west, east=east, smart_prune=True)
        print time.time() - start

    print graph.get_terminal_nodes() 
    print generate_build_actions(graph)

    nodes = get_nodes(graph)
    edges = get_edges(graph)

    for _ in range(1):
        start = time.time()
        graph = node(shopping_list=need, player=cur_player, west=west, east=east, smart_prune=False)
        print time.time() - start

    #draws the graph
    
    add_edges(add_nodes(Digraph(format='png'), nodes), edges).render('img/test')

    for shopping_list in test_generator():
        #wait this is too fancy
        pass 

def tests():
    test_xor_me()

if __name__ == "__main__":
    tests()

                        
        
    


