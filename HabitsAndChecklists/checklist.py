from turtle import color
from DataManagement.DataHelpers.dataEquivalent import DataEquivalent
from DataManagement.DataHelpers.textEquivalent import TextEquivalent
import datetime as dt
from abc import ABC, abstractmethod
from DataManagement.DataStacks.habitDataStack import HabitDataStack
from DateAndTime.calendarObjects import CalendarObjects
from UserInteraction.userInput import UserInput
from VisualsAndOutput.color import ColorEnum
from VisualsAndOutput.userOutput import UserOutput
from DataManagement.DataHelpers.dataStack import DataStack
from HabitsAndChecklists.habit import Habit



class Checklist(ABC):
    def display(self, header: str, headerColor: ColorEnum, isInChecklistDeciderFunction, 
    passiveDoneTodo: bool, referenceDate=dt.date.today(), indent: int=0):
        UserOutput.indentedPrint(header, indent=indent, textColor=headerColor)

        if passiveDoneTodo:
            passive = []
            done = []
            todo = []
        else:
            general = []
        
        for habitName in HabitDataStack.getData():
            habit = HabitDataStack.getHabit(habitName)
            if isInChecklistDeciderFunction(habit):
                if habit.required:
                    applicableCompletionDate = habit.quotaState.applicableCompletionDate(habit.recurrence, referenceDate=referenceDate)
                    allCompletionDates = habit.quotaState.allCompletionDates
                if not passiveDoneTodo:
                    general.append(habit)
                elif not habit.required:
                    passive.append(habit)
                elif applicableCompletionDate in allCompletionDates:
                    done.append(habit)
                else:
                    todo.append(habit)

        def printSection(habits: list[Habit], indent: int=0):
            if len(habits) == 0:
                UserOutput.indentedPrint("none", indent=indent)
            for habit in habits:
                UserOutput.indentedPrint(habit.title, indent=indent)
        
        if passiveDoneTodo:
            UserOutput.indentedPrint("passive", indent=indent+1)
            printSection(passive, indent=indent+2)
            
            UserOutput.indentedPrint("done", indent=indent+1)
            printSection(done, indent=indent+2)

            UserOutput.indentedPrint("todo", indent=indent+1)
            printSection(todo, indent=indent+2)
        else:
            printSection(general, indent=indent+1)
            
        

class SingleDayChecklist(Checklist):
    def __init__(self, day: dt.date=dt.date.today()):
        self.day = day


    def display(self, indent: int=0):
        dayString = self.day.strftime(CalendarObjects.DATE_STR_TEXT_OUTPUT_FORMAT)

        def isInChecklistDeciderFunction(habit: Habit) -> bool:
            return habit.isToday(referenceDate=self.day)

        super().display(f"checklist for {dayString}", ColorEnum.BLUE, isInChecklistDeciderFunction, 
        True, referenceDate=self.day, indent=indent)
                


class DayRangeChecklist(Checklist):
    def __init__(self, startDay: dt.date, endDay: dt.date):
        self.startDay = startDay
        self.endDay = endDay


    def display(self, indent: int=0):
        startDayString = self.startDay.strftime(CalendarObjects.DATE_STR_DATA_FORMAT) 
        endDayString = self.endDay.strftime(CalendarObjects.DATE_STR_DATA_FORMAT)
        UserOutput.printWhitespace()
        UserOutput.indentedPrint(f"checklist for {startDayString} to {endDayString}", textColor=ColorEnum.BLUE)
        UserOutput.printWhitespace()
        dayRange = self.dayRange()
        if len(dayRange) == 0:
            UserOutput.indentedPrint("none", indent=indent+1)
        for i in range(len(dayRange)):
            singleDayChecklist = SingleDayChecklist(dayRange[i])
            singleDayChecklist.display(indent=indent+1)
            if i < len(dayRange) - 1:
                UserOutput.printWhitespace()
            
    
    def dayRange(self):
        dayRange = []
        for n in range(int((self.endDay - self.startDay + dt.timedelta(days=1)).days)):
            dayRange.append(self.startDay + dt.timedelta(days=n))
        
        return dayRange



class LastMinuteChecklist(Checklist):
    def __init__(self):
        """no specialized constructor necessary"""


    def display(self, indent: int=0):

        def isInChecklistDeciderFunction(habit: Habit) -> bool:
            if not habit.required:
                return False
            
            done = (habit.quotaState.prevCompletionDate == habit.prevOccurrence())
            yesterday = dt.date.today() - dt.timedelta(days=1)
            prevEqApp = habit.prevOccurrence(yesterday) == habit.quotaState.applicableCompletionDate(habit.recurrence)
            return prevEqApp and not done

        super().display("last minute checklist", ColorEnum.PURPLE, isInChecklistDeciderFunction, False, indent=indent)



class OverdueChecklist(Checklist):
    def __init__(self):
        """no specialized constructor necessary"""


    def display(self, indent: int=0):

        def isInChecklistDeciderFunction(habit: Habit) -> bool:
            return habit.required and habit.quotaState.overdue

        super().display("overdue checklist", ColorEnum.RED, isInChecklistDeciderFunction, False, indent=indent)



class UpcomingChecklist(Checklist):
    def __init__(self):
        """no specialized constructor necessary"""


    def display(self, indent: int=0):

        def isInChecklistDeciderFunction(habit: Habit) -> bool:
            return habit.isUpcoming()

        super().display("upcoming checklist", ColorEnum.BLUE, isInChecklistDeciderFunction, True, indent=indent)

