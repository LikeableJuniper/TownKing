import pygame as pg
from indices import *
from classes import *

pg.init()
pg.font.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

V_LOC = 0


errorMessages = ["The password is incorrect.", "No save exists with that username.", "That username is already taken.", "Username or password cannot be empty."]

# Format of "gameData" may vary during runtime so no useful type hints are available.
gameData = {}


def openBuilding(cords: list[int, int]):
    pass


def window(gameData, windowData, logic: Logic, lastFocused: int, lastFrameClick: bool):
    """Renders a window with specified data. Returns gameData after closing."""
    global V_LOC
    inputFields: list[Input] = windowData["inputFields"]
    if lastFocused >= len(inputFields):
        lastFocused = 0

    labels: list[Label] = windowData["labels"]

    buttons: list[Button] = windowData["buttons"]

    screen.fill((100, 100, 100))
    mousePos = pg.mouse.get_pos()
    lclick = pg.mouse.get_pressed()[0]

    for button in buttons:
        button.render(screen, mousePos)
        if lclick and not lastFrameClick:
            kwargs = {"gameData": gameData, "location": V_LOC}
            if logic.submitCredentials:
                kwargs["username"] = inputFields[0].value
                kwargs["password"] = inputFields[1].value

            errCode = button(kwargs=kwargs)
            V_LOC = errCode[2]
            gameData = errCode[0]
            if errCode[1] < 0:
                labels[0].changeText(errorMessages[errCode[1]])
            if errCode[1] == AccountErrors.CREATED:
                labels[0].changeText("Successfully created account.")

    for label in labels:
        label.render(screen)
        
    if logic.renderField:
        for x, column in enumerate(gameData["field"]):
            for y, row in enumerate(column):
                row[0].render(screen, mousePos)
        
    pressed = pg.key.get_pressed()
    for i, inputField in enumerate(inputFields):
        inputField.render(screen)
        if lclick:
            if inputField.checkClicked(mousePos):
                lastFocused = i
        if lastFocused == i:
            inputField(pressed)


    #TODO: Add all game code here, none after event checks to prevent errors

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            V_LOC = Locations.EXIT
        
    return gameData, lastFocused, lclick


locationLogic = [Logic(True, False), Logic(False, True)]
windowData = [
    {
        "inputFields": [
            Input([500, 150], [150, 50], (200, 200, 100), "Name: "),
            Input([800, 150], [150, 50], (200, 200, 100), "Pswd: ")
        ],
        "labels": [
            Label([500, 310], "")
        ],
        "buttons": [
            Button((10, 10), (100, 30), (240, 30, 30), (240, 60, 60), "Exit", buttonType=ButtonTypes.EXIT),
            Button((500, 250), (150, 50), (30, 210, 170), (130, 255, 225), "Create Account", buttonType=ButtonTypes.CREATESAVE),
            Button([800, 250], [150, 50], (15, 75, 170), (80, 115, 170), "Log in", buttonType=ButtonTypes.LOADSAVE)
            ]
    },
    {"inputFields": [

    ],
    "labels": [

    ],
    "buttons": [
        Button((10, 10), (100, 30), (240, 30, 30), (240, 60, 60), "Exit", buttonType=ButtonTypes.EXIT)
        ]
    }
]
lastFocused = 0
lastFrameClick = False

while V_LOC > Locations.EXIT: # When V_LOC reaches -1, exit the game
    gameData, lastFocused, lastFrameClick = window(gameData, windowData[V_LOC], locationLogic[V_LOC], lastFocused, lastFrameClick)


print(gameData)
