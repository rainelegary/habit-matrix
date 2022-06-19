from HabitsAndChecklists.recurrence import Recurrence, RecurrencePeriod, DailyRecurrence, WeeklyRecurrence, MonthlyRecurrence, YearlyRecurrence, OnceRecurrence, DaysOfMonthKRecurrence, NthWeekdayMOfMonthKRecurrence, AggregateRecurrence
import datetime as dt
from DataObjectConversion.dictionaryEquivalent import DictionaryEquivalent
from DataObjectConversion.textEquivalent import TextEquivalent


class Habit(TextEquivalent, DictionaryEquivalent):
    def __init__(self, required: bool, upcomingBuffer: int, recurrence: Recurrence, doneByTime: dt.time):
        self.required = required
        self.upcomingBuffer = upcomingBuffer
        self.recurrence = recurrence
        self.doneByTime = doneByTime


    @staticmethod
    def setupPrompt():
        pass


    def nextOccurrence(self, referenceTime=dt.datetime.now()):
        return self.recurrence.nextOccurrence(referenceTime=referenceTime)


    def isUpcoming(self, referenceTime=dt.datetime.now()):
        nextOcc = self.nextOccurrence(referenceTime=referenceTime)
        if nextOcc == None: return False
        return referenceTime + dt.timedelta(days=self.upcomingBuffer) >= nextOcc


    def toText(self):
        pass


    def toDict(self):
        pass


    def fromDict(self, dictionary):
        pass


    






