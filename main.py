import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__(all_sprites, player_sprites)
        self.image = pygame.Surface((20, 20))
        pygame.draw.rect(self.image, pygame.Color('blue'),
                         (0, 0, 20, 20), 0)
        self.rect = pygame.Rect(x, y, 20, 20)

    def update(self):
        flag = False
        for i in wall_sprites:
            if pygame.sprite.collide_rect(self, i):
                flag = True
        for i in wall_vertical_sprites:
            if pygame.sprite.collide_rect(self, i):
                flag = True
        if not flag:
            self.rect.y += 1

    def left(self, type):
        flag = True
        if flag:
            if type == 'left':
                self.rect.x -= 5
            else:
                self.rect.x += 5

    def up(self, type):
        for i in wall_vertical_sprites:
            if pygame.sprite.collide_rect(self, i):
                if type == 'up':
                    self.rect.y -= 5
                else:
                    self.rect.y += 5


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Wall, self).__init__(all_sprites, wall_sprites)
        self.image = pygame.Surface((50, 10))
        pygame.draw.rect(self.image, pygame.Color('grey'), (0, 0, 50, 10))
        self.rect = pygame.Rect(x, y, 50, 10)


class WallVertical(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(WallVertical, self).__init__(all_sprites, wall_vertical_sprites)
        self.image = pygame.Surface((10, 50))
        pygame.draw.rect(self.image, pygame.Color('red'), (0, 0, 10, 50))
        self.rect = pygame.Rect(x, y, 10, 50)


pygame.init()
SIZE = WIGTH, HEIGTH = 500, 500
screen = pygame.display.set_mode(SIZE)
running = True
clock = pygame.time.Clock()
player_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
wall_vertical_sprites = pygame.sprite.Group()
while running:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.key.get_mods() == 64:
                    WallVertical(event.pos[0], event.pos[1])
                else:
                    if len(list(player_sprites)) == 0:
                        Player(event.pos[0], event.pos[1])
                    else:
                        for i in player_sprites:
                            i.rect.x = event.pos[0]
                            i.rect.y = event.pos[1]
            if event.button == 3:
                Wall(event.pos[0], event.pos[1])
        for i in list(player_sprites):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    i.left("left")
                if event.key == pygame.K_RIGHT:
                    i.left("right")
                if event.key == pygame.K_UP:
                    i.up("up")
                if event.key == pygame.K_DOWN:
                    i.up("down")
    screen.fill('black')
    all_sprites.draw(screen)
    player_sprites.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
