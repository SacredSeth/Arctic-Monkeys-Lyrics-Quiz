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


class StartMenu:
    """the start menu"""

    def __init__(self):
        """initialise menu"""

        self.start_frame = Frame(padx=15, pady=15)
        self.start_frame.grid()

        self.stats_button = Button(self.start_frame, text="Stats",
                                   width=15, command=self.to_stats)
        self.stats_button.grid(row=0)

        # holds the amount of times an album shows up
        self.album_question_count = {
            "Whatever People Say I Am, That's What I'm Not" : 0,
            "Favourite Worst Nightmare" : 0,
            "Humbug" : 0,
            "Suck It and See" : 0,
            "AM" : 0,
            "Tranquility Base Hotel & Casino" : 0
        }
        # holds the amount of correctly answered questions per album
        self.album_answer_count = {
            "Whatever People Say I Am, That's What I'm Not": 0,
            "Favourite Worst Nightmare": 0,
            "Humbug": 0,
            "Suck It and See": 0,
            "AM": 0,
            "Tranquility Base Hotel & Casino": 0
        }

        # make fake test stats

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.correct_answers = IntVar()
        self.correct_answers.set(0)

        rounds_played = 0
        correct_answers = 0
        # randomly populate dictionaries
        for album in af.album_list:
            to_add = random.randint(0, 2)
            self.album_question_count[album] = to_add
            rounds_played += to_add

            correct = random.randint(0, to_add)
            self.album_answer_count[album] = correct
            correct_answers += correct

        # in case of rolling a 0, 6 times in a row
        if rounds_played == 0:
            self.album_question_count["AM"] = 1
            rounds_played += 1

        self.hints_used = IntVar()
        self.hints_used.set(random.randint(0, rounds_played * 2))
        self.rounds_played.set(rounds_played)
        self.correct_answers.set(correct_answers)


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

        # manual overwriting
        # retrieved_stats = [15, 9, 7, "AM", 6, 4]
        # retrieved_stats = [38, 24, 16, "Humbug", 14, 12]
        # retrieved_stats = [1, 0, 0, "Whatever People Say I Am, That's What I'm Not", 0, 0]

        # open menu
        StatsMenu(self, retrieved_stats)


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

        # in case the user does really bad / checks stats very early
        if correct_album_answers == 0:
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
    StartMenu()
    root.mainloop()