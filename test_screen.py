from screen import Screen
from rich import print

def a():
    print("a called")

def b():
    print("b called")

def c():
    print("c called")

def check_screen():
    screen = Screen(
        "Test Screen",
        [
            ["call a", a],
            ["call b", b],
            ["call c", c]
        ]
    )

