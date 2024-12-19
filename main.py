from db import create_tables
from rich.console import Console
from rich import print

from styles import custom_theme

FILE_PATH = "./points.db"
console = Console(theme=custom_theme)

def main():
    create_tables()

    while True:
        opt = input("Enter an option : ")
        print(f"[green]You selected {opt}[/green]")

        if opt == 'x':
            print("See ya later!")
            break

if __name__ == "__main__":
    main()
