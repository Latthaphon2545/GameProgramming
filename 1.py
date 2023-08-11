import sys, pygame
pygame.init()

size = width, height = 1000, 500
speed = [2, 2]
bg_color = 255, 179, 179

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Show FPS")
ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()
clock = pygame.time.Clock()
font = pygame.font.SysFont("robotto", 24)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    textFps = font.render("FPS: "+str(int(clock.get_fps())), True, pygame.Color("red"))
    
    screen.fill(bg_color)
    screen.blit(textFps,(20,20))
    screen.blit(ball, ballrect)
    pygame.display.flip()