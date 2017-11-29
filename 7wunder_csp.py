#!/usr/bin/env python
import constraint

"""
This package is supposed to help us build constraint solver isntances for 7 wonders. Constructing something is effectively a constraint satisfication problem, so we can generate viable actions using these criteria.

Of note: we need to implement and resources (as in they can cost for ore1 and ore2 for instance)

could clone them, so we have like. orepit1, orepit2. both cost 2 (which is true), both satisfy ore.. 

Oh yeah we can just have two 
"""
class Resource(object):
    def __init__(self, name, owner, resource_val, value=0):
        """
        name -  unique identifier for this construct (and also its name, as the game allows one instance of each card per owner)
        owner - player_id that owns this card.
        value - the gold requirement of using this option
        """
        self.name = name
        self.value = value
        self.owner = owner
        self.resource_val = resource_val

    def __int__(self):
        return self.value

    def __iadd__(self, other):
        if type(other) == int:
            self.value = self.value + other
        else:
            self.value = self.value + other.value
        
    def __radd__(self, other):
        if type(other) == int:
            return self.value + other
        else:
            return self.value + other.value

    def __add__(self, other):
        if type(other) == int:
            return self.value + other
        else:
            return self.value + other.value

    def __eq__(self, b):
        return self.name == b.name and self.owner == b.owner
    
    def __gt__(self, a):
        return self.value > a

    def __lt__(self, a):
        return self.value < a

    def __str__(self):
        return str(self.value)
       
class empty_forest(Resource):
    def __init__(self, *kwargs):
        Resource.__init__(self, *kwargs)

    def resources(self):
        return set(["wood"])

    def __str__(self):
        return "emptyforest %s" % self.value

class sawmill(Resource):
    def __init__(self, *kwargs):
        Resource.__init__(self, *kwargs)

    def resources(self):
        return set(["wood", "ore"])
    def __str__(self):
        return "sawmill %i " % self.value

class ore_mine(Resource):
    def __init__(self, *kwargs):
        Resource.__init__(self, *kwargs)
    def resources(self):
        return set(["ore"])
    def __str__(self):
        return "ore_mine %i" % self.value

class slaveyard(Resource):
    def __init__(self, *kwargs):
        Resource.__init__(self, *kwargs)
    def resources(self):
        return set(["wood","ore"])

    def __str__(self):
        return "slaveyard %i" % self.value

class woodshop(Resource):
    def __init__(self, *kwargs):
        Resource.__init__(self, *kwargs)
    def resources(self):
        return set(["wood"])
    def __str__(self):
        return "woodshop %i" % self.value



from constraint import Problem
class WunderProblem(Problem):
    def __init__(self, cur_gold=Resource("cur_gold", 0)):
        self.cur_gold = cur_gold
        Problem.__init__(self)

    def add_var_factory(self, var_string, cost=0, buildings=[], neighbors=[[],[]], has_market=True):
        from constraint import AllDifferentConstraint, Variable, MaxSumConstraint
        
        domains = []
        for b in buildings:
            #this logic needs to be reworked...

            #for _ in b.resources().count(var_string)
            #    b.append(resource_building)
            #

            if var_string in b.resources():
                #we want to add a matching domain element where domain_unique = name + owner + component
                #the domain element should have a value as well, which is the gold cost of using that building
                domains.append(b)

        for building in neighbors[0]:
            if var_string in building.resources():
                domains.append(building)

        for building in neighbors[1]:
            if var_string in building.resources():
                domains.append(building)
        
        resource_vars = []
        for i in range(cost):
            if len(domains) > 0:
                var = Variable("%s%i" % (var_string, i))
                self.addVariable(var, domains)
                resource_vars.append(var)

        self.addConstraint(AllDifferentConstraint())
        self.addConstraint(MaxSumConstraint(self.cur_gold))
        return resource_vars

def west_market(*natural_resources):
    """
    Helper function that works as our constraint (only one use for the market)
    Can also work for east market (just other neighbors resources)
    """
    num_ones = 0
    for var in natural_resources:
        if var.value == 1:
            num_ones += 1
    return num_ones < 2


def s_wunders_card_csp(costs={ "woods": ["w1", "w2", "w3"]}, buildings=[]): 
    """
    This is the bulk of our testing, we only used two resources, wood and ore, 

    we designed a test scenario including one market,

    the solution largely depends on:
        1) asigning a cost to each building assignment (0 for your own, 2 for neighbors, 1 for market effects)
        2) enforcing a uniqueness constraint to buildings (name + owner)
  

    The game API should support:
        - Cards/buildings as costs and containing "resource" functions (unique strings)
        - Cards/buildings with owners
        - Cards/buildings with unique names
        - functions or indicators for markets
    """
    buildings=[slaveyard("graveyard",0,0), empty_forest("forest", 0,0)]
    west_neighbor =[sawmill("sawmill", 1, 2), woodshop("woodshop", 1, 2), sawmill("sawmill", 1, 1), woodshop("woodshop", 1, 1)]
    east_neighbor = [ore_mine("oremine", 2, 2)]
      
    from constraint import Problem
    from constraint import AllDifferentConstraint, FunctionConstraint
    from constraint import Domain
    #to do JUST buildings:
    import sys
    problem = WunderProblem(int(sys.argv[1]))
    neighbors = [west_neighbor, east_neighbor]
    wood_vars = problem.add_var_factory("wood", 3, buildings, neighbors)
    ore_vars = problem.add_var_factory("ore", 1, buildings, neighbors)
    problem.addConstraint(FunctionConstraint(west_market), list(wood_vars + ore_vars))

    for solution in problem.getSolutions():
        print ""
        print "SOLUTION"
        for resource in solution:
            print resource, solution[resource]


    return
    #neighbor buildings:
    for cost in costs:
        domains = []
        for building in neighbors[0]:
            if cost in building.resources:
                domains.append((building, 2))

        for building in neighbors[1]:
            if cost in building.resources:
                domains.append((building, 2))
                

    for c, d in zip(costs, domains):
        addVariable(c, d)


    get_constraints()
    #each card used once
    #sum of call cards(cost) < current gold
    
    


def au_coloring():
    """
    Example problem for the australia map color problem
    """
    from constraint import Problem
    from constraint import AllDifferentConstraint 
    from constraint import Domain

    colors = Domain(set(["red", "blue", "green"])) #, 1,2,3,4,5,6,7]))
    problem = Problem()
    problem.addVariable("WA", domain=colors)
    problem.addVariable("SA", domain=colors)
    problem.addVariable("Q", domain=colors)
    problem.addVariable("NSW", domain=colors)
    problem.addVariable("V", domain=colors)
    problem.addVariable("T", domain=colors)
    problem.addVariable("NT", domain=colors)
    #Oh right, its not all different, its actually
    # each adjacent edge is added as a pair such that x != y
    source = "WA"
    for label in ["NT", "SA"]:
        problem.addConstraint(AllDifferentConstraint(), [source, label])

    source = "SA"
    for label in  [ "WA", "NT", "Q", "NSW", "V"]:
        problem.addConstraint(AllDifferentConstraint(), [source, label])

    source = "NT"
    for label in ["WA","SA","Q"]:
        problem.addConstraint(AllDifferentConstraint(), [source, label])

    source = "Q"
    for label in ["NT", "SA", "NSW"]:
        problem.addConstraint(AllDifferentConstraint(), [source, label])
    source = "NSW"
    for label in [ "Q", "SA", "V"]:
        problem.addConstraint(AllDifferentConstraint(), [source, label])
    source = "V"
    for label in [ "SA", "NSW"]: 
        problem.addConstraint(AllDifferentConstraint(), [source, label])

    problem.addConstraint(AllDifferentConstraint(), ["T"]) 

    print problem.getSolutions()

if __name__ == "__main__":
    s_wunders_card_csp()  
