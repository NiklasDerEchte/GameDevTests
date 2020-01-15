import pygame

class Matrix():
    def __init__(self, window_width, window_height, tile_size):
        self.window_width = window_width
        self.window_height = window_height
        self.tile_size = tile_size
        self.tile_x_amount = int (window_width / tile_size)
        self.tile_y_amount = int (window_height / tile_size)

    def get_coord(self, tile_pos):
        return (self.tile_size*tile_pos[0], self.tile_size*tile_pos[1])

    def get_tile_pos(self, coord_pos):
        cur_x = 0
        cur_y = 0
        for x in range(self.tile_x_amount):
            if (coord_pos[0] < x*self.tile_size):
                break
            else:
                cur_x = x
        for y in range(self.tile_y_amount):
            if (coord_pos[1] < y*self.tile_size):
                break
            else:
                cur_y = y
        return (cur_x, cur_y)

    def draw(self, window):
        for x in range(self.tile_x_amount):
            pygame.draw.line(window, (0,0,0), (x*self.tile_size, 0), (x*self.tile_size, self.window_height))

        for y in range(self.tile_y_amount):
            pygame.draw.line(window, (0,0,0), (0, y*self.tile_size), (self.window_width, y*self.tile_size))

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = pygame.Rect(50, 50, 10, 10)
        self.color = (120, 0, 0)

        self.cur_pos = 1, 1
        self.next_pos = 1, 1
        self.vel_x = 0
        self.vel_y = 0

    def update(self, *args):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        self.vel_y = 0
        self.cur_pos = self.next_pos
        if keys[pygame.K_a]:
            self.vel_x = -1
        if keys[pygame.K_d]:
            self.vel_x = 1
        if keys[pygame.K_w]:
            self.vel_y = -1
        if keys[pygame.K_s]:
            self.vel_y = 1
        self.next_pos = self.cur_pos[0] + self.vel_x, self.cur_pos[1] + self.vel_y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = pygame.Rect(150, 150, 50, 50)
        self.color = (10, 20, 0)

def key_listener():
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

def update():
    global player, allSprites, matrix
    allSprites.update()
    player.update()
    player.rect.x, player.rect.y = matrix.get_coord(player.next_pos)
    hits = pygame.sprite.spritecollide(player, allSprites, False)
    if hits:
        player.next_pos = player.cur_pos
    player.rect.x, player.rect.y = matrix.get_coord(player.cur_pos)

def draw():
    global window, allSprites, player, matrix
    window.fill((255, 255, 255))
    pygame.draw.rect(window, player.color, player.rect)
    for sprite in allSprites:
        pygame.draw.rect(window, sprite.color, sprite.rect)
    matrix.draw(window)
    pygame.display.flip()

def move_player():
    global player, matrix
    step_x, step_y = player.next_pos[0] - player.cur_pos[0], player.next_pos[1] - player.cur_pos[1]
    for step in range(10):
        player.cur_pos = player.cur_pos[0] + step_x, player.cur_pos[1] + step_y
        player.rect.x, player.rect.y = player.cur_pos[0], player.cur_pos[1]
        draw()
    player.cur_pos = player.next_pos

pygame.init()
window = pygame.display.set_mode((300, 400))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
player = Player()
obstacle = Obstacle()
allSprites = pygame.sprite.Group()
allSprites.add(obstacle)
matrix = Matrix(300, 400, 10)
run = True

while run:
    clock.tick(30)
    update()
    move_player()
    draw()
    key_listener()
pygame.quit()
