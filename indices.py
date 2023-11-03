class Locations:
    EXIT = -1 # Anytime V_LOC is set to -1, exit the game
    LOGIN = 0
    GAME = 1
    BUILDING = 2

class ButtonTypes:
    DEFAULT = 0
    CREATESAVE = 1
    LOADSAVE = 2
    EXIT = 3

class AccountFeedbacks:
    CREATED = 1
    PASSED = 0
    EMPTY_CREDENTIALS = -1
    USER_EXISTS = -2
    NO_SAVE = -3
    PASSWORD_INCORRECT = -4

class Buildings:
    names = ["empty", "town_hall", "church"] # List to hold namespaces for buildings to be added to a path, e.g. "Images/{town_hall}.png"
    EMPTY = 0
    TOWNHALL = 1
    CHURCH = 2
