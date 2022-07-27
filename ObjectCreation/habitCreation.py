import datetime as dt

from DataObjectConversion.dataStack import DataStack
from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.quotaState import QuotaState
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput

from ObjectCreation.recurrenceCreation import RecurrenceCreation
from ObjectCreation.quotaStateCreation import QuotaStateCreation



class HabitCreation:
    @staticmethod
    def habitSetupPrompt(indent: int=0):
        UserOutput.indentedPrint("habit", indent)
        title = UserInput.getStringInput("habit title? ", indent=indent+1)
        required = UserInput.getBoolInput("required? ", indent=indent+1)
        upcomingBuffer = UserInput.getIntInput("notify how many days in advance? ", indent=indent+1)
        recurrence = RecurrenceCreation.generalRecurrenceSetupPrompt(indent=indent+1)
        quotaState = QuotaStateCreation.quotaStateSetupPrompt(indent=indent+1) if required else None
        return Habit(title, required, upcomingBuffer, recurrence, quotaState)

    
    @staticmethod
    def saveHabitPrompt(habit: Habit, indent: int=0):
        UserOutput.indentedPrint("habit", indent=indent)
        print(habit.toText(indent=indent+1))
        save = UserInput.getBoolInput("save the above habit? ", indent=indent)
        if save: 
            DataStack.addHabit(habit)
        return save


