import datetime
from os import system, name
import sys
from rich import print
from rich.prompt import Prompt

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

def convert_to_ddmmyyyy(date):
    # Ensure the input date is a datetime object, if it's not, try to parse it
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")  # Assuming date is in "YYYY-MM-DD" format
    
    # Convert the date to "DD-MM-YYYY" format
    return date.strftime("%d-%m-%Y")

def get_positive_number(prompt_message):
    while True:
        try:
            n = int(Prompt.ask(prompt_message))
            if n > 0:
                return n
            else:
                print("[red]The number must be greater than 0. Please try again.[/red]")
        except ValueError:
            print("[red]Invalid input. Please enter a positive number.[/red]")
