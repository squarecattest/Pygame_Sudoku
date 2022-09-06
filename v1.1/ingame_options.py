from objects import *

class IngameOptionPage:
    slide_speed = 0.02
    mask = pygame.Surface((1280, 720))
    mask.set_alpha(220)
    mask = Objects(mask, "default", (0, 0))
    option_box = Objects(Texture.ingame_option_box, "scale", (1.25, 0.5))
    title = Objects(Font.title.render("Options", False,
                    Color.title), "scale", (1.25, 1/6))
    setting_BGM_slide_bar = Objects(Texture.slide_bar, "scale", (1.25, 7/15))
    setting_SE_slide_bar = Objects(Texture.slide_bar, "scale", (1.25, 9/15))
    setting_night_mode_bar = Objects(
        Texture.select_bar, "scale", (1.25, 11/15))
    setting_snow_bar = Objects(
        [Texture.select_bar_locked,
            Texture.select_bar][Settings.night_mode], "scale", (1.25, 13/15)
    )
    setting_BGM_text = Objects(
        Font.bar.render(
            f"Volume(BGM): {Settings.volume_BGM}%", False, (255, 255, 255)),
        "rel_center", (0, -720)
    )
    setting_SE_text = Objects(
        Font.bar.render(
            f"Volume(SE): {Settings.volume_SE}%", False, (255, 255, 255)),
        "rel_center", (0, -720)
    )
    setting_BGM_slider = Objects(Texture.slider_gray, "rel_center", (0, -720))
    setting_SE_slider = Objects(Texture.slider_gray, "rel_center", (0, -720))
    setting_night_mode_text = Objects(
        Font.bar.render(
            f'Night Mode: {["OFF", "ON"][Settings.night_mode]}', False, Color.bar),
        "rel_center", (0, -720)
    )
    if Settings.night_mode:
        setting_snow_text = Objects(
            Font.bar.render(
                f'Snow: {["OFF", "Light", "Heavy"][Settings.snow_type]}', False, Color.bar),
            "rel_center", (0, -720)
        )
    else:
        setting_snow_text = Objects(
            Font.bar.render("Snow: OFF", False,
                            Color.bar_locked), "rel_center", (0, -720)
        )
    arrow_back = Objects(Texture.record_right_arrow, "rel_center", (0, -720))

    def __init__(self):
        self.sliding_in = True
        self.sliding_out = False
        self.quit = False
        self.dragging_BGM_slider = False
        self.dragging_SE_slider = False

    def slide_in(self):
        scale_x = self.option_box.scale[0]
        scale_x -= self.slide_speed
        if scale_x < 0.75:
            scale_x = 0.75
            self.sliding_in = False
        self.option_box.scale = (scale_x, 0.5)
        self.title.scale = (scale_x, 1/6)
        self.setting_BGM_slide_bar.scale = (scale_x, 7/15)
        self.setting_SE_slide_bar.scale = (scale_x, 9/15)
        self.setting_night_mode_bar.scale = (scale_x, 11/15)
        self.setting_snow_bar.scale = (scale_x, 13/15)

    def slide_out(self):
        scale_x = self.option_box.scale[0]
        scale_x += self.slide_speed
        if scale_x > 1.25:
            scale_x = 1.25
            self.sliding_out = False
        self.option_box.scale = (scale_x, 0.5)
        self.title.scale = (scale_x, 1/6)
        self.setting_BGM_slide_bar.scale = (scale_x, 7/15)
        self.setting_SE_slide_bar.scale = (scale_x, 9/15)
        self.setting_night_mode_bar.scale = (scale_x, 11/15)
        self.setting_snow_bar.scale = (scale_x, 13/15)

    def reload(self):
        self.option_box.surface = Texture.ingame_option_box
        self.title.surface = Font.title.render("Options", False, Color.title)
        self.setting_night_mode_bar.surface = Texture.select_bar
        self.setting_snow_bar.surface = [
            Texture.select_bar_locked, Texture.select_bar][Settings.night_mode]
        self.setting_night_mode_text.surface = Font.bar.render(
            f'Night Mode: {["OFF", "ON"][Settings.night_mode]}', False, Color.bar
        )
        if Settings.night_mode:
            self.setting_snow_text.surface = Font.bar.render(
                f'Snow: {["OFF", "Light", "Heavy"][Settings.snow_type]}', False, Color.bar
            )
        else:
            self.setting_snow_text.surface = Font.bar.render(
                "Snow: OFF", False, Color.bar_locked)

    def show_screen(self):
        if self.quit and not self.sliding_out:
            return True
        if self.sliding_in:
            self.slide_in()
        elif self.sliding_out:
            self.slide_out()
        BGM_center = align.scale_to_shift(
            Screen.size, self.setting_BGM_slide_bar.scale)
        SE_center = align.scale_to_shift(
            Screen.size, self.setting_SE_slide_bar.scale)
        night_mode_center = align.scale_to_shift(
            Screen.size, self.setting_night_mode_bar.scale)
        snow_center = align.scale_to_shift(
            Screen.size, self.setting_snow_bar.scale)
        box_center_x = align.scale_to_shift(
            Screen.size, self.option_box.scale)[0]
        self.setting_BGM_text.shift = (BGM_center[0], BGM_center[1] + 3)
        self.setting_BGM_slider.shift = (
            BGM_center[0] + 40 * (Settings.volume_BGM -
                                  50) // 10, BGM_center[1]
        )
        self.setting_SE_text.shift = (SE_center[0], SE_center[1] + 3)
        self.setting_SE_slider.shift = (
            SE_center[0] + 40 * (Settings.volume_SE - 50) // 10, SE_center[1]
        )
        self.setting_night_mode_text.shift = (
            night_mode_center[0], night_mode_center[1] + 3)
        self.setting_snow_text.shift = (snow_center[0], snow_center[1] + 3)
        self.arrow_back.shift = (box_center_x - 295, 0)

        Objects.multi_display(
            self.mask,
            self.option_box,
            self.title,
            self.setting_BGM_slide_bar,
            self.setting_BGM_slider,
            self.setting_BGM_text,
            self.setting_SE_slide_bar,
            self.setting_SE_slider,
            self.setting_SE_text,
            self.setting_night_mode_bar,
            self.setting_night_mode_text,
            self.setting_snow_bar,
            self.setting_snow_text,
            self.arrow_back
        )

    def action(self, control: Control):
        if not self.sliding_in and not self.sliding_out:
            if control.click_down_in(self.setting_BGM_slider):
                self.setting_BGM_slider.surface = Texture.slider_blue
                self.dragging_BGM_slider = True
                return "ingame-options"
            elif control.click_down_in(self.setting_SE_slider):
                self.setting_SE_slider.surface = Texture.slider_blue
                self.dragging_SE_slider = True
                return "ingame-options"

            elif control.is_click():
                if self.dragging_BGM_slider:
                    self.setting_BGM_slider.surface = Texture.slider_gray
                    self.dragging_BGM_slider = False
                    return "ingame-options"
                elif self.dragging_SE_slider:
                    self.setting_SE_slider.surface = Texture.slider_gray
                    self.dragging_SE_slider = False
                    Sound.play(Sound.finish)
                    return "ingame-options"
                elif control.click_in(self.setting_night_mode_bar):
                    Settings.set_night_mode()
                    Sound.play(Sound.enter)
                    return "ingame-night_mode"
                elif control.click_in(self.setting_snow_bar):
                    if Settings.night_mode:
                        Settings.set_snow_type()
                        self.setting_snow_text.surface = Font.bar.render(
                            f'Snow: {["OFF", "Light", "Heavy"][Settings.snow_type]}', False, Color.bar
                        )
                        Sound.play(Sound.enter)
                    else:
                        Sound.play(Sound.forbidden)
                    return "ingame-options"
                elif control.click_in(self.arrow_back):
                    self.sliding_out = self.quit = True
                    return "ingame-options"
            elif control.is_motion():
                if self.dragging_BGM_slider:
                    scale = control.scale_in(self.setting_BGM_slide_bar)[0]
                    if scale < 0:
                        scale = 0
                    elif scale > 1:
                        scale = 1
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
                    Settings.set_volume_SE(int(100 * scale))
                    self.setting_SE_text.surface = Font.bar.render(
                        f"Volume(SE): {int(100 * scale)}%", False, (255, 255, 255)
                    )
                return "ingame-options"

        return "ingame-options"
