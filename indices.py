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
    CREATED = 1
    PASSED = 0
    EMPTY_CREDENTIALS = -1
    USER_EXISTS = -2
    NO_SAVE = -3
    PASSWORD_INCORRECT = -4

class Buildings:
    EMPTY = 0
    TOWNHALL = 1
    CHURCH = 2
