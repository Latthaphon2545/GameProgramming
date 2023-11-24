import pygame
import random

# Initializing the pygame module
pygame.init()

# Set the window size
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load and set the background color
img_bg = pygame.image.load('./BG/BG_main.png')
resize_bg = pygame.transform.scale(img_bg, (WIDTH, HEIGHT))
screen.blit(resize_bg, (0, 0))

# Set the window title
pygame.display.set_caption("Covid19War")

# Create rectangles on the screen (x, y, width, height)
WHITE = (255, 255, 255)
pygame.draw.rect(screen, WHITE, (WIDTH/2 - 225, 100, 450, 100))
pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 300, 300, 100))
pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 450, 300, 100))
pygame.draw.rect(screen, WHITE, (20, 680, 100, 100))

# Set the text font
BLACK = (0, 0, 0)
font = pygame.font.SysFont('comicsans', 60)
text = font.render('Covid19War', 1, BLACK)
screen.blit(text, (WIDTH/2 - text.get_width()/2, 100))
text = font.render('Play', 1, BLACK)
screen.blit(text, (WIDTH/2 - text.get_width()/2, 300))
text = font.render('Quit', 1, BLACK)
screen.blit(text, (WIDTH/2 - text.get_width()/2, 450))
text = font.render('?', 1, BLACK)
screen.blit(text, (50, 680))

# Set the clock
clock = pygame.time.Clock()
FPS = 60

# Load sound
boom_sound = pygame.mixer.Sound("boom.wav")

# Initialize variables for the main loop
GAME = True
main = True
total_levels = False
level1 = False
level2 = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.playerImages = [pygame.image.load("JiJiSR/JiJiSR1.png").convert_alpha(),
                             pygame.image.load(
                                 "JiJiSR/JiJiSR1L.png").convert_alpha(),
                             pygame.image.load("JiJiSR/JiJiSR1R.png").convert_alpha()]
        self.image = self.playerImages[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 50
        self.radius = 40
        self.speedx = 0
        self.lastSpeedx = self.speedx
        self.life = 100
        self.score = 0

    def update(self):
        # Update player's horizontal position within screen boundaries
        self.rect.x += self.speedx

        # Limit player's movement to the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.speedx < 0 and self.lastSpeedx != self.speedx:
            self.image = self.playerImages[1]
        elif self.speedx > 0 and self.lastSpeedx != self.speedx:
            self.image = self.playerImages[2]
        elif self.speedx == 0 and self.lastSpeedx != self.speedx:
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
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(1, 10)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < 0:
            # to bounce back
            self.speedx = -self.speedx
        if self.rect.right > WIDTH:
            # to bounce back
            self.speedx = -self.speedx
        if self.rect.top > HEIGHT+10:
            self.reSpawn()


class Cure(pygame.sprite.Sprite):
    def __init__(self, x, y):
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


def main_menu():
    # Set the background color
    img_bg = pygame.image.load('./BG/BG_main.png')
    resize_bg = pygame.transform.scale(img_bg, (WIDTH, HEIGHT))
    screen.blit(resize_bg, (0, 0))

    # Create rectangles on screen (x, y, width, height)
    pygame.draw.rect(screen, WHITE, (WIDTH/2 - 225, 100, 450, 100))
    pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 300, 300, 100))
    pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 450, 300, 100))
    pygame.draw.rect(screen, WHITE, (20, 680, 100, 100))

    # Set the text font
    text = font.render('Covid19War', 1, BLACK)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, 100))
    text = font.render('Play', 1, BLACK)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, 300))
    text = font.render('Quit', 1, BLACK)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, 450))
    text = font.render('?', 1, BLACK)
    screen.blit(text, (50, 680))


def choose_level():
    BLACK = (0, 0, 0)
    screen.fill(BLACK)

    # Title
    pygame.draw.rect(screen, WHITE, (WIDTH/2 - 225, 100, 450, 100))
    text = font.render('Level', 1, BLACK)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, 100))

    # Levels
    for i in range(3):
        pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 300 + i*150, 300, 100))
        text = font.render('Level ' + str(i+1), 1, BLACK)
        screen.blit(text, (WIDTH/2 - text.get_width()/2, 300 + i*150))

    # Back
    pygame.draw.rect(screen, WHITE, (20, 680, 100, 100))
    text = font.render('<', 1, BLACK)
    screen.blit(text, (50, 680))


def level_set():
    img_bg_in_game = pygame.image.load('./BG/BG_in_game.png')
    resize_bg_in_game = pygame.transform.scale(img_bg_in_game, (WIDTH, HEIGHT))
    screen.blit(resize_bg_in_game, (0, 0))


while GAME:
    while main:
        main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                GAME = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] >= WIDTH/2 - 150 and pos[0] <= WIDTH/2 + 150 and pos[1] >= 300 and pos[1] <= 400:
                    print('Play')
                    choose_level()
                    main = False
                    total_levels = True
                if pos[0] >= WIDTH/2 - 150 and pos[0] <= WIDTH/2 + 150 and pos[1] >= 450 and pos[1] <= 550:
                    print('Quit')
                    main = False
                    GAME = False
                if pos[0] >= 20 and pos[0] <= 120 and pos[1] >= 680 and pos[1] <= 780:
                    print('?')
        pygame.display.update()

    while total_levels:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                total_levels = False
                GAME = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] >= WIDTH/2 - 150 and pos[0] <= WIDTH/2 + 150 and pos[1] >= 300 and pos[1] <= 400:
                    print('Level 1')
                    level1 = True
                    total_levels = False
                if pos[0] >= WIDTH/2 - 150 and pos[0] <= WIDTH/2 + 150 and pos[1] >= 450 and pos[1] <= 550:
                    print('Level 2')
                    level2 = True
                    total_levels = False
                if pos[0] >= WIDTH/2 - 150 and pos[0] <= WIDTH/2 + 150 and pos[1] >= 600 and pos[1] <= 700:
                    print('Level 3')
                if pos[0] >= 20 and pos[0] <= 120 and pos[1] >= 680 and pos[1] <= 780:
                    print('<')
                    main = True
                    total_levels = False
        pygame.display.update()

    if level1:
        allsprites = pygame.sprite.Group()
        covids = pygame.sprite.Group()
        cures = pygame.sprite.Group()

        player = Player()
        allsprites.add(player)

        # Spawn a group of covids
        for i in range(15):
            c = Covid()
            allsprites.add(c)
            covids.add(c)

        while level1:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    level1 = False
                    GAME = False

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

            # Process
            allsprites.update()

            # Check if a covid hit the player
            player_hit = pygame.sprite.spritecollide(player, covids, False)
            if player_hit:
                player.life -= 1
                boom_sound.play()

            # Check if a cure hit a covid
            cures_hits = pygame.sprite.groupcollide(covids, cures, True, True)
            for hit in cures_hits:
                c = Covid()
                allsprites.add(c)
                covids.add(c)
                player.score += 100

            # Output
            screen.fill((0, 0, 0))
            allsprites.draw(screen)
            pygame.draw.rect(screen, (0, 255, 255), (10, 10, player.life, 10))
            textScore = font.render(
                "score " + str(player.score), True, (0, 255, 255))
            screen.blit(textScore, ((WIDTH-textScore.get_width())/2, 10))
            if player.score == 200:
                level1 = False
                main = True
            pygame.display.flip()

pygame.quit()
