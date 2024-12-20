from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.table import Table

from db import get_db_connection
from screen import Screen

console = Console()

def writers_handler():
    writers_screen = Screen(
        ["Writers"],
        [
            ["add a new writer", add_writer],
            ["remove a writer", remove_writer],
            ["edit a writer's name", edit_writer_name],
            ["get all writers", get_writer_stats]
        ]
    )

def get_all_writers():
    writers = []
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name from writers")
        writers = cursor.fetchall()
        writers = [writer[0] for writer in writers]

    return writers

def add_writer():
    name = Prompt.ask("Enter writer's [blue]name[/blue]", default="enter 'c' to cancel")
    if name.strip().lower() == 'c':
        return

    writers = get_all_writers()
    if name in writers:
        print(f"[red][bold]{name}[/bold] already exists")
        Prompt.ask("[blue]Press enter to continue")
        return

    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO writers (name) values (?)
            ''', (name,))
            conn.commit()

            print(f"[green]Writer '{name}' added successfully![/green]")
            Prompt.ask("[blue]Press enter to continue")
        except Exception as ex:
            print(f"[red]Error while adding a writer : [bold]{ex}[/bold]")

def remove_writer():
    writers = get_all_writers()
    writers.append("c")
    name = Prompt.ask("Enter writer's [blue]name[/blue]", default="enter 'c' to cancel", choices=writers)
    if name.strip().lower() == 'c':
        return

    if name not in writers:
        print(f"[red][bold]{name}[/bold] does not exist")
        Prompt.ask("[blue]Press enter to continue")
        return

    confirmation = Confirm.ask(f"Do you want to remove {name}")
    if not confirmation:
        return

    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                DELETE FROM writers where name=(?)
            ''', (name,))
            conn.commit()

            print(f"[green]Writer '{name}' removed successfully![/green]")
            Prompt.ask("[blue]Press enter to continue")
        except Exception as ex:
            print(f"[red]Error while removing a writer : [bold]{ex}[/bold]")

def edit_writer_name():
    writers = get_all_writers()
    writers.append("c")
    name = Prompt.ask("Enter writer's [blue]name[/blue]", default="enter 'c' to cancel", choices=writers)
    if name.strip().lower() == 'c':
        return

    if name not in writers:
        print(f"[red][bold]{name}[/bold] does not exist")
        Prompt.ask("[blue]Press enter to continue")
        return

    new_name = Prompt.ask(f"Enter new name for [blue]{name}[/blue]", default="enter 'c' to cancel")
    if name.strip().lower() == 'c':
        return

    # Check if the new name is valid and different from the old one
    if new_name.strip() == "" or new_name == name or new_name == "enter 'c' to cancel":
        print("[red]New name cannot be empty or the same as the current name.[/red]")
        Prompt.ask("[blue]Press enter to continue")
        return

    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE writers SET name=(?) WHERE name=(?)
            ''', (new_name, name,))
            conn.commit()

            print(f"[green]Writer '{name}' changed to '{new_name}'![/green]")
            Prompt.ask("[blue]Press enter to continue")
        except Exception as ex:
            print(f"[red]Error while editing writer's name : [bold]{ex}[/bold]")


def get_writer_stats():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, total_points from writers")
        writers = cursor.fetchall()
        writers = [[writer[0], writer[1]] for writer in writers]
        
        writers = sorted(writers, key=lambda x: x[1], reverse=True)

        table = Table(title="Writers")

        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Total Points", style="cyan", no_wrap=True)

        for writer in writers:
            table.add_row(writer[0], str(writer[1]))

        print("")
        console.print(table)
        Prompt.ask("[blue]Press enter to continue")
