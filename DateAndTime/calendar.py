from DataObjectConversion.textEquivalent import TextEquivalent
from enum import Enum



class Weekday:
    def __init__(self, name: str, num: int):
        self.name = name
        self.num = num



class Weekdays(Enum):
    MONDAY = Weekday("monday", 0)
    TUESDAY = Weekday("tuesday", 1)





class Calendar(TextEquivalent):
    WEEKDAYS: dict[str, int] = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    MONTHS: dict[str, int] = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 11,
    }