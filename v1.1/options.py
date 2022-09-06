from objects import *

class OptionPage:
    title = Objects(Font.title.render("Options", False,
                    Color.title), "scale", (0.5, 1/6))
    bar_Back = Objects(Texture.select_bar, "rel_bottom", (0, -10))
    bar_text_Back = Objects(Font.bar.render(
        "Back", False, Color.bar), "rel_bottom", (0, -14))
    setting_BGM_slide_bar = Objects(Texture.slide_bar, "rel_center", (-280, 0))
    setting_SE_slide_bar = Objects(Texture.slide_bar, "rel_center", (280, 0))
    setting_BGM_text = Objects(
        Font.bar.render(
            f"Volume(BGM): {Settings.volume_BGM}%", False, (255, 255, 255)),
        "rel_center", (-280, 3)
    )
    setting_SE_text = Objects(
        Font.bar.render(
            f"Volume(SE): {Settings.volume_SE}%", False, (255, 255, 255)),
        "rel_center", (280, 3)
    )
    setting_BGM_slider = Objects(
        Texture.slider_gray, "rel_center", (-280 +
                                            40 * (Settings.volume_BGM - 50) // 10, 0)
    )
    setting_SE_slider = Objects(
        Texture.slider_gray, "rel_center", (280 +
                                            40 * (Settings.volume_SE - 50) // 10, 0)
    )
    setting_night_mode_bar = Objects(
        Texture.select_bar, "rel_center", (0, 105))
    setting_night_mode_text = Objects(
        Font.bar.render(
            f'Night Mode: {["OFF", "ON"][Settings.night_mode]}', False, Color.bar),
        "rel_center", (0, 108)
    )
    setting_snow_bar = Objects(
        [Texture.select_bar_locked,
            Texture.select_bar][Settings.night_mode], "rel_center", (0, 165)
    )
    if Settings.night_mode:
        setting_snow_text = Objects(
            Font.bar.render(
                f'Snow: {["OFF", "Light", "Heavy"][Settings.snow_type]}', False, Color.bar),
            "rel_center", (0, 168)
        )
    else:
        setting_snow_text = Objects(Font.bar.render(
            "Snow: OFF", False, Color.bar), "rel_center", (0, 168))

    def __init__(self):
        self.dragging_BGM_slider = False
        self.dragging_SE_slider = False

    def reload(self):
        self.title.surface = Font.title.render("Options", False, Color.title)
        self.bar_Back.surface = Texture.select_bar
        self.bar_text_Back.surface = Font.bar.render("Back", False, Color.bar)
        self.setting_night_mode_bar.surface = Texture.select_bar
        self.setting_night_mode_text.surface = Font.bar.render(
            f'Night Mode: {["OFF", "ON"][Settings.night_mode]}', False, Color.bar
        )
        self.setting_snow_text.surface = Font.bar.render(
            f'Snow: {["OFF", "Light", "Heavy"][Settings.snow_type]}', False, Color.bar
        )
        if Settings.night_mode:
            self.setting_snow_text.surface = Font.bar.render(
                f'Snow: {["OFF", "Light", "Heavy"][Settings.snow_type]}', False, Color.bar
            )
        else:
            self.setting_snow_text.surface = Font.bar.render(
                "Snow: OFF", False, Color.bar)

    def show_screen(self):
        Image.background.display()
        if Settings.night_mode:
            Snow.display()
        Objects.multi_display(
            self.title,
            self.bar_Back,
            self.bar_text_Back,
            self.setting_BGM_slide_bar,
            self.setting_BGM_slider,
            self.setting_BGM_text,
            self.setting_SE_slide_bar,
            self.setting_SE_slider,
            self.setting_SE_text,
            self.setting_night_mode_bar,
            self.setting_night_mode_text,
            self.setting_snow_bar,
            self.setting_snow_text
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
            elif control.click_in(self.setting_night_mode_bar):
                Settings.set_night_mode()
                Sound.play(Sound.enter)
                return "night_mode"
            elif control.click_in(self.setting_snow_bar):
                if Settings.night_mode:
                    Settings.set_snow_type()
                    self.setting_snow_text.surface = Font.bar.render(
                        f'Snow: {["OFF", "Light", "Heavy"][Settings.snow_type]}', False, Color.bar
                    )
                    Sound.play(Sound.enter)
                else:
                    Sound.play(Sound.forbidden)
                return "options"
            elif control.click_in(self.bar_Back):
                Settings.save_settings()
                Sound.play(Sound.back)
                return "home"

        elif control.is_motion():
            if self.dragging_BGM_slider:
                scale = control.scale_in(self.setting_BGM_slide_bar)[0]
                if scale < 0:
                    scale = 0
                elif scale > 1:
                    scale = 1
                self.setting_BGM_slider.shift = (-480 + 400 * scale, 0)
                Settings.set_volume_BGM(int(100 * scale))
                self.setting_BGM_text.surface = Font.bar.render(
                    f"Volume(BGM): {int(100 * scale)}%", False, (255, 255, 255)
                )
            elif self.dragging_SE_slider:
                scale = control.scale_in(self.setting_SE_slide_bar)[0]
                if scale < 0:
                    scale = 0
                elif scale > 1:
                    scale = 1
                self.setting_SE_slider.shift = (80 + 400 * scale, 0)
                Settings.set_volume_SE(int(100 * scale))
                self.setting_SE_text.surface = Font.bar.render(
                    f"Volume(SE): {int(100 * scale)}%", False, (255, 255, 255)
                )
            return "options"

        return "options"
