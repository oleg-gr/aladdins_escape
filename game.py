"""
Aladdin's Escape
Final project, Introduction to Computer Science, Fall 2012, NYUAD
Oleg Grishin
"""

import pygame, sys
import time
from random import *
from pygame.locals import *

# Floor class handles collide events for the character to stay on the floor. Not visible

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

    def collect(self,sound):
        self.image = pygame.transform.scale(self.image, (22, 22))
        if not self.die:
            sound.play()
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

class Rock (pygame.sprite.Sprite):

    def __init__ (self, left, anticipation, speed):
        pygame.sprite.Sprite.__init__(self)
        self.frames = [pygame.image.load('res/rock1.png'),pygame.image.load('res/rock2.png')]
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.init = left
        self.rect.top = -self.rect.height/2
        self.anticipation = anticipation
        self.anticipated = 0
        self.vy = 0
        self.speed = speed
        self.shakewait = 0
    
    def shake(self):
        k = randint(0,5)
        if self.shakewait == 1:
            self.rect.left += k
        elif self.shakewait == 3:
            self.rect.left -= k
        self.shakewait += 1
        self.shakewait %= 4


    def red(self):
        self.image = self.frames[1]
        
    def fall(self):
        self.rect.left = self.init
        self.image = self.frames[0]
        self.vy = self.speed
    

    def update (self):
        
        if self.anticipated in range (self.anticipation/3, self.anticipation):
            self.shake()
        if self.anticipated  in range (self.anticipation * 2 /3, self.anticipation):
            self.red ()
        elif self.anticipated > self.anticipation and self.rect.top < 300:
            self.fall()
        else:
            self.vy = 0
            
        self.anticipated += 1
        self.rect.top += self.vy



class Aladdin (pygame.sprite.Sprite):
    
    coins = 1
    
    def __init__ (self, game, level, rock_frequency, rock_anticipation):
        pygame.sprite.Sprite.__init__(self)
        self.stay = pygame.image.load('res/aladdin.png')
        self.frames = [pygame.image.load('res/aladdin.png'),pygame.image.load('res/aladdin1.png'),\
                       pygame.image.load('res/aladdin2.png'),pygame.image.load('res/aladdin3.png'),\
                       pygame.image.load('res/aladdin4.png'),pygame.image.load('res/aladdin5.png'),\
                       pygame.image.load('res/aladdin6.png'),pygame.image.load('res/aladdin7.png'),\
                       pygame.image.load('res/aladdin8.png')]
        self.frame = 0
        self.image = self.stay

        #settings for player's movements
        self.speed = 8
        self.falspeed = 10
        self.jumpspeed = -12
        self.jumpduration = 4
        
        self.x = 0
        self.y = 210
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
        self.mesrect.topleft = (483,257)
        self.message1 = self.text.render('', False, (255,255,255))
        self.mesrect1=self.message1.get_rect()
        self.mesrect1.topleft = (483,275)
        self.level = level
        if level < 10:
            self.message2 = self.text.render('level 0' + str(level), False, (255,255,255))
        else:
            self.message2 = self.text.render('level ' + str(level), False, (255,255,255))
        self.mesrect2=self.message2.get_rect()
        self.mesrect2.topleft = (460,242)
        Aladdin.coins = 0
        self.rocks = []
        self.globalrocks = game.rocks
        self.rockfrequency = 1
        self.rock_frequency = rock_frequency
        self.rock_anticipation = rock_anticipation

        


    def jump(self, sound):
        if self.jumpable:
            sound.play()
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

        
        if self.x + self.vx in range (0 - self.speed,533 - self.rect.width + self.speed):
            self.x += self.vx
        elif self.x + self.vx > 533 - self.rect.width + self.speed and Aladdin.coins == 5:
            newgame(self.level+1)
        
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
        self.message = self.text.render(str(Aladdin.coins )+ '/5', False, (255,255,255))
        self.t= time.time() - self.start
        self.rockfrequency += 1
        self.rockfrequency %= self.rock_frequency #lover in order to increase frequency of rocks falling
        if self.rockfrequency == 0:
            self.rockrandom = randint (0, 500)
            self.rocks.append(Rock(self.rockrandom, self.rock_anticipation, 10))
            self.globalrocks.add(self.rocks.pop())

        self.message1 = self.text.render(str(round(self.t,1)), False, (255,255,255))
        
        
class Game():
    def __init__(self, level, platforms, coins, rock_frequency, rock_anticipation):
        #instancing the classes
        #[bottom floor, middle floor, top floor, first stopper, second stopper]
        self.floor = [Floor(194,0,273),Floor(147,207,248),Floor(190,355,224)]
        self.stops = [Floor(10,194,261),Floor(10,342,236)]
        self.coins = coins
        self.platforms = platforms
        self.sprites = pygame.sprite.Group(self.platforms,self.coins)
        self.rocks = pygame.sprite.Group()
        self.aladdin = Aladdin(self, level, rock_frequency, rock_anticipation)
        self.character = pygame.sprite.Group(self.aladdin)
        
        #technical sprites for platforms
        """
        for item in game.platforms:
        sprites.add(item.tech_sprite_lower,item.tech_sprite_upper)
        """
    
        self.floorsprites = pygame.sprite.Group(self.floor)
        self.stopsprites = pygame.sprite.Group(self.stops)

def compare(x,y):
    if float(x[1]) > float (y[1]):
        return 1
    else:
        return -1

def build_highscores(names):
    names = sorted(names, cmp=compare)
    table = []

    for i in range(5):
        table.append ([text.render(names[i][0], False, (255,255,255)),text.render(names [i][1] + 's', False, (255,255,255))])
    return table
        
def newgame(level):
    global game, times, frame
    if level == 1:
        pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load('res/game_bg.mp3')
        pygame.mixer.music.set_volume(volume / 5.0)
        pygame.mixer.music.play(-1, 0.0)
        rock_frequency = 40
        rock_anticipation = 50
        platforms = [Platform (100, 100), Platform (40, 150), Platform (120, 180), Platform (200,200)]        
        #to put coins on platforms: (x+16,x-18)  
        coins = [Coin(116,82), Coin(56,132), Coin(136,162), Coin (216,182), Coin (300,98)]
        times = []
        game = Game (level, platforms , coins, rock_frequency, rock_anticipation)
        
    if level == 2:
        times.append(round(game.aladdin.t,1))
        game = Game (level, [Platform (100, 100), Platform (40, 150), Platform (120, 180), Platform (200,200)],\
                    [Coin(114,82), Coin(56,132), Coin(136,162), Coin (216,182), Coin (300,98)],\
                     20, 30)
    if level == 3:
        times.append(round(game.aladdin.t,1))
        game = Game (level, [Platform (100, 100), Platform (40, 150), Platform (120, 180), Platform (200,200)],\
                    [Coin(114,82), Coin(56,132), Coin(136,162), Coin (216,182), Coin (300,98)],\
                     10, 15)
    if level == 4:
        times.append(round(game.aladdin.t,1))
        frame = 'win'
        #win sound first
        pygame.mixer.music.fadeout(50)
        win_s.play()



def main():
    global game, times, frame, text, volume, win_s
#initializing the graphics
    pygame.init()
    pygame.font.init()
    FPS = 30
    fpsClock = pygame.time.Clock()
    height = 300
    width = 533

#possible scaling of the game, not implemented
    scale = 2

    screen = pygame.display.set_mode((width, height),0,32) #trying out 32 colors
    pygame.display.set_caption("Aladdin's Escape")
    bg = pygame.image.load('res/bg.png').convert()
    screen.blit(bg, (0,0))
    coin = pygame.image.load('res/coin.png')
    coin = pygame.transform.scale(coin,(14, 14))
    timer = pygame.image.load('res/time.png')
    
    win = [0,pygame.image.load('res/win1.png'),pygame.image.load('res/win2.png')]

#game
    running = True

#to collect total time
    times = []
    text = pygame.font.Font('res/font/04B_03__.ttf', 20)
    text_big = pygame.font.Font('res/font/04B_03__.ttf', 22)
#name of the player
    letters = []

#highscores
    highscores = open('res/highscores.txt', 'r')
    limit = text_big.render ('',False, (255,0,0))
    high = pygame.image.load('res/high_scores.png')
    names = []

    menu = [0,pygame.image.load('res/menu1.png'), pygame.image.load('res/menu2.png'),\
            pygame.image.load('res/menu3.png'),pygame.image.load('res/menu4.png'),\
            pygame.image.load('res/menu5.png')]
    over = [0,pygame.image.load('res/game_over1.png'),pygame.image.load('res/game_over2.png'),\
            pygame.image.load('res/game_over3.png')]
    frame = 'menu'

#options
    options = [0,pygame.image.load('res/options1.png'),pygame.image.load('res/options2.png'),pygame.image.load('res/options3.png'),\
               pygame.image.load('res/options4.png')]
    musicon = 1
    sfxon = 1
    onoffpick = [pygame.image.load('res/sound_pick_off.png'),pygame.image.load('res/sound_pick_on.png')]
    onoffunpick = [pygame.image.load('res/sound_unpick_off.png'),pygame.image.load('res/sound_unpick_on.png')]
    volume = 5
    volumepick = [0,pygame.image.load('res/volume_pick_0.png'),pygame.image.load('res/volume_pick_20.png'),\
                  pygame.image.load('res/volume_pick_40.png'),pygame.image.load('res/volume_pick_60.png'),\
                  pygame.image.load('res/volume_pick_80.png'),pygame.image.load('res/volume_pick_100.png')]
    volumeunpick = [0,pygame.image.load('res/volume_unpick_0.png'),pygame.image.load('res/volume_unpick_20.png'),\
                  pygame.image.load('res/volume_unpick_40.png'),pygame.image.load('res/volume_unpick_60.png'),\
                  pygame.image.load('res/volume_unpick_80.png'),pygame.image.load('res/volume_unpick_100.png')]

#about
    story = [1, pygame.image.load('res/story1.png'),pygame.image.load('res/story2.png')]
    rules = [0,pygame.image.load('res/rules1.png'),pygame.image.load('res/rules2.png'),pygame.image.load('res/rules3.png')]
    about = [0, pygame.image.load('res/about1.png'),pygame.image.load('res/about2.png')]

#music

    pygame.mixer.music.load('res/menu_bg.mp3')
    pygame.mixer.music.play(-1, 0.0)

#SFX
    coin_s = pygame.mixer.Sound('res/coin.wav')
    tick_s = pygame.mixer.Sound('res/tick.wav')
    jump_s = pygame.mixer.Sound('res/jump.aiff')
    over_s = pygame.mixer.Sound('res/over.aiff')
    win_s = pygame.mixer.Sound('res/win.mp3')
    tick_s.set_volume(0.5) #adjusting loud sound
    jump_s.set_volume(0.25)
    
#main game loop
    while running:

        if frame == "game":
            if pygame.sprite.spritecollideany(game.aladdin, game.rocks):#quit if the character's killed
                    pygame.mixer.music.fadeout(200)
                    over_s.play()
                    frame = "over"

            
            for event in pygame.event.get():
                if event.type == QUIT: 
                    running = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    highscores.close()
                    pygame.quit()
                    sys.exit()
            
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.aladdin.jump(jump_s)
                    if event.key == pygame.K_ESCAPE:
                        frame = "menu"
                        pygame.mixer.music.load('res/menu_bg.mp3')
                        pygame.mixer.music.set_volume(volume / 5.0)
                        pygame.mixer.music.play(-1, 0.0)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        game.aladdin.vx = 0


            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                game.aladdin.vx = game.aladdin.speed
            elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                game.aladdin.vx = -game.aladdin.speed


            collision = pygame.sprite.spritecollide(game.aladdin, game.floorsprites, False)
            if collision:
                game.aladdin.vy = 0
                game.aladdin.y = collision[0].rect.top - game.aladdin.rect.height + 1
                game.aladdin.jumpable = True            
            else:
                game.aladdin.jumpable = False
                if not game.aladdin.jumping:
                    game.aladdin.vy = game.aladdin.falspeed
                    
            
                    
            collision = pygame.sprite.spritecollide(game.aladdin, game.stopsprites, False)
            if collision:
                game.aladdin.x = collision[0].rect.left -  game.aladdin.rect.width

            for item in game.platforms:
                if pygame.sprite.collide_rect(game.aladdin,item.tech_sprite_lower) and pygame.sprite.collide_rect(game.aladdin,item.tech_sprite_upper):
                    game.aladdin.vy = 0
                    game.aladdin.y = item.tech_sprite_lower.rect.top - game.aladdin.rect.height + 1
                    game.aladdin.jumpable = True

            for item in game.coins:
                if pygame.sprite.collide_rect(game.aladdin,item):
                    item.collect(coin_s)
                    
        


                
            #character group is made to make sure that the character is drawn on top of everything
            screen.blit(bg, (0,0))
            game.sprites.clear(screen,bg)
            game.character.clear(screen,bg)
            game.rocks.clear(screen,bg)
            game.sprites.update()
            game.character.update()
            game.rocks.update()
            game.sprites.draw(screen)
            game.character.draw(screen)
            game.rocks.draw(screen)
            screen.blit(game.aladdin.message,game.aladdin.mesrect)
            screen.blit(game.aladdin.message1,game.aladdin.mesrect1)
            screen.blit(game.aladdin.message2,game.aladdin.mesrect2)
            screen.blit(coin, (463,256))
            screen.blit(timer, (463,273))

            #draw technical sprites for debugging
            """
            game.floorsprites.draw(screen)
            game.stopsprites.draw(screen)
            """

        if frame == "menu":
            
            for event in pygame.event.get():
                if event.type == QUIT: 
                    running = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    highscores.close()
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        tick_s.play()
                        menu[0] += 1
                        menu[0] %= 5
                    if event.key == pygame.K_UP:
                        tick_s.play()
                        menu[0] -= 1
                        menu[0] %= 5
                    if event.key == pygame.K_RETURN:
                        if menu[0] == 0:
                            newgame(1)
                            frame = "game"
                        if menu[0] == 1:
                            frame = "story"
                        if menu[0] == 2:
                            #file can be read() only once
                            highscores.close()
                            highscores = open('res/highscores.txt', 'r')
                            names = build_highscores([x.split(':') for x in highscores.read().rstrip('\n').split('\n')])
                            frame = "high"
                            menu[0] == 0
                        if menu[0] == 3:
                            options[0] = 0
                            frame = "options"
                        if menu[0] == 4:
                            running = False
                            pygame.mixer.music.stop()
                            highscores.close()
                            pygame.font.quit()
                            pygame.quit()
                            sys.exit()
                            
            
            screen.blit(menu[menu[0]+1], (0,0))

        if frame == "over":
            
            for event in pygame.event.get():
                if event.type == QUIT: 
                    running = False
                    pygame.mixer.music.stop()
                    highscores.close()
                    pygame.font.quit()
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        tick_s.play()
                        over[0] += 1
                        over[0] %= 3
                    if event.key == pygame.K_LEFT:
                        tick_s.play()
                        over[0] -= 1
                        over[0] %= 3
                    if event.key == pygame.K_RETURN:
                        if over[0] == 0:
                            newgame(1)
                            over_s.fadeout(50)
                            frame = "game"
                        if over[0] == 1:
                            over_s.fadeout(50)
                            pygame.mixer.music.load('res/menu_bg.mp3')
                            pygame.mixer.music.set_volume(volume / 5.0)
                            pygame.mixer.music.play(-1, 0.0)
                            frame = "menu"
                            over[0] = 0
                        if over[0] == 2:
                            running = False
                            pygame.mixer.music.stop()
                            pygame.font.quit()
                            highscores.close()
                            pygame.quit()
                            sys.exit()

            screen.blit(over[over[0]+1], (0,0))

        if frame == "win":
            for event in pygame.event.get():
                if event.type == QUIT: 
                    running = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    highscores.close()
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if len(pygame.key.name(event.key)) == 1 and len(letters) < 8:
                        letters.append(pygame.key.name(event.key).upper())
                    if event.key == pygame.K_BACKSPACE and len(letters)>0:
                        letters.pop()
                    if event.key == pygame.K_RIGHT:
                        tick_s.play()
                        win[0] += 1
                        win[0] %= 2
                    if event.key == pygame.K_LEFT:
                        tick_s.play()
                        win[0] -= 1
                        win[0] %= 2
                    if event.key == pygame.K_RETURN:
                        if win[0] == 0:
                            if len(letters) > 3:
                                frame = "high"
                                highscores.close()
                                highscores = open('res/highscores.txt', 'a')
                                highscores.write(''.join(letters) + ':' + str(sum(times))+'\n')
                                highscores.close()
                                highscores = open('res/highscores.txt', 'r')
                                names = build_highscores([x.split(':') for x in highscores.read().rstrip('\n').split('\n')])
                                limit = text_big.render ('',False, (255,0,0))
                                win_s.fadeout(50)
                                pygame.mixer.music.load('res/menu_bg.mp3')
                                pygame.mixer.music.set_volume(volume / 5.0)
                                pygame.mixer.music.play(-1, 0.0)
                            else:
                                limit = text_big.render ('___',False, (255,0,0))
                        if win[0] == 1:
                            win[0] = 0
                            frame = "menu"
                            win_s.fadeout(50)
                            pygame.mixer.music.load('res/menu_bg.mp3')
                            pygame.mixer.music.set_volume(volume / 5.0)
                            pygame.mixer.music.play(-1, 0.0)

                                 
                    
                    

            score = text.render(str(sum(times)) + 's', False, (255,255,255))
            name = text_big.render (' '.join(letters),False, (255,255,255))

            screen.blit(win[win[0]+1], (0,0))
            screen.blit(limit, (322,157))
            screen.blit(name, (174,182)) 
            screen.blit(score,(302,102))

        if frame == "high":
            
            for event in pygame.event.get():
                if event.type == QUIT: 
                    running = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    highscores.close()
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        frame = "menu"

                
            screen.blit(high, (0,0))
            screen.blit(names[0][0],(160,130))
            screen.blit(names[0][1],(300,130))
            screen.blit(names[1][0],(160,150))
            screen.blit(names[1][1],(300,150))
            screen.blit(names[2][0],(160,170))
            screen.blit(names[2][1],(300,170))
            screen.blit(names[3][0],(160,190))
            screen.blit(names[3][1],(300,190))
            screen.blit(names[4][0],(160,210))
            screen.blit(names[4][1],(300,210))

        if frame == "options":
            
           for event in pygame.event.get():
            if event.type == QUIT: 
                running = False
                pygame.mixer.music.stop()
                pygame.font.quit()
                highscores.close()
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    tick_s.play()
                    options[0] += 1
                    options[0] %= 4
                if event.key == pygame.K_UP:
                    tick_s.play()
                    options[0] -= 1
                    options[0] %= 4
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if options[0] == 0:
                        tick_s.play()
                        musicon += 1
                        musicon %= 2
                    if options[0] == 1:
                        tick_s.play()
                        sfxon += 1
                        sfxon %= 2
                if options[0] == 2:
                    if event.key == pygame.K_LEFT and volume > 0:
                        tick_s.play()
                        volume -= 1
                    if event.key == pygame.K_RIGHT and volume < 5:
                        tick_s.play()
                        volume += 1
                
                if event.key == pygame.K_RETURN:
                    if options[0] == 3:
                        frame = "menu"
                        
            screen.blit(options[options[0]+1], (0,0))

            if options[0] == 0:
                screen.blit(onoffpick[musicon],(274,126))
            else:
                screen.blit(onoffunpick[musicon],(274,126))
                
            if options[0] == 1:
                screen.blit(onoffpick[sfxon],(274,160))
            else:
                screen.blit(onoffunpick[sfxon],(274,160))

            if options[0] == 2:
                screen.blit(volumepick[volume+1],(274,194))
            else:
                screen.blit(volumeunpick[volume+1],(274,194))

            if musicon == 0:
                pygame.mixer.music.set_volume(0.0)
            else:
                pygame.mixer.music.set_volume(volume/5.0)
                
#!!!all sfx volume
            if sfxon == 0:
                coin_s.set_volume(0.0)
                tick_s.set_volume(0.0)
                jump_s.set_volume(0.0)
                over_s.set_volume(0.0)
                win_s.set_volume(0.0)
            else:
                coin_s.set_volume(volume/5.0)
                tick_s.set_volume(volume/10.0)
                jump_s.set_volume(volume/20.0)
                over_s.set_volume(volume/5.0)
                win_s.set_volume(volume/5.0)
                
        if frame == "story":

            for event in pygame.event.get():

                if event.type == QUIT: 
                    running = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    highscores.close()
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        tick_s.play()
                        story[0] += 1
                        story[0] %= 2
                    if event.key == pygame.K_RETURN:
                        if story[0] == 0:
                            frame = "menu"
                        if story[0] == 1:
                            tick_s.play()
                            frame = "rules"
                            rules[0] = 2

        
            screen.blit(story[story[0]+1], (0,0))
            
        if frame == "about":

            for event in pygame.event.get():

                if event.type == QUIT: 
                    running = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    highscores.close()
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        tick_s.play()
                        about[0] += 1
                        about[0] %= 2
                    if event.key == pygame.K_RETURN:
                        if about[0] == 0:
                            frame = "menu"
                        if about[0] == 1:
                            tick_s.play()
                            frame = "rules"
                            rules[0] = 1

        
            screen.blit(about[about[0]+1], (0,0))


        if frame == "rules":

            for event in pygame.event.get():

                if event.type == QUIT: 
                    running = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    highscores.close()
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        tick_s.play()
                        rules[0] += 1
                        rules[0] %= 3
                    if event.key == pygame.K_LEFT:
                        tick_s.play()
                        rules[0] -= 1
                        rules[0] %= 3                        
                    if event.key == pygame.K_RETURN:
                        if rules[0] == 0:
                            frame = "menu"
                        if rules[0] == 1:
                            tick_s.play()
                            frame = "story"
                            story[0] = 1
                        if rules[0] == 2:
                            tick_s.play()
                            frame = "about"
                            about[0] = 1

        
            screen.blit(rules[rules[0]+1], (0,0))
            
                        
        pygame.display.update()
        fpsClock.tick(FPS)

main()
