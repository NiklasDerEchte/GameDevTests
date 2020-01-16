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

        self.velocity = pygame.math.Vector2
        self.speed = 30
        self.target_pos = pygame.math.Vector2()
        self.target_direction = pygame.math.Vector2()
        self.direction = pygame.math.Vector2()

        self.is_moving = False

    def update_pos(self, new_pos):
        self.target_pos = new_pos

    def update(self, *args):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0
        self.is_moving = False
        if keys[pygame.K_a]:
            self.direction.x = -1
        if keys[pygame.K_d]:
            self.direction.x = 1
        if keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1

        if not self.is_moving and (self.direction.x != 0 or self.direction.y != 0):
            self.is_moving = True
            self.update_pos((self.target_pos + self.direction))
        elif self.is_moving:
            pass

        self.rect.x = self.target_pos.x
        self.rect.y = self.target_pos.y


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
    #player.rect.x, player.rect.y = matrix.get_coord(player.next_pos)
    #hits = pygame.sprite.spritecollide(player, allSprites, False)
    #if hits:
    #    player.next_pos = player.cur_pos
    #player.rect.x, player.rect.y = matrix.get_coord(player.cur_pos)

def draw():
    global window, allSprites, player, matrix
    window.fill((255, 255, 255))
    pygame.draw.rect(window, player.color, player.rect)
    for sprite in allSprites:
        pygame.draw.rect(window, sprite.color, sprite.rect)
    matrix.draw(window)
    pygame.display.flip()

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
    draw()
    key_listener()
pygame.quit()
