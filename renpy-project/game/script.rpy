# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

# define e = Character("Eileen")
define gbemu_d = gbemu.GBEmu("game.gb")

# The game starts here.

screen gbemu_screen():
    add gbemu_d at transform:
        align (0.5, 0.5)
        zoom gbemu.SCREEN_SCALE
        nearest True

label start:
    $ quick_menu = False
    window hide
    call screen gbemu_screen()
    return
