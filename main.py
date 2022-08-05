import calendar as cal
import datetime as dt
import sys

import yaml

from DataManagement.DataHelpers.dataStack import DataStack
from DataManagement.DataHelpers.generalDataStackInterface import \
    GeneralDataStackInterface
from DataManagement.DataHelpers.yamlInteraction import YAMLInteraction
from DataManagement.DataObjects.sessionInfo import SessionInfo
from DataManagement.DataStackInterfaces.habitDataStackInterface import \
    HabitDataStackInterface
from DataManagement.DataStacks.habitDataStack import HabitDataStack
from DataManagement.DataStacks.sessionInfoDataStack import SessionInfoDataStack
from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.recurrence import (DailyRecurrence, MonthlyRecurrence,
                                            Recurrence, RecurrencePeriod,
                                            WeeklyRecurrence)
from UserInteraction.commandInterface import CommandInterface
from UserInteraction.commands import (CommandEnum, CommandScope,
                                      CommandScopeEnum, ListHabitsCommand, NewObjectCommand)
from UserInteraction.userInput import UserInput
from UserInteraction.viewRunner import ViewRunner
from UserInteraction.views import (ChangeViewException, ExitException,
                                   ViewEnum, Views)


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
            Launcher.closingSequence()
    

    @staticmethod
    def openingSequence():
        GeneralDataStackInterface.sessionStartupDataUpdates()
        

    @staticmethod
    def closingSequence():
        save = UserInput.getBoolInput("save changes? ")
        if save:
            print("saving changes... ")
            GeneralDataStackInterface.sessionClosingDataUpdates()
            GeneralDataStackInterface.saveData()
            print("changes saved!")
        print("exiting program. ")
    

    @staticmethod
    def runTests():
        pass


    @staticmethod
    def runExperimental():
        ListHabitsCommand.executeCommand(["habits"], CommandScopeEnum.HOME)
        NewObjectCommand.executeCommand(["new", "habit"], CommandScopeEnum.HOME)



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
