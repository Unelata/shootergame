from pygame import *
from random import randint

lost = 0
score = 0
lifes = 10

'''Необходимые классы'''

#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 430:
            self.rect.y += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    # direction = "left"
    def update(self):
        global lost
        global score
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -100
            self.rect.x = randint(0, 600)
            if self.speed == 5:
                score -= 1
            elif self.speed == 4:
                score -= 5
            elif self.speed == 3:
                score -= 10
            elif self.speed == 2:
                score -= 15
            else:
                score -= 20
            self.speed = randint(1, 5)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#Персонажи игры:
player = Player('rocket.png', 200, 400, 50, 80, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0, 600), -100, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(0, 600), -100, 80, 50, randint(1, 5))
    asteroids.add(asteroid)


#Игровая сцена:
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

menu = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

# screamer = transform.scale(image.load('кот.jpg'), (win_width, win_height))


game = True
clock = time.Clock()
FPS = 60

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
scream = mixer.Sound('fire.ogg')


finish = False
font.init()
font2 = font.SysFont('Arial', 50)
font1 = font.SysFont('Arial', 30)
win = font2.render('WIN', True, (100, 200, 250))
menutext = font2.render('Нажмите R для продолжения игры', True, (0, 0, 0))
losetext = font2.render('Вы проиграли!', True, (255, 255, 255))
wintext = font2.render('Вы выиграли!', True, (255, 255, 255))
menutext2 = font2.render('', True, (255, 255, 255))

finish = False
pause = 1

fire_sound = mixer.Sound('fire.ogg')
bullets = sprite.Group()

bullets_count = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_p:
                finish = True
                pause = 1
            if e.key == K_r:
                finish = False
            if e.key == K_l:
                score = 0
                lost = 0
                for m in monsters:
                    m.rect.y = -100
            if e.key == K_SPACE and bullets_count < 10:
                fire_sound.play()
                player.fire()
                bullets_count += 1
                waittime = 0

    if not finish:
        window.blit(background,(0, 0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)

        bullets.update()
        bullets.draw(window)

        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 10))
        text_score = font1.render('Счёт:' + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 30))
        lifestext = font2.render(str(lifes), True, (255, 255, 255))
        window.blit(lifestext, (650, 10))

        if player.rect.y < 0:
            window.blit(screamer, (0, 0))
            scream.play()

        if bullets_count == 10 and waittime < 120:
            text = font2.render('Перезарядка', True, (255, 255, 255))
            window.blit(text, (235, 230))
            waittime += 1

        elif bullets_count == 10 and waittime >= 120:
            waittime = 0
            bullets_count = 0

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            monster = Enemy('ufo.png', randint(0, 600), -100, 80, 50, randint(1, 5))
            monsters.add(monster)
            score += 10

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            if sprite.spritecollide(player, monsters, True):
                monster = Enemy('ufo.png', randint(0, 600), -100, 80, 50, randint(1, 5))
                monsters.add(monster)
            if sprite.spritecollide(player, monsters, True):
                monster = Enemy('asteroid.png', randint(0, 600), -100, 80, 50, randint(1, 5))
                monsters.add(asteroid)
            lifes -= 1

            #menutext2 = losetext
            #pause = 0
        
        if lifes <= 0 or lost > 5:
            finish = True
            menutext2 = losetext
            pause = 0

        if score > 100:
            finish = True
            menutext2 = wintext
            pause = 0
    
    else:
        window.blit(menu, (0, 0))
        if pause:
            # window.blit(menu, (0, 0))
            window.blit(menutext, (40, 230))
        
        else:
            # window.blit(menu, (0, 0))
            window.blit(menutext2, (225, 220))
            score = 0
            lost = 0
            lifes = 10
            bullets_count = 0
            player.rect.x = 300
            player.rect.y = 400
            for m in monsters:
                m.rect.x = randint(0, 600)
                m.rect.y = -100
            for m in asteroids:
                m.rect.x = randint(0, 600)
                m.rect.y = -100
            for b in bullets:
                b.kill()
            finish = False
            display.update()
            time.delay(3000)
        

    display.update()
    clock.tick(FPS)