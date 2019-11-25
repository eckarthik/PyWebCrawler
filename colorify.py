import os, sys

if sys.platform.lower() == "win32":
    os.system('color')

class Colorify:
    """To make the CLI outputs look colorful"""

    colors = {
    'HEADER':'\033[95m',
    "OKBLUE":'\033[94m',
    "OKGREEN":'\033[92m',
    "WARNING":'\033[93m',
    "FAIL":'\033[91m',
    "ENDCOLOR":'\033[0m',
    "BOLD":'\033[01m',
    "UNDERLINE":'\033[4m',
    "BLACK":'\033[30m',
    "RED":'\033[31m',
    "GREEN":'\033[32m',
    "ORANGE":'\033[33m',
    "BLUE":'\033[34m',
    "PURPLE":'\033[35m',
    "CYAN":'\033[36m',
    "LIGHTGREY":'\033[37m',
    "DARKGREY":'\033[90m',
    "LIGHTRED":'\033[91m',
    "LIGHTGREEN":'\033[92m',
    "YELLOW":'\033[93m',
    "LIGHTBLUE":'\033[94m',
    "PINK":'\033[95m',
    "LIGHTCYAN":'\033[96m'}

    @staticmethod
    def colorify(text,color,bold=False):
        if bold:
            return Colorify.colors['BOLD']+Colorify.colors[color]+str(text)+Colorify.colors['ENDCOLOR']
        else:
            return Colorify.colors[color]+str(text)+Colorify.colors['ENDCOLOR']