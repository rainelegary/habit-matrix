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
    DEFAULT = Color("default", "d", (204, 204, 204))
    RED = Color("red", "r", (220, 15, 20))
    GREEN = Color("green", "g", (30, 200, 120))
    BLUE = Color("blue", "b", (30, 120, 220))



class ANSIEscapeSequenceEnum(Enum):
    BOLD = ANSIEscapeSequence("bold", "\u001b[1m")
    RESET = ANSIEscapeSequence("reset", "\u001b[0m")
    