from objects import *
from formats import log_format
import json

class Record:
    def __init__(self):
        self.logs = []
        try:
            with open(".\\log.json", "r") as log_file:
                self.logs = json.load(log_file)
                if not isinstance(self.logs, list):
                    self.logs = []
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass
        self.pages = (len(self.logs) - 1) // 10 + 1 or 1

    def save_log(self):
        for i in range(len(self.logs) - 100):
            self.logs.pop()
        with open(".\\log.json", "w") as log_file:
            json.dump(self.logs, log_file, indent = 4)

    def add_log(self, difficulty: int, game_time: int, moves: int, time: int):
        self.logs.insert(0, {
            "difficulty": difficulty,"game_time": game_time, "moves": moves, "time": time
        })
        for i in range(len(self.logs) - 100):
            self.logs.pop()
        self.pages = (len(self.logs) - 1) // 10 + 1 or 1
        self.save_log()

    def clear_log(self):
        self.logs.clear()
        self.save_log()
        self.pages = 1

class RecordPage:
    title = Objects(Font.title.render("Records", False, Color.title), "scale", (0.5, 1/6))
    record_bar_format = Objects(Texture.record_bar, "rel_center", (0, -93))
    record_text_format = Objects(Font.bar.render(
        "Difficulty  |  Game Time  |  Moves  |  Date Time", False, (111, 111, 111)), "rel_center", (0, -91)
    )
    bar_Clear = Objects(Texture.select_bar, "rel_bottom", (0, -45))
    bar_Clear_locked = Objects(Texture.select_bar_locked, "rel_bottom", (0, -45))
    bar_Back = Objects(Texture.select_bar, "rel_bottom", (0, -10))
    bar_text_Clear = Objects(Font.bar.render("Clear Records", False, Color.bar), "rel_bottom", (0, -43))
    bar_text_Clear_locked = Objects(
        Font.bar.render("Clear Records", False, Color.bar_locked), "rel_bottom", (0, -43)
    )
    bar_text_Back = Objects(Font.bar.render("Back", False, Color.bar), "rel_bottom", (0, -14))
    icon_previous_page = Objects(Texture.record_left_arrow, "rel_bottom",(-110, -3))
    icon_previous_page_unavailble = Objects(Texture.record_left_arrow_unavailable,
        "rel_bottom", (-110, -3)
    )
    icon_next_page = Objects(Texture.record_right_arrow, "rel_bottom", (110, -3))
    icon_next_page_unavailble = Objects(Texture.record_right_arrow_unavailable,
        "rel_bottom", (110, -3)
    )

    record_text_sep = Font.bar.render("|", False, (111, 111, 111))
    record_text_empty = Font.bar.render("---", False, Color.record)
    record_text_invalid = Font.bar.render("Invalid Record", False, Color.record_invalid)

    mask = pygame.Surface((1280, 720))
    mask.set_alpha(220)
    mask = Objects(mask, "default", (0, 0))
    dialog_box = Objects(Texture.dialog_box, "rel_center", (0, 0))
    dialog_clear_1 = Objects(
        Font.bar.render("Are you sure to clear all the", False, Color.bar), "rel_center", (0, -41)
    )
    dialog_clear_2 = Objects(Font.bar.render("records?", False, Color.bar), "rel_center", (0, -13))
    button_Cancel = Objects(Texture.dialog_button, "rel_center",(-79, 51))
    button_Yes = Objects(Texture.dialog_button, "rel_center", (79, 51))
    button_text_Cancel = Objects(Font.bar.render("Cancel", False, Color.bar), "rel_center", (-79, 51))
    button_text_Yes = Objects(Font.bar.render("Yes", False, Color.bar), "rel_center", (79, 51))

    def __init__(self):
        self.records = Record()
        self.current_page = 1
        self.ask_clear = False
    
    def reload(self):
        self.title.surface = Font.title.render("Records", False, Color.title)
        self.record_bar_format.surface = Texture.record_bar
        self.bar_Clear.surface = Texture.select_bar
        self.bar_Clear_locked.surface = Texture.select_bar_locked
        self.bar_Back.surface = Texture.select_bar
        self.bar_text_Clear.surface = Font.bar.render("Clear Records", False, Color.bar)
        self.bar_text_Clear_locked.surface = Font.bar.render("Clear Records", False, Color.bar_locked)
        self.bar_text_Back.surface = Font.bar.render("Back", False, Color.bar)
        self.record_text_empty = Font.bar.render("---", False, Color.record)
        self.record_text_invalid = Font.bar.render("Invalid Record", False, Color.record_invalid)
        self.dialog_box.surface = Texture.dialog_box
        self.dialog_clear_1.surface = Font.bar.render("Are you sure to clear all the", False, Color.bar)
        self.dialog_clear_2.surface = Font.bar.render("records?", False, Color.bar)
        self.button_Cancel.surface = Texture.dialog_button
        self.button_Yes.surface = Texture.dialog_button
        self.button_text_Cancel.surface = Font.bar.render("Cancel", False, Color.bar)
        self.button_text_Yes.surface = Font.bar.render("Yes", False, Color.bar)

    def show_screen(self):
        page = self.current_page
        Image.background.display()
        if Settings.night_mode: Snow.display()
        Objects.multi_display(
            self.title,
            self.record_bar_format,
            self.record_text_format,
            self.bar_Clear,
            self.bar_Back,
            self.bar_text_Clear,
            self.bar_text_Back
        )
        if self.records.logs:
            Objects.multi_display(
                self.bar_Clear,
                self.bar_text_Clear
            )
        else:
            Objects.multi_display(
                self.bar_Clear_locked,
                self.bar_text_Clear_locked
            )

        logs = self.records.logs[(page - 1) * 10:page * 10]
        for i in range(10):
            dx, dy = -316 + 632 * (i > 4), -27 + 66 * (i % 5)
            align.rel_center(Screen.screen, Texture.record_bar, (dx, dy))
            if i < len(logs):
                log = log_format(logs[i])
                if log == None:
                    align.rel_center(Screen.screen, self.record_text_invalid, (dx, dy + 2))
                else:
                    align.rel_center(Screen.screen,
                        Font.bar.render(log[0], False, Color.record), (dx - 159, dy - 1))
                    align.rel_center(Screen.screen,
                        Font.bar.render(log[1], False, Color.record), (dx - 82, dy - 1))
                    align.rel_center(Screen.screen,
                        Font.bar.render(log[2], False, Color.record), (dx - 20, dy - 1))
                    align.rel_center(Screen.screen,
                        Font.bar.render(log[3], False, Color.record), (dx + 104, dy + 2))
                    align.rel_center(Screen.screen, self.record_text_sep, (dx - 117, dy - 2))
                    align.rel_center(Screen.screen, self.record_text_sep, (dx - 47, dy - 2))
                    align.rel_center(Screen.screen, self.record_text_sep, (dx + 7, dy - 2))
            else:
                align.rel_center(Screen.screen, self.record_text_empty, (dx, dy - 1))

        align.rel_bottom(Screen.screen, Font.bar.render(
            f"Page {page:02}/{min(self.records.pages, 10):02}", False, Color.title
        ), (0, -75))
        if page <= 1:
            self.icon_previous_page_unavailble.display()
        else:
            self.icon_previous_page.display()
        if page >= min(self.records.pages, 10):
            self.icon_next_page_unavailble.display()
        else:
            self.icon_next_page.display()

        if self.ask_clear:
            Objects.multi_display(
                self.mask,
                self.dialog_box,
                self.dialog_clear_1,
                self.dialog_clear_2,
                self.button_Cancel,
                self.button_Yes,
                self.button_text_Cancel,
                self.button_text_Yes
            )

    def action(self, control: Control):
        if self.ask_clear:
            if control.click_in(self.button_Cancel):
                self.ask_clear = False
            elif control.click_in(self.button_Yes):
                self.records.clear_log()
                self.ask_clear = False
                Sound.play(Sound.enter)
            return "records"

        else:
            if control.click_in(self.bar_Back):
                self.current_page = 1
                Sound.play(Sound.back)
                return "home"
            elif control.click_in(self.bar_Clear):
                if self.records.logs:
                    self.ask_clear = True
                    Sound.play(Sound.enter)
                else:
                    Sound.play(Sound.forbidden)
                return "records"
            elif control.click_in(self.icon_previous_page):
                if self.current_page > 1:
                    self.current_page -= 1
                    Sound.play(Sound.turn_page)
                else:
                    Sound.play(Sound.forbidden)
                return "records"
            elif control.click_in(self.icon_next_page):
                if self.current_page < min(self.records.pages, 10):
                    self.current_page += 1
                    Sound.play(Sound.turn_page)
                else:
                    Sound.play(Sound.forbidden)
                return "records"

        return "records"