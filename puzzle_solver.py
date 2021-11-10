import numpy as np
import copy
import heapq
import itertools
import inspect

counter = itertools.count()

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def push(self, priority, item):
        heapq.heappush(self.elements, (priority, -next(counter), item))

    def get(self):
        return heapq.heappop(self.elements)[2]

class puzzle:
    def __init__(self, board, step_count):
        self.board = [board[:3], board[3:6], board[6::]]
        if len(board) == 0:
            self.add_starting_layout()
        self.goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.step_count = step_count
        self.total_cost = []
        self.parent_layout = []

    def add_starting_layout(self):
        """Accepts the player's initial puzzle layout if solvable"""

        #start = [1, 3, 6, 0, 4, 8, 5, 7, 2]
        start = [int(x) for x in input('Enter your desired starting layout as a list separated by space, starting from the upper left corner').split()]
        self.board = [start[:3], start[3:6], start[6::]]
        inversions = 0

        if len(start) != 9:
            print("Array must consist of 9 digits")

        for i in range(len(start)-1):
            for j in range(i+1, len(start)):
                if start[j] != 0 and start[i] != 0 and start[i] > start[j]:
                    inversions += 1

        if inversions % 2 == 0:
            print("Your puzzle \n{}\n{}\n{}\nwas accepted".format(start[:3], start[3:6], start[6::]))
        else:
            self.board = []
            print("The puzzle was rejected - it is not solvable")

    def find_blank(self):
        """Gives x and y coordinates of the blank tile"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j

    def manhattan_dist(self):
        """Calculates the cumulative Manhattan distance to reach the goal state"""
        manhattan = 0
        pos_goal = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
        g_board = [self.goal[:3], self.goal[3:6], self.goal[6::]]

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] != 0 and self.board[i][j] != g_board[i][j]:
                    manhattan += abs(pos_goal[(self.board[i][j]-1)][0]-i) + abs(pos_goal[(self.board[i][j]-1)][1]-j)
        return manhattan

    def manhattan_dist_fix_fs(self):
        """Calculates the Manhattan distance to fix 1 in the upper left corner"""
        manhattan_fix_fs = 0
        pos_goal = [(0,0)]
        g_board = [[1, 9, 9], [9, 9, 9], [9, 9, 9]]

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 1:
                    manhattan_fix_fs += abs(pos_goal[(self.board[i][j]-1)][0]-i) + abs(pos_goal[(self.board[i][j]-1)][1]-j)
        return manhattan_fix_fs

    def manhattan_dist_fix1(self):
        """Calculates the Manhattan distance to reach the first stage using the method where you fix 1"""
        manhattan_fix1 = 0
        pos_goal = [(0,0), (1,1), (0,2)]
        g_board = [[1, 0, 3], [9, 2, 9], [9, 9, 9]]

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] <4 and self.board[i][j] != g_board[i][j] and self.board[i][j] != 0:
                    manhattan_fix1 += abs(pos_goal[(self.board[i][j]-1)][0]-i) + abs(pos_goal[(self.board[i][j]-1)][1]-j)
        return manhattan_fix1

    def manhattan_dist_worm_fs(self):
        """Calculates the Manhattan distance to reach the first stage using the worm method"""
        manhattan_worm_fs = 0
        pos_goal = [(1,0), (0,0)]
        g_board = [[3, 9, 9], [2, 9, 9], [9, 9, 9]]

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] <4 and self.board[i][j] != g_board[i][j] and self.board[i][j] >= 2:
                    manhattan_worm_fs += abs(pos_goal[(self.board[i][j]-2)][0]-i) + abs(pos_goal[(self.board[i][j]-2)][1]-j)
        return manhattan_worm_fs

    def manhattan_dist_worm(self):
        """Calculates the Manhattan distance to reach the first stage using the worm method"""
        manhattan_worm = 0
        pos_goal = [(1,0), (0,1), (0,2)]
        g_board = [[0, 2, 3], [1, 9, 9], [9, 9, 9]]

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] <4 and self.board[i][j] != g_board[i][j] and self.board[i][j] != 0:
                    manhattan_worm += abs(pos_goal[(self.board[i][j]-1)][0]-i) + abs(pos_goal[(self.board[i][j]-1)][1]-j)
        return manhattan_worm

    def manhattan_second_row(self):
        """Calculates the cumulative Manhattan distance to reach the goal state"""

        manhattan_second_row = 0
        pos_goal = [(0,0), (0,1), (0,2), (1,1), (None, None), (None, None), (1,0)]
        g_board = [[1, 2, 3], [7, 4, 9], [9, 9, 9]]

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] not in [0, 5, 6, 8] and self.board[i][j] != g_board[i][j]:
                    manhattan_second_row += abs(pos_goal[(self.board[i][j]-1)][0]-i) + abs(pos_goal[(self.board[i][j]-1)][1]-j)

        return manhattan_second_row

    # Loss Functions
    def f(self):
        self.total_cost = self.manhattan_dist() + self.step_count

    def f_fix_fs(self):
        return self.manhattan_dist_fix_fs() + self.step_count

    def f_fix(self):
        return self.manhattan_dist_fix1() + self.step_count

    def f_worm_fs(self):
        return self.manhattan_dist_worm_fs() + self.step_count

    def f_worm(self):
        return self.manhattan_dist_worm() + self.step_count

    def f_second_row(self):
        return self.manhattan_second_row() + self.step_count

    def generate_children(self):
        """Performs all possible moves and returns list of children of class puzzle"""
        x1, y1 = self.find_blank()

        new_row_coordinates = []
        new_col_coordinates = []
        for i in range(2):
            new_row_coordinates.append(x1+(-1)**(i+1))
            new_col_coordinates.append(y1+(-1)**(i+1))

        new_coordinates = []

        for i in new_row_coordinates:
            if i >=0 and i <=2:
                new_coordinates.append((i,y1))

        for i in new_col_coordinates:
            if i >=0 and i <=2:
                new_coordinates.append((x1,i))

        ### Look for values at coordinates in starting position
        board_c = {}

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                board_c[(i,j)] = self.board[i][j]

        moving_tiles = []
        children = []

        for i in range(len(new_coordinates)):
            if new_coordinates[i] in board_c:
                moving_tiles.append(board_c[new_coordinates[i]])

        for i in range(len(new_coordinates)):
            temp_board = copy.deepcopy(self.board)
            temp_board[new_coordinates[i][0]][new_coordinates[i][1]] = 0
            temp_board[x1][y1] = moving_tiles[i]

            child = puzzle(np.squeeze(np.asarray(temp_board)).flatten().tolist(), self.step_count+1)
            child.f()
            child.parent_layout = self.parent_layout + np.squeeze(np.asarray(self.board)).flatten().tolist()
            children.append(child)

        return children

    def strategy_fix(self):
        open_1 = PriorityQueue()
        open_11 = PriorityQueue()
        g = [1, 0, 3, 9, 2, 9, 9, 9, 9]

        if self.board[0][0] != 1:
            for node in self.generate_children():
                open_1.push((node.f_fix_fs()), node)

            while True:
                current_1 = open_1.get()

                if current_1.board[0][0] == 1:
                    break

                for next_node in current_1.generate_children():
                    open_1.push((next_node.f_fix_fs()), next_node)

        else:
            current_1 = self

        stage1 = current_1

        for node in stage1.generate_children():
            open_11.push((node.f_fix()), node)

        while True:
            current_11 = open_11.get()
            b = np.squeeze(np.asarray(current_11.board)).flatten().tolist()
            intersection = [i for i, j in zip(b, g) if i == j]
            if intersection == [1, 0, 3, 2]:
                break

            for next_node in current_11.generate_children():
                if next_node.board[0] != [1, 2, 3]:
                    open_11.push((next_node.f_fix()), next_node)

        for child in current_11.generate_children():
            if child.board[0] == [1, 2, 3]:
                board = np.squeeze(np.asarray(child.board)).flatten().tolist()
                steps = child.step_count
                layouts_before = child.parent_layout

        return board, steps, layouts_before

    def strategy_worm(self):
        open_2 = PriorityQueue()
        open_22 = PriorityQueue()
        g = [0, 2, 3, 1, 9, 9, 9, 9, 9]

        if not (self.board[0][0] == 3 and self.board[1][0] == 2):
            for node in self.generate_children():
                open_2.push((node.f_worm_fs()), node)

            while True:
                current_2 = open_2.get()

                if current_2.board[0][0] == 3 and current_2.board[1][0] == 2:
                    break

                for next_node in current_2.generate_children():
                    open_2.push((next_node.f_worm_fs()), next_node)

        else:
            current_2 = self

        stage1 = current_2

        for node in stage1.generate_children():
            open_22.push((node.f_worm()), node)

        while True:
            current_22 = open_22.get()
            b = np.squeeze(np.asarray(current_22.board)).flatten().tolist()
            intersection = [i for i, j in zip(b, g) if i == j]
            if intersection == [0, 2, 3, 1]:
                break

            for next_node in current_22.generate_children():
                open_22.push((next_node.f_worm()), next_node)

        for child in current_22.generate_children():
            if child.board[0] == [1, 2, 3]:
                board = np.squeeze(np.asarray(child.board)).flatten().tolist()
                steps = child.step_count
                layouts_before = child.parent_layout

        return board, steps, layouts_before

    def solve_second_row(self):
        open = PriorityQueue()
        g = [1, 2, 3, 7, 4, 9, 9, 9, 9]

        for node in self.generate_children():
            open.push((node.f_second_row()), node)

        while True:
            current_2 = open.get()
            b = np.squeeze(np.asarray(current_2.board)).flatten().tolist()
            intersection = [i for i, j in zip(b, g) if i == j]
            if intersection == [1, 2, 3, 7, 4]:
                break

            for next_node in current_2.generate_children():
                open.push((next_node.f_second_row()), next_node)

        else:
            current_2 = self

        board = np.squeeze(np.asarray(current_2.board)).flatten().tolist()
        return board, current_2.step_count, current_2.parent_layout

    def solve_puzzle(self):
        open = PriorityQueue()

        for node in self.generate_children():
            open.push((node.total_cost), node)
        while True:
            current = open.get()
            if np.squeeze(np.asarray(current.board)).flatten().tolist() == self.goal:
                break

            for next_node in current.generate_children():
                open.push((next_node.total_cost), next_node)

        path = current.parent_layout + np.squeeze(np.asarray(current.board)).flatten().tolist()
        return path, current.step_count

def main():
    puz = puzzle([], 0)
    worm = puz.strategy_worm()
    fix_one = puz.strategy_fix()

    pw = puzzle(worm[0], 0)
    pw_second_row = pw.solve_second_row()
    worm_sr = puzzle(pw_second_row[0], 0)
    pw_solved = worm_sr.solve_puzzle()
    print('Using the Worm strategy, it takes {} moves to solve the puzzle.'.format(worm[1] + pw_second_row[1] + pw_solved[1]))
    qprint_worm = input('Print the whole path for the worm strategy?[y/n]')
    if qprint_worm == 'y':
        path = worm[-1] + pw_second_row[-1] + pw_solved[0]
        for j in range(0, len(path), 9):
            layout = path[j:j + 9]
            for i in range(0, len(layout), 3):
                print(layout[i:i + 3])
            print('\n')

    po = puzzle(fix_one[0], 0)
    po_second_row = po.solve_second_row()
    fix_one_sr = puzzle(po_second_row[0], 0)
    po_solved = fix_one_sr.solve_puzzle()
    print('Using the strategy where tile 1 is fixed first, it takes {} moves to solve the puzzle.'.format(fix_one[1] + po_second_row[1] + po_solved[1]))
    qprint_fix_one = input('Print the whole path for the Fix_one strategy?[y/n]')
    if qprint_fix_one == 'y':
        path = fix_one[-1] + po_second_row[-1] + po_solved[0]
        for j in range(0, len(path), 9):
            layout = path[j:j + 9]
            for i in range(0, len(layout), 3):
                print(layout[i:i + 3])
            print('\n')

if __name__ == '__main__':
    main()
