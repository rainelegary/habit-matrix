from enum import Enum



class Weekday:
    def __init__(self, name: str, num: int):
        self.name: str = name
        self.num: int = num



class Month:
    def __init__(self, name: str, num: int):
        self.name = name 
        self.num = num



class WeekdayEnum(Enum):
    MONDAY = Weekday("monday", 0)
    TUESDAY = Weekday("tuesday", 1)
    WEDNESDAY = Weekday("wednesday", 2)
    THURSDAY = Weekday("thursday", 3)
    FRIDAY = Weekday("friday", 4)
    SATURDAY = Weekday("saturday", 5)
    SUNDAY = Weekday("sunday", 6)



class MonthEnum(Enum):
    JANUARY = Month("january", 1)
    FEBRUARY = Month("february", 2)
    MARCH = Month("march", 3)
    APRIL = Month("april", 4)
    MAY = Month("may", 5)
    JUNE = Month("june", 6)
    JULY = Month("july", 7)
    AUGUST = Month("august", 8)
    SEPTEMBER = Month("september", 9)
    OCTOBER = Month("october", 10)
    NOVEMBER = Month("november", 11)
    DECEMBER = Month("december", 12)



class CalendarObjects:
    WEEKDAY_ID_TO_OBJ: dict[WeekdayEnum, Weekday] = {weekday: weekday.value for weekday in WeekdayEnum}
    WEEKDAY_NAME_TO_ID: dict[str, WeekdayEnum] = {weekday.value.name: weekday for weekday in WeekdayEnum}
    WEEKDAY_NUM_TO_ID: dict[int, WeekdayEnum] = {weekday.value.num: weekday for weekday in WeekdayEnum}
    WEEKDAY_NAME_TO_NUM: dict[str, int] = {weekday.value.name: weekday.value.num for weekday in WeekdayEnum}
    WEEKDAY_NUM_TO_NAME: dict[int, str] = {weekday.value.num: weekday.value.name for weekday in WeekdayEnum}

    WEEKDAY_NAMES: list[str] = [weekday.value.name for weekday in WeekdayEnum]
    WEEKDAY_NUMS: list[int] = [weekday.value.num for weekday in WeekdayEnum]
        
    MONTH_ID_TO_OBJ: dict[MonthEnum, Month] = {month: month.value for month in MonthEnum}
    MONTH_NAME_TO_ID: dict[str, MonthEnum] = {month.value.name: month for month in MonthEnum}
    MONTH_NUM_TO_ID: dict[int, MonthEnum] = {month.value.num: month for month in MonthEnum}
    MONTH_NAME_TO_NUM: dict[str, int] = {month.value.name: month.value.num for month in MonthEnum}
    MONTH_NUM_TO_NAME: dict[int, str] = {month.value.num: month.value.name for month in MonthEnum}

    MONTH_NAMES: list[str] = [month.value.name for month in MonthEnum]
    MONTH_NUMS: list[int] = [month.value.num for month in MonthEnum]

