#main.py
import pygame
from game import Game


def main():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Городки")

    background_image = pygame.image.load("assets/background.png").convert()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    cylinder_image = pygame.image.load("assets/cylinder.png").convert_alpha()
    crosshair_image = pygame.image.load("assets/crosshair.png")
    game = Game(screen, background_image, cylinder_image, crosshair_image)
    game.start_game()

    game = Game(screen, background_image, cylinder_image, crosshair_image)
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_events(event)

        game.handle_player_turn()
        game.handle_computer_turn()
        game.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()