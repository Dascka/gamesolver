from tools import file_handler as io
from solvers.partialsolvers import winningcore
from solvers.partialsolvers import fixwp
from solvers.partialsolvers import dirfixwp
from solvers.strongparity import strong_parity_solver_no_strategies as sp
from tools import operations as ops

"""
Test module for the partial solvers for strong parity games.
Some examples are solved by our algorithms and we verify the solution. 
"""

"""
Winning Core
All responses to the examples below are calculated manualy to check if the solver is working.
This include manually checking if the "partial solutions" are included in the "full solutions".
"""
def wc_example1():
    g = io.load_from_file("assets/strong parity/example_1.txt") 
    (w0, w1) = winningcore.partial_solver(g)
    return ops.are_lists_equal(w0,[1,2,3]) and ops.are_lists_equal(w1,[])

def wc_example2():
    g = io.load_from_file("assets/strong parity/example_2.txt") 
    (w0, w1) = winningcore.partial_solver(g)
    return ops.are_lists_equal(w0 , [1,2,3,4]) and ops.are_lists_equal(w1 , [])

def wc_example3():
    g = io.load_from_file("assets/strong parity/example_3.txt") 
    (w0, w1) = winningcore.partial_solver(g)
    return ops.are_lists_equal(w0 , [1,2,3,4]) and ops.are_lists_equal(w1 , [5,6,7])

def wc_example4():
    g = io.load_from_file("assets/strong parity/example_4.txt") 
    (w0, w1) = winningcore.partial_solver(g)
    return ops.are_lists_equal(w0 , [1,2,5]) and ops.are_lists_equal(w1 , [3,4,6])

def wc_example5():
    g = io.load_from_file("assets/strong parity/example_5.txt") 
    (w0, w1) = winningcore.partial_solver(g)
    return ops.are_lists_equal(w0 , [1,2,5]) and ops.are_lists_equal(w1 , [3,4,6,7])


def wc_example6():
    g = io.load_from_file("assets/strong parity/example_6.txt") 
    (w0, w1) = winningcore.partial_solver(g)
    return ops.are_lists_equal(w0 , []) and ops.are_lists_equal(w1 , [1, 2, 3, 4, 5])

def wc_example7():
    g = io.load_from_file("assets/strong parity/example_7.txt") 
    (w0, w1) = winningcore.partial_solver(g)
    return ops.are_lists_equal(w0 , []) and ops.are_lists_equal(w1 , [1])

def wc_example8():
    #Figure 3.2.7
    g = io.load_from_file("assets/strong parity/example_8.txt") 
    (w0, w1) = winningcore.partial_solver(g)
    return ops.are_lists_equal(w0 , []) and ops.are_lists_equal(w1 , [])

def wc_example9():
    #Figure 2.2.2
    g = io.load_from_file("assets/strong parity/example_9.txt") 
    (w0, w1) = winningcore.partial_solver(g)
    return ops.are_lists_equal(w0 , [1, 2, 3]) and ops.are_lists_equal(w1 , [])

"""
DirFixWP (1)
All responses to the examples below are calculated manualy to check if the solver is working.
This include manually checking if the "partial solutions" are included in the "full solutions".
"""

def dirfixwp_example1():
    g = io.load_from_file("assets/strong parity/example_1.txt") 
    (w0, w1) = dirfixwp.partial_solver(g, 1) #full solve with lambda >= 1
    return ops.are_lists_equal(w0 , [1,2,3]) and ops.are_lists_equal(w1 , [])

def dirfixwp_example2():
    g = io.load_from_file("assets/strong parity/example_2.txt") 
    (w0, w1) = dirfixwp.partial_solver(g, 1) #full solve with lambda >= 1
    return ops.are_lists_equal(w0 , [1,2,3,4]) and ops.are_lists_equal(w1 , [])

def dirfixwp_example3():
    g = io.load_from_file("assets/strong parity/example_3.txt") 
    (w0, w1) = dirfixwp.partial_solver(g, 1) #partial solve with lambda = 1
    (w0_2, w1_2) = dirfixwp.partial_solver(g, 2) #full solve with lambda >= 2
    return ops.are_lists_equal(w0 , [1,2,4]) and ops.are_lists_equal(w1 , [5,6,7]) and ops.are_lists_equal(w0_2 , [1,2,3,4]) and ops.are_lists_equal(w1_2 , [5,6,7])

def dirfixwp_example4():
    g = io.load_from_file("assets/strong parity/example_4.txt") 
    (w0, w1) = dirfixwp.partial_solver(g, 1) #partial solve with lambda = 1
    (w0_2, w1_2) = dirfixwp.partial_solver(g, 100) #not able to solve more even with a greater lambda
    return ops.are_lists_equal(w0 , [1,2,5]) and ops.are_lists_equal(w1 , [3,6]) and ops.are_lists_equal(w0_2 , [1,2,5]) and ops.are_lists_equal(w1_2 , [3,6])

def dirfixwp_example5():
    g = io.load_from_file("assets/strong parity/example_5.txt") 
    (w0, w1) = dirfixwp.partial_solver(g,1) #partial solve with lambda = 1
    (w0_2, w1_2) = dirfixwp.partial_solver(g, 100) #not able to solve more even with a greater lambda
    return ops.are_lists_equal(w0 , [1,2,5]) and ops.are_lists_equal(w1 , [3,6]) and ops.are_lists_equal(w0_2 , [1,2,5]) and ops.are_lists_equal(w1_2 , [3,6])

def dirfixwp_example6():
    g = io.load_from_file("assets/strong parity/example_6.txt") 
    (w0, w1) = dirfixwp.partial_solver(g,1) #no solutions with lambda = 1
    (w0_2, w1_2) = dirfixwp.partial_solver(g, 2) #no solutions with lambda = 2
    (w0_3, w1_3) = dirfixwp.partial_solver(g,3) #no solutions with lambda = 3
    (w0_4, w1_4) = dirfixwp.partial_solver(g, 4) #full solve with lambda >= 4
    return ops.are_lists_equal(w0 , []) and ops.are_lists_equal(w1 , []) and ops.are_lists_equal(w0_2 , []) and ops.are_lists_equal(w1_2 , []) and ops.are_lists_equal(w0_3 , []) and ops.are_lists_equal(w1_3 , []) and ops.are_lists_equal(w0_4 , []) and ops.are_lists_equal(w1_4 , [1,2,3,4,5])

def dirfixwp_example7():
    g = io.load_from_file("assets/strong parity/example_7.txt") 
    (w0, w1) = dirfixwp.partial_solver(g, 1) #full solve with lambda >= 1
    return ops.are_lists_equal(w0 , []) and ops.are_lists_equal(w1 , [1])

def dirfixwp_example8():
    #Figure 3.2.7
    g = io.load_from_file("assets/strong parity/example_8.txt") 
    (w0, w1) = dirfixwp.partial_solver(g, 100) #no solutions with any lambda because the winner is player 0 but player 1 can manage to loop to prevent window from closing
    return ops.are_lists_equal(w0 , []) and ops.are_lists_equal(w1 , [])

def dirfixwp_example9():
    g = io.load_from_file("assets/strong parity/example_9.txt") 
    (w0, w1) = dirfixwp.partial_solver(g, 1) #full solve with lambda >= 1
    return ops.are_lists_equal(w0 , [1,2,3]) and ops.are_lists_equal(w1 , [])

"""
FixWP (1)
All responses to the examples below are calculated manualy to check if the solver is working.
This include manually checking if the "partial solutions" are included in the "full solutions".
"""

def fixwp_example1():
    g = io.load_from_file("assets/strong parity/example_1.txt") 
    (w0, w1) = fixwp.partial_solver(g, 1) #full solve with lambda >= 1
    return ops.are_lists_equal(w0 , [1,2,3]) and ops.are_lists_equal(w1 , [])

def fixwp_example2():
    g = io.load_from_file("assets/strong parity/example_2.txt") 
    (w0, w1) = fixwp.partial_solver(g, 1) #full solve with lambda >= 1
    return ops.are_lists_equal(w0 , [1,2,3,4]) and ops.are_lists_equal(w1 , [])

def fixwp_example3():
    g = io.load_from_file("assets/strong parity/example_3.txt") 
    (w0, w1) = fixwp.partial_solver(g, 1) #full solve with lambda >= 1
    return ops.are_lists_equal(w0 , [1,2,4]) and ops.are_lists_equal(w1 , [5,6,7])

def fixwp_example4():
    g = io.load_from_file("assets/strong parity/example_4.txt") 
    (w0, w1) = fixwp.partial_solver(g, 1) #full solve with lambda >= 1
    return ops.are_lists_equal(w0 , [1,2,5]) and ops.are_lists_equal(w1 , [3,6])

def fixwp_example5():
    g = io.load_from_file("assets/strong parity/example_5.txt") 
    (w0, w1) = fixwp.partial_solver(g,1) #full solve with lambda >= 1
    return ops.are_lists_equal(w0 , [1,2,5]) and ops.are_lists_equal(w1 , [3,6])

def fixwp_example6():
    g = io.load_from_file("assets/strong parity/example_6.txt") 
    (w0, w1) = fixwp.partial_solver(g,1) #no solutions with lambda = 1
    (w0_2, w1_2) = fixwp.partial_solver(g, 2) #no solutions with lambda = 2
    (w0_3, w1_3) = fixwp.partial_solver(g,3) #no solutions with lambda = 3
    (w0_4, w1_4) = fixwp.partial_solver(g, 4) #full solve with lambda >= 4
    return ops.are_lists_equal(w0 , []) and ops.are_lists_equal(w1 , []) and ops.are_lists_equal(w0_2 , []) and ops.are_lists_equal(w1_2 , []) and ops.are_lists_equal(w0_3 , []) and ops.are_lists_equal(w1_3 , []) and ops.are_lists_equal(w0_4 , []) and ops.are_lists_equal(w1_4 , [1,2,3,4,5])

def fixwp_example7():
    g = io.load_from_file("assets/strong parity/example_7.txt") 
    (w0, w1) = fixwp.partial_solver(g, 1) #full solve with lambda >= 1
    return ops.are_lists_equal(w0 , []) and ops.are_lists_equal(w1 , [1])

def fixwp_example8():
    #Figure 3.2.7
    g = io.load_from_file("assets/strong parity/example_8.txt") 
    (w0, w1) = fixwp.partial_solver(g, 10) #no solutions with any lambda because the winner is player 0 but player 1 can manage to loop to prevent window from closing
    return ops.are_lists_equal(w0 , []) and ops.are_lists_equal(w1 , [])

def fixwp_example9():
    g = io.load_from_file("assets/strong parity/example_9.txt") 
    (w0, w1) = fixwp.partial_solver(g, 1) #full solve with lambda >= 1
    return ops.are_lists_equal(w0 , [1,2,3]) and ops.are_lists_equal(w1 , [])

"""
DirFixWP (2) and FixWP (2)
Doing the two in one test series to avoid running two time the full solver for the same example.
Here we are checking if the response returned by the algorithms are included to the true responses
"""

def wp_2_example1():
    g = io.load_from_file("assets/strong parity/example_1.txt") 
    (dir_w0, dir_w1) = dirfixwp.partial_solver2(g, 1) 
    (ndir_w0, ndir_w1) = fixwp.partial_solver2(g, 1) 
    (w0, w1) = sp(g)
    #checking if the partial solutions are included in the true solutions
    dir_inc_0 = all(s in w0 for s in dir_w0)
    dir_inc_1 = all(s in w1 for s in dir_w1)
    ndir_inc_0 = all(s in w0 for s in ndir_w0)
    ndir_inc_1 = all(s in w1 for s in ndir_w1)
    return dir_inc_0 and dir_inc_1 and ndir_inc_0 and ndir_inc_1

def wp_2_example2():
    g = io.load_from_file("assets/strong parity/example_2.txt") 
    (dir_w0, dir_w1) = dirfixwp.partial_solver2(g, 1) 
    (ndir_w0, ndir_w1) = fixwp.partial_solver2(g, 1) 
    (w0, w1) = sp(g)
    dir_inc_0 = all(s in w0 for s in dir_w0)
    dir_inc_1 = all(s in w1 for s in dir_w1)
    ndir_inc_0 = all(s in w0 for s in ndir_w0)
    ndir_inc_1 = all(s in w1 for s in ndir_w1)
    return dir_inc_0 and dir_inc_1 and ndir_inc_0 and ndir_inc_1

def wp_2_example3():
    g = io.load_from_file("assets/strong parity/example_3.txt") 
    #better results with lambda = 2 on the basic algorithm
    (dir_w0, dir_w1) = dirfixwp.partial_solver2(g, 2) 
    (ndir_w0, ndir_w1) = fixwp.partial_solver2(g, 2) 
    (w0, w1) = sp(g)
    dir_inc_0 = all(s in w0 for s in dir_w0)
    dir_inc_1 = all(s in w1 for s in dir_w1)
    ndir_inc_0 = all(s in w0 for s in ndir_w0)
    ndir_inc_1 = all(s in w1 for s in ndir_w1)
    return dir_inc_0 and dir_inc_1 and ndir_inc_0 and ndir_inc_1

def wp_2_example4():
    g = io.load_from_file("assets/strong parity/example_4.txt") 
    (dir_w0, dir_w1) = dirfixwp.partial_solver2(g, 1) 
    (ndir_w0, ndir_w1) = fixwp.partial_solver2(g, 1) 
    (w0, w1) = sp(g)
    dir_inc_0 = all(s in w0 for s in dir_w0)
    dir_inc_1 = all(s in w1 for s in dir_w1)
    ndir_inc_0 = all(s in w0 for s in ndir_w0)
    ndir_inc_1 = all(s in w1 for s in ndir_w1)
    return dir_inc_0 and dir_inc_1 and ndir_inc_0 and ndir_inc_1

def wp_2_example5():
    g = io.load_from_file("assets/strong parity/example_5.txt") 
    (dir_w0, dir_w1) = dirfixwp.partial_solver2(g, 1) 
    (ndir_w0, ndir_w1) = fixwp.partial_solver2(g, 1) 
    (w0, w1) = sp(g)
    dir_inc_0 = all(s in w0 for s in dir_w0)
    dir_inc_1 = all(s in w1 for s in dir_w1)
    ndir_inc_0 = all(s in w0 for s in ndir_w0)
    ndir_inc_1 = all(s in w1 for s in ndir_w1)
    return dir_inc_0 and dir_inc_1 and ndir_inc_0 and ndir_inc_1

def wp_2_example6():
    g = io.load_from_file("assets/strong parity/example_6.txt") 
    #only winnable with lambda >=4
    (dir_w0, dir_w1) = dirfixwp.partial_solver2(g, 4) 
    (ndir_w0, ndir_w1) = fixwp.partial_solver2(g, 4) 
    (w0, w1) = sp(g)
    dir_inc_0 = all(s in w0 for s in dir_w0)
    dir_inc_1 = all(s in w1 for s in dir_w1)
    ndir_inc_0 = all(s in w0 for s in ndir_w0)
    ndir_inc_1 = all(s in w1 for s in ndir_w1)
    return dir_inc_0 and dir_inc_1 and ndir_inc_0 and ndir_inc_1

def wp_2_example7():
    g = io.load_from_file("assets/strong parity/example_7.txt") 
    (dir_w0, dir_w1) = dirfixwp.partial_solver2(g, 1) 
    (ndir_w0, ndir_w1) = fixwp.partial_solver2(g, 1) 
    (w0, w1) = sp(g)
    dir_inc_0 = all(s in w0 for s in dir_w0)
    dir_inc_1 = all(s in w1 for s in dir_w1)
    ndir_inc_0 = all(s in w0 for s in ndir_w0)
    ndir_inc_1 = all(s in w1 for s in ndir_w1)
    return dir_inc_0 and dir_inc_1 and ndir_inc_0 and ndir_inc_1

def wp_2_example8():
    #Figure 3.2.7
    g = io.load_from_file("assets/strong parity/example_8.txt") 
    (dir_w0, dir_w1) = dirfixwp.partial_solver2(g, 1) 
    (ndir_w0, ndir_w1) = fixwp.partial_solver2(g, 1) 
    (w0, w1) = sp(g)
    dir_inc_0 = all(s in w0 for s in dir_w0)
    dir_inc_1 = all(s in w1 for s in dir_w1)
    ndir_inc_0 = all(s in w0 for s in ndir_w0)
    ndir_inc_1 = all(s in w1 for s in ndir_w1)
    return dir_inc_0 and dir_inc_1 and ndir_inc_0 and ndir_inc_1

def wp_2_example9():
    g = io.load_from_file("assets/strong parity/example_9.txt") 
    (dir_w0, dir_w1) = dirfixwp.partial_solver2(g, 1) 
    (ndir_w0, ndir_w1) = fixwp.partial_solver2(g, 1) 
    (w0, w1) = sp(g)
    dir_inc_0 = all(s in w0 for s in dir_w0)
    dir_inc_1 = all(s in w1 for s in dir_w1)
    ndir_inc_0 = all(s in w0 for s in ndir_w0)
    ndir_inc_1 = all(s in w1 for s in ndir_w1)
    return dir_inc_0 and dir_inc_1 and ndir_inc_0 and ndir_inc_1

def launch_tests():
    winningcore = wc_example1() and wc_example2() and wc_example3() and wc_example4() and wc_example5() and wc_example6() and wc_example7() and wc_example8() and wc_example9()

    dirfixwp = dirfixwp_example1() and dirfixwp_example2() and dirfixwp_example3() and dirfixwp_example4() and dirfixwp_example5() and dirfixwp_example6() and dirfixwp_example7() and dirfixwp_example8() and dirfixwp_example9()

    fixwp = fixwp_example1() and fixwp_example2() and fixwp_example3() and fixwp_example4() and fixwp_example5() and fixwp_example6() and fixwp_example7() and fixwp_example8() and fixwp_example9()

    wp2 = wp_2_example1() and wp_2_example2() and wp_2_example3() and wp_2_example4() and wp_2_example5() and wp_2_example6() and wp_2_example7() and wp_2_example8() and wp_2_example9()


    return winningcore and dirfixwp and fixwp and wp2