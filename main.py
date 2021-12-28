import pygame
import os
import sys

pygame.init()
FPS = 60
FPS_WINDOW = 8
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SIZE = X, Y = screen.get_size()
all_sprites = pygame.sprite.Group()
tile_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()


def load_image(file, colorkey=None):
    fullname = os.path.join('data', file)
    if not os.path.isfile(fullname):
        print(f'{file} изображение не найдено')
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


def start_window():
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
                    return
                elif event.key == pygame.K_SPACE:
                    return  # начать игру
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


start_window()

