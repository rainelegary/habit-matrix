from UserInteraction.commandInterface import CommandInterface
from UserInteraction.commands import (CommandScope, CommandScopeEnum,
                                      InvalidCommandArgsException)
from UserInteraction.userInput import CancelInputException, UserInput
from UserInteraction.userOutput import UserOutput


class ViewRunner:
    @staticmethod
    def homeView():
        print("home view")
        while True:
            try:
                CommandInterface.getInputOrCommand(prompt="home: ", commandScopeID=CommandScopeEnum.HOME)
            except InvalidCommandArgsException:
                UserOutput.indentedPrint(output="invalid command arguments, please try again.")
            except EndOfCommandException:
                pass
            except CancelInputException:
                pass

    
    @staticmethod
    def calendarView():
        print("calendar view")
        while True:
            try:
                CommandInterface.getInputOrCommand(prompt="calendar: ", commandScopeID=CommandScopeEnum.CALENDAR)
            except InvalidCommandArgsException:
                UserOutput.indentedPrint(output="invalid command arguments, please try again.")
            except EndOfCommandException:
                pass
            except CancelInputException:
                pass
            

    @staticmethod
    def habitsView():
        print("habits view")
        while True:
            try:
                CommandInterface.getInputOrCommand(prompt="habits: ", commandScopeID=CommandScopeEnum.HABITS)
            except InvalidCommandArgsException:
                UserOutput.indentedPrint(output="invalid command arguments, please try again.")
            except EndOfCommandException:
                pass
            except CancelInputException:
                pass
            

    @staticmethod
    def recurrencesView():
        print("recurrences view")
        while True:
            try:
                CommandInterface.getInputOrCommand(prompt="recurrences: ", commandScopeID=CommandScopeEnum.RECURRENCES)
            except InvalidCommandArgsException:
                UserOutput.indentedPrint(output="invalid command arguments, please try again.")
            except EndOfCommandException:
                pass
            except CancelInputException:
                pass


    @staticmethod
    def checklistsView():
        print("checklists view")
        while True:
            try:
                CommandInterface.getInputOrCommand(prompt="checklists: ", commandScopeID=CommandScopeEnum.CHECKLISTS)
            except InvalidCommandArgsException:
                UserOutput.indentedPrint(output="invalid command arguments, please try again.")
            except EndOfCommandException:
                pass
            except CancelInputException:
                pass
            