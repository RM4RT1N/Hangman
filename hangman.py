import os
from time import sleep
from termcolor import colored
import random
import sys

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
                exit()
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


def dev_menu():
    if "--dev" in sys.argv:
        return True

# Show game hud during game_state() (with an ASCII art on the right side)
def show_hud(frame,w_tab,u_tab,s_tab,num_lives):
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
                if dev_menu():
                    hud = f"{space}{show_word(s_tab)}"
                    hud_color = "blue"
            case 11:
                hud = f"{space}{show_word(w_tab)}"
                hud_color = "blue"
            case 12:
                heart = "\u2665"
                hud = f"{space}Lives: {num_lives * heart}"
            case 13:
                hud = f"{space}Lives: {num_lives}"
            case 15:
                hud = f"{space}Used letters: "
                hud_color = "yellow"
            case 16:
                hud = f"{space}{show_word(u_tab)}"
                hud_color = "red"
        hud = correct_line(hud)
        line = frame[line_nr]
        # line = hud + line
        print(f"{colored(hud, hud_color)}", end='')
        print(f"{colored(line, current_level['color'])}", end='')


def delete_last_line():
    "Use this function to delete the last line in the STDOUT"
    #cursor up one line
    sys.stdout.write('\x1b[1A')
    #delete last line
    sys.stdout.write('\x1b[2K')




def number_of_frame(curr_lives):
    current_level = game_config["level"]
    lives = current_level["lives"]
    return lives-curr_lives


def input_char():
    letter = input()
    return letter
 

def check_char(tab):
    while True:
        letter = input_char()
        if len(letter) == 1 and letter.isalpha() and letter not in tab:
            break
        elif letter.lower()=='exit':
            menu_state()
            break
        else:
            print('Add a valid letter ')
            sleep(2)
            delete_last_line()
            delete_last_line()
            
    return letter


def start_word(word):
    temp_table = []
    for i in range(len(word)):
        if word[i] == ' ':
            temp_table.append(" ")
        else:
            temp_table.append("_") 
    return temp_table
 
 
def create_table_of_word (word):
    solid_table = []
    for i in range(len(word)):
        solid_table.append(word[i])
    return solid_table


def check_lives(lives):
    if lives > 0:
        return True
    return False


def count_lives(letter, solid_table, uses_table, lives):
    low_letter = letter.lower()
    up_letter = letter.upper()
    if up_letter in solid_table or up_letter in uses_table:
        return lives
    elif low_letter in solid_table or low_letter in uses_table:
        return lives  
    else:
        lives -= 1 
        return lives


def load_data():
    with open('countries-and-capitals.txt', 'r') as file:
 
        country = random.choice(file.readlines())
        new_country = country.split(' | ')
        text = new_country[0].lstrip(" ").rstrip(" ")
    return text


def show_word(tab):
    word = ''
    for i in range(len(tab)):
        temp_word =''.join(tab[i])
        word = word + temp_word
        if i != len(tab)-1:
            word = f'{word} ' 
    return word


def game_state():
    anim = load_animation("hangman")
    table_of_used_word = []
    word = load_data()
    input_table = create_table_of_word(word)
    work_table = start_word(word)
    current_level = game_config["level"]
    lives = current_level["lives"]
    current_level = game_config["level"]
    frames = current_level["frames"]
    
    while True:
        clear_console()
        show_hud(anim[frames[number_of_frame(lives)]],work_table,table_of_used_word,input_table,lives)
        print("Hint: Write 'exit' instead of letter to go back to main menu")
        while work_table != input_table:
            
            letter = check_char(table_of_used_word)
            if letter.lower() == 'exit':
                break
            lives = count_lives(letter, input_table, table_of_used_word, lives)
            if not check_lives(lives):
                show_hud(anim[frames[number_of_frame(lives)]],work_table,table_of_used_word,input_table,lives)
                print(f'You lose. Correct word is {word}')
                input(f"Press to start new game") 
                menu_state()
                break
            for i in range(len(input_table)):
                while  input_table[i].lower() == letter.lower():
                    work_table[i] = input_table[i]
                    break          
            if not letter in table_of_used_word:
                table_of_used_word.append(letter)  
                break        
        if work_table == input_table:
            break

    print(f'Correct word :') 
    print(*input_table)
    print(f'You win') 
    input(f"Press to start new game")       
    menu_state()


if __name__ == '__main__':
    intro_state()