from enum import Enum
from abc import ABC, abstractmethod
import time
import datetime as dt
import calendar as cal
import textwrap
from UserInteraction.userIO import UserIO
from DateAndTime.calendar import Calendar

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
    # recurrenceTypes = [
    #     "daily",
    #     "weekly",
    #     "monthly",
    #     "yearly",
    #     "once",
    #     "days of month k",
    #     "nth weekday m of month k",
    #     "aggregate",
    # ]

    def __init__(self, period: RecurrencePeriod):
        self.period: RecurrencePeriod = period


    @staticmethod
    def setupPrompt():
        # choose type of recurrence
        prompt = "what kind of recurrence?\n"
        options = [rp.value for rp in RecurrencePeriod]
        recurrencePeriod = UserIO.singleSelectString(prompt=prompt, options=options)
        
        recurrence = None

        # call appropriate subclass method
        if recurrencePeriod == RecurrencePeriod.WEEKLY.value: recurrence = WeeklyRecurrence.setupPrompt()

        if recurrence == None: raise NotImplementedError("recurrence type not handled")

        # ask if user wants to save recurrence
        return recurrence


    @abstractmethod
    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        raise NotImplementedError("method not yet implemented in subclass")


    def isToday(self, referenceTime=dt.datetime.now()) -> bool:
        nextOcc = self.nextOccurrence(referenceTime=referenceTime)
        return nextOcc == referenceTime


    def toText(self, indent=0) -> str:
        text = f"recurrence: {self.period.value}\n"
        return super().indentText(text, indent)




class DailyRecurrence(Recurrence):
    def __init__(self):
        super().__init__(RecurrencePeriod.DAILY)


    @staticmethod
    def setupPrompt() -> Recurrence:

        # choose type of recurrence

        # configure settings

        # ask if user wants to save this recurrence

        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        return referenceTime

    
    def toText(self, indent: int=0) -> str:
        text = super().toText()
        
        return super().indentText(text, indent)



class WeeklyRecurrence(Recurrence):
    def __init__(self, days: list[int]):
        super().__init__(RecurrencePeriod.WEEKLY)
        self.days = days


    @staticmethod
    def setupPrompt() -> Recurrence:
        weekdayDict = Calendar.WEEKDAYS
        prompt = "which days of the week?"
        options = list(weekdayDict.keys())
        dayNames = UserIO.multiSelectString(prompt=prompt, options=options)
        dayNums = [weekdayDict[dayName] for dayName in dayNames]
        return WeeklyRecurrence(days=dayNums)


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        if not self.days: return None
        weekday = referenceTime.weekday()
        daysLeft = min((wday - weekday) % 7 for wday in self.days)
        return referenceTime + dt.timedelta(days=daysLeft)


    # def isToday(self, referenceTime=dt.datetime.now()) -> bool:
    #     weekday = referenceTime.weekday()
    #     daysLeft = min((wday - weekday) % 7 for wday in self.days)
    #     return daysLeft == 0


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
        # choose type of recurrence

        # configure settings

        # ask if user wants to save this recurrence
        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        if self.days == None: return None
        year = referenceTime.year
        month = referenceTime.month
        monthDay = referenceTime.day
        daysInMonth = cal.monthrange(year, month)[1]
        daysLeft = min((mday - monthDay) % daysInMonth for mday in self.days)
        return referenceTime + dt.timedelta(days=daysLeft)


    # def isToday(self, referenceTime=dt.datetime.now()) -> bool:
    #     return referenceTime.day in self.days


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
        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        if not self.days: return None
        year = referenceTime.year
        yearDay = referenceTime.timetuple().tm_yday
        leapyear = cal.isleap(year)
        daysInYear = 365 + 1 * leapyear
        daysLeft = min((yday - yearDay) % daysInYear for yday in self.days)
        return referenceTime + dt.timedelta(days=daysLeft)


    # def isToday(self, referenceTime=dt.datetime.now()) -> bool:
    #     return referenceTime.timetuple().tm_yday in self.days

    def toText(self, indent: int=0) -> str:
        text = super().toText()
        
        return super().indentText(text, indent)



class DaysOfMonthKRecurrence(Recurrence):
    def __init__(self, month: int, days: list[int]):
        super().__init__(RecurrencePeriod.DAYS_OF_MONTH_K)
        self.month = month
        self.days = days


    @staticmethod
    def setupPrompt() -> Recurrence:
        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        if not self.days: return None
        year = referenceTime.year
        month = referenceTime.month
        day = referenceTime.day
        if month > self.month:
            firstDay = min(self.days)
            return dt.datetime(year + 1, self.month, firstDay)
        elif month < self.month:
            return dt.datetime(year, self.month, firstDay)
        else:
            daysInMonth = cal.monthrange(year, month)[1]
            daysLeft = min((mday - day) % daysInMonth for mday in self.days)
            return referenceTime + dt.timedelta(days=daysLeft)


    # def isToday(self, referenceTime=dt.datetime.now()) -> bool:
    #     month = referenceTime.month
    #     day = referenceTime.day
    #     return (month == self.month) and (day in self.days)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        
        return super().indentText(text, indent)



class NthWeekdayMOfMonthKRecurrence(Recurrence):
    def __init__(self, month: str, weekday: int, n: int):
        super().__init__(RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K)
        self.month = month
        self.weekday = weekday
        self.n = n
    

    @staticmethod
    def setupPrompt() -> Recurrence:
        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        year = referenceTime.year
        month = referenceTime.month
        day = referenceTime.day

        if month > self.month: 
            theFirst = dt.datetime(year + 1, month, 1)
        else: 
            theFirst = dt.datetime(year, month, 1)

        weekdayOfFirst = theFirst.weekday()
        daysFromFirstToNthWeekdayM = ((self.weekday - weekdayOfFirst) % 7) + (7 * (self.n - 1))

        if month == self.month and day > 1 + daysFromFirstToNthWeekdayM:
            theFirst = dt.datetime(year + 1, month, 1)
            weekdayOfFirst = theFirst.weekday()
            daysFromFirstToNthWeekdayM = ((self.weekday - weekdayOfFirst) % 7) + (7 * (self.n - 1))

        return theFirst + dt.timedelta(days=daysFromFirstToNthWeekdayM)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        
        return super().indentText(text, indent)



class OnceRecurrence(Recurrence):
    def __init__(self, month: str, day: int, year: int):
        super().__init__(RecurrencePeriod.ONCE)
        self.year = year
        self.month = month
        self.day = day
        self.yearDay = dt.datetime(year, month, day).timetuple().tm_yday


    @staticmethod
    def setupPrompt() -> Recurrence:
        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        year = referenceTime.year
        yearDay = referenceTime.timetuple().tm_yday
        hasOccurred = (year > self.year) or (year == self.year and yearDay > self.yearDay)
        if hasOccurred: return None
        else: return dt.datetime(self.year, self.month, self.day)


    # def isToday(self, referenceTime=dt.datetime.now()) -> bool:
    #     return referenceTime.timetuple().tm_yday == self.yearDay and referenceTime.year == self.year


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        
        return super().indentText(text, indent)



class AggregateRecurrence(Recurrence):
    def __init__(self, recurrences: list[Recurrence]):
        super().__init__(RecurrencePeriod.AGGREGATE)
        self.recurrences = recurrences
    

    @staticmethod
    def setupPrompt() -> Recurrence:
        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        if not self.recurrences: return None
        soonestOccurrences = [recurrence.nextOccurrence(referenceTime=referenceTime) for recurrence in self.recurrences]
        filteredOccurrences = list(filter(lambda nextOcc: nextOcc != None, soonestOccurrences))
        return min(filteredOccurrences)

    
    def toText(self, indent: int=0) -> str:
        text = super().toText()
        
        return super().indentText(text, indent)



