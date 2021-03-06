
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
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:  # only the bottom one can reach that
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)  # x-dir: False, y-dir: True
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:  # 900 is the floor position
        can_score = True
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

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))  # anti-alias: True, color: (255, 255, 255): RGB
        score_rect = score_surface.get_rect(center = (288, 100))  # x: 288, y: 100
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))  # anti-alias: True, color: (255, 255, 255): RGB
        score_rect = score_surface.get_rect(center=(288, 100))  # x: 288, y: 100
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))  # anti-alias: True, color: (255, 255, 255): RGB
        high_score_rect = high_score_surface.get_rect(center=(288, 850))  # x: 288, y: 850
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True

#pygame.mixer.pre_init()
# pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))  # the canvas is going to be 576 x 1024
clock = pygame.time.Clock()  # to be able to limit framerate
game_font = pygame.font.SysFont('arial', 40)  # font-style: 04B_19.ttf, text-size: 40
# game_font = pygame.font.Font('04B_19.ttf', 40)  # font-style: 04B_19.ttf, text-size: 40

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = False
score = 0
high_score = 0
can_score = True

# loading the background image
# convert()  -> it converts the image to a type of file that it's easier for pygame
bg_surface = pygame.image.load("assets/pics/forest_cartoon_02.jpg").convert()
# pygame.transform.scale2x(picture)  -> to scale a picture 2x (doubling its size)
#bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load("assets/pics/floor_01.png").convert_alpha()
# floor_surface = pygame.image.load("assets/sprites/base.png").convert()
# floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# covert_alpha so that no black screen around the bird shows up when rotating
# different images to be able to animate the bird flaps
bird_downflap = pygame.image.load("assets/pics/bird_01.png").convert_alpha()
bird_midflap = pygame.image.load("assets/pics/bird_01.png").convert_alpha()
bird_upflap = pygame.image.load("assets/pics/bird_01.png").convert_alpha()

# bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/sprites/bluebird-downflap.png")).convert_alpha()
# bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/sprites/bluebird-midflap.png")).convert_alpha()
# bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/sprites/bluebird-upflap.png")).convert_alpha()
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

pipe_surface = pygame.image.load("assets/pics/pipe_green_01.png").convert_alpha()
# pipe_surface = pygame.image.load("assets/pics/rock_01.png")
#pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # 1200 in milli-seconds, so every 1.2s
pipe_height = [400, 600, 800]  # all different height that a pipe can have

game_over_surface = pygame.image.load("assets/pics/roundy_bird_welcome.png").convert_alpha()
# game_over_surface = pygame.transform.scale2x(pygame.image.load("assets/sprites/message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288, 512))

flap_sound = pygame.mixer.Sound("assets/audio/wing.wav")
death_sound = pygame.mixer.Sound("assets/audio/hit.wav")
score_sound = pygame.mixer.Sound("assets/audio/point.wav")
score_sound_countdown = 100

while True:

    for event in pygame.event.get():  # it captures all events in the game
        if event.type == pygame.QUIT:  # if we close the game
            pygame.quit()  # to exit the game
            sys.exit()  # to make sure the game exits correctly
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0  # so we reset gravity to 0
                bird_movement -= 9  # because gravity is positive
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0
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

        # Score
        pipe_score_check()
        score_display("main_game")
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    # Floor
    floor_x_pos -= 1  # so that each time it loops it moves the picture to the left on the x axis
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()  # it updates the screen
    clock.tick(120)  # to limit the framerate to 120, so the loop never runs faster than 120 fps
