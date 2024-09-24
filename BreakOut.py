import pygame
import random
from random import randint as r

from pygame.examples.eventlist import virtual_x

pygame.init() # russell test

pygame.font.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

class Player(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 25)  # arbitrary values TODO tweak
        self.vx=0
        self.speed = 10

    def draw(self):
        pygame.draw.rect(screen, 'teal', self, 0, border_radius=4) # fill = 0, outline = 1
#        pygame.draw.rect(screen, 'black', self, 1)

    def update(self):
        self.x += self.vx
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > screen.get_width():
            self.x = screen.get_width() - self.width

class Ball(pygame.Rect):

    def __init__(self, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
#        self.vx = r(2, 5) *  random.choice([1, -1])
#        self.vy = r(2, 4) #TODO tweak?
        self.vx = 0
        self.vy = 10
        self.bounceCount = 0

    def draw(self):
        pygame.draw.rect(screen, 'white', self, 0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if ball.x < 0:
            self.bounceCount=0
            ball.vx = -ball.vx
        if ball.x > screen.get_width() - ball.width:
            self.bounceCount = 0
            ball.vx = -ball.vx
        if ball.y < 0:
            self.bounceCount = 0
            ball.vy = -ball.vy
        if ball.y > screen.get_height():
            ball.y = screen.get_height()/2

class Brick(pygame.Rect):
    WIDTH = 80
    HEIGHT = 30

    def __init__(self, x, y):
        super().__init__(x, y, Brick.WIDTH, Brick.HEIGHT)
        self.color = (r(0,255), r(0,255), r(0,255))
#        self.right_box = pygame.Rect(self.right - 10, self.top + 4, 8, 12)
#        self.left_box = pygame.Rect(self.left + 2, self.top + 4, 8, 12)

    def draw(self):
        pygame.draw.rect(screen, self.color, self, 0, border_radius = 4)  # fill = 0, outline = 1
#        pygame.draw.rect(screen, 'black', self.right_box, 0)
#        pygame.draw.rect(screen, 'black', self.left_box, 0)



player = Player(screen.get_width()/2 - 50, screen.get_height() - 50)
ball = Ball(screen.get_width()/2 - 10, screen.get_height()/2 + 20, 20)

bricks = []
for x in range(4, screen.get_width()-Brick.WIDTH, Brick.WIDTH+4):
    for y in range(100, 300, Brick.HEIGHT+4):
        bricks.append(Brick(x, y))

while True:
    # Process player inputs.
#    player.x=pygame.mouse.get_pos()[0]-player.width/2
    ball.x = pygame.mouse.get_pos()[0] - ball.width / 2
    ball.y = pygame.mouse.get_pos()[1] - ball.height/2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
#        elif event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
#                player.vx = -player.speed
#            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
#                player.vx = player.speed
#        elif event.type == pygame.KEYUP:
#            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and player.vx == -player.speed:
#                player.vx = 0
#            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and player.vx == player.speed:
#                player.vx = 0


    # Do logical updates here.
    player.update()
    ball.update()

    if player.colliderect(ball) and ball.bounceCount == 0:
        ball.bounceCount+=1
        ball.vy*=-1
        diff = (ball.x + ball.w/2) - (player.x + player.w/2)
        ball.vx += diff//10

    for x in bricks:
        if x.colliderect(ball):
            ball.bounceCount = 0
            ball.vy *= -1
            diff = (ball.x + ball.w / 2) -(x.x + x.w / 2)
            ball.vx += diff // 10
            bricks.remove(x)
#        if ball.colliderect(x.right_box) and ball.right > x.right_box.right and ball.vx < 0:


    screen.fill('black')  # Fill the display with a solid color

    # Render the graphics here.
    player.draw()
    ball.draw()
    for x in bricks:
        x.draw()
    if (len(bricks)==0):
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render('You Win!', False, (255, 255, 255))
        screen.blit(text_surface, (0, 0))



    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
