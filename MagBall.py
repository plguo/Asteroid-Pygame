import pygame
import random
from color import*
from physic import*
sizeX = 800
sizeY = 500

class MagBall(pygame.sprite.DirtySprite):
    def __init__ (self,number,color,mu,di):
        #Lower than block and mouse
        self._layer = 2
        pygame.sprite.DirtySprite.__init__(self)
        #basic init
        self.radius = 30
        self.mu = mu
        self.di = di
        self.color = color
        self.number = number 
        #shape
        self.redraw()
        self.rect = self.image.get_rect()
        
    def redraw(self):
        self.image = pygame.Surface((self.radius*2,self.radius*2),flags=pygame.SRCALPHA)
        self.image.convert_alpha()
        pygame.draw.circle(self.image,self.color,(self.radius,self.radius),30,0)
        if self.number > 0:
            if self.mu:
                strings = '*'+ str(self.number)
            elif self.di:
                strings = '/'+ str(self.number)
            else:
                strings = '+' + str(self.number)
        elif self.number < 0:
            if self.mu:
                strings = '*('+ str(self.number) +')'
            elif self.di:
                strings = '/('+ str(self.number) + ')'
            else:
                strings = str(self.number)
        else:
            strings = '0'
        numberFont = pygame.font.SysFont("Arial",20,True)
        numberLabel = numberFont.render(strings,True,white)
        self.image.blit(numberLabel,
                        (self.radius-int(numberLabel.get_width()/2),
                         self.radius-int(numberLabel.get_height()/2)))

class BadBall(MagBall):
    def __init__ (self):
        rand = random.randrange(9)
        randNum = random.randint(-5,5)
        if rand < 2:
            mu = False
            di = False
        elif rand < 6:
            mu = False
            di = False
        elif rand < 8:
            mu = True
            di = False
        else:
            mu = False
            di = True
        if (randNum < 0) or (di):
            color = red
        else:
            color = green
        MagBall.__init__(self,randNum,color,mu,di)
        startY = random.randrange(sizeY-60)
        self.moveSpeed = random.randrange(2)
        self.moveDir = random.randrange(2)
        self.rect.x = sizeX + 30
        self.rect.y = startY
        self.floatX = float(self.rect.x)
        self.floatY = float(self.rect.y)
        
    def update(self,x_speed,block_group):

        if self.rect.y + self.radius*2 >= sizeY:
            self.moveDir = 2
        elif self.rect.y <= 0:
            self.moveDir = 0
            
        coll_block = 0
        coll_bool = False
        for b in block_group:
            if pygame.sprite.collide_rect(b,self):
                coll_block = get_collideDir(b,self)
                coll_bool = True
                obj_block = b
                break
        
        if coll_block == 1 and coll_bool:
            self.floatX -= x_speed + self.moveSpeed*0.5
            if self.moveDir == 2:
                self.floatY += (1 - self.moveDir)
            else:
                self.floatY = float(obj_block.rect.top-self.rect.height)
        #--#
        elif coll_block == 2 and coll_bool:
            self.floatX -= x_speed + self.moveSpeed*0.5
            if self.moveDir == 0:
                self.floatY += (1 - self.moveDir)
            else:
                self.floatY = float(obj_block.rect.bottom)
        #--#
        elif coll_block == 4 and coll_bool:
            self.floatY += (1 - self.moveDir)
        #--#
        else:
            self.floatX -= x_speed + self.moveSpeed*0.5
            self.floatY += (1 - self.moveDir)
        
        self.rect.x = int(self.floatX)
       
        #self.floatX -= x_speed
        self.rect.y = int(self.floatY)
        if (self.rect.x < -50) or (
            (self.rect.top + 1 >= sizeY) or (self.rect.bottom - 1 <= 0)):
            self.kill()
        
       
class PlayerBall(MagBall):
    def __init__ (self,number,posX,posY):
        MagBall.__init__(self,number,blue,False,False)
        self.fallBeginT = 400
        self.fallBeginY = posY
        self.rect.x = posX
        self.rect.y = posY
        self.freeFall = True
        self.losted = False
        self.moveSpeed = 0 
    def update(self,block_group):
        global sizeY
        if self.number == 0:
            self.losted = True

        if self.freeFall:
            if (sizeY - self.radius*2)>self.rect.y : 
                self.rect.y = freeFall(pygame.time.get_ticks()-self.fallBeginT,self.fallBeginY)
            else:
                self.rect.y = sizeY - self.radius*2
                
        if self.rect.y < (sizeY - self.radius*2):
            self.moveSpeed = 0.8
        else:
            self.moveSpeed = 0
        #block
        coll_block = 0
        coll_bool = False
        for b in block_group:
            if pygame.sprite.collide_rect(b,self):
                coll_block = get_collideDir(b,self)
                coll_bool = True
                obj_block = b
                break
        
        if coll_block == 1 and coll_bool:
            self.rect.y = int(obj_block.rect.top-self.rect.height)
        #--#
        elif coll_block == 2 and coll_bool:
            self.rect.y = int(obj_block.rect.bottom)
        #--#
        elif coll_block == 3 and coll_bool:
            self.moveSpeed = 0

                
    def startFall(self):
        self.fallBeginT = pygame.time.get_ticks()
        self.fallBeginY = self.rect.y
        self.freeFall = True
