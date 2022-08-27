import datetime as dt
from abc import ABC, abstractmethod
from enum import Enum

from DataManagement.DataStackInterfaces.habitDataStackSecondaryInterface import \
    HabitDataStackSecondaryInterface
from DataManagement.DataStackInterfaces.recurrenceDataStackSecondaryInterface import \
    RecurrenceDataStackSecondaryInterface
from DataManagement.DataStacks.habitDataStack import HabitDataStack
from DataManagement.DataStacks.recurrenceDataStack import RecurrenceDataStack
from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.checklist import (Checklist, DayRangeChecklist,
                                           OverdueChecklist,
                                           SingleDayChecklist,
                                           UpcomingChecklist)
from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.recurrence import Recurrence
from VisualsAndOutput.calendar import Calendar
from .userInput import UserInput

from VisualsAndOutput.userOutput import UserOutput


class InvalidCommandArgsException(Exception):
    """an exception for when incorrect command arguments are given"""
    def __init__(self, message, command):
        self.message = message
        self.command = command
    


class ExitException(Exception):
    """an exception for when the exit command is executed"""
    def __init__(self, save):
        self.save = save



class Command(ABC):
    @staticmethod
    @abstractmethod
    def executeCommand(commandArgs: dict, indent: int=0):
        raise NotImplementedError("abstract method not yet implemented in subclass")


    @staticmethod
    @abstractmethod
    def keywordArgDefaults():
        raise NotImplementedError("abstract method not yet implemented in subclass")

    
    @staticmethod
    def showCommandHelp(command, verbosity: int, indent: int=0):
        commandClass = command.value
        name = commandClass.NAME
        shortcut = commandClass.SHORTCUT
        desc = commandClass.DESCRIPTION
        obligateArgs = commandClass.OBLIGATE_ARG_DESCRIPTIONS
        keywordArgs = commandClass.KEYWORD_ARG_DESCRIPTIONS
        keywordArgDefaults = commandClass.keywordArgDefaults()

        if verbosity >= 0:
            UserOutput.indentedPrint(f"{shortcut} ({name}) - {desc}", indent=indent)
        if verbosity >= 1:
            UserOutput.indentedPrint("obligate arguments: ", indent=indent+1)
            for obArg in obligateArgs:
                UserOutput.indentedPrint(f"{obArg} - {obligateArgs[obArg]}", indent=indent+2)
            if len(obligateArgs) == 0:
                UserOutput.indentedPrint("none", indent=indent+2)
            UserOutput.indentedPrint("keyword arguments: ", indent=indent+1)
            for kwArg in keywordArgs:
                UserOutput.indentedPrint(f"{kwArg} - {keywordArgs[kwArg]} (default value = {keywordArgDefaults[kwArg]})", indent=indent+2)
            if len(keywordArgs) == 0:
                UserOutput.indentedPrint("none", indent=indent+2)
        


class HelpCommand(Command):
    NAME = "help"
    SHORTCUT = "help"
    DESCRIPTION = "get help for a specific command, or for all commands."
    OBLIGATE_ARG_DESCRIPTIONS = {
        
    }
    KEYWORD_ARG_DESCRIPTIONS = {
        "c": "name of command to get help for. 'all' to see all commands.",
        "v": "verbosity, or how much detail to show (-1 or lower being no detail, 3 or higher being high detail)",
    }
    OBLIGATE_ARGS = list(OBLIGATE_ARG_DESCRIPTIONS)
    KEYWORD_ARGS = list(KEYWORD_ARG_DESCRIPTIONS)


    class HelpCommandArgs():
        def __init__(self, commandArgs: dict):
            commandName = commandArgs["c"]
            self.command = None
            for command in CommandEnum:
                if command.value.SHORTCUT == commandName:
                    self.command = command
        
            verbosityStr = commandArgs["v"]
            try:
                self.verbosity = int(verbosityStr)
            except ValueError:
                raise InvalidCommandArgsException("the 'verbosity' argument must be an integer.", CommandEnum.HELP)
    

    @staticmethod
    def keywordArgDefaults():
        return {
            "c": "all",
            "v": "2",   
        }


    @staticmethod
    def executeCommand(commandArgs: dict, indent: int=0):
        helpCommandArgs = HelpCommand.HelpCommandArgs(commandArgs)
        command = helpCommandArgs.command
        verbosity = helpCommandArgs.verbosity

        if command == None: # show all commands
            UserOutput.indentedPrint("all commands:", indent=indent)
            UserOutput.printWhitespace(verbosity)
            i = 0
            for comd in CommandEnum:
                Command.showCommandHelp(comd, verbosity=verbosity, indent=indent+1)
                if i < len(CommandEnum) - 1:
                    UserOutput.printWhitespace(verbosity)
                i += 1
            
            UserOutput.printWhitespace()
            UserOutput.indentedPrint("NOTE: separate all command arguments with a tab.", indent=indent)
        else:
            Command.showCommandHelp(command, verbosity=verbosity, indent=indent)
            UserOutput.printWhitespace()
            UserOutput.indentedPrint("NOTE: separate all command arguments with a tab.", indent=indent)
            

            
class ExitCommand(Command):
    NAME = "exit"
    SHORTCUT = "q"
    DESCRIPTION = "exit the habit matrix"
    OBLIGATE_ARG_DESCRIPTIONS = {
        
    }
    KEYWORD_ARG_DESCRIPTIONS = {
        "save": "whether to save changes or not"
    }
    OBLIGATE_ARGS = list(OBLIGATE_ARG_DESCRIPTIONS)
    KEYWORD_ARGS = list(KEYWORD_ARG_DESCRIPTIONS)


    class ExitCommandArgs():
        def __init__(self, commandArgs: dict):
            saveStr = commandArgs["save"]
            if saveStr not in ["true", "false"]:
                raise InvalidCommandArgsException("the 'save' command argument must be true or false.", CommandEnum.EXIT)
            self.save = {"true": True, "false": False}[saveStr]


    @staticmethod
    def keywordArgDefaults():
        return {
            "save": "true"
        }
              
            
    @staticmethod
    def executeCommand(commandArgs: dict, indent: int=0):
        exitCommandArgs = ExitCommand.ExitCommandArgs(commandArgs)
        save = exitCommandArgs.save

        raise ExitException(save)



class SeeObjectCommand(Command):
    NAME = "see object"
    SHORTCUT = "see"
    DESCRIPTION = "view an object such as a habit or recurrence and its associated details."
    OBLIGATE_ARG_DESCRIPTIONS = {
        "object type": "type of object i.e. 'habit' or 'recurrence'.",
        "object name": "name of habit or recurrence."
    }
    KEYWORD_ARG_DESCRIPTIONS = {
        "v": "verbosity, or how much detail to show (-1 or lower being no detail, 3 or higher being high detail)",
    }
    OBLIGATE_ARGS = list(OBLIGATE_ARG_DESCRIPTIONS)
    KEYWORD_ARGS = list(KEYWORD_ARG_DESCRIPTIONS)


    class SeeObjectCommandArgs():
        def __init__(self, commandArgs: dict):
            objectTypeStr = commandArgs["object type"]
            if objectTypeStr not in ["habit", "recurrence"]:
                raise InvalidCommandArgsException("the 'object type' argument must be either 'habit' or 'recurrence'.", CommandEnum.SEE)
            self.objectType = {"habit": Habit, "recurrence": Recurrence}[objectTypeStr]

            self.objectName = commandArgs["object name"]

            verbosityStr = commandArgs["v"]
            try:
                self.verbosity = int(verbosityStr)
            except ValueError:
                raise InvalidCommandArgsException("the 'verbosity' argument must be an integer.")

    
    @staticmethod
    def keywordArgDefaults():
        return {
            "v": "5"
        }

    
    @staticmethod
    def executeCommand(commandArgs: dict, indent: int=0):
        objectTypeStr = commandArgs["object type"]
        seeObjectCommandArgs = SeeObjectCommand.SeeObjectCommandArgs(commandArgs)
        objectType = seeObjectCommandArgs.objectType
        objectName = seeObjectCommandArgs.objectName
        verbosity = seeObjectCommandArgs.verbosity
        try:
            if objectType == Habit:
                habit = HabitDataStack.getHabit(objectName)
                habitText = habit.toText(verbosity=verbosity, indent=indent)
                UserOutput.indentedPrint(habitText)
            elif objectType == Recurrence:
                recurrence = RecurrenceDataStack.getRecurrence(objectName)
                recurrenceText = recurrence.toText(verbosity=verbosity, indent=indent)
                UserOutput.indentedPrint(recurrenceText)
            else:
                raise InvalidCommandArgsException("unrecognized object type.", CommandEnum.SEE)
        except KeyError:
            raise InvalidCommandArgsException(f"a {objectTypeStr} with this name could not be found.", CommandEnum.SEE)



class NewObjectCommand(Command):
    NAME = "new object"
    SHORTCUT = "new"
    DESCRIPTION = "create a new object such as a habit or recurrence."
    OBLIGATE_ARG_DESCRIPTIONS = {
        "object type": "type of object to create, i.e. 'habit' or 'recurrence'."
    }
    KEYWORD_ARG_DESCRIPTIONS = {
        
    }
    OBLIGATE_ARGS = list(OBLIGATE_ARG_DESCRIPTIONS)
    KEYWORD_ARGS = list(KEYWORD_ARG_DESCRIPTIONS)


    class NewObjectCommandArgs():
        def __init__(self, commandArgs: dict):
            objectTypeStr = commandArgs["object type"]
            if objectTypeStr not in ["habit", "recurrence"]:
                raise InvalidCommandArgsException("the 'object type' command argument must be either 'habit' or 'recurrence'.", CommandEnum.NEW)
            self.objectType = {"habit": Habit, "recurrence": Recurrence}[objectTypeStr]


    @staticmethod
    def keywordArgDefaults():
        return {

        }
    

    @staticmethod
    def executeCommand(commandArgs: dict, indent: int=0):
        newObjectCommandArgs = NewObjectCommand.NewObjectCommandArgs(commandArgs)
        objectType = newObjectCommandArgs.objectType

        if objectType == Habit: 
            habit = HabitDataStackSecondaryInterface.habitSetupPrompt(indent=indent)
            HabitDataStackSecondaryInterface.saveHabitPrompt(habit, indent=indent+1)
        elif objectType == Recurrence:
            recurrence = RecurrenceDataStackSecondaryInterface.generalRecurrenceSetupPrompt(indent=indent)
            RecurrenceDataStackSecondaryInterface.generalSaveRecurrencePrompt(recurrence, indent=indent+1)
        else:
            raise InvalidCommandArgsException("unrecognized object type.", CommandEnum.NEW)



class DeleteObjectCommand(Command):
    NAME = "delete object"
    SHORTCUT = "del"
    DESCRIPTION = "delete an object such as a habit or recurrence."
    OBLIGATE_ARG_DESCRIPTIONS = {
        "object type": "type of object to delete i.e. 'habit' or 'recurrence'.",
        "object name": "name of habit or recurrence.",
    }
    KEYWORD_ARG_DESCRIPTIONS = {

    }
    OBLIGATE_ARGS = list(OBLIGATE_ARG_DESCRIPTIONS)
    KEYWORD_ARGS = list(KEYWORD_ARG_DESCRIPTIONS)


    class DeleteObjectCommandArgs():
        def __init__(self, commandArgs):
            objectTypeStr = commandArgs["object type"]
            if objectTypeStr not in ["habit", "recurrence"]:
                raise InvalidCommandArgsException("the 'object type' argument must be either 'habit' or 'recurrence'.", CommandEnum.DELETE)
            self.objectType = {"habit": Habit, "recurrence": Recurrence}[objectTypeStr]

            self.objectName = commandArgs["object name"]

    
    @staticmethod
    def keywordArgDefaults():
        return {

        }


    @staticmethod
    def executeCommand(commandArgs: dict, indent: int=0):
        objectTypeStr = commandArgs["object type"]
        deleteObjectCommandArgs = DeleteObjectCommand.DeleteObjectCommandArgs(commandArgs)
        objectType = deleteObjectCommandArgs.objectType
        objectName = deleteObjectCommandArgs.objectName
        try:
            if objectType == Habit:
                habit = HabitDataStack.getHabit(objectName)
                habitText = habit.toText(verbosity=5, indent=indent)
                UserOutput.indentedPrint(habitText)
                delete = UserInput.getBoolInput("delete the habit above? ", indent=indent)
                if delete:
                    HabitDataStack.removeHabit(objectName)
                    UserOutput.printWhitespace()
                    UserOutput.indentedPrint("habit deleted.", indent=indent)
                else:
                    UserOutput.printWhitespace()
                    UserOutput.indentedPrint("deletion cancelled.", indent=indent)
            elif objectType == Recurrence:
                recurrence = RecurrenceDataStack.getRecurrence(objectName)
                recurrenceText = recurrence.toText(verbosity=5, indent=indent)
                UserOutput.indentedPrint(recurrenceText)
                delete = UserInput.getBoolInput("delete the recurrence above? ", indent=indent)
                if delete:
                    RecurrenceDataStack.removeRecurrence(objectName)
                    UserOutput.printWhitespace()
                    UserOutput.indentedPrint("recurrence deleted.", indent=indent)
                else:
                    UserOutput.printWhitespace()
                    UserOutput.indentedPrint("deletion cancelled.", indent=indent)
            else:
                raise InvalidCommandArgsException("unrecognized object type.", CommandEnum.DELETE)
        except KeyError:
            raise InvalidCommandArgsException(f"a {objectTypeStr} with this name could not be found.", CommandEnum.DELETE)



class SeeCalendarCommand(Command):
    NAME = "see calendar"
    SHORTCUT = "cal"
    OBLIGATE_ARG_DESCRIPTIONS = {

    }
    KEYWORD_ARG_DESCRIPTIONS = {
        "date": "some representative date that lies within the time range of the desired month"
    }
    OBLIGATE_ARGS = list(OBLIGATE_ARG_DESCRIPTIONS)
    KEYWORD_ARGS = list(KEYWORD_ARG_DESCRIPTIONS)


    class SeeCalendarCommandArgs():
        def __init__(self, commandArgs: dict):
            dateStr = commandArgs["date"]
            try:
                dateFormat = CalendarObjects.DATE_STR_TEXT_INPUT_FORMAT
                self.date = dt.datetime.strptime(dateStr, dateFormat).date()
            except ValueError:
                dateFormatExample = CalendarObjects.DATE_STR_TEXT_INPUT_FORMAT_EXAMPLE
                raise InvalidCommandArgsException(f"date must be in the form {dateFormatExample}.")

    
    @staticmethod
    def keywordArgDefaults():
        today = dt.date.today().strftime(CalendarObjects.DATE_STR_TEXT_INPUT_FORMAT)

        return {
            "date": today
        }


    @staticmethod
    def executeCommand(commandArgs: dict, indent: int=0):
        seeCalendarCommandArgs = SeeCalendarCommand.SeeCalendarCommandArgs(commandArgs)
        date = seeCalendarCommandArgs.date
        Calendar.display(date)



class SeeChecklistCommand(Command):
    NAME = "see checklist"
    SHORTCUT = "scl"
    DESCRIPTION = "view a checklist of habits."
    OBLIGATE_ARG_DESCRIPTIONS = {
        "checklist type": "type of checklist i.e. 'day', 'range', 'overdue', 'upcoming', or 'all'."
    }
    KEYWORD_ARG_DESCRIPTIONS = {

    }
    OBLIGATE_ARGS = list(OBLIGATE_ARG_DESCRIPTIONS)
    KEYWORD_ARGS = list(KEYWORD_ARG_DESCRIPTIONS)


    @staticmethod
    def keywordArgDefaults():
        return {

        }


    @staticmethod
    def executeCommand(commandArgs: dict, indent: int=0):
        checklistType = commandArgs["checklist type"]
        if checklistType == "day":
            SeeChecklistCommand.dayChecklist(indent=indent)
        elif checklistType == "range":
            SeeChecklistCommand.rangeChecklist(indent=indent)
        elif checklistType == "overdue":
            SeeChecklistCommand.overdueChecklist(indent=indent)
        elif checklistType == "upcoming":
            SeeChecklistCommand.upcomingChecklist(indent=indent)
        elif checklistType == "all":
            SeeChecklistCommand.allChecklists(indent=indent)
        else:
            raise InvalidCommandArgsException("not a recognized checklist type.", CommandEnum.SEE_CHECKLIST)

        
    @staticmethod
    def dayChecklist(indent: int=0):
        day = UserInput.getDateInput(prompt="which day? ", indent=indent)
        checklist = SingleDayChecklist(day)
        UserOutput.printWhitespace()
        checklist.display(indent=indent)


    @staticmethod
    def rangeChecklist(indent: int=0):
        startDay = UserInput.getDateInput("start day? ", indent=indent)
        endDay = UserInput.getDateInput("end day? ", indent=indent)

        checklist = DayRangeChecklist(startDay, endDay)
        checklist.display(indent=indent)


    @staticmethod
    def overdueChecklist(indent: int=0):
        checklist = OverdueChecklist()
        checklist.display(indent=indent)

    
    @staticmethod
    def upcomingChecklist(indent: int=0):
        checklist = UpcomingChecklist()
        checklist.display(indent=indent)

    
    @staticmethod
    def allChecklists(indent: int=0):
        OverdueChecklist().display(indent=indent)
        UserOutput.printWhitespace()
        UpcomingChecklist().display(indent=indent)
        UserOutput.printWhitespace()
        SingleDayChecklist(dt.date.today()).display(indent=indent)



class ListObjectsCommand(Command):
    NAME = "list objects"
    SHORTCUT = "list"
    DESCRIPTION = "view a list of all existing habits or recurrences."
    OBLIGATE_ARG_DESCRIPTIONS = {
        "object type": "type of object to show a list of, i.e. 'habits' or 'recurrences'."
    }
    KEYWORD_ARG_DESCRIPTIONS = {
        "v": "verbosity, or how much detail to show (-1 or lower being no detail, 3 or higher being high detail)",
    }
    OBLIGATE_ARGS = list(OBLIGATE_ARG_DESCRIPTIONS)
    KEYWORD_ARGS = list(KEYWORD_ARG_DESCRIPTIONS)


    class ListObjectsCommandArgs():
        def __init__(self, commandArgs: dict):
            objectTypeStr = commandArgs["object type"]
            if objectTypeStr not in ["habits", "recurrences"]:
                raise InvalidCommandArgsException("the 'object type' argument must be either 'habits' or 'recurrences'.", CommandEnum.LIST_OBJECTS)
            self.objectType = {"habits": Habit, "recurrences": Recurrence}[objectTypeStr]
            
            verbosityStr = commandArgs["v"]
            try:
                self.verbosity = int(verbosityStr)
            except ValueError:
                raise InvalidCommandArgsException("the 'verbosity' argument must be an integer.", CommandEnum.LIST_OBJECTS)


    @staticmethod
    def keywordArgDefaults():
        return {
            "v": "1"
        }


    @staticmethod
    def executeCommand(commandArgs: dict, indent: int=0):
        listObjectsCommandArgs = ListObjectsCommand.ListObjectsCommandArgs(commandArgs)
        objectType = listObjectsCommandArgs.objectType
        verbosity = listObjectsCommandArgs.verbosity
        if objectType == Habit:
            ListObjectsCommand.listHabits(verbosity, indent=indent)
        elif objectType == Recurrence:
            ListObjectsCommand.listRecurrences(verbosity, indent=indent)
        else:
            raise InvalidCommandArgsException("invalid object type.", CommandEnum.LIST_OBJECTS)

    
    @staticmethod
    def listHabits(verbosity, indent: int=0):
        dataStack = HabitDataStack.getData()
        if dataStack in [None, {}]:
            UserOutput.indentedPrint("no habits yet.", indent=indent)
            return
        
        UserOutput.indentedPrint("all habits: ", indent=indent)
        UserOutput.printWhitespace(verbosity)
        i = 0
        for habitName in dataStack:
            habit = HabitDataStack.getHabit(habitName)
            habitText = habit.toText(verbosity=verbosity, indent=indent+1)
            if verbosity >= 0:
                UserOutput.indentedPrint(habitText)
            if i < len(dataStack) - 1:
                UserOutput.printWhitespace(verbosity)
            i += 1


    @staticmethod
    def listRecurrences(verbosity, indent: int=0):
        indentA = UserOutput.indentPadding(indent=indent)
        indentB = UserOutput.indentPadding(indent=indent+1)
        dataStack = RecurrenceDataStack.getData()
        if dataStack in [None, {}]:
            UserOutput.indentedPrint("no recurrences yet.", indent=indent)
            return
        
        UserOutput.indentedPrint("all recurrences: ", indent=indent)
        UserOutput.printWhitespace(verbosity)
        i = 0
        for recurrenceName in dataStack:
            recurrence = RecurrenceDataStack.getRecurrence(recurrenceName)
            recurrenceText = f"{indentB}{recurrenceName}"
            recurrenceText += f"\n{recurrence.toText(verbosity=verbosity, indent=indent+2)}"
            if verbosity >= 0:
                UserOutput.indentedPrint(recurrenceText)
            if i < len(dataStack) - 1:
                UserOutput.printWhitespace(verbosity)
            i += 1



class CompleteHabitCommand(Command):
    NAME = "complete habit"
    SHORTCUT = "done"
    DESCRIPTION = "check a habit off for today. This will increase your quota met on that habit."
    OBLIGATE_ARG_DESCRIPTIONS = {
        "habit name": "name of the habit.",
    }
    KEYWORD_ARG_DESCRIPTIONS = {
        "t": "time when the habit was completed",
    }
    OBLIGATE_ARGS = list(OBLIGATE_ARG_DESCRIPTIONS)
    KEYWORD_ARGS = list(KEYWORD_ARG_DESCRIPTIONS)


    class CompleteHabitCommandArgs():
        def __init__(self, commandArgs):
            habitName = commandArgs["habit name"]
            habitData = HabitDataStack.getData()
            if habitName not in habitData:
                raise InvalidCommandArgsException("the 'habit' argument must be the name of an existing habit.", CommandEnum.COMPLETE_HABIT)
            self.habit = HabitDataStack.getHabit(habitName)
            
            timeStr = commandArgs["t"]
            timeFormat = CalendarObjects.TIME_STR_TEXT_INPUT_FORMAT
            try:
                self.completionTime = dt.datetime.strptime(timeStr, timeFormat).time()
            except ValueError:
                timeFormatExample = CalendarObjects.TIME_STR_TEXT_INPUT_FORMAT_EXAMPLE
                raise InvalidCommandArgsException(f"the 't' argument must be in the form {timeFormatExample}", CommandEnum.COMPLETE_HABIT)
    

    @staticmethod
    def keywordArgDefaults():
        t = dt.datetime.now().time()
        timeStr = t.strftime(CalendarObjects.TIME_STR_TEXT_INPUT_FORMAT)
        return {
            "t": timeStr
        }


    @staticmethod
    def executeCommand(commandArgs: dict, indent: int=0):
        completeHabitCommandArgs = CompleteHabitCommand.CompleteHabitCommandArgs(commandArgs)
        habit = completeHabitCommandArgs.habit
        completionTime = completeHabitCommandArgs.completionTime
        HabitDataStackSecondaryInterface.completeHabit(habit, completionTime=completionTime, indent=indent)

    

class DismissHabitCommand(Command):
    NAME = "dismiss habit"
    SHORTCUT = "dismiss"
    DESCRIPTION = "dismiss a habit from the overdue checklist."
    OBLIGATE_ARG_DESCRIPTIONS = {
        "habit name": "name of the habit.",
    }
    KEYWORD_ARG_DESCRIPTIONS = {
        
    }
    OBLIGATE_ARGS = list(OBLIGATE_ARG_DESCRIPTIONS)
    KEYWORD_ARGS = list(KEYWORD_ARG_DESCRIPTIONS)


    class DismissHabitCommandArgs():
        def __init__(self, commandArgs):
            habitName = commandArgs["habit name"]
            habitData = HabitDataStack.getData()
            if habitName not in habitData:
                raise InvalidCommandArgsException("the 'habit' argument must be the name of an existing habit.", CommandEnum.DISMISS_HABIT)
            self.habit = HabitDataStack.getHabit(habitName)
    

    @staticmethod
    def keywordArgDefaults():
        return {

        }


    @staticmethod
    def executeCommand(commandArgs: dict, indent: int=0):
        completeHabitCommandArgs = DismissHabitCommand.DismissHabitCommandArgs(commandArgs)
        habit = completeHabitCommandArgs.habit
        HabitDataStackSecondaryInterface.dismissHabit(habit, indent=indent)



class CommandEnum(Enum):
    HELP = HelpCommand()
    EXIT = ExitCommand()
    SEE = SeeObjectCommand()
    NEW = NewObjectCommand()
    DELETE = DeleteObjectCommand()
    SEE_CALENDAR = SeeCalendarCommand()
    SEE_CHECKLIST = SeeChecklistCommand()
    LIST_OBJECTS = ListObjectsCommand()
    COMPLETE_HABIT = CompleteHabitCommand()
    DISMISS_HABIT = DismissHabitCommand()
    
