import pygame, time, keyboard, socket

pygame.init()
wn = pygame.display.set_mode((800, 800))
pygame.display.set_caption('RobotRTS')
clock = pygame.time.Clock()
lentities = {}

jews = [0,0]

text = []
surface = pygame.Surface((200, 200))
surface.fill('white')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                text += 'w'
            if event.key == pygame.K_a:
                text += 'a'
            if event.key == pygame.K_s:
                text += 's'
            if event.key == pygame.K_d:
                text += 'd'
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                text.remove('w')
            if event.key == pygame.K_a:
                text.remove('a')
            if event.key == pygame.K_s:
                text.remove('s')
            if event.key == pygame.K_d:
                text.remove('d')

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

    for hitler in text:
        if hitler == 'w':
            jews[1] -= 5
        if hitler == 'a':
            jews[0] -= 5
        if hitler == 's':
            jews[1] += 5
        if hitler == 'd':
            jews[0] += 5
    wn.blit(surface, (200+jews[0], 200+jews[1]))
    pygame.display.update()
    clock.tick(60)
    print(clock.get_fps())

    wn.fill('black')
