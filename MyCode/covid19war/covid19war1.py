import random
import pygame

#setup
WIDTH = 600
HEIGHT = 800
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Covid19War")
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
        self.rect.midbottom = WIDTH/2, HEIGHT-150
        self.speedx = 0
    def update(self):
        self.rect.x += self.speedx
        if self.speedx < 0:
            self.image = self.playerImages[1]
        elif self.speedx > 0:
            self.image = self.playerImages[2]
        else:
            self.image = self.playerImages[0]



allsprites = pygame.sprite.Group()
player = Player()
allsprites.add(player)

while running:
    clock.tick(FPS)
#input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speedx = -10
            if event.key == pygame.K_RIGHT:
                player.speedx = 10
            if event.key == pygame.K_SPACE:
                player.shoot()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.speedx = 0
            if event.key == pygame.K_RIGHT:
                player.speedx = 0

#process
    allsprites.update()

#output
    screen.fill((0,0,0))
    allsprites.draw(screen)
    pygame.display.flip()

pygame.quit()
