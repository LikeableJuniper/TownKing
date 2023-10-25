import pygame as pg
from hashlib import sha256
import os
import json
from vectors import Vector

pg.init()
pg.font.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
font = pg.font.Font(None, 25)

V_LOC = 0
class Locations:
    EXIT = -1 # Anytime V_LOC is set to -1, exit the game
    LOGIN = 0
    GAME = 1

class ButtonTypes:
    DEFAULT = 0
    CREATESAVE = 1
    LOADSAVE = 2
    EXIT = 3

class AccountErrors:
    PASSED = 0
    EMPTY_CREDENTIALS = -1
    USER_EXISTS = -2
    NO_SAVE = -3
    PASSWORD_INCORRECT = -4

class Buildings:
    EMPTY = 0
    TOWNHALL = 1


class Rectangle:
    def __init__(self, pos: list[int, int], dimensions: list[int, int], color):
        self.pos = pos
        self.dimensions = dimensions
        self.color = color


class Label:
    def __init__(self, pos, text):
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
        self.onClick = onClick
        self.hovered = False
        self.buttonType = buttonType
    
    def __call__(self, **kwargs):
        if self.hovered:
            if self.buttonType == ButtonTypes.CREATESAVE:
                return createSave(kwargs["username"], kwargs["password"])
            elif self.buttonType == ButtonTypes.LOADSAVE:
                return loadSave(kwargs["username"], kwargs["password"])
            elif self.buttonType == ButtonTypes.EXIT:
                locChange(Locations.EXIT)
                return kwargs["gameData"], 0
            self.onClick()
        return None, 0
    
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


alphabet = [list("abcdefghijklmnopqrstuvwxyz"), list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")]
numbers = list("0123456789")

fieldSize = [20, 20]
fieldDimensions = [600, 600]
offset = Vector(100, 300)
buttonSize = [fieldDimensions[i]/fieldSize[i] for i in range(2)]

errorMessages = ["The password is incorrect.", "No save exists with that username.", "That username is already taken.", "Username or password cannot be empty."]

gameData: dict[str, str, list[list[Button]]] = {}


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
    dictField = gameData["field"]
    classField: list[list[Button]] = [[[None, Buildings.EMPTY]]*len(gameData["field"][0])]*len(gameData["field"])
    print(type(openBuilding))
    for x, column in enumerate(dictField):
        for y, elem in enumerate(column):
            classField[x][y][0] = Button(list(offset+[x*buttonSize[0], y*buttonSize[1]]), buttonSize, (255, 200, 140), (255, 200, 140), onClick=lambda: openBuilding([x, y]))

    return gameData, AccountErrors.PASSED


def locChange(newVal):
    global V_LOC
    V_LOC = newVal


def openBuilding(cords: list[int, int]):
    pass


def login(gameData):
    """Renders the login window. Returns gameData after closing."""
    global V_LOC
    inputFields: list[Input] = [Input([500, 150], [150, 50], (200, 200, 100), "Name: "), Input([800, 150], [150, 50], (200, 200, 100), "Pswd: ")]
    lastFocused = 0 # Index of last focused on input field

    labels: list[Label] = [Label([500, 310], "")]

    buttons: list[Button] = [Button((10, 10), (100, 30), (240, 30, 30), (240, 60, 60), "Exit", onClick=lambda: locChange(Locations.EXIT), buttonType=ButtonTypes.EXIT), Button((500, 250), (150, 50), (30, 210, 170), (130, 255, 225), "Create Account", buttonType=ButtonTypes.CREATESAVE), Button([800, 250], [150, 50], (15, 75, 170), (80, 115, 170), "Log in", buttonType=ButtonTypes.LOADSAVE)]

    while V_LOC == Locations.LOGIN:
        screen.fill((100, 100, 100))
        mousePos = pg.mouse.get_pos()
        lclick = pg.mouse.get_pressed()[0]

        for button in buttons:
            button.render(screen, mousePos)
            if lclick:
                errCode = button(username=inputFields[0].value, password=inputFields[1].value, gameData=gameData)
                if type(errCode[0]) == dict:
                    if button.buttonType == ButtonTypes.LOADSAVE:
                        V_LOC = Locations.GAME
                    return errCode[0]
                if errCode[1] < 0:
                    labels[0].changeText(errorMessages[errCode[1]])
        
        for label in labels:
            label.render(screen)
        
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


def mainGame(gameData):
    """Renders the main window. Returns gameData after closing."""
    global V_LOC
    inputFields: list[Input] = []
    lastFocused = 0 # Index of last focused on input field

    labels: list[Label] = []

    buttons: list[Button] = [Button((10, 10), (100, 30), (240, 30, 30), (240, 60, 60), "Exit", buttonType=ButtonTypes.EXIT)]

    while V_LOC == Locations.GAME:
        screen.fill((100, 100, 100))
        mousePos = pg.mouse.get_pos()
        lclick = pg.mouse.get_pressed()[0]

        for button in buttons:
            button.render(screen, mousePos)
            if lclick:
                errCode = button(gameData=gameData)
                if type(errCode[0]) == dict:
                    return errCode[0]
        
        for label in labels:
            label.render(screen)
        
        for column in gameData["field"]:
            for element in column:
                element.render(screen, mousePos)
        
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


locationFuncs = [login, mainGame]

while V_LOC > Locations.EXIT: # When V_LOC reaches -1, exit the game
    gameData = locationFuncs[V_LOC](gameData)

print(gameData)
