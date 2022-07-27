import sys
from DataObjectConversion.yamlInteraction import YAMLInteraction
from DataManagement.DataStacks.dataStack import DataStack
from HabitsAndChecklists.recurrence import Recurrence, RecurrencePeriod
from HabitsAndChecklists.recurrence import DailyRecurrence, WeeklyRecurrence, MonthlyRecurrence
from HabitsAndChecklists.habit import Habit
import datetime as dt
import calendar as cal
import yaml
from UserInteraction.commands import CommandEnum, CommandScope, CommandScopeEnum
from UserInteraction.commandInterface import CommandInterface
from UserInteraction.userInput import UserInput
from DateAndTime.calendarObjects import CalendarObjects
from UserInteraction.views import ViewEnum, Views, ChangeViewException, ExitException
from UserInteraction.viewRunner import ViewRunner



class Launcher:
    @staticmethod
    def runApplication():
        try:
            view = ViewEnum.HOME
            while True:
                try: 
                    if view == ViewEnum.HOME: ViewRunner.homeView()
                    elif view == ViewEnum.CALENDAR: ViewRunner.calendarView()
                    elif view == ViewEnum.HABITS: ViewRunner.habitsView()
                    elif view == ViewEnum.RECURRENCES: ViewRunner.recurrencesView()
                    elif view == ViewEnum.CHECKLISTS: ViewRunner.checklistsView()
                    else: raise Exception("view type not handled")
                except ChangeViewException as cve:
                    view = cve.view
        except ExitException:
            Launcher.savePrompt()
    
    
    @staticmethod
    def savePrompt():
        save = UserInput.getBoolInput("save changes? ")
        if save: 
            DataStack.saveChanges()
            print("saving changes... ")
        print("exiting program. ")
    

    @staticmethod
    def runTests():
        pass


    @staticmethod
    def runExperimental():
        rec = DailyRecurrence()
        print(DailyRecurrence.fromData(rec.toData()).toData())
        dt.datetime.strptime("12/09/2022", "%m/%d/%Y")




def main():
    args = sys.argv
    if len(args) == 1 or args[1] == "app": 
        Launcher.runApplication()
    elif args[1] == "tests":
        Launcher.runTests()
    elif args[1] == "exp":
        Launcher.runExperimental()
    else:
        raise Exception("Invalid code running mode")


if __name__ == "__main__":
    main()