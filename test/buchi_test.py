from tools import file_handler as io
from solvers import buchi
from tools import operations as ops

"""
Test module for the partial solvers for strong parity games.
Some examples are solved by our algorithms and we verify the solution. 
"""

def classic_buchi_example1():
    g = io.load_from_file("assets/buchi/example_1.txt") 
    w0_1 = buchi.basic_buchi(g, [1], 0) == []
    w1_1 = buchi.basic_buchi(g, [1], 1) == []
    w0_2 = buchi.basic_buchi(g, [2], 0) == [2,4]
    w1_2 = buchi.basic_buchi(g, [2], 1) == []
    w0_3 = buchi.basic_buchi(g, [3], 0) == []
    w1_3 = buchi.basic_buchi(g, [3], 1) == []
    w0_4 = buchi.basic_buchi(g, [4], 0) == [2,4]
    w1_4 = buchi.basic_buchi(g, [4], 1) == []
    w0_5 = buchi.basic_buchi(g, [5], 0) == []
    w1_5 = buchi.basic_buchi(g, [5], 1) == []
    w0_6 = buchi.basic_buchi(g, [6], 0) == [1,2,3,4,5,6]
    w1_6 = buchi.basic_buchi(g, [6], 1) == [1,3,5,6]

    return w0_1 and w1_1 and w0_2 and w1_2 and w0_3 and w1_3 and w0_4 and w1_4 and w0_5 and w1_5 and w0_6 and w1_6

def classic_buchi_example2():
    g = io.load_from_file("assets/buchi/example_2.txt") 
    w0_0 =buchi.basic_buchi(g, [0], 0) == []
    w1_0 =buchi.basic_buchi(g, [0], 1) == [0,1,2]
    w0_1 =buchi.basic_buchi(g, [1], 0) == [0,1,2,3]
    w1_1 =buchi.basic_buchi(g, [1], 1) == [0,1,2]
    w0_2 =buchi.basic_buchi(g, [2], 0) == []
    w1_2 =buchi.basic_buchi(g, [2], 1) == [0,1,2]
    w0_3 =buchi.basic_buchi(g, [3], 0) == []
    w1_3 =buchi.basic_buchi(g, [3], 1) == []
    w0_4 =buchi.basic_buchi(g, [4], 0) == [3,4,5,6,7]
    w1_4 =buchi.basic_buchi(g, [4], 1) == []
    w0_5 =buchi.basic_buchi(g, [5], 0) == [5,6,7]
    w1_5 =buchi.basic_buchi(g, [5], 1) == [4,5,6,7]
    w0_6 =buchi.basic_buchi(g, [6], 0) == [5,6,7]
    w1_6 =buchi.basic_buchi(g, [6], 1) == []
    w0_7 =buchi.basic_buchi(g, [7], 0) == [5,6,7]
    w1_7 =buchi.basic_buchi(g, [7], 1) == []
    w0_25 = buchi.basic_buchi(g, [2, 5], 0) == [5,6,7]
    w1_25 = buchi.basic_buchi(g, [2, 5], 1) == [0,1,2,3,4,5,6,7]

    return w0_0 and w1_0 and w0_1 and w1_1 and w0_2 and w1_2 and w0_3 and w1_3 and w0_4 and w1_4 and w0_5 and w1_5 and w0_6 and w1_6 and w0_7 and w1_7 and w0_25 and w1_25
    

def new_buchi_example1():
    g = io.load_from_file("assets/buchi/example_1.txt") 
    w0_1 = buchi.new_buchi(g, [1], 0) == []
    w1_1 = buchi.new_buchi(g, [1], 1) == []
    w0_2 = buchi.new_buchi(g, [2], 0) == [2,4]
    w1_2 = buchi.new_buchi(g, [2], 1) == []
    w0_3 = buchi.new_buchi(g, [3], 0) == []
    w1_3 = buchi.new_buchi(g, [3], 1) == []
    w0_4 = buchi.new_buchi(g, [4], 0) == [2,4]
    w1_4 = buchi.new_buchi(g, [4], 1) == []
    w0_5 = buchi.new_buchi(g, [5], 0) == []
    w1_5 = buchi.new_buchi(g, [5], 1) == []
    w0_6 = buchi.new_buchi(g, [6], 0) == [1,2,3,4,5,6]
    w1_6 = buchi.new_buchi(g, [6], 1) == [1,3,5,6]

    return w0_1 and w1_1 and w0_2 and w1_2 and w0_3 and w1_3 and w0_4 and w1_4 and w0_5 and w1_5 and w0_6 and w1_6

def new_buchi_example2():
    g = io.load_from_file("assets/buchi/example_2.txt") 
    w0_0 =buchi.new_buchi(g, [0], 0) == []
    w1_0 =buchi.new_buchi(g, [0], 1) == [0,1,2]
    w0_1 =buchi.new_buchi(g, [1], 0) == [0,1,2,3]
    w1_1 =buchi.new_buchi(g, [1], 1) == [0,1,2]
    w0_2 =buchi.new_buchi(g, [2], 0) == []
    w1_2 =buchi.new_buchi(g, [2], 1) == [0,1,2]
    w0_3 =buchi.new_buchi(g, [3], 0) == []
    w1_3 =buchi.new_buchi(g, [3], 1) == []
    w0_4 =buchi.new_buchi(g, [4], 0) == [3,4,5,6,7]
    w1_4 =buchi.new_buchi(g, [4], 1) == []
    w0_5 =buchi.new_buchi(g, [5], 0) == [5,6,7]
    w1_5 =buchi.new_buchi(g, [5], 1) == [4,5,6,7]
    w0_6 =buchi.new_buchi(g, [6], 0) == [5,6,7]
    w1_6 =buchi.new_buchi(g, [6], 1) == []
    w0_7 =buchi.new_buchi(g, [7], 0) == [5,6,7]
    w1_7 =buchi.new_buchi(g, [7], 1) == []

    w0_25 = buchi.new_buchi(g, [2, 5], 0) == [5,6,7]
    w1_25 = buchi.new_buchi(g, [2, 5], 1) == [0,1,2,3,4,5,6,7]

    return w0_0 and w1_0 and w0_1 and w1_1 and w0_2 and w1_2 and w0_3 and w1_3 and w0_4 and w1_4 and w0_5 and w1_5 and w0_6 and w1_6 and w0_7 and w1_7 and w0_25 and w1_25

def launch_tests():
    return classic_buchi_example1() and classic_buchi_example2() and new_buchi_example1() and new_buchi_example2()
