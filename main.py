import pygame
import random
import os
import time
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, player_group)
        self.image = pygame.transform.scale(player_img, (80, 100))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, mobs)
        self.image = meteor_img
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(random.randrange(width - self.rect.width), random.randrange(
            -100, -40))
        self.mask = pygame.mask.from_surface(self.image)
        self.speedy = random.randrange(vmin, vmax)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, bullets)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


def show_score(choice=1):
    """Отображение результата"""
    s_font = pygame.font.SysFont('monaco', 24)
    s_surf = s_font.render(f'Time: {str(timeline // 1000)}       '
                           f'Score: {score}', True, pygame.Color('white'))
    s_rect = s_surf.get_rect()
    if choice == 1:
        s_rect.midtop = (80, 10)
    else:
        s_rect.midtop = (360, 120)
    screen.blit(s_surf, s_rect)


def game_over():
    """Конец игры при поражении"""
    go_font = pygame.font.SysFont('monaco', 72)
    go_surf = go_font.render('Game over', True, pygame.Color('red'))
    go_rect = go_surf.get_rect()
    go_rect.midtop = (360, 15)
    screen.blit(go_surf, go_rect)
    show_score(0)
    pygame.display.flip()
    time.sleep(3)
    terminate()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["STAR WARS", "",
                  "Давным давно в далекой далекой галактике...",
                  "Хан Соло вместе с Вукки вновь занимаются контробандой.",
                  "Но вот незадача: из-за того, что они попали в облако астероидов, ",
                  "невозможно совершить гипер-прыжок.",
                  "Ваша задача состоит в том чтобы облететь все космические глыбы и не разбиться.",
                  "Уничтожайте астероиды на своем пути",
                  "И да прибудет с вами Сила..."]

    fon = pygame.transform.scale(load_image('stars.jpg'), (width, height))
    screen.blit(background, background_rect)
    font1 = pygame.font.SysFont('monaco', 54)
    font2 = pygame.font.SysFont('monaco', 30)

    text_coord = 50
    for line in range(len(intro_text)):
        if line == 0:
            string_rendered = font1.render(intro_text[line], 1, pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.centerx = width // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        else:
            string_rendered = font2.render(intro_text[line], 1, pygame.Color('blue'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.centerx = width // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    size = width, height = 800, 800
    FPS = 60
    timeline = 0
    score = 0
    vmin = 1
    vmax = 8

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Star Wars")
    clock = pygame.time.Clock()

    background = load_image("stars.jpg")
    player_img = load_image("sokol.png", -1)
    meteor_img = load_image("meteorBrown_med1.png", -1)
    bullet_img = load_image("laserRed16.png", -1)
    background_rect = background.get_rect()

    start_screen()

    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player = Player()
    for i in range(8):
        m = Mob()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_ESCAPE:
                    running = False

        all_sprites.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 1
            m = Mob()

        for _ in mobs:
            if pygame.sprite.collide_mask(player, _):
                game_over()

        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        player_group.draw(screen)
        show_score()
        pygame.display.flip()
        timeline += 1000 // FPS
        if timeline % 40 == 0:
            vmin += 2
            vmax += 2
        clock.tick(FPS)

    terminate()
