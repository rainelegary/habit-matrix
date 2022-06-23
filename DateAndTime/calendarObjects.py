from enum import Enum



class Weekday:
    def __init__(self, name: str, num: int):
        self.name: str = name
        self.num: int = num



class WeekdayEnum(Enum):
    MONDAY = Weekday("monday", 0)
    TUESDAY = Weekday("tuesday", 1)
    WEDNESDAY = Weekday("wednesday", 2)
    THURSDAY = Weekday("thursday", 3)
    FRIDAY = Weekday("friday", 4)
    SATURDAY = Weekday("saturday", 5)
    SUNDAY = Weekday("sunday", 6)



class CalendarObjects:
    WEEKDAY_ID_TO_OBJ: dict[WeekdayEnum, Weekday]
    WEEKDAY_NAME_TO_ID: dict[str, WeekdayEnum]
    WEEKDAY_NUM_TO_ID: dict[int, WeekdayEnum]
    WEEKDAY_NAME_TO_NUM: dict[str, int]
    WEEKDAY_NUM_TO_NAME: dict[int, str]


    @classmethod
    def initializeClassVariables(cls):
        cls.initializeWeekdayDicts()


    @classmethod
    def initializeWeekdayDicts(cls):
        cls.WEEKDAY_ID_TO_OBJ = {}
        for weekday in WeekdayEnum:
            cls.WEEKDAY_ID_TO_OBJ[weekday] = weekday.value

        cls.WEEKDAY_NAME_TO_ID = {}
        for weekday in cls.WEEKDAY_ID_TO_OBJ:
            cls.WEEKDAY_NAME_TO_ID[weekday.value.name] = weekday

        cls.WEEKDAY_NUM_TO_ID = {}
        for weekday in cls.WEEKDAY_ID_TO_OBJ:
            cls.WEEKDAY_NUM_TO_ID[weekday.value.num] = weekday

        cls.WEEKDAY_NAME_TO_NUM = {}
        for weekday in cls.WEEKDAY_ID_TO_OBJ:
            cls.WEEKDAY_NAME_TO_NUM[weekday.value.name] = weekday.value.num

        cls.WEEKDAY_NUM_TO_NAME = {}
        for weekday in cls.WEEKDAY_ID_TO_OBJ:
            cls.WEEKDAY_NUM_TO_NAME[weekday.value.num] = weekday.value.name
        


CalendarObjects.initializeClassVariables()

