# Game solver
Python 2.7 implementation of reachability/safety games solver as well as weak parity and strong parity games solver.
The algorithm implemented for solving parity games is the recursive algorithm proposed by Zielonka. Reachability games are solved thanks to an algorithm using a predecessor list representation of the game graph. Weak parity games are solved using a linear time algorithm proposed by Chatterjee in https://arxiv.org/pdf/0805.1391.pdf.

A tool created by Clément Tamines, master student, University of Mons and forked by Dorian Labeeuw, master student, University of Mons.

## Description
This tool allows the user to input a game graph in the PGSolver file format (https://github.com/tcsprojects/pgsolver), choose an objective (reachability, weak parity or strong parity) and solve the corresponding game. The tool yields the winning region and winning strategy for both players in the command line or as a .dot file. For the strong parity objectives it is possible to solve partially the corresponding game. The report associated to this project and explaining in details the algorithms implemented can be found at [link] (in french). 

Several benchmarks have been implemented in order to test the implementations.

## Structure
The source code of the project can be found in src/be/ac/umons

    .
    ├── solver.py   #Console user interface (allowing to solve a game or test performances)
    ├── graph.py    #Game graph implementation
    ├── solvers     #Solving algorithms implementation for reachability, weak parity and strong parity games
    ├── benchmarks  #Benchmarking functions used for performance testing
    ├── operations  #Several general-purpose functions (file handling, benchmark generation, etc.)
    └── test        #Tests

## How to run
Note : players are called player 0 and player 1

* To show the help dialog :
`solver.py -h`

* To solve a reachability game : 
`solver.py -r PLAYER TARGET_SET solve -i INPUTFILE [-o OUTPUTFILE]`

    Example for player 0 and target set 1,2: `solver.py solve -r 0 1,2 -i assets/reachability/figure32.txt` will yield    

    Winning region of player 0 : [1, 2, 3, 5]  
    Winning strategy of player 0 :  
    1 -> 1   
    2 -> 1  
    5 -> 2  
    Winning region of player 1 : [4, 6]  
    Winning strategy of player 1 :  
    4 -> 6  
    6 -> 4  

* To solve a weak parity game :
`solver.py -wp solve -i INPUTFILE [-o OUTPUTFILE]`

* To solve a strong parity game :
`solver.py -sp solve -i INPUTFILE [-o OUTPUTFILE]`

* To solve a strong parity game with a partial solver :
`solver.py solve -wc -i INPUTFILE [-o OUTPUTFILE]`
`solver.py solve -winpar ALGO LAMBDA VERSION2 -i INPUTFILE [-o OUTPUTFILE]`

    Example for the algo DirFixWP version 2 with lambda = 1:`solver.py solve -winpar dirfixwp 1 True -i "assets/strong parity/example_1.txt"` will yield

    Winning region of player 0 : [2, 1, 3]
    Winning region of player 1 : []