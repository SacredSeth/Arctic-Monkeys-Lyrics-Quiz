from tkinter import *
from tkextrafont import Font
import albumfonts as af


class StartMenu:
    """
    start menu
    """
    def __init__(self):
        bg_colour = "#6C676B"
        fg_colour = "#D0CB29"
        self.start_frame = Frame(padx=10, pady=10, bg=bg_colour)
        self.start_frame.grid()

        # fonts are:
        # Autour One, Joti One, Roboto Slab, Special Gothic, Luckiest Guy, Sarpanch
        # import custom fonts
        for i, v in enumerate(af.file_list):
            font_family = af.font_families[i]
            custom_font = Font(file=v, family=font_family)

        heading = "Arctic\nMonkeys\nLyrics Quiz"
        self.title_heading = Label(self.start_frame, text=heading,
                                   font=("Joti One", "24"), bg=bg_colour,
                                   fg=fg_colour, justify="left")
        # sticky aligns the label in the frame (w is for west (left))
        self.title_heading.grid(row=0, sticky="w")

        body_text = ("Quiz to test your Arctic Monkeys knowledge.\n"
                     "Can you guess the song by just the first two lyrics?\n"
                     "Try and beat your friends in this quiz by answering as\n"
                     "many questions correctly as you can.")
        self.title_body = Label(self.start_frame, text=body_text,
                                font=("Joti One", "12"), bg=bg_colour,
                                fg=fg_colour, justify="left")
        self.title_body.grid(row=1)

        # frame to hold quick start buttons
        self.quick_buttons_frame = Frame(self.start_frame, padx=10, pady=10, bg=bg_colour)
        self.quick_buttons_frame.grid(row=2)

        # text | rounds | command
        quick_btn_info = [
            ["Quick", 5, None],
            ["Standard", 10, None],
            ["Long", 15, None]
        ]
        quick_btn_list = []
        btn_bg = "#413D40"
        for i, item in enumerate(quick_btn_info):
            self.quick_selbtn = Button(self.quick_buttons_frame,
                                       text=item[0], bg=btn_bg,
                                       fg=fg_colour, font=("Joti One", "16"),
                                       width=9, command=item[2])
            self.quick_selbtn.grid(row=0, column=i, padx=10)
            quick_btn_list.append([self.quick_selbtn, item[1]])

        self.entry_text = Label(self.start_frame, text="Enter Amount of Questions",
                                font=("Joti One", "12"), fg=fg_colour, bg=bg_colour)
        self.entry_text.grid(row=3)

        self.custom_entry = Entry(self.start_frame, font=("Arial", "12"),
                                  width=30, justify='center')
        self.custom_entry.grid(row=4)

        self.custom_button = Button(self.start_frame, text="Custom",
                                    font=("Joti One", "16"), bg=btn_bg,
                                    fg=fg_colour, command=None, width=20)
        self.custom_button.grid(row=5, pady=5)


# Main
if __name__ == "__main__":
    root = Tk()
    root.title("Lyrics Quiz")
    StartMenu()
    root.mainloop()