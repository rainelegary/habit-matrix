from HabitsAndChecklists.habit import Habit
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
        doneByTimes = None
        return Habit(title, required, upcomingBuffer, recurrence, doneByTimes)

    
    @staticmethod
    def saveHabitPrompt(habit: Habit, indent: int=0):
        UserOutput.indentedPrint("habit", indent=indent)
        print(habit.toText(indent=indent+1))
        save = UserInput.getBoolInput("save the above habit?", indent=indent)
        if save: 
            DataStack.addHabit(habit)
        return save

