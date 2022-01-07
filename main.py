import pygame
import os
import sys
import time

pygame.init()
screen = pygame.display.set_mode((45 * 30, 45 * 17 + 40), pygame.NOFRAME)
SIZE = WIDTH, HEIGHT = screen.get_size()
FPS = 50
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
        print("Файл не обнаружен")
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
        print('Файл не найден')
        sys.exit()
    with open(filename, 'r', encoding='utf-8') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Flour(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        if type in "!#|%\\":
            super().__init__(wall_sprites, all_sprites)
        else:
            super().__init__(tile_sprites, all_sprites)
        self.type = type
        self.image = pygame.transform.scale(load_image(tiles[type]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)


class Decor(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        if type == "D":
            super(Decor, self).__init__(all_sprites, door_sprites)
        elif type in "L":
            super(Decor, self).__init__(all_sprites, column_sprites)
        elif type in "H":
            super(Decor, self).__init__(all_sprites, column_up_sprites)
        else:
            super(Decor, self).__init__(all_sprites, decor_sprites)
        self.type = type
        if type != "D":
            self.image = pygame.transform.scale(load_image(decor[type]), (50, 50))
        else:
            self.image = pygame.transform.scale(load_image(decor[type]), (100, 100))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)


class BlueFountain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BlueFountain, self).__init__(all_sprites, blue_fountain)
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
        super(BlueFountainFloor, self).__init__(all_sprites, blue_fountain_floor, tile_sprites)
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
        super(RedFountain, self).__init__(all_sprites, red_fountain)
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
        super(RedFountainFloor, self).__init__(all_sprites, red_fountain_floor, tile_sprites)
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
        super(Chest, self).__init__(all_sprites, chest_sprites)
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
        super(Player, self).__init__(all_sprites, player_sprites)
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
        for nps in nps_sprites:
            while run:
                nps.player = False
                if pygame.sprite.collide_mask(self, nps):
                    self.rect.x -= x
                    self.rect.y -= y
                    run = False
                    nps.player = True
                for event in red_fountain:
                    event.player = False
                    if pygame.sprite.collide_mask(self, event):
                        self.rect.x -= x
                        self.rect.y -= y
                        run = False
                        if nps.fountain:
                            if not self.gun is None:
                                event.player = True
                                event.x = self.rect.x + 15
                                event.y = self.rect.y - 13
                for event in blue_fountain:
                    event.player = False
                    if pygame.sprite.collide_mask(self, event):
                        self.rect.x -= x
                        self.rect.y -= y
                        run = False
                        if nps.fountain:
                            if not self.gun is None:
                                event.player = True
                                event.x = self.rect.x + 15
                                event.y = self.rect.y - 13
                for event in spikes_sprites:
                    if pygame.sprite.collide_mask(self, event):
                        if event.frame == "floor_spikes_anim_f2.png" or event.frame == "floor_spikes_anim_f3.png":
                            player.hp -= 1
                for event in decor_sprites:
                    if pygame.sprite.collide_mask(self, event):
                        self.rect.x -= x
                        self.rect.y -= y
                        run = False
                for event in wall_sprites:
                    if pygame.sprite.collide_mask(self, event):
                        self.rect.x -= x
                        self.rect.y -= y
                        run = False
                for event in door_sprites:
                    if pygame.sprite.collide_mask(self, event):
                        self.rect.x -= x
                        self.rect.y -= y
                        run = False
                for event in chest_sprites:
                    event.player = False
                    if pygame.sprite.collide_mask(self, event):
                        self.rect.x -= x
                        self.rect.y -= y
                        run = False
                        if not event.open:
                            event.player = True
                            event.x = self.rect.x + 15
                            event.y = self.rect.y - 13
                for event in spikes_sprites:
                    if pygame.sprite.collide_mask(self, event):
                        if event.frame == "floor_spikes_anim_f2.png" or event.frame == "floor_spikes_anim_f3.png":
                            player.hp -= 1
                run = False

    def anim(self, type):
        self.see = type
        if type == "r":
            self.frame += 0.2
            self.image = pygame.transform.scale(load_image(self.frames[int(self.frame) % len(self.frames)]), (50, 100))
        elif type == 'l':
            self.frame += 0.2
            player.image = pygame.transform.flip(pygame.transform.scale(
                load_image(self.frames[int(self.frame) % len(self.frames)]), (50, 100)),
                True, False)


class Knife(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Knife, self).__init__(all_sprites, gun_sprtites)
        self.image = pygame.transform.scale(load_image("weapon_regular_sword.png"), (30, 65))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.number = 0
        self.damage = 1

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Nps(pygame.sprite.Sprite):
    def __init__(self):
        super(Nps, self).__init__(all_sprites, nps_sprites)
        self.image = pygame.transform.scale(load_image("wizzard_m_idle_anim_f0.png"), (50, 100))
        self.rect = self.image.get_rect().move(12 * tile_width, 10 * tile_height + 30)
        self.list_task = ["Приветствую тебя в подземелье", "Для начала возьми оружие из сундука",
                          "Молодец. Теперь отправляйся в подземелье", "Для этого подойди к красному или синему фонтану"]
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
            if self.number == 3:
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
        super(Spikes, self).__init__(all_sprites, tile_sprites, spikes_sprites)
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
        super(Hp, self).__init__(all_sprites, hp_sprites)
        if type == 1:
            self.image = pygame.transform.scale(load_image("ui_heart_full.png"), (30, 30))
        elif type == 2:
            self.image = pygame.transform.scale(load_image("ui_heart_half.png"), (30, 30))
        elif type == 3:
            self.image = pygame.transform.scale(load_image("ui_heart_empty.png"), (30, 30))
        self.rect = self.image.get_rect().move(x, y)


class Boss(pygame.sprite.Sprite):
    boss = "big_demon_idle_anim_f0.png"

    def __init__(self, x, y):
        super(Boss, self).__init__(all_sprites, boss_sprites)
        self.see = "l"
        self.image = pygame.transform.flip(
            pygame.transform.scale(load_image(Boss.boss), (115, 150)),
            True, False)
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.figth = True


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


running = True
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tile_sprites = pygame.sprite.Group()
door_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
decor_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
column_sprites = pygame.sprite.Group()
blue_fountain = pygame.sprite.Group()
red_fountain = pygame.sprite.Group()
blue_fountain_floor = pygame.sprite.Group()
red_fountain_floor = pygame.sprite.Group()
chest_sprites = pygame.sprite.Group()
gun_sprtites = pygame.sprite.Group()
nps_sprites = pygame.sprite.Group()
spikes_sprites = pygame.sprite.Group()
hp_sprites = pygame.sprite.Group()
column_up_sprites = pygame.sprite.Group()
boss_sprites = pygame.sprite.Group()
player = Player()
nps = Nps()
generate_level(load_level('level.txt'))
generate_level(load_level('decor_level.txt'))
dic = {"right": False, "left": False, "top": False, "down": False}
flag_gun = True
level_1 = True
level_2 = False
level_3 = False
while running:
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                terminate()
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
                    tile_sprites.draw(screen)
                    wall_sprites.draw(screen)
                    decor_sprites.draw(screen)
                    door_sprites.draw(screen)
                    chest_sprites.draw(screen)
                    blue_fountain.draw(screen)
                    red_fountain.draw(screen)
                    column_sprites.draw(screen)
                    gun_sprtites.draw(screen)
                    player_sprites.draw(screen)
                    column_up_sprites.draw(screen)
                    nps_sprites.draw(screen)
                    hp_sprites.draw(screen)
                    boss_sprites.draw(screen)
                    pygame.display.flip()
                    for i in blue_fountain:
                        i.update()
                    for i in red_fountain:
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
            if event.key == pygame.K_e:
                for nps in nps_sprites:
                    for i in chest_sprites:
                        if nps.gun:
                            if not i.open:
                                if i.player:
                                    if player.see == 'r':
                                        player.image = pygame.transform.scale(load_image(Player.player), (50, 100))
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
                                        gun_sprtites.draw(screen)
                                        chest_sprites.draw(screen)
                                        for i in blue_fountain:
                                            i.update()
                                        for i in red_fountain:
                                            i.update()
                                        red_fountain.draw(screen)
                                        blue_fountain.draw(screen)
                                        clock.tick(FPS)
                                        pygame.display.flip()
                    if nps.player and nps.number < 4:
                        if player.see == 'r':
                            player.image = pygame.transform.scale(load_image(Player.player), (50, 100))
                        else:
                            player.image = pygame.transform.flip(
                                pygame.transform.scale(load_image(Player.left_player), (50, 100)),
                                True, False)
                        screen.fill('black')
                        tile_sprites.draw(screen)
                        wall_sprites.draw(screen)
                        gun_sprtites.draw(screen)
                        player_sprites.draw(screen)
                        decor_sprites.draw(screen)
                        chest_sprites.draw(screen)
                        door_sprites.draw(screen)
                        column_sprites.draw(screen)
                        red_fountain.draw(screen)
                        blue_fountain.draw(screen)
                        nps_sprites.draw(screen)
                        hp_sprites.draw(screen)
                        column_up_sprites.draw(screen)
                        nps.update()
                        for i in range(70):
                            for i in blue_fountain:
                                i.update()
                            for i in red_fountain:
                                i.update()
                            red_fountain.draw(screen)
                            blue_fountain.draw(screen)
                            clock.tick(FPS)
                            pygame.display.flip()
                    if nps.fountain:
                        for i in red_fountain:
                            if i.player:
                                for ii in all_sprites:
                                    ii.kill()
                                del nps
                                generate_level(load_level("level_2.txt"))
                                player = Player(x=9, y=7)
                                boss = Boss(x=16, y=6)
                                gun = Knife(player.rect.x + 20, player.rect.y + 5)
                                player.gun = gun
                                level_1 = False
                                level_2 = True
                                level_3 = False
                        for i in blue_fountain:
                            if i.player:
                                for ii in all_sprites:
                                    ii.kill()
                                del nps
                                generate_level(load_level("level_3.txt"))
                                player = Player(x=9, y=7)
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
                player.image = pygame.transform.flip(pygame.transform.scale(load_image(Player.left_player), (50, 100)),
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
    screen.fill('black')
    tile_sprites.draw(screen)
    wall_sprites.draw(screen)
    decor_sprites.draw(screen)
    door_sprites.draw(screen)
    chest_sprites.draw(screen)
    blue_fountain.draw(screen)
    red_fountain.draw(screen)
    column_sprites.draw(screen)
    if level_2:
        boss_sprites.draw(screen)
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
                start += 0.1
                boss.image = pygame.transform.flip(
                    pygame.transform.scale(load_image(lis[int(start) % len(lis)]), (115, 150)),
                    True, False)
                tile_sprites.draw(screen)
                wall_sprites.draw(screen)
                if not player.gun is None:
                    if player.see == 'r':
                        gun.update(player.rect.x + 20, player.rect.y + 5)
                    elif player.see == 'l':
                        gun.update(player.rect.x, player.rect.y + 5)
                gun_sprtites.draw(screen)
                player_sprites.draw(screen)
                boss_sprites.draw(screen)
                hp_sprites.draw(screen)
                pygame.display.flip()
                boss.figth = False
    if not player.gun is None:
        if player.see == 'r':
            gun.update(player.rect.x + 20, player.rect.y + 5)
        elif player.see == 'l':
            gun.update(player.rect.x, player.rect.y + 5)
        gun_sprtites.draw(screen)
    player_sprites.draw(screen)
    column_up_sprites.draw(screen)
    nps_sprites.draw(screen)
    hp_sprites.draw(screen)
    player.time += 1
    if player.time % 100 == 0:
        player.damage = False
    for i in blue_fountain:
        i.update()
        i.anim_player()
    for i in red_fountain:
        i.update()
        i.anim_player()
    for i in blue_fountain_floor:
        i.update()
    for i in red_fountain_floor:
        i.update()
    for i in chest_sprites:
        i.update()
    for i in spikes_sprites:
        i.update()
    num = player.hp
    for nps in nps_sprites:
        nps.anim_player()
    for event in spikes_sprites:
        event.player()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
