from multiprocessing.connection import wait
from os import stat
from time import sleep
# from turtle import speed
from cv2 import imshow
import pygame
import sys
import cv2
def slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)
def cos(x1, y1, x2, y2):
    return 1-slope(x1, y1, x2, y2)**2 / (1 + slope(x1, y1, x2, y2) ** 2)
def sin(x1, y1, x2, y2):
    return 2*slope(x1, y1, x2, y2) / (1 + slope(x1, y1, x2, y2) ** 2)
def magnitiude(speed):
    return (speed[0] ** 2 + speed[1] ** 2) ** 0.5
class Ball():
    def __init__(self,path):
        self.x = 100
        self.y = 100
        self.radius = 10
        self.color = (255, 255, 255)
        self.ball = pygame.image.load(path)
        self.ball = pygame.transform.scale(self.ball, (self.radius * 2, self.radius * 2))


class Pygame_window:
    def __init__(self, bg):
        pygame.init()
        self.size = cv2_window.give_size(bg)
        self.width, self.height = self.size
        self.screen = pygame.display.set_mode(self.size)
        self.ball_obj=Ball("assets/ball/intro_ball.gif")
        self.bg = pygame.image.load(bg)
        self.ballrect = self.ball_obj.ball.get_rect()
        self.speed = [0, 10]

        # self.main_loop()

    def main_loop(self):
        while 1:
            self.screen.blit(self.bg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    x, y = event.pos
                    print(x, y)
                    print("pos", self.ballrect.center)
                    x1, y1 = self.ballrect.center
                    # slope_value = slope(x1, y1, x, y)
                    # print values of cos and sin
                    print(cos(x1, y1, x, y), sin(x1, y1, x, y))

                    self.speed = [magnitiude(self.speed)*cos(x1,y1,x,y), magnitiude(self.speed)*sin(x1,y1,x,y)]
                    print(self.speed)
                

                if event.type == pygame.QUIT: sys.exit()


            self.ballrect = self.ballrect.move(self.speed)

            if self.ballrect.left < 0 or self.ballrect.right > self.width:

                self.speed[0] = -self.speed[0]

            if self.ballrect.top < 0 or self.ballrect.bottom > self.height:

                self.speed[1] = -self.speed[1]


            # screen.fill(black)

            self.screen.blit(self.ball_obj.ball, self.ballrect)

            pygame.display.flip()
            sleep(0.02)

            # end if pressed esc
            

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
 



