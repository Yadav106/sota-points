from os import system, name
import sys
from rich import print

def sysexit():
    print("[purple]See ya soon! Tata!")
    sys.exit(0)

def clear():
    """
    Clears screen
    """
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

