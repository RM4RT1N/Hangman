import random
import sys


def load_data():
    with open('countries-and-capitals.txt', 'r') as f:
        country = random.choice(f.readlines())
        new_country = country.split(' | ')
    return new_country[0]


def dev_menu():
    if "--dev" in sys.argv:
        print(load_data())


dev_menu()