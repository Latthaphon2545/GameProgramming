import pygame, random, sys
from pygame.locals import *

xp = [240, 240, 240, 240, 240, 240]
yp = [100, 80, 60, 40, 20, 0]
wi_screen,hi_screen = 1000,500
wi_1, hi_1 = wi_screen - 50, hi_screen - 50
wi_rat, hi_rat = 50, 50

def crash(screen, score, wi, hi):
    fnt = pygame.font.SysFont('Impact', 40)
    text = fnt.render('Your score : ' + str(score), True, (255, 255, 255))
    text_width, text_height = text.get_size()
    center_x = (wi - text_width) // 2
    center_y = (hi - text_height) // 2
    screen.blit(text, (center_x, center_y))
    pygame.display.update()

    # Display game over text
    game_over_text = fnt.render('Game Over', True, (255, 0, 0))
    game_over_x = (wi - game_over_text.get_width()) // 2
    game_over_y = center_y - text_height  # Position above the score text
    screen.blit(game_over_text, (game_over_x, game_over_y))

    # Display options text
    options_text = fnt.render('Press Q to Quit or P to Play Again', True, (255, 255, 255))
    options_x = (wi - options_text.get_width()) // 2
    options_y = center_y + text_height  # Position below the score text
    screen.blit(options_text, (options_x, options_y))

    pygame.display.update()

    while True:
        play_again()
				

def iscollide(x1, x2, y1, y2, w1, w2, h1, h2):
	if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2: # means collision > x1+w1>x2 is the condition for collision
		return True
	else:
		return False
	
def willcollide(x1, y1):
	i = len(xp) - 1
	while i >= 1:
		if iscollide(x1, xp[i], y1, yp[i], 20, 20, 20, 20): 
			return True
		i -= 1
	if x1 < 0 or x1 > wi_1 or y1 < 0 or y1 > hi_1: return True
	return False
	

def play():

	dir = 0
	score = 0
	
	dotpos = (random.randint(0, wi_1), random.randint(0, hi_1))
	pygame.init()
	pygame.display.set_caption('DME')

	scrn=pygame.display.set_mode((wi_screen, hi_screen))

	bodyimg = pygame.Surface((20, 20))
	bodyimg.fill((153, 255, 51))
	rat = pygame.image.load("rat.png")
	rat = pygame.transform.scale(rat, (wi_rat, hi_rat))

	eat_sound = pygame.mixer.Sound("eat.mp3")

	fnt = pygame.font.SysFont('Impact', 40)
	clock = pygame.time.Clock()
	while True:
		# sneck_sound.play()
		clock.tick(10)
		for e in pygame.event.get():
			if e.type == QUIT:
				sys.exit(0)
			elif e.type == KEYDOWN:
				if e.key == K_UP or e.key == pygame.K_w and dir != 0:
					dir = 2
				elif e.key == K_DOWN or e.key == pygame.K_s and dir != 2:
					dir = 0
				elif e.key == K_LEFT or e.key == pygame.K_a and dir != 1:
					dir = 3
				elif e.key == K_RIGHT or e.key == pygame.K_d and dir != 3:
					dir = 1

		# Start AI to control the snake 
		# 2 -> up    0 -> down
		# 3 -> left  1 -> right

		# 1. find out the four distances
		dist = (dotpos[0] - xp[0], dotpos[1] - yp[0])
		# 2. find out the direction
		if dist[0] < 0 and dir != 1 and not willcollide(xp[0] - 20, yp[0]):
			dir = 3 # 3 -> left
		elif dist[0] >= 0 and dir != 3 and not willcollide(xp[0] + 20, yp[0]):
			dir = 1 # 1 -> right
		elif dist[1] < 0 and dir != 0 and not willcollide(xp[0], yp[0] - 20):
			dir = 2 # 2 -> up
		elif dist[1] >= 0 and dir != 2 and not willcollide(xp[0], yp[0] + 20):
			dir = 0 # 0 -> down
	
		i = len(xp) - 1
		while i >= 2:
			if iscollide(xp[0], xp[i], yp[0], yp[i], 20, 20, 20, 20): 
				crash(scrn, score, wi_screen, hi_screen)
			i -= 1

		if iscollide(xp[0], dotpos[0], yp[0], dotpos[1], 20, wi_rat, 20, hi_rat):
			score += 1
			xp.append(700)
			yp.append(700)
			dotpos=(random.randint(0, wi_1), random.randint(0, hi_1))
			eat_sound.play()

		if xp[0] < 0 or xp[0] > wi_1 or yp[0] < 0 or yp[0] > hi_1: 
			crash(scrn, score, wi_screen, hi_screen)

		i = len(xp) - 1
		while i >= 1:
			xp[i] = xp[i - 1]
			yp[i] = yp[i - 1]
			i -= 1

		if dir==0:
			yp[0] += 20
		elif dir==1:
			xp[0] += 20
		elif dir==2:
			yp[0] -= 20
		elif dir==3:
			xp[0] -= 20

		scrn.fill((0, 0, 0))
		# background_img = pygame.image.load("bg.png")
		# background_img = pygame.transform.scale(background_img, (wi_screen, hi_screen))
		# scrn.blit(background_img, (0, 0))

		for i in range(0, len(xp)):
			scrn.blit(bodyimg, (xp[i], yp[i]))

			
			
		scrn.blit(rat, dotpos)
		t = fnt.render(str(score), True, (255, 255, 255))
		scrn.blit(t, (10, 10))
		rat_x = 10 + t.get_width() + 5  # Adjust the x-coordinate to position it after the text
		rat_y = 10  # Use the same y-coordinate as the text
		scrn.blit(rat, (rat_x, rat_y))
		pygame.draw.rect(scrn,(255,255,153),(0,0,wi_screen,hi_screen),5)
		pygame.display.update()

def play_again():
	clock = pygame.time.Clock()
	while True:
		clock.tick(10)
		for e in pygame.event.get():
			if e.type == QUIT:
				sys.exit(0)
			elif e.type == KEYDOWN:
				if e.key == pygame.K_p:
					play()
				elif e.key == pygame.K_q:
					sys.exit(0)
					

if __name__ == '__main__':
	play()