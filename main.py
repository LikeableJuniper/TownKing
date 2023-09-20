import pygame as pg
from hashlib import sha256
import os

pg.init()
pg.font.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
font = pg.font.Font(None, 25)

V_LOC = 0
EXIT = -1 # Anytime V_LOC is set to -1, exit the game
LOGIN = 0
GAME = 1

alphabet = [list("abcdefghijklmnopqrstuvwxyz"), list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")]
numbers = list("0123456789")


def createSave(username, password):
    if not os.path.isdir("Saves"):
        os.mkdir("Saves")
    with open(f"Saves/{username}.json", "x") as f:
        f.write\
    ("""
        {
                   
        }
    """)


def locChange(newVal):
    global V_LOC
    V_LOC = newVal


class Rectangle:
    def __init__(self, pos: list[int, int], dimensions: list[int, int], color):
        self.pos = pos
        self.dimensions = dimensions
        self.color = color


class Button(Rectangle):
    def __init__(self, pos, dimensions, color, hoverColor, text="", onClick=None):
        super().__init__(pos, dimensions, color)
        self.hoverColor = hoverColor
        self.text = text
        self.onClick = onClick
        self.hovered = False
    
    def __call__(self):
        if self.hovered:
            self.onClick()
    
    def render(self, screen, mousePos):
        if self.pos[0] < mousePos[0] < self.pos[0] + self.dimensions[0] and self.pos[1] < mousePos[1] < self.pos[1] + self.dimensions[1]:
            pg.draw.rect(screen, self.hoverColor, self.pos+self.dimensions)
            self.hovered = True
        else:
            pg.draw.rect(screen, self.color, self.pos+self.dimensions)
            self.hovered = False

        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.pos[0]+self.dimensions[0]/2, self.pos[1]+self.dimensions[1]/2))
        screen.blit(text, text_rect)


class Input(Rectangle):
    def __init__(self, pos, dimensions, color, text):
        super().__init__(pos, dimensions, color)
        self.value = ""
        self.text = text
        self.lastInputs = [False] * 512
    
    def __call__(self, inputs):
        for i, char in enumerate(alphabet[int(inputs[pg.K_LSHIFT] or inputs[pg.K_RSHIFT])]):
            absIndex = pg.K_a + i
            if inputs[absIndex] and not self.lastInputs[absIndex]:
                self.value += char
        
        for i, num in enumerate(numbers):
            absIndex = pg.K_0 + i
            if inputs[absIndex] and not self.lastInputs[absIndex]:
                self.value += num
        
        if inputs[pg.K_BACKSPACE]:
            if not self.lastInputs[pg.K_BACKSPACE]:
                self.value = self.value[:-1]
        
        self.lastInputs = inputs

    
    def render(self, screen):
        pg.draw.rect(screen, self.color, self.pos+self.dimensions)

        # Rendering value of input
        text = font.render(self.value, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.pos[0]+self.dimensions[0]/2, self.pos[1]+self.dimensions[1]/2))
        screen.blit(text, text_rect)

        # Render pre-text
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(midright=(self.pos[0], self.pos[1]+self.dimensions[1]/2))
        screen.blit(text, text_rect)
    
    def checkClicked(self, mousePos: list[int, int]):
        if self.pos[0] < mousePos[0] < self.pos[0] + self.dimensions[0] and self.pos[1] < mousePos[1] < self.pos[1] + self.dimensions[1]:
            return True


def login():
    global V_LOC
    inputFields: list[Input] = [Input([500, 150], [150, 50], (200, 200, 100), "Name: "), Input([800, 150], [150, 50], (200, 200, 100), "Pswd: ")]
    lastFocused = 0 # Index of last focused on input field

    buttons: list[Button] = [Button((10, 10), (100, 30), (240, 30, 30), (240, 60, 60), "Exit", onClick=lambda: locChange(-1))]

    while V_LOC == LOGIN:
        screen.fill((100, 100, 100))
        mousePos = pg.mouse.get_pos()
        lclick = pg.mouse.get_pressed()[0]

        for button in buttons:
            button.render(screen, mousePos)
            if lclick:
                button()
        
        pressed = pg.key.get_pressed()
        for i, inputField in enumerate(inputFields):
            inputField.render(screen)
            if lclick:
                if inputField.checkClicked(mousePos):
                    lastFocused = i
            if lastFocused == i:
                inputField(pressed)


        #TODO: Add all game code here, none after input checks to prevent errors

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                V_LOC = -1


funcs = [login]

while V_LOC > EXIT: # When V_LOC reaches -1, exit the game
    funcs[V_LOC]()


