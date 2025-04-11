from pygame import *
from random import randint



WIN_W = 700
WIN_H = 500
FPS = 60
x1= 300
x2= 500
y1= 200
y2= 400
SIZE= 30
SIZE1= 40
SPEED= 4
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
UFOS = 5


class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h):
        super().__init__()
        self.image = transform.scale(
            image.load(img),
            (w, h)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, img, x, y, w, h, speed=SPEED):
        super().__init__(img, x, y, w, h)
        self.speed = speed
        self.shoots = 0
        self.missed = 0
        self.bullets = sprite.Group()

    def update(self, up, down, left, right):
        keys_pressed = key.get_pressed()
        if keys_pressed[left] and self.rect.x > 5:
            self.rect.x -= SPEED
        if keys_pressed[right] and self.rect.x < WIN_W - SIZE:
            self.rect.x += SPEED
        if keys_pressed[up] and self.rect.y > 5:
            self.rect.y -= SPEED
        if keys_pressed[down] and self.rect.y < WIN_H - SIZE:
            self.rect.y += SPEED

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + self.rect.width/2,self.rect.y,10,20,10)
        self.bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, img, x, y, w, h, speed=SPEED):
        super().__init__(img, x, y, w, h)
        self.rect.x = randint(0, WIN_W - self.rect.width)
        self.rect.y = randint(0, 40)
        self.speed=speed
    def update(self,rocket, is_ufo=True):
        if self.rect.y >= WIN_H:
            rocket.missed += 1
            self.rect.x = randint(0, WIN_W - self.rect.width)
            self.rect.y = randint(0, 40)
        self.rect.y += self.speed

class Bullet(GameSprite):
    def __init__(self, img, x, y, w, h, speed=SPEED):
        super().__init__(img, x, y, w, h)
        self.speed = speed

    def update(self):
        if self.rect.y <= 0:
            
            self.kill()
        self.rect.y -= self.speed


window = display.set_mode((WIN_W, WIN_H))

clock = time.Clock()

display.set_caption("Догонялки")

font.init()
title_font=font.SysFont('papyrus', 70)
win= title_font.render('Win', True, GREEN)
lost = title_font.render('ahah LOSE!!', True, RED)

lable_font=font.SysFont('papyrus', 20 )
count_txt = lable_font.render('Count', True, WHITE)
missed_txt = lable_font.render('Missed', True, WHITE)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.5)


background = GameSprite('galaxy.jpg', 0, 0, WIN_W, WIN_H)


ufos = sprite.Group()
for i in range(UFOS):
    enemy = Enemy('ufo.png', 0, 0, 70, 50,2)
    ufos.add(enemy)
rocket = Player('rocket.png', WIN_W // 2, WIN_H - 100,  35, 65,7) 


finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
    if not finish:
        background.draw(window)
        

        count = lable_font.render(str(rocket.shoots), True, WHITE)
        missed = lable_font.render(str(rocket.missed), True, WHITE)   

        window.blit(count_txt, (10, 10))
        window.blit(count, (100, 10))
        window.blit(missed_txt, (10, 30))
        window.blit(missed, (100, 30))

        ufos.draw(window)
        ufos.update(rocket)

        rocket.bullets.draw(window)
        rocket.bullets.update()

        rocket.draw(window)

        rocket.update(K_w, K_s, K_a, K_d)
        
        
        ufo_vs_bullets = sprite.groupcollide(
            ufos, rocket.bullets, True, True
        )   

        for collision in ufo_vs_bullets:
            rocket.shoots += 1
            enemy = Enemy('ufo.png', 0, 0, 70, 50,2)
            ufos.add(enemy)
        
        if sprite.spritecollide(rocket, ufos, False):
            window.blit(lost, (100, 200))
            display.update()
            finish = True

        if rocket.missed >= 7:
            window.blit(lost, (100, 200))
            display.update()
            finish = True

        if rocket.shoots >= 10:
            window.blit(win, (100, 200))
            display.update()
            finish = True

    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)