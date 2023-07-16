import time
import numpy as np
import random
import shutil
import tkinter as tk
from tkinter import messagebox
import pygame as pg
import os
from classes import Player, Block, Button, Battery, Mess
import instruction_texts as texts
import credit_text

pg.init()
start_point = (0, 0)
player_radius = 25
player_color = (255, 0, 0)
batteryX = 900
batteryY = 400
battery_life = 1
speed = 6
Clock = pg.time.Clock()
frame_count = 0
FPS = 60
timer = time.time()

# vars for drawgrid()
highest_x = 0
highest_y = 0

black = (0, 0, 0)
aplha_black = (0, 0, 0, 50)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (200, 200, 200)
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 1000
WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
font = pg.font.Font(None, 30)
pg.display.set_caption('Sweeping Shenanigans')


def get_current_file_path():
    current_file = __file__
    parent_directory = os.path.abspath(os.path.join(current_file, os.pardir))
    parent_directory = parent_directory.replace(os.path.sep, '/')
    return parent_directory


# images
root_dir = get_current_file_path()
root_img_dir = root_dir + "/images/"
# player movement images. i know the variable names suck, deal with it!
off_down = pg.image.load(root_img_dir + "redroomba_down.png")
off_left = pg.image.load(root_img_dir + "redroomba_left.png")
off_right = pg.image.load(root_img_dir + "redroomba_right.png")
off_up = pg.image.load(root_img_dir + "redroomba_up.png")
on_down = pg.image.load(root_img_dir + "roomba_down.png")
on_left = pg.image.load(root_img_dir + "roomba_left.png")
on_right = pg.image.load(root_img_dir + "roomba_right.png")
on_up = pg.image.load(root_img_dir + "roomba_up.png")

# battery images img-1 is full and 5 empty
root_img_battery_dir = root_dir + "/images/batteryframes/"
img_battery_1_f1 = pg.image.load(root_img_battery_dir + "battery1_frame1.png")
img_battery_2_f1 = pg.image.load(root_img_battery_dir + "battery2_frame1.png")
img_battery_3_f1 = pg.image.load(root_img_battery_dir + "battery3_frame1.png")
img_battery_4_f1 = pg.image.load(root_img_battery_dir + "battery4_frame1.png")
img_battery_1_f2 = pg.image.load(root_img_battery_dir + "battery1_frame2.png")
img_battery_2_f2 = pg.image.load(root_img_battery_dir + "battery2_frame2.png")
img_battery_3_f2 = pg.image.load(root_img_battery_dir + "battery3_frame2.png")
img_battery_4_f2 = pg.image.load(root_img_battery_dir + "battery4_frame2.png")
img_battery_5 = pg.image.load(root_img_battery_dir + "battery5.png")

# button images
img_start_button = pg.image.load(root_img_dir + "start.png")
img_start_button_pressed = pg.image.load(root_img_dir + "start_druk.png")

img_maps_button = pg.image.load(root_img_dir + "maps.png")
img_maps_button_pressed = pg.image.load(root_img_dir + "maps_druk.png")

img_mapmaker_button = pg.image.load(root_img_dir + "placeholder.png")
img_mapmaker_button_pressed = pg.image.load(root_img_dir + "placeholder.png")

img_levels_button = pg.image.load(root_img_dir + "placeholder.png")
img_levels_button_pressed = pg.image.load(root_img_dir + "placeholder.png")

img_back_button = pg.image.load(root_img_dir + "placeholder.png")
img_back_button_pressed = pg.image.load(root_img_dir + "placeholder.png")

img_quit_button = pg.image.load(root_img_dir + "quit.png")
img_quit_button_pressed = pg.image.load(root_img_dir + "quit_druk.png")

img_play_button = pg.image.load(root_img_dir + "play.png")
img_play_button_pressed = pg.image.load(root_img_dir + "play_druk.png")

img_leftarrow_button = pg.image.load(root_img_dir + "left.png")
img_leftarrow_button_pressed = pg.image.load(root_img_dir + "left_druk.png")

img_rightarrow_button = pg.image.load(root_img_dir + "right.png")
img_rightarrow_button_pressed = pg.image.load(root_img_dir + "right_druk.png")

img_credits_button = pg.image.load(root_img_dir + "credits.png")
img_credits_button_pressed = pg.image.load(root_img_dir + "credits_druk.png")

img_instructions_button = pg.image.load(root_img_dir + "instructions.png")
img_instructions_button_pressed = pg.image.load(root_img_dir + "instructions_druk.png")

img_background = pg.image.load(root_img_dir + "menu_achtergrond.png")
img_title = pg.image.load(root_img_dir + "titel.png")
img_icon = pg.image.load(root_img_dir + "icon.png")
img_mess = pg.image.load(root_img_dir + "dust.png")
pg.display.set_icon(img_icon)

# button variables
buttonwidth = 150
buttonheight = 50
arrowbuttonwidth = 50
arrowbuttonheight = 150

buttonquitposX = (WINDOW_WIDTH - buttonwidth)/2
buttonquitposY = ((WINDOW_HEIGHT + 200) - buttonheight)/2

buttonmapsposX = (WINDOW_WIDTH - buttonwidth)/2
buttonmapsposY = ((WINDOW_HEIGHT - 100) - buttonheight)/2

buttonmapmakerposX = (WINDOW_WIDTH - buttonwidth)/2
buttonmapmakerposY = ((WINDOW_HEIGHT - 100) - buttonheight)/2

buttonlevelsposX = (WINDOW_WIDTH - buttonwidth)/2
buttonlevelsposY = ((WINDOW_HEIGHT + 50) - buttonheight)/2

buttonbackposX = (WINDOW_WIDTH - buttonwidth)/2
buttonbackposY = ((WINDOW_HEIGHT + 200) - buttonheight)/2

buttonplayX = (WINDOW_WIDTH - buttonwidth)/2
buttonplayY = ((WINDOW_HEIGHT + 50) - buttonheight)/2

buttoninstructionsX = (WINDOW_WIDTH - buttonwidth)
buttoninstructionsY = (WINDOW_HEIGHT - buttonheight)

buttoncreditsX = (0)
buttoncreditsY = (WINDOW_HEIGHT - buttonheight)

instructions_title_posX = (WINDOW_WIDTH - buttonwidth)/2
instructions_title_posY = 0

instructions_arrowleft_posX = 0
instructions_arrowrigth_posX = (WINDOW_WIDTH - arrowbuttonwidth)
instructions_arrows_posY = (WINDOW_HEIGHT - arrowbuttonheight)/2

# making buttons
quitButton = Button(img_quit_button, img_quit_button_pressed, buttonquitposX, buttonquitposY, buttonwidth, buttonheight, WINDOW)
mapsButton = Button(img_maps_button, img_maps_button_pressed, buttonmapsposX, buttonmapsposY, buttonwidth, buttonheight, WINDOW)
mapmakerButton = Button(img_mapmaker_button, img_mapmaker_button_pressed, buttonmapmakerposX, buttonmapmakerposY, buttonwidth, buttonheight, WINDOW)
levelsButton = Button(img_levels_button, img_levels_button_pressed, buttonlevelsposX, buttonlevelsposY, buttonwidth, buttonheight, WINDOW)
backButton = Button(img_back_button, img_back_button_pressed, buttonbackposX, buttonbackposY, buttonwidth, buttonheight, WINDOW)
playButton = Button(img_play_button, img_play_button_pressed,buttonplayX, buttonplayY, buttonwidth, buttonheight, WINDOW)
startButton = Button(img_start_button, img_start_button_pressed,buttonplayX, buttonplayY, buttonwidth, buttonheight, WINDOW)
instructionsButton = Button(img_instructions_button, img_instructions_button_pressed, buttoninstructionsX, buttoninstructionsY, buttonwidth, buttonheight, WINDOW)
creditsButton = Button(img_credits_button, img_credits_button_pressed,buttoncreditsX, buttoncreditsY, buttonwidth, buttonheight, WINDOW)
arrow_leftButton = Button(img_leftarrow_button, img_leftarrow_button_pressed, instructions_arrowleft_posX, instructions_arrows_posY, arrowbuttonwidth, arrowbuttonheight, WINDOW)
arrow_rightButton = Button(img_rightarrow_button, img_rightarrow_button_pressed, instructions_arrowrigth_posX, instructions_arrows_posY, arrowbuttonwidth, arrowbuttonheight, WINDOW)

# lists for things ;)
arrows = [arrow_leftButton, arrow_rightButton]
buttons = [quitButton, mapsButton, playButton, instructionsButton, creditsButton]
map_buttons = [backButton, mapmakerButton, levelsButton]
player_images_on = [on_up, on_down, on_left, on_right]
player_images_off = [off_up, off_down, off_left, off_right]
player_images = player_images_on
battery_images = [img_battery_1_f1, img_battery_1_f2, img_battery_2_f1, img_battery_2_f2, img_battery_3_f1, img_battery_3_f2, img_battery_4_f1, img_battery_4_f2, img_battery_5]

instruction_texts_array = [
    [texts.play, img_play_button],
    [texts.maps, img_maps_button],
    [texts.quit, img_quit_button],
]

mess_pos_array = [
]

credits_text = credit_text.credits


def loadmap(runmapmaker, selected_level=None):
    print("loading level................")
    if runmapmaker:
        return np.load(root_dir + "/maps/testlvl_mapmaker.npy"), str(root_dir + "/maps/testlvl_mapmaker.npy")
    elif runmapmaker == False and selected_level != None:
        print('loading custom file.....{}'.format(selected_level))
        return np.load(root_dir + "/maps/CustomMaps/"+selected_level), str(root_dir + "/maps/CustomMaps/"+selected_level)
    else:
        print("was not able to load level. check the 'loadmap' function")
        return np.load(root_dir + "/maps/testlvl_mapmaker.npy"), str(root_dir + "/maps/testlvl_mapmaker.npy")


max_blocks = 200
space_blocks = 0
filled_blocks = 0

def drawgrid(max_blocks, space_blocks, filled_blocks, mess_array_fill, start_point, activemap, mess_pos_array, player=None):
    max_blocks, space_blocks, filled_blocks = max_blocks, space_blocks, filled_blocks
    mess_array_fill = mess_array_fill
    mess_pos_array = mess_pos_array
    blocksize = 50
    array = activemap
    start_point = start_point
    for row in range(len(array)):
        for col in range(len(array[row])):
            x = col * blocksize
            y = row * blocksize
            block = Block(x, y, blocksize, blocksize, WINDOW)
            if array[row][col] == 1:
                if max_blocks > (filled_blocks + space_blocks):
                    filled_blocks += 1
                if player is not None:
                    player.handle_collision(block)
                block.draw(black)
                block_alphasurface = pg.Surface((blocksize, blocksize), pg.SRCALPHA)
                pg.draw.rect(block_alphasurface, aplha_black, block_alphasurface.get_rect())
                WINDOW.blit(block_alphasurface, (x, y+25))

            if array[row][col] == 2 and start_point == (0, 0):
                if max_blocks > (filled_blocks + space_blocks):
                    filled_blocks += 1
                start_point = (x-(blocksize/2)+50, y-(blocksize/2)+50)
                
            if array[row][col] == 0 and mess_array_fill != False:
                    if max_blocks > (filled_blocks + space_blocks):
                        mess_pos_array.append([x, y])
                        space_blocks += 1
                    elif max_blocks == (filled_blocks + space_blocks):
                        mess_array_fill = False

    return space_blocks, filled_blocks, start_point, mess_pos_array, mess_array_fill
 
def drawgridlevels(max_blocks, space_blocks, filled_blocks, activemap):
    max_blocks, space_blocks, filled_blocks = max_blocks, space_blocks, filled_blocks
    blocksize = 50
    array = activemap

    for row in range(len(array)):
        for col in range(len(array[row])):
            x = col * blocksize
            y = row * blocksize
            block = Block(x, y, blocksize, blocksize, WINDOW)
            if int(array[row, col] == 1):
                if max_blocks > (filled_blocks + space_blocks):
                    filled_blocks += 1
                block.draw(black)
                block_alphasurface = pg.Surface((blocksize, blocksize), pg.SRCALPHA)
                pg.draw.rect(block_alphasurface, aplha_black, block_alphasurface.get_rect())
                WINDOW.blit(block_alphasurface, (x, y+25))

            if int(array[row, col] == 2):
                #checks for startpos
                blocksize = 50


def drawgridmaker(mx, my, save=None):
    #print("drawing {}".format(activemap))
    blocksize = 50
    mouse_buttons = pg.mouse.get_pressed()
    for row in range(len(activemap)):
        for col in range(len(activemap[row])):
            x = col * blocksize
            y = row * blocksize
            rect = pg.Rect(x, y, blocksize, blocksize)
            if mx > x and mx < (x+blocksize) and my > y and my < (y+blocksize):
                pg.draw.rect(WINDOW, red, rect)
                if mouse_buttons[0]:
                    activemap[row][col] = 1
                if mouse_buttons[1]:
                    activemap[row][col] = 2
                if mouse_buttons[2]:
                    activemap[row][col] = 0

            elif activemap[row][col] == 2:
                pg.draw.rect(WINDOW, green, rect)
            elif activemap[row][col] == 1:
                pg.draw.rect(WINDOW, white, rect)
            elif activemap[row][col] == 0:
                pg.draw.rect(WINDOW, white, rect, 1)
    if save:
        return activemap

#tkinter window that asks how you want to name your level
def get_level_name():
    def on_submit():
        name = entry.get()
        window.destroy()
        name_var.set(name)

    window = tk.Tk()
    window.title("Enter Name")
    
    # get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # place window in the center of the screen
    x = (screen_width - 150) // 2
    y = (screen_height - 150) // 2

    # set the window size and position
    window.geometry(f"250x150+{x}+{y}")

    label = tk.Label(window, text="Type level name here:")
    label.pack()

    entry = tk.Entry(window)
    entry.pack()

    button = tk.Button(window, text="Enter", command=on_submit)
    button.pack()

    name_var = tk.StringVar()
    window.mainloop()

    return name_var.get()

#tkinter window that pops-up when you want to quit the mapmaker to check if you really want to quit
def show_confirmation_popup():
    def quit_clicked():
        nonlocal result
        result = True
        window.destroy()

    def cancel_clicked():
        nonlocal result
        result = False
        window.destroy()

    window = tk.Tk()
    window.title("Confirmation")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - 200) // 2
    y = (screen_height - 150) // 2
    
    # Set the window size
    window.geometry(f"200x150+{x}+{y}")

    message = "Are you sure you want to quit?"
    label = tk.Label(window, text=message)
    label.pack(pady=20)

    quit_button = tk.Button(window, text="Quit", command=quit_clicked)
    quit_button.pack(side="left", padx=10)

    cancel_button = tk.Button(window, text="Cancel", command=cancel_clicked)
    cancel_button.pack(side="right", padx=10)

    result = None
    window.mainloop()

    return result

#tkinter window for letting the player choose the level they want to play
def get_selected_level():
    folder_path = os.path.dirname(os.path.abspath(__file__))
    levels = os.listdir(folder_path + "/maps/CustomMaps/")

    selected_level = None

    def select_file(level_name):
        print("a level was selected")
        nonlocal selected_level
        selected_level = level_name
        window.destroy()
        #return selected_level
    
    def on_close():
        selected_level = False
        print("windows closing..... ")
        window.destroy()
        return selected_level

    window = tk.Tk()
    window.title("Levels")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - 200) // 2
    y = (screen_height - 150) // 2
    
    # Set the window size
    window.geometry(f"200x150+{x}+{y}")

    window.protocol("WM_DELETE_WINDOW", on_close)

    for level_name in levels:
        button = tk.Button(window, text=level_name, command=lambda name=level_name: select_file(name))
        button.pack(padx=10, pady=5)

    window.mainloop()

    return selected_level

# copies the numpy array from your current level wich is the testlvl_mapmaker.npy file and pastes it into a new file that has the name you have given it
def copy_and_paste_file(source_path, destination_path):
    print(str(source_path))
    try:
        # Load the numpy array from the source file
        source_array = np.load(str(source_path))
        
        # Save the numpy array to the destination file
        np.save(str(destination_path), source_array)
        
        print(f"File copied and pasted successfully as: {destination_path}")
    except FileNotFoundError:
        print("Source file not found.")
    except PermissionError:
        print("Permission denied. Unable to copy and paste the file.")

# save the changes you made in the mapmaker before thos get loaded in your new file
def save_current_map(data, destination_path):
    try:
        # Save the numpy array to the destination file
        np.save(destination_path, data)
        
        print(f"File created and saved successfully as: {destination_path}")
    except PermissionError:
        print("Permission denied. Unable to create and save the file.")

# these 2 functions are used for rendering the texts,
# dont ask me how because it costs me to much of my own sanity to figure out


def flatten_text(text):
    flattened_text = []

    for item in text:
        if isinstance(item, list):
            flattened_text.extend(flatten_text(item))
        else:
            flattened_text.append(item)

    return flattened_text


def render_texts(text, text_posX, text_posY, word_spacing):
    text_posY_current = text_posY
    for line in text:
        words = line.split()
        text_posX_current = text_posX
        for word in words:
            text_surface = font.render(word, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.x = text_posX_current
            text_rect.y = text_posY_current
            WINDOW.blit(text_surface, text_rect)
            text_posX_current += text_rect.width + word_spacing
        text_posY_current += text_rect.height

first_mess = True
mess = None
def place_mess(mess_pos_array, player, first_mess):
    global mess

    if first_mess:
        mess = Mess(mess_pos_array, WINDOW, img_mess)
        mess.position()
        mess.handle_collision(player)
        mess.draw()
        first_mess = False

    if first_mess == False and mess.handle_collision(player) == True:
        mess.position()

    mess.draw()
    return first_mess

def get_npy_files():
    directory = 'maps/CustomMaps'
    npy_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".npy"):
                if file != "testlvl.npy" or file != "testlvl_mapmaker.npy":
                    npy_files.append(file)
    return npy_files

running = True
runmaps = False
runmapmaker = False
runplay = False
mainmenu = True
spawn_player = True
title_height = 0
title_down = False
start = False
instructions = False
credits = False
current_text = 0
text_posX = 75
text_posY = 200
word_spacing = 7
start_battery = False
turn_player_off = True
mess_array_fill = True
activemap, path_to_activemap = loadmap(runmapmaker)
battery_turn = False
levels = False
fetchlevels = True
activelevel = 0
maxlevel = 0
activelevelarray = []
activelevelarray_path = ""
breakloop = False

while running:
    while runmapmaker:
        keys = pg.key.get_pressed()
        WINDOW.fill((black))
        mouse = pg.mouse.get_pos()
        drawgridmaker(mouse[0], mouse[1])

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                a = 1

        if keys[pg.K_s]:
            save = True
            curent_map_data = drawgridmaker(mouse[0], mouse[1], save)
            save_current_map(curent_map_data, path_to_activemap)
            level_name = get_level_name()
            save_map = root_dir + "/maps/CustomMaps/{}.npy".format(level_name)
            copy_and_paste_file(path_to_activemap, save_map)
        if keys[pg.K_q]:
            confirmation_result = show_confirmation_popup()
            if confirmation_result is not None:
                if confirmation_result and runmapmaker == True:
                    runmapmaker = False
                    runmaps = True
                    save = True
                else:
                    # does nothing, gives error when no code exists in this statement
                    print("i dunno what went wrong")

        if event.type == pg.QUIT:
            runmapmaker = False
            runmaps = True

        savemaptext = font.render('press S to save and Q to quit', True, grey)
        WINDOW.blit(savemaptext, (0, WINDOW_HEIGHT-100))
        pg.display.flip()

    while runplay:
        Clock.tick(FPS)
        WINDOW.fill((white))
        WINDOW.blit(img_background, (0, 0))
        keys = pg.key.get_pressed()
        if spawn_player and start_point != (0, 0):
            player = Player("player", start_point[0], start_point[1], player_radius,player_color, WINDOW, player_images_off, player_images_on)
            battery = Battery(batteryX, batteryY, WINDOW, battery_images)
            spawn_player = False
            battery_life = 1
            battery_timer = time.time()
            start_battery = True

        if spawn_player == False:
            # added all vars to be returned, used to be only start_point. apperently this works and mess_array_fill is now finally False
            space_blocks, filled_blocks, start_point, mess_pos_array, mess_array_fill = drawgrid(max_blocks, space_blocks, filled_blocks, mess_array_fill, start_point,  selected_level, mess_pos_array, player)

            if battery_life < 5:
                player.move((keys[pg.K_RIGHT] - keys[pg.K_LEFT]) *
                            speed, (keys[pg.K_DOWN] - keys[pg.K_UP]) * speed)
            else:
                if turn_player_off:
                    player.change_color()
                    player.draw()
                    turn_player_off = False
                battery_timer = time.time()
            player.draw()
        else:
            space_blocks, filled_blocks, start_point, mess_pos_array, mess_array_fill = drawgrid(max_blocks, space_blocks, filled_blocks, mess_array_fill, start_point, selected_level, mess_pos_array)

        if mess_array_fill == False:
            first_mess = place_mess(mess_pos_array, player, first_mess)


        if start_battery == True and time.time() - battery_timer > 5:
            battery_life += 1
            battery_timer = time.time()

        if start_battery:
            if frame_count % 30 == 0:
                battery_turn = not battery_turn
                battery.battery_life(battery_life, battery_turn)
            battery.draw()

        if keys[pg.K_q]:
            battery_timer = time.time()
            battery_life = 1
            mainmenu = True
            runplay = False

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                a = 1

        if event.type == pg.QUIT:
            pg.quit()
        frame_count += 1
        pg.display.flip()

    while levels:
        if(fetchlevels):
            list_of_levels = get_npy_files()
            maxlevel = len(list_of_levels)
            fetchlevels = False
            activelevelarray, activelevelarray_path = loadmap(runmapmaker, list_of_levels[activelevel])
        else:
            WINDOW.blit(img_background, (0, 0))
            level_texts = font.render(list_of_levels[activelevel], True, (255,255,255))
            mouse = pg.mouse.get_pos()
            keys = pg.key.get_pressed()

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    pg.quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if arrow_rightButton.handle_collision():
                        if activelevel == maxlevel-1:
                            activelevel = 0
                        else: 
                            activelevel += 1
                        activelevelarray, activelevelarray_path = loadmap(runmapmaker, list_of_levels[activelevel])

                    if arrow_leftButton.handle_collision():
                        if activelevel == 0:
                            activelevel = maxlevel-1
                        else: 
                            activelevel -= 1
                        activelevelarray, activelevelarray_path = loadmap(runmapmaker, list_of_levels[activelevel])

            drawgridlevels(max_blocks, space_blocks, filled_blocks, activelevelarray)
            WINDOW.blit(level_texts, (WINDOW_WIDTH/2 - level_texts.get_width() // 2, 20 - level_texts.get_height() // 2))
            for arrow in arrows:
                arrow.handle_collision()
                arrow.draw()
                

            if keys[pg.K_q] or event.type == pg.QUIT:
                levels = False
                runmaps = True
                fetchlevels = True   
            
            #print(activelevel, maxlevel,list_of_levels,list_of_levels[activelevel])
            pg.display.flip()

    while instructions:
        WINDOW.blit(img_background, (0, 0))
        mouse = pg.mouse.get_pos()
        keys = pg.key.get_pressed()

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if arrow_rightButton.handle_collision():
                    if current_text == len(instruction_texts_array)-1:
                        current_text = 0
                    else:
                        current_text += 1

                if arrow_leftButton.handle_collision():
                    if current_text == 0:
                        current_text = len(instruction_texts_array)-1
                    else:
                        current_text -= 1
        flattened_texts = flatten_text(instruction_texts_array[current_text][0])
        render_texts(flattened_texts, text_posX, text_posY, word_spacing)
        WINDOW.blit(instruction_texts_array[current_text][1],
                    (instructions_title_posX, instructions_title_posY))
        for arrow in arrows:
            arrow.handle_collision()
            arrow.draw()

        if keys[pg.K_q] or event.type == pg.QUIT:
            mainmenu = True
            instructions = False
        pg.display.flip()

    while credits:
        WINDOW.blit(img_background, (0, 0))
        keys = pg.key.get_pressed()
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()

        flattened_texts = flatten_text(credits_text)
        render_texts(flattened_texts, text_posX, text_posY-100, word_spacing)

        if keys[pg.K_q]:
            mainmenu = True
            credits = False

        pg.display.flip()

    while mainmenu:
        Clock.tick(FPS)
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

            if event.type == pg.QUIT:
                pg.quit()

            if event.type == pg.MOUSEBUTTONDOWN:

                if quitButton.handle_collision() and start:
                    pg.quit()

                if mapsButton.handle_collision() and start:
                    runmaps = True
                    mainmenu = False
                    start = False

                if playButton.handle_collision() and start:
                    selected_level = get_selected_level()
                    if (selected_level == False):
                        print("closed selection window without loading level.....gameplay loop:{}".format(runplay))
                        breakloop = True
                        runplay = False
                    elif (selected_level and breakloop == False):
                        print("level found")
                        selected_level, path_to_selected_level = loadmap(runmapmaker, selected_level)
                        mainmenu = False
                        runplay = True
                        print("an level loaded succesfully.... starting gameplay loop:{}".format(runplay))
                        
                #startbutton stays here otherwise bugs might appear
                if startButton.handle_collision():
                    start = True

                if instructionsButton.handle_collision() and start:
                    instructions = True

                if creditsButton.handle_collision() and start:
                    credits = True

        if start == False and runmaps == False:
            startButton.handle_collision()
            startButton.draw()
        if start and runmaps == False:
            for button in buttons:
                button.handle_collision()
                button.draw()

        mouse = pg.mouse.get_pos()

        # end event handling
        pg.display.flip()

    while runmaps:
        Clock.tick(FPS)
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

            if event.type == pg.QUIT:
                pg.quit()

            if event.type == pg.MOUSEBUTTONDOWN:

                if backButton.handle_collision() and runmaps:
                    runmaps = False
                    mainmenu = True
                    start = True

                if mapmakerButton.handle_collision() and runmaps:
                    runmaps = False
                    runmapmaker = True

                if levelsButton.handle_collision() and runmaps:
                    runmaps = False
                    levels = True

        if runmaps:
            for button in map_buttons:
                button.handle_collision()
                button.draw()

        mouse = pg.mouse.get_pos()

        # end event handling
        pg.display.flip()
