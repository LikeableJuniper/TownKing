import pygame as pg

pg.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)


class Button:
    def __init__(self, pos, dimensions, defColor, hoverColor, onClick=None):
        self.pos = pos
        self.dimensions = dimensions
        self.defColor = defColor
        self.hoverColor = hoverColor
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
            pg.draw.rect(screen, self.defColor, self.pos+self.dimensions)
            self.hovered = False


def exitGame():
    global playing
    pg.quit()
    playing = False


buttons: list[Button] = [Button((10, 10), (100, 30), (240, 30, 30), (240, 60, 60), onClick=exitGame)]

playing = True
while playing:
    screen.fill((100, 100, 100))
    mousePos = pg.mouse.get_pos()
    lclick = pg.mouse.get_pressed()[0]

    for button in buttons:
        button.render(screen, mousePos)

    #TODO: Add all game code here, none after input checks to prevent errors

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exitGame()
        
        # Buttons
        if lclick:
            for button in buttons:
                button()