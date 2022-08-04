import datetime as dt
from DataManagement.DataStacks.habitDataStack import HabitDataStack

from DataManagement.DataHelpers.dataStack import DataStack
from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.quotaState import QuotaState
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput

from DataManagement.DataStackInterfaces.recurrenceDataStackInterface import RecurrenceDataStackInterface
from DataManagement.DataStackInterfaces.quotaStateDataStackInterface import QuotaStateDataStackInterface



class HabitDataStackInterface:
    @staticmethod
    def habitSetupPrompt(indent: int=0):
        UserOutput.indentedPrint("habit", indent)
        title = UserInput.getStringInput("habit title? ", indent=indent+1)
        required = UserInput.getBoolInput("required? ", indent=indent+1)
        upcomingBuffer = UserInput.getIntInput("notify how many days in advance? ", indent=indent+1)
        recurrence = RecurrenceDataStackInterface.generalRecurrenceSetupPrompt(indent=indent+1)
        quotaState = QuotaStateDataStackInterface.quotaStateSetupPrompt(indent=indent+1) if required else None
        return Habit(title, required, upcomingBuffer, recurrence, quotaState)

    
    @staticmethod
    def saveHabitPrompt(habit: Habit, indent: int=0) -> bool:
        UserOutput.indentedPrint(habit.toText(indent=indent))
        save = UserInput.getBoolInput("save the above habit? ", indent=indent)
        if save: 
            HabitDataStack.addHabit(habit)
        return save

    
    @staticmethod
    def completeHabit(habit, completionTime: dt.time=dt.datetime.now().time(), indent: int=0):
        QuotaStateDataStackInterface.habitCompletedUpdateQuotaState(habit, completionTime=completionTime, indent=indent)
        HabitDataStack.updateHabit(habit)


    @staticmethod
    def timeElapsedUpdateAllQuotaStates():
        allHabitData = HabitDataStack.getData()
        for habitName in allHabitData:
            habit = HabitDataStack.getHabit(habitName)
            QuotaStateDataStackInterface.timeElapsedUpdateQuotaState(habit)
            HabitDataStack.updateHabit(habit)

    
