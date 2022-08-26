from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataHelpers.dataStack import DataStack
import datetime as dt

from DateAndTime.calendarObjects import CalendarObjects



class SessionInfoDataStack(DataStack):
    YAML_FILE = YAMLFiles.SESSION_INFO
    __dataStack = YAMLInteraction.YAMLtoData(YAMLFiles.SESSION_INFO)
    if __dataStack == None: __dataStack = {}


    @classmethod
    def getPrevSession(cls) -> dt.date:
        prevSessionStr: str = cls.__dataStack["previous session"]
        date = dt.datetime.strptime(prevSessionStr, CalendarObjects.DATE_STR_DATA_FORMAT).date()
        return date


    @classmethod
    def updatePrevSession(cls, referenceDate=dt.date.today()):
        referenceDateStr = referenceDate.strftime(CalendarObjects.DATE_STR_DATA_FORMAT)
        cls.__dataStack["previous session"] = referenceDateStr

    
    @classmethod
    def incrementGlobalQuotaStreak(cls):
        cls.__dataStack["global quota streak"] += 1

    
    @classmethod
    def resetGlobalQuotaStreak(cls):
        cls.__dataStack["global quota streak"] = 0


    @classmethod
    def addCompletedDate(cls, date: dt.date):
        day = date.day
        monthAndYearStr = date.strftime("%b %Y")
        completedDates = cls.__dataStack["completed dates"]
        if monthAndYearStr in completedDates:
            completedDates[monthAndYearStr].append(day)
            completedDates.sort()
        else:
            completedDates[monthAndYearStr] = [day]
        cls.__dataStack["completed dates"] = completedDates


    @classmethod
    def getCompletedDatesInMonth(cls, referenceDate: dt.date) -> list:
        monthAndYearStr = referenceDate.strftime("%b %Y")
        completedDates = cls.__dataStack["completed dates"]
        if monthAndYearStr in completedDates:
            return completedDates[monthAndYearStr]
        else:
            return []

    
    @classmethod
    def saveData(cls):
        YAMLInteraction.dataToYAML(cls.YAML_FILE, cls.__dataStack)
    

    @classmethod
    def getData(cls):
        return cls.__dataStack


    @classmethod
    def setData(cls, data):
        cls.__dataStack = data
    
