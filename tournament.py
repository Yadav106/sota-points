from datetime import datetime
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.table import Table


from db import get_db_connection
from screen import Screen
from utils import get_positive_number

console = Console()

def tournament_handler():
    tournament_screen = Screen(
        "Tournaments",
        [
            ["create an entry", add_entry],
            ["remove an entry", remove_entry],
            ["get entries", get_entries],
            ["get current month stats", get_current_month_points],
        ]
    )

def add_entry():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name from writers")
        writers = cursor.fetchall()
        writers = [[writer[0], writer[1]] for writer in writers]

        writers_dict = {}
        for writer in writers:
            writers_dict[writer[1]] = writer[0]

        writers_list = [writer[1] for writer in writers]
        writers_list.append("c")

        name = Prompt.ask("Enter writer's [blue]name[/blue]", default="enter 'c' to cancel", choices=writers_list)
        if name.strip().lower() == 'c' or name == "enter 'c' to cancel":
            return

        writers_id = writers_dict.get(name)
        if writers_id is None:
            print("[red]Unexpected error occured (writers_id is none in add_entry for tournaments)")
            Prompt.ask("Press enter to continue")
            return

        try:
            points = int(Prompt.ask("Enter points"))
            if points < 0:
                print("[red]points cannot be negative")
                return
        except Exception:
            print(f"[red] Error occured while entering points")
            Prompt.ask("Press enter to continue")
            return

        today = datetime.now().strftime("%d-%m-%Y")
        date = Prompt.ask("Enter date (dd-mm-yyyy)", default=f"press enter for {today}")
        if date == f"press enter for {today}":
            date = today

        try:
            valid_date = datetime.strptime(date, "%d-%m-%Y")
            valid_date.strftime("%d-%m-%Y")  # Return in the same format
            date = valid_date.strftime("%Y-%m-%d")
        except Exception:
            print("[red]Invalid date format or date does not exist. Please try again.[/red]")
            Prompt.ask("Press enter to continue")
            return

        try:
            cursor.execute('''
                INSERT INTO tournaments (writer_id, points, date) values ((?), (?), (?))
            ''', (writers_id, points, date))

            cursor.execute('''
                UPDATE writers
                SET total_points = total_points + ?
                WHERE name = ?;
            ''', (points, name))
            conn.commit()
        except Exception:
            print(f"[red]Error occured while adding tournament points for user {name}")

        print(f"[green]Added entry for {name}")
        Prompt.ask("[blue]Press enter to continue")

def remove_entry():
    id = get_positive_number("Enter the id of the entry you want to remove")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT writer_id, points from tournaments where id = (?)
            ''', (id, ))

            point = cursor.fetchall()

            if len(point) == 0:
                print("[red]the given id does not exist")
                Prompt.ask("[blue]Press enter to continue")
                return

            confirmation = Confirm.ask(f"[red]do you want to delete the entry with id {id}")
            if not confirmation:
                print("[blue]deletion cancelled")
                Prompt.ask("[blue]Press enter to continue")
                return

            cursor.execute('''
                DELETE from tournaments where id = (?)
            ''', (id, ))

            cursor.execute('''
                UPDATE writers 
                SET total_points = total_points - (?)
                WHERE id = (?)
            ''', (point[0][1], point[0][0]))

            conn.commit()

            print("[green]Entry deleted successfully!")
            Prompt.ask("[blue]Press enter to continue")
    except Exception as ex:
        print(f"[red]Error while deleting entry {ex}")

def get_entries():
    n = get_positive_number('[blue]How many entries do you want to see')

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT tournaments.id, writers.name, tournaments.date, tournaments.points
                FROM tournaments
                JOIN writers ON tournaments.writer_id = writers.id
                ORDER BY tournaments.date DESC
                LIMIT ?;
            ''', (n, ))

            daily_stats = cursor.fetchall()

            table = Table(title="Tournament Stats")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Date", style="cyan", no_wrap=True)
            table.add_column("Points", style="cyan", no_wrap=True)

            for stats in daily_stats:
                table.add_row(str(stats[0]), stats[1], stats[2], str(stats[3]))

            print("")
            console.print(table)
            print("")
            print(f"[blue]Fetched [violet]{len(daily_stats)}[/violet] records")

            Prompt.ask("[blue]Press enter to continue")
    except Exception as ex:
        print(f"[red]There was some issue in fetching daily entries : {ex}")

def get_current_month_points():
    try:
        current_date = datetime.now()
        month = current_date.month
        year = current_date.year

        first_day_of_month = f'{year}-{str(month).zfill(2)}-01'

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name, SUM(points) as daily_points, date FROM writers
                INNER JOIN tournaments on tournaments.writer_id = writers.id
                WHERE date >= ?
                GROUP BY name
                ORDER BY daily_points DESC
            ''', (first_day_of_month, ))

            month_points = cursor.fetchall()

            table = Table(title=f"Points for {current_date.strftime('%B %Y')}")
            table.add_column("Writer", style="cyan", no_wrap=True)
            table.add_column("Points Earned", style="cyan", no_wrap=True)

            for point in month_points:
                table.add_row(point[0], str(point[1]))

            print("")
            console.print(table)

            Prompt.ask("[blue]Press enter to continue")

    except Exception as ex:
        print(f"[red]Error while fetching points for the current month: {ex}")
        Prompt.ask("[blue]Press enter to continue")
