import datetime as dt

from DataManagement.DataStacks.sessionInfoDataStack import SessionInfoDataStack
from DataManagement.DataStackInterfaces.habitDataStackSecondaryInterface import HabitDataStackSecondaryInterface



class SessionInfoDataStackSecondaryInterface:
    @staticmethod
    def updateSessionInfo():
        SessionInfoDataStackSecondaryInterface.updateGlobalQuotaStreak()
        SessionInfoDataStack.updatePrevSession()

    
    @staticmethod
    def updateGlobalQuotaStreak():
        prevSession = SessionInfoDataStack.getPrevSession()
        today = dt.date.today()
        if prevSession < today:
            allHabitsCompleted = HabitDataStackSecondaryInterface.allHabitsCompletedInDayRange(prevSession, today)
            if allHabitsCompleted:
                SessionInfoDataStack.incrementGlobalQuotaStreak()
            else:
                SessionInfoDataStack.resetGlobalQuotaStreak()

