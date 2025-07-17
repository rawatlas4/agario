import pygame
from socket import*
from random import randint
import threading
pygame.init()
client = socket(AF_INET,SOCK_STREAM)
client.connect(("localhost",2010))
win_width = 1200
win_height = 700
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
enemies = []
class Ball():
    def __init__(self,x,y,color,radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speed_x = 10
        self.speed_y = 10
        self.rect = pygame.Rect(self.x,self.y,self.radius*2,self.radius*2)
    def risovka(self):
        pygame.draw.circle(window,self.color,(self.rect.x,self.rect.y),self.radius)
    def reset2(self):
        pygame.draw.circle(window,self.color,(self.rect.x+self.radius,self.rect.y+self.radius),self.radius)
        font = pygame.font.Font(None,self.radius//2)
        kartinka_texta = font.render(None,1,(0,0,0))
        window.blit(kartinka_texta,(self.rect.x,self.rect.y))
pygame.time.delay(1)
prinyat_sms = client.recv(1024).decode()
prinyat_sms=prinyat_sms.split(",")
print(int(prinyat_sms[0]),int(prinyat_sms[1]),int(prinyat_sms[2]),int(prinyat_sms[3]))
my_id = int(prinyat_sms[0])
my_x = int(prinyat_sms[1])
my_y = int(prinyat_sms[2])
my_rad = int(prinyat_sms[3])
def obmen():
    global enemies
    while 1:
        try:
            enemies = []
            danni = client.recv(1024).decode()
            danni = danni.strip("|").split("|")
            for vasya in danni:
                danni2 = vasya.split(",")
                danni2 = list(map(int,danni2[:4]))
                enemies.append(danni2)
        except:
            pass
threading.Thread(target=obmen).start()
spisok = []
for _ in range(5000):
    eda = Ball(randint(-20000,20000),randint(-20000,20000),(randint(0,255),randint(0,255),randint(0,255)),randint(1,60))
    spisok.append(eda)


input_pole = pygame.Rect(0,0,300,100)




ball = Ball(600,350,(255,0,0),my_rad)
image_name_user = ""
enter_name = "ввід"
font = pygame.font.SysFont(None,ball.radius)
dla_nika = True
nik = ""
game = 1
while game:
    window.fill((255,255,255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = 0
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_BACKSPACE:
                nik = nik[0:-1]
            else:
                nik += e.unicode
            if e.key == pygame.K_RETURN:
                finish = False
                enter_name = "не ввід"
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        for eda in spisok:
            eda.rect.x +=5
        my_x -=5
    if keys[pygame.K_RIGHT]:
        for eda in spisok:
            eda.rect.x +=-5
        my_x +=5
    if keys[pygame.K_DOWN]:
        for eda in spisok:
            eda.rect.y +=-5
        my_y +=5
    if keys[pygame.K_UP]:
        for eda in spisok:
            eda.rect.y +=5
        my_y -=5
    ball.reset2()
    for i in spisok:
        i.risovka()
    for vasya in enemies:
        sdvigx = int((vasya[1] - my_x) + win_width//2)
        sdvigy = int((vasya[2] - my_y) + win_height//2)
        enemy = Ball(sdvigx,sdvigy,(0,0,0),vasya[3])
        enemy.reset2()

    if image_name_user != "":
        window.blit(image_name_user,(win_width/2,win_height/2))
    if enter_name == "ввід":
        pygame.draw.rect(window,(0,0,0),input_pole,4)
        image_name_user = font.render(nik,True,(0,0,0))
        window.blit(image_name_user,input_pole )
        input_pole.w = image_name_user.get_width()+10
    try:

        client.send(f"{my_id},{my_x},{my_y},{my_rad}".encode())
    except:
        pygame.quit()



    pygame.display.update()
    clock.tick(60)