# coding=utf-8
from graph import Graph
from collections import defaultdict
import matplotlib.pyplot as plt

"""
This module handles file reading (to load graph) and writing (to write the solution).
"""

def load_from_file(path):
    """
    Loads a game graph from a file specified by the path.
    The file must be in PGSolver format.
    :param path: path to the file.
    :return: a Graph g corresponding to the game graph in the file.
    """
    with open(path, 'r') as f:
        g = Graph()
        next(f)
        for line in f:
            split_line = line.split(" ")
            node = int(split_line[0])
            priority = int(split_line[1])

            if split_line[2] == "0":
                g.add_node(node, (0, priority))
            else:
                g.add_node(node, (1, priority))

            for succ in split_line[3].split(","):
                g.add_successor(node, int(succ))
                g.add_predecessor(int(succ), node)

    return g

def load_generalized_from_file(path):
    """
    Loads a generalized parity game graph from a file specified by the path.
    The file must be in PGSolver format for generalized parity.
    :param path: path to the file.
    :return: a Graph g corresponding to the game graph in the file.
    """
    with open(path, 'r') as f:
        g = Graph()
        next(f)
        for line in f:
            split_line = line.split(" ")
            node = int(split_line[0])
            priorities = []
            for prio in split_line[1].split(","):
                priorities += [int(prio)]
            if split_line[2] == "0":
                g.add_node(node, tuple([0]+priorities))
            else:
                g.add_node(node, tuple([1]+priorities))

            for succ in split_line[3].split(","):
                g.add_successor(node, int(succ))
                g.add_predecessor(int(succ), node)

    return g

def write_solution_to_file(g, solution, player, path):
    """
    Writes the solution of a game in dot format to a file specified by the path.
    Winning region and strategy of player 0 (1) is in blue (green).
    Nodes belonging to player 0 (1) are circles (squares).
    :param g: the game Graph.
    :param solution: if player is 0, expected solution format is (W_0, sigma_0),(W_1, sigma_1). If player is 1, invert.
    :param player: the player to which the first tuple in the solution belongs.
    :param path: the path to the file in which we write the solution.
    """

    if player == 0:
        (W_0, sigma_0), (W_1, sigma_1) = solution
    else :
        (W_1, sigma_1), (W_0, sigma_0) = solution

    with open(path, 'w') as f:
        f.write("digraph G {\n")
        f.write("splines=true;\nsep=\"+10,10\";\noverlap=scale;\nnodesep=0.6;\n")
        for node in W_0:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=blue3"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)

                if succ == sigma_0[node]:
                    to_write += '[color=blue3];\n'
                elif succ == sigma_1[node]:
                    to_write += '[color=forestgreen];\n'
                else:
                    to_write += ";\n"
            f.write(to_write)

        for node in W_1:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=forestgreen"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)

                if succ == sigma_1[node]:
                    to_write += '[color=forestgreen];\n'
                elif succ == sigma_0[node]:
                    to_write += '[color=blue3];\n'
                else:
                    to_write += ";\n"
            f.write(to_write)

        f.write('}')

def write_solution_to_file_no_strategies(g, W1, W2, path):
    """
    Writes the solution of a parity game in dot format to a file specified by the path.
    Winning region of player 0 (1) is in blue (green).
    Nodes belonging to player 0 (1) are circles (squares).
    :param g: the game Graph.
    :param W1: winning region of player 0 (1).
    :param W2: winning region of player 1 (2).
    :param path: the path to the file in which we write the solution.
    """

    with open(path, 'w') as f:
        f.write("digraph G {\n")
        f.write("splines=true;\nsep=\"+10,10\";\noverlap=scale;\nnodesep=0.6;\n")
        for node in W1:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=blue3"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)
                to_write += ";\n"
            f.write(to_write)

        for node in W2:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=forestgreen"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)
                to_write += ";\n"
            f.write(to_write)

        f.write('}')

def write_solution_to_file_no_strategies_solvpart(g, W1, W2, path):
    """
    Writes the solution of a parity game in dot format to a file specified by the path.
    Winning region of player 0 (1) is in blue (green).
    Nodes belonging to player 0 (1) are circles (squares).
    :param g: the game Graph.
    :param W1: winning region of player 0 (1).
    :param W2: winning region of player 1 (2).
    :param path: the path to the file in which we write the solution.
    """

    with open(path, 'w') as f:
        f.write("digraph G {\n")
        f.write("splines=true;\nsep=\"+10,10\";\noverlap=scale;\nnodesep=0.6;\n")
        for node in W1:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=blue3"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)
                to_write += ";\n"
            f.write(to_write)

        for node in W2:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=forestgreen"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)
                to_write += ";\n"
            f.write(to_write)

        #adding the node not solved
        for node in g.get_nodes():
            if node not in W1 and node not in W1:
                to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.get_node_priority(node)) + "\""
                if g.get_node_player(node) == 0:
                    to_write += ",shape=circle"
                elif g.get_node_player(node) == 1:
                    to_write += ",shape=square"
                else:
                    pass
                    # error
    
            to_write += ",color=black"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)
                to_write += ";\n"
            f.write(to_write)

        f.write('}')

def write_generalized_solution_to_file(g, W1, W2, path):
    """
    Writes the solution of a generalized parity game in dot format to a file specified by the path.
    Winning region of player 0 (1) is in blue (green).
    Nodes belonging to player 0 (1) are circles (squares).
    :param g: the game Graph.
    :param W1: winning region of player 0 (1).
    :param W2: winning region of player 1 (2).
    :param path: the path to the file in which we write the solution.
    """

    with open(path, 'w') as f:
        f.write("digraph G {\n")
        f.write("splines=true;\nsep=\"+10,10\";\noverlap=scale;\nnodesep=0.6;\n")
        for node in W1:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.nodes[node][1:]) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=blue3"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)
                to_write += '[color=black];\n'
            f.write(to_write)

        for node in W2:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.nodes[node][1:]) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=forestgreen"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)
                to_write += '[color=black];\n'
            f.write(to_write)

        f.write('}')

def write_graph_to_file(g, path):
    """
    Writes a game graph to a file specified by the path in dot format.
    :param g: a game Graph.
    :param path: the file to which we write the graph.
    """

    with open(path, 'w') as f:
        f.write("digraph G {\n")
        for node in g.get_nodes():
            to_write = str(node) + "[label=\"" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += "];\n"

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ) + ";\n"

            f.write(to_write)

        f.write('}')

def write_benchmark_partial_solver(comp_solv, part_solv, percent_solv, path,  n_, y, max_game_size, n_launch, lam, plot, path_plot):
    """
    After a certain number of game ran, writes the number of games completely solved, the number of games partialy solved and for the game partialy solved writes the mean of 
    the percentage solved for player 0 and player 1 and both player
    :param comp_solv: The number of games completely solved.
    :param part_solv: The number of games partialy solved.
    :param percent_solv: A list containing for each game not completely solved, the percentage solved for player 0, player 1 and both players.
    :param path: the path to the file in which we write.
    :param n_: contains data for the plot, n_[i] is a size of a game.
    :param y: contains data for the plot, y[i] is the time taken to solve the game of size n_[i].
    :param max_game_size: maximum game size used in the benchmark.
    :param n_launch: number of times we launched the benchmark. It's also equal to the number of games of each size.
    :param lam: value of lambda.
    :param plot: if True, do the plot. Generally True for random benchmark
    :param path_plot: the path to the file in which we write the plot.
    """
    #txt
    #for each game partialy solved, compute the mean of the percentage solved for both player
    percent_solv_both = defaultdict(lambda: 0.) #we need this for the plots too
    #another dictionnary to store how many of each game are not completely solved for each size
    n = defaultdict(lambda: 0) #need this for the plots too
    with open(path, 'w') as f:
        #number of games completely solved
        f.write("Games completely solved : " + str(comp_solv) + "\n")
        #number of games partialy solved
        f.write("Games partialy solved : " + str(part_solv) + "\n")
        #for each game partialy solved, compute the mean of the percentage solved for each and both player
        #for that we store in dictionnary the mean for each size of game where the keys are the size
        percent_solv_0 = defaultdict(lambda: 0.)
        percent_solv_1 = defaultdict(lambda: 0.)
        
        for (size, both, player0, player1) in percent_solv:
            percent_solv_both[size] += both
            percent_solv_0[size] += player0
            percent_solv_1[size] += player1
            n[size] += 1

        f.write("For each game not completely solved : \n" )
        #the three contains the same keys iterating on one's keys is the same as iterating on all
        for size in percent_solv_both:
            percent_solv_both[size] = percent_solv_both[size]/n[size]
            percent_solv_0[size] = percent_solv_0[size]/n[size]
            percent_solv_1[size] = percent_solv_1[size]/n[size]
            f.write("For game of size " + str(size) + " (" + str(n[size]) + " games): \n")
            f.write("\tPercentage solved for both players : " + str(percent_solv_both[size]) + "\n")
            f.write("\tPercentage solved for player 0 : " + str(percent_solv_0[size]) + "\n")
            f.write("\tPercentage solved for player 1 : " + str(percent_solv_1[size]) + "\n")
        
    #plot
    if plot:
        #create dictionnary containing the sum of time for the games of a certain size.
        #the keys of the dictionnary are the different size contained in n_
        time = defaultdict(lambda: 0)
        #we need another dict to store how many game of each size we have to compute the mean
        n2 = defaultdict(lambda: 0)
        #compute the time's mean
        for i in range(0, len(n_)):
            for j in range(0, len(n_[i])):
                size = n_[i][j]
                n2[size] += 1
                time[size] += y[i][j]
        for size in time:
            time[size] = time[size]/n2[size]

        #need to calculate the mean of percentage solved for game of each size
        #we know how many games there are for each size (n_launch)
        #we know how many games are not completely solved for each size (n[size])
        #so we can know how many game are completely solved for each size (n_launch - n[size])
        #with that we can compute the mean

        
        comp_solv = defaultdict(lambda: 0)
        #mean of percentage solved for game of each size
        mean_percent_solv = defaultdict(lambda: 0)
        for size in n2:
            #number of games completely solved for the size size
            comp_solv = n_launch - n[size]
            #compute the mean
            mean_percent_solv[size] = (percent_solv_both[size] + 100*comp_solv)/n_launch

        #do the plot
        fig, ax1 = plt.subplots()
        plt.grid(True)
        if lam != -1:
            plt.title(u"Graphes aléatoires de taille 1 à " + str(max_game_size) + " avec lambda = " + str(lam))
        else:
            plt.title(u"Graphes aléatoires de taille 1 à " + str(max_game_size))
        plt.xlabel(u'nombre de nœuds')
        # plt.yscale("log") allows logatithmic y-axis
        ax1.plot(time.keys(), time.values(), 'g.', label=u"Temps d'exécution", color='b')
        ax1.tick_params('y', colors='b')
        ax1.set_ylabel("Temps d'execution (s)", color = 'b')

        ax2 = ax1.twinx()
        ax2.plot(mean_percent_solv.keys(), mean_percent_solv.values(), 'g.', label=u"Pourcentage résolu", color='r')
        ax2.set_ylim([0, 101])
        ax2.set_ylabel("Pourcentage du jeu resolu (%)", color = 'r')
        ax2.tick_params('y', colors='r')
        fig.tight_layout()

        plt.savefig(path_plot+".png", bbox_inches='tight')
        plt.clf()
        plt.close()