from os import stat
from time import sleep
# from turtle import update
# from turtle import speed
from cv2 import imshow
import pygame
import sys
import cv2
def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
def slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)
def cos(x1, y1, x2, y2):
    return (x2-x1)/distance(x1, y1, x2, y2)
def sin(x1, y1, x2, y2):
    return (y2-y1)/distance(x1, y1, x2, y2)
def magnitiude(speed):
    return (speed[0] ** 2 + speed[1] ** 2) ** 0.5

class player():
    def __init__(self, x, y, speed, radius,type, team):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.team = team
        self.type = type

    def follow_ball(self,ball_cords):
        self.x += cos(self.x, self.y, ball_cords[0], ball_cords[1]) * self.speed
        self.y += sin(self.x, self.y, ball_cords[0], ball_cords[1]) *  self.speed
    

class Ball():
    def __init__(self,path):
        self.cords= [100.0,100.0]
        
        self.velo = [0,1]
        self.radius = 10
        self.color = (255, 255, 255)
        self.ball = pygame.image.load(path)
        self.ball = pygame.transform.scale(self.ball, (self.radius * 2, self.radius * 2))
        self.ball_rect = self.ball.get_rect()
        self.velo_mag=magnitiude(self.velo)
    def update(self):
        self.ball_rect.center = self.cords

    def move(self):
        self.cords[0] += self.velo[0]
        self.cords[1]+= self.velo[1]
        # increment velo 
        self.velo=[self.velo[0]+0.1,self.velo[1]+0.1] 
        self.update()
        


class Pygame_window:
    def __init__(self):
        pygame.init()
        self.bg_path="assets/images/background/bg.jpg"
        self.size = cv2_window.give_size(self.bg_path)
        self.width, self.height = self.size
        self.screen = pygame.display.set_mode(self.size)
        self.ball_obj=Ball("assets/ball/intro_ball.gif")
        self.bg = pygame.image.load(self.bg_path)
        self.team_size = 1
        self.players_1 = []
        self.players_1.append(player(500, 100, 5, 10, "goalkeeper", 1))

        # self.main_loop()

    def go_mouse(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                    x2, y2 = event.pos
                    x1, y1 = self.ball_obj.ball_rect.center
                    self.ball_obj.velo = [self.ball_obj.velo_mag*cos(x1,y1,x2,y2),self.ball_obj.velo_mag*sin(x1,y1,x2,y2) ]
                    print(self.ball_obj.velo)
    def reflect(self):
        if self.ball_obj.ball_rect.left < 0 or self.ball_obj.ball_rect.right > self.width:
                self.ball_obj.velo[0] = -self.ball_obj.velo[0]
        if self.ball_obj.ball_rect.top < 0 or self.ball_obj.ball_rect.bottom > self.height:
            self.ball_obj.velo[1] = -self.ball_obj.velo[1]
    


    def main_loop(self):
        while 1:
            self.screen.blit(self.bg, (0, 0))

            for event in pygame.event.get():
                self.go_mouse(event)
                if event.type == pygame.QUIT: sys.exit()

            self.ball_obj.move()
            self.reflect()


            for player in self.players_1:
                player.follow_ball(self.ball_obj.ball_rect.center)
                pygame.draw.circle(self.screen, (255, 255, 255),(int(player.x), int(player.y)), player.radius)


            self.screen.blit(self.ball_obj.ball, self.ball_obj.ball_rect)
            pygame.display.flip()
            sleep(0.02)
            

class cv2_window:
    def __init__(self, size, bg):
        self.size = size
        self.width, self.height = self.size
        self.bg = cv2.imread(bg)

        # self.main_loop()

    def main_loop(self):
        while 1:
            cv2.imshow("bg", self.bg)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    @staticmethod
    def show(img):
        while 1:
            cv2.imshow("img", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    @staticmethod
    def resize(path, ratio):
        img = cv2.imread(path)
        return cv2.resize(img, (int(img.shape[1] * ratio), int(img.shape[0] * ratio)))
    @staticmethod
    def give_size(path="",img=None):
        if img is None:
            img = cv2.imread(path)
        return (img.shape[1], img.shape[0])
 



