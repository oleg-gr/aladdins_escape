"""
    Aladdin's Escape
Final project, Introduction to Computer Science, Fall 2012, NYUAD
Oleg Grishin
"""

import pygame, sys
from pygame.locals import *

class Floor1 (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((194,26)).convert_alpha()
        self.image.fill((255,255,255,0))
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 274 - 5 #adjust to falling speed - adjusting textures
        
class Floor2 (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((149,26)).convert_alpha()
        self.image.fill((255,255,255,0))
        self.rect = self.image.get_rect()
        self.rect.left = 194
        self.rect.top = 249 - 5
        
class Floor3 (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((191,26)).convert_alpha()
        self.image.fill((255,255,255,0))
        self.rect = self.image.get_rect()
        self.rect.left = 342
        self.rect.top = 225 - 5

class Aladdin (pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.stay = pygame.image.load('res/aladdin.png')
        self.frames = [pygame.image.load('res/aladdin1.png'),pygame.image.load('res/aladdin2.png'),pygame.image.load('res/aladdin3.png'),pygame.image.load('res/aladdin4.png'),pygame.image.load('res/aladdin5.png'),pygame.image.load('res/aladdin6.png'),pygame.image.load('res/aladdin7.png')]
        self.frames1 = [pygame.image.load('res/1aladdin1.png'),pygame.image.load('res/1aladdin2.png'),pygame.image.load('res/1aladdin3.png'),pygame.image.load('res/1aladdin4.png'),pygame.image.load('res/1aladdin5.png'),pygame.image.load('res/1aladdin6.png'),pygame.image.load('res/1aladdin7.png')]
        self.speed = 7
        self.falspeed = 5
        self.image = self.stay
        self.x = 400
        self.y = 150
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.falling = True
        self.jumping = False
        self.move = 's'
        self.framecount = 0
        self.jstart = 0        
        
    def update(self):
        if self.falling:
            self.y += self.falspeed
        if self.move == 'r':
            self.image = self.frames[self.framecount]
            self.framecount += 1
            self.framecount %= len(self.frames)
        elif self.move == 'l':
            self.image = self.frames1[self.framecount]
            self.framecount += 1
            self.framecount %= len(self.frames1)
        elif self.move == 's':
            self.image = self.stay
        self.rect.left = self.x
        self.rect.top = self.y
        self.move = 's'

def main():

#initializing the graphics
    pygame.init()
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
    aladdin = Aladdin()
    floor = [Floor1(),Floor2(),Floor3()]
    sprites = pygame.sprite.Group(aladdin, floor[0], floor[1], floor[2])

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
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and (aladdin.x + aladdin.rect.width in range(0,width)):
            aladdin.x += aladdin.speed
            aladdin.move = 'r'
        elif keys[pygame.K_LEFT] and (aladdin.x - aladdin.speed in range(0,width)):
            aladdin.x -= aladdin.speed
            aladdin.move = 'l'

        for i in range(3):
            if aladdin.rect.colliderect(floor[i].rect):
                if aladdin.rect.centerx in range(floor[i].rect.left,floor[i].rect.right):
                    aladdin.falling = False
                    aladdin.y = floor[i].rect.top - aladdin.rect.height
                elif aladdin.rect.right >= floor[i].rect.left + aladdin.speed:
                    aladdin.x -= aladdin.speed
            aladdin.falling = True
            
            
        
        sprites.clear(screen,bg)
        sprites.update()
        sprites.draw(screen)
        pygame.display.update()
        fpsClock.tick(FPS)

main()
