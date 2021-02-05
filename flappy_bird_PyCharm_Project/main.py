
import pygame, sys

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


pygame.init()
screen = pygame.display.set_mode((576, 1024))  # the canvas is going to be 576 x 1024
clock = pygame.time.Clock()  # to be able to limit framerate

# loading the background image
# convert()  -> it converts the image to a type of file that it's easier for pygame
bg_surface = pygame.image.load("assets/sprites/background-day.png").convert()
# pygame.transform.scale2x(picture)  -> to scale a picture 2x (doubling its size)
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load("assets/sprites/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0;

while True:

    for event in pygame.event.get():  # it captures all events in the game
        if event.type == pygame.QUIT:  # if we close the game
            pygame.quit()  # to exit the game
            sys.exit()  # to make sure the game exits correctly

    # screen.blit(): to put 1 surface on top of the other one
    screen.blit(bg_surface, (0, 0))  # (0, 0) -> top left of the screen
    floor_x_pos -= 1  # so that each time it loops it moves the picture to the left on the x axis
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()  # it updates the screen
    clock.tick(120)  # to limit the framerate to 120, so the loop never runs faster than 120 fps




