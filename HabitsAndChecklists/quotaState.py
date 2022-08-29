import datetime as dt

from DataManagement.DataHelpers.dataEquivalent import DataEquivalent
from DataManagement.DataHelpers.textEquivalent import TextEquivalent
from DateAndTime.calendarObjects import CalendarObjects
from VisualsAndOutput.color import ColorEnum
from VisualsAndOutput.userOutput import UserOutput

from HabitsAndChecklists.recurrence import Recurrence



class QuotaState(TextEquivalent, DataEquivalent):
    def __init__(self, doneByTime: dt.time, maxDaysBefore: int, maxDaysAfter: int, quotaMet: int=0,
    quotaStreak: int=0, overdue: bool=False, prevCompletionDate: dt.datetime=None, allCompletionDates: list=None):
        self.doneByTime = doneByTime
        self.maxDaysBefore = maxDaysBefore
        self.maxDaysAfter = maxDaysAfter
        self.quotaMet = quotaMet
        self.quotaStreak = quotaStreak
        self.overdue = overdue
        self.prevCompletionDate = prevCompletionDate
        if allCompletionDates == None: 
            allCompletionDates = []
        self.allCompletionDates = allCompletionDates

    
    def applicableCompletionDate(self, recurrence: Recurrence, referenceDate: dt.date=dt.date.today()) -> dt.date:
        prevOccurrence = recurrence.prevOccurrence(referenceDate=referenceDate)
        nextOccurrence = recurrence.nextOccurrence(referenceDate=referenceDate)

        if prevOccurrence != None and self.dateIsInRange(prevOccurrence, referenceDate=referenceDate):
            applicableDate = prevOccurrence
        elif nextOccurrence != None and self.dateIsInRange(nextOccurrence, referenceDate=referenceDate):
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
            raise ValueError("start date must be before end date.")
        
        applicableDateForStart = self.applicableCompletionDate(recurrence, referenceDate=startDate)
        applicableDateForEnd = self.applicableCompletionDate(recurrence, referenceDate=endDate)

        if applicableDateForStart == None: 
            applicableDateForStart = recurrence.nextOccurrence(referenceDate=startDate)


        if applicableDateForEnd == None: 
            applicableDateForEnd = endDate

        n = 0
        workingDate = applicableDateForStart
        while workingDate != None and workingDate < applicableDateForEnd:
            workingDate = recurrence.nextOccurrence(referenceDate=workingDate+dt.timedelta(days=1))
            n += 1
        
        return n
        

    def toText(self, verbosity: int=0, indent: int=0) -> str:
        if self.doneByTime == None:
            doneByTimeString = None
        else:
            doneByTimeString = self.doneByTime.strftime(CalendarObjects.TIME_STR_TEXT_OUTPUT_FORMAT)

        if self.prevCompletionDate == None:
            prevCompletionDateStr = "none"
        else:
            prevCompletionDateStr = self.prevCompletionDate.strftime(CalendarObjects.DATE_STR_TEXT_OUTPUT_FORMAT)

        overdueStr = str(self.overdue).lower()

        indentA = UserOutput.indentPadding(indent=indent)
        indentB = UserOutput.indentPadding(indent=indent+1)
        indentC = UserOutput.indentPadding(indent=indent+2)

        text = ""
        if verbosity >= 1:
            text += f"{indentA}quota state"
            text += f"\n{indentB}quota met: {self.quotaMet}"
            text += f"\n{indentB}quota streak: {self.quotaStreak}"
        if verbosity >= 2:
            text += f"\n{indentB}done by time: {doneByTimeString}"
            text += f"\n{indentB}max days before: {self.maxDaysBefore}"
            text += f"\n{indentB}max days after: {self.maxDaysAfter}"
            text += f"\n{indentB}overdue: {overdueStr}"
            text += f"\n{indentB}previous completion date: {prevCompletionDateStr}"
        if verbosity >= 3:
            text += f"\n{indentB}all completion dates:"
            if len(self.allCompletionDates) == 0:
                text += f"\n{indentC}none"
            for date in self.allCompletionDates:
                dateStr = date.strftime(CalendarObjects.DATE_STR_TEXT_OUTPUT_FORMAT)
                text += f"\n{indentC}{dateStr}"
        return text

    
    def toData(self) -> dict:
        timeFormat = CalendarObjects.TIME_STR_DATA_FORMAT
        dateFormat = CalendarObjects.DATE_STR_DATA_FORMAT

        if self.doneByTime == None:
            doneByTimeString = None
        else:
            doneByTimeString = self.doneByTime.strftime(timeFormat)

        if self.prevCompletionDate == None:
            prevCompletionDateString = None
        else:
            prevCompletionDateString = self.prevCompletionDate.strftime(dateFormat)

        allCompletionDatesStrList = [completionDate.strftime(dateFormat) for completionDate in self.allCompletionDates]
        
        return {
            "done by time": doneByTimeString,
            "max days before": self.maxDaysBefore,
            "max days after": self.maxDaysAfter,
            "quota met": self.quotaMet,
            "quota streak": self.quotaStreak,
            "overdue": self.overdue,
            "prev completion date": prevCompletionDateString,
            "all completion dates": allCompletionDatesStrList,
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
        overdue = data["overdue"]
        prevCompletionDateString = data["prev completion date"]
        allCompletionDatesStrList = data["all completion dates"]

        timeFormat = CalendarObjects.TIME_STR_DATA_FORMAT
        dateFormat = CalendarObjects.DATE_STR_DATA_FORMAT

        if doneByTimeString == None:
            doneByTime = None
        else:
            doneByTime = dt.datetime.strptime(doneByTimeString, timeFormat).time()

        if prevCompletionDateString == None:
            prevCompletionDate = None
        else:
            prevCompletionDate = dt.datetime.strptime(prevCompletionDateString, dateFormat).date()

        allCompletionDates = [dt.datetime.strptime(dateStr, dateFormat).date() for dateStr in allCompletionDatesStrList]
        
        return QuotaState(doneByTime, maxDaysBefore, maxDaysAfter, quotaMet, 
        quotaStreak, overdue=overdue, prevCompletionDate=prevCompletionDate, allCompletionDates=allCompletionDates)
