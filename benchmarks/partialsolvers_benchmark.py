# coding=utf-8
from tools import timer, generators
from solvers.partialsolvers import fixwp, dirfixwp, winningcore
from random import randint
import matplotlib.pyplot as plt

def benchmark_random(n, start_lambda = 1, end_lambda = 10, step_lambda = 1, dir = True, iterations=3, step=10, plot=False, path=""):
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
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values (1 to n)
    per_sol = [] # list for the percentage of the game solved

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    lam = start_lambda #current lambda used by the algorithme

    # print first line of output
    print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "|" + "Percentage solved".center(19) + "|" + "\n" + \
          "-" * 115

    #for each value of lambda
    for lam in range(start_lambda, end_lambda + 1, step_lambda):
        #print current value of lambda
        print "lambda value : ".center(40) + str(lam) + "\n" + "-" * 115
        y_temp = []
        n_temp = []
        per_sol_temp = []
        nbr_generated = 0
        # games generated are size 1 to n
        for i in range(1, n + 1, step):
            temp = []  # temp list for #iterations recordings
            prio = randint(0, i)  # number of priorities
            min_out = randint(1, i)
            max_out = randint(min_out, i)
            g = generators.random(i, prio, min_out, max_out)  # generated game

            # #iterations calls to the solver are timed
            for j in range(iterations):
                with chrono:
                    if(dir):
                        (w0, w1) = dirfixwp.partial_solver(g, lam)  # dirfixwp call
                    else:
                        (w0, w1) = fixwp.partial_solver(g, lam)  # fixwp call
                temp.append(chrono.interval)  # add time recording

            min_recording = min(temp)
            percent_solved = ((len(w0) + len(w1)) /(i)) * 100
            y_temp.append(min_recording)  # get the minimum out of #iterations recordings
            n_temp.append(i)
            per_sol_temp.append(percent_solved)
            total_time += min_recording
            

            print "Random graph".center(40) + "|" + str(i).center(12) + "|" \
                + str(y_temp[nbr_generated]).center(40) + "|" + str(percent_solved).center(19) + "|" + "\n" + "-" * 115

            nbr_generated += 1  # updating the number of generated mesures
        y.append(y_temp)
        n_.append(n_temp)
        per_sol.append(per_sol_temp)


    # at the end, print total time
    print "-" * 115 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
          str(total_time).center(40) + "|" + "\n" + "-" * 115 + "\n"

    if plot:
        i = 0
        for lam in range(start_lambda, end_lambda + 1, step_lambda):
            fig, ax1 = plt.subplots()
            plt.grid(True)
            plt.title(u"Graphes complet de taille 1 à " + str(n) + " avec lambda = " + str(lam))
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

def benchmark_worst_case(n, iterations=3, step=10, plot=False, path=""):
    """
    Benchmarks the partial solvers algorithm for strong parity games using the worst case generator which yields an
    exponential complexity. Calls strong parity solver on games generated using the worst case generator function.
    Games of size 5 to 5*n are solved and a timer records the time taken to get the solution.The solver can be timed
    several times and the minimum value is selected using optional parameter iterations (to avoid recording time
    spikes and delays due to system load). The result can be plotted using matplotlib.
    :param n: number of nodes in generated graph (nodes is 5*n due to construction).
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values (5 to 5n)

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    # print first line of output
    print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "|" + "Percentage solved".center(19) + "|" + "\n" + \
          "-" * 115

    # games generated are size 1 to n
    for i in range(1, n + 1, step):
        temp = []  # temp list for #iterations recordings
        g = generators.strong_parity_worst_case(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                (w0, w1) = fixwp.partial_solver(g, 1)  # solver call
            temp.append(chrono.interval)  # add time recording

        min_recording = min(temp)
        y.append(min_recording)  # get the minimum out of #iterations recordings
        n_.append(5 * i)
        total_time += min_recording
        percent_solved = ((len(w0) + len(w1)) /(i*5)) * 100

        print "Worst-case graph".center(40) + "|" + str(i * 5).center(12) + "|" \
              + str(y[nbr_generated]).center(40) + "|" + str(percent_solved).center(19) + "|" + "\n" + "-" * 115

        nbr_generated += 1  # updating the number of generated mesures

        # at the end, print total time
    print "-" * 115 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
          str(total_time).center(40) + "|" + "\n" + "-" * 115 + "\n"

    if plot:
        plt.grid(True)
        plt.title(u"Graphes 'pire cas' de taille 5 à " + str(5 * n))
        plt.xlabel(u'nombre de nœuds')
        plt.ylabel(u'temps (s)')
        # plt.yscale("log") allows logatithmic y-axis
        points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
        plt.legend(loc='upper left', handles=[points])
        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()

def benchmark_complete_wp(n, start_lambda = 1, end_lambda = 10, step_lambda = 1, dir = True, iterations=3, step=10, plot=False, path=""):
    """
    Benchmarks the window parity algorithms for strong parity games using the complete game generator.
    Calls window parity partial solver on games generated using the complete game generator function.
    Games of size 1 to n are solved and a timer records the time taken to get the solution.The solver can be timed
    several times and the minimum value is selected using optional parameter iterations (to avoid recording time
    spikes and delays due to system load). The result can be plotted using matplotlib.
    :param n: number of nodes in generated graph (nodes is n due to construction).
    :param end_lambda: maximum value of lambda.
    :param start_lambda: starting value of lambda.
    :param step_lambda: step to be taken between the different value of lambda.
    :param dir: if True, uses DirFixWP if not, uses FixWP.
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values (1 to n)
    per_sol = [] # list for the percentage of the game solved

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    lam = start_lambda #current lambda used by the algorithme

    # print first line of output
    print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "|" + "Percentage solved".center(19) + "|" + "\n" + \
          "-" * 115

    #for each value of lambda
    for lam in range(start_lambda, end_lambda + 1, step_lambda):
        #print current value of lambda
        print "lambda value : ".center(40) + str(lam) + "\n" + "-" * 115
        y_temp = []
        n_temp = []
        per_sol_temp = []
        nbr_generated = 0
        # games generated are size 1 to n
        for i in range(1, n + 1, step):
            temp = []  # temp list for #iterations recordings
            g = generators.complete_graph(i)  # generated game

            # #iterations calls to the solver are timed
            for j in range(iterations):
                with chrono:
                    if(dir):
                        (w0, w1) = dirfixwp.partial_solver(g, lam)  # dirfixwp call
                    else:
                        (w0, w1) = fixwp.partial_solver(g, lam)  # fixwp call
                temp.append(chrono.interval)  # add time recording

            min_recording = min(temp)
            percent_solved = ((len(w0) + len(w1)) /(i)) * 100
            y_temp.append(min_recording)  # get the minimum out of #iterations recordings
            n_temp.append(i)
            per_sol_temp.append(percent_solved)
            total_time += min_recording
            

            print "Complete graph".center(40) + "|" + str(i).center(12) + "|" \
                + str(y_temp[nbr_generated]).center(40) + "|" + str(percent_solved).center(19) + "|" + "\n" + "-" * 115

            nbr_generated += 1  # updating the number of generated mesures
        y.append(y_temp)
        n_.append(n_temp)
        per_sol.append(per_sol_temp)


    # at the end, print total time
    print "-" * 115 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
          str(total_time).center(40) + "|" + "\n" + "-" * 115 + "\n"

    if plot:
        i = 0
        for lam in range(start_lambda, end_lambda + 1, step_lambda):
            fig, ax1 = plt.subplots()
            plt.grid(True)
            plt.title(u"Graphes complet de taille 1 à " + str(n) + " avec lambda = " + str(lam))
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

#Grande différence de temps entre DirFixWP et FixWP ici !!!!
def benchmark_ladder_wp(n, start_lambda = 1, end_lambda = 10, step_lambda = 1, dir = True, iterations=3, step=10, plot=False, path=""):
    """
    Benchmarks the recursive algorithm for strong parity games using the lader game generator which yields.
    Calls strong parity solver on games generated using the ladder game generator function.
    Games of size 1 to n are solved and a timer records the time taken to get the solution.The solver can be timed
    several times and the minimum value is selected using optional parameter iterations (to avoid recording time
    spikes and delays due to system load). The result can be plotted using matplotlib.
    :param n: number of nodes in generated graph (nodes is n due to construction).
    :param end_lambda: maximum value of lambda.
    :param start_lambda: starting value of lambda.
    :param step_lambda: step to be taken between the different value of lambda.
    :param dir: if True, uses DirFixWP if not, uses FixWP.
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values (1 to n)
    per_sol = [] # list for the percentage of the game solved

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    lam = start_lambda #current lambda used by the algorithme

    # print first line of output
    print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "|" + "Percentage solved".center(19) + "|" + "\n" + \
          "-" * 115

    #for each value of lambda
    for lam in range(start_lambda, end_lambda + 1, step_lambda):
        #print current value of lambda
        print "lambda value : ".center(40) + str(lam) + "\n" + "-" * 115
        y_temp = []
        n_temp = []
        per_sol_temp = []
        nbr_generated = 0
        # games generated are size 1 to n
        for i in range(1, n + 1, step):
            temp = []  # temp list for #iterations recordings
            g = generators.ladder(i)  # generated game

            # #iterations calls to the solver are timed
            for j in range(iterations):
                with chrono:
                    if(dir):
                        (w0, w1) = dirfixwp.partial_solver(g, lam)  # dirfixwp call
                    else:
                        (w0, w1) = fixwp.partial_solver(g, lam)  # fixwp call
                temp.append(chrono.interval)  # add time recording

            min_recording = min(temp)
            percent_solved = ((len(w0) + len(w1)) /(2*i)) * 100
            y_temp.append(min_recording)  # get the minimum out of #iterations recordings
            n_temp.append(i)
            per_sol_temp.append(percent_solved)
            total_time += min_recording
            

            print "Ladder graph".center(40) + "|" + str(i).center(12) + "|" \
                + str(y_temp[nbr_generated]).center(40) + "|" + str(percent_solved).center(19) + "|" + "\n" + "-" * 115

            nbr_generated += 1  # updating the number of generated mesures
        y.append(y_temp)
        n_.append(n_temp)
        per_sol.append(per_sol_temp)


    # at the end, print total time
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