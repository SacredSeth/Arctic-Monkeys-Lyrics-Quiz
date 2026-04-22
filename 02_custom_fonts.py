from tkinter import *
from tkextrafont import Font
import albumfonts as af


class StartMenu:
    """
    start menu
    """
    def __init__(self):

        self.start_frame = Frame(padx=15, pady=15)
        self.start_frame.grid()

        for i, v in enumerate(af.file_list):
            font_family = af.font_families[i]
            custom_font = Font(file=v, family=font_family)
            self.test_text = Label(self.start_frame, text=font_family,
                                   font=custom_font)
            self.test_text.grid(row=i)


# Main
if __name__ == "__main__":
    root = Tk()
    root.title("Lyrics Quiz")
    StartMenu()
    root.mainloop()