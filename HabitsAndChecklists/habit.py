from HabitsAndChecklists.recurrence import Recurrence, RecurrencePeriod, DailyRecurrence, WeeklyRecurrence, MonthlyRecurrence, YearlyRecurrence, OnceRecurrence, DaysOfMonthKRecurrence, NthWeekdayMOfMonthKRecurrence, AggregateRecurrence
import datetime as dt
from DataObjectConversion.dictionaryEquivalent import DictionaryEquivalent
from DataObjectConversion.textEquivalent import TextEquivalent
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput



class Habit(TextEquivalent):
    def __init__(self, title: str, required: bool, upcomingBuffer: int, recurrence: Recurrence, doneByTimes: list[dt.time]):
        self.title = title
        self.required = required
        self.upcomingBuffer = upcomingBuffer
        self.recurrence = recurrence
        self.doneByTimes = doneByTimes


    @staticmethod
    def setupPrompt(indent: int=0):
        indentA = UserOutput.indentPadding(indent)
        indentB = UserOutput.indentPadding(indent + 1)
        print(f"{indentA}habit")
        title = UserInput.getStringInput(f"habit title? ", indent=indent+1)
        required = UserInput.getBoolInput(f"required? ", indent=indent+1)
        upcomingBuffer = UserInput.getIntInput(f"notify how many days in advance? ", indent=indent+1)
        recurrence = Recurrence.setupPrompt(indent=indent+1)
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
        text += f"{UserOutput.indentStyle}required: {self.required}\n"
        text += f"{UserOutput.indentStyle}upcoming buffer: {self.upcomingBuffer} days\n"
        text += self.recurrence.toText(indent=1)
        return super().indentText(text, indent)

