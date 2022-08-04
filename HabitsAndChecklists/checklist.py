from DataManagement.DataHelpers.dataEquivalent import DataEquivalent
from DataManagement.DataHelpers.textEquivalent import TextEquivalent
import datetime as dt
from abc import ABC, abstractmethod
from DataManagement.DataStacks.habitDataStack import HabitDataStack
from DateAndTime.calendarObjects import CalendarObjects
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput
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
        for habit in self.getHabits():
            UserOutput.indentedPrint(habit.title, indent=indent+1)
        
    
    def getHabits(self):
        dataStack = HabitDataStack.getData()
        if dataStack == None:
            return
        
        for habitName in dataStack:
            habit = HabitDataStack.getHabit(habitName)
            if habit.isToday(self.day):
                yield habit
                


class DayRangeChecklist(Checklist):
    def __init__(self, startDay: dt.date, endDay: dt.date):
        self.startDay = startDay
        self.endDay = endDay


    def display(self, indent: int=0):
        startDayString = self.startDay.strftime(CalendarObjects.DATE_STR_DATA_FORMAT) 
        endDayString = self.endDay.strftime(CalendarObjects.DATE_STR_DATA_FORMAT)
        UserOutput.indentedPrint(f"checklist for {startDayString} to {endDayString}")
        for day in self.dayRange():
            singleDayChecklist = SingleDayChecklist(day)
            singleDayChecklist.display(indent=indent+1)
    

    def dayRange(self):
        for n in range(int((self.endDay - self.startDay + dt.timedelta(days=1)).days)):
            yield self.startDay + dt.timedelta(days=n)



class OverdueChecklist(Checklist):
    def __init__(self):
        """no specialized constructor necessary"""


    def display(self, indent: int=0):
        UserOutput.indentedPrint("overdue checklist", indent=indent)
        dataStack = HabitDataStack.getData()
        if dataStack == None:
            UserOutput.indentedPrint("none", indent=indent)
            return None
        
        for habitName in dataStack:
            habit = HabitDataStack.getHabit(habitName)
            quotaState = habit.quotaState
            if quotaState is not None and quotaState.quotaMet < 0:
                UserOutput.indentedPrint(f"{habit.title}", indent=indent+1)



class UpcomingChecklist(Checklist):
    def __init__(self):
        """no specialized constructor necessary"""


    def display(self, indent: int=0):
        UserOutput.indentedPrint("upcoming checklist", indent=indent)
        dataStack = HabitDataStack.getData()
        if dataStack == None:
            UserOutput.indentedPrint("none", indent=indent)
            return None
        
        for habitName in dataStack:
            habit = HabitDataStack.getHabit(habitName)
            if habit.isUpcoming():
                UserOutput.indentedPrint(f"{habit.title}", indent=indent+1)


