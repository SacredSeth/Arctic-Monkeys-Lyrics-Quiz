from tkinter import *
from tkextrafont import Font
import albumfonts as af
import csv
import random
from functools import partial
from PIL import Image, ImageTk


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


def font_size(text, family):
    """
    Calculates an appropriate font size for the length of the title to fit in a button.
    :param text: The title to fit into the button
    :param family: The font family
    :return: The font size (int)
    """


# classes
class StartMenu:
    """
    start menu
    """
    def __init__(self):
        """
        Initialize the start menu
        """

        # get design details for the start menu
        [font_fam, fg_colour, btn_bg, menu_bg] = af.get_album_details("Favourite Worst Nightmare")[:4]

        self.start_frame = Frame(padx=10, pady=10, bg=menu_bg)
        self.start_frame.grid()

        # load the custom fonts
        load_fonts()

        # label text
        heading = "Arctic\nMonkeys\nLyrics Quiz"
        body_text = ("Quiz to test your Arctic Monkeys knowledge.\n"
                     "Can you guess the song by just the first two lyrics?\n"
                     "Try and beat your friends in this quiz by answering as\n"
                     "many questions correctly as you can.")

        # contains the information for the labels
        # text | font | justify | row | sticky
        start_labels_info = [
            [heading, (font_fam, 24), "left", 0, "w"],
            [body_text, (font_fam, 12), "left", 1, None],
            ["Enter Rounds:", (font_fam, 12), "center", 3, None]
        ]

        start_labels_ref = []
        for item in start_labels_info:
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=fg_colour, bg=menu_bg, justify=item[2])
            make_label.grid(row=item[3], sticky=item[4])
            start_labels_ref.append(make_label)

        # assign the error provider
        self.error_provider = start_labels_ref[2]

        # frame to hold quick start buttons
        self.quick_buttons_frame = Frame(self.start_frame, padx=10, pady=10, bg=menu_bg)
        self.quick_buttons_frame.grid(row=2)

        # text | rounds
        quick_btn_info = [
            ["Quick", 5],
            ["Standard", 10],
            ["Long", 15]
        ]

        quick_btn_list = []
        for i, item in enumerate(quick_btn_info):
            self.quick_selbtn = Button(self.quick_buttons_frame, text=item[0],
                                       bg=btn_bg, fg=fg_colour, font=(font_fam, 16),
                                       width=9, command=partial(self.quick_game, item[1]))
            self.quick_selbtn.grid(row=0, column=i, padx=10)
            quick_btn_list.append(self.quick_selbtn)

        self.custom_entry = Entry(self.start_frame, font=("Arial", 12),
                                  width=30, justify='center')
        self.custom_entry.grid(row=4)

        self.custom_button = Button(self.start_frame, text="Custom",
                                    font=(font_fam, 16), bg=btn_bg,
                                    fg=fg_colour, command=self.round_check, width=20)
        self.custom_button.grid(row=5, pady=5)


    def round_check(self):
        """
        Checks that rounds entered is > 0
        :return: valid num of rounds
        """

        # gets entered value
        rounds_wanted = self.custom_entry.get()
        error = "Enter Int > 0"
        has_err = False

        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                self.custom_entry.delete(0, END)
                self.error_provider.config(text="Enter Rounds:")

                # invent the game with number of rounds
                PlayGame(rounds_wanted)
                # hide the main window
                root.withdraw()

            else:
                has_err = True

        except ValueError:
            has_err = True

        # display error
        if has_err:
            self.error_provider.config(text=error)
            self.custom_entry.delete(0, END)


    def quick_game(self, rounds):
        """
        For use with quick buttons, directly opens game menu
        with set number of games without checking.
        :param rounds: Number of desired rounds
        :return:
        """
        self.custom_entry.delete(0, END)
        self.error_provider.config(text="Enter Rounds:")

        # invent the game with number of rounds
        PlayGame(rounds)
        # hide the main window
        root.withdraw()


class PlayGame:
    """The Game (you lost)"""

    def __init__(self, rnds):
        """
        initialize the game
        """

        load_fonts()  # load custom fonts

        # grey background
        bg_colour = "#E6E6E6"

        # set round variables
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(rnds)

        self.round_cont_incr = IntVar()
        self.round_cont_incr.set(rnds)

        self.correct_answers = IntVar()
        self.correct_answers.set(0)

        self.hints_used = IntVar()
        self.hints_used.set(0)

        self.hint_level = IntVar()
        self.hint_level.set(0)

        # holds the amount of times an album shows up
        self.album_question_count = {
            "Whatever People Say I Am, That's What I'm Not": 0,
            "Favourite Worst Nightmare": 0,
            "Humbug": 0,
            "Suck It and See": 0,
            "AM": 0,
            "Tranquility Base Hotel & Casino": 0
        }

        # holds the amount of correctly answered questions per album
        # starting dictionary is identical to self.album_question_count
        self.album_answer_count = {
            "Whatever People Say I Am, That's What I'm Not": 0,
            "Favourite Worst Nightmare": 0,
            "Humbug": 0,
            "Suck It and See": 0,
            "AM": 0,
            "Tranquility Base Hotel & Casino": 0
        }

        # set up the GUI
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
                                     font=("Arial", 12), width=33, wraplength=300,
                                     command=partial(self.round_results, i),
                                     bg=btn_bg)
            self.choice_btn.grid(row=i, padx=5, pady=5)
            self.choice_button_ref.append(self.choice_btn)

        # stats and next question button frame
        self.stats_next_frame = Frame(self.game_frame, padx=5, pady=5, bg=bg_colour)
        self.stats_next_frame.grid(row=5)

        # list to hold button details
        # root | text | font | bg | command | width | row | column
        game_button_list = [
            [self.game_frame, "Hints Used: 0/2", ("Arial", "9"), "#0050EF", self.get_hint, 15, 4, None],
            [self.stats_next_frame, "Stats", ("Arial", "12"), 'black', self.to_stats, 15, 0, 0],
            [self.stats_next_frame, "Next Question", ("Arial", "12"), "#A4802A", self.new_round, 15, 0, 1],
            [self.game_frame, "End Game", ("Arial", "12"), "#A20025", self.close_game, 32, 6, None]
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

        # once GUI has been created - start a new round
        self.new_round()


    def new_round(self):
        """
        chooses the rounds' songs and sets up the labels / buttons accordingly
        """

        bg_colour = "#E6E6E6"
        btn_bg = "#C6C6C6"

        # get amount of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # reset hint level
        self.hint_level.set(0)

        # get songs for the buttons, and the correct ans
        self.round_choices_list, self.round_ans = get_round_choices()

        # update heading and labels
        self.round_heading.config(text=f"Round {rounds_played} / {rounds_wanted}")
        self.round_lyrics.config(text=self.round_ans[1], font=("Arial", 12, "bold"),
                                 bg=bg_colour, fg='black')
        self.result_label.config(text="Which Arctic Monkeys song is this?", bg="#E6E6E6")

        # update buttons
        self.hint_button.config(text="Hints Used: 0/2", state=NORMAL)
        self.stats_button.config(state=DISABLED)
        for i, item in enumerate(self.choice_button_ref):
            item.config(text=self.round_choices_list[i][0], font=("Arial", 12),
                        bg=btn_bg, fg='black', state=NORMAL)

        self.next_button.config(text="Next Question", state=DISABLED)
        self.end_game_button.config(text="End Game")


    def round_results(self, user_guess):
        """
        retrieves which button was pressed (index 0-3),
        and checks if it is the correct answer. updates
        results and adds to stats references
        :param user_guess: index of pressed button
        :return:
        """

        # boolean value if correct ans
        result = bool(self.round_choices_list[user_guess] == self.round_ans)

        # get amount of rounds played
        rounds_played = self.rounds_played.get()

        # get current amount of correct answers
        current_points = self.correct_answers.get()

        ans_song_name = self.round_ans[0]
        chosen_song_name = self.choice_button_ref[user_guess].cget('text')
        ans_song_album = self.round_ans[2]

        # add one to the amount of times the question's album shows up
        self.album_question_count[ans_song_album] += 1

        if result:
            result_text = f"Correct! '{chosen_song_name}' is the song."
            result_bg = "#82B366"

            # add one to amount of correct answers for this album
            self.album_answer_count[ans_song_album] += 1

            current_points += 1
            self.correct_answers.set(current_points)

        else:
            result_text = f"Incorrect. The song was '{ans_song_name}'"
            result_bg = "#F8CECC"

        self.result_label.config(text=result_text, bg=result_bg)

        self.next_button.config(state=NORMAL)
        self.hint_button.config(state=DISABLED)
        self.stats_button.config(state=NORMAL)

        # check if game is over
        rounds_wanted = self.rounds_wanted.get()

        # end of game code
        if rounds_played == rounds_wanted:
            # end of game statistics

            # success rate
            success_rate = current_points / rounds_played * 100

            # label config
            self.round_heading.config(text="Game Over")
            self.round_lyrics.config(text=f"{success_rate:.0f}%")
            self.result_label.config(text="See stats menu for more details")

            round_increment = self.round_cont_incr.get()
            rounds_wanted += round_increment
            self.rounds_wanted.set(rounds_wanted)

            # buttons
            self.next_button.config(text=f"Play Again ({round_increment} rounds)")
            self.end_game_button.config(text="Main Menu")

            for item in self.choice_button_ref:
                item.config(state=DISABLED)


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
                [alb_font, alb_fg, alb_bg] = af.get_album_details(btn_album)[:3]
                btn.config(font=(alb_font, "12"), fg=alb_fg, bg=alb_bg)

            # increment hint level
            hint_level += 1

        else:
            # get album of the current question
            ans_album = self.round_ans[2]

            # get album design details and assign them to the lyric heading
            [lyr_font, lyr_fg, lyr_bg] = af.get_album_details(ans_album)[:3]
            self.round_lyrics.config(font=(lyr_font, "12"), fg=lyr_fg, bg=lyr_bg)

            # increment hint level
            hint_level += 1

        # update data
        self.hint_button.config(text=f"Hints Used: {hint_level}/2")
        self.hint_level.set(hint_level)
        hints_used = self.hints_used.get()
        hints_used += 1
        self.hints_used.set(hints_used)


    def to_stats(self):
        """Opens StatsMenu class"""

        self.stats_button.config(state=DISABLED)

        # format stats as:
        # [rounds_played, correct_answers, hints_used,
        # favourite_album, album_questions, correct_album_answers]

        # retrieve stats
        rounds_played = self.rounds_played.get()
        correct_answers = self.correct_answers.get()
        hints_used = self.hints_used.get()
        favourite_album = max(self.album_answer_count, key=self.album_answer_count.get)
        album_questions = self.album_question_count[favourite_album]

        # No correct answers, instead shows most seen album
        if album_questions == 0:
            favourite_album = max(self.album_question_count, key=self.album_question_count.get)
            album_questions = self.album_question_count[favourite_album]

        correct_album_answers = self.album_answer_count[favourite_album]

        retrieved_stats = [rounds_played, correct_answers, hints_used,
                           favourite_album, album_questions, correct_album_answers]

        # open menu
        StatsMenu(self, retrieved_stats)


    def close_game(self):
        """closes the active game"""
        # reshow root and close current window
        root.deiconify()
        self.play_box.destroy()


class StatsMenu:
    """the stats menu"""

    def __init__(self, parent, user_stats):
        """initialise menu"""

        # import fonts
        load_fonts()

        # unload stats
        rounds_played = user_stats[0]
        correct_answers = user_stats[1]
        hints_used = user_stats[2]
        favourite_album = user_stats[3]
        album_questions = user_stats[4]
        correct_album_answers = user_stats[5]

        # get design details
        [menu_font, menu_fg, btn_bg, menu_bg, image_file, release_date] = af.get_album_details(favourite_album)

        self.stats_box = Toplevel()

        # if users press cross at top, closes stats and
        # releases stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, parent))

        self.stats_frame = Frame(self.stats_box, padx=15, pady=15, bg=menu_bg)
        self.stats_frame.grid()

        self.stats_heading = Label(self.stats_frame, text="Statistics",
                                   font=(menu_font, 16), bg=menu_bg,
                                   fg=menu_fg, justify="center")
        self.stats_heading.grid(row=0)

        self.close_button = Button(self.stats_frame, text="Close",
                                   font=(menu_font, 14), bg=btn_bg,
                                   fg=menu_fg, width=20,
                                   command=partial(self.close_stats, parent))
        self.close_button.grid(row=2)

        # create the container
        self.stats_container = Frame(self.stats_frame, padx=10, pady=10, bg=menu_bg)
        self.stats_container.grid(row=1)

        # create the album stats container
        self.album_frame = Frame(self.stats_container, padx=5, pady=5, bg=menu_bg)
        self.album_frame.grid(row=2, column=0)

        correct_percentage = correct_answers / rounds_played * 100
        hints_percentage = hints_used / (rounds_played * 2) * 100

        # in case the user checks stats very early
        if album_questions == 0:
            album_percentage = 0
        else:
            album_percentage = correct_album_answers / album_questions * 100

        # list containing all the stats labels
        # root | text | font | row | column
        stats_label_list = [
            [self.stats_container, "Correct Answers:", (menu_font, 12), 0, 0],
            [self.stats_container, f"{correct_answers:.0f} / {rounds_played:.0f}  ( {correct_percentage:.1f}% )", ("Arial", 12), 0, 1],
            [self.stats_container, "Hints Used:", (menu_font, 12), 1, 0],
            [self.stats_container, f"{hints_used} / {rounds_played * 2}  ( {hints_percentage:.1f}% )", ("Arial", 12), 1, 1],
            [self.album_frame, "Favourite Album:", (menu_font, 12), 0, None],
            [self.album_frame, f"{favourite_album}", ("Arial", 10), 1, None],
            [self.album_frame, f"{release_date}", ("Arial", 10), 2, None],
            [self.album_frame, f"Correct Answers:\n({correct_album_answers}/{album_questions}  {album_percentage:.1f}%)", ("Arial", 10), 3, None]
        ]

        # make the labels
        stats_label_ref = []
        for item in stats_label_list:
            make_label = Label(item[0], text=item[1], font=item[2],
                               fg=menu_fg, bg=menu_bg)
            make_label.grid(row=item[3], column=item[4])

            stats_label_ref.append(make_label)

        # use pillow to resize album cover
        og_album_cover = Image.open(image_file)
        resized_cover = og_album_cover.resize((160, 160))

        # image file
        self.album_cover = ImageTk.PhotoImage(resized_cover)

        # add the image
        self.fav_album_cover = Label(self.stats_container, image=self.album_cover)
        self.fav_album_cover.grid(row=2, column=1)


    def close_stats(self, parent):
        """destroys/closes stats menu"""
        parent.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main
if __name__ == "__main__":
    root = Tk()
    root.title("Lyrics Quiz")
    StartMenu()
    root.mainloop()