from itertools import product
from time import time
from objects import *
import align
import sudoku

class Sudoku:
    def __init__(self, __puzzle: list[list[int]]):
        self.__puzzle, self.__fixed = [], []
        for i in range(9):
            self.__puzzle.append(__puzzle[i].copy())
            for j in range(9):
                if __puzzle[i][j]: self.__fixed.append((i, j))

    def possibilities(self, block: tuple[int]):
        def index_to_row(index: int):
            return tuple((index, j) for j in range(9) if j != block[1])

        def index_to_column(index: int):
            return tuple((i, index) for i in range(9) if i != block[0])

        def index_to_square(block: tuple[int]):
            i, j = (block[0] // 3) * 3, (block[1] // 3) * 3
            return tuple((i + k, j + l) for k, l in product(range(3), range(3)) if (i + k, j + l) != block)
        num_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for i, j in index_to_row(block[0]):
            num_set.discard(self.__puzzle[i][j])
        for i, j in index_to_column(block[1]):
            num_set.discard(self.__puzzle[i][j])
        for i, j in index_to_square(block):
            num_set.discard(self.__puzzle[i][j])
        return num_set
    
    def get_hint_block(self):
        def index_to_row(block: tuple[int]):
            return tuple((block[0], j) for j in range(9) if j != block[1])

        def index_to_column(block: tuple[int]):
            return tuple((i, block[1]) for i in range(9) if i != block[0])

        def index_to_square(block: tuple[int]):
            i, j = (block[0] // 3) * 3, (block[1] // 3) * 3
            return tuple((i + k, j + l) for k, l in product(range(3), range(3)) if (i + k, j + l) != block)

        def only_left(block: tuple[int]):
            for i, j in index_to_row(block):
                if not self.__puzzle[i][j]: break
            else: return True
            for i, j in index_to_column(block):
                if not self.__puzzle[i][j]: break
            else: return True
            for i, j in index_to_square(block):
                if not self.__puzzle[i][j]: break
            else: return True
            return False
        
        def only_placable(block: tuple[int]):
            for num in self.possibilities(block):
                for i, j in index_to_row(block):
                    if not self.__puzzle[i][j] and num in self.possibilities((i, j)): break
                else: return True
                for i, j in index_to_column(block):
                    if not self.__puzzle[i][j] and num in self.possibilities((i, j)): break
                else: return True
                for i, j in index_to_square(block):
                    if not self.__puzzle[i][j] and num in self.possibilities((i, j)): break
                else: return True
            return False
        # prior
        for i, j in product(range(9), range(9)):
            if not self.__puzzle[i][j] and only_left((i, j)): return (i, j)
        # second
        for i, j in product(range(9), range(9)):
            if not self.__puzzle[i][j] and len(self.possibilities((i, j))) == 1: return (i, j)
        # posterior
        for i, j in product(range(9), range(9)):
            if not self.__puzzle[i][j] and only_placable((i, j)): return (i, j)
        return None

    def __check_solved(self):
        for i, j in product(range(9), range(9)):
            if not self.__puzzle[i][j]: return False
            if not self.__puzzle[i][j] in self.possibilities((i, j)): return False
        return True

    def change_block(self, block: tuple[int], num: int):
        '''
        return True if the puzzle is solved after changing.

        return False if the puzzle is not solved.
        '''
        self.__puzzle[block[0]][block[1]] = num
        return self.__check_solved()

    def get_puzzle(self):
        return self.__puzzle

    def get_num(self, block: tuple[int]):
        return self.__puzzle[block[0]][block[1]]

    def get_fixed(self):
        return self.__fixed

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
    bar_Mode = Interactable(Texture.select_bar_ingame, (840, 195))
    bar_Undo = Interactable(Texture.select_bar_ingame, (840, 243))
    bar_Hint = Interactable(Texture.select_bar_ingame, (840, 291))
    bar_Clear = Interactable(Texture.select_bar_ingame, (840, 339))
    bar_Solve = Interactable(Texture.select_bar_ingame, (840, 387))
    bar_Back = Interactable(Texture.select_bar_ingame, (840, 435))
    bar_text_Mode = Font.bar.render("Mode:  Enter", False, (0, 0, 0))
    bar_text_Undo = Font.bar.render("Undo", False, (0, 0, 0))
    bar_text_Hint = Font.bar.render("Hint", False, (0, 0, 0))
    bar_text_Clear = Font.bar.render("Clear", False, (0, 0, 0))
    bar_text_Solve = Font.bar.render("Solve  by  Bot", False, (0, 0, 0))
    bar_text_Back = Font.bar.render("Back  to  Title  Screen", False, (0, 0, 0))
    mask = pygame.Surface((1120, 630))
    mask.set_alpha(220)
    dialog_clear_1 = Font.bar.render("Are you sure to clear up the", False, (0, 0, 0))
    dialog_clear_2 = Font.bar.render("puzzle? (Timer will not reset.)", False, (0, 0, 0))
    dialog_solve_1 = Font.bar.render("Are you sure to solve this", False, (0, 0, 0))
    dialog_solve_2 = Font.bar.render("puzzle by bot? The record will", False, (0, 0, 0))
    dialog_solve_3 = Font.bar.render("not be saved.", False, (0, 0, 0))
    dialog_back_1 = Font.bar.render("Are you sure to return to title", False, (0, 0, 0))
    dialog_back_2 = Font.bar.render( "screen? The record will not be", False, (0, 0, 0))
    dialog_back_3 = Font.bar.render("saved.", False, (0, 0, 0))
    button_Cancel = Interactable(Texture.dialog_button, (481, 366))
    button_Yes = Interactable(Texture.dialog_button, (639, 366))
    bar_text_Cancel = Font.bar.render("Cancel", False, (0, 0, 0))
    bar_text_Yes = Font.bar.render("Yes", False, (0, 0, 0))

    def __init__(self, difficulty: int):
        self.difficulty = difficulty
        self.difficulty_text = Font.subtitle.render(
            "Difficulty: " + ["Easy", "Normal", "Hard"][difficulty - 1], False, (0, 0, 0))
        self.__original = sudoku.random_create(difficulty)
        self.puzzle = Sudoku(self.__original)
        self.__fixed = self.puzzle.get_fixed()
        self.undos = [] # [(block: tuple, before changed num: int|None, reverse: bool), (), ...]
        self.time = time()
        self.selected = None
        self.hinted = None
        self.guessing = False
        self.guesses = set()
        self.solved = False
        self.solved_by_bot = False
        self.ask_clear = False
        self.ask_solve = False
        self.ask_quit = False

    def select_block(self, block: tuple[int]):
        if block in self.__fixed: return None
        return block
    
    def undo(self):
        if self.undos:
            block, num, reverse = self.undos.pop()
            if num != None: self.puzzle.change_block(block, num)
            if reverse: self.guesses.symmetric_difference_update({block})
            self.selected = block
            self.hinted = None
            Sound.play(Sound.enter)
        else: Sound.play(Sound.forbidden)
    
    def clear(self):
        for i, j in product(range(9), range(9)):
            if not (i, j) in self.__fixed: self.puzzle.change_block((i, j), 0)
        self.selected = None
        self.hinted = None
        self.undos.clear()

    def solve_by_bot(self):
        try:
            self.puzzle.solve()
        except sudoku.Unsolvable:
            self.puzzle = Sudoku(self.__original)
            self.puzzle.solve()
        self.solved = True
        self.solved_by_bot = True
        self.selected = None
        self.hinted = None
        self.guesses.clear()
        self.total_time = int(time() - self.time)

    def show_screen(self, screen: pygame.Surface):
        align.default(screen, Image.background, (0, 0))
        align.center(screen, Texture.block, (168, 203))
        align.center(screen, Texture.block, (168, 315))
        align.center(screen, Texture.block, (168, 427))
        align.center(screen, Texture.block, (280, 203))
        align.center(screen, Texture.block, (280, 315))
        align.center(screen, Texture.block, (280, 427))
        align.center(screen, Texture.block, (392, 203))
        align.center(screen, Texture.block, (392, 315))
        align.center(screen, Texture.block, (392, 427))
        puzzle_nums = self.puzzle.get_puzzle()
        for i, j in product(range(9), range(9)):
            dx, dy = 36 * i + 4 * (i // 3), 36 * j + 4 * (j // 3)
            pos = (132 + dx, 167 + dy)
            num = puzzle_nums[i][j]
            if (i, j) in self.__fixed: align.center(screen, self.number_fixed[num], pos)
            elif puzzle_nums[i][j]:
                if puzzle_nums[i][j] in self.puzzle.possibilities((i, j)):
                    if (i, j) in self.guesses: align.center(screen, self.number_guessed[num], pos)
                    else: align.center(screen, self.number_entered[num], pos)
                else: align.center(screen, self.number_repeated[num], pos)
        if self.selected != None:
            dx, dy = 36 * self.selected[0] + 4 * (self.selected[0] // 3), 36 * self.selected[1] + 4 * (self.selected[1] // 3)
            pos = (132 + dx, 167 + dy)
            align.center(screen, self.selected_block, pos)
        if self.hinted != None:
            dx, dy = 36 * self.hinted[0] + 4 * (self.hinted[0] // 3), 36 * self.hinted[1] + 4 * (self.hinted[1] // 3)
            pos = (132 + dx, 167 + dy)
            align.center(screen, self.hint_block, pos)

        align.center(screen, self.difficulty_text, (840, 105))
        align.center(screen, Texture.timer, (798, 135))
        if self.solved: passed_time = self.total_time
        else: passed_time = int(time() - self.time)
        if passed_time < 6000: align.center(screen, Font.subtitle.render(f"{passed_time // 60:02}:{passed_time % 60:02}", False, (0, 0, 0)), (858, 137))
        else: align.center(screen, Font.subtitle.render("99:59", False, (0, 0, 0)), (858, 137))

        align.center(screen, *self.bar_Mode)
        align.center(screen, *self.bar_Undo)
        align.center(screen, *self.bar_Hint)
        align.center(screen, *self.bar_Clear)
        align.center(screen, *self.bar_Solve)
        align.center(screen, *self.bar_Back)
        align.center(screen, self.bar_text_Mode, (self.bar_Mode.pos[0], self.bar_Mode.pos[1] + 3))
        align.center(screen, self.bar_text_Undo, self.bar_Undo.pos)
        align.center(screen, self.bar_text_Hint, self.bar_Hint.pos)
        align.center(screen, self.bar_text_Clear, self.bar_Clear.pos)
        align.center(screen, self.bar_text_Solve, (self.bar_Solve.pos[0], self.bar_Solve.pos[1] + 3))
        align.center(screen, self.bar_text_Back, (self.bar_Back.pos[0], self.bar_Back.pos[1] + 3))

        if self.ask_clear:
            align.default(screen, self.mask, (0, 0))
            align.center(screen, Texture.dialog_box, (560, 315))
            align.center(screen, self.dialog_clear_1, (560, 274))
            align.center(screen, self.dialog_clear_2, (560, 302))
            align.center(screen, *self.button_Cancel)
            align.center(screen, *self.button_Yes)
            align.center(screen, self.bar_text_Cancel, self.button_Cancel.pos)
            align.center(screen, self.bar_text_Yes, self.button_Yes.pos)

        if self.ask_solve:
            align.default(screen, self.mask, (0, 0))
            align.center(screen, Texture.dialog_box, (560, 315))
            align.center(screen, self.dialog_solve_1, (560, 260))
            align.center(screen, self.dialog_solve_2, (560, 288))
            align.center(screen, self.dialog_solve_3, (560, 316))
            align.center(screen, *self.button_Cancel)
            align.center(screen, *self.button_Yes)
            align.center(screen, self.bar_text_Cancel, self.button_Cancel.pos)
            align.center(screen, self.bar_text_Yes, self.button_Yes.pos)

        if self.ask_quit:
            align.default(screen, self.mask, (0, 0))
            align.center(screen, Texture.dialog_box, (560, 315))
            align.center(screen, self.dialog_back_1, (560, 260))
            align.center(screen, self.dialog_back_2, (560, 288))
            align.center(screen, self.dialog_back_3, (560, 316))
            align.center(screen, *self.button_Cancel)
            align.center(screen, *self.button_Yes)
            align.center(screen, self.bar_text_Cancel, self.button_Cancel.pos)
            align.center(screen, self.bar_text_Yes, self.button_Yes.pos)
        
    def action(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.__dict__.get("button") == 1:
            pos = event.__dict__.get("pos", (0, 0))
            if not self.solved:
                if self.ask_clear:
                    if align.in_centered_object(pos, *self.button_Cancel):
                        self.ask_clear = False
                    elif align.in_centered_object(pos, *self.button_Yes):
                        self.clear()
                        self.ask_clear = False
                        Sound.play(Sound.enter)
                    return "ingame"
                elif self.ask_solve:
                    if align.in_centered_object(pos, *self.button_Cancel):
                        self.ask_solve = False
                    elif align.in_centered_object(pos, *self.button_Yes):
                        self.solve_by_bot()
                        Sound.play(Sound.enter)
                        self.ask_solve = False
                    return "ingame"
                elif self.ask_quit:
                    if align.in_centered_object(pos, *self.button_Cancel):
                        self.ask_quit = False
                        return "ingame"
                    elif align.in_centered_object(pos, *self.button_Yes):
                        Sound.play(Sound.enter)
                        return "home"
                    return "ingame"
                else:
                    if align.in_centered_object(pos, *self.bar_Mode):
                        self.guessing = not self.guessing
                        self.bar_text_Mode = Font.bar.render(f'Mode:  {["Enter", "Guess"][self.guessing]}', False, (0, 0, 0))
                        Sound.play(Sound.enter)
                    elif align.in_centered_object(pos, *self.bar_Undo):
                        self.undo()
                    elif align.in_centered_object(pos, *self.bar_Hint):
                        self.hinted = self.puzzle.get_hint_block()
                        if self.selected == None: self.selected = self.hinted
                        if self.hinted: Sound.play(Sound.enter)
                        else: Sound.play(Sound.forbidden)
                    elif align.in_centered_object(pos, *self.bar_Clear):
                        self.ask_clear = True
                        Sound.play(Sound.enter)
                    elif align.in_centered_object(pos, *self.bar_Solve):
                        self.ask_solve = True
                        Sound.play(Sound.enter)
                    elif align.in_centered_object(pos, *self.bar_Back):
                        self.ask_quit = True
                        Sound.play(Sound.enter)
                    else:
                        self.hinted = None
                        pos = (pos[0] - 116, pos[1] - 151)
                        if pos[0] % 112 <= 103 and (pos[0] % 112) % 36 <= 31 and pos[1] % 112 <= 103 and (pos[1] % 112) % 36 <= 31:
                            i, j = 3 * (pos[0] // 112) + (pos[0] % 112) // 36, 3 * (pos[1] // 112) + (pos[1] % 112) // 36
                            if 0 <= i <= 8 and 0 <= j <= 8:
                                self.selected = self.select_block((i, j))
                                return "ingame"
                        self.selected = None
                    return "ingame"
            elif align.in_centered_object(pos, *self.bar_Back):
                Sound.play(Sound.enter)
                return "save"
                
        elif event.type == pygame.KEYDOWN and self.selected != None:
            button = event.__dict__.get("unicode")
            if button == "\x08" or button == "\x7f": button = "0"
            if button in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                undo_code = 2 * (int(button) != self.puzzle.get_num(self.selected)) + (self.guessing ^ (self.selected in self.guesses))
                if undo_code == 1:
                    self.undos.append((self.selected, None, True))
                if undo_code == 2:
                    self.undos.append((self.selected, self.puzzle.get_num(self.selected), False))
                if undo_code == 3:
                    self.undos.append((self.selected, self.puzzle.get_num(self.selected), True))

                if self.guessing: self.guesses.add(self.selected)
                else: self.guesses.discard(self.selected)
                if int(button) != self.puzzle.get_num(self.selected):
                    self.hinted = None
                    if self.puzzle.change_block(self.selected, int(button)):
                        self.solved = True
                        self.selected = None
                        self.hinted = None
                        self.guesses.clear()
                        self.total_time = int(time() - self.time)
                        Sound.play(Sound.finish)
            else:
                direction = event.__dict__.get("key")
                temp_selected = list(self.selected)
                if direction == pygame.K_LEFT:
                    while(temp_selected[0] >= 1):
                        temp_selected[0] -= 1
                        if self.select_block(tuple(temp_selected)):
                            self.selected = tuple(temp_selected)
                            break
                elif direction == pygame.K_RIGHT:
                    while(temp_selected[0] <= 7):
                        temp_selected[0] += 1
                        if self.select_block(tuple(temp_selected)):
                            self.selected = tuple(temp_selected)
                            break
                elif direction == pygame.K_UP:
                    while(temp_selected[1] >= 1):
                        temp_selected[1] -= 1
                        if self.select_block(tuple(temp_selected)) != None:
                            self.selected = tuple(temp_selected)
                            break
                elif direction == pygame.K_DOWN:
                    while(temp_selected[1] <= 7):
                        temp_selected[1] += 1
                        if self.select_block(tuple(temp_selected)):
                            self.selected = tuple(temp_selected)
                            break
            return "ingame"
        return "ingame"
