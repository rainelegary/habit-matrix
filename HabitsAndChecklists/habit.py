from HabitsAndChecklists.recurrence import Recurrence, RecurrencePeriod, DailyRecurrence, WeeklyRecurrence, MonthlyRecurrence, YearlyRecurrence, OnceRecurrence, DaysOfMonthKRecurrence, NthWeekdayMOfMonthKRecurrence, AggregateRecurrence
import datetime as dt
from DataObjectConversion.dictionaryEquivalent import DictionaryEquivalent
from DataObjectConversion.textEquivalent import TextEquivalent
from UserInteraction.userInput import UserInput



class Habit(TextEquivalent):
    def __init__(self, title: str, required: bool, upcomingBuffer: int, recurrence: Recurrence, doneByTimes: list[dt.time]):
        self.title = title
        self.required = required
        self.upcomingBuffer = upcomingBuffer
        self.recurrence = recurrence
        self.doneByTimes = doneByTimes


    @staticmethod
    def setupPrompt():
        title = UserInput.getStringInput("habit title? ")
        required = UserInput.getBoolInput("required? ")
        upcomingBuffer = UserInput.getIntInput("notify how many days in advance? ")
        recurrence = Recurrence.setupPrompt()
        doneByTimes = None
        return Habit(title, required, upcomingBuffer, recurrence, doneByTimes)


    def nextOccurrence(self, referenceDate: dt.date=dt.date.today()):
        return self.recurrence.nextOccurrence(referenceDate=referenceDate)


    def isUpcoming(self, referenceDate: dt.date=dt.date.today()) -> bool:
        nextOcc = self.nextOccurrence(referenceDate=referenceDate)
        if nextOcc == None: return False
        return referenceDate + dt.timedelta(days=self.upcomingBuffer) >= nextOcc


    def toText(self, indent: int=0):
        text = f"habit: {self.title}\n"
        text += f"  required: {self.required}\n"
        text += f"  upcoming buffer: {self.upcomingBuffer} days\n"
        text += self.recurrence.toText(indent=1)
        return super().indentText(text, indent)

