from tkinter import *
from tkextrafont import Font
import albumfonts as af

class StartMenu:
    """start menu"""

    def __init__(self):
        self.start_frame = Frame(padx=15, pady=15)
        self.start_frame.grid()

        self.error_provider = Label(self.start_frame, text="Enter Rounds:",
                                    font=("Arial", "12"))
        self.error_provider.grid(row=0)

        self.round_entry = Entry(self.start_frame)
        self.round_entry.grid(row=1)

        self.to_game_btn = Button(self.start_frame, text="Play Game",
                                  command=self.round_check)
        self.to_game_btn.grid(row=2)


    def round_check(self):
        """
        Checks that rounds entered is > 0
        :return: valid num of rounds
        """

        # gets entered value
        rounds_wanted = self.round_entry.get()
        error = "Enter Int > 0"
        has_err = "no"

        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                self.round_entry.delete(0, END)
                self.error_provider.config(text="Enter Rounds:")

                # invent the game with number of rounds
                PlayGame(rounds_wanted)
                # hide the main window
                root.withdraw()

            else:
                has_err = "yes"

        except ValueError:
            has_err = "yes"

        # display error
        if has_err == "yes":
            self.error_provider.config(text=error)
            self.round_entry.delete(0, END)


class PlayGame:
    """The Game (you lost)"""

    def __init__(self, rnds):
        """
        initialize the game
        """

        # fonts are:
        # Autour One, Joti One, Roboto Slab, Special Gothic, Luckiest Guy, Sarpanch
        # import custom fonts
        for i, v in enumerate(af.file_list):
            font_family = af.font_families[i]
            custom_font = Font(file=v, family=font_family)

        # grey background
        bg_colour = "#E6E6E6"

        # set round variables
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(rnds)

        self.points = IntVar()
        self.points.set(0)

        self.play_box = Toplevel(bg=bg_colour)
        self.game_frame = Frame(self.play_box, bg=bg_colour)
        self.game_frame.grid(padx=15, pady=15)

        # if users press the 'x' on the game window, end the entire game!
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        # label list (text | font | row | justify)
        game_labels_list = [
            ["Round # of #", ("Joti One", "24"), 0, "left"],
            ["Lyrics go here", ("Arial", "12", "bold"), 1, "center"],
            ["Which Arctic Monkeys song is this?", ("Arial", "9"), 2, "center"]
        ]
        game_labels_ref = []
        for item in game_labels_list:
            make_label = Label(self.game_frame, text=item[0],
                                    font=item[1], wraplength=300,
                                    justify=item[3], bg=bg_colour)
            make_label.grid(row=item[2])
            game_labels_ref.append(make_label)

        # retrieve labels

        self.round_heading = game_labels_ref[0]
        # align the label on the left of the frame
        self.round_heading.grid_configure(sticky='w')

        self.round_lyrics = game_labels_ref[1]
        self.result_label = game_labels_ref[2]

        # set up answer buttons
        self.song_choice_frame = Frame(self.game_frame, padx=5, pady=5, bg=bg_colour)
        self.song_choice_frame.grid(row=3)

        self.choice_button_ref = []
        btn_bg = "#C6C6C6"
        # create 2X2 grid of buttons
        for i in range(0, 4):
            self.choice_btn = Button(self.song_choice_frame, text="Song Name",
                                     font=("Arial", "12"), width=15,
                                     command=None, bg=btn_bg)
            self.choice_btn.grid(row=i // 2,
                                 column=i % 2,
                                 padx=5, pady=5)
            self.choice_button_ref.append(self.choice_btn)

        # hint button stats
        self.hints_used = IntVar()
        self.hints_used.set(0)

        # stats and next question button frame
        self.stats_next_frame = Frame(self.game_frame, padx=5, pady=5, bg=bg_colour)
        self.stats_next_frame.grid(row=5)

        # list to hold button details
        # root | text | font | bg | command | width | row | column
        game_button_list = [
            [self.game_frame, "Hints Used: 0/2", ("Arial", "9"), "#0050EF", None, 15, 4, None],
            [self.stats_next_frame, "Stats", ("Arial", "12"), 'black', None, 15, 0, 0],
            [self.stats_next_frame, "Next Question", ("Arial", "12"), "#A4802A", None, 15, 0, 1],
            [self.game_frame, "End Game", ("Arial", "12"), "#A20025", None, 32, 6, None]
        ]

        # create the buttons
        game_button_ref = []
        for item in game_button_list:
            make_button = Button(item[0], text=item[1], font=item[2],
                                 bg=item[3], command=item[4],
                                 width=item[5], fg='white')
            make_button.grid(row=item[6], column=item[7], padx=5)
            game_button_ref.append(make_button)

        # assign buttons to self object
        self.hint_button = game_button_ref[0]
        self.stats_button = game_button_ref[1]
        self.next_button = game_button_ref[2]
        self.end_game_button = game_button_ref[3]


# main
if __name__ == "__main__":
    root = Tk()
    root.title("Lyrics Quiz")
    StartMenu()
    root.mainloop()