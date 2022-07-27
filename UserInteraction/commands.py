import datetime as dt
from abc import ABC, abstractmethod
from enum import Enum
from tokenize import Single

from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.checklist import (Checklist, DayRangeChecklist,
                                           OverdueChecklist,
                                           SingleDayChecklist,
                                           UpcomingChecklist)
from HabitsAndChecklists.habit import Habit
from DataManagement.DataStackInterfaces.habitDataStackInterface import HabitDataStackInterface
from DataManagement.DataStackInterfaces.recurrenceDataStackInterface import RecurrenceDataStackInterface

from UserInteraction.userOutput import UserOutput
from UserInteraction.views import (ChangeViewException, ExitException,
                                   ViewEnum, Views)


class InvalidCommandArgsException(Exception):
    """an exception for when incorrect command arguments are given"""



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
            habit = HabitCreation.habitSetupPrompt(indent=indent)
            HabitCreation.saveHabitPrompt(habit, indent=indent+1)
        elif objectTypeName == "recurrence":
            recurrence = RecurrenceCreation.generalRecurrenceSetupPrompt(indent=indent)
            RecurrenceCreation.generalSaveRecurrencePrompt(recurrence, indent=indent+1)
        else:
            raise InvalidCommandArgsException("unrecognized object type")


class SeeChecklistCommand(Command):
    NAME = "see checklist"
    SHORTCUT = "check"


    @staticmethod
    def executeCommand(commandArgs: list[str], commandScopeID, indent: int=0):
        if len(commandArgs) < 2:
            raise InvalidCommandArgsException("no checklist type specified")
        checklistType = commandArgs[1]
        if checklistType == "day":
            SeeChecklistCommand.dayChecklist(commandArgs, indent=indent)
        elif checklistType == "range":
            SeeChecklistCommand.rangeChecklist(commandArgs, indent=indent)
        elif checklistType == "overdue":
            SeeChecklistCommand.overdueChecklist(commandArgs, indent=indent)
        elif checklistType == "upcoming":
            SeeChecklistCommand.upcomingChecklist(commandArgs, indent=indent)
        elif checklistType == "all":
            SeeChecklistCommand.allChecklists(commandArgs, indent=indent)
        else:
            raise InvalidCommandArgsException("not a recognized checklist type")

        
    @staticmethod
    def dayChecklist(commandArgs, indent: int=0):
        if len(commandArgs) < 3:
            day = dt.date.today()
        else:
            dayString = commandArgs[2]
            try:
                day = dt.datetime.strptime(dayString, CalendarObjects.DATE_STR_FORMAT).date()
            except ValueError:
                UserOutput.indentedPrint(f"not a valid date, please enter dates in the form {CalendarObjects.DATE_STR_FORMAT_EXAMPLE}", indent=indent)
                return

        checklist = SingleDayChecklist(day)
        checklist.display(indent=indent)

        

    @staticmethod
    def rangeChecklist(commandArgs, indent: int=0):
        if len(commandArgs) < 4:
            raise InvalidCommandArgsException("please specify a start and end date")
        startDayString = commandArgs[2]
        endDayString = commandArgs[3]
        try:
            startDay = dt.datetime.strptime(startDayString, CalendarObjects.DATE_STR_FORMAT).date()
            endDay = dt.datetime.strptime(endDayString, CalendarObjects.DATE_STR_FORMAT).date()
        except ValueError:
            UserOutput.indentedPrint(f"not a valid range of dates, please enter dates in the form {CalendarObjects.DATE_STR_FORMAT_EXAMPLE}", indent=indent)
            return

        checklist = DayRangeChecklist(startDay, endDay)
        checklist.display(indent=indent)


    @staticmethod
    def overdueChecklist(commandArgs, indent: int=0):
        checklist = OverdueChecklist()
        checklist.display(indent=indent)

    
    @staticmethod
    def upcomingChecklist(commandArgs, indent: int=0):
        checklist = UpcomingChecklist()
        checklist.display(indent=indent)

    
    @staticmethod
    def allChecklists(commandArgs, indent: int=0):
        SingleDayChecklist(dt.date.today()).display()
        OverdueChecklist().display()
        UpcomingChecklist().display()



class CommandEnum(Enum):
    CHANGE_VIEW = ChangeViewCommand()
    EXIT = ExitCommand()
    NEW = NewObjectCommand()
    SEE_CHECKLIST = SeeChecklistCommand()



class CommandScopeEnum(Enum):
    ALL = CommandScope(name="all", parent=None, whitelist=[CommandEnum.EXIT])
    VIEW = CommandScope(name="view", parent=ALL, whitelist=[CommandEnum.CHANGE_VIEW])
    HOME = CommandScope(name="home", parent=VIEW, whitelist=[CommandEnum.NEW])
    CALENDAR = CommandScope(name="calendar", parent=VIEW)
    HABITS = CommandScope(name="habits", parent=VIEW, whitelist=[CommandEnum.NEW])
    RECURRENCES = CommandScope(name="recurrences", parent=VIEW, whitelist=[CommandEnum.NEW])
    CHECKLISTS = CommandScope(name="checklists", parent=VIEW, whitelist=[CommandEnum.SEE_CHECKLIST])
