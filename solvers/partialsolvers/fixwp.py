from tools import operations as ops
from graph import Graph
from solvers import buchi
from solvers.reachability import attractor as attr

def build_buchi_game(g, j, lam):
    """
    Build the game on which we will solve a buchi objective.
    :param g: the game to solve.
    :param j: the player for which we want to create the new game.
    :param lam: the maximum size of a window.
    :return: g' the new game created. Note that we don't return beta like we do in the theory because we define a unique id for beta that is -s
    and we can retrieve it from the list of states.
    """
    g_new = Graph()
    for s in g.get_nodes(): #O(n) * O(d) * O(lambda)
        for c in range(0, ops.max_priority(g) + 1): #O(d) * O(lambda)
            for l in range(0, lam): #O(lambda)
                s_player = g.get_node_player(s)
                #node id is the concatenation of s, c and l plus letters to make the separation. 
                # Ex : if we have a node s = 5, c = 10, l = 2 we would have the node id = s5c10l2. 
                #this way we have unique id and we can easily find a specific node if we want to
                node_id = compute_id(s, c, l)
                #node informations are in the following format : (player, base node id, maximum color on the current window, step on current window) aka (s_player, s, c, l)
                g_new.add_node(node_id, (s_player, s, c, l))
        #add the state beta that detects the lambda-bad windows. We use a special identification and descriptor for this state
        g_new.add_node(-s, (-1, s, -1, -1))
    
    #iterate on all the node of g_new
    for node_id in g_new.get_nodes(): # (O(m + n) * O(d) * O(lambda)) (the two loops make a complexity O(m + n) with the + n for the beta_s)
        if node_id > -1:
            (s, c, l) = g_new.nodes[node_id][1:4]
            trans_list = g.get_successors(s)
            #iterate on all successors (in g) of the node s
            for s2 in trans_list:
                #when we encounter a c of parity j we know we can reset the window and go to the next state. So we add the corresponding transition in the new game
                if((c % 2) == j):
                    #we want to add a transition from (s, c, l) towards (s2, c2, l2)
                    #compute c2 to be the color of s2
                    c2 = g.get_node_priority(s2)
                    #compute the id of the node we want to add a transition toward
                    node_id_trans = compute_id(s2, c2, 0)

                #when we are just continuing on the current window
                elif((c % 2) != j and l < (lam - 1)):
                    #we want to add a transition from (s, c, l) towards (s2, c2, l2)
                    #compute c2 to be the maximum between c and the color of s2
                    c2 = max(c, g.get_node_priority(s2))
                    #compute the id of the node we want to add a transition toward
                    node_id_trans = compute_id(s2, c2, l + 1)

                #when we just detected a lambda-bad window
                else:
                    #we want to add a transition from (s, c, l) towards beta_s2 the beta corresponding to state s2
                    node_id_trans = -s2
                
                #we add the transition we just compute to g_new
                g_new.add_successor(node_id, node_id_trans)
                g_new.add_predecessor(node_id_trans, node_id)
        else:
            #beta case, we add a transition from beta_s to (s, c(s), 0)
            node_id_trans = compute_id(- node_id, g.get_node_priority(-node_id), 0)
            g_new.add_successor(node_id, node_id_trans)
            g_new.add_predecessor(node_id_trans, node_id)

    return (g_new)

def solve_fixwp(g, j, lam):
    """
    Compute the winning state on the game g for the player j and the objective FixWP_j(lam). To do this, we will construct a new game g_new 
    with the function build_buchi_game and we will compute the winning regions of a co-buchi objective on it (actually we compute a buchi 
    objective in order to get the winning regions of the co-buchi objective). With that we will have the winning state of FixWP_j(lam).
    :param g: the game to solve.
    :param j: the player for who we want to retrieve the winning state of his objective.
    :param lam: the maximum size of a window.
    :return: a list containing the winning state of the player j.
    """
    #construction of the game on which we will solve the buchi/co_buchi objective.
    g_new = build_buchi_game(g, j, lam)
    #The map and the lambda function take all the node in g and return a list with each the opposite of each element, that corresponds to the beta states
    beta = map(lambda x: x*-1, g.get_nodes())
    #we compute the winning region of the player jbar for the objective Buchi(beta). 
    w_buchi = buchi.basic_buchi(g_new, beta, ops.opponent(j))
    #now we will transform what we just got into the winning region of the play j for the objective Buchi(S \ beta).
    #instead of basically computing the winning region of the co-buchi objective, we directly keep the state s that we are interested in.
    #because the true winning region of the co_buchi objective contains state in the following format : (s, c, l).
    w_cobuchi = []
    for node_id in g_new.get_nodes():
        #to avoid taking beta states. str are considered as > 0
        if node_id > 0:
            s = g_new.nodes[node_id][1]
            if (node_id not in w_buchi) and (s not in w_cobuchi):
                w_cobuchi.append(s)

    #now we just have to return w_cobuchi because it is equal to the winning region of the player j for the objective FixWP_j(lam)
    return w_cobuchi

def partial_solver(g, lam):
    """
    Compute an under-approximation of the winning regions of the two player for a strong parity objective. For that purpose we compute
    the winning region of j for the objective FixWP_j(lam) with the function solve_fixwp and we compute the winning region of jbar 
    for the objective FixWP_jbar(lam)
    :param g: the game to solve.
    :param lam: the maximum size of a window
    :return: an under-approximation of the winning regions of the two players for a strong parity objective
    """
    W0 = solve_fixwp(g, 0, lam)
    W1 = solve_fixwp(g, 1, lam)
    return (W0, W1)

def partial_solver2(g, lam):
    """
    Compute an under-approximation of the winning regions of the two player for a strong parity objective. For that purpose we compute
    the winning region of j for the objective FixWP_j(lam) with the function solve_fixwp and instead of returning it directly, we 
    compute an attractor for the player j on the set computed previously and we recursively call the function with a subgame where we 
    removed the states in the attractor. The result returned for player j is the union between the attractor and the result from the 
    recursive call. For the player jbar, the result is just the result from the recursive call.
    :param g: the game to solve.
    :param lam: the maximum size of a window
    :return: an under-approximation of the winning regions of the two players for a strong parity objective
    """
    #Following the same method as the winning core, so same notations are used 
    #Following the pseudo code given on the report
    #First we compute the solution set for player 0 for FixWP_0(lam) which is an under-approximation of player 0 winning region
    wp_w0 = solve_fixwp(g, 0, lam)
    #can happen that wp_w0 is empty, so checking 
    if len(wp_w0) != 0:
        #compute attractor in g for player 0 to the target set wp_w0
        att = attr(g, wp_w0, 0)[0]
        #computing a subgame g_prime that only contains states of (S \ a_prime)
        states_prime = [s for s in g.get_nodes() if not s in att]
        g_prime = g.subgame(states_prime)
        #recursively compute the partial solutions of g_prime
        (W0_prime, W1_prime) = partial_solver2(g_prime, lam)
        #we know that a_prime is part of player 0 winning region so we add it to W0_prime
        W0 = att + W0_prime
        W1 = W1_prime
        return (W0, W1)
    #we're in the case where wp_w0 was empty. this part of the algorithm is really similar to the part upside
    #computing  wp_w1 that is the solution set for player 1 for FixWP_1(lam), an under-approximation of player 1 winning region
    wp_w1 = solve_fixwp(g, 1, lam)
    #can happen that wp_w1 is empty, so checking 
    if len(wp_w1) != 0:
        #compute attractor in g for player 1 to the target set wp_w1
        att = attr(g, wp_w1, 1)[0]
        #computing a subgame g_prime that only contains states of (S \ a_prime)
        states_prime = [s for s in g.get_nodes() if not s in att]
        g_prime = g.subgame(states_prime)
        #recursively compute the partial solutions of g_prime
        (W0_prime, W1_prime) = partial_solver2(g_prime, lam)
        #we know that a_prime is part of player 1 winning region so we add it to W1_prime
        W1 = att + W1_prime
        W0 = W0_prime
        return (W0, W1)
    #we're in the cas where wp_w0 and wp_w1 was empty. In this case we can't say anything about the winning regions of the players.
    return ([], [])

def compute_id(s, c, l):
    """
    Compute the id of a node in g_new by concatenating s, c, l with letters to identify each part in the id.
    :param s: the id of the state in g.
    :param c: the maximum color seen on the current window.
    :param l: the number of step in the current window.
    :return: the id of the node (s, c, l) in g_new.
    """
    res = "s" + str(s) + "c" + str(c) + "l" + str(l)
    return res