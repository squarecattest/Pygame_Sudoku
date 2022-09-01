from random import random, choice, shuffle, sample, randrange
from itertools import product
#import random
class Unsolvable(Exception):
    pass

class Sudoku:
    def __init__(self, puzzle: list[list[int]], guess_indexs: tuple[int] = (0, 0)):
        self.puzzle = []
        self.possibilities = []
        self.rows, self.columns, self.squares = [], [], [] # numbers to fill in
        for i in range(9):
            self.puzzle.append(puzzle[i].copy())
            self.rows.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
            self.columns.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
            self.squares.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
            self.possibilities.append([])
            for j in range(9):
                if puzzle[i][j]: self.possibilities[i].append(set())
                else: self.possibilities[i].append({1, 2, 3, 4, 5, 6, 7, 8, 9})
        self.guess_indexs = self.next_guess_index(*guess_indexs)
        for i, j in product(range(9), range(9)):
            if self.puzzle[i][j]: self.update((i, j))
    
    def index_to_row(self, index: int):
        return tuple((index, j) for j in range(9))
    
    def index_to_column(self, index: int):
        return tuple((i, index) for i in range(9))
    
    def index_to_square(self, index: int):
        i, j = (index // 3) * 3, (index % 3) * 3
        return ((i, j), (i + 1, j), (i + 2, j), (i, j + 1), (i + 1, j + 1), (i + 2, j + 1),
                (i, j + 2), (i + 1, j + 2), (i + 2, j + 2))

    def block_to_square(self, i: int, j: int):
        return self.index_to_square((i // 3) * 3 + j // 3)
    
    def next_guess_index(self, i: int, j: int):
        while self.puzzle[i][j]:
            (i, j) = (i, j + 1) if j < 8 else (i + 1, 0)
        return i, j

    def copy(self):
        return Sudoku(self.puzzle, self.guess_indexs) # efficiency?

    def overwrite(self, sudoku):
        self.guess_indexs = sudoku.guess_indexs
        for i in range(9):
            self.puzzle[i] = sudoku.puzzle[i].copy()
            self.rows[i] = sudoku.rows[i].copy()
            self.columns[i] = sudoku.columns[i].copy()
            self.squares[i] = sudoku.squares[i].copy()
            for j in range(9):
                self.possibilities[i][j] = sudoku.possibilities[i][j].copy()

    def check_solved(self):
        for i, j in product(range(9), range(9)):
            if not self.puzzle[i][j]: return False
        return True

    def check_repeat_functions(self, *functions):
        for func in functions:
            for i in range(9):
                blocks = func(i)
                for num in range(1, 10):
                    if [self.puzzle[k][l] for k, l in blocks].count(num) > 1:
                        raise Unsolvable

    def check_repeat(self):
        self.check_repeat_functions(self.index_to_row, self.index_to_column, self.index_to_square)

    # main

    def update(self, pos: tuple[int]):
        '''
        Update the puzzle's possiblility. (when initialized, or a block is filled)
        '''
        i, j = pos
        num = self.puzzle[i][j]
        self.rows[i].discard(num)
        self.columns[j].discard(num)
        self.squares[(i // 3) * 3 + j // 3].discard(num)
        for k, l in self.index_to_row(i):
            self.possibilities[k][l].discard(num)
        for k, l in self.index_to_column(j):
            self.possibilities[k][l].discard(num)
        for k, l in self.block_to_square(i, j):
            self.possibilities[k][l].discard(num)

    def fill_in(self, blocks: tuple[tuple[int]], left_nums: set[int]):
        '''
        Fill in the blanks if it has only one possibility.
        Used in function fill_in_loop.
        '''
        left_nums_copy = left_nums.copy()
        updated = False
        for num in left_nums_copy:
            count = 0
            for i, j in blocks:
                if num in self.possibilities[i][j]:
                    pos = (i, j)
                    count += 1
                    if count > 1: break
            if not count: raise Unsolvable
            if count == 1:
                self.puzzle[pos[0]][pos[1]] = num
                self.possibilities[pos[0]][pos[1]].clear()
                self.update(pos)
                updated = True
        return updated
    
    def guess(self):
        '''
        For those whose puzzle can't be further filled in, guess from the first blank.
        '''
        self.guess_indexs = self.next_guess_index(*self.guess_indexs)
        for num in self.possibilities[self.guess_indexs[0]][self.guess_indexs[1]]:
            copied = self.copy()
            copied.puzzle[self.guess_indexs[0]][self.guess_indexs[1]] = num
            copied.possibilities[self.guess_indexs[0]][self.guess_indexs[1]].clear()
            copied.update(self.guess_indexs)
            try:
                copied.solve()
                return self.overwrite(copied)
            except Unsolvable:
                continue
        # Only when all the possiblities are false raise an error.
        raise Unsolvable

    def fill_in_loop(self):
        '''
        The place where we execute fill-in loop.
        '''
        while not self.check_solved():
            updated = False
            for i in range(9):
                updated = updated or self.fill_in(self.index_to_row(i), self.rows[i])
                updated = updated or self.fill_in(self.index_to_column(i), self.columns[i])
                updated = updated or self.fill_in(self.index_to_square(i), self.squares[i])
            if not updated: return False # not finished
        return True # finished
    
    def solve(self):
        '''
        The place where we execute fill-guess iteration.
        '''
        if not self.fill_in_loop():
            self.check_repeat()
            self.guess()

def random_create(difficulty: int):
    first_row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    spawn_chance = 0.25
    blank_chance = [33, 40, 45, 50]
    while True:
        try:
            shuffle(first_row)
            sudoku = [first_row.copy()]
            for i in range(8): sudoku.extend([[0] * 9])
            sudoku = Sudoku(sudoku)
            for i, j in product(range(8), range(9)):
                if random() < spawn_chance and sudoku.possibilities[i][j]:
                    if not sudoku.possibilities[i][j]: raise Unsolvable
                    sudoku.puzzle[i][j] = choice([num for num in sudoku.possibilities[i][j]])
                    sudoku.update((i, j))
            sudoku.solve()
        except Unsolvable: pass
        else: break
    for i, j in sample(tuple(product(range(9), range(9))), k = randrange(blank_chance[difficulty - 1], blank_chance[difficulty])):
        sudoku.puzzle[i][j] = 0
    return sudoku.puzzle
    
    

    
