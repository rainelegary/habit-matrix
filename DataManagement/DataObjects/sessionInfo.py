import datetime as dt
from DataManagement.DataHelpers.dataEquivalent import DataEquivalent
from DateAndTime.calendarObjects import CalendarObjects


class SessionInfo(DataEquivalent):
    def __init__(self, prevUpdate: dt.date):
        self.prevUpdate = prevUpdate

    
    def changePrevUpdate(self):
        self.prevUpdate = dt.date.today()


    def toData(self) -> dict:
        if self.prevUpdate == None:
            prevSession = None
        else:
            prevSession = self.prevUpdate.strftime(CalendarObjects.DATE_STR_DATA_FORMAT)
        return {
            "previous session": prevSession
        }

    
    @staticmethod
    def fromData(data: dict):
        prevUpdateString = data["previous session"]
        if prevUpdateString == None:
            prevUpdate = None
        else:
            prevUpdate = dt.datetime.strptime(prevUpdateString, CalendarObjects.DATE_STR_DATA_FORMAT).date()
        return SessionInfo(prevUpdate)


    