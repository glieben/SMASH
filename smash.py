import pygame

pygame.init()
#needs double parenthesis to set screen size.
screen = pygame.display.set_mode((1200,800))#pixels size.

#RECT OUTSIDE GAME LOOP, YOU DON'T WANT IT TO BE INIT INFINITELY.
player = pygame.Rect((300, 250, 50, 50))


run = True#program loop
canJump = True
startTicks = 0
while run:
#parent element, color, rect reference.
    screen.fill(("black"))#REFRESHES SCREEN, SO PREV GRAPHICS DIE.

    pygame.draw.rect(screen, ("white"), player)
    
    if player.y < 750:
        player.move_ip(0, 1)#gravity

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True: #pygame key = a == true. SYNTAX.
        player.move_ip(-1, 0)#IP = IN PLACE.
    if key[pygame.K_d] == True: #pygame key = b == true. SYNTAX.
        player.move_ip(1, 0)#IP = IN PLACE.
    if key[pygame.K_w] == True and canJump == True: #JUMP   
        player.move_ip(0, -500)#IP = IN PLACE.
        canJump = False
        startTicks = pygame.time.get_ticks()
        print(0)

    if ((pygame.time.get_ticks() - startTicks) /1000) > 2:
        canJump = True


    for event in pygame.event.get():#iterates through all pygame events.
        if event.type == pygame.QUIT:
            run = False#exits loop

    pygame.display.update()#draw rewrites it, this shows it on screen.

pygame.quit()#actual quit.
    