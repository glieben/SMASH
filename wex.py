import pygame

#classes and methods-----------------------
class Platform:
    def __init__(self, name):
        platList.append(self)
        self.name = name
        self.rect = pygame.Rect(WIDTH/12 - 50, HEIGHT-150, WIDTH/1.2 + 100, 1)#xpos, ypos, width, height
#+80 so 40 on each side, for climbing up platform
class SubPlatform(Platform):
    def __init__(self, name, LRM):#LRM dictates position of sub, 0=left, 1=mid, 2=right.
        super().__init__(name)
        middle = 0
        if LRM == 1:
            middle = 200 
        self.rect = pygame.Rect((WIDTH/12) + (5 * WIDTH * LRM) /18, HEIGHT-400 - middle, (WIDTH/18) * 5, 1)

class Characters:
    def __init__(self, name, player, color):
        charList.append(self)
        self.name = name
        self.player = player #int, either p1 or p2.
        self.hp = 200
        if player == 1:
            self.rect = pygame.Rect(WIDTH/12 - 50, HEIGHT-400, 100, 100)
            self.hpBar = pygame.Rect(10, HEIGHT-100, 400, 50)
            self.orientation = 1 #just base init.
            self.hpOrientation = -1
        else:
            self.rect = pygame.Rect(WIDTH - (WIDTH/12 + 50), HEIGHT-400, 100, 100)
            self.hpBar = pygame.Rect(WIDTH - 410, HEIGHT-100, 400, 50)
            self.orientation = -1
            self.hpOrientation = 1

        self.color = color
        self.jumpV = JUMPV
        self.jump = False
        self.onGround = True
        self.lastJump = 0
        self.midair = False
        self.canMidair = True
        self.fallV = FALLV
        self.fall = False
        self.oneBase = False
        self.controls = CONTROLS[self.player]
        self.moveset = MOVESET[self.player]

        self.guard = False
        self.guardHp = 200

        self.punch = False
        self.grab = False
        self.canMove = True
        self.canAttack = True
        self.lastAttack = 0
        self.lastMove = 0

        self.immobilized = False
        self.immobilizeStart = 0

        self.combo = ""
        self.tempCombo = "-"
        self.comboTimer = 0

        self.COMBOS = { #dict of combos, where LIST = [DMG, XMOVE, YMOVE, FALL, STUNTIME, HBOX]
            "UA" : [5 * self.orientation, 0, True],
            "RR" : [200, -20, False],
            "LL" : [-200, -20, False],
        }
        
        self.dashed = False




#character subclasses---------------
class Haein(Characters):
    def __init__(self, name, player, color):
        super().__init__(name, player, color)
        self.COMBOS.update({
            
        })

class Musashi(Characters):
    def __init__(self, name, player, color):
        super().__init__(name, player, color)
        self.COMBOS.update({
            
        })



def getHit(dmg, player, kb, direction):
    player.hp -= dmg
    player.hpBar.inflate_ip(-2*dmg, 0)
    player.hpBar.move_ip(player.hpOrientation*dmg, 0)
    player.rect.move_ip(kb * direction, 0)

def guardHit(dmg, player):#PLAYER IS OTHER PLAYER USUALLY.
    player.guardHp -= dmg






#consts & lists---------------
WIDTH = 1280
HEIGHT = 960
platList = []
charList = []
GRAVITY = 0.6
JUMPV = 18
FALLV = 0

CONTROLS = {
    1 : {
        "left" : pygame.K_a,
        "right" : pygame.K_d,
        "up" : pygame.K_w,
        "down" : pygame.K_s
    },

    2 : {
        "left" : pygame.K_LEFT,
        "right" : pygame.K_RIGHT,
        "up" : pygame.K_UP,
        "down" : pygame.K_DOWN
    }
}

MOVESET = {
    1 : {
        "grab" : pygame.K_r,
        "attack" : pygame.K_t,
        "guard" : pygame.K_f,
        "special" : pygame.K_g #not sure if will be implemented.
    },

    2 : {
        "grab" : pygame.K_k,
        "attack" : pygame.K_l,
        "guard" : pygame.K_COMMA,
        "special" : pygame.K_PERIOD
    }
}

#inits-----------------
basePlatform = Platform("Base")
leftPlatform = SubPlatform("Left", 0)
midPlatform = SubPlatform("Middle", 1)
rightPlatform = SubPlatform("Right", 2)

haein = Haein("Haein", 1, "purple")
musashi = Musashi("Musashi", 2, "Black")


#pygame--------------------------------
pygame.init()
font = pygame.font.SysFont("Comic Sans", 100)
run = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #exit mainloop

    screen.fill("white")#bg fill color  CHANGE TO PROPER BACKGROUND LTR.
    currentTime = pygame.time.get_ticks()
    

    for player in charList:#player inputs
        centerx = player.rect.center[0]
        centery = player.rect.center[1]

#atk moves      
        key = pygame.key.get_pressed()
        if key[player.moveset["guard"]] and not (player.jump or player.fall) and player.guardHp > 0:#centered, -5 to center the larger hitbox
            player.guardbox = pygame.Rect(player.rect.x - 5, player.rect.y - 5, 110, 110)
            player.guard = True
            player.canMove = False
            

        elif player.canAttack and not player.immobilized:
            if key[player.moveset["attack"]]:#-30 for punchbox width
                player.canAttack = False
                player.lastAttack = pygame.time.get_ticks()#not redundant; actually needed.
                player.combo += "A"#these stuff first, so if combo exists, dont punch.

#COMBOS------------------------
                didCombo = False
                for x in range(len(player.combo) - 1):
                    currentCombo = player.combo[x:len(player.combo)]
                    print(currentCombo)
                    if currentCombo in player.COMBOS: #LONGEST COMBOS ON TOP, DECREASING AS TIME GOES ON. IT GOES INTO A LONGER COMBO FIRST IF POSSIBLE.
                        #2 length combos
                        movestats = player.COMBOS[currentCombo]
                        player.rect.move_ip(movestats[0], movestats[1])
                        if movestats[2]:
                            player.jumpV = 0
                        didCombo = True

                if not didCombo:
                    player.punchbox = pygame.Rect((centerx - 30) + (80 * player.orientation), player.rect.y + 20, 60, 40)
                    player.punch = True 
                


            elif key[player.moveset["grab"]] and player.guardHp > 0:
                player.grabbox = pygame.Rect((centerx - 20) + (50 * player.orientation), player.rect.y + 20, 40, 40)
                player.grab = True 
                player.canAttack = False
                player.lastAttack = pygame.time.get_ticks()
                player.combo += "G"

            elif key[player.moveset["special"]]:#NO FUNCTION YET
                player.canAttack = False
                player.lastAttack = pygame.time.get_ticks()



#movement---------------
        if player.canMove and not player.immobilized:
            if player.combo in player.COMBOS and not player.dashed: #dashes.
                #2 length combos
                movestats = player.COMBOS[player.combo]
                player.rect.move_ip(movestats[0], movestats[1])
                player.dashed = True
            #before movement so can check for atkdash first.


            if key[player.controls["up"]]: #dupe check
                if not player.jump and player.onGround:#jump also takes prio to midair
                    player.jump = True
                    player.combo += "U" #no dupe checks since singular.
                    player.lastJump = pygame.time.get_ticks()
                elif player.canMidair and currentTime - player.lastJump > 250:#50ms delay between midair.
                    player.midair = True
                    player.combo += "U"

            if key[player.controls["left"]]:
                player.rect.move_ip(-5, 0)
                player.orientation = -1
                if currentTime - player.lastMove > 20 or player.combo == "": #prevents dupes of movement in combo
                    player.combo += "L"
                player.lastMove = pygame.time.get_ticks()
                
                

            if key[player.controls["right"]]:
                player.rect.move_ip(5, 0)
                player.orientation = 1
                if currentTime - player.lastMove > 20 or player.combo == "": #prevents dupes of movement in combo, but allows if combo resets.
                    player.combo += "R"
                player.lastMove = pygame.time.get_ticks()

            

        for plats in platList:#draw plats
            pygame.draw.rect(screen, "black", plats.rect)


        posx = player.rect.x
        if player.midair:
            player.jumpV = JUMPV
            player.midair = False
            player.canMidair = False
            player.jump = True

        if player.jump:
            player.rect.move_ip(0, -player.jumpV)
            player.jumpV -= GRAVITY

#jump logic-------- + gravity
        player.fall = True #by default true.
        player.onBase = False #by default false.
        for plats in platList:
            #check if there is a platform under. +VE IS DOWN
            #MOVE = MOVE_IP BUT DOES NOT UPDATE LOL
            temprect = player.rect.move(0, 1)
            if (player.rect).colliderect(plats.rect): 
                if player.jump and player.jumpV <= 0 and (player.rect.bottom + player.jumpV) <= plats.rect.top:#only while moving down can you stop
                    player.rect.bottom = (plats.rect.top) #NEW SYNTAX DISCOVERED. TO SET POSITION = EQUALS.
                    player.jump = False #there is bottom, top, left, right, can also do 8 directions.
                    player.jumpV = JUMPV
                    

            #reaches ground
            if player.jump == False and temprect.colliderect(plats.rect) and (temprect.bottom - 1) <= plats.rect.top:#if there is a platform below,
                player.fall = False
                player.fallV = FALLV
                if plats.name == "Base": #prevents falling if base plat is below.
                    player.onBase = True
                player.canMidair = True #resets midair, as well as jump.
                player.onGround = True
                


        if player.fall and player.jump == False :#no platform, and not in jump, fall
            player.fallV += GRAVITY
            player.rect.move_ip(0, player.fallV)

            for plats in platList:
                if (player.rect).colliderect(plats.rect) and (player.rect.bottom +- player.fallV) <= plats.rect.top:
                    player.rect.bottom = (plats.rect.top)
            player.onGround = False

#drop
        elif key[player.controls["down"]] and not(player.fall or player.onBase):
            player.rect.move_ip(0, 1)


#fighting---------- different for so p1 isnt first, then p2.
    for player in charList:
        for obj in charList:#get other player. only needed in attack phase
            if obj != player:
                otherPlayer = obj

        if player.punch:
            pygame.draw.rect(screen, "red", player.punchbox)
            player.punch = False

            if (player.punchbox).colliderect(otherPlayer.rect):
                if otherPlayer.guard:
                    guardHit(10, otherPlayer)
                else:
                    getHit(10, otherPlayer, 5, player.orientation)

        if player.grab:
            pygame.draw.rect(screen, "green", player.grabbox)
            player.grab = False

            if (player.grabbox).colliderect(otherPlayer.rect):
                otherPlayer.immobilized = True
                otherPlayer.immobilizeStart = pygame.time.get_ticks()
        
        if otherPlayer.immobilized and (currentTime - otherPlayer.immobilizeStart) > 300:
            otherPlayer.immobilized = False

            
        if player.canAttack == False and currentTime - player.lastAttack > 500:
            player.canAttack = True
            player.combo = ""#resets combo after attack move.
            

#combo resetting
        if player.tempCombo != player.combo:
            player.comboTimer = currentTime
        player.tempCombo = player.combo

        if currentTime - player.comboTimer > 300:
            player.combo = "" #reset combo if no inputs in 300ms.
            player.comboTimer = currentTime #auto resets timer.
            player.dashed = False #reset dash after combo timer.


        textObj = font.render(player.combo, False, ("black"))
        textRect = textObj.get_rect(center=((WIDTH/2 + 500 * player.hpOrientation),(50)))
        screen.blit(textObj, textRect)

#attr reset. in other loop so input>attack>attr set are all in the same timeframe
    for player in charList:
        if player.guard:
            pygame.draw.rect(screen, "blue", player.guardbox)
            player.guard = False
            player.canMove = True

        pygame.draw.rect(screen, player.color, player.rect)
        pygame.draw.rect(screen, "red", player.hpBar)








    pygame.display.flip()#flip updates a section of the screen.
    clock.tick(60)#sets fps

pygame.quit()