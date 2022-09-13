import os
import time
from os.path import exists
from termcolor import colored

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
        file_exists = exists(f".{slash}Data{slash}{file_name}{file_index}.txt")
        file_index += 1
    return file_index-1


# Load logo animations from file and return list of the strings
# Every string is frame of the ASCII animation
def load_animation(file_name):
    slash = get_os_slash()
    logo_strings = []

    frames_count = check_frames_count(file_name)

    for file_index in range(0, frames_count):
        logo_file = open(f".{slash}Data{slash}{file_name}{file_index}.txt", "rt")
        logo_strings.append(logo_file.read())
        print(logo_strings[file_index])
        logo_file.close()
    return logo_strings


# Parameters:
# animations: ASCII animations list (literally a list of strings)
# animation_time: duration of animation (in seconds)
# logo_color: selected color of the animation
def show_animation(animations, animation_time, animation_color):
    animation_interval = animation_time / len(animations)

    clear_console()
    time.sleep(1)

    for current_logo_text in animations:
        clear_console()
        print(f"{colored(current_logo_text, animation_color)}")
        time.sleep(animation_interval)


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


# Game loop
def hangman_game():
    clear_console()
    draw_letters_ui()
    time.sleep(1)

    logo_animations = load_animation("logo")
    hangman_animation = load_animation("hangman")
    dead_animation = load_animation("dead")

    show_animation(logo_animations, 2.5, "red")
    show_animation(hangman_animation, 8, "cyan")

    max_lives = 5
    for current_lives in reversed(range(0, max_lives+1)):
        clear_console()
        if current_lives > 0:
            print(f"Lives: {current_lives * ' ❤ '}")
        else:
            print(f"{colored('YOU ARE DEAD!', 'red')} {' ☠ '} ")
        time.sleep(1)
    time.sleep(2)
    show_animation(dead_animation, 1, "green")


if __name__ == '__main__':
    hangman_game()
