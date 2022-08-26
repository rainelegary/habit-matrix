import calendar as cal
import datetime as dt
import sys

import yaml

from DataManagement.DataHelpers.dataStack import DataStack
from DataManagement.DataHelpers.generalDataStackInterface import \
    GeneralDataStackInterface
from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataStackInterfaces.habitDataStackSecondaryInterface import \
    HabitDataStackSecondaryInterface
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
from types import MappingProxyType


class Launcher:
    @staticmethod
    def runApplication():
        UserOutput.printWhitespace(2)
        try:
            while True:
                try:
                    CommandInterface.getCommand(prompt="< habit </> matrix > ")
                    UserOutput.printWhitespace(2)
                except InvalidCommandArgsException as icae:
                    UserOutput.indentedPrint(output="invalid command arguments;")
                    UserOutput.indentedPrint(icae.message)
                    UserOutput.printWhitespace()
                    if icae.command != None:
                        Command.showCommandHelp(icae.command, verbosity=5)
                        UserOutput.printWhitespace()
                    UserOutput.indentedPrint("NOTE: separate all command arguments with a tab.")
                    UserOutput.printWhitespace(2)
                except CancelInputException:
                    UserOutput.printWhitespace()
                    UserOutput.indentedPrint(output="input cancelled.")
                    UserOutput.printWhitespace(2)
        except ExitException as ee:
            save = ee.save
            Launcher.closingSequence(save)
    

    @staticmethod
    def openingSequence():
        GeneralDataStackInterface.sessionStartupDataUpdates()
        

    @staticmethod
    def closingSequence(save):
        if save:
            UserOutput.indentedPrint("saving changes...")
            GeneralDataStackInterface.sessionClosingDataUpdates()
            GeneralDataStackInterface.saveData()
            UserOutput.indentedPrint("changes saved!")
            UserOutput.printWhitespace()
        UserOutput.indentedPrint("exiting habit matrix. ")
        UserOutput.printWhitespace()
    

    @staticmethod
    def runTests():
        pass


    @staticmethod
    def runExperimental():
        import os
        os.system("")

        # Red 
        print("\033[31mHello World\033[0m")
        print("\u001b[32mmoment")

        def colored(r, g, b, text):
            return f"\033[38;2;{r};{g};{b}m{text} \033[0m"

        # Black: \u001b[30m
        # Red: \u001b[31m
        # Green: \u001b[32m
        # Yellow: \u001b[33m
        # Blue: \u001b[34m
        # Magenta: \u001b[35m
        # Cyan: \u001b[36m
        # White: \u001b[37m
        # Reset: \u001b[0m



def main():
    args = sys.argv
    if len(args) < 2:
        Launcher.runApplication()
    elif args[1] == "app":
        Launcher.runApplication()
    elif args[1] == "tests":
        Launcher.runTests()
    elif args[1] == "exp":
        Launcher.runExperimental()
    else:
        raise Exception("Invalid code running mode")


if __name__ == "__main__":
    main()
