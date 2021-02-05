
import pygame, sys

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


pygame.init()
screen = pygame.display.set_mode((576, 1024))  # the canvas is going to be 576 x 1024
clock = pygame.time.Clock()  # to be able to limit framerate

# Game Variables
gravity = 0.25
bird_movement = 0

# loading the background image
# convert()  -> it converts the image to a type of file that it's easier for pygame
bg_surface = pygame.image.load("assets/sprites/background-day.png").convert()
# pygame.transform.scale2x(picture)  -> to scale a picture 2x (doubling its size)
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load("assets/sprites/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0;

bird_surface = pygame.image.load("assets/sprites/bluebird-midflap.png").convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100, 512))  # it takes the bird_surface and puts a rectangle around it

while True:

    for event in pygame.event.get():  # it captures all events in the game
        if event.type == pygame.QUIT:  # if we close the game
            pygame.quit()  # to exit the game
            sys.exit()  # to make sure the game exits correctly
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0  # so we reset gravity to 0
                bird_movement -= 12  # because gravity is positive

    # screen.blit(): to put 1 surface on top of the other one
    screen.blit(bg_surface, (0, 0))  # (0, 0) -> top left of the screen

    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)  # instead of passing the coordinates, we pass the bird_rect
    floor_x_pos -= 1  # so that each time it loops it moves the picture to the left on the x axis
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()  # it updates the screen
    clock.tick(120)  # to limit the framerate to 120, so the loop never runs faster than 120 fps




