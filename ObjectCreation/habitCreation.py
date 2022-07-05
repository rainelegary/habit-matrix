from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.recurrence import Recurrence
from ObjectCreation.recurrenceCreation import RecurrenceCreation
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput


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