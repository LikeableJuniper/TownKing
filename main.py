import pygame as pg

pg.init()
pg.font.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
font = pg.font.Font(None, 25)

alphabet = list("abcdefghijklmnopqrstuvwxyz")


class Rectangle:
    def __init__(self, pos, dimensions, color):
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
    def __init__(self, pos, dimensions, color):
        super().__init__(pos, dimensions, color)
        self.value = ""
        self.lastInput: int = None
    
    def __call__(self, inputs):
        for i, char in enumerate(alphabet):
            if inputs[i+pg.K_a]:
                if self.lastInput != i:
                    self.value += char
                    self.lastInput = i
                
            elif self.lastInput == i:
                print("reset")
                self.lastInput = None
        
        # To save the backspace input to self.lastInput, -1 is used as pg.K_BACKSPACE returns a value already used by the letter "i"
        if inputs[pg.K_BACKSPACE]:
            if (self.lastInput != -1):
                self.value = self.value[:-1]
                self.lastInput = -1
        elif self.lastInput == -1:
            self.lastInput = None

    
    def render(self, screen):
        pg.draw.rect(screen, self.color, self.pos+self.dimensions)

        text = font.render(self.value, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.pos[0]+self.dimensions[0]/2, self.pos[1]+self.dimensions[1]/2))
        screen.blit(text, text_rect)


def exitGame():
    global playing
    pg.quit()
    playing = False

inputFields: list[Input] = [Input([500, 150], [150, 50], (200, 200, 100))]
lastFocused = 0 # Index of last focused on input field

buttons: list[Button] = [Button((10, 10), (100, 30), (240, 30, 30), (240, 60, 60), "Exit", onClick=exitGame)]

playing = True
while playing:
    screen.fill((100, 100, 100))
    mousePos = pg.mouse.get_pos()
    lclick = pg.mouse.get_pressed()[0]

    for button in buttons:
        button.render(screen, mousePos)
    
    pressed = pg.key.get_pressed()
    for i, inputField in enumerate(inputFields):
        inputField.render(screen)
        if lastFocused == i:
            inputField(pressed)


    #TODO: Add all game code here, none after input checks to prevent errors

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exitGame()
        
        # Buttons
        if lclick:
            for button in buttons:
                button()