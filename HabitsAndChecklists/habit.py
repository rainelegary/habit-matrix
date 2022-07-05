from DataObjectConversion.dataEquivalent import DataEquivalent
from HabitsAndChecklists.recurrence import Recurrence, RecurrencePeriod, DailyRecurrence, WeeklyRecurrence, MonthlyRecurrence, YearlyRecurrence, OnceRecurrence, DaysOfMonthKRecurrence, NthWeekdayMOfMonthKRecurrence, AggregateRecurrence
import datetime as dt
from DataObjectConversion.textEquivalent import TextEquivalent
from UserInteraction.userOutput import UserOutput



class Habit(TextEquivalent, DataEquivalent):
    def __init__(self, title: str, required: bool, upcomingBuffer: int, recurrence: Recurrence, doneByTimes: list[dt.time]):
        self.title = title
        self.required = required
        self.upcomingBuffer = upcomingBuffer
        self.recurrence = recurrence
        self.doneByTimes = doneByTimes


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()):
        return self.recurrence.nextOccurrence(referenceDate=referenceDate)


    def isUpcoming(self, referenceDate: dt.date=dt.date.today()) -> bool:
        nextOcc = self.nextOccurrence(referenceDate=referenceDate)
        if nextOcc == None: return False
        return referenceDate + dt.timedelta(days=self.upcomingBuffer) >= nextOcc


    def toText(self, indent: int=0):
        text = f"habit: {self.title}\n"
        text += f"{UserOutput.indentStyle}required: {self.required}\n"
        text += f"{UserOutput.indentStyle}upcoming buffer: {self.upcomingBuffer} days\n"
        text += self.recurrence.toText(indent=1)
        return super().indentText(text, indent)

    
    def toData(self):
        return {
            self.title: {
                "required": self.required,
                "upcoming buffer": self.upcomingBuffer,
                "recurrence": self.recurrence.toData(),
                "done by times": self.doneByTimes,
            }
        }


    @staticmethod
    def fromData(data: dict):
        title = list(data.keys())[0]
        details = data[title]
        required = details["required"]
        upcomingBuffer = details["upcoming buffer"]
        recurrence = details["recurrence"]
        doneByTimes = details["done by times"]
        return Habit(title, required, upcomingBuffer, recurrence, doneByTimes)
