from DataObjectConversion.dataEquivalent import DataEquivalent
from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.recurrence import Recurrence, RecurrencePeriod, DailyRecurrence, WeeklyRecurrence, MonthlyRecurrence, YearlyRecurrence, OnceRecurrence, DaysOfMonthKRecurrence, NthWeekdayMOfMonthKRecurrence, AggregateRecurrence
import datetime as dt
from DataObjectConversion.textEquivalent import TextEquivalent
from UserInteraction.userOutput import UserOutput



class DoneByTimes(TextEquivalent, DataEquivalent):
    def __init__(self, listOfTimes: list[dt.time]):
        self.listOfTimes = listOfTimes
        self.timeIntegers = sorted([t.hour for t in self.listOfTimes])


    def toText(self, indent: int=0) -> str:
        return f"{UserOutput.indentPadding(indent)}done by times: {self.timeIntegers}"

    
    def toData(self) -> list[int]:
        return self.timeIntegers

    
    @staticmethod
    def fromData(data: list[int]):
        if data is None: return None
        timeIntegers = data
        listOfTimes = sorted([dt.time(hour=t) for t in timeIntegers])
        return DoneByTimes(listOfTimes)



class QuotaState(TextEquivalent, DataEquivalent):
    def __init__(self, maxDaysBefore: int, maxDaysAfter: int, prevDate: dt.date=None, quotaMet: int=0, quotaStreak: int=0):
        self.maxDaysBefore = maxDaysBefore
        self.maxDaysAfter = maxDaysAfter
        self.prevDate = prevDate
        self.quotaMet = quotaMet
        self.quotaStreak = quotaStreak
        self.earliestPossibleDate = self.calculateEarliestPossibleDate()

    
    def updateQuotaTaskCompleted(self, indent: int=0):
        if self.earliestPossibleDate > dt.date.today() + dt.timedelta(days=self.maxDaysBefore): 
            UserOutput.indentedPrint("task already completed to maximum degree", indent=indent)
            return
        if self.quotaMet >= 0:
            self.quotaMet += 1
            self.quotaStreak += 1
        else: 
            self.quotaMet += 2
            
        self.prevDate = self.earliestPossibleDate
        self.earliestPossibleDate = self.calculateEarliestPossibleDate(prevDate=self.prevDate)
    

    def updateQuotaTimeElapsed(self, decrease: int=1):
        self.quotaMet -= decrease
    

    def calculateEarliestPossibleDate(self):
        if self.quotaMet >= 0:
            return dt.date.today()
        if self.prevDate is None:
            return dt.date.today() - dt.timedelta(days=self.maxDaysAfter)
        return max(self.prevDate + dt.timedelta(days=1), dt.date.today() - dt.timedelta(days=self.maxDaysAfter))

    
    def toText(self, indent: int=0) -> str:
        text = "quota state"
        text += f"\n{UserOutput.indentStyle}max days before: {self.maxDaysBefore}"
        text += f"\n{UserOutput.indentStyle}max days after: {self.maxDaysAfter}"
        text += f"\n{UserOutput.indentStyle}quota met: {self.quotaMet}"
        text += f"\n{UserOutput.indentStyle}quota streak: {self.quotaStreak}"
        return super().indentText(text, indent=indent)

    
    def toData(self) -> dict:
        return {
            "max days before": self.maxDaysBefore,
            "max days after": self.maxDaysAfter,
            "prev date": self.prevDate.strftime(CalendarObjects.DATE_STR_FORMAT) if self.prevDate is not None else None,
            "quota met": self.quotaMet,
            "quota streak": self.quotaStreak,
        }

    
    @staticmethod
    def fromData(data: dict):
        if data is None: return None
        maxDaysBefore = data["max days before"]
        maxDaysAfter = data["max days after"]
        prevDateString = data["prev date"]
        prevDate = dt.datetime.strptime(prevDateString, CalendarObjects.DATE_STR_FORMAT).date() if prevDateString is not None else None
        quotaMet = data["quota met"]
        quotaStreak = data["quota streak"]
        return QuotaState(maxDaysBefore, maxDaysAfter, prevDate, quotaMet, quotaStreak)



class Habit(TextEquivalent, DataEquivalent):
    def __init__(self, title: str, required: bool, upcomingBuffer: int, recurrence: Recurrence, doneByTimes: DoneByTimes, quotaState: QuotaState):
        self.title = title
        self.required = required
        self.upcomingBuffer = upcomingBuffer
        self.recurrence = recurrence
        self.doneByTimes = doneByTimes
        self.quotaState = quotaState


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        return self.recurrence.nextOccurrence(referenceDate=referenceDate)

    
    def isToday(self, referenceDate: dt.date=dt.date.today()) -> bool:
        nextOcc = self.recurrence.nextOccurrence(referenceDate=referenceDate)
        return nextOcc == referenceDate


    def isUpcoming(self, referenceDate: dt.date=dt.date.today()) -> bool:
        nextOcc = self.nextOccurrence(referenceDate=referenceDate)
        if nextOcc == None: return False
        return referenceDate + dt.timedelta(days=self.upcomingBuffer) >= nextOcc


    def toText(self, indent: int=0):
        text = f"habit: {self.title}"
        text += f"\n{UserOutput.indentStyle}required: {self.required}"
        text += f"\n{UserOutput.indentStyle}upcoming buffer: {self.upcomingBuffer} days"
        text += f"\n{self.recurrence.toText(indent=1)}"
        text += f"\n{self.doneByTimes.toText(indent=1)}" if self.doneByTimes is not None else ""
        text += f"\n{self.quotaState.toText(indent=1)}" if self.quotaState is not None else ""
        return super().indentText(text, indent)

    
    def toData(self) -> dict:
        return {
            self.title: {
                "required": self.required,
                "upcoming buffer": self.upcomingBuffer,
                "recurrence": self.recurrence.toData(),
                "done by times": self.doneByTimes.toData() if self.doneByTimes is not None else None,
                "quota state": self.quotaState.toData() if self.quotaState is not None else None,
            }
        }


    @staticmethod
    def fromData(data: dict):
        title = list(data.keys())[0]
        details = data[title]
        required = details["required"]
        upcomingBuffer = details["upcoming buffer"]
        recurrence = Recurrence.fromData(details["recurrence"])
        doneByTimes = DoneByTimes.fromData(details["done by times"])
        quotaState = QuotaState.fromData(details["quota state"])
        return Habit(title, required, upcomingBuffer, recurrence, doneByTimes, quotaState)

