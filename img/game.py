import pygame
from pygame.locals import *
import random

pygame.init()

screen_width_size = 460
screen_height_size = 500
screen = pygame.display.set_mode((screen_width_size, screen_height_size))
pygame.display.set_caption("Flappy bird game")

#==== GROUND ANIMATION ====# 
clock = pygame.time.Clock()
fps = 50

#==== GAME VARIABLES ====#
ground_scroll = 0
scroll_speed = 2
flying = False
game_over = False
pipe_gape = 100
pipe_frequency = 2000
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pipe_pass = False
font = pygame.font.SysFont('impact', 30)
white = (255, 255, 255 )

#==== IMAGES AND SCALING ====#
background_image = pygame.image.load('img/bg.png')
background_image = pygame.transform.scale(background_image, (460, 420))
background_bottom = pygame.image.load('img/ground.png')
background_bottom = pygame.transform.scale(background_bottom, (480, 80))
button_image = pygame.image.load('img/restart.png')

#==== SHOW SCORE ====#
def show_score_centered(text, font, text_color, y):
    score_text = font.render(text, True, text_color)
    text_rect = score_text.get_rect(center=(screen_width_size / 2, y))
    screen.blit(score_text, text_rect)

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height_size / 2)
    score = 0
    return score

#==== BIRD CLASS ====#
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            img = pygame.transform.scale(img, (35, 25))
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.clicked = False

#==== UPDATING BIRD VELOCITY ====#
    def update(self):
        if flying == True:
            self.velocity += 0.2
            if self.velocity > 30:
                self.velocity = 0
            if self.rect.bottom < 420:
                self.rect.y += int(self.velocity)

        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = -5
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter +- 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.image):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

#==== PIPE IMAGE CLASS ====#
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.image = pygame.transform.scale(self.image, (35, 250))
        self.rect = self.image.get_rect()

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gape / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gape / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill() 

#==== BUTTON CLASS ====#
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):
        action = False
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
       
bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height_size / 2))
bird_group.add(flappy)
pipe_group = pygame.sprite.Group()
button = Button(screen_width_size // 2 - 50, screen_height_size // 2 - 50, button_image)

#==== GAME RUNNING SECTION ====#
run = True
while run:
    clock.tick(fps)
    screen.blit(background_image, (0, 0))
    pipe_group.draw(screen)
    screen.blit(background_bottom, (ground_scroll, 420))

    if game_over == False and flying == True:
        current_spot = pygame.time.get_ticks()
        if current_spot - last_pipe > pipe_frequency:
            pipe_height = random.randint(-50, 50)
            bottom_pipe = Pipe(screen_width_size, int(screen_height_size / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width_size, int(screen_height_size / 2) + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = current_spot
        
        pipe_group.update()

        #==== GROUND SCROLL ====#
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 20:
            ground_scroll = 0

    bird_group.draw(screen)
    bird_group.update()

    #==== SCORE FUNCTIONALITY ====#
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.left < pipe_group.sprites()[0].rect.right\
                and pipe_pass == False:
                pipe_pass = True

        if pipe_pass == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pipe_pass = False

    #==== DRAW SCORE ====#
    formatted_score = f"SCORE : {score}"
    show_score_centered(formatted_score, font, white, 20)
   
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    
    if flappy.rect.bottom >= 420:
        game_over = True
        flaying = False
    
    if game_over:
        if button.draw():
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False:
            flying = True
    pygame.display.update()
pygame.quit()