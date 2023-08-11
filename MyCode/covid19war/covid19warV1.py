import random
import pygame

#setup
WIDTH = 600
HEIGHT = 800
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Covid19War")
font = pygame.font.SysFont("robotto", 40, bold=True)
bg = pygame.image.load("bg.png")
bg_offset = bg.get_height()-HEIGHT
pygame.mixer.init()
boom_sound = pygame.mixer.Sound("boom.wav")
clock = pygame.time.Clock()
running = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.playerImages = [pygame.image.load("JiJiSR1.png").convert_alpha(),
                         pygame.image.load("JiJiSR1L.png").convert_alpha(),
                         pygame.image.load("JiJiSR1R.png").convert_alpha()]
        self.image = self.playerImages[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = WIDTH/2, HEIGHT-50
        self.radius = 40
        self.speedx = 0
        self.lastSpeedx = self.speedx
        self.life = 100
        self.score = 0

    def update(self):
        self.rect.x += self.speedx
        if (self.speedx < 0 ) and (self.lastSpeedx != self.speedx):
            #print("left",self.lastSpeedx,self.speedx)
            self.image = self.playerImages[1]
        elif (self.speedx > 0 ) and (self.lastSpeedx != self.speedx):
            #print("right",self.lastSpeedx,self.speedx)
            self.image = self.playerImages[2]
        elif (self.speedx == 0)  and (self.lastSpeedx != self.speedx):
            #print("center",self.lastSpeedx,self.speedx)
            self.image = self.playerImages[0]
        self.lastSpeedx = self.speedx
    def shoot(self):
        cure = Cure(self.rect.centerx, self.rect.top)
        allsprites.add(cure)
        cures.add(cure)

class Covid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("covid19.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*.7/2)
        self.reSpawn()
    def reSpawn(self):
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedx = random.randrange(-2,2)
        self.speedy = random.randrange(1,10)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT+10:
            self.reSpawn()

class Cure(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cure.png").convert_alpha()
        self.image_orig = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
    def update(self):
        self.rect.y += self.speedy
        self.rotate()
        if self.rect.bottom < 0:
            self.kill()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            print("rotate")

allsprites = pygame.sprite.Group()
covids = pygame.sprite.Group()
cures = pygame.sprite.Group()

player = Player()
allsprites.add(player)
for i in range(10):
    c = Covid()
    allsprites.add(c)
    covids.add(c)
time_cnt = 600
while running:
    clock.tick(FPS)
#input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speedx = -6
            if event.key == pygame.K_RIGHT:
                player.speedx = 6
            if (event.key == pygame.K_SPACE) and (player.life > 0):
                player.shoot()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.speedx = 0
            if event.key == pygame.K_RIGHT:
                player.speedx = 0
            if (event.key == pygame.K_RETURN) and (player.life < 0):
                player.life = 100
                player.score = 0

#process
    allsprites.update()
    player_hit = pygame.sprite.spritecollide(player,covids,False,pygame.sprite.collide_circle)
    if player_hit:
        player.life -= 1
        boom_sound.play()
    cures_hits = pygame.sprite.groupcollide(covids, cures,True,True)
    for hit in cures_hits:
        c = Covid()
        allsprites.add(c)
        covids.add(c)
        player.score += 100
    if time_cnt > 0:
        time_cnt -= 1
    elif bg_offset > 0:
        time_cnt = 120
        bg_offset -= 1
#output
    #screen.fill((0,0,0))
    screen.blit(bg,(-0,-bg_offset))
    allsprites.draw(screen)
    for hit in cures_hits:
        pygame.draw.circle(screen,(255,255,255),hit.rect.center,40)
    pygame.draw.rect(screen,(0,255,255),(10,10,player.life,10))
    textScore = font.render("score " + str(player.score), True, (0,255,255))
    screen.blit(textScore,((WIDTH-textScore.get_width())/2, 10))
    if player.life < 0:
        textOver = font.render("Game Over ", True, (0,255,255))
        screen.blit(textOver,((WIDTH-textOver.get_width())/2, HEIGHT/2-50))
        textOver = font.render("Press Enter to try again", True, (0,255,255))
        screen.blit(textOver,((WIDTH-textOver.get_width())/2, HEIGHT/2))
    pygame.display.flip()

pygame.quit()
