import datetime as dt
from DataManagement.DataObjects.sessionInfo import SessionInfo
from DataManagement.DataStacks.sessionInfoDataStack import SessionInfoDataStack

from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.quotaState import QuotaState
from HabitsAndChecklists.recurrence import Recurrence
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput


class QuotaStateDataStackInterface:
    @staticmethod
    def quotaStateSetupPrompt(indent: int=0):
        timeFormatExample = CalendarObjects.TIME_STR_TEXT_INPUT_FORMAT_EXAMPLE
        doneByTime = UserInput.getTimeInput(f"What time of day should this habit be completed by? {timeFormatExample} ", 
        indent=indent)
        maxDaysBefore = UserInput.getIntInput("how many days early can the habit be checked off? ", indent=indent)
        maxDaysAfter = UserInput.getIntInput("how many days late can the habit be checked off? ", indent=indent)
        return QuotaState(doneByTime, maxDaysBefore, maxDaysAfter)


    @staticmethod
    def habitCompletedUpdateQuotaState(habit: Habit, completionTime: dt.time=dt.datetime.now().time(), indent: int=0):
        recurrence = habit.recurrence
        quotaState = habit.quotaState
        
        applicableDate = quotaState.applicableCompletionDate(recurrence)
        if applicableDate is None:
            UserOutput.indentedPrint("Error: no applicable date for this habit to be completed.", indent=indent)
            return

        if quotaState.doneByTime < completionTime:
            timeStr = quotaState.doneByTime.strftime(CalendarObjects.TIME_STR_TEXT_OUTPUT_FORMAT)
            UserOutput.indentedPrint(f"Error: this habit must be completed by {timeStr}.")
            return

        if quotaState.prevCompletionDate == applicableDate:
            UserOutput.indentedPrint("Error: habit already completed for applicable date.")
            return
        
        quotaState.quotaMet += 1
        quotaState.quotaMet = max(quotaState.quotaMet, 1)
        quotaState.quotaStreak += 1    
        quotaState.prevCompletionDate = applicableDate

        ind = UserOutput.indentStyle
        reportString = f"successfully completed habit: {habit.title}\n"
        reportString += f"{ind}quota met: {quotaState.quotaMet}\n"
        reportString += f"{ind}quota streak: {quotaState.quotaStreak}"
        reportString = UserOutput.indentTextBlock(reportString, indent=indent)
        UserOutput.indentedPrint(reportString)


    @staticmethod
    def timeElapsedUpdateQuotaState(habit: Habit):
        recurrence = habit.recurrence
        quotaState = habit.quotaState

        sessionInfo = SessionInfo.fromData(SessionInfoDataStack.getData())
        prevUpdate = sessionInfo.prevUpdate
        today = dt.date.today()

        prevApplicableDate = quotaState.applicableCompletionDate(recurrence, referenceDate=prevUpdate)
        currentApplicableDate = quotaState.applicableCompletionDate(recurrence, referenceDate=today)

        numDatesBetween = quotaState.numApplicableDatesBetween(recurrence, prevApplicableDate, currentApplicableDate)
        
        quotaState.quotaMet -= numDatesBetween
        quotaState.quotaMet = max(quotaState.quotaMet, -1)
        
        if quotaState.quotaMet < 0:
            quotaState.quotaStreak = 0

        