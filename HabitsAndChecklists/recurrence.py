import calendar as cal
import datetime as dt
from abc import ABC, abstractmethod
from enum import Enum

from DataManagement.DataHelpers.dataEquivalent import DataEquivalent
from DataManagement.DataHelpers.textEquivalent import TextEquivalent
from DateAndTime.calendarObjects import CalendarObjects, MonthEnum, WeekdayEnum
from VisualsAndOutput.userOutput import UserOutput


class RecurrencePeriod(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    DAYS_OF_MONTH_K = "days of month k"
    NTH_WEEKDAY_M_OF_MONTH_K = "nth weekday m of month k"
    ONCE = "once"
    AGGREGATE = "aggregate"



class Recurrence(TextEquivalent, DataEquivalent, ABC):
    RECURRENCE_PERIOD_NAME_TO_ID = {rp.value: rp for rp in RecurrencePeriod}
    recurrencePeriod = None

    def __init__(self):
        "no specialized constructor necessary"


    @abstractmethod
    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        raise NotImplementedError("method not yet implemented in subclass")

    
    @abstractmethod
    def prevOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        raise NotImplementedError("method not yet implemented in subclass")


    def isToday(self, referenceDate: dt.date=dt.date.today()) -> bool:
        nextOcc = self.nextOccurrence(referenceDate=referenceDate)
        return nextOcc == referenceDate


    def toText(self, verbosity: int=0, indent=0) -> str:
        indentA = UserOutput.indentPadding(indent=indent)
        text = ""
        if verbosity >= 0:
            text += f"{indentA}recurrence: {self.recurrencePeriod.value}"
        return text
    

    def toData(self, subData) -> dict:
        return {
            "recurrence type": self.recurrencePeriod.value,
            "details": subData,
        }


    @staticmethod
    def fromData(data):
        fromDataMethodDict = {
            RecurrencePeriod.DAILY: DailyRecurrence.fromData,
            RecurrencePeriod.WEEKLY: WeeklyRecurrence.fromData,
            RecurrencePeriod.MONTHLY: MonthlyRecurrence.fromData,
            RecurrencePeriod.YEARLY: YearlyRecurrence.fromData,
            RecurrencePeriod.DAYS_OF_MONTH_K: DaysOfMonthKRecurrence.fromData,
            RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K: NthWeekdayMOfMonthKRecurrence.fromData,
            RecurrencePeriod.ONCE: OnceRecurrence.fromData,
            RecurrencePeriod.AGGREGATE: AggregateRecurrence.fromData,
        }

        recurrencePeriodName = data["recurrence type"]
        recurrencePeriod = Recurrence.RECURRENCE_PERIOD_NAME_TO_ID[recurrencePeriodName]

        try: 
            fromDataMethod = fromDataMethodDict[recurrencePeriod]
        except KeyError:
            raise NotImplementedError(f"recurrence type {recurrencePeriodName} not handled")
        
        return fromDataMethod(data)



class DailyRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.DAILY

    def __init__(self):
        "no specialized constructor necessary"


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        return referenceDate

    
    def prevOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        return referenceDate

    
    def toText(self, verbosity: int=0, indent: int=0) -> str:
        text = ""
        if verbosity >= 0:
            text += super().toText(verbosity=verbosity, indent=indent)
        return text


    def toData(self):
        data = {}
        return super().toData(data)


    @staticmethod
    def fromData(data):
        return DailyRecurrence()



class WeeklyRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.WEEKLY

    def __init__(self, weekdays: list[WeekdayEnum]):
        self.weekdays = weekdays
        self.weekdayNames = [wday.value.name for wday in weekdays]
        self.weekdayNums = [wday.value.num for wday in weekdays]


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.weekdays: return None
        weekday = referenceDate.weekday()
        daysLeft = min((wday - weekday) % 7 for wday in self.weekdayNums)
        return referenceDate + dt.timedelta(days=daysLeft)


    def prevOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.weekdays: return None
        weekday = referenceDate.weekday()
        daysAgo = min((weekday - wday) % 7 for wday in self.weekdayNums)
        return referenceDate - dt.timedelta(days=daysAgo)


    def toText(self, verbosity: int=0, indent: int=0) -> str:
        indentB = UserOutput.indentPadding(indent=indent+1)
        text = ""
        if verbosity >= 0:
            text += super().toText(verbosity=verbosity, indent=indent)
            weekdayNamesStr = ", ".join(self.weekdayNames)
            text += f"\n{indentB}{weekdayNamesStr}"
        return text


    def toData(self):
        data = {
            "weekday names": self.weekdayNames
        }
        return super().toData(data)


    @staticmethod
    def fromData(data):
        details = data["details"]
        weekdayNames = details["weekday names"]
        weekdayDict = CalendarObjects.WEEKDAY_NAME_TO_ID
        weekdays = [weekdayDict[weekdayName] for weekdayName in weekdayNames]
        return WeeklyRecurrence(weekdays)



class MonthlyRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.MONTHLY

    def __init__(self, days: list[int]):
        self.days = days


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if self.days == None: return None
        year = referenceDate.year
        month = referenceDate.month
        monthDay = referenceDate.day
        daysInMonth = cal.monthrange(year, month)[1]
        daysLeft = min((mday - monthDay) % daysInMonth for mday in self.days)
        return referenceDate + dt.timedelta(days=daysLeft)
    

    def prevOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if self.days == None: return None
        year = referenceDate.year
        month = referenceDate.month
        monthDay = referenceDate.day
        daysInPrevMonth = cal.monthrange(year, ((month - 2) % 12) + 1)[1]
        daysAgo = min(((monthDay - mday) % daysInPrevMonth) for mday in self.days)
        return referenceDate - dt.timedelta(days=daysAgo)


    def toText(self, verbosity: int=0, indent: int=0) -> str:
        indentB = UserOutput.indentPadding(indent=indent+1)
        text = ""
        if verbosity >= 0:
            text += super().toText(verbosity=verbosity, indent=indent)
            daysStr = ", ".join(list(map(str, self.days)))
            text += f"\n{indentB}month days: {daysStr}"
        return text

    
    def toData(self):
        data = {
            "month days": self.days
        }
        return super().toData(data)


    @staticmethod
    def fromData(data):
        details = data["details"]
        days = details["month days"]
        return MonthlyRecurrence(days)



class YearlyRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.YEARLY

    def __init__(self, days: list[int]):
        self.days = days


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.days: 
            return None
        year = referenceDate.year
        yearDay = referenceDate.timetuple().tm_yday
        leapyear = cal.isleap(year)
        daysInYear = 365 + 1 * leapyear
        daysLeft = min((yday - yearDay) % daysInYear for yday in self.days)
        return referenceDate + dt.timedelta(days=daysLeft)

    
    def prevOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.days: 
            return None
        year = referenceDate.year
        yearDay = referenceDate.timetuple().tm_yday
        prevLeapyear = cal.isleap(year - 1)
        daysInPrevYear = 365 + 1 * prevLeapyear
        daysAgo = min(((yearDay - yday) % daysInPrevYear) for yday in self.days)
        return referenceDate - dt.timedelta(days=daysAgo)


    def toText(self, verbosity: int=0, indent: int=0) -> str:
        indentB = UserOutput.indentPadding(indent=indent+1)
        text = ""
        if verbosity >= 0:
            text += super().toText(verbosity=verbosity, indent=indent)
            daysStr = ", ".join(list(map(str, self.days)))
            text += f"\n{indentB}year days: {daysStr}"
        return text

    
    def toData(self):
        data = {
            "days of the year": self.days
        }
        return super().toData(data)


    @staticmethod
    def fromData(data):
        details = data["details"]
        days = details["days of the year"]
        return YearlyRecurrence(days)



class DaysOfMonthKRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.DAYS_OF_MONTH_K

    def __init__(self, month: MonthEnum, days: list[int]):
        self.month = month
        self.monthName = month.value.name
        self.monthNum = month.value.num
        self.days = days


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.days: 
            return None
        
        year = referenceDate.year
        month = referenceDate.month
        day = referenceDate.day
        firstDay = min(self.days)
        lastDay = max(self.days)

        if month > self.monthNum or (month == self.monthNum and day > lastDay):
            return dt.date(year + 1, self.monthNum, firstDay)
        elif month < self.monthNum:
            return dt.date(year, self.monthNum, firstDay)
        else:
            daysInMonth = cal.monthrange(year, month)[1]
            daysLeft = min((mday - day) % daysInMonth for mday in self.days)
            return referenceDate + dt.timedelta(days=daysLeft)


    def prevOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.days:
            return None
        
        year = referenceDate.year
        month = referenceDate.month
        day = referenceDate.day
        firstDay = min(self.days)
        lastDay = max(self.days)

        if month < self.monthNum or (month == self.monthNum and day < firstDay):
            return dt.date(year - 1, self.monthNum, lastDay)
        elif month > self.monthNum:
            return dt.date(year, self.monthNum, lastDay)
        else:
            daysInPrevMonth = cal.monthrange(year, month - 1)[1]
            daysAgo = min((day - mday) % daysInPrevMonth for mday in self.days)
            return referenceDate - dt.timedelta(days=daysAgo)


    def toText(self, verbosity: int=0, indent: int=0) -> str:
        indentB = UserOutput.indentPadding(indent=indent+1)
        text = ""
        if verbosity >= 0:
            text += super().toText(verbosity=verbosity, indent=indent)
            text += f"\n{indentB}month: {self.month.value.name}"
            daysStr = ", ".join(list(map(str, self.days)))
            text += f"\n{indentB}days: {daysStr}"
        return text
    

    def toData(self):
        data = {
            "month name": self.monthName,
            "days": self.days,
        }
        return super().toData(data)


    @staticmethod
    def fromData(data):
        details = data["details"]
        monthName = details["month name"]
        monthDict = CalendarObjects.MONTH_NAME_TO_ID
        month = monthDict[monthName]
        days = details["days"]
        return DaysOfMonthKRecurrence(month, days)



class NthWeekdayMOfMonthKRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K

    def __init__(self, month: MonthEnum, weekday: WeekdayEnum, n: int):
        self.month = month
        self.monthName = month.value.name
        self.monthNum = month.value.num
        self.weekday = weekday
        self.n = n


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        year = referenceDate.year
        month = referenceDate.month
        day = referenceDate.day

        if month > self.month.value.num: 
            firstDayOfMonth = dt.date(year + 1, self.monthNum, 1)
        else: 
            firstDayOfMonth = dt.date(year, self.monthNum, 1)

        weekdayOfFirst = firstDayOfMonth.weekday()
        weekdayNum = self.weekday.value.num
        daysFromFirstToNthWeekdayM = ((weekdayNum - weekdayOfFirst) % 7) + (7 * (self.n - 1))

        if month == self.month.value.num and day > 1 + daysFromFirstToNthWeekdayM:
            firstDayOfMonth = dt.date(year + 1, self.monthNum, 1)
            weekdayOfFirst = firstDayOfMonth.weekday()
            daysFromFirstToNthWeekdayM = ((weekdayNum - weekdayOfFirst) % 7) + (7 * (self.n - 1))

        return firstDayOfMonth + dt.timedelta(days=daysFromFirstToNthWeekdayM)


    def prevOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        year = referenceDate.year
        month = referenceDate.month
        day = referenceDate.day

        if month < self.month.value.num:
            firstDayOfMonth = dt.date(year - 1, self.monthNum, 1)
        else:
            firstDayOfMonth = dt.date(year, self.monthNum, 1)

        weekdayOfFirst = firstDayOfMonth.weekday()
        weekdayNum = self.weekday.value.num
        daysFromFirstToNthWeekdayM = ((weekdayNum - weekdayOfFirst) % 7) + (7 * (self.n - 1))

        if month == self.month.value.num and day < 1 + daysFromFirstToNthWeekdayM:
            firstDayOfMonth = dt.date(year - 1, self.monthNum, 1)
            weekdayOfFirst = firstDayOfMonth.weekday()
            daysFromFirstToNthWeekdayM = ((weekdayNum - weekdayOfFirst) % 7) + (7 * (self.n - 1))
        
        return firstDayOfMonth + dt.timedelta(days=daysFromFirstToNthWeekdayM)

    
    def toText(self, verbosity: int=0, indent: int=0) -> str:
        indentB = UserOutput.indentPadding(indent=indent+1)
        text = ""
        if verbosity >= 0:
            text += super().toText(verbosity=verbosity, indent=indent)
            numberSuffix = UserOutput.numberSuffix(self.n)
            text += f"\n{indentB}{self.n}{numberSuffix} {self.weekday.value.name} of {self.month.value.name}"
        return text
    

    def toData(self):
        data = {
            "month name": self.month.value.name,
            "weekday name": self.weekday.value.name,
            "n": self.n,
        }
        return super().toData(data)


    @staticmethod
    def fromData(data):
        details = data["details"]
        monthName = details["month name"]
        monthDict = CalendarObjects.MONTH_NAME_TO_ID
        month = monthDict[monthName]
        weekdayName = details["weekday name"]
        weekdayDict = CalendarObjects.WEEKDAY_NAME_TO_ID
        weekday = weekdayDict[weekdayName]
        n = details["n"]
        return NthWeekdayMOfMonthKRecurrence(month, weekday, n)



class OnceRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.ONCE

    def __init__(self, date: dt.date):
        self.date = date


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if referenceDate > self.date: 
            nextOcc = None
        else: 
            nextOcc = self.date
        
        return nextOcc

    
    def prevOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if referenceDate < self.date:
            prevOcc = None
        else:
            prevOcc = self.date
        
        return prevOcc


    def toText(self, verbosity: int=0, indent: int=0) -> str:
        indentB = UserOutput.indentPadding(indent=indent+1)
        text = ""
        if verbosity >= 0:
            text += super().toText(verbosity=verbosity, indent=indent)
            text += f"\n{indentB}{self.date.strftime(CalendarObjects.DATE_STR_TEXT_OUTPUT_FORMAT)}"
        return text

    
    def toData(self):
        data = {
            "date": self.date.strftime(CalendarObjects.DATE_STR_DATA_FORMAT)
        }
        return super().toData(data)


    @staticmethod
    def fromData(data):
        details = data["details"]
        dateStr = details["date"]
        date = dt.datetime.strptime(dateStr, CalendarObjects.DATE_STR_DATA_FORMAT).date()
        return OnceRecurrence(date)



class AggregateRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.AGGREGATE

    def __init__(self, recurrences: list[Recurrence]):
        self.recurrences = recurrences


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.recurrences: 
            return None

        soonestOccurrences = [recurrence.nextOccurrence(referenceDate=referenceDate) for recurrence in self.recurrences]
        filteredSoonest = list(filter(lambda nextOcc: nextOcc != None, soonestOccurrences))

        if len(filteredSoonest) == 0: 
            return None
        
        return min(filteredSoonest)

    
    def prevOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.recurrences:
            return None
        
        mostRecentOccurrences = [recurrence.prevOccurrence(referenceDate=referenceDate) for recurrence in self.recurrences]
        filteredMostRecent = list(filter(lambda prevOcc: prevOcc != None, mostRecentOccurrences))

        if len(filteredMostRecent) == 0:
            return None
        
        return min(filteredMostRecent)

    
    def toText(self, verbosity: int=0, indent: int=0) -> str:
        text = ""
        if verbosity >= 0:
            text += super().toText(indent=indent)
        if verbosity >= 1:
            for recurrence in self.recurrences:
                text += f"\n{recurrence.toText(indent=indent+1)}"
        return text

    
    def toData(self) -> dict:
        data = {
            "recurrences": [recurrence.toData() for recurrence in self.recurrences]
        }
        return super().toData(data)


    @staticmethod
    def fromData(data: dict):
        details = data["details"]
        recurrenceData = details["recurrences"]
        recurrences = [Recurrence.fromData(recurrence) for recurrence in recurrenceData]
        return AggregateRecurrence(recurrences)
