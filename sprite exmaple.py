# pygame template - skeleton for a new pygame project

import pygame
import random

WIDTH = 800
HEIGHT = 600

# define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

FPS = 30  # how fast your game run that stand for frames per second

pygame.init()  # initialize the pygame
pygame.mixer.init()  # sound effect

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PYGAME SKELETON")

clock = pygame.time.Clock()  # handle the speed and  keep track of how fast we going


class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50,50))
        self.image = pygame.image.load(
            "a.png").convert()  # when computer loads a image file that file alwys rectangular so use set_colorkey
        self.image.set_colorkey(BLACK)
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.y_speed = 5

    def update(self):
        # moving objects
        self.rect.x += 5
        #left to right
        if self.rect.left > WIDTH:
            self.rect.right=0

        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT - 200:
            self.y_speed = -5
        if self.rect.top < 200:
            self.y_speed = 5

        if self.rect.x > WIDTH:
            self.rect.x = 0



all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
# game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)  # for more and more updates , without right game loop FPS , it will lagging

    # process input(event)
    for event in pygame.event.get():
        # close window
        if event.type == pygame.QUIT:
            running = False

    # update game
    all_sprites.update()

    # draw/ render
    screen.fill(BLUE)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the dispaly
    pygame.display.flip()

pygame.quit()
