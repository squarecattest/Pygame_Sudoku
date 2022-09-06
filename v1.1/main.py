from objects import Screen, Control, Settings, Snow
Settings.init()

import pygame
import home
import records
import options
import ingame_options
import puzzle
from sys import exit

def quit():
    save()
    pygame.quit()
    exit()

def save():
    record_page.records.save_log()
    Settings.save_settings()
    home_page.saves.save_game_saves()

if __name__ == "__main__":
    pygame.init()
    size = (1120, 630)
    title = "Sudoku"
    icon = pygame.image.load(".\\icon.png")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size = size, flags = pygame.RESIZABLE)
    screen.fill((0, 0, 0))
    Screen.set(screen)
    pygame.display.set_caption(title)
    pygame.display.set_icon(icon)
    if Settings.night_mode: pygame.mixer.music.load(".\\bgm\\bgm_night.ogg")
    else: pygame.mixer.music.load(".\\bgm\\bgm_day.ogg")
    pygame.mixer.music.play(loops = -1)

    screen_state = "home"  # home, records, options, ingame, ingame-options
    home_page = home.HomePage()
    record_page = records.RecordPage()
    option_page = options.OptionPage()

    if Settings.night_mode: Snow.init()

    while(True):
        clock.tick(60)
        Screen.set(screen)
        events = pygame.event.get()
        for event in events:
            control = Control(event)
            if event.type == pygame.QUIT:
                quit()
            if screen_state == "home":
                screen_state = home_page.action(control)
                if screen_state == "home":
                    pass
                elif screen_state == "start":
                    puzzle_page = puzzle.PuzzlePage(home_page.difficulty)
                    puzzle_page.reload()
                    screen_state = "ingame"
                    home_page.state = "home"
                    break
                elif screen_state == "continue":
                    puzzle_page = puzzle.PuzzlePage(home_page.get_saves())
                    puzzle_page.reload()
                    screen_state = "ingame"
                    home_page.state = "home"
                    break
                elif screen_state == "quit":
                    quit()
            elif screen_state == "records":
                screen_state = record_page.action(control)
            elif screen_state == "options":
                screen_state = option_page.action(control)
                if screen_state == "options":
                    pass
                elif screen_state == "night_mode":
                    home_page.reload()
                    record_page.reload()
                    option_page.reload()
                    screen_state = "options"
            elif screen_state == "ingame":
                screen_state = puzzle_page.action(control)
                if screen_state == "ingame":
                    pass
                elif screen_state == "ingame-options":
                    ingame_option_page = ingame_options.IngameOptionPage()
                    break
                elif screen_state == "save_log":
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
            elif screen_state == "ingame-options":
                screen_state = ingame_option_page.action(control)
                if screen_state == "ingame-options":
                    pass
                elif screen_state == "ingame-night_mode":
                    home_page.reload()
                    record_page.reload()
                    option_page.reload()
                    puzzle_page.reload()
                    ingame_option_page.reload()
                    screen_state = "ingame-options"
                    break
            else:
                raise Exception(
                    f'screen_state should be "home", "records", "options" or "ingame", but get {screen_state}')
        
        if Settings.night_mode: Snow.update()

        if screen_state == "home":
            home_page.show_screen()
        elif screen_state == "records":
            record_page.show_screen()
        elif screen_state == "options":
            option_page.show_screen()
        elif screen_state == "ingame":
            puzzle_page.show_screen()
        elif screen_state == "ingame-options":
            puzzle_page.show_screen()
            if ingame_option_page.show_screen():
                del ingame_option_page
                screen_state = "ingame"
        pygame.display.update()
