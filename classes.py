import pygame as pg
import math
class Player:
    def __init__(self, name, x, y, radius, color,WINDOW):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.WINDOW = WINDOW

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        pg.draw.circle(self.WINDOW, self.color, (self.x, self.y), self.radius)

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