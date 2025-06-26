import socket
import threading, random, time

HEADER = 64
PORT = 5056
SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '0.0.0.0'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT!'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

pwc = {}
class Sprite:
    def __init__(self, x, y, name='Dummy', size=(20,20), heading=90, team='s', give_energy=50, types='Dummy'): # team: s=self, f=friendly, e=enemy, n=neatral
        self.x = x
        self.y = y
        self.heading = heading
        self.size = size
        self.name = name
        self.energy = 100
        self.team = team
        self.give_energy = give_energy
        self.type = types
        
all_entities = []
all_entities.append(Sprite(0,0))

def find_key(tar):
    d = {'a': 1, 'b': 2, 'c': 2}
    tar = tar
    keys = [key for key, val in d.items() if val == tar]
    return keys

def handle_client(conn, addr, conn_num):
    print(f'[NEW CONNECTION] {addr} conneced')
    connected = True
    pwc[conn_num] = {'xy': [random.randint(-50, 50), random.randint(-50, 50)]}
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            timr = time.time()
            msg = conn.recv(msg_length).decode(FORMAT)
            print(time.time() - timr)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            msg = list(msg)
            for ms in msg:
                if ms == 'w':
                    pwc[conn_num]['xy'][1] += 5
                if ms == 'a':
                    pwc[conn_num]['xy'][0] += 5
                if ms == 's':
                    pwc[conn_num]['xy'][1] -= 5
                if ms == 'd':
                    pwc[conn_num]['xy'][0] -= 5
            text = ''
            text += str(50-pwc[conn_num]['xy'][0]) + '.' + str(50 - pwc[conn_num]['xy'][1]) + ',green,200.200\t'
            text += str(200-pwc[conn_num]['xy'][0]) + '.' + str(200 - pwc[conn_num]['xy'][1]) + ',red,200.200'
            conn.send(text.encode(FORMAT))
            
    conn.close()
    print(f'Connection {addr} terminated.')
    print('\n[ACTIVE CONNECTIONS] ' + str(threading.active_count() - 2))

def start():
    server.listen()
    print('[LISTENING] Server is listening on ' + SERVER)
    i = 0
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, (i)))
        thread.start()
        print('\n[ACTIVE CONNECTIONS] ' + str(threading.active_count() - 1))
        i += 1

print('[STARTING] Server is starting...')
start()
