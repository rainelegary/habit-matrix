from enum import Enum

from DataManagement.DataHelpers.dataEquivalent import DataEquivalent



class Weekday:
    def __init__(self, name: str, num: int):
        self.name = name
        self.num = num



class Month:
    def __init__(self, name: str, num: int):
        self.name = name 
        self.num = num



# class MonthAndYear(DataEquivalent):
#     def __init__(self, monthName: str, year: int):
#         self.monthName = monthName
#         self.year = year
    

#     def toData(self) -> str:
#         return f"{self.monthName} {self.year}"
    

#     def fromData(self, data: str):
#         monthName, yearStr = data.split()
#         year = int(yearStr)
#         return MonthAndYear(monthName, year)



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
    DATE_STR_DATA_FORMAT = f"%b %d, %Y"
    DATE_STR_TEXT_OUTPUT_FORMAT = f"%b %d, %Y"
    DATE_STR_TEXT_INPUT_FORMAT = f"%b %d, %Y"
    DATE_STR_TEXT_INPUT_FORMAT_EXAMPLE = f"mmm dd, yyyy"

    TIME_STR_DATA_FORMAT = f"%H:%M"
    TIME_STR_TEXT_OUTPUT_FORMAT = f"%H:%M"
    TIME_STR_TEXT_INPUT_FORMAT = f"%H:%M"
    TIME_STR_TEXT_INPUT_FORMAT_EXAMPLE = f"hh:mm"

    WEEKDAY_NAME_TO_ID: dict[str, WeekdayEnum] = {weekday.value.name: weekday for weekday in WeekdayEnum}
    WEEKDAY_NUM_TO_ID: dict[int, WeekdayEnum] = {weekday.value.num: weekday for weekday in WeekdayEnum}
    WEEKDAY_NAME_TO_NUM: dict[str, int] = {weekday.value.name: weekday.value.num for weekday in WeekdayEnum}
    WEEKDAY_NUM_TO_NAME: dict[int, str] = {weekday.value.num: weekday.value.name for weekday in WeekdayEnum}

    WEEKDAY_NAMES: list[str] = [weekday.value.name for weekday in WeekdayEnum]
    WEEKDAY_NUMS: list[int] = [weekday.value.num for weekday in WeekdayEnum]
        
    MONTH_NAME_TO_ID: dict[str, MonthEnum] = {month.value.name: month for month in MonthEnum}
    MONTH_NUM_TO_ID: dict[int, MonthEnum] = {month.value.num: month for month in MonthEnum}
    MONTH_NAME_TO_NUM: dict[str, int] = {month.value.name: month.value.num for month in MonthEnum}
    MONTH_NUM_TO_NAME: dict[int, str] = {month.value.num: month.value.name for month in MonthEnum}

    MONTH_NAMES: list[str] = [month.value.name for month in MonthEnum]
    MONTH_NUMS: list[int] = [month.value.num for month in MonthEnum]

