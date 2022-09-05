import pygame
import home
import records
import options
import puzzle
from objects import Control
from sys import exit

FPS = 60

def quit():
    save()
    pygame.quit()
    exit()

def save():
    record_page.records.save_log()
    option_page.settings.save_settings()
    home_page.saves.save_game_saves()

if __name__ == "__main__":
    pygame.init()
    size = (1120, 630)
    title = "Sudoku"
    icon = pygame.image.load(".\\icon.png")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size = size, flags = pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    pygame.display.set_caption(title)
    pygame.display.set_icon(icon)
    pygame.mixer.music.load(".\\bgm\\bgm.ogg")
    pygame.mixer.music.play(loops = -1)

    screen_state = "home"  # home, records, options, ingame
    home_page = home.HomePage()
    record_page = records.RecordPage()
    option_page = options.OptionPage()
    
    while(True):
        clock.tick(FPS)
        Control.set_screen(screen)
        events = pygame.event.get()
        for event in events:
            control = Control(event)
            if event.type == pygame.QUIT:
                quit()
            if screen_state == "home":
                screen_state = home_page.action(control)
                if screen_state == "quit":
                    quit()
                if screen_state == "start":
                    puzzle_page = puzzle.PuzzlePage(home_page.difficulty)
                    screen_state = "ingame"
                    home_page.state = "home"
                    break
                elif screen_state == "continue":
                    puzzle_page = puzzle.PuzzlePage(home_page.get_saves())
                    screen_state = "ingame"
                    home_page.state = "home"
                    break
            elif screen_state == "records":
                screen_state = record_page.action(control)
            elif screen_state == "options":
                screen_state = option_page.action(control)
            elif screen_state == "ingame":
                screen_state = puzzle_page.action(control)
                if screen_state == "save_log":
                    if not puzzle_page.solved_by_bot:
                        record_page.records.add_log(
                            puzzle_page.difficulty, puzzle_page.total_time, puzzle_page.moves, int(puzzle_page.time)
                        )
                    home_page.update_saves(None)
                    screen_state = "ingame"
                    break
                elif screen_state == "clear_temp":
                    home_page.update_saves(None)
                    screen_state = "ingame"
                    break
                elif screen_state == "save_temp":
                    home_page.update_saves(puzzle_page.save_temp())
                    del puzzle_page
                    screen_state = "home"
                    break
                elif screen_state == "back":
                    del puzzle_page
                    screen_state = "home"
                    break
            else:
                raise Exception(
                    f'screen_state should be "home", "records", "options" or "ingame", but get {screen_state}')

        if screen_state == "home":
            home_page.show_screen(screen)
        elif screen_state == "records":
            record_page.show_screen(screen)
        elif screen_state == "options":
            option_page.show_screen(screen)
        elif screen_state == "ingame":
            puzzle_page.show_screen(screen)
        pygame.display.update()
