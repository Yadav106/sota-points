from rich.tree import Tree
from time import sleep

from screen import Screen

def daily_handler():
    daily_screen = Screen(
        "Dailies",
        [
            ["create an entry", add_entry]
        ]
    )

def add_entry():
    print("Adding entry")
    sleep(1)

