# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 16:03:59 2022

@author: manzo
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 12:12:56 2022

@author: manzo
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 12:54:18 2022

@author: manzo
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 12:31:15 2021

@author: manzo
"""

import pygame
import os
import random
import math
import sys
import neat
import numpy as np
import sympy as sy
import sympy.geometry as gm
import parking as parking


pygame.init()

RED = (200,0,0)
FUCSIA = (255,0,255)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CAR = pygame.image.load(os.path.join("CarAssets", "carf.png"))




TRACK = pygame.image.load(os.path.join("CarAssets", "track2.png"))


air_density = 1.225
friction_coef = 1.7
drag_coef = 0.7
lift_coef = -2.0
g = 9.8

MAX_FRONT_ACC = 0.5
DRAG_SCALING = 0.1
MAX_VELOCITY = 6

ROTATION_VEL = 2

class Car(pygame.sprite.Sprite):
    def __init__(self, img=CAR):
        super().__init__()
        self.image_ori = img
        # self.image_ori.set_colorkey(WHITE)
        # self.image_ori(WHITE).convert_apha()
        
        self.w_ori = img.get_width()
        self.h_ori = img.get_height()
        
        self.image = img
        
        
        self.front_acc_time = 0

        self.x = 150
        self.y = 650
        self.x_velocity = 0
        self.y_velocity = 0
        self.x_accelleration = 0
        self.y_accelleration = 0
        self.body_orientation = 0
        self.wheels_orientation = 0
        self.mass = 700
        
        self.pedal_time = 0
        
        self.front_area = 1.5
        
        self.rect = self.image.get_rect(center=(self.x, self.y)) #da ytube
        
       # self.rect = pygame.Rect(self.x, self.y, img.get_width(), img.get_height())
        
        self.left_sensor = [0,0]
        self.right_sensor = [0,0]
        self.leftb_sensor = [0,0]
        self.rightb_sensor = [0,0]
        
        self.radars = []
        
        self.crashed = False
        
        self.command = [0,0,0,0]
        self.previous_pos = [0,0]
        self.still = 0
        
        self.finish_line = False
        self.NOTMOV = False
        self.FRONTMOV = False
        self.BCKMOV = False
     
    def move(self):
        
        self.x_velocity += self.x_accelleration/30 #diviso 30 perchè per ogni frame
        self.y_velocity += self.y_accelleration/30
        if (self.x_velocity > 30):
            self.x_velocity = 30
        if (self.y_velocity > 30):
            self.y_velocity = 30
        
        # self.rect.x += self.x_velocity 
        # self.rect.y -= self.y_velocity
        self.x += self.x_velocity 
        self.y -= self.y_velocity
        self.rect.x = math.floor(self.x)
        self.rect.y = math.floor(self.y)
        
        #print(self.y, type(self.y_velocity))
    # def shift(self):
    #     self.rect.x -= 800
        
   
        
     
    
    def input_analisys(self):
        self.previous_pos[0] = self.left_sensor[0]
        self.previous_pos[1] = self.left_sensor[1]
        if self.x_velocity == 0 and self.y_velocity == 0:
            self.NOTMOV = True
            self.FRONTMOV = False
            self.BCKMOV = False
        
        if (self.command[0] == 1 and (self.NOTMOV or self.FRONTMOV)): #w
            self.pedal_time += 2
            self.NOTMOV = False
            self.FRONTMOV = True
            if (self.pedal_time > 90):
                self.pedal_time = 90
                
            self.x_velocity = self.accelleration(self.pedal_time)*np.cos(np.radians(self.body_orientation))
            self.y_velocity = self.accelleration(self.pedal_time)*np.sin(np.radians(self.body_orientation))
            
        elif (self.command[3] == 1 and (self.FRONTMOV)):
            self.pedal_time -= 4
            if (self.pedal_time < 0):
                self.pedal_time = 0
            
            self.x_velocity = self.accelleration(self.pedal_time)*np.cos(np.radians(self.body_orientation))
            self.y_velocity = self.accelleration(self.pedal_time)*np.sin(np.radians(self.body_orientation))
            
        elif (self.command[3] == 1 and (self.NOTMOV or self.BCKMOV)):
            self.pedal_time += 2
            self.NOTMOV = False
            self.BCKMOV = True
            if (self.pedal_time > 90):
                self.pedal_time = 90
                
            self.x_velocity = -self.accelleration(self.pedal_time)*np.cos(np.radians(self.body_orientation))
            self.y_velocity = -self.accelleration(self.pedal_time)*np.sin(np.radians(self.body_orientation))
 
        elif (self.command[0] == 1 and (self.NOTMOV or self.BCKMOV)):
            self.pedal_time -= 4
            if (self.pedal_time < 0):
                self.pedal_time = 0
            
            self.x_velocity = -self.accelleration(self.pedal_time)*np.cos(np.radians(self.body_orientation))
            self.y_velocity = -self.accelleration(self.pedal_time)*np.sin(np.radians(self.body_orientation))


        elif(self.FRONTMOV):
            self.pedal_time -= 1
            if (self.pedal_time < 0):
                self.pedal_time = 0
                
            self.x_velocity = self.accelleration(self.pedal_time)*np.cos(np.radians(self.body_orientation))
            self.y_velocity = self.accelleration(self.pedal_time)*np.sin(np.radians(self.body_orientation))
        
        elif(self.BCKMOV):
            self.pedal_time -= 1
            if (self.pedal_time < 0):
                self.pedal_time = 0
                
            self.x_velocity = -self.accelleration(self.pedal_time)*np.cos(np.radians(self.body_orientation))
            self.y_velocity = -self.accelleration(self.pedal_time)*np.sin(np.radians(self.body_orientation))

        
        # ROTATION   
        if (self.command[1] == 1 and ((self.x_velocity**2 + self.y_velocity**2)**0.5) > 1): #a
            if (abs((self.x_velocity**2 + self.y_velocity**2)**0.5 <= 5)):
                self.body_orientation += ROTATION_VEL
            elif ( abs(self.x_velocity**2 + self.y_velocity**2)**0.5 <= 20 and abs(self.x_velocity**2 + self.y_velocity**2)**0.5 > 5):                
                self.body_orientation += ROTATION_VEL
                    
        if (self.command[2] == 1 and ((self.x_velocity**2 + self.y_velocity**2)**0.5) > 1): #a
            if (abs((self.x_velocity**2 + self.y_velocity**2)**0.5 <= 5)):
                self.body_orientation -= ROTATION_VEL
            elif ( abs(self.x_velocity**2 + self.y_velocity**2)**0.5 <= 20 and abs(self.x_velocity**2 + self.y_velocity**2)**0.5 > 5):                
                self.body_orientation -= ROTATION_VEL
                
        if(self.body_orientation >= 360):
            self.body_orientation = 0
        if(self.body_orientation < 0):
            self.body_orientation += 360
            
           
       
           
    
    def accelleration(self, time):
        
        velocity = MAX_VELOCITY*time/40
        if (velocity > MAX_VELOCITY):
            velocity = MAX_VELOCITY
        return velocity
    

    def rot_center(self, image, angle, x, y):
        #rotated_image = pygame.transform.rotate(self.image_ori, self.body_orientation)


        self.image = pygame.transform.rotate(self.image_ori, self.body_orientation)
       # new_rect = rotated_image.get_rect(center = self.image.get_rect(center = (center_x, center_y)).center)    
       # self.image = rotated_image
       # self.rect = new_rect
        self.rect = self.image.get_rect(center=self.rect.center) 
        
    def draw_sensors(self):
        if (self.body_orientation <= 90 and self.body_orientation >= 0):
            self.left_sensor = [self.rect.x + self.w_ori*(math.cos(np.radians(self.body_orientation))), self.rect.y]
            self.right_sensor = [self.rect.x + self.image.get_width(), self.rect.y + self.h_ori*math.cos(np.radians(self.body_orientation))]
        
            self.rightb_sensor = [self.rect.x - self.h_ori*(-1)*math.sin(np.radians(self.body_orientation)), self.rect.y + self.image.get_height()]
            self.leftb_sensor = [self.rect.x , self.rect.y - self.w_ori*(-1)*math.sin(np.radians(self.body_orientation))]
        
        elif(self.body_orientation < 360 and self.body_orientation >= 270):
            self.left_sensor = [self.rect.x + self.image.get_width(), self.rect.y + self.w_ori*(-1)*math.sin(np.radians(self.body_orientation))]
            self.right_sensor = [self.rect.x + self.w_ori*math.cos(np.radians(self.body_orientation)), self.rect.y + self.image.get_height()]
        
            self.rightb_sensor = [self.rect.x, self.rect.y - self.h_ori*(-1)*math.cos(np.radians(self.body_orientation))]
            self.leftb_sensor = [self.rect.x - self.h_ori*math.sin(np.radians(self.body_orientation)) ,self.rect.y]
        
        elif(self.body_orientation >= 180 and self.body_orientation < 270):
            self.left_sensor = [self.rect.x + self.h_ori*(-1)*math.sin(np.radians(self.body_orientation)), self.rect.y + self.image.get_height()]
            self.right_sensor = [self.rect.x , self.rect.y + self.w_ori*(-1)*math.sin(np.radians(self.body_orientation))]
        
            self.rightb_sensor = [self.rect.x - self.w_ori*(math.cos(np.radians(self.body_orientation))), self.rect.y]
            self.leftb_sensor = [self.rect.x + self.image.get_width(), self.rect.y - self.h_ori*math.cos(np.radians(self.body_orientation))]

        
        elif(self.body_orientation > 90 and self.body_orientation < 180):
            self.left_sensor = [self.rect.x, self.rect.y + self.h_ori*(-1)*math.cos(np.radians(self.body_orientation))]
            self.right_sensor = [self.rect.x + self.h_ori*math.sin(np.radians(self.body_orientation)) ,self.rect.y]

            self.rightb_sensor = [self.rect.x + self.image.get_width(), self.rect.y - self.w_ori*(-1)*math.sin(np.radians(self.body_orientation))]
            self.leftb_sensor = [self.rect.x - self.w_ori*math.cos(np.radians(self.body_orientation)), self.rect.y + self.image.get_height()]

        
        self.know = [self.rect.x, self.rect.y]
        self.know2 = [self.rect.x + self.image.get_width(), self.rect.y + self.image.get_height()]
        self.know3 = [self.rect.x + self.image.get_width(), self.rect.y]
        self.know4 = [self.rect.x, self.rect.y + self.image.get_height()]
        
        # pygame.draw.circle(SCREEN, FUCSIA, self.left_sensor, 5)
        # pygame.draw.circle(SCREEN, FUCSIA, self.right_sensor, 5)
        # pygame.draw.circle(SCREEN, YELLOW, self.leftb_sensor, 5)
        # pygame.draw.circle(SCREEN, FUCSIA, self.rightb_sensor, 5)
        

       
    
    def radar(self, radar_angle):
        length = 10
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])
       # print(x,y)
       # while not SCREEN.get_at((x, y)) == pygame.Color(2, 105, 31, 255) and length < 200:
        while not (SCREEN.get_at((x, y)).r <= 3 and SCREEN.get_at((x, y)).g <= 3 and SCREEN.get_at((x, y)).b <= 3) and length < 200:
            
            length += 1
            x = int(self.rect.center[0] + math.cos(math.radians(self.body_orientation + radar_angle)) * length)
            if x < 50:
                x = 50
            y = int(self.rect.center[1] - math.sin(math.radians(self.body_orientation + radar_angle)) * length)
            if y < 5:
                y = 5
            if y > SCREEN_HEIGHT-5:
                y = SCREEN_HEIGHT-5
        # Draw Radar
        #pygame.draw.line(SCREEN, (255, 255, 255, 255), self.rect.center, (x, y), 1)
       # pygame.draw.circle(SCREEN, (0, 255, 0, 0), (x, y), 3)

        dist = int(math.sqrt(math.pow(self.rect.center[0] - x, 2)
                             + math.pow(self.rect.center[1] - y, 2)))

        self.radars.append([radar_angle, dist])
        #print(dist)
        
        
    
    def detect_collision(self):
        x_l = int(self.left_sensor[0])
        y_l = int(self.left_sensor[1])
        x_r = int(self.right_sensor[0])
        y_r = int(self.right_sensor[1])
        x_lb = int(self.leftb_sensor[0])
        y_lb = int(self.leftb_sensor[1])
        x_rb = int(self.rightb_sensor[0])
        y_rb = int(self.rightb_sensor[1])
        if(x_l <= 1 or x_r <= 1 or x_lb <= 1 or x_rb <= 1 or y_l >= 1100 or y_r >= 1100 or y_lb >= 1100 or y_rb >= 1100):
            return True
        #print(SCREEN.get_at((x_l, y_l)))
        l_col = (SCREEN.get_at((x_l, y_l)))
        r_col = (SCREEN.get_at((x_r, y_r)))
        lb_col = (SCREEN.get_at((x_lb, y_lb)))
        rb_col = (SCREEN.get_at((x_rb, y_rb)))
        if ((l_col.r <=3 and l_col.g <=3 and l_col.b <=3)  or (r_col.r <=3 and r_col.g <=3 and r_col.b <=3) or (lb_col.r <=3 and lb_col.g <=3 and lb_col.b <=3)  or (rb_col.r <=3 and rb_col.g <=3 and rb_col.b <=3) or (l_col == (31, 158, 69, 255))) :
         #   print((self.left_sensor[0], self.left_sensor[1]))
 
            return True
        # if(self.x_velocity == 0 and self.y_velocity == 0):  
        #     self.still += 1
        # else:
        #     self.still = 0
        # if self.still >= 10:
        #    # print("Too slow")
        #     return True
        return False
    
    # def detect_finishline(self):
    #     if(self.left_sensor[0] <= 485 and self.left_sensor[0] >= 470 and self.left_sensor[1] >= 600 and self.left_sensor[1] < 900):
    #         return True
    #     else:
    #         return False
    
    def update(self):
        
        self.draw_sensors()
        self.input_analisys()
        self.move()
        self.crashed = self.detect_collision()
       # self.finish_line = self.detect_finishline()
        self.radars.clear()
        angles = [-180, -145, -35, 0, 35, 145]
        for i in range(len(angles)):
            self.radar(angles[i])
        
       
    def draw(self, SCREEN):
        # pygame.Surface.set_colorkey(self.rect,(255,255,255))
       SCREEN.blit(self.image, (self.rect.x, self.rect.y))
     
       
       
    def data(self, x, y):
        input = [0, 0, 0, 0, 0, 0,    0]
        index = 0
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
            index = i
        dist = ((self.rect.centerx - x)**2 + (self.rect.centery - y)**2)**0.5
        input[index +1] = dist
        #print(input)
        return input 
    
    def distance(self,x,y):
        dist = ((self.rect.centerx - x)**2 + (self.rect.centery - y)**2)**0.5
        return dist
    
       
def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)        


def eval_genomes(genomes, config): #sostituisci con main ed elimina la parte finale
    clock = pygame.time.Clock()
    fit = 1
    global cars, ge, nets, shifts
    
    cars = []
    ge = []
    nets = []
    
    park = parking.Park()
    park.fixed_gen()
    park.draw()
    
    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
   # command = [0,0,0,0]
    time = 0
    while True: 
        time += 1
        #print(time)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if len(cars) == 0:
            break
        
        if (time >= 250):
            for i, car in enumerate(cars):
                ge[i].fitness += 1000 - car.sprite.distance(park.obj_coord[0], park.obj_coord[1])*2
                print(ge[i].fitness)
                remove(i)   
                
        for i, car in enumerate(cars):
            #ge[i].fitness -= car.sprite.distance(park.obj_coord[0], park.obj_coord[1])/10
   
            
            
            if car.sprite.crashed:
                ge[i].fitness -= 500
                ge[i].fitness += 1000 - car.sprite.distance(park.obj_coord[0], park.obj_coord[1])*2
                print(ge[i].fitness)
                remove(i)
                
        
         
        
        
        
        
        
        for i, car in enumerate(cars):
           output = nets[i].activate(car.sprite.data(park.obj_coord[0], park.obj_coord[1]))
           if output[0] > 0.7:
               car.sprite.command[0] = 1
               car.sprite.command[3] = 0
           if output[1] > 0.7:
               car.sprite.command[1] = 1
               car.sprite.command[2] = 0
           if output[0] <= 0.7:
               car.sprite.command[3] = 1
               car.sprite.command[0] = 0
           if output[1] <= 0.4:
               car.sprite.command[2] = 1
               car.sprite.command[1] = 0
           if output[1] > 0.4 and output[1] <= 0.7:
               car.sprite.command[2] = 0
               car.sprite.command[1] = 0
        
        park.draw() 
        for car in cars:
            car.update()
            car.sprite.rot_center(car.sprite.image_ori, car.sprite.body_orientation, car.sprite.rect.centerx, car.sprite.rect.centery) 
            if car.sprite.crashed == False:
                car.draw(SCREEN)            
           
        
        
        clock.tick(60)
        pygame.display.update()
        



def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)

    # pop.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # pop.add_reporter(stats)

    pop.run(eval_genomes)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'PARKconfig.txt')
    run(config_path)
    