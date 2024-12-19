from db import create_tables

from dailies import *
from screen import Screen
from short_story import short_story_handler
from tournament import tournament_handler
from utils import *
from test_screen import check_screen

FILE_PATH = "./points.db"

def main_screen_handler():
    main_screen = Screen(
        "Main Screen",
        [
            ["dailies", daily_handler],
            ["short story", short_story_handler],
            ["tournaments", tournament_handler]
        ],
        show_back=False
    )

def main():
    create_tables()
    main_screen_handler()
    # check_screen()

if __name__ == "__main__":
    main()
