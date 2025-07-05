import pygame, time, keyboard, socket, random

with open('Assets/MEM/Settings.txt') as g:
    f = g.read().split('\n')
    pygame.init()
    f[0] = f[0].split('x')
    size = []
    for i in range(len(f[0])):
        size.append(int(f[0][i]))

    if f[0] == 'FULL':
        wn = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
        full = True
    else:
        wn = pygame.display.set_mode(tuple(size), pygame.RESIZABLE)
        full = False
    pygame.display.set_caption('RiseOfRitler')
    clock = pygame.time.Clock()
    lentities = {}

    g.close()

class Sprite:
    def __init__(self, x, y, heading, team):
        self.x = x
        self.y = y
        self.heading = heading
        self.team = team
        

jews = [0,0]
bots = []
for i in range(5):
    bots.append(Sprite(random.randint(0,500), random.randint(0,500), 0, 'self'))

text = []
surface = pygame.Surface((20, 20))
surface.fill('white')

cols = []
ke = False
full = False
FPS = 60
L = 300/FPS

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            x, y = wn.get_size()
            with open('Assets/MEM/Settings.txt', 'r') as f:
                g = f.read().split('\n')
                f.close()
            with open('Assets/MEM/Settings.txt', 'w') as f:
                if full:
                    g[0] = 'FULL'
                else:
                    g[0] = f'{x}x{y}'
                f.write('\n'.join(g))
                f.close()
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
            if event.key == pygame.K_F11:
                if full:
                    wn = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
                    full = False
                else:
                    wn = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
                    full = True
            if event.key == pygame.K_LSHIFT:
                ke = True
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                text.remove('w')
            if event.key == pygame.K_a:
                text.remove('a')
            if event.key == pygame.K_s:
                text.remove('s')
            if event.key == pygame.K_d:
                text.remove('d')
            if event.key == pygame.K_LSHIFT:
                ke = False


        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            thing = False
            bot_clicked = []
            for bot in bots:
                if bot.x > pos[0] - 10 + jews[0]:
                    if bot.x < pos[0] + 10 + jews[0]:
                        if bot.y > pos[1] - 10 + jews[1]:
                            if bot.y < pos[1] + 10 + jews[1]:
                                cols.append(bot)
                                bot_clicked.append(bot)
                                thing = True
            if cols != [] and not ke:
                for col in cols:
                    if col not in bot_clicked:
                        col.x = pos[0]
                        col.y = pos[1]
                
            if not ke and not thing:
                print('EXE')
                cols = []
                
            bot_clicked = []

    for hitler in text:
        if hitler == 'w':
            jews[1] -= L
        if hitler == 'a':
            jews[0] -= L
        if hitler == 's':
            jews[1] += L
        if hitler == 'd':
            jews[0] += L
            
    for bot in bots:
        wn.blit(surface, (bot.x+jews[0]-10, bot.y+jews[1]-10))
    pygame.display.update()
    clock.tick(FPS)

    wn.fill('black')
