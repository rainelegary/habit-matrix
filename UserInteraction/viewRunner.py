from UserInteraction.commands import CommandScope, CommandScopeEnum, InvalidCommandArgsException
from UserInteraction.commandInterface import CommandInterface
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput


class ViewRunner:
    @staticmethod
    def homeView():
        print("{{ << -- home view -- >> }}")
        while True:
            try:
                UserInput.getInputOrCommand(prompt="home: ", commandScopeID=CommandScopeEnum.HOME)
            except InvalidCommandArgsException:
                UserOutput.indentedPrint(output="invalid command arguments, please try again.")

    
    @staticmethod
    def calendarView():
        print("{{ << -- calendar view -- >> }}")
        while True:
            try:
                UserInput.getInputOrCommand(prompt="calendar: ", commandScopeID=CommandScopeEnum.CALENDAR)
            except InvalidCommandArgsException:
                UserOutput.indentedPrint(output="invalid command arguments, please try again.")
            

    @staticmethod
    def habitsView():
        print("{{ << -- habits view -- >> }}")
        while True:
            try:
                UserInput.getInputOrCommand(prompt="habits: ", commandScopeID=CommandScopeEnum.HABITS)
            except InvalidCommandArgsException:
                UserOutput.indentedPrint(output="invalid command arguments, please try again.")
            

    @staticmethod
    def recurrencesView():
        print("{{ << -- checklists view -- >> }}")
        while True:
            try:
                UserInput.getInputOrCommand(prompt="recurrences: ", commandScopeID=CommandScopeEnum.RECURRENCES)
            except InvalidCommandArgsException:
                UserOutput.indentedPrint(output="invalid command arguments, please try again.")


    @staticmethod
    def checklistsView():
        print("{{ << -- checklists view -- >> }}")
        while True:
            try:
                UserInput.getInputOrCommand(prompt="checklists: ", commandScopeID=CommandScopeEnum.CHECKLISTS)
            except InvalidCommandArgsException:
                UserOutput.indentedPrint(output="invalid command arguments, please try again.")
            