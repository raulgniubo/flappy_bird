
import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop= (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:  # only the bottom one can reach that
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)  # x-dir: False, y-dir: True
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:  # 900 is the floor position
        return False

    return True  # returns True if no collision so game_active = True

def rotate_bird(bird):
    # the bird is rotating at (-bird movement * 3) speed (minus means direction). The scale is 1.
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect


pygame.init()
screen = pygame.display.set_mode((576, 1024))  # the canvas is going to be 576 x 1024
clock = pygame.time.Clock()  # to be able to limit framerate

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = False

# loading the background image
# convert()  -> it converts the image to a type of file that it's easier for pygame
bg_surface = pygame.image.load("assets/sprites/background-day.png").convert()
# pygame.transform.scale2x(picture)  -> to scale a picture 2x (doubling its size)
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load("assets/sprites/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# covert_alpha so that no black screen around the bird shows up when rotating
# different images to be able to animate the bird flaps
bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/sprites/bluebird-downflap.png")).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/sprites/bluebird-midflap.png")).convert_alpha()
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/sprites/bluebird-upflap.png")).convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))

BIRDFLAP = pygame.USEREVENT + 1  # +1 because we don't want it to be the same as the other one
pygame.time.set_timer(BIRDFLAP, 200)  # 200 milli-seconds

# covert_alpha so that no black screen around the bird shows up when rotating
# bird_surface = pygame.image.load("assets/sprites/bluebird-midflap.png").convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (100, 512))  # it takes the bird_surface and puts a rectangle around it

pipe_surface = pygame.image.load("assets/sprites/pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # 1200 in milli-seconds, so every 1.2s
pipe_height = [400, 600, 800]  # all different height that a pipe can have

while True:

    for event in pygame.event.get():  # it captures all events in the game
        if event.type == pygame.QUIT:  # if we close the game
            pygame.quit()  # to exit the game
            sys.exit()  # to make sure the game exits correctly
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0  # so we reset gravity to 0
                bird_movement -= 9  # because gravity is positive
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
        if event.type == SPAWNPIPE:  # every 1.2s
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    # screen.blit(): to put 1 surface on top of the other one
    screen.blit(bg_surface, (0, 0))  # (0, 0) -> top left of the screen

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)  # instead of passing the coordinates, we pass the bird_rect
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Floor
    floor_x_pos -= 1  # so that each time it loops it moves the picture to the left on the x axis
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()  # it updates the screen
    clock.tick(120)  # to limit the framerate to 120, so the loop never runs faster than 120 fps




