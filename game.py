import os
from time import sleep
from termcolor import colored


# --------------------------------------------------
# What are we used:
# --------------------------------------------------
# Loops:
# for loops and while loops
# --------------------------------------------------
# Data types:
# dictionary for game settings and level options
# lists to store animation and animation frames, and some difficulty level options
# --------------------------------------------------
# Imported functionality:
# os for getcwd(), os.path.exists() and os.name
# os.system() to clear a terminal
# colored() from termcolor
# time.sleep from time to froze a terminal for a moment (useful for animation)
# --------------------------------------------------
# String functionality:
# isalpha() to check if letter is a part of the alphabet
# lower() to make a string lower case (in game menu for example)
# rsptrip()
# lstrip()
# --------------------------------------------------


level_easy = {
    "color": "green",
    "lives": 8,
    "frames": [0, 1, 2, 3, 4, 5, 6, 7, 8]
}

level_normal = {
    "color": "yellow",
    "lives": 6,
    "frames": [0, 1, 2, 4, 6, 7, 8]
}

level_hard = {
    "color": "red",
    "lives": 3,
    "frames": [0, 5, 7, 8]
}

level_perfect = {
    "color": "magenta",
    "lives": 1,
    "frames": [0, 8]
}

game_config = {
    "level": level_easy,
    "logo_color": "red"
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
    file_exists = True
    file_index = 0
    while file_exists:
        catalog = os.getcwd()
        file_exists = os.path.exists(f"{catalog}/Data/{file_name}{file_index}.txt")
        file_index += 1
    return file_index - 1


# Load logo animations from file and return list of the strings
# Every string is frame of the ASCII animation
def load_animation(file_name):
    animation_strings = []

    frames_count = check_frames_count(file_name)

    for file_index in range(0, frames_count):
        catalog = os.getcwd()
        logo_file = open(f"{catalog}/Data/{file_name}{file_index}.txt", "rt", encoding='utf8')
        animation_strings.append(logo_file.readlines())
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
        for frame in current_animation:
            print(f"{colored(frame, animation_color)}", end='')

        sleep(animation_interval)


# Show a static ASCII art frame
def show_static(frame, animation_color):
    for line in frame:
        print(f"{colored(line, animation_color)}", end='')


# Draw game menu
def draw_menu():
    clear_console()
    menu_text = {
        "[1] NEW GAME - EASY": "green",
        "[2] NEW GAME - NORMAL": "yellow",
        "[3] NEW GAME - HARD": "red",
        "[4] NEW GAME - PERFECT": "magenta",
        "[E] EXIT": "white"
    }
    menu_logo = load_animation("logo")
    show_static(menu_logo[len(menu_logo) - 1], game_config["logo_color"])

    print(3 * '\n')
    menu_space = 22 * ' '

    for menu_item in menu_text:
        print(f"{menu_space}{colored(menu_item, menu_text.get(menu_item))}")


# Show the animation before game start
def intro_state():
    clear_console()
    intro_animation = load_animation("logo")
    sleep(0.5)
    play_animation(intro_animation, 1.5, "red")
    menu_state()


# Everything what happen during menu
def menu_state():
    game_config["logo_color"] = "cyan"
    draw_menu()

    menu_space = 22 * ' '
    print("\n")
    player_selection = str(input(f"{menu_space}Your selection: "))
    fade_time = 1
    player_selection = player_selection.lower()
    while True:
        match player_selection:
            case "1":
                game_config["logo_color"] = "green"
                draw_menu()
                sleep(fade_time)
                game_config["level"] = level_easy
                game_state()
                break
            case "2":
                game_config["logo_color"] = "yellow"
                draw_menu()
                sleep(fade_time)
                game_config["level"] = level_normal
                game_state()
                break
            case "3":
                game_config["logo_color"] = "red"
                draw_menu()
                sleep(fade_time)
                game_config["level"] = level_hard
                game_state()
                break
            case "4":
                game_config["logo_color"] = "magenta"
                draw_menu()
                sleep(fade_time)
                game_config["level"] = level_perfect
                game_state()
                break
            case "e" | "exit":
                game_config["logo_color"] = "white"
                draw_menu()
                sleep(fade_time)
                clear_console()
                break
            case _:
                print(f"\n{menu_space}{colored('WRONG SELECTION - Use 1-4 or E', 'red')}")
                sleep(2.5)
                menu_state()
                break


# Make a line fit in selected size, fill by spaces or cut the string and return edited line
def correct_line(line, line_size=50):
    line_length = len(line)
    if line_length < line_size:
        missing_chars = line_size - line_length
        line += missing_chars * " "
    elif line_length > line_size:
        extra_lines = line_length - line_size
        line = line[:-extra_lines]
    return line


# Show game hud during game_state() (with an ASCII art on the right side)
def show_hud(frame):
    current_level = game_config["level"]
    lives = current_level["lives"]
    for line_nr in range(0, len(frame)):
        hud = ""
        space = 7 * ' '
        hud_color = "red"
        match line_nr:
            case 2:
                hud = f"{space}Guess a country"
                hud_color = "white"
            case 10:
                hud = f"{space} _ _ _ _  _ _ _"
                hud_color = "blue"
            case 12:
                heart = "\u2764\uFE0F"
                hud = f"{space}Lives: {lives * heart}"
            case 15:
                hud = f"{space}Used letters: "
                hud_color = "yellow"
            case 16:
                hud = f"{2 * ' '}[A] [B] [C] [D] [E] [F] [G] [H] [I] [J]"
                hud_color = "red"
        hud = correct_line(hud)
        line = frame[line_nr]
        # line = hud + line
        print(f"{colored(hud, hud_color)}", end='')
        print(f"{colored(line, current_level['color'])}", end='')


def game_state():
    anim = load_animation("hangman")
    letter = ""
    while not letter == "exit":
        clear_console()
        show_hud(anim[0])
        print("Hint: Write 'exit' instead of letter to go back to main menu")
        letter = input("Guess a letter A-Z: ")
    menu_state()


if __name__ == '__main__':
    intro_state()
