from enum import Enum
from abc import ABC, abstractmethod
from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.recurrence import Recurrence
from UserInteraction.views import ExitException, ViewEnum, ChangeViewException, Views


class InvalidCommandArgsException(Exception):
    """an exception for when incorrect command arguments are given"""



class EndOfCommandException(Exception):
    """an exception to be raised whenever a command ends"""



class Command(ABC):
    @staticmethod
    @abstractmethod
    def executeCommand(commandArgs: list[str], commandScopeID, indent: int=0):
        raise NotImplementedError("abstract method not yet implemented in subclass")



class CommandScope:
    def __init__(self, name: str, parent, whitelist: list[Command]=None, blacklist: list[Command]=None):
        if whitelist == None: whitelist = []
        if blacklist == None: blacklist = []
        self.name = name
        self.parent = parent
        self.whitelist = whitelist
        self.blacklist = blacklist



class ChangeViewCommand(Command):
    NAME = "change view"
    SHORTCUT = "cv"


    @staticmethod
    def executeCommand(commandArgs: list[str], commandScopeID, indent: int=0):
        if len(commandArgs) < 2:
            raise InvalidCommandArgsException("not enough arguments")
        viewString = commandArgs[1]
        if viewString not in Views.VIEW_STRINGS:
            raise InvalidCommandArgsException("unrecognized view name")
        view = Views.VIEW_STRING_TO_ID[viewString]
        raise ChangeViewException(view)



class ExitCommand(Command):
    NAME = "exit"
    SHORTCUT = "q"


    @staticmethod
    def executeCommand(commandArgs: list[str], commandScopeID, indent: int=0):
        raise ExitException("exiting program")



class NewObjectCommand(Command):
    NAME = "new object"
    SHORTCUT = "new"


    @staticmethod
    def executeCommand(commandArgs: list[str], commandScopeID, indent: int=0):
        SCOPE_ID_TO_OBJ_TYPE_NAME = {
            CommandScopeEnum.HOME: "habit",
            CommandScopeEnum.HABITS: "habit",
            CommandScopeEnum.RECURRENCES: "recurrence",
        }

        if len(commandArgs) < 2:
            objectTypeName = SCOPE_ID_TO_OBJ_TYPE_NAME[commandScopeID]
        else:
            objectTypeName = commandArgs[1]

        if objectTypeName == "habit": 
            Habit.setupPrompt(indent=indent)
        elif objectTypeName == "recurrence":
            Recurrence.setupPrompt(indent=indent)
        else:
            raise InvalidCommandArgsException("unrecognized object type")
        
        raise EndOfCommandException()

        

class CommandEnum(Enum):
    CHANGE_VIEW = ChangeViewCommand()
    EXIT = ExitCommand()
    NEW = NewObjectCommand()



class CommandScopeEnum(Enum):
    ALL = CommandScope(name="all", parent=None, whitelist=[CommandEnum.EXIT])
    VIEW = CommandScope(name="view", parent=ALL, whitelist=[CommandEnum.CHANGE_VIEW])
    HOME = CommandScope(name="home", parent=VIEW, whitelist=[CommandEnum.NEW])
    CALENDAR = CommandScope(name="calendar", parent=VIEW)
    HABITS = CommandScope(name="habits", parent=VIEW, whitelist=[CommandEnum.NEW])
    RECURRENCES = CommandScope(name="recurrences", parent=VIEW, whitelist=[CommandEnum.NEW])
    CHECKLISTS = CommandScope(name="checklists", parent=VIEW)
