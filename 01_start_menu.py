# Imports
from tkinter import *


# Classes
class StartMenu:
    """
    The start menu for the Arctic Monkeys Lyric Quiz
    """
    def __init__(self):

        bg_colour = "#6C676B"
        fg_colour = "#D0CB29"
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        heading = "Arctic\nMonkeys\nLyrics Quiz"
        self.title_heading = Label(self.start_frame, text=heading,
                                   font=("Joti One", "16", "bold"),
                                   bg=bg_colour, fg=fg_colour, justify="left")
        self.title_heading.grid(row=0)


# Main
if __name__ == "__main__":
    root = Tk()
    root.title("Arctic Monkeys Lyric Quiz")
    StartMenu()
    root.mainloop()