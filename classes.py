import pygame as pg
from indices import *
from vectors import Vector
import os
import json
from hashlib import sha256

pg.font.init()
font = pg.font.Font(None, 25)

alphabet = [list("abcdefghijklmnopqrstuvwxyz"), list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")]
numbers = list("0123456789")

fieldSize = [10, 10]
fieldDimensions = [600, 600]
offset = Vector(100, 100)
buttonMargin = [5, 5]
buttonSize = [fieldDimensions[i]/fieldSize[i]for i in range(2)]
buttonWidth = (Vector(buttonMargin) + Vector(buttonSize)).components


def createSave(username: str, password: str):
    """Function to create a save in "Saves/" directory. Returns data in the following format: (function value, error code)"""
    if not (username and password):
        return None, AccountErrors.EMPTY_CREDENTIALS
    if not os.path.isdir("Saves"):
        os.mkdir("Saves")
    if f"{username}.json" in os.listdir("Saves"):
        return None, AccountErrors.USER_EXISTS
    with open(f"Saves/{username}.json", "x") as f:
        field = []
        for x in range(fieldSize[0]):
            field.append([])
            for y in range(fieldSize[1]):
                field[x].append([None, Buildings.EMPTY]) # None is a placeholder for button element during main loop
        saveData = {"username": username, "password": str(sha256(bytes(password.encode())).hexdigest()), "field": field}
        json.dump(saveData, f)
    return None, AccountErrors.PASSED


def loadSave(username: str, password: str):
    """Function to load a save. Returns data in the following format: (function value, error code)"""
    if f"{username}.json" not in os.listdir("Saves"):
        return None, AccountErrors.NO_SAVE
    with open(f"Saves/{username}.json", "r") as f:
        gameData = json.load(f)
    if sha256(bytes(password.encode())).hexdigest() != gameData["password"]:
        return None, AccountErrors.PASSWORD_INCORRECT
    # Load button element in "field" as class from dict
    classField: list[list[Button]] = []
    for x in range(len(gameData["field"])):
        classField.append([])
        for y in range(len(gameData["field"][0])):
            classField[x].append([Button(list(offset+[x*buttonWidth[0], y*buttonWidth[1]]), buttonSize, (255, 200, 140), (255, 255, 160)), 0])
    
    gameData["field"] = classField

    print(gameData)

    return gameData, AccountErrors.PASSED


class Logic:
    def __init__(self, submitCredentials, renderField):
        """Class to hold booleans, defining whether or not a certain part of the loop should be executed during the "window" function."""
        self.submitCredentials: bool = submitCredentials
        self.renderField: bool = renderField


class Rectangle:
    def __init__(self, pos: list[int, int], dimensions: list[int, int], color):
        self.pos = pos
        self.dimensions = dimensions
        self.color = color


class Label:
    def __init__(self, pos, text):
        """Label with text disappearing after 3000 frames from last change."""
        self.pos = pos
        self.text = text
        self.lastChange = 0 # How many frames since the value was last changed
    
    def render(self, screen: pg.Surface):
        self.lastChange += 1
        if self.lastChange >= 3000: self.text = ""
        if self.text:
            screen.blit(font.render(self.text, False, (255, 50, 50)), self.pos)
    
    def changeText(self, newText):
        self.text = newText
        self.lastChange = 0


class Button(Rectangle):
    def __init__(self, pos=[], dimensions=[], color=(), hoverColor=(), text="", onClick=lambda: None, buttonType=ButtonTypes.DEFAULT, dictValue: dict=None):
        if dictValue:
            pos, dimensions, color, hoverColor, text, onClick, buttonType = dictValue.values()
        super().__init__(pos, dimensions, color)
        self.hoverColor = hoverColor
        self.text = text
        self.hovered = False
        self.buttonType = buttonType
    
    def __call__(self, **kwargs):
        """Calls on every click. If mouse cursor is hovering over current button, run its "onClick" function. Returns data in the following format: gameData, error code, new location(may stay unchanged)"""
        kwargs = kwargs["kwargs"]
        if self.hovered:
            if self.buttonType == ButtonTypes.CREATESAVE:
                return createSave(kwargs["username"], kwargs["password"]) + tuple([kwargs["location"]])
            elif self.buttonType == ButtonTypes.LOADSAVE:
                returnVal = loadSave(kwargs["username"], kwargs["password"]) + tuple([Locations.GAME])
                print(returnVal[0]["field"][0][0][0].pos)
                return returnVal
            elif self.buttonType == ButtonTypes.EXIT:
                return kwargs["gameData"], 0, Locations.EXIT
        return kwargs["gameData"], 0, kwargs["location"]

    def __repr__(self):
        return "Button"
    
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

