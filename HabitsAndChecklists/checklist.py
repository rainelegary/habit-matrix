from DataObjectConversion.dataEquivalent import DataEquivalent
from DataObjectConversion.textEquivalent import TextEquivalent
import datetime as dt
from abc import ABC, abstractmethod
from DateAndTime.calendarObjects import CalendarObjects
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput
from DataManagement.DataStacks.dataStack import DataStack
from HabitsAndChecklists.habit import Habit



class Checklist(ABC):
    @abstractmethod
    def display(self):
        raise NotImplementedError("method not yet implemented in subclass")



class SingleDayChecklist(Checklist):
    def __init__(self, day: dt.date=dt.date.today()):
        self.day = day


    def display(self, indent: int=0):
        dayString = self.day.strftime(CalendarObjects.DATE_STR_FORMAT)
        UserOutput.indentedPrint(f"checklist for {dayString}", indent=indent)
        for habit in self.getHabits():
            UserOutput.indentedPrint(habit.title, indent=indent+1)
        
    
    def getHabits(self):
        for habitName in DataStack.habits:
            habit = DataStack.getHabit(habitName)
            if habit.isToday(self.day):
                yield habit
                


class DayRangeChecklist(Checklist):
    def __init__(self, startDay: dt.date, endDay: dt.date):
        self.startDay = startDay
        self.endDay = endDay


    def display(self, indent: int=0):
        startDayString = self.startDay.strftime(CalendarObjects.DATE_STR_FORMAT) 
        endDayString = self.endDay.strftime(CalendarObjects.DATE_STR_FORMAT)
        UserOutput.indentedPrint(f"checklist for {startDayString} to {endDayString}")
        for day in self.dayRange():
            SingleDayChecklist.display(day, indent=indent+1)
    

    def dayRange(self):
        for n in range(int((self.endDay - self.startDay + dt.timedelta(days=1)).days)):
            yield self.startDay + dt.timedelta(n)



class OverdueChecklist(Checklist):
    def __init__(self):
        """no specialized constructor necessary"""


    def display(self, indent: int=0):
        UserOutput.indentedPrint("overdue checklist", indent=indent)
        for habitName in DataStack.habits:
            habit = DataStack.getHabit(habitName)
            quotaState = habit.quotaState
            if quotaState is not None and quotaState.quotaMet < 0:
                UserOutput.indentedPrint(f"{habit.title}", indent=indent+1)



class UpcomingChecklist(Checklist):
    def __init__(self):
        """no specialized constructor necessary"""


    def display(self, indent: int=0):
        UserOutput.indentedPrint("upcoming checklist", indent=indent)
        for habitName in DataStack.habits:
            habit = DataStack.getHabit(habitName)
            if habit.isUpcoming():
                UserOutput.indentedPrint(f"{habit.title}", indent=indent+1)


