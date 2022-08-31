from enum import Enum



class Color:
    def __init__(self, name, letter, rgb):
        self.name = name
        self.letter = letter
        self.rgb = rgb
        r, g, b = rgb
        self.code = f"\u001b[38;2;{r};{g};{b}m"



class ANSIEscapeSequence:
    def __init__(self, name, code):
        self.name = name
        self.code = code



class ColorEnum(Enum):
    DEFAULT = Color("default", "d", (210, 210, 210))
    RED = Color("red", "r", (230, 20, 60))
    GREEN = Color("green", "g", (0, 210, 90))
    BLUE = Color("blue", "b", (10, 110, 220))
    SKY = Color("cyan", "c", (120, 168, 240))
    YELLOW = Color("yellow", "y", (220, 220, 80))
    PURPLE = Color("purple", "p", (160, 30, 240))
    # green 30, 200, 120
    # default 204, 204, 204



class ANSIEscapeSequenceEnum(Enum):
    BOLD = ANSIEscapeSequence("bold", "\u001b[1m")
    RESET = ANSIEscapeSequence("reset", "\u001b[0m")
    