import datetime as dt
from DataManagement.DataHelpers.dataEquivalent import DataEquivalent
from DateAndTime.calendarObjects import CalendarObjects


class SessionInfo(DataEquivalent):
    def __init__(self, prevUpdate: dt.date):
        self.prevUpdate = prevUpdate


    def toData(self) -> dict:
        return {
            "previous update": self.prevLogin.strftime(CalendarObjects.DATE_STR_FORMAT) if self.prevLogin is not None else None
        }

    
    @staticmethod
    def fromData(data: dict):
        prevUpdateString = data["previous update"]
        prevUpdate = dt.datetime.strptime(prevUpdateString, CalendarObjects.DATE_STR_FORMAT) if prevUpdateString is not None else None
        return SessionInfo(prevUpdate)


    