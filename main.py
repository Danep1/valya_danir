import pygame
import os
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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = (obj.rect.x + self.dx) % width
        obj.rect.y = (obj.rect.y + self.dy) % height

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self, *args):
        if args:
            event = args[0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(- tile_width, 0)
                if event.key == pygame.K_RIGHT:
                    self.move(tile_width, 0)
                if event.key == pygame.K_UP:
                    self.move(0, - tile_height)
                if event.key == pygame.K_DOWN:
                    self.move(0, tile_height)

    def move(self, dx, dy):
        x, y = self.rect.x, self.rect.y
        x += dx
        y += dy
        if 0 < x < width or 0 < y < height:
            self.rect.x, self.rect.y = x, y


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def new_level(file_level_name):
    try:
        level = load_level(file_level_name)
    except FileNotFoundError or FileExistsError:
        print('!!!ОШИБКА!!! Указанный файл в папке /data не сущесвтует/не найден')
        return None
    else:
        return level


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('white_background.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    fps = 60
    size = width, height = 450, 450
    tile_width = tile_height = 50
    background = pygame.Color('black')

    level = new_level('level.txt')

    pygame.init()

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    screen.fill(background)
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    camera = Camera()

    box_image = pygame.transform.scale(load_image('box.png'), (tile_width, tile_height))
    grass_image = pygame.transform.scale(load_image('grass.png'), (tile_width, tile_height))
    tile_images = {'wall': box_image, 'empty': grass_image}
    player_image = pygame.transform.scale(load_image('mario.png', -1),
                                          (tile_width, tile_height))
    player, level_x, level_y = generate_level(level)

    start_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            for _ in all_sprites:
                _.update(event)

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill(background)
        all_sprites.draw(screen)
        player_group.draw(screen)
        clock.tick(fps)
        pygame.display.flip()

    terminate()
