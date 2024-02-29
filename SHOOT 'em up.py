import pygame
import random
from os import path
from pygame import mixer

img_dir = path.join(path.dirname(__file__), "image")
sound_dir = path.join(path.dirname(__file__), "Sound")

icon = pygame.image.load(path.join(img_dir, "spaceship.png"))
pygame.display.set_icon(icon)

# DISPLAY setup
WIDTH = 480
HEIGHT = 640

# define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Frames per second
FPS = 60  # how fast your game run that stand for frames per second
POWERUP_TIME = 5000
# initialize the pygame
pygame.init()

# for sound effect
pygame.mixer.init()

# display setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Caption
pygame.display.set_caption("Shoot 'Em Up")

# Background picture
background = pygame.image.load(path.join(img_dir, "12595f2f6007b339e844e6c42311917b (1).jpg")).convert()
background_rect = background.get_rect()

# image loading
player_img = pygame.image.load(path.join(img_dir, "a.png")).convert()
# mini player pic for lives
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

# powerup image
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, "shield_gold.png")).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, "bolt_gold.png")).convert()
# load all game sound
shoot_sound = pygame.mixer.Sound(path.join(sound_dir, "laser.wav"))
# powerup sound
shield_sound = pygame.mixer.Sound(path.join(sound_dir, "pow4.wav"))
power_sound = pygame.mixer.Sound(path.join(sound_dir, "pow5.wav"))
player_die_sound = pygame.mixer.Sound(path.join(sound_dir, "rumble1.ogg"))
expl_sound = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sound.append(pygame.mixer.Sound(path.join(sound_dir, snd)))
mixer.music.load("background.wav")
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# for fasting the game
clock = pygame.time.Clock()  # handle the speed and  keep track of how fast we going

# for more mobs
mobs_images = []
mobs_list = ["meteorBrown_big3.png", "meteorBrown_small2.png", "meteorBrown_tiny1.png",
             "meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_small1.png", "meteorBrown_med1.png"]

for img in mobs_list:
    mobs_images.append(pygame.image.load(path.join(img_dir, img)).convert())

# mobs explosion
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []

# player explosion
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

    # for player explosion
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

# for showing text on the screen
font_name = pygame.font.match_font("arial")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):  # parcentage
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Shoot'Em Up!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow Keys Move, Space To Fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press A Key To Begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# Player setup
class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # dnt know

        self.image = pygame.transform.scale(player_img, (64, 64))
        # when computer loads a image file that file alwys "rectangular" so use set_colorkey to remove rectangular
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        # reactangular collusion is very bad for gaming cz you can see no mobs touch when you r dieing. so make it circular collusion . then we can see the player mobs collusion
        self.radius = int(self.rect.width / 2) - 13  # we are drawing a circle on the ship
        # sprite has a property called radius
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.centerx = int(WIDTH / 2)  # center likhle hobe nah centerx
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0  # steady the ship

        # for player lives
        self.shield = 100

        # continous shooting
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()  # what time we last shoot whether we can know its time to shhoot again

        # player lives
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

        # powerup gun
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = int(WIDTH / 2)
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0

        # player movement
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx

        # limitation for fly for the ship
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    # for shoot the bullet from the top of ship
    def shoot(self):
        # its been long enough for us to shoot agaain
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    # lplayer lives
    def hide(self):
        # hide the player temporarilly
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


# enemy movement
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(mobs_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()

        # for circular collusion
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        # randomly appear int he screen
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 16)
        self.speedx = random.randrange(-3, 3)

        # for mob rotate

        self.rot = 0  # how far in degrees the sprite should be rotated
        self.rot_speed = random.randrange(-8, 15)

        # its time to rotate the image again
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)

            # for round rotatation
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, "laserRed07.png ")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10  # for going top, height less

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.rect.center = center
        self.speedy = 2  # for going top, height less

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update < self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


'''all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(15):
    newmob()


score = 0'''
game_over = True

# game loop
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        for i in range(15):
            newmob()

        score = 0

    # keep loop running at the right speed
    clock.tick(FPS)  # for more and more updates , without right game loop FPS , it will lagging

    # process input(event)
    for event in pygame.event.get():
        # close window
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # update game
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)  # dekha lagbe abr
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sound).play()

        # explosion
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)  # dekha lagbe abr
    for hit in hits:
        player.shield -= hit.radius * 2

        # explosion
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, "player")
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
            # player.kill()
            # running = False

    # check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100

        if hit.type == 'gun':
            player.powerup()
            power_sound.play()

    # if the player died and the explosion has finished playing
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # DRAW /render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)

    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    # for shield bar
    draw_shield_bar(screen, 5, 5, player.shield)
    # *after* drawing everything, flip the dispaly
    pygame.display.flip()

pygame.quit()
