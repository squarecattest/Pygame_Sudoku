from objects import *
import json


class Settings:
    def __init__(self):
        self.settings = {}
        try:
            with open(".\\settings.json", "r") as settings:
                self.settings = json.load(settings)
                if not isinstance(self.settings, dict):
                    self.settings = {}
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass
        self.volumn_BGM = self.settings.get("volumn_BGM", 100)
        if not isinstance(self.volumn_BGM, int) or not 0 <= self.volumn_BGM <= 100:
            self.volumn_BGM = 100
        self.volumn_SE = self.settings.get("volumn_SE", 100)
        if not isinstance(self.volumn_SE, int) or not 0 <= self.volumn_SE <= 100:
            self.volumn_SE = 100
        Sound.set_volumn_BGM(self.volumn_BGM)
        Sound.set_volume_SE(self.volumn_SE)

    def set_volumn_BGM(self, volumn: int):
        self.volumn_BGM = volumn
        Sound.set_volumn_BGM(self.volumn_BGM)
    
    def set_volumn_SE(self, volumn: int):
        self.volumn_SE = volumn
        Sound.set_volume_SE(self.volumn_SE)

    def save_settings(self):
        self.settings = {
            "volumn_BGM": self.volumn_BGM,
            "volumn_SE": self.volumn_SE
        }
        with open(".\\settings.json", "w") as setting_file:
            json.dump(self.settings, setting_file, indent=4)

class OptionPage:
    title = Objects(Font.title.render("Options", False, (0, 0, 0)), "scale", (0.5, 1/6))
    bar_Back = Objects(Texture.select_bar, "rel_bottom", (0, -10))
    bar_text_Back = Objects(Font.bar.render("Back", False, (0, 0, 0)), "rel_bottom", (0, -14))
    setting_BGM_slide_bar = Objects(Texture.slide_bar, "rel_center", (-280, 105))
    setting_SE_slide_bar = Objects(Texture.slide_bar, "rel_center", (280, 105))

    def __init__(self):
        self.settings = Settings()
        self.setting_BGM_text = Objects(
            Font.bar.render(f"Volumn(BGM): {self.settings.volumn_BGM}%", False, (255, 255, 255)),
            "rel_center", (-280, 108))
        self.setting_SE_text = Objects(
            Font.bar.render(f"Volumn(SE): {self.settings.volumn_SE}%", False, (255, 255, 255)),
            "rel_center", (280, 108))
        self.setting_BGM_slider = Objects(Texture.slider_gray, "rel_center",
            (-280 + 40 * (self.settings.volumn_BGM - 50) // 10, 105))
        self.setting_SE_slider = Objects(Texture.slider_gray, "rel_center",
            (280 + 40 * (self.settings.volumn_SE - 50) // 10, 105))

        self.dragging_BGM_slider = False
        self.dragging_SE_slider = False

    def show_screen(self, screen: pygame.Surface):
        Objects.multi_display(screen,
            Background.background,
            self.title,
            self.bar_Back,
            self.bar_text_Back,
            self.setting_BGM_slide_bar,
            self.setting_BGM_slider,
            self.setting_BGM_text,
            self.setting_SE_slide_bar,
            self.setting_SE_slider,
            self.setting_SE_text
        )

    def action(self, control: Control):
        if control.click_down_in(self.setting_BGM_slider):
            self.setting_BGM_slider.surface = Texture.slider_blue
            self.dragging_BGM_slider = True
            return "options"
        elif control.click_down_in(self.setting_SE_slider):
            self.setting_SE_slider.surface = Texture.slider_blue
            self.dragging_SE_slider = True
            return "options"

        elif control.is_click():
            if self.dragging_BGM_slider:
                self.setting_BGM_slider.surface = Texture.slider_gray
                self.dragging_BGM_slider = False
                return "options"
            elif self.dragging_SE_slider:
                self.setting_SE_slider.surface = Texture.slider_gray
                self.dragging_SE_slider = False
                Sound.play(Sound.finish)
                return "options"
            elif control.click_in(self.bar_Back):
                self.settings.save_settings()
                return "home"

        elif control.is_motion():
            if self.dragging_BGM_slider:
                scale = control.scale_in(self.setting_BGM_slide_bar)[0]
                if scale < 0: scale = 0
                elif scale > 1: scale = 1
                self.setting_BGM_slider.shift = (-480 + 400 * scale, 105)
                self.settings.set_volumn_BGM(int(100 * scale))
                self.setting_BGM_text.surface = Font.bar.render(
                    f"Volumn(BGM): {self.settings.volumn_BGM}%", False, (255, 255, 255)
                )
            elif self.dragging_SE_slider:
                scale = control.scale_in(self.setting_SE_slide_bar)[0]
                if scale < 0: scale = 0
                elif scale > 1: scale = 1
                self.setting_SE_slider.shift = (80 + 400 * scale, 105)
                self.settings.set_volumn_SE(int(100 * scale))
                self.setting_SE_text.surface = Font.bar.render(
                    f"Volumn(SE): {self.settings.volumn_SE}%", False, (255, 255, 255)
                )
            return "options"
        
        return "options"