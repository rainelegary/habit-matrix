import datetime as dt

from DataManagement.DataHelpers.dataEquivalent import DataEquivalent
from DataManagement.DataHelpers.textEquivalent import TextEquivalent
from DateAndTime.calendarObjects import CalendarObjects
from UserInteraction.userOutput import UserOutput

from HabitsAndChecklists.recurrence import Recurrence



class QuotaState(TextEquivalent, DataEquivalent):
    def __init__(self, doneByTime: dt.time, maxDaysBefore: int, maxDaysAfter: int, quotaMet: int=0, quotaStreak: int=0, prevCompletionDate: dt.datetime=None,):
        self.doneByTime = doneByTime
        self.maxDaysBefore = maxDaysBefore
        self.maxDaysAfter = maxDaysAfter
        self.quotaMet = quotaMet
        self.quotaStreak = quotaStreak
        self.prevCompletionDate = prevCompletionDate

    
    def applicableCompletionDate(self, recurrence: Recurrence, referenceDate: dt.date=dt.date.today()) -> dt.date:
        prevOccurrence = recurrence.prevOccurrence(referenceDate=referenceDate)
        nextOccurrence = recurrence.nextOccurrence(referenceDate=referenceDate)

        if self.dateIsInRange(prevOccurrence, referenceDate=referenceDate):
            applicableDate = prevOccurrence
        elif self.dateIsInRange(nextOccurrence, referenceDate=referenceDate):
            applicableDate = nextOccurrence
        else:
            applicableDate = None
        
        return applicableDate


    def dateIsInRange(self, date: dt.date, referenceDate: dt.date=dt.date.today()) -> bool:
        if date == None:
            raise ValueError("Invalid date format: NoneType")
        elif date + dt.timedelta(days=self.maxDaysAfter) < referenceDate:
            inRange = False
        elif date - dt.timedelta(days=self.maxDaysBefore) > referenceDate:
            inRange = False
        else:
            inRange = True
        
        return inRange


    def numApplicableDatesBetween(self, recurrence: Recurrence, startDate: dt.date, endDate: dt.date) -> int:
        if endDate < startDate:
            raise ValueError("start date must come before end date.")
        
        applicableDateForStart = self.applicableCompletionDate(recurrence, referenceDate=startDate)
        applicableDateForEnd = self.applicableCompletionDate(recurrence, referenceDate=endDate)

        if applicableDateForStart == None: applicableDateForStart = startDate
        if applicableDateForEnd == None: applicableDateForEnd = endDate

        n = 0
        workingDate = applicableDateForStart
        while workingDate != None and workingDate < applicableDateForEnd:
            workingDate = recurrence.nextOccurrence(referenceDate=workingDate+dt.timedelta(days=1))
            n += 1
        
        return n
        

    def toText(self, indent: int=0) -> str:
        if self.doneByTime == None:
            doneByTimeString = None
        else:
            doneByTimeString = self.doneByTime.strftime(CalendarObjects.TIME_STR_TEXT_OUTPUT_FORMAT)

        if self.prevCompletionDate == None:
            prevCompletionDateString = None
        else:
            prevCompletionDateString = self.prevCompletionDate.strftime(CalendarObjects.DATE_STR_TEXT_OUTPUT_FORMAT)

        ind = UserOutput.indentPadding(indent=1)
        text = "quota state"
        text += f"\n{ind}done by time: {doneByTimeString}"
        text += f"\n{ind}max days before: {self.maxDaysBefore}"
        text += f"\n{ind}max days after: {self.maxDaysAfter}"
        text += f"\n{ind}quota met: {self.quotaMet}"
        text += f"\n{ind}quota streak: {self.quotaStreak}"
        text += f"\n{ind}previous completion date: {prevCompletionDateString}"
        return super().indentText(text, indent=indent)

    
    def toData(self) -> dict:
        if self.doneByTime == None:
            doneByTimeString = None
        else:
            doneByTimeString = self.doneByTime.strftime(CalendarObjects.TIME_STR_TEXT_OUTPUT_FORMAT)

        if self.prevCompletionDate == None:
            prevCompletionDateString = None
        else:
            prevCompletionDateString = self.prevCompletionDate.strftime(CalendarObjects.DATE_STR_TEXT_OUTPUT_FORMAT)
        
        return {
            "done by time": doneByTimeString,
            "max days before": self.maxDaysBefore,
            "max days after": self.maxDaysAfter,
            "quota met": self.quotaMet,
            "quota streak": self.quotaStreak,
            "prev completion date": prevCompletionDateString,
        }

    
    @staticmethod
    def fromData(data: dict):
        if data is None: 
            return None
        
        doneByTimeString = data["done by time"]
        maxDaysBefore = data["max days before"]
        maxDaysAfter = data["max days after"]
        quotaMet = data["quota met"]
        quotaStreak = data["quota streak"]
        prevCompletionDateString = data["prev completion date"]

        if doneByTimeString == None:
            doneByTime = None
        else:
            doneByTime = dt.datetime.strptime(doneByTimeString, CalendarObjects.TIME_STR_DATA_FORMAT).time()

        if prevCompletionDateString == None:
            prevCompletionDate = None
        else:
            prevCompletionDate = dt.datetime.strptime(prevCompletionDateString, CalendarObjects.DATE_STR_DATA_FORMAT).date()
        
        return QuotaState(doneByTime, maxDaysBefore, maxDaysAfter, quotaMet, quotaStreak, prevCompletionDate)
