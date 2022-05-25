# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

import re

# colors
red = "\033[38;2;255;100;100m"
dark_red = "\033[38;2;230;40;40m"
blue = "\033[38;2;100;100;255m"
orange = "\033[38;2;255;150;0m"
yellow = "\033[38;2;255;205;50m"
gray = "\033[38;2;140;140;140m"
reset = "\033[0m"
bold = "\033[1m"

# Color formating
colors = {
    "§B": bold,
    "§R": reset,
    "§r": red,
    "§o": orange,
    "§b": blue,
    "§y": yellow,
    "§g": gray,
}

colors_regex = re.compile("§[a-zA-Z]")

# Remove all the color codes in a string
def remove_colors(text):
    return colors_regex.sub("", text)


# Format all the color codes in a string
def format_colors(text):
    for key, value in colors.items():
        text = text.replace(key, value)
    return text
