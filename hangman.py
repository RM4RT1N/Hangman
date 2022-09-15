# PART 1
# display a menu with at least 3 difficulty choices and ask the user
# to select the desired level
difficulty = "1" # sample data, normally the user should choose the difficulty


# STEP 2
# based on the chosen difficulty level, set the values 
# for the player's lives
word_to_guess = "Cairo" # sample data, normally the word should be chosen from the countries-and-capitals.txt
lives = 5 # sample data, normally the lives should be chosen based on the difficulty


# STEP 3
# display the chosen word to guess with all letters replaced by "_"
# for example instead of "Cairo" display "_ _ _ _ _"


# STEP 4
# ask the user to type a letter
# here you should validate if the typed letter is the word 
# "quit", "Quit", "QUit", "QUIt", "QUIT", "QuIT"... you get the idea :)
# HINT: use the upper() or lower() built-in Python functions


# STEP 5
# validate if the typed letter is already in the tried letters
# HINT: search on the internet: `python if letter in list`
# If it is not, than append to the tried letters
# If it has already been typed, return to STEP 5. HINT: use a while loop here
already_tried_letters = [] # this list will contain all the tried letters


# STEP 6
# if the letter is present in the word iterate through all the letters in the variable
# word_to_guess. If that letter is present in the already_tried_letters then display it,
# otherwise display "_".


# if the letter is not present in the word decrease the value in the lives variable
# and display a hangman ASCII art. You can search the Internet for "hangman ASCII art",
# or draw a new beautiful one on your own.



# STEP 7
# check if the variable already_tried_letters already contains all the letters necessary
# to build the value in the variable word_to_guess. If so display a winning message and exit
# the app.
# If you still have letters that are not guessed check if you have a non negative amount of lives
# left. If not print a loosing message and exit the app.
# If neither of the 2 conditions mentioned above go back to STEP 4

import os
import random
 
 
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
 
 
def input_char():
    letter = input()
    return letter
 

def check_char():
    while True:
        letter = input_char()
        if len(letter) == 1 and letter.isalpha():
            new_char = letter.lower()
            break
        else:
            print('Podaj literę alfabetu ')
            
    return new_char
 
 
def menu():
    while True:
        clear_console()
        print('''
HANGMAN  v1.0
Wybierz poziom trudności:
1. Łatwy
2. Średni
3. Trudny 
        ''')
        level = is_input()
        if level >= 1 and level <= 3:  
            break
    match level:
        case 1:
            print('wybrałes poziom łatwy')
            lives = 6
        case 2:
            print('wybrałes poziom średni')
            lives = 4
        case 3:
            print('wybrałes poziom trudny')
            lives = 2
        case _:
            print('Wybierz liczbę od 1 do 3')
    return lives
 
 
 
def is_input():
 
    while True:
        num = input()
        try:
            num_to_int = int(num)
            break
        except:
            print('Podaj liczbę')
            continue
    return num_to_int
 
 
def load_data():
    with open('r.txt', 'r') as file:
 
        country = random.choice(file.readlines())
        new_country = country.split(' | ')
        new_country[0].lstrip().rstrip()
    return new_country[0]
 
 
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
 
 
def check_lives(lives):
    if lives > 0:
        return True
    return False


def count_lives(letter, solid_table, uses_table, lives):
    if letter in solid_table or letter in uses_table:
        return lives
    else:
        lives -= 1 
        return lives
 
 
 
def hangman():
    clear_console()
    lives = menu()
 
    word = load_data()
    input_table = create_table_of_word(word)
    work_table = start_word(word)
    table_of_used_word = []
 
    while work_table != input_table:
   
        print(*work_table)    
        print('podaj znak, pamietaj ze uzyles juz')
        print(*table_of_used_word)
        letter = check_char()
        lives = count_lives(letter, input_table, table_of_used_word, lives)
        if not check_lives(lives):
            print(f'Przegrales, prawidlowe slowo to {word}')
 
            break
        for i in range(len(input_table)):
            while  input_table[i].lower() == letter.lower():
                work_table[i] = input_table[i]
 
                break          
        if not letter in table_of_used_word:
            table_of_used_word.append(letter)  

        if work_table == input_table:   
            print(f'Hasło brzmiało :') 
            print(*input_table)
            print('wygrałeś')      
            
             
            break        
 
hangman()