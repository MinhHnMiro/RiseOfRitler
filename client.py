import pygame, time, keyboard, socket

pygame.init()
wn = pygame.display.set_mode((800, 800))
pygame.display.set_caption('RobotRTS')
clock = pygame.time.Clock()

HEADER = 64
PORT = 5056
#PORT = 32383
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT!'
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = '29.ip.gl.ply.gg'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    timr = time.time()
    text = client.recv(HEADER).decode(FORMAT)
    print(time.time() - timr)
    return text

lentities = {}

text = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            send(DISCONNECT_MESSAGE)
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

    msg = send(''.join(text))
    msg = msg.split('\t')
    ms = []
    for concaine in msg:
        ms.append(concaine.split(','))

    for i in range(len(ms)):
        ms[i][2] = ms[i][2].split('.')
        ms[i][0] = ms[i][0].split('.')
    for i in range(len(ms)):
        for j in range(2):
            ms[i][0][j] = int(ms[i][0][j])
            ms[i][2][j] = int(ms[i][2][j])

    for i in range(len(ms)):
        surface = pygame.Surface(tuple(ms[i][2]))
        surface.fill(ms[i][1])
        wn.blit(surface, tuple(ms[i][0]))

    pygame.display.update()
    clock.tick(60)
    #print(clock.get_fps())

    wn.fill('black')
