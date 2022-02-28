import random

import pygame
import os
import sys

pygame.init()
screen = pygame.display.set_mode((45 * 30, 45 * 17 + 40), pygame.NOFRAME)
SIZE = WIDTH, HEIGHT = screen.get_size()
FPS = 50
FPS_WINDOW = 8
X, Y = screen.get_size()
tiles = {'$': 'floor_1.png', '@': "floor_8.png", '^': 'floor_2.png', '*': 'floor_7.png',
         '(': 'floor_4.png', '№': 'floor_3.png', ')': 'floor_5.png', '+': 'floor_6.png',
         '>': 'floor_ladder.png', '<': 'hole.png', "#": 'wall_hole_1.png', "!": "wall_mid.png",
         "%": "wall_banner_green.png", '|': 'wall_side_front_left.png', '\\': "wall_side_front_right.png",
         "Q": "wall_fountain_basin_red_anim_f2.png", "A": "wall_fountain_basin_blue_anim_f2.png",
         "&": "wall_banner_yellow.png", ";": "floor_spikes_anim_f0.png"}
decor = {"H": "column_top.png", "M": "column_mid.png", "L": "coulmn_base.png", "S": "wall_side_mid_left.png",
         "P": "wall_side_mid_right.png", "T": "wall_left.png", "C": "wall_mid.png", "R": "wall_corner_right.png",
         "O": "wall_corner_left.png", "_": "wall_top_mid.png", "I": "wall_inner_corner_l_top_left.png",
         "U": "wall_inner_corner_l_top_rigth.png", "J": "wall_corner_top_left.png", "G": "wall_corner_top_right.png",
         "W": "wall_fountain_mid_red_anim_f2.png", "E": "wall_fountain_mid_blue_anim_f2.png",
         "D": "doors_leaf_closed.png", "B": "crate.png", "V": "chest_empty_open_anim_f0.png",
         "N": "wall_right.png"}
tile_width = tile_height = 45


def load_image(file, colorkey=None):
    fullname = os.path.join('data', file)
    if not os.path.isfile(fullname):
        print(file)
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename):
    filename = "data/" + filename
    if not os.path.isfile(filename):
        print('file')
        sys.exit()
    with open(filename, 'r', encoding='utf-8') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Flour(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        if type in "!#|%\\":
            super().__init__(base.wall_sprites, base.all_sprites)
        else:
            super().__init__(base.tile_sprites, base.all_sprites)
        self.type = type
        self.image = pygame.transform.scale(load_image(tiles[type]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)


class Decor(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        if type in "L":
            super(Decor, self).__init__(base.all_sprites, base.column_sprites)
        elif type in "H":
            super(Decor, self).__init__(base.all_sprites, base.column_up_sprites)
        else:
            super(Decor, self).__init__(base.all_sprites, base.decor_sprites)
        self.type = type
        self.image = pygame.transform.scale(load_image(decor[type]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)


class Door(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super(Door, self).__init__(base.all_sprites, base.door_sprites)
        self.image = pygame.transform.scale(load_image(decor[type]), (100, 100))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.player = False
        self.x = None
        self.y = None

    def anim_player(self):
        if self.player:
            font = pygame.font.Font(None, 50)
            text = font.render("F", True, (255, 255, 255))
            screen.blit(text, (self.x, self.y))
            pygame.display.flip()


class BlueFountain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BlueFountain, self).__init__(base.all_sprites, base.blue_fountain)
        self.list_image = ["wall_fountain_mid_blue_anim_f0.png", "wall_fountain_mid_blue_anim_f1.png",
                           "wall_fountain_mid_blue_anim_f2.png"]
        self.number = 0
        self.image = pygame.transform.scale(load_image(self.list_image[self.number % 3]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.player = False
        self.x = None
        self.y = None

    def update(self):
        self.number += 0.2
        self.image = pygame.transform.scale(load_image(self.list_image[int(self.number) % 3]), (50, 50))

    def anim_player(self):
        if self.player:
            font = pygame.font.Font(None, 50)
            text = font.render("E", True, (255, 255, 255))
            screen.blit(text, (self.x, self.y))
            pygame.display.flip()


class BlueFountainFloor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BlueFountainFloor, self).__init__(base.all_sprites, base.blue_fountain_floor, base.tile_sprites)
        self.list_image = ["wall_fountain_basin_blue_anim_f0.png", "wall_fountain_basin_blue_anim_f1.png",
                           "wall_fountain_basin_blue_anim_f2.png"]
        self.number = 0
        self.image = pygame.transform.scale(load_image(self.list_image[self.number % 3]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.number += 0.2
        self.image = pygame.transform.scale(load_image(self.list_image[int(self.number) % 3]), (50, 50))


class RedFountain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(RedFountain, self).__init__(base.all_sprites, base.red_fountain)
        self.list_image = ["wall_fountain_mid_red_anim_f0.png", "wall_fountain_mid_red_anim_f1.png",
                           "wall_fountain_mid_red_anim_f2.png"]
        self.number = 0
        self.image = pygame.transform.scale(load_image(self.list_image[self.number % 3]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)

        self.player = False
        self.x = None
        self.y = None

    def update(self):
        self.number += 0.2
        self.image = pygame.transform.scale(load_image(self.list_image[int(self.number) % 3]), (50, 50))

    def anim_player(self):
        if self.player:
            font = pygame.font.Font(None, 50)
            text = font.render("E", True, (255, 255, 255))
            screen.blit(text, (self.x, self.y))
            pygame.display.flip()


class RedFountainFloor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(RedFountainFloor, self).__init__(base.all_sprites, base.red_fountain_floor, base.tile_sprites)
        self.list_image = ["wall_fountain_basin_red_anim_f0.png", "wall_fountain_basin_red_anim_f1.png",
                           "wall_fountain_basin_red_anim_f2.png"]
        self.number = 0
        self.image = pygame.transform.scale(load_image(self.list_image[self.number % 3]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.number += 0.2
        self.image = pygame.transform.scale(load_image(self.list_image[int(self.number) % 3]), (50, 50))


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Chest, self).__init__(base.all_sprites, base.chest_sprites)
        self.image = pygame.transform.scale(load_image("chest_empty_open_anim_f0.png"), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.player = False
        self.x = None
        self.y = None
        self.list_image = ["chest_empty_open_anim_f0.png", 'chest_empty_open_anim_f1.png',
                           'chest_empty_open_anim_f2.png']
        self.number = 0
        self.open = False

    def update(self):
        if nps.gun:
            if self.player:
                if not self.open:
                    font = pygame.font.Font(None, 50)
                    text = font.render("E", True, (255, 255, 255))
                    screen.blit(text, (self.x, self.y))
                    pygame.display.flip()

    def anim(self):
        self.number += 0.2
        if not self.open:
            self.image = pygame.transform.scale(load_image(self.list_image[int(self.number) % 3]), (50, 50))


class Player(pygame.sprite.Sprite):
    player = "knight_f_idle_anim_f3.png"
    left_player = "knight_f_idle_anim_f3.png"

    def __init__(self, x=None, y=None):
        super(Player, self).__init__(base.player_sprites)
        self.image = pygame.transform.scale(load_image(Player.player), (50, 100))
        if x is None and y is None:
            self.rect = self.image.get_rect().move(10 * tile_width, 11 * tile_height + 30)
        else:
            self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.frames = ["knight_f_run_anim_f0.png", "knight_f_run_anim_f1.png", "knight_f_run_anim_f2.png",
                       "knight_f_run_anim_f3.png", "knight_f_hit_anim_f0.png"]
        self.frame = 0
        self.hp = 5
        self.gun = None
        self.damage = False
        self.time = 0
        self.see = "r"

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
        run = True
        while run:
            for nps in base.nps_sprites:
                nps.player = False
            for event in base.boss_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.hp -= 0.5
                    self.rect.x -= x
                    self.rect.y -= y
            for event in base.wall_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    run = False
            for nps in base.nps_sprites:
                if pygame.sprite.collide_mask(self, nps):
                    self.rect.x -= x
                    self.rect.y -= y
                    run = False
                    nps.player = True
            for event in base.door_sprites:
                event.player = False
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    run = False
                    event.player = True
                    event.x = self.rect.x + 15
                    event.y = self.rect.y - 13
            for event in base.red_fountain:
                event.player = False
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    run = False
                    for nps in base.nps_sprites:
                        if nps.fountain or base.time_level:
                            if not self.gun is None:
                                event.player = True
                                event.x = self.rect.x + 15
                                event.y = self.rect.y - 13
            for event in base.blue_fountain:
                event.player = False
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    run = False
                    for nps in base.nps_sprites:
                        if nps.fountain or base.boss_level:
                            if not self.gun is None:
                                event.player = True
                                event.x = self.rect.x + 15
                                event.y = self.rect.y - 13
            for event in base.spikes_sprites:
                if pygame.sprite.collide_mask(self, event):
                    if event.frame == "floor_spikes_anim_f2.png" or event.frame == "floor_spikes_anim_f3.png":
                        self.hp -= 1
            for event in base.decor_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    run = False
            for event in base.wall_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    run = False
            for event in base.chest_sprites:
                event.player = False
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    run = False
                    if not event.open:
                        event.player = True
                        event.x = self.rect.x + 15
                        event.y = self.rect.y - 13
            for event in base.spikes_sprites:
                if pygame.sprite.collide_mask(self, event):
                    if event.frame == "floor_spikes_anim_f2.png" or event.frame == "floor_spikes_anim_f3.png":
                        self.hp -= 1
            run = False

    def anim(self, type):
        self.see = type
        if type == "r":
            self.frame += 0.2
            self.image = pygame.transform.scale(load_image(self.frames[int(self.frame) % len(self.frames)]), (50, 100))
        elif type == 'l':
            self.frame += 0.2
            self.image = pygame.transform.flip(pygame.transform.scale(
                load_image(self.frames[int(self.frame) % len(self.frames)]), (50, 100)),
                True, False)

    def move_level(self, x, y):
        self.rect.x = x * tile_width
        self.rect.y = y * tile_height - 30


class Knife(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Knife, self).__init__(base.all_sprites, base.gun_sprtites)
        self.image = pygame.transform.scale(load_image("weapon_regular_sword.png"), (30, 65))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.number = 0
        self.damage = 2

    def attack(self):
        run = True
        while run:
            for event in base.boss_sprites:
                if player.rect.x + player.rect.w + 32 >= event.rect.x:
                    event.hp -= self.damage
            run = False

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Nps(pygame.sprite.Sprite):
    def __init__(self):
        super(Nps, self).__init__(base.all_sprites, base.nps_sprites)
        self.image = pygame.transform.scale(load_image("wizzard_m_idle_anim_f0.png"), (50, 100))
        self.rect = self.image.get_rect().move(12 * tile_width, 10 * tile_height + 30)
        self.list_task = ["Приветствую тебя в подземелье", "Для начала возьми оружие из сундука",
                          "Молодец. Теперь отправляйся в подземелье", "Для этого подойди к красному или синему фонтану",
                          "В красном фонтане тебя ждет Монстр", 'В синем фонтане тебя ждет бесконечный поток огня',
                          "А если захочешь покинуть подземелье, подойди к двери"]
        self.number = 0
        self.gun = False
        self.fountain = False
        self.mask = pygame.mask.from_surface(self.image)
        self.player = False

    def update(self):
        try:
            if not player.gun is None:
                self.number += 1
                font = pygame.font.Font(None, 50)
                text = font.render(self.list_task[self.number], True, (255, 255, 255))
                screen.blit(text, (self.rect.x - text.get_size()[0] // 2, self.rect.y - 13))
                pygame.display.flip()
            elif player.gun is None and self.gun:
                font = pygame.font.Font(None, 50)
                text = font.render(self.list_task[self.number], True, (255, 255, 255))
                screen.blit(text, (self.rect.x - text.get_size()[0] // 2, self.rect.y - 13))
                pygame.display.flip()
            elif player.gun is None and not self.gun:
                font = pygame.font.Font(None, 50)
                text = font.render(self.list_task[self.number], True, (255, 255, 255))
                screen.blit(text, (self.rect.x - text.get_size()[0] // 2, self.rect.y - 13))
                pygame.display.flip()
                self.number += 1
            if self.number == 1:
                self.gun = True
            if self.number == 6:
                self.fountain = True
        except IndexError:
            pass

    def anim_player(self):
        if self.number < len(self.list_task):
            if self.player:
                font = pygame.font.Font(None, 50)
                text = font.render("E", True, (255, 255, 255))
                screen.blit(text, (self.rect.x + 15, self.rect.y - 13))
                pygame.display.flip()


class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Spikes, self).__init__(base.all_sprites, base.tile_sprites, base.spikes_sprites)
        self.image = pygame.transform.scale(load_image("floor_spikes_anim_f0.png"), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.frames = ["floor_spikes_anim_f0.png", "floor_spikes_anim_f1.png", "floor_spikes_anim_f2.png",
                       "floor_spikes_anim_f3.png"]
        self.frame = "floor_spikes_anim_f0.png"
        self.number = 0
        self.time = 1
        self.skipe = 0

    def update(self):
        if int(self.time) % 100 == 0:
            self.number += 0.1
            self.image = pygame.transform.scale(load_image(self.frames[int(self.number) % len(self.frames)]),
                                                (50, 50))
            if int(self.number) % len(self.frames) == 0 and int(self.number) != 0:
                self.time += 0.2
                self.image = pygame.transform.scale(load_image("floor_spikes_anim_f0.png"), (50, 50))
        else:
            self.skipe = int(self.number)
            self.time += 0.2

    def player(self):
        if pygame.sprite.collide_mask(self, player):
            if int(self.number) % len(self.frames) == 0 and int(self.number) != self.skipe:
                if not player.damage:
                    player.hp -= 1
                    player.damage = True


class Hp(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super(Hp, self).__init__(base.all_sprites, base.hp_sprites)
        if type == 1:
            self.image = pygame.transform.scale(load_image("ui_heart_full.png"), (30, 30))
        elif type == 2:
            self.image = pygame.transform.scale(load_image("ui_heart_half.png"), (30, 30))
        elif type == 3:
            self.image = pygame.transform.scale(load_image("ui_heart_empty.png"), (30, 30))
        self.rect = self.image.get_rect().move(x, y)


class FireBall(pygame.sprite.Sprite):
    fire = load_image('Fire-Ball-1.png', -1)

    def __init__(self, x, y):
        super(FireBall, self).__init__(base.all_sprites, base.fireball_sprites)
        self.image = pygame.transform.scale(FireBall.fire, (60, 60))
        self.rect = self.image.get_rect().move(x, y)
        self.frames = ['Fire-Ball-1.png', 'Fire-Ball-2.png', 'Fire-Ball-3.png', 'Fire-Ball-4.png']
        self.frame = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x):
        self.frame += 0.2
        if int(self.frame) % 5 == 0:
            self.image = pygame.transform.scale(load_image(self.frames[int(self.frame) % len(self.frames)], -1),
                                                (60, 60))
        self.rect.x += x
        run = True
        while run:
            for event in base.wall_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.kill()
                    break
            for event in base.player_sprites:
                if pygame.sprite.collide_mask(self, event):
                    event.hp -= 2.5
                    self.kill()
                    break
            run = False


class Boss(pygame.sprite.Sprite):
    boss = "big_demon_idle_anim_f0.png"

    def __init__(self, x, y):
        super(Boss, self).__init__(base.all_sprites, base.boss_sprites)
        self.see = "l"
        self.image = pygame.transform.flip(
            pygame.transform.scale(load_image(Boss.boss), (115, 150)),
            True, False)
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.figth = True
        self.hp = 62
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)
        self.see = 'l'
        self.frame = 0
        self.frames = ['big_demon_idle_anim_f0.png', 'big_demon_idle_anim_f1.png',
                       'big_demon_idle_anim_f2.png', 'big_demon_idle_anim_f3.png']
        self.attack_num = 0

    def update(self):
        y = self.rect.y
        if player.rect.y < self.rect.y:
            self.rect.y -= self.speed
        elif player.rect.y > self.rect.y:
            self.rect.y += self.speed
        run = True
        while run:
            for event in base.wall_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.rect.y = y
            run = False

    def anim(self):
        self.frame += 0.2
        self.image = pygame.transform.flip(pygame.transform.scale(
            load_image(self.frames[int(self.frame) % len(self.frames)]), (115, 150)),
            True, False)

    def attack(self):
        self.attack_num += 0.2
        if int(self.attack_num) % 20 == 0 and int(self.attack_num) != 0:
            FireBall(self.rect.x - 20, self.rect.y + 20)
            self.attack_num += 1


def ending():
    clock = pygame.time.Clock()
    intro_text = ["GAME OVER", "",
                  f"У вас {player.hp * 1.9} очков",
                  "Для завершения нажмите пробел"]
    score_fon = 0
    font1 = pygame.font.Font('fonts/F77 Minecraft.ttf', 90)  # должен быть предустановлен шрифт
    font2 = pygame.font.Font('fonts/F77 Minecraft.ttf', 50)  # должен быть предустановлен шрифт
    while True:
        text_coord = 50
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    terminate()
        screen.blit(pygame.transform.scale(load_image(f'start{score_fon % 3}.png'),
                                           (X, Y)), (0, 0))
        for line in intro_text:
            if 'GAME OVER' == line:
                string_rendered = font1.render(line, True, pygame.Color('white'))
                x_t, y_t = string_rendered.get_size()
                intro_rect = string_rendered.get_rect()
                text_coord = 50
                intro_rect.top = text_coord
                intro_rect.x = X // 2 - x_t // 2
                text_coord += intro_rect.height
            elif 'У вас' in line:
                string_rendered = font2.render(line, True, pygame.Color('white'))
                x_t, y_t = string_rendered.get_size()
                intro_rect = string_rendered.get_rect()
                text_coord += 50
                intro_rect.top = text_coord
                intro_rect.x = X // 2 - x_t // 2
                text_coord += intro_rect.height
            elif 'пробел' in line:
                string_rendered = font2.render(line, True, pygame.Color('white'))
                x_t, y_t = string_rendered.get_size()
                intro_rect = string_rendered.get_rect()
                text_coord += 100
                intro_rect.top = text_coord
                intro_rect.x = X // 2 - x_t // 2
                text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        score_fon += 1
        pygame.display.flip()
        clock.tick(FPS_WINDOW)


def generate_level(level):
    x, y, player = None, None, None
    for i in range(len(level)):
        for ii in range(len(level[0])):
            if level[i][ii] == "A":
                BlueFountainFloor(ii, i)
            elif level[i][ii] == 'Q':
                RedFountainFloor(ii, i)
            elif level[i][ii] == ';':
                Spikes(ii, i)
            elif level[i][ii] in list(tiles):
                Flour(level[i][ii], ii, i)
            elif level[i][ii] == 'D':
                Door(level[i][ii], ii, i)
            elif level[i][ii] == 'V':
                Chest(ii, i)
            elif level[i][ii] == "E":
                BlueFountain(ii, i)
            elif level[i][ii] == "W":
                RedFountain(ii, i)
            elif level[i][ii] in list(decor):
                Decor(level[i][ii], ii, i)


def terminate():
    pygame.quit()
    sys.exit()


def main():
    clock = pygame.time.Clock()
    running = True
    fire = 0
    time = 0
    level_1 = True
    level_2 = False
    level_3 = False
    while running:
        num = player.hp
        if float(num) <= 0.0:
            running = False
            ending()
        x, y = 40, 0
        for _ in range(5):
            if num - 1 >= 0:
                num -= 1
                Hp(x, y, 1)
            elif num - 0.5 >= 0:
                num -= 0.5
                Hp(x, y, 2)
            else:
                Hp(x, y, 3)
            x += 30
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                ending()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ending()
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.see == 'r':
                    player.image = pygame.transform.scale(load_image(Player.player), (50, 100))
                else:
                    player.image = pygame.transform.flip(
                        pygame.transform.scale(load_image(Player.left_player), (50, 100)),
                        True, False)
                if player.gun:
                    image = gun.image
                    number = 0
                    for i in range(30):
                        number += 0.2
                        if int(number) % 20 == 0:
                            if player.see == 'r':
                                gun.image = pygame.transform.rotate(gun.image, -10)
                            elif player.see == 'l':
                                gun.update(player.rect.x - 20 - 10 * i, player.rect.y + 5)
                                gun.image = pygame.transform.rotate(gun.image, 10)
                        screen.fill('black')
                        base.tile_sprites.draw(screen)
                        base.wall_sprites.draw(screen)
                        base.decor_sprites.draw(screen)
                        base.door_sprites.draw(screen)
                        base.chest_sprites.draw(screen)
                        base.blue_fountain.draw(screen)
                        base.red_fountain.draw(screen)
                        base.column_sprites.draw(screen)
                        base.gun_sprtites.draw(screen)
                        base.player_sprites.draw(screen)
                        base.column_up_sprites.draw(screen)
                        base.nps_sprites.draw(screen)
                        base.hp_sprites.draw(screen)
                        base.boss_sprites.draw(screen)
                        if level_2:
                            boss.update()
                            boss.anim()
                            boss.attack()
                            for j in base.fireball_sprites:
                                j.update(-5)
                        base.fireball_sprites.draw(screen)
                        if i == 28:
                            gun.attack()
                        pygame.display.flip()
                        for i in base.blue_fountain:
                            i.update()
                        for i in base.red_fountain:
                            i.update()
                        clock.tick(FPS)
                    gun.image = image
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    dic['right'] = True
                if event.key == pygame.K_LEFT:
                    dic['left'] = True
                if event.key == pygame.K_UP:
                    dic["top"] = True
                if event.key == pygame.K_DOWN:
                    dic["down"] = True
                if event.key == pygame.K_f:
                    for door in base.door_sprites:
                        if door.player:
                            ending()
                if event.key == pygame.K_e:
                    for nps in base.nps_sprites:
                        for i in base.chest_sprites:
                            if nps.gun:
                                if not base.boss_level and not base.time_level:
                                    if not i.open:
                                        if i.player:
                                            if player.see == 'r':
                                                player.image = pygame.transform.scale(load_image(Player.player),
                                                                                      (50, 100))
                                            else:
                                                player.image = pygame.transform.flip(
                                                    pygame.transform.scale(load_image(Player.left_player), (50, 100)),
                                                    True, False)
                                            for _ in range(10):
                                                i.anim()
                                            i.open = True
                                            gun = Knife(i.rect.x // tile_width + 0.2, i.rect.y // tile_height - 1.5)
                                            player.gun = gun
                                            for _ in range(70):
                                                base.gun_sprtites.draw(screen)
                                                base.chest_sprites.draw(screen)
                                                for i in base.blue_fountain:
                                                    i.update()
                                                for i in base.red_fountain:
                                                    i.update()
                                                base.red_fountain.draw(screen)
                                                base.blue_fountain.draw(screen)
                                                clock.tick(FPS)
                                                pygame.display.flip()
                        if not base.boss_level and not base.time_level:
                            if nps.player and nps.number < 7:
                                if player.see == 'r':
                                    player.image = pygame.transform.scale(load_image(Player.player), (50, 100))
                                else:
                                    player.image = pygame.transform.flip(
                                        pygame.transform.scale(load_image(Player.left_player), (50, 100)),
                                        True, False)
                                if nps.number == 6:
                                    start = True
                                screen.fill('black')
                                base.tile_sprites.draw(screen)
                                base.wall_sprites.draw(screen)
                                base.gun_sprtites.draw(screen)
                                base.player_sprites.draw(screen)
                                base.decor_sprites.draw(screen)
                                base.chest_sprites.draw(screen)
                                base.door_sprites.draw(screen)
                                base.column_sprites.draw(screen)
                                base.red_fountain.draw(screen)
                                base.blue_fountain.draw(screen)
                                base.nps_sprites.draw(screen)
                                base.hp_sprites.draw(screen)
                                base.column_up_sprites.draw(screen)
                                nps.update()
                                for i in range(70):
                                    for i in base.blue_fountain:
                                        i.update()
                                    for i in base.red_fountain:
                                        i.update()
                                    base.red_fountain.draw(screen)
                                    base.blue_fountain.draw(screen)
                                    clock.tick(FPS)
                                    pygame.display.flip()
                        if nps.fountain or base.time_level or base.boss_level:
                            if not base.boss_level:
                                for i in base.red_fountain:
                                    if i.player:
                                        for ii in base.all_sprites:
                                            ii.kill()
                                        del nps
                                        generate_level(load_level("level_2.txt"))
                                        player.move_level(x=9, y=7)
                                        player.see = 'r'
                                        boss = Boss(x=26, y=6)
                                        gun = Knife(player.rect.x + 20, player.rect.y + 5)
                                        player.gun = gun
                                        level_1 = False
                                        level_2 = True
                                        level_3 = False
                            if not base.time_level:
                                for i in base.blue_fountain:
                                    if i.player:
                                        for ii in base.all_sprites:
                                            if ii not in list(base.player_sprites):
                                                ii.kill()
                                        del nps
                                        generate_level(load_level("level_3.txt"))
                                        player.rect.move(9 * tile_width, 7 * tile_height + 30)
                                        player.see = 'r'
                                        gun = Knife(player.rect.x + 20, player.rect.y + 5)
                                        player.gun = gun
                                        level_1 = False
                                        level_2 = False
                                        level_3 = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    dic['right'] = False
                    player.image = pygame.transform.scale(load_image(Player.player), (50, 100))
                    player.frame = 0
                if event.key == pygame.K_LEFT:
                    dic['left'] = False
                    player.image = pygame.transform.flip(
                        pygame.transform.scale(load_image(Player.left_player), (50, 100)),
                        True, False)
                    player.frame = 0
                if event.key == pygame.K_UP:
                    dic["top"] = False
                    if player.see == 'r':
                        player.image = pygame.transform.scale(load_image(Player.player), (50, 100))
                    else:
                        player.image = pygame.transform.flip(
                            pygame.transform.scale(load_image(Player.left_player), (50, 100)),
                            True, False)
                    player.frame = 0
                if event.key == pygame.K_DOWN:
                    dic["down"] = False
                    if player.see == 'r':
                        player.image = pygame.transform.scale(load_image(Player.player), (50, 100))
                    else:
                        player.image = pygame.transform.flip(
                            pygame.transform.scale(load_image(Player.left_player), (50, 100)),
                            True, False)
                    player.frame = 0
        if dic['right']:
            player.update(10, 0)
            player.anim("r")
        if dic['left']:
            player.update(-10, 0)
            player.anim('l')
        if dic["top"]:
            player.anim(player.see)
            player.update(0, -10)
        if dic['down']:
            player.update(0, 10)
            player.anim(player.see)
        if level_2:
            boss.update()
            boss.anim()
            boss.attack()
            for event in base.fireball_sprites:
                event.update(-5)
        if level_3:
            fire += 0.2
            if int(fire) % 5 == 0 and int(fire) != 0:
                FireBall(28 * tile_width, random.randint(1, 15) * tile_height + 30)
                fire += 0.2
                time += 1
            for i in base.fireball_sprites:
                i.update(-5)
        screen.fill('black')
        base.tile_sprites.draw(screen)
        base.wall_sprites.draw(screen)
        base.decor_sprites.draw(screen)
        base.door_sprites.draw(screen)
        base.chest_sprites.draw(screen)
        base.blue_fountain.draw(screen)
        base.red_fountain.draw(screen)
        base.column_sprites.draw(screen)
        base.fireball_sprites.draw(screen)
        if level_2:
            base.boss_sprites.draw(screen)
            if boss.figth:
                start = 0
                lis = ["big_demon_idle_anim_f0.png", "big_demon_idle_anim_f1.png", "big_demon_idle_anim_f2.png",
                       "big_demon_idle_anim_f3.png"]
                num = player.hp
                if float(num) == 0.0:
                    running = False
                    terminate()
                x, y = 40, 0
                for _ in range(5):
                    if num - 1 >= 0:
                        num -= 1
                        Hp(x, y, 1)
                    elif num - 0.5 >= 0:
                        num -= 0.5
                        Hp(x, y, 2)
                    else:
                        Hp(x, y, 3)
                    x += 30
                for _ in range(200):
                    if _ % 5 == 0 and _ != 0:
                        boss.anim()
                    base.tile_sprites.draw(screen)
                    base.wall_sprites.draw(screen)
                    if not player.gun is None:
                        if player.see == 'r':
                            gun.update(player.rect.x + 20, player.rect.y + 5)
                        elif player.see == 'l':
                            gun.update(player.rect.x, player.rect.y + 5)
                    base.gun_sprtites.draw(screen)
                    base.player_sprites.draw(screen)
                    base.boss_sprites.draw(screen)
                    base.hp_sprites.draw(screen)
                    pygame.display.flip()
                    boss.figth = False
        if not player.gun is None:
            if player.see == 'r':
                gun.update(player.rect.x + 20, player.rect.y + 5)
            elif player.see == 'l':
                gun.update(player.rect.x, player.rect.y + 5)
            base.gun_sprtites.draw(screen)
        base.player_sprites.draw(screen)
        base.column_up_sprites.draw(screen)
        base.nps_sprites.draw(screen)
        base.hp_sprites.draw(screen)
        player.time += 1
        if player.time % 100 == 0:
            player.damage = False
        for i in base.blue_fountain:
            i.update()
            i.anim_player()
        for i in base.red_fountain:
            i.update()
            i.anim_player()
        for i in base.blue_fountain_floor:
            i.update()
        for i in base.red_fountain_floor:
            i.update()
        for i in base.chest_sprites:
            i.update()
        for i in base.spikes_sprites:
            i.update()
        num = player.hp
        for nps in base.nps_sprites:
            nps.anim_player()
        for event in base.spikes_sprites:
            event.player()
        for event in base.door_sprites:
            event.anim_player()
        pygame.display.flip()
        if level_2:
            if boss.hp <= 60.0:
                for i in base.all_sprites:
                    i.kill()
                level_2 = False
                level_3 = False
                level_1 = True
                generate_level(load_level('level.txt'))
                generate_level(load_level('decor_level.txt'))
                nps = Nps()
                player.move_level(9, 11)
                base.boss_level = True
                player.gun = Knife(1, 1)
                gun = player.gun
                if player.see == 'r':
                    gun.update(player.rect.x + 20, player.rect.y + 5)
                elif player.see == 'l':
                    gun.update(player.rect.x, player.rect.y + 5)
        if level_3:
            if time == 40:
                for i in base.all_sprites:
                    i.kill()
                level_2 = False
                level_3 = False
                level_1 = True
                generate_level(load_level('level.txt'))
                generate_level(load_level('decor_level.txt'))
                nps = Nps()
                player.move_level(10, 11)
                base.time_level = True
                player.gun = Knife(1, 1)
                gun = player.gun
                if player.see == 'r':
                    gun.update(player.rect.x + 20, player.rect.y + 5)
                elif player.see == 'l':
                    gun.update(player.rect.x, player.rect.y + 5)
        if base.time_level and base.boss_level:
            if level_1:
                for i in base.all_sprites:
                    i.kill()
                level_2 = False
                level_3 = False
                level_1 = True
                generate_level(load_level('level.txt'))
                generate_level(load_level('decor_level.txt'))
                nps = Nps()
                player.move_level(10, 11)
                base.time_level = True
                base.boss_level = True
                player.gun = Knife(1, 1)
                gun = player.gun
                if player.see == 'r':
                    gun.update(player.rect.x + 20, player.rect.y + 5)
                elif player.see == 'l':
                    gun.update(player.rect.x, player.rect.y + 5)
                level_1 = False
        clock.tick(FPS)


def start_window():
    clock = pygame.time.Clock()
    intro_text = ["DUNGEON", "",
                  "Соревнуйся, сражайся, побеждай",
                  "Нажмите ПРОБЕЛ чтобы начать игру"]
    score_fon = 0
    font1 = pygame.font.Font('fonts/F77 Minecraft.ttf', 90)  # должен быть предустановлен шрифт
    font2 = pygame.font.Font('fonts/F77 Minecraft.ttf', 50)  # должен быть предустановлен шрифт
    while True:
        text_coord = 50
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()
                elif event.key == pygame.K_SPACE:
                    main()  # начать игру
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
        screen.blit(pygame.transform.scale(load_image(f'start{score_fon % 3}.png'),
                                           (X, Y)), (0, 0))
        for line in intro_text:
            if 'DUNGEON' == line:
                string_rendered = font1.render(line, True, pygame.Color('white'))
                x_t, y_t = string_rendered.get_size()
                intro_rect = string_rendered.get_rect()
                text_coord = 50
                intro_rect.top = text_coord
            elif 'Соревнуйся' in line:
                string_rendered = font2.render(line, True, pygame.Color('white'))
                x_t, y_t = string_rendered.get_size()
                intro_rect = string_rendered.get_rect()
                text_coord += 50
                intro_rect.top = text_coord
            elif 'ПРОБЕЛ' in line:
                string_rendered = font2.render(line, True, pygame.Color('white'))
                x_t, y_t = string_rendered.get_size()
                intro_rect = string_rendered.get_rect()
                text_coord += 100
                intro_rect.top = text_coord
            intro_rect.x = X // 2 - x_t // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        score_fon += 1
        pygame.display.flip()
        clock.tick(FPS_WINDOW)


class Base:
    def __init__(self):
        self.boss_level = False
        self.time_level = False
        self.all_sprites = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.decor_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.column_sprites = pygame.sprite.Group()
        self.blue_fountain = pygame.sprite.Group()
        self.red_fountain = pygame.sprite.Group()
        self.blue_fountain_floor = pygame.sprite.Group()
        self.red_fountain_floor = pygame.sprite.Group()
        self.chest_sprites = pygame.sprite.Group()
        self.gun_sprtites = pygame.sprite.Group()
        self.nps_sprites = pygame.sprite.Group()
        self.spikes_sprites = pygame.sprite.Group()
        self.hp_sprites = pygame.sprite.Group()
        self.column_up_sprites = pygame.sprite.Group()
        self.boss_sprites = pygame.sprite.Group()
        self.fireball_sprites = pygame.sprite.Group()

base = Base()
nps = Nps()
player = Player()
generate_level(load_level('level.txt'))
generate_level(load_level('decor_level.txt'))
dic = {"right": False, "left": False, "top": False, "down": False}
flag_gun = True
#pygame.mixer.music.load('data/Dungeons & Dragons_ По Ту Сторону Страниц — Fantasy Town Ambience. DnD Music. Музыка для DnD. [Alvone prod.] (www.lightaudio.ru).mp3')
#pygame.mixer.music.play()
start_window()
pygame.quit()
