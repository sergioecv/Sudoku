import numpy as np

# grid = [[5, 3, 4, 0, 7, 0, 0, 0, 0],
#         [6, 0, 0, 1, 9, 5, 0, 0, 0],
#         [0, 9, 8, 0, 0, 0, 0, 6, 0],
#         [8, 0, 0, 0, 6, 0, 0 ,0 ,3],
#         [4, 0, 0, 8, 0, 3, 0, 0, 1],
#         [7, 0, 0, 0, 2, 0, 0, 0, 6],
#         [0, 6, 0, 0, 0, 0, 2, 8, 0],
#         [0, 0, 0, 4, 1, 9, 0, 0, 5],
#         [0, 0, 0, 0, 8, 0, 0, 7, 9]]

solution = 0

#Method that checks if the value is valid for the grid
def possible(y, x, n, grid):
    for i in range(9):
        if grid[y][i] == n or grid[i][x] == n:
            return False
    xi = (x//3)*3
    yi = (y//3)*3
    for i in range(3):
        for j in range(3):
            if grid[yi+i][xi+j] == n:
                return False
    return True

#Method that solves the sudoku with 'possible' method
def solve(grid1):
    global solution
    #global grid
    for y in range(9):
        for x in range(9):
            if grid1[y][x] == 0:
                for n in range(9,0,-1):
                    if possible(y,x,n,grid1):
                        grid1[y][x] = n
                        solve(grid1)
                        grid1[y][x] = 0

                return False
    solution += 1
    #print(np.matrix(grid1))
    return True

#Checks if there is a possible solution with 
def possibleSolution(grid1):
    global solution
    solve(grid1)
    if solution == 1:
        solution = 0
        return True
    else:
        solution = 0
        return False

#def main():
    # print("Main")
    # print(possibleSolution(grid))

#main()
