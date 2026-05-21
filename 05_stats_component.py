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


    def to_stats(self):
        """Opens StatsMenu class"""

        self.stats_button.config(state=DISABLED)

        # retrieve stats
        retrieved_stats = [0, 10]

        # open menu
        StatsMenu(self, retrieved_stats)


class StatsMenu:
    """the stats menu"""

    def __init__(self, parent, user_stats):
        """initialise menu"""

        # import fonts
        load_fonts()

        # get design details
        [menu_font, menu_fg, btn_bg, menu_bg, image_file] = af.get_album_details("Favourite Worst Nightmare")

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

        # list containing all the stats labels
        # root | text | font | row | column
        stats_label_list = [
            [self.stats_container, "Correct Answers:", (menu_font, 12), 0, 0],
            [self.stats_container, "## / ##  ( ##% )", ("Arial", 12), 0, 1],
            [self.stats_container, "Hints Used:", (menu_font, 12), 1, 0],
            [self.stats_container, "## / ##  ( ##% )", ("Arial", 12), 1, 1],
            [self.album_frame, "Favourite Album:", (menu_font, 12), 0, None],
            [self.album_frame, "Album Name", ("Arial", 10), 1, None],
            [self.album_frame, "release date", ("Arial", 10), 2, None],
            [self.album_frame, "Correct Answers:\n(#/#  #%)", ("Arial", 10), 3, None]
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