from random import shuffle

def generate():
    return SudokuGenerator().grid

class SudokuGenerator:
    """generates and solves Sudoku puzzles using a backtracking algorithm"""
    def __init__(self):
        self.grid = [[0 for i in range(9)] for j in range(9)]
        self.path = []
        self.generate_solution(self.grid)

    def num_used_in_row(self,grid,row,number):
        """returns True if the number has been used in that row"""
        if number in grid[row]:
            return True
        return False

    def num_used_in_column(self,grid,col,number):
        """returns True if the number has been used in that column"""
        for i in range(9):
            if grid[i][col] == number:
                return True
        return False

    def num_used_in_subgrid(self,grid,row,col,number):
        """returns True if the number has been used in that subgrid/box"""
        sub_row = (row // 3) * 3
        sub_col = (col // 3)  * 3
        for i in range(sub_row, (sub_row + 3)): 
            for j in range(sub_col, (sub_col + 3)): 
                if grid[i][j] == number: 
                    return True
        return False

    def valid_location(self,grid,row,col,number):
        """return False if the number has been used in the row, column or subgrid"""
        if self.num_used_in_row(grid, row,number):
            return False
        elif self.num_used_in_column(grid,col,number):
            return False
        elif self.num_used_in_subgrid(grid,row,col,number):
            return False
        return True

    def find_empty_square(self,grid):
        """return the next empty square coordinates in the grid"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i,j)
        return

    def generate_solution(self, grid):
        """generates a full solution with backtracking"""
        number_list = [1,2,3,4,5,6,7,8,9]
        for i in range(0,81):
            row=i//9
            col=i%9
            #find next empty cell
            if grid[row][col]==0:
                shuffle(number_list)      
                for number in number_list:
                    if self.valid_location(grid,row,col,number):
                        self.path.append((number,row,col))
                        grid[row][col]=number
                        if not self.find_empty_square(grid):
                            return True
                        else:
                            if self.generate_solution(grid):
                                #if the grid is full
                                return True
                break
        grid[row][col]=0  
        return False