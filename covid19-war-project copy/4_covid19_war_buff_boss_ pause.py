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

# pause game
pause = False

# Load img sound
img_sound = pygame.image.load('sound.png')
img_unsound = pygame.image.load('unsound.png')
img_sound = pygame.transform.scale(img_sound, (70, 70))
img_unsound = pygame.transform.scale(img_unsound, (70, 70))

# Load sound
boom_sound = pygame.mixer.Sound("boom.wav")
boom_sound.set_volume(0.3)
pygame.mixer.music.load("bg.mp3")
pygame.mixer.music.set_volume(0.1)

# Initialize variables for the main loop
GAME = True
main = True
total_levels = False
level1 = False
boss1 = False
doctor = 0
img_value = 0
level2 = False
boss2 = False
level3 = False
boss3 = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.playerImages = [   pygame.image.load("JiJiSR/JiJiSR1.png").convert_alpha(),
                                pygame.image.load("JiJiSR/JiJiSR1L.png").convert_alpha(),
                                pygame.image.load("JiJiSR/JiJiSR1R.png").convert_alpha()
                             ]
        self.image = self.playerImages[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 50
        self.radius = 40
        self.speedx = 0
        self.lastSpeedx = self.speedx
        self.life = 100
        self.score = 0
        self.invulnerable_buff = False  # New: Player's invulnerability state
        self.invulnerable_timer_buff = 0  # New: Timer for invulnerability
        self.time_invulnerable_buff = 5000

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

        # Check for invulnerability timer
        if self.invulnerable_buff:
            # set image transparency to 50%
            self.image.set_alpha(128)
            current_time = pygame.time.get_ticks()
            # show time left in game window
            time_left = self.time_invulnerable_buff - (current_time - self.invulnerable_timer_buff)
            print(time_left)
            if current_time - self.invulnerable_timer_buff >= self.time_invulnerable_buff:
                self.invulnerable_buff = False
                self.playerImages = [   pygame.image.load("JiJiSR/JiJiSR1.png").convert_alpha(),
                                        pygame.image.load("JiJiSR/JiJiSR1L.png").convert_alpha(),
                                        pygame.image.load("JiJiSR/JiJiSR1R.png").convert_alpha()
                                    ]
                self.image = self.playerImages[0]

                
    def shoot(self):
        cure = Cure(self.rect.centerx, self.rect.top)
        allsprites.add(cure)
        cures.add(cure)
        
class Covid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("covid19.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
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

class Buff(pygame.sprite.Sprite):
    def __init__(self, buff_type):
        pygame.sprite.Sprite.__init__(self)
        self.buff_type = buff_type
        self.image = pygame.image.load(f"Buff/buff{buff_type}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)

    def apply_buff(self, player):
        if self.buff_type == 1:
            # Buff 1: Make the player invulnerable for 3 seconds
            player.invulnerable_buff = True
            player.invulnerable_timer_buff = pygame.time.get_ticks()
            # clear buff
            self.kill()          
        
        elif self.buff_type == 2:
            # Buff 2: Clear all COVID-19 viruses
            for covid in covids:
                covid.kill()
            # Spawn a new group of COVID-19 viruses
            spawn_covid(5)
            # clear buff
            self.kill()

        elif self.buff_type == 3:
            # Buff 3: Increase player's life
            player.life += 10  # You can adjust the amount as needed
            # clear buff
            self.kill()

        elif self.buff_type == 4:
            global doctor
            doctor += 1

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("boss.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.top = 20
        self.speedx = 2
        self.health = 200
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 2000
    

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx = -self.speedx
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            laser = Laser(self.rect.centerx, self.rect.bottom)
            allsprites.add(laser)
            boss_lasers.add(laser)
    
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill()

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
    # text = font.render('?', 1, BLACK)
    # screen.blit(text, (50, 680))
    screen.blit(img_sound, (35, 695))
    if img_value%2 == 0:
        screen.blit(img_sound, (35, 695))
    else:

        screen.blit(img_unsound, (35, 695))

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

def spawn_covid(amount):
    for i in range(amount):
        c = Covid()
        allsprites.add(c)
        covids.add(c)

def player_loss():
    RED = (255, 0, 0)
    screen.fill(RED)
    # Score
    text = font.render('Score: ' + str(player.score), 1, WHITE)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, 200))
    # Game over
    text = font.render('Game Over', 1, WHITE)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, 300))
    # Back
    pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 400, 300, 100))
    text = font.render('Menu(M)', 1, BLACK)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, 400))

def player_win():
    GREEN = (0, 255, 0)
    screen.fill(GREEN)
    # Score
    text = font.render('Score: ' + str(player.score), 1, WHITE)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, 200))
    # Game over
    text = font.render('You Win', 1, WHITE)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, 300))
    # Back
    pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 400, 300, 100))
    text = font.render('Menu(M)', 1, BLACK)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, 400))

pygame.mixer.music.play()
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
                    img_value += 1
                    if img_value%2 == 0:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main = False
                    GAME = False
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
                    level2 = False
                    level3 = False
                    total_levels = False
                if pos[0] >= WIDTH/2 - 150 and pos[0] <= WIDTH/2 + 150 and pos[1] >= 450 and pos[1] <= 550:
                    print('Level 2')
                    level1 = False  
                    level2 = True
                    level3 = False
                    total_levels = False
                if pos[0] >= WIDTH/2 - 150 and pos[0] <= WIDTH/2 + 150 and pos[1] >= 600 and pos[1] <= 700:
                    print('Level 3')
                    level1 = False
                    level2 = False
                    level3 = True
                    total_levels = False
                if pos[0] >= 20 and pos[0] <= 120 and pos[1] >= 680 and pos[1] <= 780:
                    print('<')
                    total_levels = False
                    main = True
        pygame.display.update()

    if level1:
        allsprites = pygame.sprite.Group()
        covids = pygame.sprite.Group()
        cures = pygame.sprite.Group()
        buffs = pygame.sprite.Group()

        player = Player()
        allsprites.add(player)

        # Spawn a group of covids
        spawn_covid(113)

        while level1:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    level1 = False
                    GAME = False

                if event.type == pygame.KEYDOWN:
                    if not pause:
                        if event.key == pygame.K_LEFT:
                            player.speedx = -10
                        if event.key == pygame.K_RIGHT:
                            player.speedx = 10
                        if event.key == pygame.K_SPACE:
                            player.shoot()       
                    if event.key == pygame.K_p:
                        if pause:
                            pause = False
                        else:
                            pause = True
                    if event.key == pygame.K_m:
                        level1 = False
                        main = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.speedx = 0
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 0

            if pause:
                # Make to draw.rect show on screen when pause with text pause
                pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 300, 300, 100))
                text = font.render('Menu(M)', 1, BLACK)
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 300))
                # Make only text ro resume game under menu(M)
                text = font.render('Press P to resume game', 1, WHITE)
                text = pygame.transform.scale(text, (text.get_width()/3, text.get_height()/3))
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 410))


            if not pause:
                # Process
                allsprites.update()
                # boss_lasers.update()

                # Check if a covid hit the player
                if not player.invulnerable_buff:
                    player_hit = pygame.sprite.spritecollide(player, covids, False)
                    if player_hit:
                        player.life -= 10
                        # delete covid on the touch of player
                        for hit in player_hit:
                            hit.kill()
                            # add new covid
                            c = Covid()
                            allsprites.add(c)
                            covids.add(c)
                
                # Check if a cure hit a covid
                cures_hits = pygame.sprite.groupcollide(covids, cures, True, True)
                for hit in cures_hits:
                    c = Covid()
                    allsprites.add(c)
                    covids.add(c)
                    player.score += 100

                # Create buffs with random chance
                if random.randint(1, 300) == 1:
                    buff_type = random.randint(1, 3)  # Randomly choose one of the three buff types
                    buff = Buff(buff_type)
                    allsprites.add(buff)
                    buffs.add(buff)

                if random.randint(1, 500) == 1:
                    buff_type = 4
                    buff = Buff(buff_type)
                    allsprites.add(buff)
                    buffs.add(buff)

                # Check if a buff hits the player and apply its effect
                buff_hits = pygame.sprite.spritecollide(player, buffs, True)
                for buff in buff_hits:
                    buff.apply_buff(player)

                if doctor == 2:
                    doctor = 0
                    level1 = False
                    boss1 = True

                # Output
                bg_in_game = pygame.image.load('./BG/BG_in_game.png')
                resize_bg_in_game = pygame.transform.scale(bg_in_game, (WIDTH, HEIGHT))
                screen.blit(resize_bg_in_game, (0, 0))
                # screen.fill((0, 0, 0))

                allsprites.draw(screen)

                if player.life <= 0:
                    player_loss()

                else:
                    # Draw amount of doctor and show buff4 in text beside doctor
                    # pygame.draw.rect(screen, (255, 255, 255), (500, 20, 50, 80))
                    img_buff4 = pygame.image.load("Buff/buff4.png")
                    img_buff4 = pygame.transform.scale(img_buff4, (50, 50))
                    screen.blit(img_buff4, (500, 20))
                    textDoctor = font.render(str(doctor), True, BLACK)
                    textDoctor = pygame.transform.scale(textDoctor, (textDoctor.get_width()/2, textDoctor.get_height()/2))
                    screen.blit(textDoctor, (518, 60))

                    pygame.draw.rect(screen, BLACK, (10, 50, player.life, 30))
                    # Draw player's life in text beside life bar
                    if player.life >= 100:
                        textLife = font.render("life player: " + str(player.life)[0] + str(player.life)[1], True, BLACK)
                    else:
                        textLife = font.render("life player: " + str(player.life)[0], True, BLACK)
                    # resize textLife
                    textLife = pygame.transform.scale(textLife, (textLife.get_width()/4, textLife.get_height()/4))
                    screen.blit(textLife, (10, 20))

                    textScore = font.render("score " + str(player.score), True, BLACK)
                    screen.blit(textScore, ((WIDTH-textScore.get_width())/2, 10))
            
            pygame.display.flip()

    if boss1:
        allsprites = pygame.sprite.Group()
        cures = pygame.sprite.Group()
        boss = Boss()
        boss_lasers = pygame.sprite.Group()

        allsprites.add(player)
        allsprites.add(boss)
        print(doctor)

        while boss1:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    boss1 = False
                    GAME = False

                if event.type == pygame.KEYDOWN:
                    if not pause:
                        if event.key == pygame.K_LEFT:
                            player.speedx = -10
                        if event.key == pygame.K_RIGHT:
                            player.speedx = 10
                        if event.key == pygame.K_SPACE:
                            player.shoot()
                    if event.key == pygame.K_ESCAPE:
                        if pause:
                            pause = False
                        else:
                            pause = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.speedx = 0
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 0
            if pause:
                # Make to draw.rect show on screen when pause with text pause
                pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 300, 300, 100))
                text = font.render('Pause', 1, BLACK)
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 300))
                pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 450, 300, 100))
                text = font.render('Quit', 1, BLACK)
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 450))
                pygame.display.flip()
            
            if not pause:
                # Process
                allsprites.update()
                boss_lasers.update()

                # Check if player or boss is defeated
                laser_hits = pygame.sprite.spritecollide(player, boss_lasers, True)
                for hit in laser_hits:
                    player.life -= 10

                # Check if a cure hit a boss deleat boss health by 10 and delete boss when health is 0
                boss_hits = pygame.sprite.spritecollide(boss, cures, True)
                for hit in boss_hits:
                    boss.health -= 10
                    if boss.health == 0:
                        boss.kill()
                        player.score += 1000
                        level2 = True
                        boss1 = False

                # Output
                bg_in_game = pygame.image.load('./BG/BG_in_game.png')
                resize_bg_in_game = pygame.transform.scale(bg_in_game, (WIDTH, HEIGHT))
                screen.blit(resize_bg_in_game, (0, 0))
                # screen.fill((0, 0, 0))
                allsprites.draw(screen)
                allsprites.draw(screen)

                pygame.draw.rect(screen, BLACK, (10, 50, player.life, 30))
                # Draw player's life in text beside life bar
                if player.life >= 100:
                    textLife = font.render("life player: " + str(player.life)[0] + str(player.life)[1], True, BLACK)
                else:
                    textLife = font.render("life player: " + str(player.life)[0], True, BLACK)
                # resize textLife
                textLife = pygame.transform.scale(textLife, (textLife.get_width()/4, textLife.get_height()/4))
                screen.blit(textLife, (10, 20))

                # Draw boss's life
                pygame.draw.rect(screen, WHITE, (10, 130, boss.health, 30))
                if boss.health >= 100:
                    textBossLife = font.render("life boss: " + str(boss.health)[0] + str(boss.health)[1], True, WHITE)
                else:
                    textBossLife = font.render("life boss: " + str(boss.health)[0], True, WHITE)
                # resize textBossLife
                textBossLife = pygame.transform.scale(textBossLife, (textBossLife.get_width()/4, textBossLife.get_height()/4))
                screen.blit(textBossLife, (10, 100))


                textScore = font.render("score " + str(player.score), True, BLACK)
                screen.blit(textScore, ((WIDTH-textScore.get_width())/2, 10))
                pygame.display.flip()

    if level2:
        allsprites = pygame.sprite.Group()
        covids = pygame.sprite.Group()
        cures = pygame.sprite.Group()
        buffs = pygame.sprite.Group()

        player = Player()
        allsprites.add(player)

        # Spawn a group of covids
        spawn_covid(10)

        while level2:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    level2 = False
                    GAME = False

                if event.type == pygame.KEYDOWN:
                    if not pause:
                        if event.key == pygame.K_LEFT:
                            player.speedx = -10
                        if event.key == pygame.K_RIGHT:
                            player.speedx = 10
                        if event.key == pygame.K_SPACE:
                            player.shoot()       
                    if event.key == pygame.K_p:
                        if pause:
                            pause = False
                        else:
                            pause = True
                    if event.key == pygame.K_m:
                        level1 = False
                        main = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.speedx = 0
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 0

            if pause:
                # Make to draw.rect show on screen when pause with text pause
                pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 300, 300, 100))
                text = font.render('Menu(M)', 1, BLACK)
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 300))
                # Make only text ro resume game under menu(M)
                text = font.render('Press P to resume game', 1, WHITE)
                text = pygame.transform.scale(text, (text.get_width()/3, text.get_height()/3))
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 410))


            if not pause:
                # Process
                allsprites.update()
                # boss_lasers.update()

                # Check if a covid hit the player
                if not player.invulnerable_buff:
                    player_hit = pygame.sprite.spritecollide(player, covids, False)
                    if player_hit:
                        player.life -= 10
                        # delete covid on the touch of player
                        for hit in player_hit:
                            hit.kill()
                
                # Check if a cure hit a covid
                cures_hits = pygame.sprite.groupcollide(covids, cures, True, True)
                for hit in cures_hits:
                    c = Covid()
                    allsprites.add(c)
                    covids.add(c)
                    player.score += 100

                # Create buffs with random chance
                if random.randint(1, 300) == 1:
                    buff_type = random.randint(1, 3)  # Randomly choose one of the three buff types
                    buff = Buff(buff_type)
                    allsprites.add(buff)
                    buffs.add(buff)

                if random.randint(1, 500) == 1:
                    buff_type = 4
                    buff = Buff(buff_type)
                    allsprites.add(buff)
                    buffs.add(buff)

                # Check if a buff hits the player and apply its effect
                buff_hits = pygame.sprite.spritecollide(player, buffs, True)
                for buff in buff_hits:
                    buff.apply_buff(player)

                if doctor == 2:
                    doctor = 0
                    level2 = False
                    boss2 = True

                # Output
                bg_in_game = pygame.image.load('./BG/BG_in_game.png')
                resize_bg_in_game = pygame.transform.scale(bg_in_game, (WIDTH, HEIGHT))
                screen.blit(resize_bg_in_game, (0, 0))
                # screen.fill((0, 0, 0))
                allsprites.draw(screen)

                # Draw amount of doctor and show buff4 in text beside doctor
                # pygame.draw.rect(screen, (255, 255, 255), (500, 20, 50, 80))
                img_buff4 = pygame.image.load("Buff/buff4.png")
                img_buff4 = pygame.transform.scale(img_buff4, (50, 50))
                screen.blit(img_buff4, (500, 20))
                textDoctor = font.render(str(doctor), True, BLACK)
                textDoctor = pygame.transform.scale(textDoctor, (textDoctor.get_width()/2, textDoctor.get_height()/2))
                screen.blit(textDoctor, (518, 60))

                pygame.draw.rect(screen, BLACK, (10, 50, player.life, 30))
                # Draw player's life in text beside life bar
                if player.life >= 100:
                    textLife = font.render("life player: " + str(player.life)[0] + str(player.life)[1], True, BLACK)
                else:
                    textLife = font.render("life player: " + str(player.life)[0], True, BLACK)
                # resize textLife
                textLife = pygame.transform.scale(textLife, (textLife.get_width()/4, textLife.get_height()/4))
                screen.blit(textLife, (10, 20))

                textScore = font.render("score " + str(player.score), True, BLACK)
                screen.blit(textScore, ((WIDTH-textScore.get_width())/2, 10))
            
            pygame.display.flip()

    if boss2:
        allsprites = pygame.sprite.Group()
        cures = pygame.sprite.Group()
        boss = Boss()
        boss_lasers = pygame.sprite.Group()
        boss.health = 250

        allsprites.add(player)
        allsprites.add(boss)
        print(doctor)

        while boss2:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    boss2 = False
                    GAME = False

                if event.type == pygame.KEYDOWN:
                    if not pause:
                        if event.key == pygame.K_LEFT:
                            player.speedx = -10
                        if event.key == pygame.K_RIGHT:
                            player.speedx = 10
                        if event.key == pygame.K_SPACE:
                            player.shoot()
                    if event.key == pygame.K_ESCAPE:
                        if pause:
                            pause = False
                        else:
                            pause = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.speedx = 0
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 0
            if pause:
                # Make to draw.rect show on screen when pause with text pause
                pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 300, 300, 100))
                text = font.render('Pause', 1, BLACK)
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 300))
                pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 450, 300, 100))
                text = font.render('Quit', 1, BLACK)
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 450))
                pygame.display.flip()
            
            if not pause:
                # Process
                allsprites.update()
                boss_lasers.update()

                # Check if player or boss is defeated
                laser_hits = pygame.sprite.spritecollide(player, boss_lasers, True)
                for hit in laser_hits:
                    player.life -= 10

                # Check if a cure hit a boss deleat boss health by 10 and delete boss when health is 0
                # set boss health -> 300 to make boss stronger
                boss_hits = pygame.sprite.spritecollide(boss, cures, True)
                for hit in boss_hits:
                    boss.health -= 10
                    if boss.health == 0:
                        boss.kill()
                        player.score += 1000
                        level3 = True
                        boss2 = False

                # Output
                bg_in_game = pygame.image.load('./BG/BG_in_game.png')
                resize_bg_in_game = pygame.transform.scale(bg_in_game, (WIDTH, HEIGHT))
                screen.blit(resize_bg_in_game, (0, 0))
                # screen.fill((0, 0, 0))
                allsprites.draw(screen)
                allsprites.draw(screen)

                pygame.draw.rect(screen, BLACK, (10, 50, player.life, 30))
                # Draw player's life in text beside life bar
                if player.life >= 100:
                    textLife = font.render("life player: " + str(player.life)[0] + str(player.life)[1], True, BLACK)
                else:
                    textLife = font.render("life player: " + str(player.life)[0], True, BLACK)
                # resize textLife
                textLife = pygame.transform.scale(textLife, (textLife.get_width()/4, textLife.get_height()/4))
                screen.blit(textLife, (10, 20))

                # Draw boss's life
                pygame.draw.rect(screen, WHITE, (10, 130, boss.health, 30))
                if boss.health >= 100:
                    textBossLife = font.render("life boss: " + str(boss.health)[0] + str(boss.health)[1], True, WHITE)
                else:
                    textBossLife = font.render("life boss: " + str(boss.health)[0], True, WHITE)
                # resize textBossLife
                textBossLife = pygame.transform.scale(textBossLife, (textBossLife.get_width()/4, textBossLife.get_height()/4))
                screen.blit(textBossLife, (10, 100))


                textScore = font.render("score " + str(player.score), True, BLACK)
                screen.blit(textScore, ((WIDTH-textScore.get_width())/2, 10))
                pygame.display.flip()

    if level3:
        allsprites = pygame.sprite.Group()
        covids = pygame.sprite.Group()
        cures = pygame.sprite.Group()
        buffs = pygame.sprite.Group()

        player = Player()
        allsprites.add(player)

        # Spawn a group of covids
        spawn_covid(20)

        while level3:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    level3 = False
                    GAME = False

                if event.type == pygame.KEYDOWN:
                    if not pause:
                        if event.key == pygame.K_LEFT:
                            player.speedx = -10
                        if event.key == pygame.K_RIGHT:
                            player.speedx = 10
                        if event.key == pygame.K_SPACE:
                            player.shoot()       
                    if event.key == pygame.K_p:
                        if pause:
                            pause = False
                        else:
                            pause = True
                    if event.key == pygame.K_m:
                        level1 = False
                        main = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.speedx = 0
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 0

            if pause:
                # Make to draw.rect show on screen when pause with text pause
                pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 300, 300, 100))
                text = font.render('Menu(M)', 1, BLACK)
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 300))
                # Make only text ro resume game under menu(M)
                text = font.render('Press P to resume game', 1, WHITE)
                text = pygame.transform.scale(text, (text.get_width()/3, text.get_height()/3))
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 410))


            if not pause:
                # Process
                allsprites.update()
                # boss_lasers.update()

                # Check if a covid hit the player
                if not player.invulnerable_buff:
                    player_hit = pygame.sprite.spritecollide(player, covids, False)
                    if player_hit:
                        player.life -= 10
                        # delete covid on the touch of player
                        for hit in player_hit:
                            hit.kill()
                
                # Check if a cure hit a covid
                cures_hits = pygame.sprite.groupcollide(covids, cures, True, True)
                for hit in cures_hits:
                    c = Covid()
                    allsprites.add(c)
                    covids.add(c)
                    player.score += 100

                # Create buffs with random chance
                if random.randint(1, 300) == 1:
                    buff_type = random.randint(1, 3)  # Randomly choose one of the three buff types
                    buff = Buff(buff_type)
                    allsprites.add(buff)
                    buffs.add(buff)

                if random.randint(1, 500) == 1:
                    buff_type = 4
                    buff = Buff(buff_type)
                    allsprites.add(buff)
                    buffs.add(buff)

                # Check if a buff hits the player and apply its effect
                buff_hits = pygame.sprite.spritecollide(player, buffs, True)
                for buff in buff_hits:
                    buff.apply_buff(player)

                if doctor == 2:
                    doctor = 0
                    level3 = False
                    boss3 = True

                # Output
                bg_in_game = pygame.image.load('./BG/BG_in_game.png')
                resize_bg_in_game = pygame.transform.scale(bg_in_game, (WIDTH, HEIGHT))
                screen.blit(resize_bg_in_game, (0, 0))
                # screen.fill((0, 0, 0))
                allsprites.draw(screen)

                # Draw amount of doctor and show buff4 in text beside doctor
                # pygame.draw.rect(screen, (255, 255, 255), (500, 20, 50, 80))
                img_buff4 = pygame.image.load("Buff/buff4.png")
                img_buff4 = pygame.transform.scale(img_buff4, (50, 50))
                screen.blit(img_buff4, (500, 20))
                textDoctor = font.render(str(doctor), True, BLACK)
                textDoctor = pygame.transform.scale(textDoctor, (textDoctor.get_width()/2, textDoctor.get_height()/2))
                screen.blit(textDoctor, (518, 60))

                pygame.draw.rect(screen, BLACK, (10, 50, player.life, 30))
                # Draw player's life in text beside life bar
                if player.life >= 100:
                    textLife = font.render("life player: " + str(player.life)[0] + str(player.life)[1], True, BLACK)
                else:
                    textLife = font.render("life player: " + str(player.life)[0], True, BLACK)
                # resize textLife
                textLife = pygame.transform.scale(textLife, (textLife.get_width()/4, textLife.get_height()/4))
                screen.blit(textLife, (10, 20))

                textScore = font.render("score " + str(player.score), True, BLACK)
                screen.blit(textScore, ((WIDTH-textScore.get_width())/2, 10))
            
            pygame.display.flip()

    if boss3:
        allsprites = pygame.sprite.Group()
        cures = pygame.sprite.Group()
        boss = Boss()
        boss_lasers = pygame.sprite.Group()
        boss.health = 300

        allsprites.add(player)
        allsprites.add(boss)
        print(doctor)

        while boss3:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    boss3 = False
                    GAME = False

                if event.type == pygame.KEYDOWN:
                    if not pause:
                        if event.key == pygame.K_LEFT:
                            player.speedx = -10
                        if event.key == pygame.K_RIGHT:
                            player.speedx = 10
                        if event.key == pygame.K_SPACE:
                            player.shoot()
                    if event.key == pygame.K_ESCAPE:
                        if pause:
                            pause = False
                        else:
                            pause = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.speedx = 0
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 0
            if pause:
                # Make to draw.rect show on screen when pause with text pause
                pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 300, 300, 100))
                text = font.render('Pause', 1, BLACK)
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 300))
                pygame.draw.rect(screen, WHITE, (WIDTH/2 - 150, 450, 300, 100))
                text = font.render('Quit', 1, BLACK)
                screen.blit(text, (WIDTH/2 - text.get_width()/2, 450))
                pygame.display.flip()
            
            if not pause:
                # Process
                allsprites.update()
                boss_lasers.update()

                # Check if player or boss is defeated
                laser_hits = pygame.sprite.spritecollide(player, boss_lasers, True)
                for hit in laser_hits:
                    player.life -= 10

                # Check if a cure hit a boss deleat boss health by 10 and delete boss when health is 0
                # set boss health -> 300 to make boss stronger
                boss_hits = pygame.sprite.spritecollide(boss, cures, True)
                for hit in boss_hits:
                    boss.health -= 10
                    if boss.health == 0:
                        boss.kill()
                        player.score += 1000
                        level3 = True
                        boss2 = False

                # Output
                bg_in_game = pygame.image.load('./BG/BG_in_game.png')
                resize_bg_in_game = pygame.transform.scale(bg_in_game, (WIDTH, HEIGHT))
                screen.blit(resize_bg_in_game, (0, 0))
                # screen.fill((0, 0, 0))
                allsprites.draw(screen)
                allsprites.draw(screen)

                pygame.draw.rect(screen, BLACK, (10, 50, player.life, 30))
                # Draw player's life in text beside life bar
                if player.life >= 100:
                    textLife = font.render("life player: " + str(player.life)[0] + str(player.life)[1], True, BLACK)
                else:
                    textLife = font.render("life player: " + str(player.life)[0], True, BLACK)
                # resize textLife
                textLife = pygame.transform.scale(textLife, (textLife.get_width()/4, textLife.get_height()/4))
                screen.blit(textLife, (10, 20))

                # Draw boss's life
                pygame.draw.rect(screen, WHITE, (10, 130, boss.health, 30))
                if boss.health >= 100:
                    textBossLife = font.render("life boss: " + str(boss.health)[0] + str(boss.health)[1], True, WHITE)
                else:
                    textBossLife = font.render("life boss: " + str(boss.health)[0], True, WHITE)
                # resize textBossLife
                textBossLife = pygame.transform.scale(textBossLife, (textBossLife.get_width()/4, textBossLife.get_height()/4))
                screen.blit(textBossLife, (10, 100))


                textScore = font.render("score " + str(player.score), True, BLACK)
                screen.blit(textScore, ((WIDTH-textScore.get_width())/2, 10))
                pygame.display.flip()

pygame.quit()