from tkinter import *
from tkextrafont import Font
import albumfonts as af
import csv
import random
from functools import partial


# functions
def load_fonts():
    """loads the custom fonts"""
    # fonts are:
    # Autour One, Joti One, Roboto Slab, Special Gothic, Luckiest Guy, Sarpanch
    # import custom fonts
    for i, v in enumerate(af.file_list):
        font_family = af.font_families[i]

        try:  # load the font
            custom_font = Font(file=v, family=font_family)

        except:  # if the font is already loaded
            continue  # skip this font


def get_song_list():
    """Returns the list of all lyrics and songs in the csv file"""

    file = open("00_Arctic_Monkeys_Lyrics.csv", "r")
    all_songs = list(csv.reader(file, delimiter=","))
    file.close()

    # remove first row
    all_songs.pop(0)

    return all_songs


def get_round_choices():
    """
    chooses 4 random unique songs, one of which will be the correct answer
    :return: List of options, correct answer
    """

    song_list = get_song_list()

    round_choices = []
    # loop so we have 4 unique songs
    while len(round_choices) < 4:
        random_song = random.choice(song_list)

        # check song not already in list
        if random_song not in round_choices:
            round_choices.append(random_song)

    # choose a random song to be the correct answer
    correct_ans = random.choice(round_choices)

    return round_choices, correct_ans


# classes
class Hints:
    """class for testing hints"""

    def __init__(self):
        """initialise class"""

        load_fonts()

        # grey background
        bg_colour = "#E6E6E6"

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        # no rounds wanted because this will be infinite in length

        # keep track of how many hints are used (for later stat calculations)
        self.hints_used = IntVar()
        self.hints_used.set(0)

        # for each round
        self.hint_level = IntVar()
        self.hint_level.set(0)

        self.game_frame = Frame(bg=bg_colour, padx=15, pady=15)
        self.game_frame.grid()

        # label list (text | font | justify)
        game_labels_list = [
            ["Round #", ("Joti One", "24"), "left"],
            ["Lyrics go here", ("Arial", "12", "bold"), "center"],
            ["Which Arctic Monkeys song is this?", ("Arial", "9"), "center"]
        ]

        game_labels_ref = []
        for i, item in enumerate(game_labels_list):
            make_label = Label(self.game_frame, text=item[0],
                               font=item[1], wraplength=300,
                               justify=item[2], bg=bg_colour)
            make_label.grid(row=i)
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
                                     font=("Arial", "12"), width=15, bg=btn_bg)
            self.choice_btn.grid(row=i // 2,
                                 column=i % 2,
                                 padx=5, pady=5)
            self.choice_button_ref.append(self.choice_btn)

        # game buttons
        # text | font | bg | command | width | row
        game_button_list = [
            ["Hints Used: 0/2", ("Arial", "9"), "#0050EF", self.get_hint, 15, 4],
            ["New Questions", ("Arial", "14"), "#A4802A", self.new_round, 15, 5]
        ]

        # create the buttons
        game_button_ref = []
        for item in game_button_list:
            make_button = Button(self.game_frame, text=item[0], font=item[1],
                                 bg=item[2], command=item[3],
                                 width=item[4], fg='white')
            make_button.grid(row=item[5], padx=5)
            game_button_ref.append(make_button)

        # reference the buttons
        self.hint_button = game_button_ref[0]
        self.next_button = game_button_ref[1]

        # start new round
        self.new_round()


    def new_round(self):
        """
        chooses the rounds' songs and sets up the labels / buttons accordingly
        """

        bg_colour = "#E6E6E6"
        btn_bg = "#C6C6C6"

        # get amount of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        self.rounds_played.set(rounds_played)

        # reset hint level
        self.hint_level.set(0)

        # get songs for the buttons, and the correct ans
        self.round_choices_list, self.round_ans = get_round_choices()

        # update heading and labels
        self.round_heading.config(text=f"Round {rounds_played + 1}")
        self.round_lyrics.config(text=self.round_ans[1], font=("Arial", "12", "bold"),
                                 bg=bg_colour, fg='black')
        self.result_label.config(text="Which Arctic Monkeys song is this?", bg="#E6E6E6")

        # update buttons
        self.hint_button.config(text="Hints Used: 0/2")
        for i, item in enumerate(self.choice_button_ref):
            item.config(text=self.round_choices_list[i][0], font=("Arial", "12"),
                        bg=btn_bg, fg='black')


    def get_hint(self):
        """adds one to hint level and provides correct hint"""

        # retrieve the current hint level of the round
        hint_level = self.hint_level.get()

        # hint level can only be between 0 - 2
        if hint_level == 2:
            # do nothing, as all hints are used
            return

        elif hint_level == 1:
            # loop through each choice button
            for i, btn in enumerate(self.choice_button_ref):
                # get button album
                btn_album = self.round_choices_list[i][2]

                # retrieve album design and assign it to the button
                [alb_font, alb_fg, alb_bg] = af.get_font_details(btn_album)
                btn.config(font=(alb_font, "12"), fg=alb_fg, bg=alb_bg)

            # increment hint level
            hint_level += 1

        else:
            # get album of the current question
            ans_album = self.round_ans[2]

            # get album design details and assign them to the lyric heading
            [lyr_font, lyr_fg, lyr_bg] = af.get_font_details(ans_album)
            self.round_lyrics.config(font=(lyr_font, "12"), fg=lyr_fg, bg=lyr_bg)

            # increment hint level
            hint_level += 1

        # update data
        self.hint_button.config(text=f"Hints Used: {hint_level}/2")
        self.hint_level.set(hint_level)


# main
if __name__ == "__main__":
    root = Tk()
    root.title("Hint Testing")
    Hints()
    root.mainloop()