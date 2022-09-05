from objects import *
from formats import save_format
import json

class Saves:
    def __init__(self):
        self.temp_saves = [None, None, None]
        try:
            with open(".\\saves.json", "r") as save_file:
                saves = json.load(save_file)
                if not isinstance(saves, list) or not len(saves) == 3:
                    self.temp_saves = [None, None, None]
                    return
                for i in range(3):
                    self.temp_saves[i] = save_format(saves[i], i)
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass
    
    def __bool__(self):
        return bool(self.temp_saves[0] or self.temp_saves[1] or self.temp_saves[2])

    def save_game_saves(self):
        with open(".\\saves.json", "w") as save_file:
            json.dump(self.temp_saves, save_file, indent = 4)
    
    def clear(self):
        self.temp_saves = [None, None, None]
        self.save_game_saves()

class HomePage:
    # home page
    title = Objects(Font.title.render("Sudoku", False, (0, 0, 0)), "scale", (0.5, 1/6))
    bar_Start_Game = Objects(Texture.select_bar, "rel_center", (0, 0))
    bar_text_Start_Game = Objects(Font.bar.render("Start Game", False, (0, 0, 0)), "rel_center", (0, 3))
    bar_Records = Objects(Texture.select_bar, "rel_center", (0, 60))
    bar_text_Records = Objects(Font.bar.render("Records", False, (0, 0, 0)), "rel_center", (0, 60))
    bar_Options = Objects(Texture.select_bar, "rel_center", (0, 120))
    bar_text_Options = Objects(Font.bar.render("Options", False, (0, 0, 0)), "rel_center", (0, 120))
    bar_Quit_Game = Objects(Texture.select_bar, "rel_center", (0, 180))
    bar_text_Quit_Game = Objects(Font.bar.render("Quit Game", False, (0, 0, 0)), "rel_center", (0, 183))

    # difficultiy select
    text_Difficulty = Objects(Font.bar.render("Difficulty", False, (0, 0, 0)), "rel_center", (0, 30))
    bar_text_Easy = Objects(Font.bar.render("Easy", False, (0, 0, 0)), "rel_center", (0, 60))
    bar_text_Normal = Objects(Font.bar.render("Normal", False, (0, 0, 0)), "rel_center", (0, 60))
    bar_text_Hard = Objects(Font.bar.render("Hard", False, (0, 0, 0)), "rel_center", (0, 60))
    bar_Clear_Saves = Objects(Texture.select_bar, "rel_center", (-105, 120))
    bar_Clear_Saves_locked = Objects(Texture.select_bar_locked, "rel_center", (-105, 120))
    bar_Cancel = Objects(Texture.select_bar, "rel_center", (-105, 180))
    bar_Continue = Objects(Texture.select_bar, "rel_center", (105, 120))
    bar_Continue_locked = Objects(Texture.select_bar_locked, "rel_center", (105, 120))
    bar_New_Game = Objects(Texture.select_bar, "rel_center", (105, 180))
    bar_text_Clear_Saves = Objects(
        Font.bar.render("Clear Saves", False, (0, 0, 0)), "rel_center", (-105, 123)
    )
    bar_text_Cancel = Objects(Font.bar.render("Cancel", False, (0, 0, 0)), "rel_center", (-105, 180))
    bar_text_Continue = Objects(Font.bar.render("Continue", False, (0, 0, 0)), "rel_center", (105, 120))
    bar_text_New_Game = Objects(Font.bar.render("New Game", False, (0, 0, 0)), "rel_center", (105, 183))
    difficulty_left_arrow = Objects(Texture.difficulty_left_arrow, "rel_center", (-70, 60))
    difficulty_right_arrow = Objects(Texture.difficulty_right_arrow, "rel_center", (70, 60))

    mask = pygame.Surface((1280, 720))
    mask.set_alpha(220)
    mask = Objects(mask, "default", (0, 0))
    dialog_box = Objects(Texture.dialog_box, "rel_center", (0, 0))
    dialog_clear_1 = Objects(
        Font.bar.render("Are you sure to clear all the", False, (0, 0, 0)), "rel_center", (0, -41)
    )
    dialog_clear_2 = Objects(Font.bar.render("game saves?", False, (0, 0, 0)), "rel_center", (0, -13))
    dialog_start_1 = Objects(
        Font.bar.render("Are you sure to start a new", False, (0, 0, 0)), "rel_center", (0, -55)
    )
    dialog_start_2 = Objects(
        Font.bar.render("game? The game save will be", False, (0, 0, 0)), "rel_center", (0, -27)
    )
    dialog_start_3 = Objects(Font.bar.render("overwritten.", False, (0, 0, 0)), "rel_center", (0, 1))
    button_Cancel = Objects(Texture.dialog_button, "rel_center",(-79, 51))
    button_Yes = Objects(Texture.dialog_button, "rel_center", (79, 51))
    button_text_Cancel = Objects(Font.bar.render("Cancel", False, (0, 0, 0)), "rel_center", (-79, 51))
    button_text_Yes = Objects(Font.bar.render("Yes", False, (0, 0, 0)), "rel_center", (79, 51))

    def __init__(self):
        self.difficulty = 1
        self.state = "home"
        self.saves = Saves()
        self.ask_clear = False
        self.ask_start = False

    def get_saves(self):
        return self.saves.temp_saves[self.difficulty - 1]
    
    def update_saves(self, save: dict | None):
        self.saves.temp_saves[self.difficulty - 1] = save
        self.saves.save_game_saves()
    
    def has_saves(self): # At this difficulty. For all saves, use bool(self.saves)
        return bool(self.saves.temp_saves[self.difficulty - 1])

    def show_screen(self, screen: pygame.Surface):
        if self.state == "home":
            self.show_home_page(screen)
        elif self.state == "difficulty_select":
            self.show_difficulty_select(screen)
        else:
            raise Exception(f'HomePage.state should be "home" or "difficulty_select", but get {self.state}')

    def action(self, control: Control):
        if self.state == "home":
            return self.home_page_select(control)
        elif self.state == "difficulty_select":
            return self.difficulty_select(control)
        else:
            raise Exception(f'HomePage.state should be "home" or "difficulty_select", but get {self.state}')

    def show_home_page(self, screen: pygame.Surface):
        Objects.multi_display(screen,
            Background.background,
            self.title,
            self.bar_Start_Game,
            self.bar_Records,
            self.bar_Options,
            self.bar_Quit_Game,
            self.bar_text_Start_Game,
            self.bar_text_Records,
            self.bar_text_Options,
            self.bar_text_Quit_Game,
        )

    def home_page_select(self, control: Control):
        if control.click_in(self.bar_Start_Game):
            self.state = "difficulty_select"
            Sound.play(Sound.enter)
            return "home"
        elif control.click_in(self.bar_Records):
            Sound.play(Sound.enter)
            return "records"
        elif control.click_in(self.bar_Options):
            Sound.play(Sound.enter)
            return "options"
        elif control.click_in(self.bar_Quit_Game):
            return "quit"

        return "home"

    def show_difficulty_select(self, screen: pygame.Surface):
        Objects.multi_display(screen,
            Background.background,
            self.title,
            self.text_Difficulty,
            self.bar_Records,
            self.bar_Cancel,
            self.bar_New_Game,
            self.bar_text_Cancel,
            self.bar_text_New_Game
        )
        if self.has_saves(): self.bar_Continue.display(screen)
        else: self.bar_Continue_locked.display(screen)
        self.bar_text_Continue.display(screen)
        if self.saves: self.bar_Clear_Saves.display(screen)
        else: self.bar_Clear_Saves_locked.display(screen)
        self.bar_text_Clear_Saves.display(screen)

        if self.difficulty == 1:
            Objects.multi_display(screen, self.bar_text_Easy, self.difficulty_right_arrow)
        elif self.difficulty == 2:
            Objects.multi_display(screen, self.bar_text_Normal, self.difficulty_left_arrow, self.difficulty_right_arrow)
        elif self.difficulty == 3:
            Objects.multi_display(screen, self.bar_text_Hard, self.difficulty_left_arrow)
        
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
        
        elif self.ask_start:
            Objects.multi_display(screen,
                self.mask,
                self.dialog_box,
                self.dialog_start_1,
                self.dialog_start_2,
                self.dialog_start_3,
                self.button_Cancel,
                self.button_Yes,
                self.button_text_Cancel,
                self.button_text_Yes
            )

    def difficulty_select(self, control: Control):
        if self.ask_clear:
            if control.click_in(self.button_Cancel):
                self.ask_clear = False
            elif control.click_in(self.button_Yes):
                self.saves.clear()
                self.ask_clear = False
                Sound.play(Sound.enter)
            return "home"

        elif self.ask_start:
            if control.click_in(self.button_Cancel):
                self.ask_start = False
                return "home"
            elif control.click_in(self.button_Yes):
                self.update_saves(None)
                self.ask_start = False
                Sound.play(Sound.enter)
                return "start"

        else:
            if control.click_in(self.bar_Cancel):
                self.state = "home"
                return "home"
            elif control.click_in(self.bar_Clear_Saves):
                if self.saves:
                    self.ask_clear = True
                    Sound.play(Sound.enter)
                else:
                    Sound.play(Sound.forbidden)
                return "home"
            elif control.click_in(self.bar_New_Game):
                if self.has_saves():
                    self.ask_start = True
                    Sound.play(Sound.enter)
                    return "home"
                else:
                    Sound.play(Sound.enter)
                    return "start"
            elif control.click_in(self.bar_Continue):
                if self.has_saves():
                    Sound.play(Sound.enter)
                    return "continue"
                else:
                    Sound.play(Sound.forbidden)
                    return "home"
            elif control.click_in(self.difficulty_left_arrow) and self.difficulty >= 2:
                self.difficulty -= 1
                Sound.play(Sound.enter)
            elif control.click_in(self.difficulty_right_arrow) and self.difficulty <= 2:
                self.difficulty += 1
                Sound.play(Sound.enter)
            
        return "home"
