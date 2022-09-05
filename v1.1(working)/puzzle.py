from objects import *
import sudoku
from itertools import product
from time import time
from types import NoneType
from typing import overload


class Sudoku:
    def __init__(self, __puzzle: list[list[int]]):
        self.__puzzle, self.__fixed = [], set()
        for i in range(9):
            self.__puzzle.append(__puzzle[i].copy())
            for j in range(9):
                if __puzzle[i][j]:
                    self.__fixed.add((i, j))
    @staticmethod
    def index_to_row(block: tuple[int]):
        return tuple((block[0], j) for j in range(9) if j != block[1])

    @staticmethod
    def index_to_column(block: tuple[int]):
        return tuple((i, block[1]) for i in range(9) if i != block[0])

    @staticmethod
    def index_to_square(block: tuple[int]):
        i, j = (block[0] // 3) * 3, (block[1] // 3) * 3
        return tuple((i + k, j + l) for k, l in product(range(3), range(3)) if (i + k, j + l) != block)

    def possibilities(self, block: tuple[int]):
        num_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for i, j in self.index_to_row(block) + self.index_to_column(block) + self.index_to_square(block):
            num_set.discard(self.__puzzle[i][j])
        return num_set

    def get_hint_block(self):
        def get_repeated():
            repeated = []
            for i, j in product(range(9), range(9)):
                if self.__puzzle[i][j] and not (i, j) in self.__fixed \
                    and not self.__puzzle[i][j] in self.possibilities((i, j)):
                    repeated.append((i, j))
            return repeated
        
        def get_error():
            '''
            Warning:
            This function could potentially cause IndexError: index out of range when fill_origin
            initializing. If the puzzle is full filled, guess_index in class `Sudoku` will have
            no available index. In this version, the condition is catched by get_repeated, where
            this function will not be called.
            '''
            origin = [[0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9, [0] * 9]
            filled = []
            for block in self.__fixed:
                origin[block[0]][block[1]] = self.__puzzle[block[0]][block[1]]
            for i, j in product(range(9), range(9)):
                if self.__puzzle[i][j] and not (i, j) in self.__fixed:
                    filled.append((i, j))
            length = len(filled)
            split = [-1, length - 1] # [min_solvable, max_unsolvable]
            while True:
                if split[1] == 0: return filled[0]
                if split[1] - split[0] == 1:
                    return filled[split[1]]
                fill_origin = origin.copy()
                mid = (split[0] + split[1]) // 2
                for i in range(mid + 1):
                    block = filled[i]
                    fill_origin[block[0]][block[1]] = self.__puzzle[block[0]][block[1]]
                fill_origin = sudoku.Sudoku(fill_origin)
                try:
                    fill_origin.solve()
                except sudoku.Unsolvable:
                    split[1] = mid
                else:
                    split[0] = mid

        def only_left(block: tuple[int]):
            for i, j in self.index_to_row(block):
                if not self.__puzzle[i][j]:
                    break
            else:
                return True
            for i, j in self.index_to_column(block):
                if not self.__puzzle[i][j]:
                    break
            else:
                return True
            for i, j in self.index_to_square(block):
                if not self.__puzzle[i][j]:
                    break
            else:
                return True
            return False

        def only_placable(block: tuple[int]):
            for num in self.possibilities(block):
                for i, j in self.index_to_row(block):
                    if not self.__puzzle[i][j] and num in self.possibilities((i, j)):
                        break
                else:
                    return True
                for i, j in self.index_to_column(block):
                    if not self.__puzzle[i][j] and num in self.possibilities((i, j)):
                        break
                else:
                    return True
                for i, j in self.index_to_square(block):
                    if not self.__puzzle[i][j] and num in self.possibilities((i, j)):
                        break
                else:
                    return True
            return False
        repeated = get_repeated()
        if repeated: return repeated, "repeated"
        try:
            try_solve = sudoku.Sudoku(self.__puzzle)
            try_solve.solve()
        except sudoku.Unsolvable:
            return get_error(), "error"
        else:
            # prior
            for i, j in product(range(9), range(9)):
                if not self.__puzzle[i][j] and only_left((i, j)):
                    return (i, j), "hint"
            # second
            for i, j in product(range(9), range(9)):
                if not self.__puzzle[i][j] and len(self.possibilities((i, j))) == 1:
                    return (i, j), "hint"
            # posterior
            for i, j in product(range(9), range(9)):
                if not self.__puzzle[i][j] and only_placable((i, j)):
                    return (i, j), "hint"
            return None, None

    def change_block(self, block: tuple[int], num: int):
        '''
        return True if the puzzle is solved after changing.

        return False if the puzzle is not solved.
        '''
        def check_solved():
            for i, j in product(range(9), range(9)):
                if not self.__puzzle[i][j]:
                    return False
                if not self.__puzzle[i][j] in self.possibilities((i, j)):
                    return False
            return True

        if not block in self.__fixed:
            self.__puzzle[block[0]][block[1]] = num
            return check_solved()
        return False

    def get_puzzle(self):
        return self.__puzzle

    def get_num(self, block: tuple[int]):
        return self.__puzzle[block[0]][block[1]]

    def get_fixed(self):
        return self.__fixed
    
    def get_same_num_blocks(self, block: tuple[int]):
        block_num = self.__puzzle[block[0]][block[1]]
        same_num_blocks = []
        for i, j in product(range(9), range(9)):
            if self.__puzzle[i][j] == block_num and (i, j) != block:
                same_num_blocks.append((i, j))
        return same_num_blocks

    def solve(self):
        solution = sudoku.Sudoku(self.__puzzle)
        solution.solve()
        self.__puzzle = solution.puzzle


class PuzzlePage:
    color_fixed = (0, 0, 0)
    color_entered = (52, 52, 255)
    color_guessed = (50, 205, 50)
    color_repeated = (229, 50, 50)
    number_fixed = [0,
                    Font.number.render("1", False, color_fixed),
                    Font.number.render("2", False, color_fixed),
                    Font.number.render("3", False, color_fixed),
                    Font.number.render("4", False, color_fixed),
                    Font.number.render("5", False, color_fixed),
                    Font.number.render("6", False, color_fixed),
                    Font.number.render("7", False, color_fixed),
                    Font.number.render("8", False, color_fixed),
                    Font.number.render("9", False, color_fixed)]
    number_entered = [0,
                      Font.number.render("1", False, color_entered),
                      Font.number.render("2", False, color_entered),
                      Font.number.render("3", False, color_entered),
                      Font.number.render("4", False, color_entered),
                      Font.number.render("5", False, color_entered),
                      Font.number.render("6", False, color_entered),
                      Font.number.render("7", False, color_entered),
                      Font.number.render("8", False, color_entered),
                      Font.number.render("9", False, color_entered)]
    number_guessed = [0,
                      Font.number.render("1", False, color_guessed),
                      Font.number.render("2", False, color_guessed),
                      Font.number.render("3", False, color_guessed),
                      Font.number.render("4", False, color_guessed),
                      Font.number.render("5", False, color_guessed),
                      Font.number.render("6", False, color_guessed),
                      Font.number.render("7", False, color_guessed),
                      Font.number.render("8", False, color_guessed),
                      Font.number.render("9", False, color_guessed)]
    number_repeated = [0,
                       Font.number.render("1", False, color_repeated),
                       Font.number.render("2", False, color_repeated),
                       Font.number.render("3", False, color_repeated),
                       Font.number.render("4", False, color_repeated),
                       Font.number.render("5", False, color_repeated),
                       Font.number.render("6", False, color_repeated),
                       Font.number.render("7", False, color_repeated),
                       Font.number.render("8", False, color_repeated),
                       Font.number.render("9", False, color_repeated)]
    selected_block = pygame.Surface((32, 32))
    selected_block.fill((255, 255, 255))
    selected_block.set_alpha(130)
    hint_block = pygame.Surface((32, 32))
    hint_block.fill(color_entered)
    hint_block.set_alpha(97)
    error_hint_block = pygame.Surface((32, 32))
    error_hint_block.fill(color_repeated)
    error_hint_block.set_alpha(97)
    same_num_block = pygame.Surface((32, 32))
    same_num_block.fill((121, 201, 249))
    same_num_block.set_alpha(97)
    timer = Objects(Texture.timer, "rel_center", (238, -205))
    passed_time_text = Objects(Font.subtitle.render("00:00", False, (0, 0, 0)), "rel_center", (298, -203))
    icon_moves = Objects(Texture.moves, "rel_center", (245, -166))
    moves_text = Objects(Font.subtitle.render("000", False, (0, 0, 0)), "rel_center", (291, -166))
    bar_Mode = Objects(Texture.select_bar_ingame, "rel_center", (280, -120))
    bar_Undo = Objects(Texture.select_bar_ingame, "rel_center", (280, -72))
    bar_Hint = Objects(Texture.select_bar_ingame, "rel_center", (280, -24))
    bar_Clear = Objects(Texture.select_bar_ingame, "rel_center", (280, 24))
    bar_Solve = Objects(Texture.select_bar_ingame, "rel_center", (280, 72))
    bar_Back = Objects(Texture.select_bar_ingame, "rel_center", (280, 120))
    bar_Mode_locked = Objects(Texture.select_bar_ingame_locked, "rel_center", (280, -120))
    bar_Undo_locked = Objects(Texture.select_bar_ingame_locked, "rel_center", (280, -72))
    bar_Hint_locked = Objects(Texture.select_bar_ingame_locked, "rel_center", (280, -24))
    bar_Clear_locked = Objects(Texture.select_bar_ingame_locked, "rel_center", (280, 24))
    bar_Solve_locked = Objects(Texture.select_bar_ingame_locked, "rel_center", (280, 72))
    bar_text_Mode = Objects(Font.bar.render("Mode:  Enter", False, (0, 0, 0)), "rel_center", (280, -117))
    bar_text_Undo = Objects(Font.bar.render("Undo", False, (0, 0, 0)), "rel_center", (280, -72))
    bar_text_Hint = Objects(Font.bar.render("Hint", False, (0, 0, 0)), "rel_center", (280, -24))
    bar_text_Clear = Objects(Font.bar.render("Clear", False, (0, 0, 0)), "rel_center", (280, 24))
    bar_text_Solve = Objects(Font.bar.render("Solve", False, (0, 0, 0)), "rel_center", (280, 72))
    bar_text_Back = Objects(Font.bar.render(
        "Back  to  Title  Screen", False, (0, 0, 0)), "rel_center", (280, 123)
    )

    mask = pygame.Surface((1280, 720))
    mask.set_alpha(220)
    mask = Objects(mask, "default", (0, 0))
    dialog_box = Objects(Texture.dialog_box, "rel_center", (0, 0))
    dialog_clear_1 = Objects(
        Font.bar.render("Are you sure to clear up the", False, (0, 0, 0)), "rel_center", (0, -41)
    )
    dialog_clear_2 = Objects(
        Font.bar.render("puzzle? (Timer will not reset.)", False, (0, 0, 0)), "rel_center", (0, -13)
    )
    dialog_solve_1 = Objects(
        Font.bar.render("Are you sure to solve this", False, (0, 0, 0)), "rel_center", (0, -55)
    )
    dialog_solve_2 = Objects(
        Font.bar.render("puzzle by bot? The record will", False, (0, 0, 0)), "rel_center", (0, -27)
    )
    dialog_solve_3 = Objects(
        Font.bar.render("not be saved.", False, (0, 0, 0)), "rel_center", (0, 1)
    )
    dialog_back_1 = Objects(
        Font.bar.render("Are you sure to return to title", False, (0, 0, 0)), "rel_center", (0, -41)
    )
    dialog_back_2 = Objects(
        Font.bar.render("screen?", False, (0, 0, 0)), "rel_center", (0, -13)
    )
    button_Cancel = Objects(Texture.dialog_button, "rel_center", (-79, 51))
    button_Yes = Objects(Texture.dialog_button, "rel_center", (79, 51))
    button_text_Cancel = Objects(Font.bar.render("Cancel", False, (0, 0, 0)), "rel_center", (-79, 51))
    button_text_Yes = Objects(Font.bar.render("Yes", False, (0, 0, 0)), "rel_center", (79, 51))

    result_box = Objects(Texture.result_box, "rel_center", (0, 0))
    result_title = Objects(Font.subtitle.render("Result", False, (0, 0, 0)), "rel_center", (0, -103))
    result_timer = Objects(Texture.result_timer, "rel_center", (-29, -38))
    result_moves = Objects(Texture.result_moves, "rel_center", (-19, -8))
    result_hints = Objects(Texture.result_hint, "rel_center", (-21, 22))
    button_OK = Objects(Texture.dialog_button, "rel_center", (0, 95))
    button_text_OK = Objects(Font.bar.render("OK", False, (0, 0, 0)), "rel_center", (0, 95))

    @overload
    def __init__(self, difficulty: int | None):
        ...

    @overload
    def __init__(self, load_file: dict):
        ...

    def __init__(self, difficulty_or_file: int | None | dict):
        if isinstance(difficulty_or_file, (int, NoneType)):
            difficulty = difficulty_or_file or 1
            self.difficulty = difficulty
            self.original = sudoku.random_create(difficulty)
            self.puzzle = Sudoku(self.original)
            self.__fixed = self.puzzle.get_fixed()
            self.undos = [] # [(block: tuple, before changed num: int|None, reverse: bool), (), ...]
            self.moves = 0
            self.used_hints = 0
            self.time = time()
            self.guesses = set()
        elif isinstance(difficulty_or_file, dict):
            saved_file = difficulty_or_file
            self.difficulty = saved_file.get("difficulty")
            self.original = saved_file.get("original")
            self.puzzle = Sudoku(self.original)
            self.__fixed = set(saved_file.get("fixed"))
            for i, j, num in saved_file.get("inputs"):
                self.puzzle.change_block((i, j), num)
            self.undos = saved_file.get("undos")
            self.moves = saved_file.get("moves")
            self.used_hints = saved_file.get("used_hints")
            self.time = time() - saved_file.get("time")
            self.guesses = set(saved_file.get("guesses"))
        else: raise Exception("Error occured when initializing puzzle.")
        self.difficulty_text = Objects(Font.subtitle.render(
            "Difficulty: " + ["Easy", "Normal", "Hard"][self.difficulty - 1], False, (0, 0, 0)
        ), "rel_center", (280, -240))
        self.result_text_difficulty = Objects(Font.bar.render(
            "Difficulty: " + ["Easy", "Normal", "Hard"][self.difficulty - 1], False, (0, 0, 0)
        ), "rel_center", (0, -65))
        self.selected = None
        self.hinted = None
        self.hint_mode = None
        self.guessing = False
        self.solved = False
        self.solved_by_bot = False
        self.ask_clear = False
        self.ask_solve = False
        self.ask_quit = False
        self.show_result = False
    
    def fill_block(self, block: tuple[int], num: int):
        '''
        return True if the puzzle is solved after filling.

        return False if the puzzle is not solved.
        '''
        if block in self.__fixed:
            Sound.play(Sound.forbidden)
            return False
        undo_code = 2 * (num != self.puzzle.get_num(block)) \
                    + (self.guessing ^ (block in self.guesses))
        if undo_code & 2 and num: self.moves += 1
        if undo_code == 1: self.undos.append((block, None, True))
        elif undo_code == 2: self.undos.append((block, self.puzzle.get_num(block), False))
        elif undo_code == 3: self.undos.append((block, self.puzzle.get_num(block), True))
        
        if self.guessing: self.guesses.add(block)
        else: self.guesses.discard(block)

        if undo_code & 2:
            self.hinted = self.hint_mode = None
            return self.puzzle.change_block(block, num)
        return False
    
    def finished(self):
        self.solved = True
        self.show_result = True
        self.selected = None
        self.hinted = self.hint_mode = None
        self.guesses.clear()
        self.total_time = int(time() - self.time)
        if self.total_time < 6000:
            self.result_time_text = Objects(Font.bar.render(
                f"{self.total_time // 60:02}:{self.total_time % 60:02}", False, (0, 0, 0)
            ), "rel_center", (19, -38))
        else:
            self.result_time_text = Objects(Font.bar.render(
                "99:59", False, (0, 0, 0)
            ), "rel_center", (19, -38))
        self.result_moves_text = Objects(Font.bar.render(
            f"{min(self.moves, 999):03}", False, (0, 0, 0)
        ), "rel_center", (19, -8))
        self.result_hints_text = Objects(Font.bar.render(
            f"{min(self.used_hints, 999):03}", False, (0, 0, 0)
        ), "rel_center", (19, 22))
        self.result_correct_moves_text = Objects(Font.bar.render(
            f"Correct Moves: {int((81 - len(self.__fixed)) * 100 / self.moves)}%", False, (0, 0, 0)
        ), "rel_center", (0, 55))
        Sound.play(Sound.finish)

    def undo(self):
        if self.undos:
            block, num, reverse = self.undos.pop()
            if num != None:
                self.puzzle.change_block(block, num)
                self.moves += 1
            if reverse:
                self.guesses.symmetric_difference_update({block})
            self.selected = block
            self.hinted, self.hint_mode = None, None
            Sound.play(Sound.enter)
        else:
            Sound.play(Sound.forbidden)
    
    def hint(self):
        self.hinted, self.hint_mode = self.puzzle.get_hint_block()
        if self.hinted:
            if self.hint_mode == "hint":
                self.selected = self.selected or self.hinted
                Sound.play(Sound.enter)
            elif self.hint_mode == "error":
                Sound.play(Sound.forbidden)
            elif self.hint_mode == "repeated":
                Sound.play(Sound.forbidden)
            else:
                raise Exception(f'PuzzlePage.hint_mode should be "hint", "repeated" or "error", but get {self.hint_mode}')
            self.used_hints += 1
        else:
            Sound.play(Sound.forbidden)

    def clear(self):
        for i, j in product(range(9), range(9)):
            if not (i, j) in self.__fixed:
                self.puzzle.change_block((i, j), 0)
        self.selected = None
        self.hinted, self.hint_mode = None, None
        self.undos.clear()
        self.moves += 1
        Sound.play(Sound.enter)

    def solve_by_bot(self):
        try:
            self.puzzle.solve()
        except sudoku.Unsolvable:
            self.puzzle = Sudoku(self.original)
            self.puzzle.solve()
        self.solved = True
        self.solved_by_bot = True
        self.selected = None
        self.hinted, self.hint_mode = None, None
        self.guesses.clear()
        self.passed_time_text.surface = Font.bar.render("--:--", False, (0, 0, 0))
        self.moves_text.surface = Font.bar.render("---", False, (0, 0, 0))
        self.total_time = int(time() - self.time)
        Sound.play(Sound.enter)
    
    def save_temp(self):
        self.bar_text_Mode.surface = Font.bar.render('Mode:  Enter', False, (0, 0, 0))
        inputs = []
        for i, j in product(range(9), range(9)):
            if not (i, j) in self.__fixed and self.puzzle.get_num((i, j)):
                inputs.append([i, j, self.puzzle.get_num((i, j))])
        return {
            "difficulty": self.difficulty,
            "original": self.original,
            "fixed": list(self.__fixed),
            "inputs": inputs,
            "undos": self.undos,
            "moves": self.moves,
            "used_hints": self.used_hints,
            "time": time() - self.time,
            "guesses": list(self.guesses)
        }

    def show_screen(self, screen: pygame.Surface):
        Background.background.display(screen)

        ## blocks & nums
        for i, j in product(range(-1, 2), range(-1, 2)):
            align.rel_center(screen, Texture.block, (-280 + 112 * i, 112 * j))
        puzzle_nums = self.puzzle.get_puzzle()
        for i, j in product(range(9), range(9)):
            dx, dy = 36 * i + 4 * (i // 3), 36 * j + 4 * (j // 3)
            shift = (-280 - 148 + dx, -148 + dy)
            num = puzzle_nums[i][j]
            if (i, j) in self.__fixed:
                align.rel_center(screen, self.number_fixed[num], shift)
            elif puzzle_nums[i][j]:
                if puzzle_nums[i][j] in self.puzzle.possibilities((i, j)):
                    if (i, j) in self.guesses:
                        align.rel_center(screen, self.number_guessed[num], shift)
                    else:
                        align.rel_center(screen, self.number_entered[num], shift)
                else:
                    align.rel_center(screen, self.number_repeated[num], shift)

        ### block masks
        if self.selected:
            dx, dy = 36 * self.selected[0] + 4 * (self.selected[0] // 3), \
                     36 * self.selected[1] + 4 * (self.selected[1] // 3)
            shift = (-280 - 148 + dx, -148 + dy)            
            align.rel_center(screen, self.selected_block, shift)
            if self.puzzle.get_num(self.selected):
                for block in self.puzzle.get_same_num_blocks(self.selected):
                    dx, dy = 36 * block[0] + 4 * (block[0] // 3), \
                             36 * block[1] + 4 * (block[1] // 3)
                    shift = (-280 - 148 + dx, -148 + dy)
                    align.rel_center(screen, self.same_num_block, shift)
        if self.hinted:
            if self.hint_mode == "repeated":
                for block in self.hinted:
                    dx, dy = 36 * block[0] + 4 * (block[0] // 3), \
                             36 * block[1] + 4 * (block[1] // 3)
                    shift = (-280 - 148 + dx, -148 + dy)
                    align.rel_center(screen, self.error_hint_block, shift)
            else:
                dx, dy = 36 * self.hinted[0] + 4 * (self.hinted[0] // 3), \
                         36 * self.hinted[1] + 4 * (self.hinted[1] // 3)
                shift = (-280 - 148 + dx, -148 + dy)
                if self.hint_mode == "hint":
                    align.rel_center(screen, self.hint_block, shift)
                elif self.hint_mode == "error":
                    align.rel_center(screen, self.error_hint_block, shift)
                else:
                    raise Exception(f'PuzzlePage.hint_mode should be "hint", "repeated" or "error", but get {self.hint_mode}')
        
        ## end
        ## bars
        if not self.solved_by_bot:
            if self.solved:
                passed_time = self.total_time
            else:
                passed_time = int(time() - self.time)
            if passed_time < 6000:
                self.passed_time_text.surface = Font.subtitle.render(
                    f"{passed_time // 60:02}:{passed_time % 60:02}", False, (0, 0, 0)
                )
            else:
                self.passed_time_text.surface = Font.subtitle.render("99:59", False, (0, 0, 0))
            self.moves_text.surface = Font.subtitle.render(f"{min(self.moves, 999):03}", False, (0, 0, 0))
        Objects.multi_display(screen,
            self.difficulty_text,
            self.timer,
            self.passed_time_text,
            self.icon_moves,
            self.moves_text
        )
        if not self.solved:
            Objects.multi_display(screen,
                self.bar_Mode,
                self.bar_Undo,
                self.bar_Hint,
                self.bar_Clear,
                self.bar_Solve
            )
        else:
            Objects.multi_display(screen,
                self.bar_Mode_locked,
                self.bar_Undo_locked,
                self.bar_Hint_locked,
                self.bar_Clear_locked,
                self.bar_Solve_locked,
            )
        Objects.multi_display(screen,
            self.bar_Back,
            self.bar_text_Mode,
            self.bar_text_Undo,
            self.bar_text_Hint,
            self.bar_text_Clear,
            self.bar_text_Solve,
            self.bar_text_Back
        )
        ## end

        if self.ask_clear:
            Objects.multi_display(screen,
                self.mask,
                self.dialog_box,
                self.dialog_clear_1,
                self.dialog_clear_2,
                self.button_Cancel,
                self.button_Yes,
                self.button_text_Cancel,
                self.button_text_Yes
            )
        elif self.ask_solve:
            Objects.multi_display(screen,
                self.mask,
                self.dialog_box,
                self.dialog_solve_1,
                self.dialog_solve_2,
                self.dialog_solve_3,
                self.button_Cancel,
                self.button_Yes,
                self.button_text_Cancel,
                self.button_text_Yes
            )
        elif self.ask_quit:
            Objects.multi_display(screen,
                self.mask,
                self.dialog_box,
                self.dialog_back_1,
                self.dialog_back_2,
                self.button_Cancel,
                self.button_Yes,
                self.button_text_Cancel,
                self.button_text_Yes
            )
        elif self.show_result:
            Objects.multi_display(screen,
                self.mask,
                self.result_box,
                self.result_title,
                self.result_text_difficulty,
                self.result_timer,
                self.result_time_text,
                self.result_moves,
                self.result_moves_text,
                self.result_hints,
                self.result_hints_text,
                self.result_correct_moves_text,
                self.button_OK,
                self.button_text_OK
            )

    def action(self, control: Control):
        if not self.solved:
            if self.ask_clear:
                if control.click_in(self.button_Cancel):
                    self.ask_clear = False
                elif control.click_in(self.button_Yes):
                    self.clear()
                    self.ask_clear = False
                return "ingame"
            elif self.ask_solve:
                if control.click_in(self.button_Cancel):
                    self.ask_solve = False
                    return "ingame"
                elif control.click_in(self.button_Yes):
                    self.solve_by_bot()
                    self.ask_solve = False
                    return "clear_temp"
                return "ingame"
            elif self.ask_quit:
                if control.click_in(self.button_Cancel):
                    self.ask_quit = False
                    return "ingame"
                elif control.click_in(self.button_Yes):
                    Sound.play(Sound.enter)
                    return "save_temp"
                return "ingame"
            else:
                if control.click_in(self.bar_Mode) or control.key_in(Control.K_SHIFT):
                    self.guessing = not self.guessing
                    self.bar_text_Mode.surface = Font.bar.render(
                        f'Mode:  {["Enter", "Guess"][self.guessing]}', False, (0, 0, 0)
                    )
                    Sound.play(Sound.enter)
                elif control.click_in(self.bar_Undo) or control.key_in(pygame.K_u):
                    self.undo()
                elif control.click_in(self.bar_Hint) or control.key_in(pygame.K_h):
                    self.hint()
                elif control.click_in(self.bar_Clear) or control.key_in(pygame.K_c):
                    self.ask_clear = True
                    Sound.play(Sound.enter)
                elif control.click_in(self.bar_Solve) or control.key_in(pygame.K_s):
                    self.ask_solve = True
                    Sound.play(Sound.enter)
                elif control.click_in(self.bar_Back) or control.key_in(pygame.K_b):
                    self.ask_quit = True
                    Sound.play(Sound.enter)
                elif control.is_click():
                    self.hinted = self.hint_mode = None
                    self.selected = control.click_in_block()
                elif control.is_key() and self.selected:
                    if control.key_in(pygame.K_LEFT):
                        if self.selected[0] > 0:
                            self.selected = (self.selected[0] - 1, self.selected[1])
                    elif control.key_in(pygame.K_RIGHT):
                        if self.selected[0] < 8:
                            self.selected = (self.selected[0] + 1, self.selected[1])
                    elif control.key_in(pygame.K_UP):
                        if self.selected[1] > 0:
                            self.selected = (self.selected[0], self.selected[1] - 1)
                    elif control.key_in(pygame.K_DOWN):
                        if self.selected[1] < 8:
                            self.selected = (self.selected[0], self.selected[1] + 1)
                    else:
                        num = control.key_in_num()
                        if num != None and self.fill_block(self.selected, num):
                            self.finished()
                            return "save_log"
                return "ingame"
        
        elif self.show_result:
            if control.click_in(self.button_OK):
                self.show_result = False
                Sound.play(Sound.enter)
            return "ingame"
        
        else:
            if control.click_in(self.bar_Mode, self.bar_Undo, self.bar_Hint, self.bar_Clear, self.bar_Solve):
                Sound.play(Sound.forbidden)
                return "ingame"
            elif control.click_in(self.bar_Back):
                Sound.play(Sound.enter)
                return "back"
            
        return "ingame"

        if event.type == pygame.MOUSEBUTTONUP and event.__dict__.get("button") == 1:
            pos = event.__dict__.get("pos", (0, 0))
            if not self.solved:
                        center = (screen.get_size()[0] // 2, screen.get_size()[1] // 2)
                        shift = (pos[0] - center[0], pos[1] - center[1])
                        rel_shift = (shift[0] + 280 + 148 + 16, shift[1] + 148 + 16)
                        if rel_shift[0] % 112 <= 103 and (rel_shift[0] % 112) % 36 <= 31 and rel_shift[1] % 112 <= 103 and (rel_shift[1] % 112) % 36 <= 31:
                            i, j = 3 * (rel_shift[0] // 112) + (rel_shift[0] % 112) // 36, \
                                   3 * (rel_shift[1] // 112) + (rel_shift[1] % 112) // 36
                            if 0 <= i <= 8 and 0 <= j <= 8:
                                self.selected = (i, j)
                                return "ingame"
                        self.selected = None
                        return "ingame"
            elif self.show_result:
                if self.button_OK.contain(screen, pos):
                    self.show_result = False
                    Sound.play(Sound.enter)
                return "ingame"
            else:
                if self.bar_Mode.contain(screen, pos) or self.bar_Undo.contain(screen, pos) \
                    or self.bar_Hint.contain(screen, pos) or self.bar_Clear.contain(screen, pos) \
                    or self.bar_Solve.contain(screen, pos):
                    Sound.play(Sound.forbidden)
                    return "ingame"
                elif self.bar_Back.contain(screen, pos):
                    self.bar_text_Mode.surface = Font.bar.render('Mode:  Enter', False, (0, 0, 0))
                    Sound.play(Sound.enter)
                    return "back"
            return "ingame"
        
        if event.type == pygame.KEYDOWN and not self.ask_clear and not self.ask_solve and not self.ask_quit:
            key = event.__dict__.get("key")
            button = event.__dict__.get("unicode")
            if not self.solved:
                if key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
                    self.guessing = not self.guessing
                    self.bar_text_Mode.surface = Font.bar.render(
                        f'Mode:  {["Enter", "Guess"][self.guessing]}', False, (0, 0, 0)
                    )
                    Sound.play(Sound.enter)
                    return "ingame"
                elif key == pygame.K_u:
                    self.undo()
                    return "ingame"
                elif key == pygame.K_h:
                    self.hint()
                    return "ingame"
                elif key == pygame.K_c:
                    self.ask_clear = True
                    Sound.play(Sound.enter)
                    return "ingame"
            if self.selected:
                if button == "\x08" or button == "\x7f": # backspace, delete
                    button = "0"
                if button in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    if self.selected in self.__fixed:
                        Sound.play(Sound.forbidden)
                        return "ingame"
                    undo_code = 2 * (int(button) != self.puzzle.get_num(self.selected)
                                    ) + (self.guessing ^ (self.selected in self.guesses))
                    if undo_code & 2 and int(button):
                        self.moves += 1
                    if undo_code == 1:
                        self.undos.append((self.selected, None, True))
                    elif undo_code == 2:
                        self.undos.append(
                            (self.selected, self.puzzle.get_num(self.selected), False))
                    elif undo_code == 3:
                        self.undos.append(
                            (self.selected, self.puzzle.get_num(self.selected), True))

                    if self.guessing:
                        self.guesses.add(self.selected)
                    else:
                        self.guesses.discard(self.selected)
                    if int(button) != self.puzzle.get_num(self.selected):
                        self.hinted, self.hint_mode = None, None
                        if self.puzzle.change_block(self.selected, int(button)):
                            self.solved = True
                            self.show_result = True
                            self.selected = None
                            self.hinted, self.hint_mode = None, None
                            self.guesses.clear()
                            self.total_time = int(time() - self.time)
                            if self.total_time < 6000:
                                self.result_time_text = Objects(Font.bar.render(
                                    f"{self.total_time // 60:02}:{self.total_time % 60:02}", False, (0, 0, 0)
                                ), "rel_center", (19, -38))
                            else:
                                self.result_time_text = Objects(Font.bar.render(
                                    "99:59", False, (0, 0, 0)
                                ), "rel_center", (19, -38))
                            self.result_moves_text = Objects(Font.bar.render(
                                f"{min(self.moves, 999):03}", False, (0, 0, 0)
                            ), "rel_center", (19, -8))
                            self.result_hints_text = Objects(Font.bar.render(
                                f"{min(self.used_hints, 999):03}", False, (0, 0, 0)
                            ), "rel_center", (19, 22))
                            self.result_correct_moves_text = Objects(Font.bar.render(
                                f"Correct Moves: {int((81 - len(self.__fixed)) * 100 / self.moves)}%", False, (0, 0, 0)
                            ), "rel_center", (0, 55))
                            Sound.play(Sound.finish)
                            return "save_log"
                    return "ingame"
                else:
                    if key == pygame.K_LEFT:
                        if self.selected[0] > 0:
                            self.selected = (self.selected[0] - 1, self.selected[1])
                    elif key == pygame.K_RIGHT:
                        if self.selected[0] < 8:
                            self.selected = (self.selected[0] + 1, self.selected[1])
                    elif key == pygame.K_UP:
                        if self.selected[1] > 0:
                            self.selected = (self.selected[0], self.selected[1] - 1)
                    elif key == pygame.K_DOWN:
                        if self.selected[1] < 8:
                            self.selected = (self.selected[0], self.selected[1] + 1)
                    return "ingame"
        return "ingame"