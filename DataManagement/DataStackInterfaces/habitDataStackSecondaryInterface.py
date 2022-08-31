import datetime as dt
from DataManagement.DataStacks.habitDataStack import HabitDataStack

from DataManagement.DataHelpers.dataStack import DataStack
from DataManagement.DataStacks.sessionInfoDataStack import SessionInfoDataStack
from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.quotaState import QuotaState
from UserInteraction.userInput import UserInput
from VisualsAndOutput.userOutput import UserOutput

from DataManagement.DataStackInterfaces.recurrenceDataStackSecondaryInterface import RecurrenceDataStackSecondaryInterface



class HabitDataStackSecondaryInterface:
    @staticmethod
    def habitSetupPrompt(indent: int=0):
        UserOutput.indentedPrint("habit", indent)
        title = UserInput.getStringInput("habit title? ", indent=indent+1)
        recurrence = RecurrenceDataStackSecondaryInterface.generalRecurrenceSetupPrompt(indent=indent+1)
        upcomingBuffer = UserInput.getIntInput("notify how many days in advance? ", indent=indent+1)
        required = UserInput.getBoolInput("required? ", indent=indent+1)
        if required:
            quotaState = HabitDataStackSecondaryInterface.quotaStateSetupPrompt(indent=indent+1)
        else:
            quotaState = None
        return Habit(title, recurrence, upcomingBuffer, required, quotaState)

    
    @staticmethod
    def saveHabitPrompt(habit: Habit, indent: int=0) -> bool:
        UserOutput.indentedPrint(habit.toText(verbosity=5, indent=indent))
        save = UserInput.getBoolInput("save the above habit? ", indent=indent)
        if save: 
            HabitDataStack.addHabit(habit)
        return save

    
    @staticmethod
    def completeHabit(habit: Habit, completionTime: dt.time=dt.datetime.now().time(), indent: int=0):
        recurrence = habit.recurrence
        quotaState = habit.quotaState

        if quotaState == None:
            UserOutput.indentedPrint("Error: this habit has no quota, so it cannot be marked as complete.", indent=indent)
            return
        
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
        quotaState.overdue = False  
        quotaState.prevCompletionDate = applicableDate
        quotaState.allCompletionDates.append(applicableDate)
        quotaState.allCompletionDates.sort()
        HabitDataStack.updateHabit(habit)

        ind = UserOutput.indentPadding(1)
        reportString = f"successfully completed habit: {habit.title}\n"
        reportString += f"{ind}quota met: {quotaState.quotaMet}\n"
        reportString += f"{ind}quota streak: {quotaState.quotaStreak}"
        reportString = UserOutput.indentTextBlock(reportString, indent=indent)
        UserOutput.indentedPrint(reportString)

        allHabitsCompleted = HabitDataStackSecondaryInterface.allHabitsCompletedOnDate(applicableDate)

        if allHabitsCompleted:
            applicableDateStr = applicableDate.strftime(CalendarObjects.DATE_STR_TEXT_OUTPUT_FORMAT)
            reportString = f"successfully completed all habits for {applicableDateStr}."
            UserOutput.printWhitespace()
            UserOutput.indentedPrint(reportString)
            SessionInfoDataStack.addCompletedDate(applicableDate)

    
    @staticmethod
    def dismissHabit(habit: Habit, indent: int=0):
        if habit.quotaState == None:
            UserOutput.indentedPrint("Error: this habit does not need to be dismissed as it can never be overdue.", indent=indent)
            return

        if not habit.quotaState.overdue:
            UserOutput.indentedPrint("Error: this habit cannot be dismissed as it is not overdue.", indent=indent)
            return
        
        habit.quotaState.overdue = False
        HabitDataStack.updateHabit(habit)
        UserOutput.indentedPrint("habit dismissed.", indent=indent)


    @staticmethod
    def allHabitsCompletedInDayRange(startDay: dt.date, endDay: dt.date) -> bool:
        dayRange = []
        for n in range(int((endDay - startDay).days)):
            dayRange.append(startDay + dt.timedelta(days=n))
        
        allHabitsCompleted = True
        for date in dayRange:
            if not HabitDataStackSecondaryInterface.allHabitsCompletedOnDate(date):
                allHabitsCompleted = False

        return allHabitsCompleted


    @staticmethod
    def allHabitsCompletedOnDate(date: dt.date) -> bool:
        allHabitsCompleted = True
        for habitName in HabitDataStack.getData():
            habit = HabitDataStack.getHabit(habitName)
            complete = (not habit.required) or (date in habit.quotaState.allCompletionDates)
            if habit.isToday(referenceDate=date) and not complete:
                allHabitsCompleted = False
        
        return allHabitsCompleted


    @staticmethod
    def quotaStateSetupPrompt(indent: int=0):
        timeFormatExample = CalendarObjects.TIME_STR_TEXT_INPUT_FORMAT_EXAMPLE
        doneByTime = UserInput.getTimeInput(f"What time of day should this habit be completed by? {timeFormatExample} ", 
        indent=indent)
        maxDaysBefore = UserInput.getIntInput("how many days early can the habit be checked off? ",
        minimum=0, maximum=None, indent=indent)
        maxDaysAfter = UserInput.getIntInput("how many days late can the habit be checked off? ", 
        minimum=0, maximum=None, indent=indent)
        return QuotaState(doneByTime, maxDaysBefore, maxDaysAfter)

    
    @staticmethod
    def timeElapsedUpdateAllQuotaStates():
        allHabitData = HabitDataStack.getData()
        for habitName in allHabitData:
            habit = HabitDataStack.getHabit(habitName)
            HabitDataStackSecondaryInterface.timeElapsedUpdateQuotaState(habit)
            HabitDataStack.updateHabit(habit)


    @staticmethod
    def timeElapsedUpdateQuotaState(habit: Habit):
        recurrence = habit.recurrence
        quotaState = habit.quotaState

        if quotaState == None:
            return

        prevSession = SessionInfoDataStack.getPrevSession()
        today = dt.date.today()

        prevApplicableDate = quotaState.applicableCompletionDate(recurrence, referenceDate=prevSession)
        currentApplicableDate = quotaState.applicableCompletionDate(recurrence, referenceDate=today)

        if prevApplicableDate == None:
            prevApplicableDate = prevSession
        
        if currentApplicableDate == None:
            currentApplicableDate = today

        numDatesBetween = quotaState.numApplicableDatesBetween(recurrence, prevApplicableDate, currentApplicableDate)
        prevOcc = habit.prevOccurrence(referenceDate=today - dt.timedelta(days=1))
        prevComp = quotaState.prevCompletionDate

        if numDatesBetween > 0 and (prevComp == None or prevOcc > prevComp):
            quotaState.overdue = True

        quotaState.quotaMet -= numDatesBetween
        quotaState.quotaMet = max(quotaState.quotaMet, -1)
        
        if quotaState.quotaMet < 0:
            quotaState.quotaStreak = 0

