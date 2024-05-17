from generator.kenken_generator.kenken_generator import generate
from solver.solver import Puzzle, solve

from random import choice


def generatePuzzle(min_suggestions, max_suggestions, operations):
    size, cliques, board, cliques_solver = generate(
        9, operations, is_also_sudoku=True)
    puzzle = Puzzle(size, cliques_solver)
    sols = solve(puzzle, exhaustive=True)
    possible_assignements = {}
    for new_digit_cell in board.keys():
        new_digit = board[new_digit_cell]
        cell = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'[new_digit_cell[0] - 1] + str(
                new_digit_cell[1])
        possible_assignements[new_digit_cell] = [cell, str(new_digit)]
    assignements = []
    other_assignements = {}
    for i in range(min_suggestions):
        new_assignement = choice(list(possible_assignements.keys()))
        assignements.append(possible_assignements.pop(new_assignement))
        other_assignements[new_assignement] = board[new_assignement]
    while len(sols) > 1 and len(assignements) < max_suggestions:
        new_assignement = choice(list(possible_assignements.keys()))
        assignements.append(possible_assignements.pop(new_assignement))
        other_assignements[new_assignement] = board[new_assignement]
        sols = solve(puzzle, exhaustive=True, assignements=assignements)
    if (not min_suggestions <= len(other_assignements) <= max_suggestions) or len(sols) > 1:
        return generatePuzzle(min_suggestions, max_suggestions, operations)
    return [cliques, other_assignements], board


def generatePuzzles(
        nb_puzzles,
        min_suggestions,
        max_suggestions,
        operations,
        notifyPuzzleCreated):
    puzzles = []
    solutions = []
    for i in range(nb_puzzles):
        gen_puzzle = generatePuzzle(
            min_suggestions, max_suggestions, operations)
        puzzles.append(
            gen_puzzle[0])
        solutions.append(
            gen_puzzle[1])
        notifyPuzzleCreated()
    return puzzles, solutions