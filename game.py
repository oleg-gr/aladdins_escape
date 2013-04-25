"""
    Aladdin's Escape
Final project, Introduction to Computer Science, Fall 2012, NYUAD
Oleg Grishin
"""

import pygame, sys
from pygame.locals import *
import time

# Floor classes handle collide events for the character to stay on the floor. Not visible

class Floor(pygame.sprite.Sprite):
    def __init__(self,length,left,top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((length,1))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

class Platform(pygame.sprite.Sprite):
    def __init__(self,left,top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('res/platform.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.tech_sprite_lower = Floor(self.rect.width - 34,self.rect.left + 17,self.rect.top - 1)
        self.tech_sprite_upper = Floor(self.rect.width - 34,self.rect.left + 17,self.rect.top - 51)
        #dimensions of the character sprite + some space for falspeed

class Coin(pygame.sprite.Sprite):
    def __init__(self,left,top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('res/coin.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.wait = 0
        self.die = False

    def collect(self):
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.die = True
        
    def update(self):
        
        if self.die:
            self.wait +=1
            self.rect.top -= 3
        if self.wait > 8:
            self.kill()
            Aladdin.coins +=1
        if self.wait == 1:
            self.rect.left -= 3



class Aladdin (pygame.sprite.Sprite):
    
    coins = 1
    
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.stay = pygame.image.load('res/aladdin.png')
        self.frames = [pygame.image.load('res/aladdin.png'),\
                       pygame.image.load('res/aladdin1.png'),pygame.image.load('res/aladdin2.png'),\
                       pygame.image.load('res/aladdin3.png'),pygame.image.load('res/aladdin4.png'),\
                       pygame.image.load('res/aladdin5.png'),pygame.image.load('res/aladdin6.png'),\
                       pygame.image.load('res/aladdin7.png'),pygame.image.load('res/aladdin8.png')]
        self.frame = 0
        self.image = self.stay

        #settings for player's movements
        self.speed = 8
        self.falspeed = 10
        self.jumpspeed = -12
        self.jumpduration = 4
        
        self.x = 450
        self.y = 150
        self.vx = 0
        self.vy = self.falspeed
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.jumptimer = 0
        self.jumping = False
        self.jumpable = False
        self.start = time.time()
        self.t= time.time() - self.start
        self.text = pygame.font.Font('res/font/04B_03__.ttf', 14)
        self.message = self.text.render('' + str(Aladdin.coins) + '/5', False, (255,255,255))
        self.mesrect=self.message.get_rect()
        self.mesrect.topleft = (373,254)
        self.text1 = pygame.font.Font('res/font/04B_03__.ttf', 14)
        self.message1 = self.text1.render('', False, (255,255,255))
        self.mesrect1=self.message1.get_rect()
        self.mesrect1.topleft = (373,269)
        Aladdin.coins = 0
        


    def jump(self):
        if self.jumpable:
            self.jumptimer = 0
            self.jumping = True
        
    def update(self):
    
        if self.jumping:
            if self.jumptimer < self.jumpduration:
                self.jumptimer +=1
                self.vy = self.jumpspeed
            else:
                self.jumptimer = 0
                self.jumping = False

        
        if self.x + self.vx in range (0,533 - self.rect.width):
            self.x += self.vx
            
        
        if self.vy != 0 and self.vx >= 0:
            self.image = self.frames[3]
        elif self.vy != 0 and self.vx < 0:
            self.image = self.frames[3]
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.vx == 0:
            self.image = self.stay
        elif self.vx > 0:
            self.image = self.frames[self.frame]
            self.frame += 1
            self.frame %= len(self.frames)
        elif self.vx < 0:
            self.image = self.frames[self.frame]
            self.image = pygame.transform.flip(self.image, True, False)
            self.frame += 1
            self.frame %= len(self.frames)
        
        self.y += self.vy
        self.rect.left = self.x
        self.rect.top = self.y
        self.message = self.text.render('Coins collected: ' + str(Aladdin.coins) + '/5', False, (255,255,255))
        self.t= time.time() - self.start
        self.message1 = self.text1.render('Time: ' + str(round(self.t,1)), False, (255,255,255))

        

def main():
#initializing the graphics
    pygame.init()
    pygame.font.init()
    FPS = 30
    fpsClock = pygame.time.Clock()
    height = 300
    width = 533

#possible scaling of the game
    scale = 2

    screen = pygame.display.set_mode((width, height),0,32) #trying out 32 colors
    pygame.display.set_caption("Aladdin's Escape")
    bg = pygame.image.load('res/bg.png').convert()
    screen.blit(bg, (0,0))

#game
    running = True
#instancing the classes
    aladdin = Aladdin()
    #[bottom floor, middle floor, top floor, first stopper, second stopper]
    floor = [Floor(194,0,273),Floor(147,207,248),Floor(190,355,224)]
    stops = [Floor(10,194,261),Floor(10,342,236)]
    platforms = [Platform (100, 100), Platform (40, 150), Platform (120, 180), Platform (200,200)]
    coins = [Coin(116,82), Coin(56,132), Coin(136,162), Coin (216,182), Coin (300,98)]
    #to put coins on platforms: (x+16,x - 18)
    sprites = pygame.sprite.Group(platforms,coins)
    character = pygame.sprite.Group(aladdin)

    #technical sprites for platforms
    """
    for item in platforms:
        sprites.add(item.tech_sprite_lower,item.tech_sprite_upper)
    """
        
    floorsprites = pygame.sprite.Group(floor)
    stopsprites = pygame.sprite.Group(stops)
        

#music
    """
    pygame.mixer.music.load('res/background.mp3')
    pygame.mixer.music.play(-1, 0.0)
    """

#main game loop
    while running:
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.mixer.music.stop()
                pygame.font.quit()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    aladdin.jump()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    aladdin.vx = 0


        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            aladdin.vx = aladdin.speed
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            aladdin.vx = -aladdin.speed


        collision = pygame.sprite.spritecollide(aladdin, floorsprites, False)
        if collision:
            aladdin.vy = 0
            aladdin.y = collision[0].rect.top - aladdin.rect.height + 1
            aladdin.jumpable = True            
        else:
            aladdin.jumpable = False
            if not aladdin.jumping:
                aladdin.vy = aladdin.falspeed
                
        
                
        collision = pygame.sprite.spritecollide(aladdin, stopsprites, False)
        if collision:
            aladdin.x = collision[0].rect.left -  aladdin.rect.width

        for item in platforms:
            if pygame.sprite.collide_rect(aladdin,item.tech_sprite_lower) and pygame.sprite.collide_rect(aladdin,item.tech_sprite_upper):
                aladdin.vy = 0
                aladdin.y = item.tech_sprite_lower.rect.top - aladdin.rect.height + 1
                aladdin.jumpable = True

        for item in coins:
            if pygame.sprite.collide_rect(aladdin,item):
                item.collect()
                
                
    


            
        #character group is made to make sure that the character is drawn on top of everything
        screen.blit(bg, (0,0))
        sprites.clear(screen,bg)
        character.clear(screen,bg)
        sprites.update()
        character.update()
        sprites.draw(screen)
        character.draw(screen)
        screen.blit(aladdin.message,aladdin.mesrect)
        screen.blit(aladdin.message1,aladdin.mesrect1)

        #draw technical sprites for debugging
        """
        floorsprites.draw(screen)
        stopsprites.draw(screen)
        """

        
        pygame.display.update()
        fpsClock.tick(FPS)

main()
