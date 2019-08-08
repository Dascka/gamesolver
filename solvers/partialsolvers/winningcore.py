from tools import operations as ops
from graph import Graph
from solvers.reachability import attractor as attr

def compute_gdagger(g, j):
    """
    Compute and return the product game g_dagger from g for the player j.
    :param g: the game on which g_dagger is based.
    :param j: the player for who g_dagger is computed.
    :return: the product game g_dagger from g for the player j.
    """
    #creating a list containing all colors in the game
    d = ops.max_priority(g)
    colors = range(0, d+1)

    g_dagger = Graph()
    #adding all states in g_dagger. The stated are created doing a cartesian product between g states and colors
    for s in g.get_nodes():
        for v in colors:
            #node_id is a concatenation of the node id in g and the color c that will be added in the node_info
            node_id = int(str(s) + str(v))
            #computing the color of the state
            s_color = g.get_node_priority(s)
            node_color = -1
            if v % 2 == j:
                node_color = s_color
            else:
                node_color = v
            #player of s is the same as the player of the node we are creating
            s_player = g.get_node_player(s)
            #node info take this form : (player, base node id, color computed, v : supposed to be the maximal color encoutered on the path)
            node_info = (s_player, s, node_color, v)
            #add the node in g_dagger
            g_dagger.add_node(node_id, node_info)
    
    #now adding the trasitions between the states.
    #we add a trasition ((s1, v1), (s2, v2)) iff (s1, s2) is a transition in g and if v2 = max(v1, c(s2))
    for s1 in g_dagger.get_nodes():
        #getting the id of the corresponding node in g
        s1_id_g = g_dagger.nodes[s1][1]
        for s2 in g.get_successors(s1_id_g):
            #getting the color of s2 in g
            s2_color = g.get_node_priority(s2)
            #getting v1  from the state s1
            v1 = g_dagger.nodes[s1][3]
            v2 = max(v1, s2_color)
            #with that we've got (s2, v2) towards which we want to add a transition from s1 (s1 is already a state of g_dagger we can considerate it as (s1_id_g, v1))
            #getting the node id of (s2, v2) in g_dagger
            node_id_trans = int(str(s2) + str(v2))
            g_dagger.add_successor(s1, node_id_trans)
            g_dagger.add_predecessor(node_id_trans, s1)

    return g_dagger

def compute_Bi(g, j, b_i):
    """
    Compute the step i+1 of the under-approximation of the winning core. For this purpose we create the game g_dagger on which we compute the attractor on a specific region. By checking if the (s, 0) are in the attractor computed, we know if the state s is in b_i+1 or not.
    :param g: the game to solve.
    :param j: the player for who we want to compute B_i+1.
    :param b_i: the previous step computed before
    :return: the states of B_i+1 in a list.
    """
    #compute the new game g_dagger 
    g_dagger = compute_gdagger(g, j)
    #get the color of parity j to be able to compute a target for the future computation of an attractor
    j_colors = get_j_colors(g, j)
    #compute the cartesian product between j_colors and b_i. That will be the target for the future computation of an attractor
    target = []
    for s in b_i:
        for c in j_colors:
            #computing node id of (s, c)
            sc_id = int(str(s) + str(c))
            target.append(sc_id)
    #a for attractor, we compute the attractor for player j on the target we computed just before.
    a = attr(g_dagger, target, j)[0]

    #checking if (s, 0) is in the attractor a, if so we know that s is in b_i+1
    b_i_next = []
    for s in b_i:
        #compute the id of the node (s, 0)
        s0_id = int(str(s) + str(0))
        if s0_id in a:
            b_i_next.append(s)

    return b_i_next

def compute_Bn(g, j):
    """
    Compute the under-approximation of the winning core. For this puropose we compute iteratively each b_i until we have b_n or until we have a convergence in the sequence.
    :param g: the game to solve.
    :param j: the player for who we want to compute B_n.
    :return: the states of B_n in a list.
    """
    #b_0 = S
    b_i = g.get_nodes()

    #compute the b_i until having b_n or a convergence
    for i in range (len(g.get_nodes())):
        #compute b_i+1
        b_i_next = compute_Bi(g, j, b_i)
        #checking if the sequence converged or not
        if ops.are_lists_equal(b_i, b_i_next):
            b_i = b_i_next
            break
        else:
            b_i = b_i_next

    return b_i

def partial_solver(g):
    """
    Compute an under-approximation of the winning regions of the two player for a strong parity objective. For that purpose we compute
    an under-approximation of the winning core for a player j, we compute an attractor for the player on the set computed previously 
    and we recursively call the function with a subgame where we removed the states in the attractor. The result returned for player j 
    is the union between the attractor and the result from the recursive call. For the player jbar, the result is just the result from 
    the recursive call.
    :param g: the game to solve.
    :return: an under-approximation of the winning regions of the two players for a strong parity objective
    """
    #Following the pseudo code given on the report
    #First we compute B_n for player 0 which is an under-approximation of player 0 winning core 
    a = compute_Bn(g, 0)
    #can happen that a is empty, so checking 
    if len(a) != 0:
        #compute attractor in g for player 0 to the target set a
        a_prime = attr(g, a, 0)[0]
        #computing a subgame g_prime that only contains states of (S \ a_prime)
        states_prime = []
        for s in g.get_nodes():
            if s not in a_prime:
                states_prime.append(s)
        g_prime = g.subgame(states_prime)
        #recursively compute the partial solutions of g_prime
        (W0_prime, W1_prime) = partial_solver(g_prime)
        #we know that a_prime is part of player 0 winning region so we add it to W0_prime
        W0 = a_prime + W0_prime
        W1 = W1_prime
        return (W0, W1)
    #we're in the case where a was empty. this part of the algorithm is really similar to the part upside
    #computing a new a that is B_n for player 1, an under-approximation of player 1 winning core 
    a = compute_Bn(g, 1)
    #can happen that a is empty, so checking 
    if len(a) != 0:
        #compute attractor in g for player 1 to the target set a
        a_prime = attr(g, a, 1)[0]
        #computing a subgame g_prime that only contains states of (S \ a_prime)
        states_prime = []
        for s in g.get_nodes():
            if s not in a_prime:
                states_prime.append(s)
        g_prime = g.subgame(states_prime)
        #recursively compute the partial solutions of g_prime
        (W0_prime, W1_prime) = partial_solver(g_prime)
        #we know that a_prime is part of player 1 winning region so we add it to W1_prime
        W1 = a_prime + W1_prime
        W0 = W0_prime
        return (W0, W1)
    #we're in the cas where a was empty for player 0 and player 1. In this case we can't say anything about the winning regions of the players.
    return ([], [])


def get_j_colors(g, j):
    """
    Give the colors of parity j
    :param g: the game to solve.
    :param j: the player for who we want to get the colors.
    :return: the colors of parity j.
    """
    d = ops.max_priority(g)
    j_colors = []
    for i in range(1, d+1):
        if i%2 == j:
            j_colors.append(i)
    return j_colors