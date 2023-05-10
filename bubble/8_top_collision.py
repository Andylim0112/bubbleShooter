import pygame, random, math 
import os

class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position=(0,0)):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)
        self.speed = 5 #speed of the ball

    def set_rect(self, position):
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def set_angle(self, angle):
        self.angle = angle
        self.rad_angle = math.radians(self.angle)

    def move(self):
        to_x = self.speed * math.cos(self.rad_angle)
        to_y = self.speed * math.sin(self.rad_angle) * -1

        self.rect.x += to_x
        self.rect.y += to_y

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.set_angle(180 - self.angle)


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



def get_random_bubble_color():
    colors = []
    for row in map:
        for col in row:
            if col not in colors and col not in [".", "/"]:
                colors.append(col)
    return random.choice(colors)

def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    return Bubble(image, color)


def prepare_bubbles():
    global curr_bubble, next_bubble
    if next_bubble:
        curr_bubble = next_bubble
    else: curr_bubble = create_bubble()
    
    curr_bubble.set_rect((screen_width // 2, 624))
    next_bubble = create_bubble()
    next_bubble.set_rect((screen_width //4, 688))



def process_collision():
    global curr_bubble, fire
    hit_bubble = pygame.sprite.spritecollideany(curr_bubble, bubble_group, pygame.sprite.collide_mask)
    if hit_bubble or curr_bubble.rect.top <= 0:
        row_idx, col_idx = get_map_index(*curr_bubble.rect.center)
        place_bubble(curr_bubble, row_idx,  col_idx)
        curr_bubble = None
        fire = False
        
def get_map_index(x,y):
    row_idx = y // CELL_SIZE
    col_idx = x // CELL_SIZE
    if row_idx % 2 ==1:
        col_idx = (x- (CELL_SIZE // 2)) // CELL_SIZE
        if col_idx < 0:
            col_idx = 0
        elif col_idx > MAP_COLUMN_COUNT -2:
            col_idx = MAP_COLUMN_COUNT -2
    return row_idx, col_idx


def place_bubble(bubble, row_idx, col_idx):
    map[row_idx][col_idx] = bubble.color
    position = get_bubble_position(row_idx, col_idx)
    bubble.set_rect(position)
    bubble_group.add(bubble)



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
MAP_ROW_COUNT = 11
MAP_COLUMN_COUNT = 8

curr_bubble = None # the bubble ur gonna shoot
next_bubble = None # bubble ur gonna shoot next
fire = False #whether the ball is fired or not

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
            elif event.key == pygame.K_SPACE:
                if curr_bubble and not fire:
                    fire = True
                    curr_bubble.set_angle(shooter.angle)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_angle = 0;


    if not curr_bubble:
        prepare_bubbles()


    if fire:
        process_collision()
    screen.blit(background, (0,0))
    bubble_group.draw(screen)
    shooter.rotate(to_angle)
    shooter.draw(screen)
    if curr_bubble:
        if fire:
            curr_bubble.move()
        curr_bubble.draw(screen)


    if next_bubble:
        next_bubble.draw(screen)

    pygame.display.update()

pygame.quit()