# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 17:54:52 2022

@author: manzo
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 13:10:50 2022

@author: manzo
"""

import pygame
import os
import random
import math
import sys

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND = pygame.image.load(os.path.join("CarAssets", "ParkStretto.png"))
CAR = pygame.image.load(os.path.join("CarAssets", "car88.png"))
CAR = pygame.transform.smoothscale(CAR, (90,45))

class Park:
    def __init__(self):
        self.parks = []
        
        self.obj_coord = (0,0)
        
        
        
    def fixed_gen(self):
        self.parks = [(1,1),(2,2) ,(3,1) ,(4,1) ,(5,0) ,(6,0) ,(7,0) ,(8,1) ,(9,1) ,(10,1) ]
    # def draw(self,i):
    #     #pygame.draw.circle(SCREEN, (0, 255, 110, 0), self.points[i], 3)
    #     if (i > 0):
    #         pygame.draw.line(SCREEN, (2, 105, 31, 255), (self.points[i-1][0], self.points[i-1][1]+TRACK_WIDTH), (self.points[i][0], self.points[i][1]+TRACK_WIDTH), 22)
    #         pygame.draw.line(SCREEN, (2, 105, 31, 255), (self.points[i-1][0], self.points[i-1][1]-TRACK_WIDTH), (self.points[i][0], self.points[i][1]-TRACK_WIDTH), 22)
    #     if (self.points[i][2] == 1):
    #         pygame.draw.line(SCREEN, (255, 0, 0, 255), (self.points[i][0], self.points[i][1] + TRAF_WIDTH ), (self.points[i][0], self.points[i][1] - TRAF_WIDTH ), 5)
    #     if (self.points[i][2] == 2):
    #         pygame.draw.line(SCREEN, (0, 255, 0, 255), (self.points[i][0], self.points[i][1] + TRAF_WIDTH ), (self.points[i][0], self.points[i][1] - TRAF_WIDTH ), 5)
    def random_gen(self):
       self.objective = random.randint(1,10)
       for i in range(1,11):
            if (i == self.objective):
                self.parks.append((i,2))
            else:
                occupied = random.randint(0,1)
                self.parks.append((i,occupied))
       print(self.parks) 
       
    def draw(self):
        SCREEN.blit(GROUND, (0, 0))
          
        if(self.parks[0][1] == 2):
            pygame.draw.circle(SCREEN, (110, 255, 110, 0), (330,165) ,5)    #1
            self.obj_coord = (330,165)
        if(self.parks[1][1] == 2):
            pygame.draw.circle(SCREEN, (110, 255, 110, 0), (330,225) ,5)
            self.obj_coord = (330,225)
        if(self.parks[2][1] == 2):
            pygame.draw.circle(SCREEN, (110, 255, 110, 0), (330,285) ,5)
            self.obj_coord = (330,285)
        if(self.parks[3][1] == 2):
            pygame.draw.circle(SCREEN, (110, 255, 110, 0), (330,350) ,5)
            self.obj_coord = (330,350)
        if(self.parks[4][1] == 2):
            pygame.draw.circle(SCREEN, (110, 255, 110, 0), (330,412) ,5)
            self.obj_coord = (330,412)
        
        if(self.parks[5][1] == 2):
            pygame.draw.circle(SCREEN, (110, 255, 110, 0), (770,165) ,5)
            self.obj_coord = (770,165)
        if(self.parks[6][1] == 2):
            pygame.draw.circle(SCREEN, (110, 255, 110, 0), (770,225) ,5)
            self.obj_coord = (770,225)
        if(self.parks[7][1] == 2):
            pygame.draw.circle(SCREEN, (110, 255, 110, 0), (770,285) ,5)
            self.obj_coord = (770,285)
        if(self.parks[8][1] == 2):
            pygame.draw.circle(SCREEN, (110, 255, 110, 0), (770,350) ,5)
            self.obj_coord = (770,350)
        if(self.parks[9][1] == 2):
            pygame.draw.circle(SCREEN, (110, 255, 110, 0), (770,412) ,5)    #10
            self.obj_coord = (770,412)
        
        
         

        
        if(self.parks[0][1] == 1):
            SCREEN.blit(CAR,  pygame.rect.Rect(285,140, 128, 128))      #1
        if(self.parks[1][1] == 1):
            SCREEN.blit(CAR,  pygame.rect.Rect(285,200, 128, 128))  
        if(self.parks[2][1] == 1):
            SCREEN.blit(CAR,  pygame.rect.Rect(285,260, 128, 128))  
        if(self.parks[3][1] == 1):
            SCREEN.blit(CAR,  pygame.rect.Rect(285,325, 128, 128))  
        if(self.parks[4][1] == 1):
            SCREEN.blit(CAR,  pygame.rect.Rect(285,387, 128, 128))  
        
        if(self.parks[5][1] == 1):
            SCREEN.blit(CAR,  pygame.rect.Rect(725,140, 128, 128))
        if(self.parks[6][1] == 1):
            SCREEN.blit(CAR,  pygame.rect.Rect(725,200, 128, 128))  
        if(self.parks[7][1] == 1):
            SCREEN.blit(CAR,  pygame.rect.Rect(725,260, 128, 128))
        if(self.parks[8][1] == 1):
            SCREEN.blit(CAR,  pygame.rect.Rect(725,325, 128, 128))  
        if(self.parks[9][1] == 1):
            SCREEN.blit(CAR,  pygame.rect.Rect(725,387, 128, 128))  
          
    
       # pygame.display.update()
        
        
# if __name__ == '__main__':
    
#     p = Park()
#     SCREEN.blit(GROUND, (0, 0))
#     SCREEN.blit(CAR,  pygame.rect.Rect(285,140, 128, 128))    
#     while True:
        
#         p.draw()
        
#         #pygame.display.update()
#         pygame.display.flip()
        
    
#     pygame.quit() 
      
    
    