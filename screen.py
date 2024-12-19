from rich.tree import Tree
from rich import print
from time import sleep

from utils import clear, sysexit

class Screen:
    def __init__(self, title, opts = [], show_back = True):
        self.title = title
        self.opts = opts
        self.cache = {}
        self.show_back = show_back

        self.tree = Tree(f"[violet]{self.title}")
        self.create_branches()
        self.loop()

    def create_branches(self):
        char = 97

        for opt in self.opts:
            self.tree.add(f"[blue]{chr(char)}) {opt[0]}")
            self.cache[chr(char)] = opt[1]
            char += 1

        if self.show_back:
            self.tree.add("[blue]u) go back")

        self.tree.add(f"[blue]x) exit")
        self.cache['x'] = sysexit

    def loop(self):
        while True:
            clear()
            print(self.tree)
            opt = input("Enter your option : ")

            if opt == 'u' and self.show_back:
                return

            cached_func = self.cache.get(opt, None)

            if cached_func is None:
                print(f"[red][bold]{opt}[/bold] is not a valid option")
                sleep(1)
            else:
                cached_func()
