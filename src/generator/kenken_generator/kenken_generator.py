
# @ reduce: determine the result of an operation
from functools import reduce

# @ random, shuffle, randint, choice: generate a random kenken puzzle
from random import random, randint, choice

from copy import deepcopy

from generator.sudoku_generator.sudoku_generator import (
    generate as generate_sudoku)

def operation(operator):
    """
    A utility function used in order to determine the operation corresponding
    to the operator that is given in string format
    """
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: abs(a - b)
    elif operator == '*':
        return lambda a, b: a * b
    elif operator == '/':
        return lambda a, b: a / b
    else:
        return None

def adjacent(xy1, xy2):
    """
    Checks wheither two positions represented in 2D coordinates are adjacent
    """
    x1, y1 = xy1
    x2, y2 = xy2

    dx, dy = x1 - x2, y1 - y2

    return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

def generate(size, operations, is_also_sudoku: bool = False):
    """
    Generate a random kenken puzzle of the given size
      * Initially create a latin square of size 'size' and elements the values [1...size]
      * Shuffle the board by rows and columns in order to get a somewhat random
        board that still satisfies the different row-col constraint of kenken
      * Initialize the 'uncaged' set with all cell coordinates
      * Proceed in creating cliques:
        * Randomly choose a clique size in the range [1..4]
        * Set the first cell in the 'uncaged' set in row major order as
          the root cell of the clique and remove it from the 'uncaged' set
        * Randomly visit at most 'clique-size' 'uncaged' adjacent cells
          in random directions while adding them to the current clique
          and removing them from the 'uncaged' cells
        * The size of the resulting clique is:
          * == 1:
            there is no operation to be performed and the target of the clique
            is equal to the only element of the clique
          * == 2:
            * if the two elements of the clique can be divided without a remainder
              then the operation is set to division and the target is the quotient
            * otherwise, the operation is set to subtraction and the target is the
              difference of the elements
          * >  2:
           randomly choose an operation between addition and multiplication.
            The target of the operation is the result of applying the decided
            operation on all the elements of the clique
        * Continue until the 'uncaged' set is empty i.e. there is no cell belonging
          to no clique
    """

    if is_also_sudoku:
        board = generate_sudoku()
    else:
        board = [[((i + j) % size) + 1 for i in range(size)] for j in range(size)]

        for c1 in range(size):
            for c2 in range(size):
                if random() > 0.5:
                    for r in range(size):
                        board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

    board = {(j + 1, i + 1): board[i][j] for i in range(size) for j in range(size)}

    uncaged = sorted(board.keys(), key=lambda var: var[1])

    operations_without_division = operations.copy()
    if '/' in operations_without_division:
        operations_without_division.remove('/')

    operations_for_all_cliques = operations.copy()
    if '/' in operations_for_all_cliques:
        operations_for_all_cliques.remove('/')
    if '-' in operations_for_all_cliques:
        operations_for_all_cliques.remove('-')

    cliques = []
    while uncaged:

        cliques.append([])

        csize = randint(2, 4)

        cell = uncaged[0]

        uncaged.remove(cell)

        cliques[-1].append(cell)

        for _ in range(csize - 1):

            adjs = [other for other in uncaged if adjacent(cell, other)]

            cell = choice(adjs) if adjs else None

            if not cell:
                break

            uncaged.remove(cell)
            
            cliques[-1].append(cell)
            
        csize = len(cliques[-1])
        if csize == 1:
            cell = cliques[-1][0]
            cliques[-1] = ((cell, ), '.', board[cell])
            continue
        elif csize == 2:
            fst, snd = cliques[-1][0], cliques[-1][1]
            if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                if '/' in operations:
                    operator = '/'
                else:
                    operator = choice(operations_without_division)
            else:
                if '-' in operations:
                    operator = '-'
                else:
                    operator = choice(operations_without_division)
        else:
            operator = choice(operations_for_all_cliques)

        target = reduce(operation(operator), [board[cell] for cell in cliques[-1]])

        cliques[-1] = (tuple(cliques[-1]), operator, int(target))

    def convertToSolverFormat(clique):
        letter_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        clique_solver = []
        clique_solver.append(clique[1])
        clique_solver.append(clique[2])
        for cell in clique[0]:
            clique_solver.append(letter_string[cell[0] - 1] + str(cell[1]))
        return clique_solver

    cliques_solver = [convertToSolverFormat(clique) for clique in cliques]

    return size, cliques, board, cliques_solver