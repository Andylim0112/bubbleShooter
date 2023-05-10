import pygame
import os

class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)

class Shooter(pygame.sprite.Sprite):
    def __init__(self, image, position, angle):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.angle = angle
        self.original_image = image
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3)

    def rotate(self, angle):
        self.angle += angle

        if self.angle > 170:
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.position)


def setup():
    global map
    map = [
      #  ["R", "R", "Y", "Y", "B", "B", "G", "G"]
      list("RRYYBBGG"), 
      list("RRYYBBG/"),
      list("BBGGRRYY"),
      list("BGGRRYY/"),
      list("........"),
      list("......./"),
      list("........"),
      list("......./"),
      list("........"),
      list("......./"),
      list("........")
    ]

    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col in [".", "/"]:
                continue
            position = get_bubble_position(row_idx, col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image, col, position))

def get_bubble_position(row_idx, col_idx):
    pos_x = col_idx * CELL_SIZE + (BUBBLE_WIDTH//2)
    pos_y = row_idx * CELL_SIZE + (BUBBLE_HEIGHT //2)
    if row_idx % 2 ==1:
        pos_x += CELL_SIZE //2
    return pos_x, pos_y


def get_bubble_image(color):
    if color == "R":
        return bubble_images[0]
    elif color == "Y":
        return bubble_images[1]
    elif color == "B":
        return bubble_images[2]
    elif color =="G":
        return bubble_images[3]
    elif color == "p":
        return bubble_images[4]
    else:
        return bubble_images[5]



pygame.init()
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Puzzle Bobble")
clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))


bubble_images = [
    pygame.image.load(os.path.join(current_path, "red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "black.png")).convert_alpha()
]

shooter_image = pygame.image.load(os.path.join(current_path, "shooter.png"))
shooter = Shooter(shooter_image, (screen_width //2, 624), 90)

#constants for games
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62
RED = (255, 0, 0)


to_angle = 0 #angle
angle_speed = 1.5 #move 1.5degrees

map = []
bubble_group = pygame.sprite.Group()
setup()

running = True

while running: 
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_angle += angle_speed
            elif event.key == pygame.K_RIGHT:
                to_angle -= angle_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_angle = 0;

    screen.blit(background, (0,0))
    bubble_group.draw(screen)
    shooter.rotate(to_angle)
    shooter.draw(screen)
    pygame.display.update()

pygame.quit()