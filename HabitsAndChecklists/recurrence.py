from enum import Enum
from abc import ABC, abstractmethod
import time
import datetime as dt
import calendar as cal
import textwrap

from UserInteraction.userInput import UserInput
from DateAndTime.calendar import Calendar
from DateAndTime.calendarObjects import CalendarObjects, MonthEnum, WeekdayEnum


from DataObjectConversion.textEquivalent import TextEquivalent
from UserInteraction.userOutput import UserOutput



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
    def __init__(self):
        "no specialized constructor necessary"


    @staticmethod
    def setupPrompt(indent: int=0) -> object:
        indentA = UserOutput.indentPadding(indent)
        indentB = UserOutput.indentPadding(indent + 1)
        print(f"{indentA}recurrence")
        prompt = f"what kind of recurrence?"
        options = [rp.value for rp in RecurrencePeriod]
        recurrencePeriod = UserInput.singleSelectString(prompt, options, indent=indent+1)
        
        recurrence = None

        # call appropriate subclass method
        if recurrencePeriod == RecurrencePeriod.DAILY.value: 
            recurrence = DailyRecurrence.setupPrompt(indent=indent+1)
        if recurrencePeriod == RecurrencePeriod.WEEKLY.value: 
            recurrence = WeeklyRecurrence.setupPrompt(indent=indent+1)
        if recurrencePeriod == RecurrencePeriod.MONTHLY.value: 
            recurrence = MonthlyRecurrence.setupPrompt(indent=indent+1)
        if recurrencePeriod == RecurrencePeriod.YEARLY.value: 
            recurrence = YearlyRecurrence.setupPrompt(indent=indent+1)
        if recurrencePeriod == RecurrencePeriod.DAYS_OF_MONTH_K.value: 
            recurrence = DaysOfMonthKRecurrence.setupPrompt(indent=indent+1)
        if recurrencePeriod == RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K.value: 
            recurrence = NthWeekdayMOfMonthKRecurrence.setupPrompt(indent=indent+1)
        if recurrencePeriod == RecurrencePeriod.ONCE.value: 
            recurrence = OnceRecurrence.setupPrompt(indent=indent+1)
        if recurrencePeriod == RecurrencePeriod.AGGREGATE.value: 
            recurrence = AggregateRecurrence.setupPrompt(indent=indent+1)

        if recurrence == None: raise NotImplementedError(f"recurrence type {recurrencePeriod} not handled")

        # ask if user wants to save recurrence
        return recurrence


    @abstractmethod
    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        raise NotImplementedError("method not yet implemented in subclass")


    def isToday(self, referenceDate: dt.date=dt.date.today()) -> bool:
        nextOcc = self.nextOccurrence(referenceDate=referenceDate)
        return nextOcc == referenceDate


    def toText(self, indent=0) -> str:
        text = f"recurrence: {self.recurrencePeriod.value}"
        return super().indentText(text, indent)



class DailyRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.DAILY

    def __init__(self):
        "no specialized constructor necessary"

    @staticmethod
    def setupPrompt(indent: int=0) -> Recurrence:
        indentA = UserOutput.indentPadding(indent)
        print(f"{indentA}{RecurrencePeriod.DAILY.value} recurrence")
        return DailyRecurrence()


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        return referenceDate

    
    def toText(self, indent: int=0) -> str:
        text = super().toText()
        return super().indentText(text, indent)



class WeeklyRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.WEEKLY

    def __init__(self, weekdays: list[WeekdayEnum]):
        self.weekdays = weekdays
        self.weekdayNames = [CalendarObjects.WEEKDAY_ID_TO_OBJ[wday].name for wday in self.weekdays]
        self.weekdayNums = [CalendarObjects.WEEKDAY_ID_TO_OBJ[wday].num for wday in self.weekdays]


    @staticmethod
    def setupPrompt(indent: int=0) -> Recurrence:
        indentA = UserOutput.indentPadding(indent)
        print(f"{indentA}{RecurrencePeriod.WEEKLY.value} recurrence")
        dayNames = UserInput.multiSelectString("which weekdays? ", CalendarObjects.WEEKDAY_NAMES, indent=indent+1)
        dayNums = sorted([CalendarObjects.WEEKDAY_NAME_TO_NUM[dayName] for dayName in dayNames])
        weekdays = [CalendarObjects.WEEKDAY_NUM_TO_ID[dayNum] for dayNum in dayNums]
        return WeeklyRecurrence(weekdays)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.weekdays: return None
        weekday = referenceDate.weekday()
        daysLeft = min((wday - weekday) % 7 for wday in self.weekdayNums)
        return referenceDate + dt.timedelta(days=daysLeft)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        text += f"\n{UserOutput.indentStyle}weekdays: {self.weekdayNames}"
        return super().indentText(text, indent)



class MonthlyRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.MONTHLY

    def __init__(self, days: list[int]):
        self.days = days


    @staticmethod
    def setupPrompt(indent: int=0) -> Recurrence:
        indentA = UserOutput.indentPadding(indent)
        indentB = UserOutput.indentPadding(indent + 1)
        print(f"{indentA}{RecurrencePeriod.MONTHLY.value} recurrence")
        days = UserInput.getIntListInput("which month days? ", indent=indent+1)
        return MonthlyRecurrence(days)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if self.days == None: return None
        year = referenceDate.year
        month = referenceDate.month
        monthDay = referenceDate.day
        daysInMonth = cal.monthrange(year, month)[1]
        daysLeft = min((mday - monthDay) % daysInMonth for mday in self.days)
        return referenceDate + dt.timedelta(days=daysLeft)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        text += f"\n{UserOutput.indentStyle}days of the month: {self.days}"
        return super().indentText(text, indent)



class YearlyRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.YEARLY

    def __init__(self, days: list[int]):
        self.days = days

    
    @staticmethod
    def setupPrompt(indent: int=0) -> Recurrence:
        indentA = UserOutput.indentPadding(indent)
        indentB = UserOutput.indentPadding(indent + 1)
        print(f"{indentA}{RecurrencePeriod.YEARLY.value} recurrence")
        days = UserInput.getIntListInput("which days of the year? ", indent=indent+1)
        return YearlyRecurrence(days)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.days: return None
        year = referenceDate.year
        yearDay = referenceDate.timetuple().tm_yday
        leapyear = cal.isleap(year)
        daysInYear = 365 + 1 * leapyear
        daysLeft = min((yday - yearDay) % daysInYear for yday in self.days)
        return referenceDate + dt.timedelta(days=daysLeft)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        text += f"\n{UserOutput.indentStyle}days of the year: {self.days}"
        return super().indentText(text, indent)



class DaysOfMonthKRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.DAYS_OF_MONTH_K

    def __init__(self, month: MonthEnum, days: list[int]):
        self.month = month
        self.monthName = month.value.name
        self.monthNum = month.value.num
        self.days = days


    @staticmethod
    def setupPrompt(indent: int=0) -> Recurrence:
        indentA = UserOutput.indentPadding(indent)
        indentB = UserOutput.indentPadding(indent + 1)
        print(f"{indentA}{RecurrencePeriod.DAYS_OF_MONTH_K.value} recurrence")
        monthName = UserInput.singleSelectString("which month? ", CalendarObjects.MONTH_NAMES, indent=indent+1)
        month = CalendarObjects.MONTH_NAME_TO_ID[monthName]
        days = UserInput.getIntListInput(prompt=f"which days of {monthName}? ", indent=indent+1)
        return DaysOfMonthKRecurrence(month, days)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.days: return None
        year = referenceDate.year
        month = referenceDate.month
        day = referenceDate.day
        if month > self.monthNum:
            firstDay = min(self.days)
            return dt.date(year + 1, self.monthNum, firstDay)
        elif month < self.monthNum:
            return dt.date(year, self.monthNum, firstDay)
        else:
            daysInMonth = cal.monthrange(year, month)[1]
            daysLeft = min((mday - day) % daysInMonth for mday in self.days)
            return referenceDate + dt.timedelta(days=daysLeft)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        text += f"\n{UserOutput.indentStyle}month: {self.month.value.name}"
        text += f"\n{UserOutput.indentStyle}days: {self.days}"
        return super().indentText(text, indent)



class NthWeekdayMOfMonthKRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K

    def __init__(self, month: MonthEnum, weekday: WeekdayEnum, n: int):
        self.month = month
        self.weekday = weekday
        self.n = n
    

    @staticmethod
    def setupPrompt(indent: int=0) -> Recurrence:
        indentA = UserOutput.indentPadding(indent)
        indentB = UserOutput.indentPadding(indent + 1)
        print(f"{indentA}{RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K.value} recurrence")
        monthName = UserInput.singleSelectString("which month? ", CalendarObjects.MONTH_NAMES, indent=indent+1)
        weekdayName = UserInput.singleSelectString("which weekday? ", CalendarObjects.WEEKDAY_NAMES, indent=indent+1)
        n = UserInput.getIntInput(f"which (n)th {weekdayName} of {monthName}? ", indent=indent+1)
        month = CalendarObjects.MONTH_NAME_TO_ID[monthName]
        weekday = CalendarObjects.WEEKDAY_NAME_TO_ID[weekdayName]
        return NthWeekdayMOfMonthKRecurrence(month, weekday, n)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        year = referenceDate.year
        month = referenceDate.month
        day = referenceDate.day

        if month > self.month.value.num: 
            theFirst = dt.date(year + 1, month, 1)
        else: 
            theFirst = dt.date(year, month, 1)

        weekdayOfFirst = theFirst.weekday()
        weekdayNum = self.weekday.value.num
        daysFromFirstToNthWeekdayM = ((weekdayNum - weekdayOfFirst) % 7) + (7 * (self.n - 1))

        if month == self.month.value.num and day > 1 + daysFromFirstToNthWeekdayM:
            theFirst = dt.date(year + 1, month, 1)
            weekdayOfFirst = theFirst.weekday()
            daysFromFirstToNthWeekdayM = ((weekdayNum - weekdayOfFirst) % 7) + (7 * (self.n - 1))

        return theFirst + dt.timedelta(days=daysFromFirstToNthWeekdayM)


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        numberSuffix = UserOutput.numberSuffix(self.n)
        text += f"\n{UserOutput.indentStyle}{self.n}{numberSuffix} {self.weekday.value.name} of {self.month.value.name}"
        return super().indentText(text, indent)



class OnceRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.ONCE

    def __init__(self, date: dt.date):
        self.date = date
        self.year = date.year
        self.monthName = CalendarObjects.MONTH_NUM_TO_NAME[date.month]
        self.day = date.day


    @staticmethod
    def setupPrompt(indent: int=0) -> Recurrence:
        indentA = UserOutput.indentPadding(indent)
        indentB = UserOutput.indentPadding(indent + 1)
        print(f"{indentA}{RecurrencePeriod.ONCE.value} recurrence")
        year = UserInput.getIntInput("which year? ", indent=indent+1)
        monthName = UserInput.singleSelectString("which month? ", CalendarObjects.MONTH_NAMES, indent=indent+1)
        day = UserInput.getIntInput(f"which day of {monthName}? ", indent=indent+1)
        month = CalendarObjects.MONTH_NAME_TO_NUM[monthName]
        date = dt.date(year, month, day)
        return OnceRecurrence(date)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if referenceDate > self.date: return None
        else: return self.date


    def toText(self, indent: int=0) -> str:
        text = super().toText()
        text += f"\n{UserOutput.indentStyle}date: {self.monthName} {self.day}, {self.year}"
        return super().indentText(text, indent)



class AggregateRecurrence(Recurrence):
    recurrencePeriod = RecurrencePeriod.AGGREGATE

    def __init__(self, recurrences: list[Recurrence]):
        self.recurrences = recurrences
    

    @staticmethod
    def setupPrompt(indent: int=0) -> Recurrence:
        indentA = UserOutput.indentPadding(indent)
        indentB = UserOutput.indentPadding(indent + 1)
        print(f"{indentA}{RecurrencePeriod.AGGREGATE.value} recurrence")
        recurrences = []
        keepAdding = UserInput.getBoolInput("add a recurrence? ", indent=indent+1)
        while keepAdding:
            recurrence = Recurrence.setupPrompt(indent=indent+1)
            recurrences.append(recurrence)
            keepAdding = UserInput.getBoolInput("add another recurrence? ", indent=indent+1)
        return AggregateRecurrence(recurrences)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        if not self.recurrences: return None
        soonestOccurrences = [recurrence.nextOccurrence(referenceDate=referenceDate) for recurrence in self.recurrences]
        filteredSoonest = list(filter(lambda nextOcc: nextOcc != None, soonestOccurrences))
        if len(filteredSoonest) == 0: return None
        return min(filteredSoonest) 

    
    def toText(self, indent: int=0) -> str:
        text = super().toText()
        for recurrence in self.recurrences:
            text += "\n" + recurrence.toText(indent=1)
        return super().indentText(text, indent)