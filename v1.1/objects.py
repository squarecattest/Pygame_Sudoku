import pygame
import align
import json
from formats import settings_format
from random import random, randrange
pygame.init()

class Screen:
    @classmethod
    def set(cls, screen: pygame.Surface):
        cls.screen = screen
        cls.size = screen.get_size()

class Color:
    title_day = (0, 0, 0)
    title_night = (237, 237, 237)
    bar_day = (0, 0, 0)
    bar_night = (255, 255, 255)
    bar_locked_day = (0, 0, 0)
    bar_locked_night = (128, 128, 128)
    num_fixed_day = (0, 0, 0)
    num_fixed_night = (198, 198, 198)
    num_entered_day = (52, 52, 255)
    num_entered_night = (128, 128, 198)  # (128, 128, 168)
    num_guessed_day = (50, 205, 50)
    num_guessed_night = (128, 198, 128)
    num_repeated_day = (229, 50, 50)
    num_repeated_night = (198, 98, 98)
    same_num_day = (121, 201, 249)
    same_num_night = (61, 101, 125)
    record_day = (255, 255, 255)
    record_night = (198, 198, 198)
    record_invalid_day = (255, 0, 0)
    record_invalid_night = (198, 98, 98)
    # mask color

    @classmethod
    def night_mode(cls, is_night: bool):
        if is_night:
            cls.title = cls.title_night
            cls.bar = cls.bar_night
            cls.bar_locked = cls.bar_locked_night
            cls.record = cls.record_night
            cls.record_invalid = cls.record_invalid_night
            cls.num_fixed = cls.num_fixed_night
            cls.num_entered = cls.num_entered_night
            cls.num_guessed = cls.num_guessed_night
            cls.num_repeated = cls.num_repeated_night
            cls.same_num = cls.same_num_night
        else:
            cls.title = cls.title_day
            cls.bar = cls.bar_day
            cls.bar_locked = cls.bar_locked_day
            cls.record = cls.record_day
            cls.record_invalid = cls.record_invalid_day
            cls.num_fixed = cls.num_fixed_day
            cls.num_entered = cls.num_entered_day
            cls.num_guessed = cls.num_guessed_day
            cls.num_repeated = cls.num_repeated_day
            cls.same_num = cls.same_num_day

class Font:
    title = pygame.font.Font(".\\font\\Minecraftia-Regular.ttf", 84)
    ingame_option_title = pygame.font.Font(".\\font\\Minecraftia-Regular.ttf", 64)
    bar = pygame.font.Font(".\\font\\Minecraftia-Regular.ttf", 16)
    subtitle = number = pygame.font.Font(".\\font\\Minecraftia-Regular.ttf", 24)

class Image:
    background_day = pygame.image.load(".\\image\\background_day.png")
    background_night = pygame.image.load(".\\image\\background_night.png")

    @classmethod
    def night_mode(cls, is_night: bool):
        if is_night:
            cls.background = Objects(
                cls.background_night, "rel_bottom", (0, 0))
        else:
            cls.background = Objects(cls.background_day, "rel_bottom", (0, 0))

class Texture:
    difficulty_left_arrow = pygame.image.load(".\\texture\\difficulty_left_arrow.png")
    difficulty_right_arrow = pygame.image.load(".\\texture\\difficulty_right_arrow.png")
    record_left_arrow_unavailable = pygame.image.load(".\\texture\\record_left_arrow_unavailable.png")
    record_right_arrow_unavailable = pygame.image.load(".\\texture\\record_right_arrow_unavailable.png")
    record_left_arrow = pygame.image.load(".\\texture\\record_left_arrow.png")
    record_right_arrow = pygame.image.load(".\\texture\\record_right_arrow.png")
    timer = pygame.image.load(".\\texture\\timer.png")
    moves = pygame.image.load(".\\texture\\moves.png")
    result_timer = pygame.image.load(".\\texture\\result_timer.png")
    result_moves = pygame.image.load(".\\texture\\result_moves.png")
    result_hint = pygame.image.load(".\\texture\\result_hint.png")
    slide_bar = pygame.image.load(".\\texture\\slide_bar.png")
    slider_gray = pygame.image.load(".\\texture\\slider_gray.png")
    slider_blue = pygame.image.load(".\\texture\\slider_blue.png")
    snow_small = pygame.image.load(".\\texture\\snow_small.png")
    snow_large = pygame.image.load(".\\texture\\snow_large.png")
    snow_large.set_colorkey((27, 29, 32))

    block_day = pygame.image.load(".\\texture\\block_day.png")
    block_night = pygame.image.load(".\\texture\\block_night.png")
    dialog_box_day = pygame.image.load(".\\texture\\dialog_box_day.png")
    dialog_box_night = pygame.image.load(".\\texture\\dialog_box_night.png")
    result_box_day = pygame.image.load(".\\texture\\result_box_day.png")
    result_box_night = pygame.image.load(".\\texture\\result_box_night.png")
    select_bar_day = pygame.image.load(".\\texture\\select_bar_day.png")
    select_bar_night = select_bar_locked_day = pygame.image.load(".\\texture\\select_bar_night.png")
    select_bar_locked_night = pygame.image.load(".\\texture\\select_bar_locked_night.png")
    select_bar_ingame_day = pygame.image.load(".\\texture\\select_bar_ingame_day.png")
    select_bar_ingame_night = select_bar_ingame_locked_day = pygame.image.load(
        ".\\texture\\select_bar_ingame_night.png"
    )
    select_bar_ingame_locked_night = pygame.image.load(".\\texture\\select_bar_ingame_locked_night.png")
    record_bar_day = pygame.image.load(".\\texture\\record_bar_day.png")
    record_bar_night = pygame.image.load(".\\texture\\record_bar_night.png")
    dialog_button_day = pygame.image.load(".\\texture\\dialog_button_day.png")
    dialog_button_night = pygame.image.load(".\\texture\\dialog_button_night.png")
    ingame_option_box_day = pygame.image.load(".\\texture\\ingame_option_box_day.png")
    ingame_option_box_night = pygame.image.load(".\\texture\\ingame_option_box_night.png")

    @classmethod
    def night_mode(cls, is_night: bool):
        if is_night:
            cls.block = cls.block_night
            cls.select_bar = cls.select_bar_night
            cls.select_bar_locked = cls.select_bar_locked_night
            cls.select_bar_ingame = cls.select_bar_ingame_night
            cls.select_bar_ingame_locked = cls.select_bar_ingame_locked_night
            cls.record_bar = cls.record_bar_night
            cls.dialog_box = cls.dialog_box_night
            cls.dialog_button = cls.dialog_button_night
            cls.result_box = cls.result_box_night
            cls.ingame_option_box = cls.ingame_option_box_night
        else:
            cls.block = cls.block_day
            cls.select_bar = cls.select_bar_day
            cls.select_bar_locked = cls.select_bar_locked_day
            cls.select_bar_ingame = cls.select_bar_ingame_day
            cls.select_bar_ingame_locked = cls.select_bar_ingame_locked_day
            cls.record_bar = cls.record_bar_day
            cls.dialog_box = cls.dialog_box_day
            cls.dialog_button = cls.dialog_button_day
            cls.result_box = cls.result_box_day
            cls.ingame_option_box = cls.ingame_option_box_day


class Number:
    fixed_day = [0,
                 Font.number.render("1", False, Color.num_fixed_day),
                 Font.number.render("2", False, Color.num_fixed_day),
                 Font.number.render("3", False, Color.num_fixed_day),
                 Font.number.render("4", False, Color.num_fixed_day),
                 Font.number.render("5", False, Color.num_fixed_day),
                 Font.number.render("6", False, Color.num_fixed_day),
                 Font.number.render("7", False, Color.num_fixed_day),
                 Font.number.render("8", False, Color.num_fixed_day),
                 Font.number.render("9", False, Color.num_fixed_day)
                 ]
    entered_day = [0,
                   Font.number.render("1", False, Color.num_entered_day),
                   Font.number.render("2", False, Color.num_entered_day),
                   Font.number.render("3", False, Color.num_entered_day),
                   Font.number.render("4", False, Color.num_entered_day),
                   Font.number.render("5", False, Color.num_entered_day),
                   Font.number.render("6", False, Color.num_entered_day),
                   Font.number.render("7", False, Color.num_entered_day),
                   Font.number.render("8", False, Color.num_entered_day),
                   Font.number.render("9", False, Color.num_entered_day)
                   ]
    guessed_day = [0,
                   Font.number.render("1", False, Color.num_guessed_day),
                   Font.number.render("2", False, Color.num_guessed_day),
                   Font.number.render("3", False, Color.num_guessed_day),
                   Font.number.render("4", False, Color.num_guessed_day),
                   Font.number.render("5", False, Color.num_guessed_day),
                   Font.number.render("6", False, Color.num_guessed_day),
                   Font.number.render("7", False, Color.num_guessed_day),
                   Font.number.render("8", False, Color.num_guessed_day),
                   Font.number.render("9", False, Color.num_guessed_day)
                   ]
    repeated_day = [0,
                    Font.number.render("1", False, Color.num_repeated_day),
                    Font.number.render("2", False, Color.num_repeated_day),
                    Font.number.render("3", False, Color.num_repeated_day),
                    Font.number.render("4", False, Color.num_repeated_day),
                    Font.number.render("5", False, Color.num_repeated_day),
                    Font.number.render("6", False, Color.num_repeated_day),
                    Font.number.render("7", False, Color.num_repeated_day),
                    Font.number.render("8", False, Color.num_repeated_day),
                    Font.number.render("9", False, Color.num_repeated_day)
                    ]
    fixed_night = [0,
                   Font.number.render("1", False, Color.num_fixed_night),
                   Font.number.render("2", False, Color.num_fixed_night),
                   Font.number.render("3", False, Color.num_fixed_night),
                   Font.number.render("4", False, Color.num_fixed_night),
                   Font.number.render("5", False, Color.num_fixed_night),
                   Font.number.render("6", False, Color.num_fixed_night),
                   Font.number.render("7", False, Color.num_fixed_night),
                   Font.number.render("8", False, Color.num_fixed_night),
                   Font.number.render("9", False, Color.num_fixed_night)
                   ]
    entered_night = [0,
                     Font.number.render("1", False, Color.num_entered_night),
                     Font.number.render("2", False, Color.num_entered_night),
                     Font.number.render("3", False, Color.num_entered_night),
                     Font.number.render("4", False, Color.num_entered_night),
                     Font.number.render("5", False, Color.num_entered_night),
                     Font.number.render("6", False, Color.num_entered_night),
                     Font.number.render("7", False, Color.num_entered_night),
                     Font.number.render("8", False, Color.num_entered_night),
                     Font.number.render("9", False, Color.num_entered_night)
                     ]
    guessed_night = [0,
                     Font.number.render("1", False, Color.num_guessed_night),
                     Font.number.render("2", False, Color.num_guessed_night),
                     Font.number.render("3", False, Color.num_guessed_night),
                     Font.number.render("4", False, Color.num_guessed_night),
                     Font.number.render("5", False, Color.num_guessed_night),
                     Font.number.render("6", False, Color.num_guessed_night),
                     Font.number.render("7", False, Color.num_guessed_night),
                     Font.number.render("8", False, Color.num_guessed_night),
                     Font.number.render("9", False, Color.num_guessed_night)
                     ]
    repeated_night = [0,
                      Font.number.render("1", False, Color.num_repeated_night),
                      Font.number.render("2", False, Color.num_repeated_night),
                      Font.number.render("3", False, Color.num_repeated_night),
                      Font.number.render("4", False, Color.num_repeated_night),
                      Font.number.render("5", False, Color.num_repeated_night),
                      Font.number.render("6", False, Color.num_repeated_night),
                      Font.number.render("7", False, Color.num_repeated_night),
                      Font.number.render("8", False, Color.num_repeated_night),
                      Font.number.render("9", False, Color.num_repeated_night)
                      ]

    @classmethod
    def night_mode(cls, is_night: bool):
        if is_night:
            cls.fixed = cls.fixed_night
            cls.entered = cls.entered_night
            cls.guessed = cls.guessed_night
            cls.repeated = cls.repeated_night
        else:
            cls.fixed = cls.fixed_day
            cls.entered = cls.entered_day
            cls.guessed = cls.guessed_day
            cls.repeated = cls.repeated_day

class Sound:
    enter = pygame.mixer.Sound(".\\sound\\enter.mp3")
    back = pygame.mixer.Sound(".\\sound\\back.mp3")
    finish = pygame.mixer.Sound(".\\sound\\finish.mp3")
    forbidden = pygame.mixer.Sound(".\\sound\\forbidden.mp3")
    turn_page = pygame.mixer.Sound(".\\sound\\turn_page.mp3")

    @staticmethod
    def set_volume_BGM(volume: int):
        pygame.mixer.music.set_volume(0.35 * volume / 100)

    @classmethod
    def set_volume_SE(cls, volume: int):
        volume = 0.5 * volume / 100
        cls.enter.set_volume(volume)
        cls.back.set_volume(volume)
        cls.finish.set_volume(volume)
        cls.forbidden.set_volume(volume)
        cls.turn_page.set_volume(volume)

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

    def display(self):
        self.__alignment(Screen.screen, self.surface,
                         self.pos or self.scale or self.shift)

    @staticmethod
    def multi_display(*objects):
        for object in objects:
            object.display()

    def contain(self, pos: tuple[int]):
        return self.__in_object(
            Screen.size, pos, self.surface.get_size(), self.pos or self.scale or self.shift
        )

    def scale_of(self, pos: tuple[int]):
        return self.__scale_of_object(
            Screen.size, pos, self.surface.get_size(), self.pos or self.scale or self.shift
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
        if not self.type == Control.LEFTCLICK_RELEASE:
            return False
        return any([object.contain(self.pos) for object in objects])

    def click_down_in(self, object: Objects):
        '''
        Check if left clicking (pressing down) inside an object.
        '''
        if not self.type == Control.LEFTCLICK:
            return False
        return object.contain(self.pos)

    def is_key(self):
        '''
        Check if keyboard inputting.
        '''
        return self.type == Control.KEYBOARD

    def key_in(self, key: int | str):
        '''
        Check if keyboard input the key.
        '''
        if not self.type == Control.KEYBOARD:
            return False
        if key == Control.K_SHIFT:
            return self.key == pygame.K_LSHIFT or self.key == pygame.K_RSHIFT
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
        return self.pos[0] - Screen.size[0] // 2, self.pos[1] - Screen.size[1] // 2

    def motion_scale(self):
        '''
        Return the scaled mouse position.
        '''
        return self.pos[0] / Screen.size[0], self.pos[1] / Screen.size[1]

    def scale_in(self, object: Objects):
        '''
        Return the scale inside the object.
        '''
        return object.scale_of(self.pos)

    # for puzzle
    def key_in_num(self):
        '''
        Return the number input. Backspace, Delete will be seen as 0.
        '''
        if not self.type == Control.KEYBOARD:
            return None
        if self.key == pygame.K_0 or self.key == pygame.K_KP0 or self.key == pygame.K_BACKSPACE \
                or self.key == pygame.K_DELETE:
            return 0
        elif self.key == pygame.K_1 or self.key == pygame.K_KP1:
            return 1
        elif self.key == pygame.K_2 or self.key == pygame.K_KP2:
            return 2
        elif self.key == pygame.K_3 or self.key == pygame.K_KP3:
            return 3
        elif self.key == pygame.K_4 or self.key == pygame.K_KP4:
            return 4
        elif self.key == pygame.K_5 or self.key == pygame.K_KP5:
            return 5
        elif self.key == pygame.K_6 or self.key == pygame.K_KP6:
            return 6
        elif self.key == pygame.K_7 or self.key == pygame.K_KP7:
            return 7
        elif self.key == pygame.K_8 or self.key == pygame.K_KP8:
            return 8
        elif self.key == pygame.K_9 or self.key == pygame.K_KP9:
            return 9
        return None

    # for puzzle
    def click_in_block(self):
        '''
        Return the block clicked. ((0, 0) ~ (8, 8))
        '''
        if not self.type == Control.LEFTCLICK_RELEASE:
            return None
        shift = (self.pos[0] - Screen.size[0] // 2,
                 self.pos[1] - Screen.size[1] // 2)
        rel_shift = (shift[0] + 280 + 148 + 16, shift[1] + 148 + 16)
        if rel_shift[0] % 112 <= 103 and (rel_shift[0] % 112) % 36 <= 31 \
                and rel_shift[1] % 112 <= 103 and (rel_shift[1] % 112) % 36 <= 31:
            i, j = 3 * (rel_shift[0] // 112) + (rel_shift[0] % 112) // 36, \
                3 * (rel_shift[1] // 112) + (rel_shift[1] % 112) // 36
            if 0 <= i <= 8 and 0 <= j <= 8:
                return (i, j)
        return None

class Settings:
    bgm_start_play = 0

    @classmethod
    def init(cls):
        try:
            with open(".\\settings.json", "r") as settings:
                cls.volume_BGM, cls.volume_SE, cls.night_mode, cls.snow_type \
                    = settings_format(json.load(settings))
        except FileNotFoundError:
            cls.volume_BGM, cls.volume_SE, cls.night_mode, cls.snow_type = settings_format(
                None)
        except json.decoder.JSONDecodeError:
            cls.volume_BGM, cls.volume_SE, cls.night_mode, cls.snow_type = settings_format(
                None)
        Sound.set_volume_BGM(cls.volume_BGM)
        Sound.set_volume_SE(cls.volume_SE)
        Color.night_mode(cls.night_mode)
        Image.night_mode(cls.night_mode)
        Texture.night_mode(cls.night_mode)
        Number.night_mode(cls.night_mode)
        Snow.type = cls.snow_type

    @classmethod
    def set_volume_BGM(cls, volumn: int):
        cls.volume_BGM = volumn
        Sound.set_volume_BGM(volumn)

    @classmethod
    def set_volume_SE(cls, volumn: int):
        cls.volume_SE = volumn
        Sound.set_volume_SE(volumn)

    @classmethod
    def set_night_mode(cls):
        cls.night_mode = not cls.night_mode
        Color.night_mode(cls.night_mode)
        Image.night_mode(cls.night_mode)
        Texture.night_mode(cls.night_mode)
        Number.night_mode(cls.night_mode)
        cls.switch_music()
        if cls.night_mode:
            Snow.init()

    @classmethod
    def set_snow_type(cls):
        cls.snow_type += 1
        if cls.snow_type == 3:
            cls.snow_type = 0
        Snow.type = cls.snow_type

    @classmethod
    def switch_music(cls):
        play_at = (int(pygame.mixer.music.get_pos() * 1205000 /
                   1203450) + cls.bgm_start_play) % 1205000
        if cls.night_mode:
            pygame.mixer.music.load(".\\bgm\\bgm_night.ogg")
        else:
            pygame.mixer.music.load(".\\bgm\\bgm_day.ogg")
        pygame.mixer.music.play(loops=-1, start=play_at / 1000)
        cls.bgm_start_play = play_at

    @classmethod
    def save_settings(cls):
        settings = {
            "volumn_BGM": cls.volume_BGM,
            "volumn_SE": cls.volume_SE,
            "night_mode": cls.night_mode,
            "snow_type": cls.snow_type
        }
        with open(".\\settings.json", "w") as setting_file:
            json.dump(settings, setting_file, indent=4)

class Snow:
    OFF = 0
    LIGHT = 1
    BLIZZARD = 2

    on_screen_num = 40
    vel_small = (-1, 2)
    vel_large = (-2, 4)
    snows_small = []  # list[[Surface, pos(list), vel(tuple)]]
    snows_large = []

    @classmethod
    def init(cls):
        if cls.type >= cls.LIGHT:
            tries = cls.on_screen_num
            while tries:
                pos = [randrange(0, Screen.size[0]),
                       randrange(0, Screen.size[1])]
                if not any([cls.overlapped(pos, snow[1]) for snow in cls.snows_small]):
                    cls.snows_small.append(
                        [Texture.snow_small, pos, cls.vel_small])
                tries -= 1

        if cls.type == cls.BLIZZARD:
            tries = int(cls.on_screen_num * 1.5)
            while tries:
                pos = [randrange(0, Screen.size[0]),
                       randrange(0, Screen.size[1])]
                if not any([cls.overlapped(pos, snow[1]) for snow in cls.snows_large]):
                    cls.snows_large.append(
                        [Texture.snow_large, pos, cls.vel_large])
                tries -= 1

    @classmethod
    def spawn(cls):
        if cls.type >= cls.LIGHT:
            if random() < cls.on_screen_num / Screen.size[1]:
                pos = [randrange(0, Screen.size[0] +
                                 int(Screen.size[1] / 2)), -32]
                cls.snows_small.append(
                    [Texture.snow_small, pos, cls.vel_small])

        if cls.type == cls.BLIZZARD:
            if random() < cls.on_screen_num * 1.5 / Screen.size[1]:
                pos = [randrange(0, Screen.size[0] +
                                 int(Screen.size[1] / 2)), -32]
                cls.snows_large.append(
                    [Texture.snow_large, pos, cls.vel_large])

    @classmethod
    def update(cls):
        delete_small = []
        delete_large = []
        for i in range(len(cls.snows_small)):
            snow = cls.snows_small[i]
            snow[1][0] += snow[2][0]
            snow[1][1] += snow[2][1]
            if snow[1][0] < -32 or snow[1][1] > Screen.size[1] + 32:
                delete_small.insert(0, i)
        for i in range(len(cls.snows_large)):
            snow = cls.snows_large[i]
            snow[1][0] += snow[2][0]
            snow[1][1] += snow[2][1]
            if snow[1][0] < -32 or snow[1][1] > Screen.size[1] + 32:
                delete_large.insert(0, i)
        for i in delete_small:
            cls.snows_small.pop(i)
        for i in delete_large:
            cls.snows_large.pop(i)
        cls.spawn()

    @staticmethod
    def display():
        for snow in Snow.snows_small:
            align.abs(Screen.screen, snow[0], tuple(snow[1]))

        for snow in Snow.snows_large:
            align.abs(Screen.screen, snow[0], tuple(snow[1]))

    @staticmethod
    def overlapped(pos1: list[int], pos2: list[int]):
        return -64 < pos1[0] - pos2[0] < 64 or -64 < pos1[1] - pos2[1] < 64
