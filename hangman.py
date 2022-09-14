import os
import time
from os.path import exists
from termcolor import colored

# Game state ("intro", "menu", "game", "dead", "exit)
app_state = "intro"

# Termcolor text colors
# grey
# red
# green
# yellow
# blue
# magenta
# cyan
# white

# Set of letters
# They keep the color of the text.
# cyan - default color (letter still not used)
# red - fail color (letter used, but it was a miss)
# green - success color (letter used, and it was a correct answer)
letters = {
    "A": "cyan",
    "Ą": "cyan",
    "B": "cyan",
    "C": "cyan",
    "Ć": "cyan",
    "D": "cyan",
    "E": "cyan",
    "Ę": "cyan",
    "F": "cyan",
    "G": "cyan",
    "H": "cyan",
    "I": "cyan",
    "J": "cyan",
    "K": "cyan",
    "L": "cyan",
    "Ł": "cyan",
    "M": "cyan",
    "N": "cyan",
    "Ń": "cyan",
    "O": "cyan",
    "Ó": "cyan",
    "P": "cyan",
    "Q": "cyan",
    "R": "cyan",
    "S": "cyan",
    "Ś": "cyan",
    "T": "cyan",
    "U": "cyan",
    "V": "cyan",
    "W": "cyan",
    "X": "cyan",
    "Y": "cyan",
    "Z": "cyan",
    "Ź": "cyan",
    "Ż": "cyan",
}


# Clear console (useful for animation and game)
def clear_console():
    # Windows only
    if os.name == "nt":
        system_clear = "cls"
    # Mac and Linux
    else:
        system_clear = "clear"
    os.system(system_clear)


# Check if OS is using "\" backslash (Windows only) or "/" forward slash (Linux, Mac)
def get_os_slash():
    # Windows only
    if os.name == "nt":
        return "\\"
    # other os
    else:
        return "/"


# Return a number of frames in animation.
# Every frame is stored in different .txt file
# Files with frames of the ASCII animation must be named with number if the frame in postfix.
# For example if file_name is "animation", then function is looking for files
# with name "animation0.txt", "animation1.txt", "animation2.txt" and so on.
# Function is checking "Data" folder and check if files exists.
# Function know the number of animation if they are named in correct way.
# Parameter:
# file_name: name of frame file
def check_frames_count(file_name):
    slash = get_os_slash()
    file_exists = True
    file_index = 0
    while file_exists:
        catalog = os.getcwd()
        file_exists = exists(f"{catalog}{slash}Data{slash}{file_name}{file_index}.txt")
        file_index += 1
    return file_index-1


# Load logo animations from file and return list of the strings
# Every string is frame of the ASCII animation
def load_animation(file_name):
    slash = get_os_slash()
    animation_strings = []

    frames_count = check_frames_count(file_name)

    for file_index in range(0, frames_count):
        catalog = os.getcwd()
        logo_file = open(f"{catalog}{slash}Data{slash}{file_name}{file_index}.txt", "rt")
        animation_strings.append(logo_file.read())
        logo_file.close()
    return animation_strings


# Parameters:
# animations: ASCII animations list (literally a list of strings)
# animation_time: duration of animation (in seconds)
# logo_color: selected color of the animation
def play_animation(animations, animation_time, animation_color):
    animation_interval = animation_time / len(animations)
    clear_console()
    for current_animation in animations:
        clear_console()
        print(f"{colored(current_animation, animation_color)}")
        time.sleep(animation_interval)


def show_static(animation, animation_color):
    print(f"{colored(animation, animation_color)}")


def use_letter(letter):
    sign = letter.upper()
    print(sign)
    print(letters[sign])
    letters[sign] = "red"


def draw_letters_ui():
    use_letter("A")
    use_letter("B")
    use_letter("C")
    print(letters.get("A"))
    alphabet = ""
    for sign in letters:
        alphabet += f"[{sign}] "
    print("Possible letters:")

    guit_text = f"{colored(alphabet, 'cyan')}"
    print(guit_text)


# Animated intro.
def intro_state():
    clear_console()
    intro_animation = load_animation("logo")
    time.sleep(0.5)
    play_animation(intro_animation, 1.7, "red")
    global app_state
    app_state = "menu"
    hangman_game()


def draw_menu(logo_color):
    clear_console()
    menu_text = {
        "[1] NEW GAME - EASY": "green",
        "[2] NEW GAME - NORMAL": "yellow",
        "[3] NEW GAME - HARD": "red",
        "[4] NEW GAME - PERFECT": "magenta",
        "[E] EXIT": "white"
    }
    menu_logo = load_animation("logo")
    show_static(menu_logo[len(menu_logo)-1], logo_color)
    print(3 * '\n')
    menu_space = 22 * ' '

    for menu_item in menu_text:
        print(f"{menu_space}{colored(menu_item, menu_text.get(menu_item))}")


# Everything what happen during menu
def menu_state():
    global app_state
    draw_menu("cyan")

    menu_space = 22 * ' '
    print("\n")
    player_selection = str(input(f"{menu_space}Your selection: "))
    fade_time = 1

    while True:
        match player_selection:
            case "1":
                color = "green"
                draw_menu(color)
                time.sleep(fade_time)
                app_state = "game"
                hangman_game(color)
                break
            case "2":
                color = "yellow"
                draw_menu(color)
                time.sleep(fade_time)
                app_state = "game"
                hangman_game(color)
                break
            case "3":
                color = "red"
                draw_menu(color)
                time.sleep(fade_time)
                app_state = "game"
                hangman_game(color)
                break
            case "4":
                color = "magenta"
                draw_menu(color)
                time.sleep(fade_time)
                app_state = "game"
                hangman_game(color)
                break
            case "E" | "e":
                color = "white"
                draw_menu(color)
                time.sleep(fade_time)
                app_state = "exit"
                hangman_game(color)
                break
            case _:
                print("\n")
                print(f"{menu_space}{ colored('WRONG SELECTION - Use 1-4 or E', 'red')}")
                time.sleep(2.5)
                menu_state()
                break


# Everything what happen, when player is playing.
def game_state(color):
    hangman_animation = load_animation("hangman")
    play_animation(hangman_animation, 8, color)
    global app_state

    app_state = "dead"
    hangman_game()


def dead_state():
    hangman_animation = load_animation("dead")
    play_animation(hangman_animation, 2,  "green")

    global app_state
    app_state = "menu"
    hangman_game()


# Game loop
def hangman_game(color="red"):
    match app_state:
        case "intro":
            intro_state()
        case "menu":
            menu_state()
        case "game":
            game_state(color)
        case "dead":
            dead_state()
        case "exit" | _:
            clear_console()


if __name__ == '__main__':
    hangman_game()

    # logo_animations = load_animation("logo")
    # hangman_animation = load_animation("hangman")
    # dead_animation = load_animation("dead")
    #
    # show_animation(logo_animations, 2.5, "red")
    # show_animation(hangman_animation, 8, "cyan")

    # max_lives = 5
    # for current_lives in reversed(range(0, max_lives+1)):
    #     clear_console()
    #     if current_lives > 0:
    #         print(f"Lives: {current_lives * ' ❤ '}")
    #     else:
    #         print(f"{colored('YOU ARE DEAD!', 'red')} {' ☠ '} ")
    #     time.sleep(1)
    # time.sleep(2)
    # show_animation(dead_animation, 1, "green")
