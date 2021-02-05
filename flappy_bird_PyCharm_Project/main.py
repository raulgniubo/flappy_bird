
import pygame, sys

pygame.init()
screen = pygame.display.set_mode((576, 1024))  # the canvas is going to be 576 x 1024
clock = pygame.time.Clock()  # to be able to limit framerate

bg_surface = pygame.image.load("assets/sprites/background-day.png")
# pygame.transform.scale2x(picture)  -> to scale a picture 2x (doubling its size)
bg_surface = pygame.transform.scale2x(bg_surface)

while True:

    for event in pygame.event.get():  # it captures all events in the game
        if event.type == pygame.QUIT:  # if we close the game
            pygame.quit()  # to exit the game
            sys.exit()  # to make sure the game exits correctly

    # screen.blit(): to put 1 surface on top of the other one
    screen.blit(bg_surface, (0, 0))  # (0, 0) -> top left of the screen

    pygame.display.update()  # it updates the screen
    clock.tick(120)  # to limit the framerate to 120, so the loop never runs faster than 120 fps




