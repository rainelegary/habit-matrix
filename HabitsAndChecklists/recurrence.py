from enum import Enum
from abc import ABC, abstractmethod
import time
import datetime as dt
import calendar as cal



class RecurrencePeriod(Enum):
    DAILY = 1

    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4

    DAYS_OF_MONTH_K = 5
    NTH_WEEKDAY_M_OF_MONTH_K = 6

    ONCE = 7

    AGGREGATE = 8



class Recurrence(ABC):
    def __init__(self, period: RecurrencePeriod):
        self.period: RecurrencePeriod = period


    @staticmethod
    @abstractmethod
    def setupPrompt() -> None:
        raise NotImplementedError("method not yet implemented in subclass")


    @abstractmethod
    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        raise NotImplementedError("method not yet implemented in subclass")


    def isToday(self, referenceTime=dt.datetime.now()) -> bool:
        nextOcc = self.nextOccurrence(referenceTime=referenceTime)
        return nextOcc == referenceTime



class DailyRecurrence(Recurrence):
    def __init__(self):
        super().__init__(RecurrencePeriod.DAILY)


    @staticmethod
    def setupPrompt() -> None:
        # generate a never recurrence if needed
        # generate an aggregate recurrence if needed
        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        return referenceTime



class WeeklyRecurrence(Recurrence):
    def __init__(self, days: list[int]):
        super().__init__(RecurrencePeriod.WEEKLY)
        self.days = days


    @staticmethod
    def setupPrompt() -> None:
        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        if not self.days: return None
        weekday = referenceTime.weekday()
        daysLeft = min((wday - weekday) % 7 for wday in self.days)
        return referenceTime + dt.timedelta(days=daysLeft)


    # def isToday(self, referenceTime=dt.datetime.now()) -> bool:
    #     weekday = referenceTime.weekday()
    #     daysLeft = min((wday - weekday) % 7 for wday in self.days)
    #     return daysLeft == 0



class MonthlyRecurrence(Recurrence):
    def __init__(self, days: list[int]):
        super().__init__(RecurrencePeriod.MONTHLY)
        self.days = days


    @staticmethod
    def setupPrompt() -> None:
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



class YearlyRecurrence(Recurrence):
    def __init__(self, days: list[int]):
        super().__init__(RecurrencePeriod.YEARLY)
        self.days = days

    
    @staticmethod
    def setupPrompt() -> None:
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



class OnceRecurrence(Recurrence):
    def __init__(self, month: str, day: int, year: int):
        super().__init__(RecurrencePeriod.ONCE)
        self.year = year
        self.month = month
        self.day = day
        self.yearDay = dt.datetime(year, month, day).timetuple().tm_yday


    @staticmethod
    def setupPrompt() -> None:
        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        year = referenceTime.year
        yearDay = referenceTime.timetuple().tm_yday
        hasOccurred = (year > self.year) or (year == self.year and yearDay > self.yearDay)
        if hasOccurred: return None
        else: return dt.datetime(self.year, self.month, self.day)


    # def isToday(self, referenceTime=dt.datetime.now()) -> bool:
    #     return referenceTime.timetuple().tm_yday == self.yearDay and referenceTime.year == self.year



class DaysOfMonthKRecurrence(Recurrence):
    def __init__(self, month: int, days: list[int]):
        super().__init__(RecurrencePeriod.DAYS_OF_MONTH_K)
        self.month = month
        self.days = days


    @staticmethod
    def setupPrompt() -> None:
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



class NthWeekdayMOfMonthKRecurrence(Recurrence):
    def __init__(self, month: str, weekday: int, n: int):
        super().__init__(RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K)
        self.month = month
        self.weekday = weekday
        self.n = n
    

    @staticmethod
    def setupPrompt() -> None:
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



class AggregateRecurrence(Recurrence):
    def __init__(self, recurrences: list[Recurrence]):
        super().__init__(RecurrencePeriod.AGGREGATE)
        self.recurrences = recurrences
    

    @staticmethod
    def setupPrompt() -> None:
        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()) -> dt.datetime:
        if not self.recurrences: return None
        soonestOccurrences = [recurrence.nextOccurrence(referenceTime=referenceTime) for recurrence in self.recurrences]
        filteredOccurrences = list(filter(lambda nextOcc: nextOcc != None, soonestOccurrences))
        return min(filteredOccurrences)



