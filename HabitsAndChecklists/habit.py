from DataObjectConversion.dataEquivalent import DataEquivalent
from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.recurrence import Recurrence, RecurrencePeriod, DailyRecurrence, WeeklyRecurrence, MonthlyRecurrence, YearlyRecurrence, OnceRecurrence, DaysOfMonthKRecurrence, NthWeekdayMOfMonthKRecurrence, AggregateRecurrence
import datetime as dt
from DataObjectConversion.textEquivalent import TextEquivalent
from UserInteraction.userOutput import UserOutput
from HabitsAndChecklists.quotaState import QuotaState



class Habit(TextEquivalent, DataEquivalent):
    def __init__(self, title: str, required: bool, upcomingBuffer: int, recurrence: Recurrence, quotaState: QuotaState):
        self.title = title
        self.required = required
        self.upcomingBuffer = upcomingBuffer
        self.recurrence = recurrence
        self.quotaState = quotaState


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        return self.recurrence.nextOccurrence(referenceDate=referenceDate)

    
    def prevOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        return self.recurrence.prevOccurence(referenceDate=referenceDate)

    
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
        text += f"\n{self.quotaState.toText(indent=1)}" if self.quotaState is not None else ""
        return super().indentText(text, indent)

    
    def toData(self) -> dict:
        return {
            self.title: {
                "required": self.required,
                "upcoming buffer": self.upcomingBuffer,
                "recurrence": self.recurrence.toData(),
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
        quotaState = QuotaState.fromData(details["quota state"])
        return Habit(title, required, upcomingBuffer, recurrence, quotaState)

