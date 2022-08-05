import datetime as dt

from DataManagement.DataHelpers.dataEquivalent import DataEquivalent
from DataManagement.DataHelpers.textEquivalent import TextEquivalent
from DateAndTime.calendarObjects import CalendarObjects
from UserInteraction.userOutput import UserOutput

from HabitsAndChecklists.quotaState import QuotaState
from HabitsAndChecklists.recurrence import (AggregateRecurrence,
                                            DailyRecurrence,
                                            DaysOfMonthKRecurrence,
                                            MonthlyRecurrence,
                                            NthWeekdayMOfMonthKRecurrence,
                                            OnceRecurrence, Recurrence,
                                            RecurrencePeriod, WeeklyRecurrence,
                                            YearlyRecurrence)



class Habit(TextEquivalent, DataEquivalent):
    def __init__(self, title: str, recurrence: Recurrence, upcomingBuffer: int, required: bool, quotaState: QuotaState):
        self.title = title
        self.recurrence = recurrence
        self.upcomingBuffer = upcomingBuffer
        self.required = required
        self.quotaState = quotaState


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        return self.recurrence.nextOccurrence(referenceDate=referenceDate)

    
    def prevOccurrence(self, referenceDate: dt.date=dt.date.today()) -> dt.date:
        return self.recurrence.prevOccurrence(referenceDate=referenceDate)

    
    def isToday(self, referenceDate: dt.date=dt.date.today()) -> bool:
        nextOcc = self.recurrence.nextOccurrence(referenceDate=referenceDate)
        return nextOcc == referenceDate


    def isUpcoming(self, referenceDate: dt.date=dt.date.today()) -> bool:
        nextOcc = self.nextOccurrence(referenceDate=referenceDate)
        if nextOcc == None: return False
        return referenceDate + dt.timedelta(days=self.upcomingBuffer) >= nextOcc


    def toText(self, verbosity: int=0, indent: int=0):
        indentA = UserOutput.indentPadding(indent=indent)
        indentB = UserOutput.indentPadding(indent=indent+1)
        text = ""
        if verbosity >= 0:
            text += f"{indentA}habit: {self.title}"
        if verbosity >= 1:
            text += f"\n{self.recurrence.toText(verbosity=verbosity-1, indent=indent+1)}"
        if verbosity >= 2:
            text += f"\n{indentB}upcoming buffer: {self.upcomingBuffer} days"
            text += f"\n{indentB}required: {self.required}"
            if self.quotaState != None:
                text += f"\n{self.quotaState.toText(verbosity=verbosity-1, indent=indent+1)}"
        return text

    
    def toData(self) -> dict:
        if self.quotaState == None:
            quotaStateData = None
        else:
            quotaStateData = self.quotaState.toData()

        return {
            self.title: {
                "recurrence": self.recurrence.toData(),
                "upcoming buffer": self.upcomingBuffer,
                "required": self.required,
                "quota state": quotaStateData,
            }
        }


    @staticmethod
    def fromData(data: dict):
        title = list(data.keys())[0]
        details = data[title]

        recurrence = Recurrence.fromData(details["recurrence"])
        upcomingBuffer = details["upcoming buffer"]
        required = details["required"]
        quotaState = QuotaState.fromData(details["quota state"])
        return Habit(title, recurrence, upcomingBuffer, required, quotaState)

