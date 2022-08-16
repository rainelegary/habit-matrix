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
from UserInteraction.commands import (Command, CommandEnum, InvalidCommandArgsException, NewObjectCommand, ExitException)
from UserInteraction.userInput import CancelInputException, UserInput
from UserInteraction.userOutput import UserOutput


class Launcher:
    @staticmethod
    def runApplication():
        try:
            while True:
                try:
                    CommandInterface.getCommand(prompt="<///HABIT -> MATRIX///> ")
                    UserOutput.indentedPrint("")
                except InvalidCommandArgsException as icae:
                    UserOutput.indentedPrint(output="invalid command arguments;")
                    UserOutput.indentedPrint(icae.message)
                    UserOutput.indentedPrint("")
                    if icae.command != None:
                        Command.showCommandHelp(icae.command, verbosity=5)
                except CancelInputException:
                    UserOutput.indentedPrint(output="input cancelled.")
        except ExitException as ee:
            save = ee.save
            Launcher.closingSequence(save)
    

    @staticmethod
    def openingSequence():
        GeneralDataStackInterface.sessionStartupDataUpdates()
        

    @staticmethod
    def closingSequence(save):
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
        print("".startswith(" "))



def main():
    args = sys.argv
    if len(args) < 2:
        Launcher.runApplication()
    if args[1] == "app":
        Launcher.runApplication()
    elif args[1] == "tests":
        Launcher.runTests()
    elif args[1] == "exp":
        Launcher.runExperimental()
    else:
        raise Exception("Invalid code running mode")


if __name__ == "__main__":
    main()
