from tools import operations as ops
from graph import Graph
from solvers.reachability import attractor as attr
import copy
import numpy as np

def construct_g_i_k(g, i, k, j):
    """
    Construct the graph g_i_k for player j.
    Works in (O(n) + O(m*n))=O(m*n) 
    :param g: the game on which we look for the inedges of s2.
    :param s1: the first state of the edge.
    :param s2 : the second state of the edge.
    :param i: the step i of the algorithme used to compute 2**i.
    :return: true if the edge (s1, s2) is in first the 2**i inedges from the edges of g, else if not.
    """
    #stocking it to avoid computing it multiples times
    exp = 2**i
    #creating the new game graph
    g_new = Graph()
    #adding the states so they can have the proper color. We add every state from g. 
    #the color of the states is blue if the state belong to j and has an out degree > exp. The color is red if the state belong to j and has an out degree > exp.
    #The color is white ohterwise.
    #colors : O = blue, 1 = red, 2 = white.
    for s in g.get_nodes(): #O(n)
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
    
    for s1 in g.get_nodes():#O(m) with the second loop
        succ = g.get_successors(s1)
        for s2 in succ:
            if len(succ) <= exp or in_first_edge(g, s1, s2, i):#O(n) cause of in_first_edge
                g_new.add_successor(s1, s2)
                g_new.add_predecessor(s2, s1)
    return g_new
            

def in_first_edge(g, s1, s2, i):
    """
    Return if the edge (s1, s2) is in first the 2**i inedges from the edges of g. We suppose that the edges are sorted properly according to the sort explained in theory.
    Works in O(n)
    :param g: the game on which we look for the inedges of s2.
    :param s1: the first state of the edge.
    :param s2 : the second state of the edge.
    :param i: the step i of the algorithme used to compute 2**i.
    :return: true if the edge (s1, s2) is in first the 2**i inedges from the edges of g, else if not.
    """
    inedges = g.get_predecessors(s2)
    exp = 2**i
    #cheking if the edge between (s1, s2) is in the first 2^i predessors edges of s2.
    for i in range(len(inedges)):#O(n), the state has at max n predecessors
        if i > exp:
            return False
        if inedges[i] == s1:
            return True
    return False

def new_buchi(g, t, j):
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
    # x = s \ y so the states that are not in the attractor
    y, x = attr(g, t, j) #O(m+n)
    #d the set of states that we removed from the current game g_k
    #s_k = s \ d, so the states that are not in the attractor
    d, s_k = attr(g, x, ops.opponent(j)) #O(n+m)
    #we have to sort the edge of g_k such that edge (u, v) are first with u such that u belongs to jbar and u is not in t
    #we do it only one time, once it's sorted it will stay sorted with the way subgames are created
    for v in g.get_nodes(): #O(m)
        first_succ = []
        last_succ = []
        for u in g.get_predecessors(v):
            if g.get_node_player(u) == ops.opponent(j) and u not in t:
                first_succ.append(u)
            else:
                last_succ.append(u)
        g.predecessors[v] = first_succ + last_succ
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
    #"repeat until" equivalent. We repeat the loop until we have i = log_2(n)
    while True: #O(log(n))
        #construct a special graph with and ordering on inedges and color on states
        g_i_k = construct_g_i_k(g_k, i, k, j) #O(n*m)
        #compute z_i_k to be a set containing states from g_i_k such that they are (i) red (color 1) without outedges in g_i_k or (ii) blue (color 0) in g_i_k
        z = []
        for s in g_i_k.get_nodes():#O(n)
            s_color = g_i_k.get_node_priority(s)
            if (s_color == 1 and len(g_i_k.get_successors(s)) == 0) or s_color == 0:
                z.append(s)
        #actualing the target set to correspond with the current set of state
        t_k = [s for s in t_k if s in s_k] #O(n^2)
        target = t_k + z
        #computing y with our new value
        #y is the attractor in g for player j towards the set t 
        # x = s \ y so the states that are not in the attractor
        y, x = attr(g, target, j) #O(m+n)
        #incrementing i
        i = i + 1
        #if x is not empty we compute a new d and remove it from the g_k
        if len(x) != 0:
            #d the set of states that we removed from the current game g_k
            #s_k = s \ d, so the states that are not in the attractor
            d, s_k = attr(g, x, ops.opponent(j)) #O(n+m)
            g_k = g_k.subgame(s_k)
            k = k + 1
            U = U + d
        #we stop when i = log_2(n)
        if len(g.get_nodes()) == 0 or i >= np.log2(len(g.get_nodes())):
            break
    #we will return all states but those who were removed ie we return the set of states S \ U
    Wj = [s for s in g.get_nodes() if s not in U] #O(n^2)
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
    g_current = copy.deepcopy(g) #O(n + m)
    #the states of the game on current iteration
    s_current = g_current.get_nodes()
    #
    w_current = []
    U = []
    #"repeat until" equivalent. Loop until w_current is empty
    while True: #O(n) loop => total : O(n^3)
        #current target set that only contains states of s_k
        t_current = [s for s in t if s in s_current] #O(n^2)
        w_current = avoid_set_classical(g_current, t_current, j) #O(n^2) (see avoid_set_classical)
        #s_current = s_current \ w_current, we remove the states from w_current
        s_current = [s for s in s_current if s not in w_current] #O(n^2)
        g_current = g_current.subgame(s_current) #O(n^2)
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
    :param t: the target set such that t is included in g's states.
    :return: a set of states that are winning for player j for the buchi objective.
    """
    jbar = ops.opponent(j)
    a, abar = attr(g, t, j) #O(n+m)
    w_current = attr(g, abar, jbar)[0] #O(n+m)
    #the total is in O(2n+2m+n^2) = O(n^2)
    return w_current