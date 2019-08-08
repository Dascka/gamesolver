from tools import operations as ops
from graph import Graph
from solvers.reachability import attractor as attr
import copy
import numpy as np

def construct_g_i_k(g, i, k, j):
    #stocking it to avoid computing it multiples times
    exp = 2**i
    #creating the new game graph
    g_new = Graph()
    #adding the states so they can have the proper color. We add every state from g. 
    #the color of the states is blue if the state belong to j and has an out degree > exp. The color is red if the state belong to j and has an out degree > exp.
    #The color is white ohterwise.
    #colors : O = blue, 1 = red, 2 = white.
    for s in g.get_nodes():
        color = -1
        if g.get_node_player(s) == j:
            if len(g.get_successors(s)) > exp:
                color = 0
            else:
                color = 2
        else:
            if len(g.get_successors(s)) > exp:
                color = 1
            else:
                color = 2
        g_new.add_node(s, (g.get_node_player(s), color))
    
    for s1 in g.get_nodes():
        succ = g.get_successors(s1)
        for s2 in succ:
            if len(succ) <= exp or in_first_edge(g, s1, s2, i):
                g_new.add_successor(s1, s2)
                g_new.add_predecessor(s2, s1)
    return g_new
            

def in_first_edge(g, s1, s2, i):
    """
    Return if the edge (s1, s2) is in first the 2**i inedges from the edges of g. We suppose that the edges are sorted properly according to the sort explained in theory.
    :param g: the game on which we look for the inedges of s2.
    :param s1: the first state of the edge.
    :param s2 : the second state of the edge.
    :param i: the step i of the algorithme used to compute 2**i.
    :return: true if the edge (s1, s2) is in first the 2**i inedges from the edges of g, else if not.
    """
    inedges = g.get_predecessors(s2)
    exp = 2**i
    for i in range(len(inedges)):
        if i > exp:
            return False
        if inedges[i] == s1:
            return True
    return False

def opt_buchi(g, t, j):
    """
    Solve a Buchi objective on the game g for the target set t. This version of the algorithm works in O(n^2) where n is the number of states in g. 
    This algorithm returns the winning state for player j only. If we want to we can get the winning states for player jbar by taking S \ Wj.
    :param g: the game to solve.
    :param t: the target set.
    :return: the winning regions of player j for the objective Buchi(g, t).
    """
    #first loop index, we are iterating on k and i. Not directly but those two number change and so are the rest of the data
    k = 0
    #y is the attractor in g for player j towards the set t 
    y = attr(g, t, j)[0]
    #doing X = S \ Y
    x = [s for s in g.get_nodes() if s not in y]
    #set of states that we removed from the current game g_k
    d = attr(g, x, ops.opponent(j))[0]
    #set of states of the current game g_k
    s_k = [s for s in g.get_nodes() if s not in d]
    #the current game g_k
    g_k = g.subgame(s_k)
    #target set in iteration k to correspond with the remaining state of g_k
    t_k = copy.deepcopy(t)
    #updating the iteration we are on
    k = k + 1
    #set of all the states we removed from g from that start
    U = d
    #second loop index
    i = 1
    #repeat until equivalent. We repeat the loot until we have i = log_2(n)
    while True:
        #construct a special graph with and ordering on inedges and color on states
        g_i_k = construct_g_i_k(g_k, i, k, j)
        #compute z_i_k to be a set containing states from g_i_k such that they are (i) red (color 1) without outedges in g_i_k or (ii) blue (color 0) in g_i_k
        z = []
        for s in g_i_k.get_nodes():
            s_color = g_i_k.get_node_priority(s)
            if (s_color == 1 and len(g_i_k.get_successors(s)) == 0) or s_color == 0:
                z.append(s)
        #actualing the target set to correspond with the current set of state
        t_k = [s for s in t_k if s in s_k]
        #computing y with our new value
        y = attr(g_i_k, t_k + z, j)[0]
        #actualising x_k to correspond with the new y
        x = [s for s in g_i_k.get_nodes() if s not in y]
        #incrementing i
        i = i + 1
        #if x is not empty we compute a new d and remove it from the g_k
        if len(x) != 0:
            d = attr(g_k, x, ops.opponent(j))[0]
            s_k = [s for s in g_k.get_nodes() if s not in d]
            g_k = g_k.subgame(s_k)
            k = k + 1
            U = U + d
        #we stop when i = log_2(n)
        if len(g.get_nodes()) == 0 or i >= np.log2(len(g.get_nodes())):
            break
    #we will return all states but those who were removed ie we return the set of states S \ U
    Wj = [s for s in g.get_nodes() if s not in U]
    return Wj

def basic_buchi(g, t, j):
    """
    Solve a Buchi objective on the game g for the target set t. This version of the algorithm works in O(n*m) where n is the number of states and m the number of edges in g. 
    This algorithm returns the winning state for player j only. If we want to we can get the winning states for player jbar by taking S \ Wj.
    The algorithm works by removing states from the graph, those states are computed such that they are not winning for player j and the algorithm continue with a subgraph
    until there is no more state to remove.
    :param g: the game to solve.
    :param t: the target set such that t in included in g's states.
    :return: the winning regions of player j for the objective Buchi(g, t).
    """
    #the game on which we will work while iterating.
    g_current = copy.deepcopy(g)
    #the states of the game on current iteration
    s_current = g_current.get_nodes()
    #
    w_current = []
    U = []
    #repeat until equivalent. We repeat the loot until we have i = log_2(n)
    while True:
        #current target set that only contains states of s_k
        t_current = [s for s in t if s in s_current]
        w_current = avoid_set_classical(g_current, t_current, j)
        #s_current = s_current \ w_current, we remove the states from w_current
        s_current = [s for s in s_current if s not in w_current]
        g_current = g_current.subgame(s_current)
        U = U + w_current
        #we stop the loop when w_current is empty
        if len(w_current) == 0:
            break
    Wj = [s for s in g.get_nodes() if s not in U]
    return Wj

def avoid_set_classical(g, t, j):
    """
    Compute a set of states that are winning for player j for the buchi objective.
    :param g: the game to solve.
    :param t: the target set such that t in included in g's states.
    :return: a set of states that are winning for player j for the buchi objective.
    """
    jbar = ops.opponent(j)
    a = attr(g, t, j)[0]
    abar = [s for s in g.get_nodes() if s not in a]
    w_current = attr(g, abar, jbar)[0]
    return w_current