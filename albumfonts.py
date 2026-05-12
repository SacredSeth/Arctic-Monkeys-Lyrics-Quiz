# Ordered list of albums where the index corresponds
# to the font details in the other lists
album_list = ["Whatever People Say I Am, That's What I'm Not",
              "Favourite Worst Nightmare",
              "Humbug",
              "Suck It and See",
              "AM",
              "Tranquility Base Hotel & Casino"]

# list containing the file paths to the fonts
file_list = ["Fonts\AutourOne-Regular.ttf",
             "Fonts\JotiOne-Regular.ttf",
             "Fonts\RobotoSlab-Regular.ttf",
             "Fonts\SpecialGothicExpandedOne-Regular.ttf",
             "Fonts\LuckiestGuy-Regular.ttf",
             "Fonts\Sarpanch-Regular.ttf"]

# Names of the fonts / Font families
font_families = ["Autour One", "Joti One", "Roboto Slab",
                 "Special Gothic Expanded One", "Luckiest Guy", "Sarpanch"]

# Button details for hints: fg | bg
btn_details = [
    ["#000000", "#9EBCBB"],
    ["#D0CB29", "#413D40"],
    ["#FEFFE8", "#580641"],
    ["#000000", "#FFF5EB"],
    ["#FFFFFF", "#000000"],
    ["#FFFFFF", "#381F0F"]
]

def get_font_details(album):
    """
    returns all the details for a desired font
    :param album: the album/index of the desired font
    :return: list of details: Family | fg | bg
    """
    index = album_list.index(album)  # get index of album

    details = [
        font_families[index],
        btn_details[index][0],
        btn_details[index][1]
    ]
    return details