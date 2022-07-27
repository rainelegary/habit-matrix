import datetime as dt

from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.quotaState import QuotaState
from HabitsAndChecklists.recurrence import Recurrence
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput


class QuotaStateDataStackInterface:
    @staticmethod
    def quotaStateSetupPrompt(indent: int=0):
        doneByTimeString = UserInput.getStringInput(f"What time of day should this task be completed by? {CalendarObjects.TIME_STR_FORMAT_EXAMPLE}", indent=indent)
        doneByTime = dt.datetime.strptime(doneByTimeString, CalendarObjects.TIME_STR_FORMAT).time()
        maxDaysBefore = UserInput.getIntInput("how many days early can the habit be checked off? ", indent=indent)
        maxDaysAfter = UserInput.getIntInput("how many days late can the habit be checked off? ", indent=indent)
        return QuotaState(doneByTime, maxDaysBefore, maxDaysAfter)


    @staticmethod
    def habitCompletedUpdateQuotaState(habit: Habit, indent: int=0):
        recurrence = habit.recurrence
        quotaState = habit.quotaState
        
        applicableDate = quotaState.applicableCompletionDate(recurrence)
        if applicableDate is None:
            UserOutput.indentedPrint("Error: no applicable date for this habit to be completed.", indent=indent)
            return

        if quotaState.doneByTime < dt.datetime.now().time():
            timeStr = quotaState.doneByTime.strftime(CalendarObjects.TIME_STR_FORMAT)
            UserOutput.indentedPrint(f"Error: this task must be completed by {timeStr}.")
            return
        
        if quotaState.quotaMet > 0:
            quotaState.quotaMet += 1
        else: 
            quotaState.quotaMet = 1
            
        quotaState.prevCompletionDate = applicableDate


    

    @staticmethod
    def timeElapsedUpdateQuotaState(habit: Habit):
        title = habit.title
        recurrence = habit.recurrence
        quotaState = habit.quotaState

        

        

        
