from enum import Enum
from abc import ABC, abstractmethod
import time
import datetime as dt
import calendar as cal
import textwrap

from sympy import O
from UserInteraction.userIO import UserIO
from DateAndTime.calendar import Calendar
from DateAndTime.calendarObjects import CalendarObjects, MonthEnum, WeekdayEnum


from DataObjectConversion.textEquivalent import TextEquivalent



class RecurrencePeriod(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    DAYS_OF_MONTH_K = "days of month k"
    NTH_WEEKDAY_M_OF_MONTH_K = "nth weekday m of month k"
    ONCE = "once"
    AGGREGATE = "aggregate"



class Recurrence(TextEquivalent, ABC):
    def __init__(self, period: RecurrencePeriod):
        self.period: RecurrencePeriod = period


    @staticmethod
    def setupPrompt():
        # choose type of recurrence
        prompt = "what kind of recurrence?"
        options = [rp.value for rp in RecurrencePeriod]
        recurrencePeriod = UserIO.singleSelectString(prompt=prompt, options=options)
        
        recurrence = None

        # call appropriate subclass method
        if recurrencePeriod == RecurrencePeriod.DAILY.value: recurrence = DailyRecurrence.setupPrompt()
        if recurrencePeriod == RecurrencePeriod.WEEKLY.value: recurrence = WeeklyRecurrence.setupPrompt()
        if recurrencePeriod == RecurrencePeriod.MONTHLY.value: recurrence = MonthlyRecurrence.setupPrompt()
        if recurrencePeriod == RecurrencePeriod.YEARLY.value: recurrence = YearlyRecurrence.setupPrompt()
        if recurrencePeriod == RecurrencePeriod.DAYS_OF_MONTH_K.value: recurrence = DaysOfMonthKRecurrence.setupPrompt()
        if recurrencePeriod == RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K.value: recurrence = NthWeekdayMOfMonthKRecurrence.setupPrompt()
        if recurrencePeriod == RecurrencePeriod.ONCE.value: recurrence = OnceRecurrence.setupPrompt()
        if recurrencePeriod == RecurrencePeriod.AGGREGATE.value: recurrence = AggregateRecurrence.setupPrompt()

        if recurrence == None: raise NotImplementedError(f"recurrence type {recurrencePeriod} not handled")

        # ask if user wants to save recurrence
        return recurrence


    @abstractmethod
    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.datetime:
        raise NotImplementedError("method not yet implemented in subclass")


    def isToday(self, referenceDate: dt.date=dt.date.today()) -> bool:
        nextOcc = self.nextOccurrence(referenceDate=referenceDate)
        return nextOcc == referenceDate


    def toText(self, indent=0) -> str:
        text = f"recurrence: {self.period.value}"
        return super().indentText(text, indent)



class DailyRecurrence(Recurrence):
    def __init__(self):
        super().__init__(RecurrencePeriod.DAILY)


    @staticmethod
    def setupPrompt() -> Recurrence:
        return DailyRecurrence()


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.datetime:
        return referenceDate

    
    def toText(self, indent: int=0) -> str:
        text = super().toText()
        return super().indentText(text, indent)



class WeeklyRecurrence(Recurrence):
    def __init__(self, weekdays: list[WeekdayEnum]):
        super().__init__(RecurrencePeriod.WEEKLY)
        self.weekdays = weekdays


    @staticmethod
    def setupPrompt() -> Recurrence:
        dayNames = UserIO.multiSelectString("which weekdays? ", CalendarObjects.WEEKDAY_NAMES)
        dayNums = sorted([CalendarObjects.WEEKDAY_NAME_TO_NUM[dayName] for dayName in dayNames])
        weekdays = [CalendarObjects.WEEKDAY_NUM_TO_ID[dayNum] for dayNum in dayNums]
        return WeeklyRecurrence(weekdays)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.datetime:
        if not self.weekdays: return None
        weekday = referenceDate.weekday()
        weekdayNums = [CalendarObjects.WEEKDAY_ID_TO_OBJ[wday].num for wday in self.weekdays]
        daysLeft = min((wday - weekday) % 7 for wday in weekdayNums)
        return referenceDate + dt.timedelta(days=daysLeft)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        text += f"  days: {self.days}"
        return super().indentText(text, indent)



class MonthlyRecurrence(Recurrence):
    def __init__(self, days: list[int]):
        super().__init__(RecurrencePeriod.MONTHLY)
        self.days = days


    @staticmethod
    def setupPrompt() -> Recurrence:
        days = UserIO.getIntListInput("which days of the month? ")
        return MonthlyRecurrence(days)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.datetime:
        if self.days == None: return None
        year = referenceDate.year
        month = referenceDate.month
        monthDay = referenceDate.day
        daysInMonth = cal.monthrange(year, month)[1]
        daysLeft = min((mday - monthDay) % daysInMonth for mday in self.days)
        return referenceDate + dt.timedelta(days=daysLeft)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        text += f"  days: {self.days}"
        return super().indentText(text, indent)



class YearlyRecurrence(Recurrence):
    def __init__(self, days: list[int]):
        super().__init__(RecurrencePeriod.YEARLY)
        self.days = days

    
    @staticmethod
    def setupPrompt() -> Recurrence:
        days = UserIO.getIntListInput("which days of the year? ")
        return YearlyRecurrence(days)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.datetime:
        if not self.days: return None
        year = referenceDate.year
        yearDay = referenceDate.timetuple().tm_yday
        leapyear = cal.isleap(year)
        daysInYear = 365 + 1 * leapyear
        daysLeft = min((yday - yearDay) % daysInYear for yday in self.days)
        return referenceDate + dt.timedelta(days=daysLeft)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        text += f"  days: {self.days}"
        return super().indentText(text, indent)



class DaysOfMonthKRecurrence(Recurrence):
    def __init__(self, month: MonthEnum, days: list[int]):
        super().__init__(RecurrencePeriod.DAYS_OF_MONTH_K)
        self.month = month
        self.days = days


    @staticmethod
    def setupPrompt() -> Recurrence:
        monthName = UserIO.singleSelectString("which month? ", CalendarObjects.MONTH_NAMES)
        month = CalendarObjects.MONTH_NAME_TO_ID[monthName]
        days = UserIO.getIntListInput(prompt=f"which days of {monthName}? ")
        return DaysOfMonthKRecurrence(month, days)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.datetime:
        if not self.days: return None
        year = referenceDate.year
        month = referenceDate.month
        day = referenceDate.day
        if month > self.month:
            firstDay = min(self.days)
            return dt.datetime(year + 1, self.month, firstDay)
        elif month < self.month:
            return dt.datetime(year, self.month, firstDay)
        else:
            daysInMonth = cal.monthrange(year, month)[1]
            daysLeft = min((mday - day) % daysInMonth for mday in self.days)
            return referenceDate + dt.timedelta(days=daysLeft)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        text += f"  month: {self.month.value.name}\n"
        text += f"  days: {self.days}"
        return super().indentText(text, indent)



class NthWeekdayMOfMonthKRecurrence(Recurrence):
    def __init__(self, month: MonthEnum, weekday: WeekdayEnum, n: int):
        super().__init__(RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K)
        self.month = month
        self.weekday = weekday
        self.n = n
    

    @staticmethod
    def setupPrompt() -> Recurrence:
        monthName = UserIO.singleSelectString("which month? ", CalendarObjects.MONTH_NAMES)
        weekdayName = UserIO.singleSelectString("which weekday? ", CalendarObjects.WEEKDAY_NAMES)
        n = UserIO.getIntInput(f"which (n)th occurrence of {weekdayName} in {monthName}")
        month = CalendarObjects.MONTH_NAME_TO_ID[monthName]
        weekday = CalendarObjects.WEEKDAY_NAME_TO_ID[weekdayName]
        return NthWeekdayMOfMonthKRecurrence(month, weekday, n)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.datetime:
        year = referenceDate.year
        month = referenceDate.month
        day = referenceDate.day

        if month > self.month.num: 
            theFirst = dt.datetime(year + 1, month, 1)
        else: 
            theFirst = dt.datetime(year, month, 1)

        weekdayOfFirst = theFirst.weekday()
        weekdayNum = self.weekday.value.num
        daysFromFirstToNthWeekdayM = ((weekdayNum - weekdayOfFirst) % 7) + (7 * (self.n - 1))

        if month == self.month and day > 1 + daysFromFirstToNthWeekdayM:
            theFirst = dt.datetime(year + 1, month, 1)
            weekdayOfFirst = theFirst.weekday()
            daysFromFirstToNthWeekdayM = ((weekdayNum - weekdayOfFirst) % 7) + (7 * (self.n - 1))

        return theFirst + dt.timedelta(days=daysFromFirstToNthWeekdayM)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        text += f"  occurrence {self.n} of {self.weekday.value.name} in {self.month.value.name}"
        return super().indentText(text, indent)



class OnceRecurrence(Recurrence):
    def __init__(self, occurrence: dt.datetime):
        super().__init__(RecurrencePeriod.ONCE)
        self.occurrence = occurrence
        self.year = occurrence.year
        self.monthName = CalendarObjects.MONTH_NUM_TO_NAME[occurrence.month]
        self.day = occurrence.day


    @staticmethod
    def setupPrompt() -> Recurrence:
        month = UserIO.getIntInput("which month? ")
        day = UserIO.getIntInput("which day? ")
        year = UserIO.getIntInput("which year? ")
        occurrence = dt.datetime(year, month, day)
        return OnceRecurrence(occurrence)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.datetime:
        hasOccurred = referenceDate > self.occurrence
        if hasOccurred: return None
        else: return self.occurrence


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        text += f"  occurrence: {self.monthName} {self.day}, {self.year}"
        return super().indentText(text, indent)



class AggregateRecurrence(Recurrence):
    def __init__(self, recurrences: list[Recurrence]):
        super().__init__(RecurrencePeriod.AGGREGATE)
        self.recurrences = recurrences
    

    @staticmethod
    def setupPrompt() -> Recurrence:
        pass


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.datetime:
        if not self.recurrences: return None
        soonestOccurrences = [recurrence.nextOccurrence(referenceDate=referenceDate) for recurrence in self.recurrences]
        filteredOccurrences = list(filter(lambda nextOcc: nextOcc != None, soonestOccurrences))
        return min(filteredOccurrences)

    
    def toText(self, indent: int=0) -> str:
        text = super().toText()
        
        return super().indentText(text, indent)



