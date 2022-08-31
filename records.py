from objects import *
import align
import json
from time import localtime

class RecordPage:
    title = Font.title.render("Records", False, (0, 0, 0))
    record_text_format = Font.bar.render("Difficulty  |  Game Time  |  Date Time", False, (111, 111, 111))
    record_text_sep = Font.bar.render("|", False, (111, 111, 111))
    record_text_empty = Font.bar.render("---", False, (255, 255, 255))
    record_text_invalid = Font.bar.render("Invalid Record", False, (255, 0, 0))
    bar_Clear = Interactable(Texture.select_bar, (560, 570))
    bar_Back = Interactable(Texture.select_bar, (560, 605))
    bar_text_Clear = Font.bar.render("Clear Records", False, (0, 0, 0))
    bar_text_Back = Font.bar.render("Back", False, (0, 0, 0))
    icon_previous_page = Interactable(Texture.record_left_arrow, (450, 605))
    icon_next_page = Interactable(Texture.record_right_arrow, (670, 605))
    
    mask = pygame.Surface((1120, 630))
    mask.set_alpha(220)
    dialog_clear_1 = Font.bar.render("Are you sure to clear all the", False, (0, 0, 0))
    dialog_clear_2 = Font.bar.render("records?", False, (0, 0, 0))
    button_Cancel = Interactable(Texture.dialog_button, (481, 366))
    button_Yes = Interactable(Texture.dialog_button, (639, 366))
    bar_text_Cancel = Font.bar.render("Cancel", False, (0, 0, 0))
    bar_text_Yes = Font.bar.render("Yes", False, (0, 0, 0))

    def __init__(self):
        self.logs = []
        try:
            with open(".\\log.json", "r") as log_file:
                self.logs = json.load(log_file)
                if not isinstance(self.logs, list): self.logs = []
        except FileNotFoundError: pass
        except json.decoder.JSONDecodeError: pass
        self.current_page = 1
        self.pages = (len(self.logs) - 1) // 10 + 1 or 1
        self.ask_clear = False
    
    def output_log(self):
        for i in range(len(self.logs) - 100): self.logs.pop()
        with open(".\\log.json", "w") as log_file: json.dump(self.logs, log_file, indent = 4)
    
    def add_log(self, difficulty: int, game_time: int, time: int):
        self.logs.insert(0, {"difficulty": difficulty, "game_time": game_time, "time": time})
        for i in range(len(self.logs) - 100): self.logs.pop()
        self.pages = (len(self.logs) - 1) // 10 + 1 or 1
    
    def clear_log(self):
        self.logs.clear()
        self.current_page = 1
        self.pages = 1

    def show_screen(self, screen: pygame.Surface):
        page = self.current_page
        difficulty = [0, "Easy", "Normal", "Hard"]
        align.default(screen, Image.background, (0, 0))
        align.center(screen, self.title, (560, 105))
        align.center(screen, *self.bar_Clear)
        align.center(screen, self.bar_text_Clear, (self.bar_Clear.pos[0], self.bar_Clear.pos[1] + 3))
        align.center(screen, *self.bar_Back)
        align.center(screen, self.bar_text_Back, self.bar_Back.pos)
        align.center(screen, Texture.record_bar, (560, 222))
        align.center(screen, self.record_text_format, (560, 223))
        align.center(screen, Texture.record_bar, (280, 288))
        align.center(screen, Texture.record_bar, (280, 354))
        align.center(screen, Texture.record_bar, (280, 420))
        align.center(screen, Texture.record_bar, (280, 486))
        align.center(screen, Texture.record_bar, (280, 552))
        align.center(screen, Texture.record_bar, (840, 288))
        align.center(screen, Texture.record_bar, (840, 354))
        align.center(screen, Texture.record_bar, (840, 420))
        align.center(screen, Texture.record_bar, (840, 486))
        align.center(screen, Texture.record_bar, (840, 552))
        logs = self.logs[(page - 1) * 10:page * 10]
        for i in range(10):
            dx, dy = 560 * (i > 4), 66 * (i % 5)
            if i < len(logs):
                log = log_format(logs[i])
                if log == None:
                    align.center(screen, self.record_text_invalid, (280 + dx, 291 + dy))
                else:
                    align.center(screen, Font.bar.render(difficulty[log[0]], False, (255, 255, 255)), (154 + dx, 288 + dy))
                    align.center(screen, Font.bar.render(log[1], False, (255, 255, 255)), (225 + dx, 288 + dy))
                    align.center(screen, Font.bar.render(log[2], False, (255, 255, 255)), (351 + dx, 291 + dy))
                    align.center(screen, self.record_text_sep, (194 + dx, 288 + dy))
                    align.center(screen, self.record_text_sep, (258 + dx, 288 + dy))
            else:
                align.center(screen, self.record_text_empty, (280 + dx, 287 + dy))
        
        align.center(screen, Font.bar.render(f"Page {page:02}/{min(self.pages, 10):02}", False, (0, 0, 0)), (560, 545))
        if page <= 1: align.center(screen, Texture.record_left_arrow_unavailable, self.icon_previous_page.pos)
        else: align.center(screen, *self.icon_previous_page)
        if page >= min(self.pages, 10): align.center(screen, Texture.record_right_arrow_unavailable, self.icon_next_page.pos)
        else: align.center(screen, *self.icon_next_page)
        
        if self.ask_clear:
            align.default(screen, self.mask, (0, 0))
            align.center(screen, Texture.dialog_box, (560, 315))
            align.center(screen, self.dialog_clear_1, (560, 274))
            align.center(screen, self.dialog_clear_2, (560, 302))
            align.center(screen, *self.button_Cancel)
            align.center(screen, *self.button_Yes)
            align.center(screen, self.bar_text_Cancel, self.button_Cancel.pos)
            align.center(screen, self.bar_text_Yes, self.button_Yes.pos)
    
    def action(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.__dict__.get("button") == 1:
            pos = event.__dict__.get("pos", (0, 0))
            if self.ask_clear:
                if align.in_centered_object(pos, *self.button_Cancel):
                    self.ask_clear = False
                elif align.in_centered_object(pos, *self.button_Yes):
                    self.clear_log()
                    self.ask_clear = False
                    Sound.play(Sound.enter)
            else:
                if align.in_centered_object(pos, *self.bar_Back):
                    return "home"
                if align.in_centered_object(pos, *self.bar_Clear):
                    self.ask_clear = True
                    Sound.play(Sound.enter)
                elif align.in_centered_object(pos, *self.icon_previous_page):
                    if self.current_page > 1:
                        Sound.play(Sound.turn_page)
                        self.current_page -= 1
                    else: Sound.play(Sound.forbidden)
                elif align.in_centered_object(pos, *self.icon_next_page):
                    if self.current_page < min(self.pages, 10):
                        Sound.play(Sound.turn_page)
                        self.current_page += 1
                    else: Sound.play(Sound.forbidden)
        return "records"

def log_format(log: dict):
    if not isinstance(log, dict): return None
    difficulty = log.get("difficulty")
    if not difficulty in [1, 2, 3]: return None
    game_time = log.get("game_time")
    if not isinstance(game_time, int) or not game_time >= 0: return None
    date_time = log.get("time")
    if not isinstance(date_time, (int, float)) or not date_time >= 0: return None

    if game_time < 6000: game_time = f"{game_time // 60:02}:{game_time % 60:02}"
    else: game_time = "99:59"
    date_time = localtime(date_time)
    date_time = f"{date_time.tm_year}-{date_time.tm_mon:02}-{date_time.tm_mday:02} {date_time.tm_hour:02}:{date_time.tm_min:02}"
    return (difficulty, game_time, date_time)