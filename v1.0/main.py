import pygame
import home
import records
import options
import puzzle
from sys import exit

FPS = 60

def quit():
    record_page.output_log()
    option_page.save_settings()
    pygame.quit()
    exit()

if __name__ == "__main__":
    pygame.init()
    size = (1120, 630)
    title = "Sudoku"
    icon = pygame.image.load(".\\icon.png")

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size = size)
    screen.fill((0, 0, 0))
    pygame.display.set_caption(title)
    pygame.display.set_icon(icon)
    pygame.mixer.music.load(".\\bgm\\bgm.mp3")
    pygame.mixer.music.play(loops = -1)

    screen_state = "home" #home, records, ingame, (options)
    home_page = home.HomePage()
    record_page = records.RecordPage()
    option_page = options.OptionPage()
    while(True):
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            if screen_state == "home":
                screen_state = home_page.action(event)
                if screen_state == "quit":
                    quit()
                if screen_state == "start":
                    puzzle_page = puzzle.PuzzlePage(home_page.difficulty)
                    screen_state = "ingame"
                    home_page.state = "home"
                    break
            elif screen_state == "records":
                screen_state = record_page.action(event)
            elif screen_state == "options":
                screen_state = option_page.action(event)
            elif screen_state == "ingame":
                screen_state = puzzle_page.action(event)
                if screen_state == "save":
                    if not puzzle_page.solved_by_bot:
                        record_page.add_log(puzzle_page.difficulty, puzzle_page.total_time, int(puzzle_page.time))
                    del puzzle_page
                    screen_state = "home"
                    break
                elif screen_state == "home":
                    del puzzle_page
                    break
            else: raise Exception(f'screen_state should be "home", "records", "options" or "ingame", but get {screen_state}')
        
        if screen_state == "home": home_page.show_screen(screen)
        elif screen_state == "records": record_page.show_screen(screen)
        elif screen_state == "options": option_page.show_screen(screen)
        elif screen_state == "ingame": puzzle_page.show_screen(screen)
        pygame.display.update()
