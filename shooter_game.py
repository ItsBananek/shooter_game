from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 33, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > win_height:
            lost += 1
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

lost = 0
score = 0
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
player = Player('rocket.png', 5, win_height - 100, 80, 100, 10)
bullets = sprite.Group()
asteroids = sprite.Group()
monsters = sprite.Group()
for i in range (5):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
for i in range (3):
    asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), 40, 80, 50, randint(1, 10))
    asteroids.add(asteroid)
finish = False


numfir = 0 
reltime = False
game = True
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
shoot = mixer.Sound("fire.ogg")
lose = font1.render('Вы проиграли!',  True, (255, 0, 0))
win = font1.render('Вы выиграли!',  True, (3, 171, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if numfir < 5 and reltime == False:
                    numfir += 1
                    player.fire()
                    shoot.play()
                if numfir >= 5 and reltime == False:
                    lasttime = timer()
                    reltime = True
    if not finish:
        window.blit(background, (0, 0))
        losttext = font2.render('Пропущено врагов:' + str(lost), 1, (0, 75, 156))
        destroyedtext = font2.render('Уничтожено врагов:' + str(score), 1, (0, 75, 156))
        bullets_and_monsters = sprite.groupcollide(monsters, bullets, True, True)
        if reltime == True:
            nowtime = timer()
            if nowtime - lasttime < 3:
                reloadtext = font2.render('Перезарядка...', 1, (255, 162, 0))
                window.blit(reloadtext, (50, 200))
            else:
                numfir = 0
                reltime = False
        for i in bullets_and_monsters:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, True) or (lost >= 10) or sprite.spritecollide(player, asteroids, True):
            finish = True
            window.blit(lose, (200, 200))
        if score >= 20:
            finish = True
            window.blit(win, (200,200))

        monsters.draw(window)
        bullets.draw(window)
        window.blit(losttext, (10, 50))
        window.blit(destroyedtext, (10, 20))
        player.update()
        bullets.update()
        monsters.update()
        asteroids.update()
        asteroids.draw(window)
        player.reset()
        display.update()
    time.delay(FPS)