from puzzle import Puzzle

class KillerSudoku(Puzzle):

    def __init__(self) -> None:
        self.cliques: list[Clique] = []


class Clique:
    
    def __init__(self) -> None:
        self.cells: list[Cell] = []
        self.operation = None

    
class Cell:

    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
        self.value = None


class Operation:

    def calculate(values: "list[int]") -> int:
        pass


class Sum(Operation):

    def calculate(values: "list[int]") -> int:
        return sum(values)


class Difference(Operation):

    def calculate(values: "list[int]") -> int:
        if len(values) != 2:
            raise Exception(
                "Difference operation can only be applied to a list"
                "of two values"
            )
        return abs(values[0] - values[1])


class Division(Operation):

    def calculate(values: "list[int]") -> int:
        if len(values) != 2:
            raise Exception(
                "Difference operation can only be applied to a list"
                "of two values"
            )
        if values[1]%values[0] == 0:
            return values[1]//values[0]
        elif values[0]%values[1] == 0:
            return values[0]//values[1]
        else:
            raise Exception(
                "Division operation can only be applied to a list"
                "of two values where one is divisible by the other"
            )