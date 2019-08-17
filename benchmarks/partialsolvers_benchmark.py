# coding=utf-8
from tools import timer, generators
from tools import file_handler as io
from solvers.partialsolvers import fixwp, dirfixwp, winningcore
from solvers.strongparity import strong_parity_solver_no_strategies as sp
from random import randint
import matplotlib.pyplot as plt

def launch_random_wp(game_size, n_launch, lam=1, step = 10, dir=True, v2 = False, plot=False, path="", save_res = False, path_res = ""):
    """
    Launch a random benchmark on window parity solver n_launch times. Record the games that are not solved completely and record their resolution percentage for each player
    :param game_size: number of nodes in generated graph (nodes is n due to construction).
    :param n_launch: number of times the random benchmark is used.
    :param lam: value of lambda.
    :param: step to be taken between the different value of lambda.
    :param dir: if True, uses DirFixWP if not, uses FixWP.
    :param v2: if True, uses partial_solver2. If False, uses partial_solver.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the plots.
    :param save_res: if True, save the results on a file.
    :param path_res: path to the file in which to write the result.
    :return: a tuple containing the number of games completely solved, the number of games partialy solved and a list containing for each game partialy solved the percentage
    solved for each player and in total.
    """
    #count the number of games completely solved
    comp_solv = 0
    #count the number of games not completely solved
    part_solv = 0
    #list of tuples containing (a, b, c) where a is the total percentage solved, b is the percentage solved for player 0 and c is the percentage solved for player 1 
    percent_solv = []
    #y[i] contains time to resolve game of size n_[i]
    y = []
    n_ = []
    for i in range(0, n_launch):
        #the benchmark return the games that are nos completely solved 
        (games, (n_ret, y_ret)) = benchmark_random_wp(game_size, start_lambda=lam, end_lambda=lam, dir=dir, v2=v2, step=step, plot=False, ret=True, path=path, prt = False)
        #append n_ret and y_ret to a list
        #careful, n_ret and y_ret are lists but only contains one element (only one lambda in the benchmark call)
        n_.append(n_ret[0])
        y.append(y_ret[0])
        for (g, w0, w1) in games:
            #one more game not solved completely
            part_solv += 1
            #checking is the solutions are included to the true solutions. Computing the true sols with Zielonka algorithm
            (sp_w0, sp_w1) = sp(g)
            a =  all(s in sp_w1 for s in w1) #cheking if included
            b =  all(s in sp_w0 for s in w0) #cheking if included
            #if not included stop the algorithm 
            if not a or not b:
                print "Error the solutions found are not included to the true solutions"
                return -1
            #total percentage solved
            percent_solved_total = ((float(len(w0)) + len(w1)) /(len(sp_w0) + len(sp_w1))) * 100 
            #percentage solved for player 0
            if len(sp_w0) > 0:
                percent_solved_0 = (float(len(w0)) /len(sp_w0)) * 100
            else:
                percent_solved_0 = 100
            #percentage solved for player 1
            if len(sp_w1) > 0:
                percent_solved_1 = (float(len(w1)) /len(sp_w1)) * 100
            else:
                percent_solved_1 = 100
            #adding the percentages computed to the list + the size of the game
            percent_solv.append((len(g.get_nodes()), percent_solved_total, percent_solved_0, percent_solved_1))

        comp_solv += game_size/step - len(games)

    #writes informations in a txt and if needed creates a plot.
    #the informations written are the game completely solved, and for the game not completely solved the percentage solved for each players and this for each size of game
    if save_res:
        io.write_benchmark_partial_solver(comp_solv, part_solv, percent_solv, path_res, n_, y, game_size, n_launch, lam, plot, path)
    #Return what is basically written in the txt file.
    return (comp_solv, part_solv, percent_solv)

def benchmark_random_wp(n, start_lambda = 1, end_lambda = 10, step_lambda = 1, dir = True, v2 = False, iterations=3, step=10, ret = False, plot=False, path="", prt = True):
    """
    Benchmarks the window parity algorithms for strong parity games using the random game generator.
    Calls window parity partial solver on games generated using the random game generator function.
    Games of size 1 to n are solved and a timer records the time taken to get the solution.The solver can be timed
    several times and the minimum value is selected using optional parameter iterations (to avoid recording time
    spikes and delays due to system load). The result can be plotted using matplotlib.
    :param n: number of nodes in generated graph (nodes is n due to construction).
    :param end_lambda: maximum value of lambda.
    :param start_lambda: starting value of lambda.
    :param step_lambda: step to be taken between the different value of lambda.
    :param dir: if True, uses DirFixWP if not, uses FixWP.
    :param v2: if True, uses partial_solver2. If False, uses partial_solver.
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param ret: if True, return the winning region of the games that were not completely solved.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    :param prt: True if the prints are activated.
    :return: Percentage of game solved, size of the games such that we return the time taken to resolve those games.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values (1 to n)
    per_sol = [] # list for the percentage of the game solved

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    lam = start_lambda #current lambda used by the algorithme

    not_comp_solved = [] #store the game that are not completely solved

    # print first line of output
    if prt:
        print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "|" + "Percentage solved".center(19) + "|" + "\n" + \
            "-" * 115

    #for each value of lambda
    for lam in range(start_lambda, end_lambda + 1, step_lambda):
        #print current value of lambda
        if prt:
            print "lambda value : ".center(40) + str(lam) + "\n" + "-" * 115
        y_temp = [] # stores time recordings for the current value of lambda
        n_temp = [] # stores the size of the game for the current value of lambda 
        per_sol_temp = [] #stores the resolution percentage of the games for the current value of lambda
        nbr_generated = 0
        # games generated are size 1 to n
        for i in range(1, n + 1, step):
            temp = []  # temp list for #iterations recordings
            prio = randint(0, i)  # number of priorities
            min_out = randint(1, i) # minimum number of out edges
            max_out = randint(min_out, i) #maximum number of out edges
            g = generators.random(i, prio, min_out, max_out)  # generated game

            # #iterations calls to the solver are timed
            for j in range(iterations):
                with chrono:
                    if dir:
                        if v2:
                            (w0, w1) = dirfixwp.partial_solver2(g, lam)  # dirfixwp version 2 call
                        else:
                            (w0, w1) = dirfixwp.partial_solver(g, lam)  # dirfixwp call
                    else:
                        if v2:
                            (w0, w1) = fixwp.partial_solver2(g, lam)  # fixwp version 2 call
                        else:
                            (w0, w1) = fixwp.partial_solver(g, lam)  # fixwp call
                temp.append(chrono.interval)  # add time recording

            min_recording = min(temp)
            percent_solved = ((float(len(w0)) + len(w1)) /(i)) * 100
            #checking if completely solved
            if percent_solved != 100:
                not_comp_solved.append((g, w0, w1))

            y_temp.append(min_recording)  # get the minimum out of #iterations recordings
            n_temp.append(i) 
            per_sol_temp.append(percent_solved)
            total_time += min_recording
            

            if prt:
                print "Random graph".center(40) + "|" + str(i).center(12) + "|" \
                + str(y_temp[nbr_generated]).center(40) + "|" + str(percent_solved).center(19) + "|" + "\n" + "-" * 115

            nbr_generated += 1  # updating the number of generated mesures
        y.append(y_temp)
        n_.append(n_temp)
        per_sol.append(per_sol_temp)


    # at the end, print total time
    if prt:
        print "-" * 115 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
          str(total_time).center(40) + "|" + "\n" + "-" * 115 + "\n"

    if plot:
        i = 0
        for lam in range(start_lambda, end_lambda + 1, step_lambda):
            fig, ax1 = plt.subplots()
            plt.grid(True)
            plt.title(u"Graphes aléatoires de taille 1 à " + str(n) + " avec lambda = " + str(lam))
            plt.xlabel(u'nombre de nœuds')
            # plt.yscale("log") allows logatithmic y-axis
            ax1.plot(n_[i], y[i], 'g.', label=u"Temps d'exécution", color='b')
            ax1.tick_params('y', colors='b')
            ax1.set_ylabel("Temps d'execution (s)", color = 'b')

            ax2 = ax1.twinx()
            ax2.plot(n_[i], per_sol[i], 'g.', label=u"Pourcentage résolu", color='r')
            ax2.set_ylim([0, 101])
            ax2.set_ylabel("Pourcentage du jeu resolu (%)", color = 'r')
            ax2.tick_params('y', colors='r')
            fig.tight_layout()

            plt.savefig(path+str(lam)+".png", bbox_inches='tight')
            plt.clf()
            plt.close()
            i = i + 1

    if ret:
        return (not_comp_solved, (n_, y))

def launch_random_wc(game_size, n_launch, step = 10, plot=False, path="", save_res = False, path_res = ""):
    """
    Launch a random benchmark on window parity solver n_launch times. Record the games that are not solved completely and record their resolution percentage for each player
    :param game_size: number of nodes in generated graph (nodes is n due to construction).
    :param n_launch: number of times the random benchmark is used.
    :param: step to be taken between the different value of lambda.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    :param save_res: if True, save the results on a file.
    :param path_res: path to the file in which to write the result.
    :return: a tuple containing the number of games completely solved, the number of games partialy solved and a list containing for each game partialy solved the percentage
    solved for each player and in total.
    """
    #count the number of games completely solved
    comp_solv = 0
    #count the number of games not completely solved
    part_solv = 0
    #list of tuples containing (a, b, c) where a is the total percentage solved, b is the percentage solved for player 0 and c is the percentage solved for player 1 
    percent_solv = []
    #y[i] contains time to resolve game of size n_[i]
    y = []
    n_ = []
    for i in range(0, n_launch + 1):
        #the benchmark return the games that are nos completely solved
        (games, (n_ret, y_ret)) = benchmark_random_wc(game_size, step=step, plot=False, ret=True, path=path, prt = False)
        #append n_ret and y_ret to a list
        n_.append(n_ret)
        y.append(y_ret)
        for (g, w0, w1) in games:
            #one more game not solved completely
            part_solv += 1
            #checking is the solutions are included to the true solutions. Computing the true sols with Zielonka algorithm
            (sp_w0, sp_w1) = sp(g)
            a =  all(s in sp_w1 for s in w1) #cheking if included
            b =  all(s in sp_w0 for s in w0) #cheking if included
            #if not included stop the algorithm 
            if not a or not b:
                print "Error the solutions found are not included to the true solutions"
                return -1
            #total percentage solved
            percent_solved_total = ((float(len(w0)) + len(w1)) /(len(sp_w0) + len(sp_w1))) * 100 
            #percentage solved for player 0
            if len(sp_w0) > 0:
                percent_solved_0 = (float(len(w0)) /len(sp_w0)) * 100
            else:
                percent_solved_0 = 100
            #percentage solved for player 1
            if len(sp_w1) > 0:
                percent_solved_1 = (float(len(w1)) /len(sp_w1)) * 100
            else:
                percent_solved_1 = 100
            #adding the percentages computed to the list + the size of the game
            percent_solv.append((len(g.get_nodes()), percent_solved_total, percent_solved_0, percent_solved_1))

        comp_solv += game_size/step - len(games)

    #writes informations in a txt and if needed creates a plot.
    #the informations written are the game completely solved, and for the game not completely solved the percentage solved for each players and this for each size of game
    if save_res:
        io.write_benchmark_partial_solver(comp_solv, part_solv, percent_solv, path_res, n_, y, game_size, n_launch, -1, plot, path)
    #Return what is basically written in the txt file.
    return (comp_solv, part_solv, percent_solv)
    
    
    
def benchmark_random_wc(n, iterations=3, step=10, ret = False, plot=False, path="", prt = True):
    """
    Benchmarks the window parity algorithms for strong parity games using the random game generator.
    Calls window parity partial solver on games generated using the random game generator function.
    Games of size 1 to n are solved and a timer records the time taken to get the solution.The solver can be timed
    several times and the minimum value is selected using optional parameter iterations (to avoid recording time
    spikes and delays due to system load). The result can be plotted using matplotlib.
    :param n: number of nodes in generated graph (nodes is n due to construction).
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param ret: if True, return the winning region of the games that were not completely solved.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    :param prt: True if the prints are activated.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values (1 to n)
    per_sol = [] # list for the percentage of the game solved

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    not_comp_solved = [] #store the game that are not completely solved

    # print first line of output
    if prt:
        print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "|" + "Percentage solved".center(19) + "|" + "\n" + \
            "-" * 115

    # games generated are size 1 to n
    for i in range(1, n + 1, step):
        temp = []  # temp list for #iterations recordings
        prio = randint(0, i)  # number of priorities
        min_out = randint(1, i) # minimum number of out edges
            max_out = randint(min_out, i) #maximum number of out edges
        g = generators.random(i, prio, min_out, max_out)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                (w0, w1) = winningcore.partial_solver(g)  # winning core call
            temp.append(chrono.interval)  # add time recording

        min_recording = min(temp)
        percent_solved = ((float(len(w0)) + len(w1)) /(i)) * 100
        if percent_solved != 100:
            not_comp_solved.append((g, w0, w1))

        y.append(min_recording)  # get the minimum out of #iterations recordings
        n_.append(i)
        per_sol.append(percent_solved)
        total_time += min_recording
        

        if prt:
            print "Random graph".center(40) + "|" + str(i).center(12) + "|" \
            + str(y[nbr_generated]).center(40) + "|" + str(percent_solved).center(19) + "|" + "\n" + "-" * 115

        nbr_generated += 1  # updating the number of generated mesures


    # at the end, print total time
    if prt:
        print "-" * 115 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
            str(total_time).center(40) + "|" + "\n" + "-" * 115 + "\n"

    if plot:
        fig, ax1 = plt.subplots()
        plt.grid(True)
        plt.title(u"Graphes aléatoires de taille 1 à " + str(n))
        plt.xlabel(u'nombre de nœuds')
        # plt.yscale("log") allows logatithmic y-axis
        ax1.plot(n_, y, 'g.', label=u"Temps d'exécution", color='b')
        ax1.tick_params('y', colors='b')
        ax1.set_ylabel("Temps d'execution (s)", color = 'b')

        ax2 = ax1.twinx()
        ax2.plot(n_, per_sol, 'g.', label=u"Pourcentage résolu", color='r')
        ax2.set_ylim([0, 101])
        ax2.set_ylabel("Pourcentage du jeu resolu (%)", color = 'r')
        ax2.tick_params('y', colors='r')
        fig.tight_layout()

        plt.savefig(path+".png", bbox_inches='tight')
        plt.clf()
        plt.close()

    if ret:
        return (not_comp_solved, (n_, y))

def benchmark_worst_case_wp(n, start_lambda = 1, end_lambda = 10, step_lambda = 1, dir = True, v2 = False, iterations=3, step=10, plot=False, path="", save_res = False, path_res = "", prt = True):
    """
    Benchmarks the window parity algorithms for strong parity games using the random game generator.
    Calls window parity partial solver on games generated using the random game generator function.
    Games of size 1 to n are solved and a timer records the time taken to get the solution.The solver can be timed
    several times and the minimum value is selected using optional parameter iterations (to avoid recording time
    spikes and delays due to system load). The result can be plotted using matplotlib.
    :param n: number of nodes in generated graph (nodes is n due to construction).
    :param end_lambda: maximum value of lambda.
    :param start_lambda: starting value of lambda.
    :param step_lambda: step to be taken between the different value of lambda.
    :param dir: if True, uses DirFixWP if not, uses FixWP.
    :param v2: if True, uses partial_solver2. If False, uses partial_solver.
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    :param save_res: if True, save the results on a file.
    :param path_res: path to the file in which to write the result.
    :param prt: True if the prints are activated.
    :return: Percentage of game solved, size of the games such that we return the time taken to resolve those games.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values (5 to 5n)
    per_sol = [] # list for the percentage of the game solved

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    lam = start_lambda #current lambda used by the algorithme

    not_comp_solved = [] #store the game that are not completely solved

    # print first line of output
    if prt:
        print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "|" + "Percentage solved".center(19) + "|" + "\n" + \
          "-" * 115

    #for each value of lambda
    for lam in range(start_lambda, end_lambda + 1, step_lambda):
        #print current value of lambda
        if prt:
            print "lambda value : ".center(40) + str(lam) + "\n" + "-" * 115
        y_temp = [] # stores time recordings for the current value of lambda
        n_temp = [] # stores the size of the game for the current value of lambda 
        per_sol_temp = [] #stores the resolution percentage of the games for the current value of lambda
        nbr_generated = 0      
        # games generated are size 1 to 5*n
        for i in range(1, n + 1, step):
            temp = []  # temp list for #iterations recordings
            g = generators.strong_parity_worst_case(i)  # generated game

            # #iterations calls to the solver are timed
            for j in range(iterations):
                with chrono:
                    if dir:
                        if v2:
                            (w0, w1) = dirfixwp.partial_solver2(g, lam)  # dirfixwp version 2 call
                        else:
                            (w0, w1) = dirfixwp.partial_solver(g, lam)  # dirfixwp call
                    else:
                        if v2:
                            (w0, w1) = fixwp.partial_solver2(g, lam)  # fixwp version 2 call
                        else:
                            (w0, w1) = fixwp.partial_solver(g, lam)  # fixwp call
                temp.append(chrono.interval)  # add time recording

            min_recording = min(temp)
            total_time += min_recording
            percent_solved = ((float(len(w0)) + len(w1)) /(i*5)) * 100
            #checking if completely solved
            if percent_solved != 100:
                not_comp_solved.append((g, w0, w1))

            y_temp.append(min_recording)  # get the minimum out of #iterations recordings
            n_temp.append(5 * i)
            per_sol_temp.append(percent_solved)

            if prt:
                print "Worst-case graph".center(40) + "|" + str(i * 5).center(12) + "|" \
                + str(y_temp[nbr_generated]).center(40) + "|" + str(percent_solved).center(19) + "|" + "\n" + "-" * 115

            nbr_generated += 1  # updating the number of generated mesures

        y.append(y_temp)
        n_.append(n_temp)
        per_sol.append(per_sol_temp)

    # at the end, print total time
    if prt:
        print "-" * 115 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
        str(total_time).center(40) + "|" + "\n" + "-" * 115 + "\n"

    if plot:
        i = 0
        for lam in range(start_lambda, end_lambda + 1, step_lambda):
            fig, ax1 = plt.subplots()
            plt.grid(True)
            plt.title(u"Graphes pires cas de taille 1 à " + str(5*n) + " avec lambda = " + str(lam))
            plt.xlabel(u'nombre de nœuds')
            # plt.yscale("log") allows logatithmic y-axis
            ax1.plot(n_[i], y[i], 'g.', label=u"Temps d'exécution", color='b')
            ax1.tick_params('y', colors='b')
            ax1.set_ylabel("Temps d'execution (s)", color = 'b')

            ax2 = ax1.twinx()
            ax2.plot(n_[i], per_sol[i], 'g.', label=u"Pourcentage résolu", color='r')
            ax2.set_ylim([0, 101])
            ax2.set_ylabel("Pourcentage du jeu resolu (%)", color = 'r')
            ax2.tick_params('y', colors='r')
            fig.tight_layout()

            plt.savefig(path+str(lam)+".png", bbox_inches='tight')
            plt.clf()
            plt.close()
            i = i + 1

    #save the percent solve for each player for each lambda for each size of game in a txt file
    if save_res:
        i = 0
        for lam in range(start_lambda, end_lambda + 1, step_lambda):
            #computing the percent solved for each player for the games not solved completely
            part_solv = 0
            comp_solv = 0
            percent_solv = []
            for (g, w0, w1) in not_comp_solved:
                #one more game not solved completely
                part_solv += 1
                #checking is the solutions are included to the true solutions. Computing the true sols with Zielonka algorithm
                (sp_w0, sp_w1) = sp(g)
                a =  all(s in sp_w1 for s in w1) #cheking if included
                b =  all(s in sp_w0 for s in w0) #cheking if included
                #if not included stop the algorithm 
                if not a or not b:
                    print "Error the solutions found are not included to the true solutions"
                    return -1
                #total percentage solved
                percent_solved_total = ((float(len(w0)) + len(w1)) /(len(sp_w0) + len(sp_w1))) * 100 
                #percentage solved for player 0
                if len(sp_w0) > 0:
                    percent_solved_0 = (float(len(w0)) /len(sp_w0)) * 100
                else:
                    percent_solved_0 = 100
                #percentage solved for player 1
                if len(sp_w1) > 0:
                    percent_solved_1 = (float(len(w1)) /len(sp_w1)) * 100
                else:
                    percent_solved_1 = 100
                #adding the percentages computed to the list + the size of the game
                percent_solv.append((len(g.get_nodes()), percent_solved_total, percent_solved_0, percent_solved_1))
    
            comp_solv += 5*n/step - len(not_comp_solved)

            io.write_benchmark_partial_solver(comp_solv, part_solv, percent_solv, path_res+"_"+str(lam)+".txt", n_[i], y[i], 5*n, 1, lam, False, "")


def benchmark_worst_case_wc(n, iterations=3, step=10, plot=False, path="", save_res = False, path_res = "", prt = True):
    """
    Benchmarks the window parity algorithms for strong parity games using the random game generator.
    Calls window parity partial solver on games generated using the random game generator function.
    Games of size 1 to n are solved and a timer records the time taken to get the solution.The solver can be timed
    several times and the minimum value is selected using optional parameter iterations (to avoid recording time
    spikes and delays due to system load). The result can be plotted using matplotlib.
    :param n: number of nodes in generated graph (nodes is n due to construction).
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    :param save_res: if True, save the results on a file.
    :param path_res: path to the file in which to write the result.
    :param prt: True if the prints are activated.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values (5 to 5n)
    per_sol = [] # list for the percentage of the game solved

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    not_comp_solved = [] #store the game that are not completely solved

    # print first line of output
    if prt:
        print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "|" + "Percentage solved".center(19) + "|" + "\n" + \
            "-" * 115

    # games generated are size 1 to 5*n
    for i in range(1, n + 1, step):
        temp = []  # temp list for #iterations recordings
        g = generators.strong_parity_worst_case(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                (w0, w1) = winningcore.partial_solver(g)  # winning core call
            temp.append(chrono.interval)  # add time recording

        min_recording = min(temp)
        total_time += min_recording
        percent_solved = ((float(len(w0)) + len(w1)) /(i*5)) * 100
        #checking if completely solved
        if percent_solved != 100:
            not_comp_solved.append((g, w0, w1))

        y.append(min_recording)  # get the minimum out of #iterations recordings
        n_.append(5 * i)
        per_sol.append(percent_solved)

        if prt:
            print "Worst-case graph".center(40) + "|" + str(i * 5).center(12) + "|" \
            + str(y[nbr_generated]).center(40) + "|" + str(percent_solved).center(19) + "|" + "\n" + "-" * 115

        nbr_generated += 1  # updating the number of generated mesures

    # at the end, print total time
    if prt:
        print "-" * 115 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
        str(total_time).center(40) + "|" + "\n" + "-" * 115 + "\n"

    if plot:
        i = 0
        fig, ax1 = plt.subplots()
        plt.grid(True)
        plt.title(u"Graphes pires cas de taille 1 à " + str(5*n))
        plt.xlabel(u'nombre de nœuds')
        # plt.yscale("log") allows logatithmic y-axis
        ax1.plot(n_, y, 'g.', label=u"Temps d'exécution", color='b')
        ax1.tick_params('y', colors='b')
        ax1.set_ylabel("Temps d'execution (s)", color = 'b')

        ax2 = ax1.twinx()
        ax2.plot(n_, per_sol, 'g.', label=u"Pourcentage résolu", color='r')
        ax2.set_ylim([0, 101])
        ax2.set_ylabel("Pourcentage du jeu resolu (%)", color = 'r')
        ax2.tick_params('y', colors='r')
        fig.tight_layout()

        plt.savefig(path+".png", bbox_inches='tight')
        plt.clf()
        plt.close()
        i = i + 1

    #save the percent solve for each player for each lambda for each size of game in a txt
    if save_res:
        #computing the percent solved for each player for the games not solved completely
        part_solv = 0
        comp_solv = 0
        percent_solv = []
        for (g, w0, w1) in not_comp_solved:
            #one more game not solved completely
            part_solv += 1
            #checking is the solutions are included to the true solutions. Computing the true sols with Zielonka algorithm
            (sp_w0, sp_w1) = sp(g)
            a =  all(s in sp_w1 for s in w1) #cheking if included
            b =  all(s in sp_w0 for s in w0) #cheking if included
            #if not included stop the algorithm 
            if not a or not b:
                print "Error the solutions found are not included to the true solutions"
                return -1
            #total percentage solved
            percent_solved_total = ((float(len(w0)) + len(w1)) /(len(sp_w0) + len(sp_w1))) * 100 
            #percentage solved for player 0
            if len(sp_w0) > 0:
                percent_solved_0 = (float(len(w0)) /len(sp_w0)) * 100
            else:
                percent_solved_0 = 100
            #percentage solved for player 1
            if len(sp_w1) > 0:
                percent_solved_1 = (float(len(w1)) /len(sp_w1)) * 100
            else:
                percent_solved_1 = 100
            #adding the percentages computed to the list + the size of the game
            percent_solv.append((len(g.get_nodes()), percent_solved_total, percent_solved_0, percent_solved_1))

        comp_solv += 5*n/step - len(not_comp_solved)

        io.write_benchmark_partial_solver(comp_solv, part_solv, percent_solv, path_res+".txt", n_, y, 5*n, 1, -1, False, "")

def benchmark_ladder_wp(n, start_lambda = 1, end_lambda = 10, step_lambda = 1, dir = True, v2 = False, iterations=3, step=10, plot=False, path="", save_res = False, path_res = "", prt = True):
    """
    Benchmarks the window parity algorithms for strong parity games using the random game generator.
    Calls window parity partial solver on games generated using the random game generator function.
    Games of size 1 to n are solved and a timer records the time taken to get the solution.The solver can be timed
    several times and the minimum value is selected using optional parameter iterations (to avoid recording time
    spikes and delays due to system load). The result can be plotted using matplotlib.
    :param n: number of nodes in generated graph (nodes is n due to construction).
    :param end_lambda: maximum value of lambda.
    :param start_lambda: starting value of lambda.
    :param step_lambda: step to be taken between the different value of lambda.
    :param dir: if True, uses DirFixWP if not, uses FixWP.
    :param v2: if True, uses partial_solver2. If False, uses partial_solver.
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    :param save_res: if True, save the results on a file.
    :param path_res: path to the file in which to write the result.
    :param prt: True if the prints are activated.
    :return: Percentage of game solved, size of the games such that we return the time taken to resolve those games.
    """
    y = []  # list for the time recordings
    n_ = []  # list for the x values (1 to n)
    per_sol = [] # list for the percentage of the game solved

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    lam = start_lambda #current lambda used by the algorithme

    not_comp_solved = [] #store the game that are not completely solved

    # print first line of output
    if prt:
        print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "|" + "Percentage solved".center(19) + "|" + "\n" + \
          "-" * 115

    #for each value of lambda
    for lam in range(start_lambda, end_lambda + 1, step_lambda):
        #print current value of lambda
        if prt:
            print "lambda value : ".center(40) + str(lam) + "\n" + "-" * 115
        y_temp = [] # stores time recordings for the current value of lambda
        n_temp = [] # stores the size of the game for the current value of lambda 
        per_sol_temp = [] #stores the resolution percentage of the games for the current value of lambda
        nbr_generated = 0
        # games generated are size 1 to n
        for i in range(1, n + 1, step):
            temp = []  # temp list for #iterations recordings
            g = generators.ladder(i)  # generated game

            # #iterations calls to the solver are timed
            for j in range(iterations):
                with chrono:
                    if dir:
                        if v2:
                            (w0, w1) = dirfixwp.partial_solver2(g, lam)  # dirfixwp version 2 call
                        else:
                            (w0, w1) = dirfixwp.partial_solver(g, lam)  # dirfixwp call
                    else:
                        if v2:
                            (w0, w1) = fixwp.partial_solver2(g, lam)  # fixwp version 2 call
                        else:
                            (w0, w1) = fixwp.partial_solver(g, lam)  # fixwp call
                temp.append(chrono.interval)  # add time recording

            min_recording = min(temp)
            percent_solved = ((len(w0) + len(w1)) /(2*i)) * 100
            if percent_solved != 100:
                not_comp_solved.append((g, w0, w1))
            y_temp.append(min_recording)  # get the minimum out of #iterations recordings
            n_temp.append(i)
            per_sol_temp.append(percent_solved)
            total_time += min_recording
            

            if prt:
                print "Ladder graph".center(40) + "|" + str(i).center(12) + "|" \
                + str(y_temp[nbr_generated]).center(40) + "|" + str(percent_solved).center(19) + "|" + "\n" + "-" * 115

            nbr_generated += 1  # updating the number of generated mesures
        y.append(y_temp)
        n_.append(n_temp)
        per_sol.append(per_sol_temp)


    # at the end, print total time
    if prt:
        print "-" * 115 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
          str(total_time).center(40) + "|" + "\n" + "-" * 115 + "\n"

    if plot:
        i = 0
        for lam in range(start_lambda, end_lambda + 1, step_lambda):
            fig, ax1 = plt.subplots()
            plt.grid(True)
            plt.title(u"Graphes Ladder de taille 1 à " + str(n) + " avec lambda = " + str(lam))
            plt.xlabel(u'nombre de nœuds')
            # plt.yscale("log") allows logatithmic y-axis
            ax1.plot(n_[i], y[i], 'g.', label=u"Temps d'exécution", color='b')
            ax1.tick_params('y', colors='b')
            ax1.set_ylabel("Temps d'execution (s)", color = 'b')

            ax2 = ax1.twinx()
            ax2.plot(n_[i], per_sol[i], 'g.', label=u"Pourcentage résolu", color='r')
            ax2.set_ylim([0, 101])
            ax2.set_ylabel("Pourcentage du jeu resolu (%)", color = 'r')
            ax2.tick_params('y', colors='r')
            fig.tight_layout()

            plt.savefig(path+str(lam)+".png", bbox_inches='tight')
            plt.clf()
            plt.close()
            i = i + 1

    #save the percent solve for each player for each lambda for each size of game in a txt
    if save_res:
        i = 0
        for lam in range(start_lambda, end_lambda + 1, step_lambda):
            #computing the percent solved for each player for the games not solved completely
            part_solv = 0
            comp_solv = 0
            percent_solv = []
            for (g, w0, w1) in not_comp_solved:
                #one more game not solved completely
                part_solv += 1
                #checking is the solutions are included to the true solutions. Computing the true sols with Zielonka algorithm
                (sp_w0, sp_w1) = sp(g)
                a =  all(s in sp_w1 for s in w1) #cheking if included
                b =  all(s in sp_w0 for s in w0) #cheking if included
                #if not included stop the algorithm 
                if not a or not b:
                    print "Error the solutions found are not included to the true solutions"
                    return -1
                #total percentage solved
                percent_solved_total = ((float(len(w0)) + len(w1)) /(len(sp_w0) + len(sp_w1))) * 100 
                #percentage solved for player 0
                if len(sp_w0) > 0:
                    percent_solved_0 = (float(len(w0)) /len(sp_w0)) * 100
                else:
                    percent_solved_0 = 100
                #percentage solved for player 1
                if len(sp_w1) > 0:
                    percent_solved_1 = (float(len(w1)) /len(sp_w1)) * 100
                else:
                    percent_solved_1 = 100
                #adding the percentages computed to the list + the size of the game
                percent_solv.append((len(g.get_nodes()), percent_solved_total, percent_solved_0, percent_solved_1))
    
            comp_solv += n/step - len(not_comp_solved)

            io.write_benchmark_partial_solver(comp_solv, part_solv, percent_solv, path_res+"_"+str(lam)+".txt", n_[i], y[i], n, 1, lam, False, "")

def benchmark_ladder_wc(n, iterations=3, step=10, plot=False, path="", save_res = False, path_res = "", prt = True):
    """
    Benchmarks the window parity algorithms for strong parity games using the random game generator.
    Calls window parity partial solver on games generated using the random game generator function.
    Games of size 1 to n are solved and a timer records the time taken to get the solution.The solver can be timed
    several times and the minimum value is selected using optional parameter iterations (to avoid recording time
    spikes and delays due to system load). The result can be plotted using matplotlib.
    :param n: number of nodes in generated graph (nodes is n due to construction).
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    :param save_res: if True, save the results on a file.
    :param path_res: path to the file in which to write the result.
    :param prt: True if the prints are activated.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values (1 to n)
    per_sol = [] # list for the percentage of the game solved

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    not_comp_solved = [] #store the game that are not completely solved

    # print first line of output
    if prt:
        print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "|" + "Percentage solved".center(19) + "|" + "\n" + \
            "-" * 115

    # games generated are size 1 to n
    for i in range(1, n + 1, step):
        temp = []  # temp list for #iterations recordings
        g = generators.ladder(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                (w0, w1) = winningcore.partial_solver(g)  # winning core call
            temp.append(chrono.interval)  # add time recording

        min_recording = min(temp)
        percent_solved = ((float(len(w0)) + len(w1)) /(i)) * 100
        if percent_solved != 100:
            not_comp_solved.append((g, w0, w1))

        y.append(min_recording)  # get the minimum out of #iterations recordings
        n_.append(i)
        per_sol.append(percent_solved)
        total_time += min_recording
        

        if prt:
            print "Ladder graph".center(40) + "|" + str(i).center(12) + "|" \
            + str(y[nbr_generated]).center(40) + "|" + str(percent_solved).center(19) + "|" + "\n" + "-" * 115

        nbr_generated += 1  # updating the number of generated mesures


    # at the end, print total time
    if prt:
        print "-" * 115 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
            str(total_time).center(40) + "|" + "\n" + "-" * 115 + "\n"

    if plot:
        fig, ax1 = plt.subplots()
        plt.grid(True)
        plt.title(u"Graphes Ladder de taille 1 à " + str(n))
        plt.xlabel(u'nombre de nœuds')
        # plt.yscale("log") allows logatithmic y-axis
        ax1.plot(n_, y, 'g.', label=u"Temps d'exécution", color='b')
        ax1.tick_params('y', colors='b')
        ax1.set_ylabel("Temps d'execution (s)", color = 'b')

        ax2 = ax1.twinx()
        ax2.plot(n_, per_sol, 'g.', label=u"Pourcentage résolu", color='r')
        ax2.set_ylim([0, 101])
        ax2.set_ylabel("Pourcentage du jeu resolu (%)", color = 'r')
        ax2.tick_params('y', colors='r')
        fig.tight_layout()

        plt.savefig(path+".png", bbox_inches='tight')
        plt.clf()
        plt.close()

    if save_res:
        #computing the percent solved for each player for the games not solved completely
        part_solv = 0
        comp_solv = 0
        percent_solv = []
        for (g, w0, w1) in not_comp_solved:
            #one more game not solved completely
            part_solv += 1
            #checking is the solutions are included to the true solutions. Computing the true sols with Zielonka algorithm
            (sp_w0, sp_w1) = sp(g)
            a =  all(s in sp_w1 for s in w1) #cheking if included
            b =  all(s in sp_w0 for s in w0) #cheking if included
            #if not included stop the algorithm 
            if not a or not b:
                print "Error the solutions found are not included to the true solutions"
                return -1
            #total percentage solved
            percent_solved_total = ((float(len(w0)) + len(w1)) /(len(sp_w0) + len(sp_w1))) * 100 
            #percentage solved for player 0
            if len(sp_w0) > 0:
                percent_solved_0 = (float(len(w0)) /len(sp_w0)) * 100
            else:
                percent_solved_0 = 100
            #percentage solved for player 1
            if len(sp_w1) > 0:
                percent_solved_1 = (float(len(w1)) /len(sp_w1)) * 100
            else:
                percent_solved_1 = 100
            #adding the percentages computed to the list + the size of the game
            percent_solv.append((len(g.get_nodes()), percent_solved_total, percent_solved_0, percent_solved_1))

        comp_solv += n/step - len(not_comp_solved)

        io.write_benchmark_partial_solver(comp_solv, part_solv, percent_solv, path_res+".txt", n_, y, n, 1, -1, False, "")