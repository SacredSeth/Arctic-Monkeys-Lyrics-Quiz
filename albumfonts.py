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

# Button details for hints: fg | btn_bg | menu_bg
album_colours = [
    ["#000000", "#9EBCBB", "#9EBCBB"],
    ["#D0CB29", "#413D40", "#6C676B"],
    ["#FEFFE8", "#580641", "#580641"],
    ["#000000", "#FFF5EB", "#FFF5EB"],
    ["#FFFFFF", "#000000", "#000000"],
    ["#FFFFFF", "#381F0F", "#381F0F"]
]

# images of the album covers
album_images = [
    "Album Covers\Whatever.png",
    "Album Covers\Favourite.png",
    "Album Covers\Humbug.png",
    "Album Covers\Suck.png",
    "Album Covers\AM.png",
    "Album Covers\Tranquility.png"
]

def get_album_details(album):
    """
    returns all the details for a desired font
    :param album: the album/index of the desired font
    :return: list of details: Family | fg | bg(btn) | bg(menu) | cover
    """
    index = album_list.index(album)  # get index of album

    details = [
        font_families[index],
        album_colours[index][0],
        album_colours[index][1],
        album_colours[index][2],
        album_images[index]
    ]

    return details