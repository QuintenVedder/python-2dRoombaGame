import time
import numpy as np
import random
import maps
import pygame as pg
import os
import sys
from classes import Player, Block
sys.path.append('shootergame/maps/')
pg.init()
map_name = str(random.randint(0, 99999999999999))
map_file_name = "{}".format(map_name)
start_point = (0, 0)
player_radius = 15
player_color = (255, 0, 0)
speed = 1
Clock = pg.time.Clock()
FPS = 30
timer = time.time()

def get_current_file_path():
    current_file = __file__
    parent_directory = os.path.abspath(os.path.join(current_file, os.pardir))
    parent_directory = parent_directory.replace('\\', '\\\\')
    return parent_directory
# images
root_dir = get_current_file_path()
root_img_dir = root_dir + "\\images\\"
img_start_button = pg.image.load(root_img_dir + "\\start.png")
img_start_button_pressed = pg.image.load(root_img_dir + "\\start_druk.png")

img_maps_button = pg.image.load(root_img_dir + "\\maps.png")
img_maps_button_pressed = pg.image.load(root_img_dir + "\\maps_druk.png")

img_quit_button = pg.image.load(root_img_dir + "\\quit.png")
img_quit_button_pressed = pg.image.load(root_img_dir + "\\quit_druk.png")

img_play_button = pg.image.load(root_img_dir + "\\play.png")
img_play_button_pressed = pg.image.load(root_img_dir + "\\play_druk.png")

img_leftarrow_button = pg.image.load(root_img_dir + "\\left.png")
img_leftarrow_button_pressed = pg.image.load(root_img_dir + "\\left_druk.png")

img_rightarrow_button = pg.image.load(root_img_dir + "\\right.png")
img_rightarrow_button_pressed = pg.image.load(
    root_img_dir + "\\right_druk.png")

img_credits_button = pg.image.load(root_img_dir + "\\credits.png")
img_credits_button_pressed = pg.image.load(root_img_dir + "\\credits_druk.png")

img_instructions_button = pg.image.load(root_img_dir + "\\instructions.png")
img_instructions_button_pressed = pg.image.load(
    root_img_dir + "\\instructions_druk.png")

img_background = pg.image.load(root_img_dir + "\\menu_achtergrond.png")
img_title = pg.image.load(root_img_dir + "\\titel.png")


black = (0, 0, 0)
aplha_black = (0, 0, 0, 50)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (200, 200, 200)
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 1000
WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
font = pg.font.Font('freesansbold.ttf', 35)
# button variables
buttonwidth = 150
buttonheight = 50
buttonquitposX = (WINDOW_WIDTH - buttonwidth)/2
buttonquitposY = ((WINDOW_HEIGHT + 200) - buttonheight)/2

buttonmapmakingposX = (WINDOW_WIDTH - buttonwidth)/2
buttonmapmakingposY = ((WINDOW_HEIGHT - 100) - buttonheight)/2

buttonplayX = (WINDOW_WIDTH - buttonwidth)/2
buttonplayY = ((WINDOW_HEIGHT + 50) - buttonheight)/2

buttoninstructionsX = (WINDOW_WIDTH - buttonwidth)
buttoninstructionsY = (WINDOW_HEIGHT - buttonheight)

buttoncreditsX = (0)
buttoncreditsY = (WINDOW_HEIGHT - buttonheight)


def loadmap():
    if os.path.exists(root_dir + "\\maps\\" + map_file_name + ".npy"):
        return np.load(root_dir + "\\maps\\" + map_file_name + ".npy")
    else:
        return np.load(root_dir + "\\maps\\testlvl.npy")


activemap = loadmap()



def drawgrid(start_point, activemap, player=None):
    blocksize = 50
    array = activemap
    start_point = start_point
    for row in range(len(array)):
        for col in range(len(array[row])):
            x = col * blocksize
            y = row * blocksize
            block = Block(x, y, blocksize, blocksize, WINDOW)
            if array[row][col] == 1:
                if player is not None:
                    player.handle_collision(block)
                block.draw(black)
                block_alphasurface = pg.Surface(
                    (blocksize, blocksize), pg.SRCALPHA)
                pg.draw.rect(block_alphasurface, aplha_black,
                             block_alphasurface.get_rect())
                WINDOW.blit(block_alphasurface, (x, y+25))
            if array[row][col] == 2 and start_point == (0, 0):
                start_point = (x-(blocksize/2)+50, y-(blocksize/2)+50)
    return start_point


def drawgridmaker(mx, my):
    blocksize = 50
    for row in range(len(activemap)):
        for col in range(len(activemap[row])):
            x = col * blocksize
            y = row * blocksize
            rect = pg.Rect(x, y, blocksize, blocksize)
            if mx > x and mx < (x+blocksize) and my > y and my < (y+blocksize):
                pg.draw.rect(WINDOW, red, rect)
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            activemap[row][col] = 1
                        if event.button == 2:
                            activemap[row][col] = 2
                        if event.button == 3:
                            activemap[row][col] = 0

            elif activemap[row][col] == 2:
                pg.draw.rect(WINDOW, green, rect)
            elif activemap[row][col] == 1:
                pg.draw.rect(WINDOW, white, rect)
            elif activemap[row][col] == 0:
                pg.draw.rect(WINDOW, white, rect, 1)


runmapmaker = False
runplay = False
mainmenu = True
spawn_player = True
title_height = 0
title_down = False
start = False
instructions = False

while mainmenu:
    Clock.tick(FPS)
    while runmapmaker:
        WINDOW.fill((black))
        mouse = pg.mouse.get_pos()
        drawgridmaker(mouse[0], mouse[1])

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    np.save("shootergame/maps/" + map_file_name, activemap)
                if event.key == pg.K_q:
                    mainmenu = True
                    runmapmaker = False

        if event.type == pg.QUIT:
            runmapmaker = False

        savemaptext = font.render('press S to save and Q to quit', True, grey)
        WINDOW.blit(savemaptext, (0, WINDOW_HEIGHT-100))
        pg.display.flip()

    while runplay:
        WINDOW.fill((white))
        WINDOW.blit(img_background, (0, 0))
        keys = pg.key.get_pressed()
        if spawn_player and start_point != (0, 0):
            player = Player(
                "player", start_point[0], start_point[1], player_radius, player_color, WINDOW)
            spawn_player = False

        if spawn_player == False:
            start_point = drawgrid(start_point, activemap, player)
            player.move((keys[pg.K_RIGHT] - keys[pg.K_LEFT]) *
                        speed, (keys[pg.K_DOWN] - keys[pg.K_UP]) * speed)
            player.draw()
        else:
            start_point = drawgrid(start_point, activemap)

        if keys[pg.K_q]:
            mainmenu = True
            runplay = False

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                a = 1

        if event.type == pg.QUIT:
            runplay = False
        pg.display.flip()

    while instructions:
        a = 1



    WINDOW.fill((white))
    WINDOW.blit(img_background, (0, 0))
    if time.time() - timer > 1:
        title_down = not title_down
        if title_down:
            title_height += 20
        else:
            title_height -= 20
        timer = time.time()

    WINDOW.blit(img_title, (210, title_height))

    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            if buttonquitposX <= mouse[0] <= buttonquitposX+buttonwidth and buttonquitposY <= mouse[1] <= buttonquitposY+buttonheight:
                pg.quit()

            if buttonmapmakingposX <= mouse[0] <= buttonmapmakingposX+buttonwidth and buttonmapmakingposY <= mouse[1] <= buttonmapmakingposY+buttonheight:
                runmapmaker = True

            if buttonplayX <= mouse[0] <= buttonplayX+buttonwidth and buttonplayY <= mouse[1] <= buttonplayY+buttonheight:
                if start:
                    runplay = True
                else:
                    start = True

    mouse = pg.mouse.get_pos()
#  quit button
    if buttonquitposX <= mouse[0] <= buttonquitposX+buttonwidth and buttonquitposY <= mouse[1] <= buttonquitposY+buttonheight:
        if start:
            WINDOW.blit(img_quit_button_pressed,
                        (buttonquitposX, buttonquitposY))

    else:
        if start:
            WINDOW.blit(img_quit_button, (buttonquitposX, buttonquitposY))

#  map making button
    if buttonmapmakingposX <= mouse[0] <= buttonmapmakingposX+buttonwidth and buttonmapmakingposY <= mouse[1] <= buttonmapmakingposY+buttonheight:
        if start:
            WINDOW.blit(img_maps_button_pressed,
                        (buttonmapmakingposX, buttonmapmakingposY))

    else:
        if start:
            WINDOW.blit(img_maps_button,
                        (buttonmapmakingposX, buttonmapmakingposY))

#  play button
    if buttonplayX <= mouse[0] <= buttonplayX+buttonwidth and buttonplayY <= mouse[1] <= buttonplayY+buttonheight:
        if start:
            WINDOW.blit(img_play_button_pressed, (buttonplayX, buttonplayY))
        else:
            WINDOW.blit(img_start_button_pressed, (buttonplayX, buttonplayY))

    else:
        if start:
            WINDOW.blit(img_play_button, (buttonplayX, buttonplayY))
        else:
            WINDOW.blit(img_start_button, (buttonplayX, buttonplayY))

# instruction button
    if buttoninstructionsX <= mouse[0] <= buttoninstructionsX+buttonwidth and buttoninstructionsY <= mouse[1] <= buttoninstructionsY+buttonheight:
        if start:
            WINDOW.blit(img_instructions_button_pressed,
                        (buttoninstructionsX, buttoninstructionsY))

    else:
        if start:
            WINDOW.blit(img_instructions_button,
                        (buttoninstructionsX, buttoninstructionsY))


# credits button
    if buttoncreditsX <= mouse[0] <= buttoncreditsX+buttonwidth and buttoncreditsY <= mouse[1] <= buttoncreditsY+buttonheight:
        if start:
            WINDOW.blit(img_credits_button_pressed,
                        (buttoncreditsX, buttoncreditsY))

    else:
        if start:
            WINDOW.blit(img_credits_button, (buttoncreditsX, buttoncreditsY))

    if event.type == pg.QUIT:
        mainmenu = False

    # end event handling
    pg.display.flip()
