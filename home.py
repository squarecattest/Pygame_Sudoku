from objects import *
import align

class HomePage:
    # home page
    title = Font.title.render("Sudoku", False, (0, 0, 0))
    bar_Start_Game = Interactable(Texture.select_bar, (560, 330))
    bar_text_Start_Game = Font.bar.render("Start Game", False, (0, 0, 0))
    bar_Records = Interactable(Texture.select_bar, (560, 390))
    bar_text_Records = Font.bar.render("Records", False, (0, 0, 0))
    bar_Options = Interactable(Texture.select_bar, (560, 450))
    bar_text_Options = Font.bar.render("Options", False, (0, 0, 0))
    bar_Quit_Game = Interactable(Texture.select_bar, (560, 510))
    bar_text_Quit_Game = Font.bar.render("Quit Game", False, (0, 0, 0))

    # difficultiy select
    text_Difficulty = Font.bar.render("Difficulty", False, (0, 0, 0))
    bar_text_Easy = Font.bar.render("Easy", False, (0, 0, 0))
    bar_text_Normal = Font.bar.render("Normal", False, (0, 0, 0))
    bar_text_Hard = Font.bar.render("Hard", False, (0, 0, 0))
    bar_Cancel = Interactable(Texture.select_bar, (455, 510))
    bar_text_Cancel = Font.bar.render("Cancel", False, (0, 0, 0))
    bar_Start = Interactable(Texture.select_bar, (665, 510))
    bar_text_Start = Font.bar.render("Start", False, (0, 0, 0))
    difficulty_left_arrow = Interactable(Texture.difficulty_left_arrow, (482, 390))
    difficulty_right_arrow = Interactable(Texture.difficulty_right_arrow, (637, 390))

    def __init__(self):
        self.difficulty = 1
        self.state = "home"
    
    def show_screen(self, screen: pygame.Surface):
        if self.state == "home": self.show_home_page(screen)
        elif self.state == "difficulty_select": self.show_difficulty_select(screen)
        else: raise Exception(f'HomePage.state should be "home" or "difficulty_select", but get {self.state}')

    def action(self, event: pygame.event.Event):
        if self.state == "home": return self.home_page_select(event)
        elif self.state == "difficulty_select": return self.difficulty_select(event)
        else: raise Exception(f'HomePage.state should be "home" or "difficulty_select", but get {self.state}')

    def show_home_page(self, screen: pygame.Surface):
        align.default(screen, Image.background, (0, 0))
        align.center(screen, self.title, (560, 105))
        align.center(screen, *self.bar_Start_Game)
        align.center(screen, *self.bar_Records)
        align.center(screen, *self.bar_Options)
        align.center(screen, *self.bar_Quit_Game)
        align.center(screen, self.bar_text_Start_Game, (560, 333))
        align.center(screen, self.bar_text_Records, (560, 390))
        align.center(screen, self.bar_text_Options, (560, 450))
        align.center(screen, self.bar_text_Quit_Game, (560, 513))

    def home_page_select(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.__dict__.get("button") == 1:
            pos = event.__dict__.get("pos", (0, 0))
            if align.in_centered_object(pos, *self.bar_Start_Game):
                self.state = "difficulty_select"
                Sound.play(Sound.enter)
                return "home"
            elif align.in_centered_object(pos, *self.bar_Records):
                Sound.play(Sound.enter)
                return "records"
            elif align.in_centered_object(pos, *self.bar_Options):
                Sound.play(Sound.enter)
                return "options"
            elif align.in_centered_object(pos, *self.bar_Quit_Game):
                return "quit"
        return "home"
    
    def show_difficulty_select(self, screen: pygame.Surface):
        align.default(screen, Image.background, (0, 0))
        align.center(screen, self.title, (560, 105))
        align.center(screen, Texture.select_bar, (560, 390))
        align.center(screen, *self.bar_Cancel)
        align.center(screen, *self.bar_Start)
        align.center(screen, self.text_Difficulty, (560, 360))
        align.center(screen, self.bar_text_Cancel, (455, 510))
        align.center(screen, self.bar_text_Start, (665, 510))
        if self.difficulty == 1:
            align.center(screen, self.bar_text_Easy, (560, 390))
            align.right(screen, *self.difficulty_right_arrow)
        elif self.difficulty == 2:
            align.center(screen, self.bar_text_Normal, (560, 390))
            align.left(screen, *self.difficulty_left_arrow)
            align.right(screen, *self.difficulty_right_arrow)
        elif self.difficulty == 3:
            align.center(screen, self.bar_text_Hard, (560, 390))
            align.left(screen, *self.difficulty_left_arrow)

    def difficulty_select(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.__dict__.get("button") == 1:
            pos = event.__dict__.get("pos", (0, 0))
            if align.in_centered_object(pos, Texture.select_bar, (455, 510)):
                self.state = "home"
                return "home"
            elif align.in_centered_object(pos, Texture.select_bar, (665, 510)):
                Sound.play(Sound.enter)
                return "start"
            elif align.in_left_centered_object(pos, *self.difficulty_left_arrow) and self.difficulty >= 2:
                Sound.play(Sound.enter)
                self.difficulty -= 1
            elif align.in_right_centered_object(pos, *self.difficulty_right_arrow) and self.difficulty <= 2:
                Sound.play(Sound.enter)
                self.difficulty += 1
        return "home"