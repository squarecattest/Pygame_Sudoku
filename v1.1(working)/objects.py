import pygame
import align
import json
from formats import settings_format

pygame.init()


class Image:
    background = pygame.image.load(".\\image\\background_day.png")


class Texture:
    block = pygame.image.load(".\\texture\\block.png")
    dialog_box = pygame.image.load(".\\texture\\dialog_box.png")
    dialog_button = pygame.image.load(".\\texture\\dialog_button.png")
    result_box = pygame.image.load(".\\texture\\result_box.png")
    difficulty_left_arrow = pygame.image.load(
        ".\\texture\\difficulty_left_arrow.png")
    difficulty_right_arrow = pygame.image.load(
        ".\\texture\\difficulty_right_arrow.png")
    record_bar = pygame.image.load(".\\texture\\record_bar.png")
    record_left_arrow_unavailable = pygame.image.load(
        ".\\texture\\record_left_arrow_unavailable.png")
    record_right_arrow_unavailable = pygame.image.load(
        ".\\texture\\record_right_arrow_unavailable.png")
    record_left_arrow = pygame.image.load(".\\texture\\record_left_arrow.png")
    record_right_arrow = pygame.image.load(
        ".\\texture\\record_right_arrow.png")
    select_bar = pygame.image.load(".\\texture\\select_bar.png")
    select_bar_locked = pygame.image.load(".\\texture\\select_bar_locked.png")
    select_bar_ingame = pygame.image.load(".\\texture\\select_bar_ingame.png")
    select_bar_ingame_locked = pygame.image.load(".\\texture\\select_bar_ingame_locked.png")
    timer = pygame.image.load(".\\texture\\timer.png")
    moves = pygame.image.load(".\\texture\\moves.png")
    result_timer = pygame.image.load(".\\texture\\result_timer.png")
    result_moves = pygame.image.load(".\\texture\\result_moves.png")
    result_hint = pygame.image.load(".\\texture\\result_hint.png")
    slide_bar = pygame.image.load(".\\texture\\slide_bar.png")
    slider_gray = pygame.image.load(".\\texture\\slider_gray.png")
    slider_blue = pygame.image.load(".\\texture\\slider_blue.png")


class Font:
    title = pygame.font.Font(".\\font\\Minecraftia-Regular.ttf", 64)
    bar = pygame.font.Font(".\\font\\Minecraftia-Regular.ttf", 16)
    subtitle = number = pygame.font.Font(
        ".\\font\\Minecraftia-Regular.ttf", 24)


class Sound:
    enter = pygame.mixer.Sound(".\\sound\\enter.mp3")
    finish = pygame.mixer.Sound(".\\sound\\finish.mp3")
    forbidden = pygame.mixer.Sound(".\\sound\\forbidden.mp3")
    turn_page = pygame.mixer.Sound(".\\sound\\turn_page.mp3")

    @staticmethod
    def set_volumn_BGM(volumn: int):
        pygame.mixer.music.set_volume(0.5 * volumn / 100)

    @classmethod
    def set_volume_SE(cls, volumn: int):
        volumn = 0.5 * volumn / 100
        cls.enter.set_volume(volumn)
        cls.finish.set_volume(volumn)
        cls.forbidden.set_volume(volumn)
        cls.turn_page.set_volume(volumn)

    @staticmethod
    def play(sound: pygame.mixer.Sound):
        sound.stop()
        sound.play()

class Objects:
    '''
    the class to store the attributes of displayed object.

    `alignment`: "default", "abs", "scale", "rel_center", "rel_left", "rel_right", "rel_top" or "rel_bottom".
    '''

    def __init__(self, object: pygame.Surface, alignment: str, pos_or_scale_or_shift: tuple[int] | tuple[float]):
        self.surface = object
        self.pos = self.shift = self.scale = None
        match alignment:
            case "default":
                self.pos = pos_or_scale_or_shift
                self.__alignment = align.default
                self.__in_object = align.in_default_object
                self.__scale_of_object = align.scale_of_default_object
            case "abs":
                self.pos = pos_or_scale_or_shift
                self.__alignment = align.abs
                self.__in_object = align.in_abs_object
                self.__scale_of_object = align.scale_of_abs_object
            case "scale":
                self.scale = pos_or_scale_or_shift
                self.__alignment = align.scale
                self.__in_object = align.in_scaled_object
                self.__scale_of_object = align.scale_of_scaled_object
            case "rel_center":
                self.shift = pos_or_scale_or_shift
                self.__alignment = align.rel_center
                self.__in_object = align.in_rel_center_object
                self.__scale_of_object = align.scale_of_rel_center_object
            case "rel_left":
                self.shift = pos_or_scale_or_shift
                self.__alignment = align.rel_left
                self.__in_object = align.in_rel_left_object
                self.__scale_of_object = align.scale_of_rel_left_object
            case "rel_right":
                self.shift = pos_or_scale_or_shift
                self.__alignment = align.rel_right
                self.__in_object = align.in_rel_right_object
                self.__scale_of_object = align.scale_of_rel_right_object
            case "rel_top":
                self.shift = pos_or_scale_or_shift
                self.__alignment = align.rel_top
                self.__in_object = align.in_rel_top_object
                self.__scale_of_object = align.scale_of_rel_top_object
            case "rel_bottom":
                self.shift = pos_or_scale_or_shift
                self.__alignment = align.rel_bottom
                self.__in_object = align.in_rel_bottom_object
                self.__scale_of_object = align.scale_of_rel_bottom_object
            case _:
                raise Exception(
                    f'alignment should be "default", "abs", "scale", "rel_center", "rel_left", "rel_right", "rel_top" or "rel_bottom", but get {alignment}')

    def display(self, screen: pygame.Surface):
        self.__alignment(screen, self.surface, self.pos or self.scale or self.shift)

    @staticmethod
    def multi_display(screen: pygame.Surface, *objects):
        for object in objects:
            object.display(screen)

    def contain(self, screen_size: tuple[int], pos: tuple[int]):
        return self.__in_object(
            screen_size, pos, self.surface.get_size(), self.pos or self.scale or self.shift
        )
    
    def scale_of(self, screen_size: tuple[int], pos: tuple[int]):
        return self.__scale_of_object(
            screen_size, pos, self.surface.get_size(), self.pos or self.scale or self.shift
        )

class Control:
    '''
    The class to handle player's input.
    '''
    KEYBOARD = 0
    #KEYBOARD_RELEASE = 1
    LEFTCLICK = 2
    LEFTCLICK_RELEASE = 3
    #RIGHTCLICK = 4
    #RIGHTCLICK_RELEASE = 5
    MOUSEMOTION = 6
    K_SHIFT = "SHIFT"

    @classmethod
    def set_screen(cls, screen: pygame.Surface):
        cls.screen_size = screen.get_size()

    def __init__(self, event: pygame.event.Event):
        self.event = event
        self.pos = event.__dict__.get("pos")
        self.key = event.__dict__.get("key")
        if event.type == pygame.MOUSEBUTTONDOWN and event.__dict__.get("button") == 1:
            self.type = Control.LEFTCLICK
        elif event.type == pygame.MOUSEBUTTONUP and event.__dict__.get("button") == 1:
            self.type = Control.LEFTCLICK_RELEASE
        elif event.type == pygame.KEYDOWN:
            self.type = Control.KEYBOARD
        elif event.type == pygame.MOUSEMOTION:
            self.type = Control.MOUSEMOTION
        else:
            self.type = None
    
    def is_click(self):
        return self.type == Control.LEFTCLICK_RELEASE
    
    def is_click_down(self):
        return self.type == Control.LEFTCLICK
    
    def click_in(self, *objects: Objects):
        '''
        Check if left clicking inside an object.
        '''
        if not self.type == Control.LEFTCLICK_RELEASE: return False
        return any([object.contain(Control.screen_size, self.pos) for object in objects])
    
    def click_down_in(self, object: Objects):
        '''
        Check if left clicking (pressing down) inside an object.
        '''
        if not self.type == Control.LEFTCLICK: return False
        return object.contain(Control.screen_size, self.pos)
    
    def is_key(self):
        '''
        Check if keyboard inputting.
        '''
        return self.type == Control.KEYBOARD

    def key_in(self, key: int | str):
        '''
        Check if keyboard input the key.
        '''
        if not self.type == Control.KEYBOARD: return False
        if key == Control.K_SHIFT: return self.key == pygame.K_LSHIFT or self.key == pygame.K_RSHIFT
        return self.key == key
    
    def is_motion(self):
        '''
        Check if the mouse is moving.
        '''
        return self.type == Control.MOUSEMOTION
    
    def motion_pos(self):
        '''
        Return the mouse position.
        '''
        return self.pos
    
    def motion_shift(self):
        '''
        Return the shifted mouse position.
        '''
        return self.pos[0] - self.screen_size[0] // 2, self.pos[1] - self.screen_size[1] // 2

    def motion_scale(self):
        '''
        Return the scaled mouse position.
        '''
        return self.pos[0] / self.screen_size[0], self.pos[1] / self.screen_size[1]
    
    def scale_in(self, object: Objects):
        '''
        Return the scale inside the object.
        '''
        return object.scale_of(Control.screen_size, self.pos)
    
    # for puzzle
    def key_in_num(self):
        '''
        Return the number input. Backspace, Delete will be seen as 0.
        '''
        if not self.type == Control.KEYBOARD: return None
        if self.key == pygame.K_0 or self.key == pygame.K_KP0 or self.key == pygame.K_BACKSPACE \
            or self.key == pygame.K_DELETE: return 0
        elif self.key == pygame.K_1 or self.key == pygame.K_KP1: return 1
        elif self.key == pygame.K_2 or self.key == pygame.K_KP2: return 2
        elif self.key == pygame.K_3 or self.key == pygame.K_KP3: return 3
        elif self.key == pygame.K_4 or self.key == pygame.K_KP4: return 4
        elif self.key == pygame.K_5 or self.key == pygame.K_KP5: return 5
        elif self.key == pygame.K_6 or self.key == pygame.K_KP6: return 6
        elif self.key == pygame.K_7 or self.key == pygame.K_KP7: return 7
        elif self.key == pygame.K_8 or self.key == pygame.K_KP8: return 8
        elif self.key == pygame.K_9 or self.key == pygame.K_KP9: return 9
        return None
    
    # for puzzle
    def click_in_block(self):
        '''
        Return the block clicked. ((0, 0) ~ (8, 8))
        '''
        if not self.type == Control.LEFTCLICK_RELEASE: return None
        shift = (self.pos[0] - Control.screen_size[0] // 2, self.pos[1] - Control.screen_size[1] // 2)
        rel_shift = (shift[0] + 280 + 148 + 16, shift[1] + 148 + 16)
        if rel_shift[0] % 112 <= 103 and (rel_shift[0] % 112) % 36 <= 31 \
            and rel_shift[1] % 112 <= 103 and (rel_shift[1] % 112) % 36 <= 31:
            i, j = 3 * (rel_shift[0] // 112) + (rel_shift[0] % 112) // 36, \
                   3 * (rel_shift[1] // 112) + (rel_shift[1] % 112) // 36
            if 0 <= i <= 8 and 0 <= j <= 8: return (i, j)
        return None

class Background:
    background = Objects(Image.background, "rel_bottom", (0, 0))

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

    @classmethod
    def init(cls):
        try:
            with open(".\\settings.json", "r") as settings:
                cls.volumn_BGM, cls.volumn_SE, cls.night_mode = settings_format(json.load(settings))
        except FileNotFoundError:
            cls.volumn_BGM, cls.volumn_SE, cls.night_mode = settings_format(None)
        except json.decoder.JSONDecodeError:
            cls.volumn_BGM, cls.volumn_SE, cls.night_mode = settings_format(None)
        Sound.set_volumn_BGM(cls.volumn_BGM)
        Sound.set_volume_SE(cls.volumn_SE)

    @classmethod
    def set_volumn_BGM(cls, volumn: int):
        cls.volumn_BGM = volumn
        Sound.set_volumn_BGM(volumn)
    
    @classmethod
    def set_volumn_SE(cls, volumn: int):
        cls.volumn_SE = volumn
        Sound.set_volume_SE(volumn)

    @classmethod
    def save_settings(cls):
        settings = {
            "volumn_BGM": cls.volumn_BGM,
            "volumn_SE": cls.volumn_SE,
            "night_mode": cls.night_mode
        }
        with open(".\\settings.json", "w") as setting_file:
            json.dump(settings, setting_file, indent = 4)