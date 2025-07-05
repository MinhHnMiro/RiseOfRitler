import pygame, time, keyboard, socket, random
from math import sqrt

with open('Assets/MEM/Settings.txt') as g:
    f = g.read().split('\n')
    pygame.init()
    f[0] = f[0].split('x')
    size = []
    for i in range(len(f[0])):
        size.append(int(f[0][i]))

    if f[1] == 'True':
        wn = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
        full = True
    else:
        wn = pygame.display.set_mode(tuple(size), pygame.RESIZABLE)
        full = False
    pygame.display.set_caption('RiseOfRitler')
    clock = pygame.time.Clock()
    lentities = {}

    g.close()

def check_collision(first, second):
    if first[0] > second[0] - 10:
        if first[0] < second[0] + 10:
            if first[1] > second[1] - 10:
                if first[1] < second[1] + 10:
                    return True
    return False

def normalize(vector):
    pytha = sqrt(vector[0]**2 + vector[1]**2)
    x = vector[0] / pytha
    y = vector[1] / pytha
    return [x, y]

class Sprite:
    def __init__(self, x, y, heading, team):
        self.x = x
        self.y = y
        self.heading = heading
        self.team = team # s=self, e=enemy, u=unattackable
        self.target_type = 's' # s=space, r=robot
        self.surface = pygame.Surface((20, 20))
        self.surface.fill('white')
        self.target = None
        self.dx, self.dy = [0,0]
        self.speed = 2

    def update_target(self):
        x = self.target[0] - self.x
        y = self.target[1] - self.y
        co = [x, y]
        nor = []
        for i in range(2):
            if co[i] < 0:
                nor.append(co[i]*-1)
            else:
                nor.append(co[i])
        num = max(nor)
        pr = normalize([x*num, y*num])
        for i in range(2):
            pr[i] *= self.speed
        self.dx, self.dy = pr

    def pos(self):
        return [self.x, self.y]
    
    def update(self):
        if self.target != None:
            if self.target_type == 's':
                if 5 > self.x - self.target[0] > -5 and 5 > self.y - self.target[1] > -5:
                    self.target = None
            if self.target_type == 'r':
                x = self.target.pos()[0] - self.x
                y = self.target.pos()[1] - self.y
                co = [x, y]
                nor = []
                for i in range(2):
                    if co[i] < 0:
                        nor.append(co[i]*-1)
                    else:
                        nor.append(co[i])
                num = max(nor)
                pr = normalize([x*num, y*num])
                for i in range(2):
                    pr[i] *= self.speed
                self.dx, self.dy = pr
                if 5 > self.x - self.target.pos()[0] > -5 and 5 > self.y - self.target.pos()[1] > -5:
                    self.target = None
                
            self.x += self.dx
            self.y += self.dy

        else:
            self.dx = 0
            self.dy = 0


class Daniel(Sprite):
    def __init__(self, x, y, heading, team):
        Sprite.__init__(self, x, y, heading, team)
        self.speed = 3
        self.surface.fill('orange')
        
jews = [0,0]
bots = []
for i in range(2):
    bots.append(Daniel(random.randint(0,500), random.randint(0,500), 0, 's'))
for i in range(3):
    bots.append(Sprite(random.randint(0,500), random.randint(0,500), 0, 'me'))

text = []

cols = []
ke = False
full = False
FPS = int(f[3])
L = round(300/FPS)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            x, y = wn.get_size()
            with open('Assets/MEM/Settings.txt', 'r') as f:
                g = f.read().split('\n')
                f.close()
            with open('Assets/MEM/Settings.txt', 'w') as f:
                if full:
                    g[1] = 'True'
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
                    with open('Assets/MEM/Settings.txt', 'r') as f:
                        g = f.read().split('\n')
                        f.close()
                        size = []
                        g[0] = g[0].split('x')
                        for i in range(len(g[0])):
                            size.append(int(g[0][i]))
                    with open('Assets/MEM/Settings.txt', 'w') as f:
                        g[1] = 'False'
                        x, y = wn.get_size()
                        g[0] = f'{x}x{y}'
                        f.write('\n'.join(g))
                        f.close()
                    wn = pygame.display.set_mode(tuple(size), pygame.RESIZABLE)
                    full = False
                else:
                    with open('Assets/MEM/Settings.txt', 'r') as f:
                        g = f.read().split('\n')
                        f.close()
                    with open('Assets/MEM/Settings.txt', 'w') as f:
                        g[1] = 'True'
                        x, y = wn.get_size()
                        g[0] = f'{x}x{y}'
                        f.write('\n'.join(g))
                        f.close()
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
            num = []
            for i in range(2):
                num.append(pos[i] - jews[i])
            for bot in bots:
                if check_collision(bot.pos(), num):
                    if bot.team == 'e' or bot.team == 'me' and bool(len(cols)):
                        for col in cols:
                            col.target = bot
                            col.target_type = 'r'
                            print('Target')
                        cols = []
                            
                    else:
                        cols.append(bot)
                        bot_clicked.append(bot)
                        thing = True
                        print('Sel')
                    
            if cols != [] and not ke:
                for col in cols:
                    if col not in bot_clicked:
                        if col.team == 's' or 'me':
                            col.target = [pos[0]-jews[0], pos[1]-jews[1]]
                            col.update_target()
                        elif col.team == 'e':
                            pass
                
            if not ke and not thing:
                cols = []
                
            bot_clicked = []

    for hitler in text:
        if hitler == 'w':
            jews[1] += L
        if hitler == 'a':
            jews[0] += L
        if hitler == 's':
            jews[1] -= L
        if hitler == 'd':
            jews[0] -= L
            
    for bot in bots:
        bot.update()
        wn.blit(bot.surface, (bot.x+jews[0]-10, bot.y+jews[1]-10))
    pygame.display.update()
    clock.tick(FPS)
    #print(clock.get_fps())

    wn.fill('black')
