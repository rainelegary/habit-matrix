import calendar as cal
import datetime as dt
import sys
import os

import yaml

from DataManagement.DataHelpers.dataStack import DataStack
from DataManagement.DataHelpers.generalDataStackInterface import \
    GeneralDataStackInterface
from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataStackInterfaces.habitDataStackSecondaryInterface import \
    HabitDataStackSecondaryInterface
from DataManagement.DataStacks.habitDataStack import HabitDataStack
from DataManagement.DataStacks.imageDataStack import ImageDataStack
from DataManagement.DataStacks.sessionInfoDataStack import SessionInfoDataStack
from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.recurrence import (DailyRecurrence, MonthlyRecurrence,
                                            Recurrence, RecurrencePeriod,
                                            WeeklyRecurrence)
from UserInteraction.commandInterface import CommandInterface
from UserInteraction.commands import (Command, CommandEnum, InvalidCommandArgsException, NewObjectCommand, ExitException)
from UserInteraction.userInput import CancelInputException, UserInput
from VisualsAndOutput.calendar import Calendar
from VisualsAndOutput.color import ColorEnum
from VisualsAndOutput.userOutput import UserOutput
from types import MappingProxyType

from VisualsAndOutput.visualDisplay import VisualDisplay


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
        # image = ImageDataStack.getImage("checked box")
        # display = VisualDisplay(15, 15)
        # display.addImage(image, 0, 0)
        # display.display()

        Calendar.display()


def main():
    os.system("") # enables colored output

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
