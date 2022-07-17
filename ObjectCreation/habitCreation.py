import datetime as dt
from HabitsAndChecklists.habit import Habit, DoneByTimes, QuotaState
from ObjectCreation.recurrenceCreation import RecurrenceCreation
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput
from DataObjectConversion.dataStack import DataStack



class HabitCreation:
    @staticmethod
    def habitSetupPrompt(indent: int=0):
        UserOutput.indentedPrint("habit", indent)
        title = UserInput.getStringInput("habit title? ", indent=indent+1)
        required = UserInput.getBoolInput("required? ", indent=indent+1)
        upcomingBuffer = UserInput.getIntInput("notify how many days in advance? ", indent=indent+1)
        recurrence = RecurrenceCreation.generalRecurrenceSetupPrompt(indent=indent+1)
        doneByTimes = DoneByTimesCreation.doneByTimesSetupPrompt(indent=indent+1) if required else None
        quotaState = QuotaStateCreation.quotaStateSetupPrompt(indent=indent+1) if required else None
        return Habit(title, required, upcomingBuffer, recurrence, doneByTimes, quotaState)

    
    @staticmethod
    def saveHabitPrompt(habit: Habit, indent: int=0):
        UserOutput.indentedPrint("habit", indent=indent)
        print(habit.toText(indent=indent+1))
        save = UserInput.getBoolInput("save the above habit? ", indent=indent)
        if save: 
            DataStack.addHabit(habit)
        return save



class DoneByTimesCreation:
    @staticmethod
    def doneByTimesSetupPrompt(indent: int=0):
        prompting = True
        while prompting:
            timeIntegers = UserInput.getIntListInput("which times should this habit be completed by? ", indent=indent)
            try:
                listOfTimes = [dt.time(t) for t in timeIntegers]
            except ValueError:
                UserOutput.indentedPrint("please keep times in the range 0 to 23.", indent=indent)
            else:
                prompting = False
        
        return DoneByTimes(listOfTimes)
        


class QuotaStateCreation:
    @staticmethod
    def quotaStateSetupPrompt(indent: int=0):
        maxDaysBefore = UserInput.getIntInput("how many days early can the habit be checked off? ", indent=indent)
        maxDaysAfter = UserInput.getIntInput("how many days late can the habit be checked off? ", indent=indent)
        return QuotaState(maxDaysBefore, maxDaysAfter)

