import pygame as pg
import math
import random
class Player:
    def __init__(self, name, x, y, radius, color, WINDOW, player_images_off, player_images_on):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.WINDOW = WINDOW 
        self.images_off = player_images_off
        self.images_on = player_images_on      
        self.images = self.images_on
        self.facing = self.images[0]  
        self.currently_facing = None

    def move(self, dx, dy):

        if dx == 0 and dy == 0:
            self.facing = self.facing
        elif dx > 0:
            self.facing = self.images[3]
            self.currently_facing = "right"
        elif dx < 0:
            self.facing = self.images[2]
            self.currently_facing = "left"
        elif dy > 0:
            self.facing = self.images[1]
            self.currently_facing = "down"
        elif dy < 0:
            self.facing = self.images[0]
            self.currently_facing = "up"

        self.x += dx
        self.y += dy

    def draw(self):
        self.WINDOW.blit(self.facing, (self.x - (self.radius), self.y - (self.radius)))

    def turn_off(self):
        self.images = self.images_off
        self.facing = self.images[0]
        if self.currently_facing == "right":
            self.facing = self.images[3]
        elif self.currently_facing == "left":
            self.facing = self.images[2]
        elif self.currently_facing == "down":
            self.facing = self.images[1]
        elif self.currently_facing == "up":
            self.facing = self.images[0]

    def handle_collision(player, block):

        closest_x = max(block.left, min(player.x, block.right))
        closest_y = max(block.top, min(player.y, block.bottom))
        distance = math.sqrt((player.x - closest_x)**2 + (player.y - closest_y)**2)
        
        if distance < player.radius:
            overlap_x = player.radius - abs(player.x - closest_x)
            overlap_y = player.radius - abs(player.y - closest_y)
            
            if overlap_x < overlap_y:
                if player.x < closest_x:
                    player.x -= overlap_x
                else:
                    player.x += overlap_x
            else:
                if player.y < closest_y:
                    player.y -= overlap_y
                else:
                    player.y += overlap_y

class Block:
    def __init__(self, x, y, width, height,WINDOW):
        self.rect = pg.Rect(x, y, width, height)
        self.WINDOW = WINDOW
        self.top = y
        self.left = x
        self.bottom = y + height
        self.right = x + width

    def draw(self,color):
        pg.draw.rect(self.WINDOW, color, self.rect)

class Button:
    def __init__(self, image, pressed_image, x, y, width, height,WINDOW):
        self.hover = False
        self.image = image
        self.pressed_image = pressed_image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.WINDOW = WINDOW

    def draw(self):
        if self.hover:
            self.WINDOW.blit(self.pressed_image, (self.x, self.y))
        else:
            self.WINDOW.blit(self.image, (self.x, self.y))

    def handle_collision(self):
        mouse = pg.mouse.get_pos()
        if self.x <= mouse[0] <= self.x+self.width and self.y <= mouse[1] <= self.y+self.height:
            self.hover = True
            return True
        else:
            self.hover = False
            return False
        
class Battery:
    def __init__(self, x, y,WINDOW, battery_images):
        self.x = x
        self.y = y
        self.WINDOW = WINDOW
        self.images = battery_images
        self.active_image = self.images[0]
        self.battery_1 = [battery_images[0], battery_images[1]]
        self.battery_2 = [battery_images[2], battery_images[3]]
        self.battery_3 = [battery_images[4], battery_images[5]]
        self.battery_4 = [battery_images[6], battery_images[7]]
        self.battery_5 = battery_images[8]
        self.facing = None

    def battery_life(self, battery_life, turn):
        self.turn = turn
        if battery_life == 1:
            if turn == False:
                self.facing = self.battery_1[0]
            else:
                self.facing = self.battery_1[1]
        elif battery_life == 2:
            if turn == False:
                self.facing = self.battery_2[0]
            else:
                self.facing = self.battery_2[1]
        elif battery_life == 3:
            if turn == False:
                self.facing = self.battery_3[0]
            else:
                self.facing = self.battery_3[1]
        elif battery_life == 4:
            if turn == False:
                self.facing = self.battery_4[0]
            else:
                self.facing = self.battery_4[1]
        elif battery_life == 5:
            self.facing = self.battery_5

    def draw(self):
        if self.facing:
            self.WINDOW.blit(self.facing, (self.x, self.y))

class Mess:
    def __init__(self, array, WINDOW, mess_images):
        self.WINDOW = WINDOW  
        #self.image = mess_images[random.randint(0, len(mess_images))]
        self.image = mess_images
        self.pos_array = array

    def position(self):
        pos = random.randint(0, len(self.pos_array)-1)
        self.x = self.pos_array[pos][0]
        self.y = self.pos_array[pos][1]
        self.top = self.y
        self.left = self.x
        self.bottom = self.y + 50
        self.right = self.x + 50
        self.middlex = self.x - (self.x / 2)
        self.middley = self.y - (self.y / 2)

    def draw(self):
        self.WINDOW.blit(self.image, (self.x, self.y))

    def handle_collision(mess, player):
        closest_x = max(mess.left, min(player.x, mess.right))
        closest_y = max(mess.top, min(player.y, mess.bottom))
        distance = math.sqrt((player.x - closest_x)**2 + (player.y - closest_y)**2)
        
        if distance < player.radius:
            return True
        return False
    
class Charger:
    def __init__(self, WINDOW, pos, image):
        self.WINDOW = WINDOW  
        self.image = image
        self.x = pos[0] - 25
        self.y = pos[1] - 25
        self.top = self.y
        self.left = self.x
        self.bottom = self.y + 50
        self.right = self.x + 50

    def draw(self):
        self.WINDOW.blit(self.image, (self.x, self.y))

    def handle_collision(charger, player):
        closest_x = max(charger.left, min(player.x, charger.right))
        closest_y = max(charger.top, min(player.y, charger.bottom))
        distance = math.sqrt((player.x - closest_x)**2 + (player.y - closest_y)**2)
        
        if distance < player.radius:
            return True
        return False
