from pygame import *
from random import choice, randint

class GameSprite(sprite.Sprite):
    def __init__(self, img, x,y, w,h):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Snake(GameSprite):
    def __init__(self, img, x,y, w,h, t):
        super().__init__(img, x,y, w,h)
        self.type = t
        self.speed = 25
        self.direction = '0'
        self.cur_image = self.image
        self.wait = 30

    def update(self):
        if self.direction == 'l':
            self.rect.x -= self.speed
        elif self.direction == 'r':
            self.rect.x += self.speed
        elif self.direction == 'u':
            self.rect.y -= self.speed
        elif self.direction == 'd':
            self.rect.y += self.speed

    def get_direction(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.direction!='r':
            self.direction = 'l'
            self.image = transform.rotate(self.cur_image, -90)
        if keys[K_RIGHT] and self.direction!='r':
            self.direction = 'r'
            self.image = transform.rotate(self.cur_image, 90)
        if keys[K_UP] and self.direction!='u':
            self.direction = 'u'
            self.image = transform.rotate(self.cur_image, 180)           
        if keys[K_DOWN] and self.direction!='d':
            self.direction = 'd'
            self.image = transform.rotate(self.cur_image, 0)

    def set_direct(self):
        if self.direction == 'l':
            self.image = transform.rotate(self.cur_image, -90)
        if self.direction == 'r':
            self.image = transform.rotate(self.cur_image, 90)
        if self.direction == 'u':
            self.image = transform.rotate(self.cur_image, 180)           
        if self.direction == 'd':
            self.image = transform.rotate(self.cur_image, 0)

    def eat(self, food):
        global speed
        speed +=1
        food.position()


class Food(GameSprite):
    def __init__(self, imgs, x,y, w,h):
        super().__init__(imgs[0], x,y, w,h)
        self.costumes = []
        self.costumes.append(self.image)
        for i in range(len(imgs)-1):
            self.image = transform.scale(image.load(imgs[i+1]),(w,h))
            self.costumes.append(self.image)

    def set_costume(self, n):
        self.image = self.costumes[n]

    def rand_costume(self):
        self.image = choice(self.costumes)

    def position(self):
        self.rect.x = randint(randint(0, 700-self.rect.width)/25)*25
        self.rect.y = randint(randint(0, 500-self.rect.height)/25)*25
        self.rand_costume()

font.init()
font1 = font.SysFont('Arial',30)

head = Snake('litso.png',350,250, 25,25, 0)
tail = Snake('telo.png', 350, 225, 25,25, 0)
snake = [head, tail]
food = Food(['Untitled.png', 'watermalon.png'], -100, -100, 25, 25)

#torso = Snake('torso.png',)

window = display.set_mode((700,500))
display.set_caption('Snake')



game = True
clock = time.Clock()
fps = 60
speed = 1
global_wait = fps

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill((180,200,180))

    window.fill((255,255,255))
    head.get_direction()
    if wait == 0:
        wait = head.wait()
        for e in range(1, len(snake)-1,0,-1):
            snake[e].reset()
            snake[e].direction = snake[e-1].direction
            snake[e].rect.x = snake[e-1].rect.x
            snake[e].rect.y = snake[e-1].rect.y
            snake[e].set_direct()
        head.update()

    else:
        wait -= 1
    head.reset()
    food.reset()
    for s in snake:
        s.reset()
    if head.rect.colliderect(food):
        head.eat(food)
        s = Snake('2.png', head.rect.x, head.rect.y, 25, 25, 0)
        snake.insert(1,s)
    if speed%5 == 0:
        head.wait -=2
        if head.wait <2:
            head.wait = 2

    score_text = font1.render('Счёт:'+str(score), 1, (0,0,0))
    window.blit(score_text, (10,10))

    clock.tick(fps)
    display.update()
    food.reset()
