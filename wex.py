import pygame

#classes and methods-----------------------
class Platform:
    def __init__(self, name):
        self.name = name
        self.rect = pygame.Rect(WIDTH/12 - 50, HEIGHT-150, WIDTH/1.2 + 100, 100)#xpos, ypos, width, height
#+80 so 40 on each side, for climbing up platform
class SubPlatform(Platform):
    def __init__(self, name, LRM):#LRM dictates position of sub, 0=left, 1=mid, 2=right.
        super().__init__(name)
        middle = 0
        if LRM == 1:
            middle = 200 
        self.rect = pygame.Rect((WIDTH/12) + (5 * WIDTH * LRM) /18, HEIGHT-400 - middle, (WIDTH/18) * 5, 50)









#consts---------------
WIDTH = 1280
HEIGHT = 960


#inits
basePlatform = Platform("Base")
leftPlatform = SubPlatform("Left", 0)
midPlatform = SubPlatform("Middle", 1)
rightPlatform = SubPlatform("Right", 2)


#pygame--------------------------------
pygame.init()
run = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #exit mainloop

    screen.fill("white")#bg fill color  CHANGE TO PROPER BACKGROUND LTR.
    pygame.draw.rect(screen, "black", basePlatform.rect)
    pygame.draw.rect(screen, "black", leftPlatform.rect)
    pygame.draw.rect(screen, "black", midPlatform.rect)
    pygame.draw.rect(screen, "black", rightPlatform.rect)

    
    pygame.display.flip()#flip updates a section of the screen.
    clock.tick(60)#sets fps

pygame.quit()