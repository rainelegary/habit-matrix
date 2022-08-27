from DataManagement.DataHelpers.dataEquivalent import DataEquivalent
from DataManagement.DataHelpers.textEquivalent import TextEquivalent
import datetime as dt
from abc import ABC, abstractmethod
from DataManagement.DataStacks.habitDataStack import HabitDataStack
from DateAndTime.calendarObjects import CalendarObjects
from UserInteraction.userInput import UserInput
from VisualsAndOutput.userOutput import UserOutput
from DataManagement.DataHelpers.dataStack import DataStack
from HabitsAndChecklists.habit import Habit



class Checklist(ABC):
    @abstractmethod
    def display(self):
        raise NotImplementedError("method not yet implemented in subclass")



class SingleDayChecklist(Checklist):
    def __init__(self, day: dt.date=dt.date.today()):
        self.day = day


    def display(self, indent: int=0):
        dayString = self.day.strftime(CalendarObjects.DATE_STR_TEXT_OUTPUT_FORMAT)
        UserOutput.indentedPrint(f"checklist for {dayString}", indent=indent)

        atLeastOne = False
        for habitName in HabitDataStack.getData():
            habit = HabitDataStack.getHabit(habitName)
            if habit.isToday(referenceDate=self.day):
                atLeastOne = True
                UserOutput.indentedPrint(habit.title, indent=indent+1)

        if not atLeastOne:
            UserOutput.indentedPrint("none", indent=indent+1)
                


class DayRangeChecklist(Checklist):
    def __init__(self, startDay: dt.date, endDay: dt.date):
        self.startDay = startDay
        self.endDay = endDay


    def display(self, indent: int=0):
        startDayString = self.startDay.strftime(CalendarObjects.DATE_STR_DATA_FORMAT) 
        endDayString = self.endDay.strftime(CalendarObjects.DATE_STR_DATA_FORMAT)
        UserOutput.printWhitespace()
        UserOutput.indentedPrint(f"checklist for {startDayString} to {endDayString}")
        UserOutput.printWhitespace()
        dayRange = self.dayRange()
        if len(dayRange == 0):
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



class OverdueChecklist(Checklist):
    def __init__(self):
        """no specialized constructor necessary"""


    def display(self, indent: int=0):
        UserOutput.indentedPrint("overdue checklist", indent=indent)
        dataStack = HabitDataStack.getData()
        if dataStack == None:
            UserOutput.indentedPrint("none", indent=indent)
            return None
        
        atLeastOne = False
        for habitName in dataStack:
            habit = HabitDataStack.getHabit(habitName)
            quotaState = habit.quotaState
            if quotaState is not None and quotaState.overdue:
                atLeastOne = True
                UserOutput.indentedPrint(f"{habit.title}", indent=indent+1)

        if not atLeastOne:
            UserOutput.indentedPrint("none", indent=indent+1)



class UpcomingChecklist(Checklist):
    def __init__(self):
        """no specialized constructor necessary"""


    def display(self, indent: int=0):
        UserOutput.indentedPrint("upcoming checklist", indent=indent)
        dataStack = HabitDataStack.getData()
        if dataStack in [None, {}]:
            UserOutput.indentedPrint("none", indent=indent)
            return None
        
        atLeastOne = False
        for habitName in dataStack:
            habit = HabitDataStack.getHabit(habitName)
            if habit.isUpcoming():
                atLeastOne = True
                UserOutput.indentedPrint(f"{habit.title}", indent=indent+1)
        
        if not atLeastOne:
            UserOutput.indentedPrint("none", indent=indent+1)


