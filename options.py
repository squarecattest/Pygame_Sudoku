from objects import *
import align
import json

class OptionPage:
    title = Font.title.render("Options", False, (0, 0, 0))
    bar_Back = Interactable(Texture.select_bar, (560, 605))
    bar_text_Back = Font.bar.render("Back", False, (0, 0, 0))
    setting_volumn_BGM = Interactable(Texture.slide_bar, (280, 420))
    setting_volumn_SE = Interactable(Texture.slide_bar, (840, 420))
    def __init__(self):
        self.settings = {}
        try:
            with open(".\\settings.json", "r") as settings:
                self.settings = json.load(settings)
                if not isinstance(self.settings, dict): self.settings = {}
        except FileNotFoundError: pass
        except json.decoder.JSONDecodeError: pass
        self.dragging_volumn_BGM = False
        self.dragging_volumn_SE = False
        self.volumn_BGM = self.settings.get("volumn_BGM", 100)
        if not isinstance(self.volumn_BGM, int) or not 0 <= self.volumn_BGM <= 100: self.volumn_BGM = 100
        self.volumn_SE = self.settings.get("volumn_SE", 100)
        if not isinstance(self.volumn_SE, int) or not 0 <= self.volumn_SE <= 100: self.volumn_SE = 100
        Sound.set_volumn_BGM(Sound(), self.volumn_BGM)
        Sound.set_volume_SE(Sound(), self.volumn_SE)
        self.setting_text_volumn_BGM = Font.bar.render(f"Volumn(BGM): {self.volumn_BGM}%", False, (255, 255, 255))
        self.slider_volumn_BGM = Interactable(Texture.slider_gray, 
            (self.setting_volumn_BGM.pos[0] + 38 * (self.volumn_BGM - 50) // 10, self.setting_volumn_BGM.pos[1]))
        self.setting_text_volumn_SE = Font.bar.render(f"Volumn(SE): {self.volumn_SE}%", False, (255, 255, 255))
        self.slider_volumn_SE = Interactable(Texture.slider_gray, 
            (self.setting_volumn_SE.pos[0] + 38 * (self.volumn_SE - 50) // 10, self.setting_volumn_SE.pos[1]))
        
    def save_settings(self):
        self.settings = {
            "volumn_BGM": self.volumn_BGM,
            "volumn_SE": self.volumn_SE
        }
        with open(".\\settings.json", "w") as setting_file: json.dump(self.settings, setting_file, indent = 4)
    
    def show_screen(self, screen: pygame.Surface):
        align.default(screen, Image.background, (0, 0))
        align.center(screen, self.title, (560, 105))
        align.center(screen, *self.bar_Back)
        align.center(screen, self.bar_text_Back, self.bar_Back.pos)
        align.center(screen, *self.setting_volumn_BGM)
        align.center(screen, *self.slider_volumn_BGM)
        align.center(screen, self.setting_text_volumn_BGM, (self.setting_volumn_BGM.pos[0], self.setting_volumn_BGM.pos[1] + 3))
        align.center(screen, *self.setting_volumn_SE)
        align.center(screen, *self.slider_volumn_SE)
        align.center(screen, self.setting_text_volumn_SE, (self.setting_volumn_SE.pos[0], self.setting_volumn_SE.pos[1] + 3))

    def action(self, event: pygame.event.Event):
        pos = event.__dict__.get("pos", (0, 0))
        if event.type == pygame.MOUSEBUTTONDOWN and event.__dict__.get("button") == 1:
            if align.in_centered_object(pos, *self.slider_volumn_BGM):
                self.slider_volumn_BGM.surface = Texture.slider_blue
                self.dragging_volumn_BGM = True
            elif align.in_centered_object(pos, *self.slider_volumn_SE):
                self.slider_volumn_SE.surface = Texture.slider_blue
                self.dragging_volumn_SE = True

        elif event.type == pygame.MOUSEBUTTONUP and event.__dict__.get("button") == 1:
            if self.dragging_volumn_BGM:
                self.slider_volumn_BGM.surface = Texture.slider_gray
                self.dragging_volumn_BGM = False
            elif self.dragging_volumn_SE:
                self.slider_volumn_SE.surface = Texture.slider_gray
                self.dragging_volumn_SE = False
                Sound.play(Sound.finish)
            elif align.in_centered_object(pos, *self.bar_Back):
                return "home"

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_volumn_BGM:
                if pos[0] > self.setting_volumn_BGM.pos[0] + 190:
                    self.slider_volumn_BGM.pos = (self.setting_volumn_BGM.pos[0] + 190, self.setting_volumn_BGM.pos[1])
                elif pos[0] < self.setting_volumn_BGM.pos[0] - 190:
                    self.slider_volumn_BGM.pos = (self.setting_volumn_BGM.pos[0] - 190, self.setting_volumn_BGM.pos[1])
                else:
                    self.slider_volumn_BGM.pos = (pos[0], self.setting_volumn_BGM.pos[1])
                self.volumn_BGM = (self.slider_volumn_BGM.pos[0] - self.setting_volumn_BGM.pos[0]) * 10 // 38 + 50
                Sound.set_volumn_BGM(Sound(), self.volumn_BGM)
                self.setting_text_volumn_BGM = Font.bar.render(f"Volumn(BGM): {self.volumn_BGM}%", False, (255, 255, 255))
            elif self.dragging_volumn_SE:
                if pos[0] > self.setting_volumn_SE.pos[0] + 190:
                    self.slider_volumn_SE.pos = (self.setting_volumn_SE.pos[0] + 190, self.setting_volumn_SE.pos[1])
                elif pos[0] < self.setting_volumn_SE.pos[0] - 190:
                    self.slider_volumn_SE.pos = (self.setting_volumn_SE.pos[0] - 190, self.setting_volumn_SE.pos[1])
                else:
                    self.slider_volumn_SE.pos = (pos[0], self.setting_volumn_SE.pos[1])
                self.volumn_SE = (self.slider_volumn_SE.pos[0] - self.setting_volumn_SE.pos[0]) * 10 // 38 + 50
                Sound.set_volume_SE(Sound(), self.volumn_SE)
                self.setting_text_volumn_SE = Font.bar.render(f"Volumn(SE): {self.volumn_SE}%", False, (255, 255, 255))

        return "options"