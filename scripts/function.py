from operator import index
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



global player_coords
player_coords = {}
global index_player
index_player = 0

class player():

    def __init__(self, x, y, speed, radius,type, team):
        global player_coords
        global index_player
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.team = team
        self.type = type
        self.index = index_player
        player_coords[index_player] = [x, y]


        index_player += 1
        


    def follow_ball(self,ball_cords):
        self.x += cos(self.x, self.y, ball_cords[0], ball_cords[1]) * self.speed
        self.y += sin(self.x, self.y, ball_cords[0], ball_cords[1]) *  self.speed

    # if player touch the ball
    def touch_ball(self,ball_cords):
        if distance(self.x, self.y, ball_cords[0], ball_cords[1]) <= self.radius:
            return True
        else:
            return False
    def closest_player(self):
        closest = None
        for i in player_coords:
            if i != self.index:
                if closest == None:
                    closest = i
                else:
                    if distance(self.x, self.y, player_coords[i][0], player_coords[i][1]) < distance(self.x, self.y, player_coords[closest][0], player_coords[closest][1]):
                        closest = i
        return closest

    def pass_ball(self,ball):
        closest_player = self.closest_player()
        velo_pass=10
        ball.velo = [ball.velo_mag*cos(ball.cords[0],ball.cords[1],player_coords[closest_player][0],player_coords[closest_player][1]),ball.velo_mag*sin(ball.cords[0],ball.cords[1],player_coords[closest_player][0],player_coords[closest_player][1])]
        print(ball.velo)
        ball.moving = True
        
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
        self.moving=True
    def update(self):
        self.ball_rect.center = self.cords

    def move(self):
        self.cords[0] += self.velo[0]
        self.cords[1]+= self.velo[1]
        # increment velo 
        # self.velo=[self.velo[0],self.velo[1]] 
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
        self.players_1.append(player(700, 200, 4, 10, "goalkeeper", 1))
        self.players_1.append(player(500, 700, 6, 10, "goalkeeper", 1))
        # self.players_1.append(player(300, 500, 4, 10, "goalkeeper", 1))
        # self.players_1.append(player(10, 300, 4, 10, "goalkeeper", 1))
        

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
        index=0
        while 1:
            # print("worlk")
            self.screen.blit(self.bg, (0, 0))

            for event in pygame.event.get():
                self.go_mouse(event)
                if event.type == pygame.QUIT: sys.exit()
                # if space pressed pass ball
                if event.type == pygame.KEYDOWN:
                    if self.ball_obj.moving==False:
                        if event.key == pygame.K_SPACE:
                            self.players_1[index].pass_ball(self.ball_obj)

            
            self.reflect()
            if self.ball_obj.moving==False:
                for player in self.players_1:
                    pygame.draw.circle(self.screen, (255, 255, 255),(int(player.x), int(player.y)), player.radius)

                    self.players_1[index].follow_ball([50,50])


            if self.ball_obj.moving==True:
                for player in self.players_1:
                    pygame.draw.circle(self.screen, (255, 255, 255),(int(player.x), int(player.y)), player.radius)
                    if(player.touch_ball(self.ball_obj.ball_rect.center)):
                        if player.index!=index:
                            print("touch")
                            self.ball_obj.ball_rect.center=[player.x,player.y]
                            self.ball_obj.velo=[0,0]
                            player.follow_ball((164,300))
                            index=player.index
                            print(index)
                            self.ball_obj.moving=False
                        else:
                            print("same player")
                            player.follow_ball(self.ball_obj.ball_rect.center)
                        # self.ball_obj.velo_mag=magnitiude(self.ball_obj.velo)
                        # print(self.ball_obj.velo)
                    else:
                        # self.ball_obj.moving=True
                        player.follow_ball(self.ball_obj.ball_rect.center)
            pygame.draw.circle(self.screen, (255, 0, 0), (164,300), self.ball_obj.radius)
            if self.ball_obj.moving:
                self.ball_obj.move()



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
 



