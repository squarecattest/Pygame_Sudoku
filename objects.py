import pygame
pygame.init()

class Image:
    background = pygame.image.load(".\\image\\background_day.png")

class Texture:
    block = pygame.image.load(".\\texture\\block.png")
    dialog_box = pygame.image.load(".\\texture\\dialog_box.png")
    dialog_button = pygame.image.load(".\\texture\\dialog_button.png")
    difficulty_left_arrow = pygame.image.load(".\\texture\\difficulty_left_arrow.png")
    difficulty_right_arrow = pygame.image.load(".\\texture\\difficulty_right_arrow.png")
    record_bar = pygame.image.load(".\\texture\\record_bar.png")
    record_left_arrow_unavailable = pygame.image.load(".\\texture\\record_left_arrow_unavailable.png")
    record_right_arrow_unavailable = pygame.image.load(".\\texture\\record_right_arrow_unavailable.png")
    record_left_arrow = pygame.image.load(".\\texture\\record_left_arrow.png")
    record_right_arrow = pygame.image.load(".\\texture\\record_right_arrow.png")
    select_bar_ingame = pygame.image.load(".\\texture\\select_bar_ingame.png")
    select_bar = pygame.image.load(".\\texture\\select_bar.png")
    timer = pygame.image.load(".\\texture\\timer.png")
    slide_bar = pygame.image.load(".\\texture\\slide_bar.png")
    slider_gray = pygame.image.load(".\\texture\\slider_gray.png")
    slider_blue = pygame.image.load(".\\texture\\slider_blue.png")

class Font:
    title = pygame.font.Font(".\\font\\Minecraftia-Regular.ttf", 64)
    bar = pygame.font.Font(".\\font\\Minecraftia-Regular.ttf", 16)
    subtitle = number = pygame.font.Font(".\\font\\Minecraftia-Regular.ttf", 24)

class Sound:
    enter = pygame.mixer.Sound(".\\sound\\enter.mp3")
    finish = pygame.mixer.Sound(".\\sound\\finish.mp3")
    forbidden = pygame.mixer.Sound(".\\sound\\forbidden.mp3")
    turn_page = pygame.mixer.Sound(".\\sound\\turn_page_2.mp3")

    def set_volumn_BGM(self, volumn: int):
        pygame.mixer.music.set_volume(0.5 * volumn / 100)
        
    def set_volume_SE(self, volumn: int):
        volumn = 0.5 * volumn / 100
        self.enter.set_volume(volumn)
        self.finish.set_volume(volumn)
        self.forbidden.set_volume(volumn)
        self.turn_page.set_volume(volumn)

    def play(sound: pygame.mixer.Sound):
        sound.stop()
        sound.play()

class Interactable:
    '''
    Convenient for interactable objects.

    Built in iterable to use unpack operation in module `align`.
    '''
    def __init__(self, object: pygame.Surface, pos: tuple[int]):
        self.surface = object
        self.pos = pos
    
    def __iter__(self):
        self.__index = 0
        return self
    
    def __next__(self):
        if self.__index == 0:
            self.__index = 1
            return self.surface
        elif self.__index == 1:
            self.__index = 2
            return self.pos
        else: raise StopIteration