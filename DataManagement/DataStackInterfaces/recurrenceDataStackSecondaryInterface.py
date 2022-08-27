from calendar import monthrange
import datetime as dt
from DataManagement.DataStacks.recurrenceDataStack import RecurrenceDataStack
from DateAndTime.calendarObjects import CalendarObjects
from HabitsAndChecklists.recurrence import (AggregateRecurrence,
                                            DailyRecurrence,
                                            DaysOfMonthKRecurrence,
                                            MonthlyRecurrence,
                                            NthWeekdayMOfMonthKRecurrence,
                                            OnceRecurrence, Recurrence,
                                            RecurrencePeriod, WeeklyRecurrence,
                                            YearlyRecurrence)
from UserInteraction.userInput import UserInput
from VisualsAndOutput.userOutput import UserOutput



class RecurrenceDataStackSecondaryInterface:
    @staticmethod
    def generalRecurrenceSetupPrompt(indent: int=0):
        UserOutput.indentedPrint("recurrence", indent=indent)
        prompt = f"what kind of recurrence?"
        options = [rp.value for rp in RecurrencePeriod]
        recurrencePeriodName = UserInput.singleSelectString(prompt, options, indent=indent+1)
        recurrencePeriod = Recurrence.RECURRENCE_PERIOD_NAME_TO_ID[recurrencePeriodName]

        setupPromptMethodDict = {
            RecurrencePeriod.DAILY: RecurrenceDataStackSecondaryInterface.dailyRecurrencesetupPrompt,
            RecurrencePeriod.WEEKLY: RecurrenceDataStackSecondaryInterface.weeklyRecurrenceSetupPrompt,
            RecurrencePeriod.MONTHLY: RecurrenceDataStackSecondaryInterface.monthlyRecurrenceSetupPrompt,
            RecurrencePeriod.YEARLY: RecurrenceDataStackSecondaryInterface.yearlyRecurrenceSetupPrompt,
            RecurrencePeriod.DAYS_OF_MONTH_K: RecurrenceDataStackSecondaryInterface.daysOfMonthKRecurrenceSetupPrompt,
            RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K: RecurrenceDataStackSecondaryInterface.nthWeekdayOfMonthKRecurrenceSetupPrompt,
            RecurrencePeriod.ONCE: RecurrenceDataStackSecondaryInterface.onceRecurrenceSetupPrompt,
            RecurrencePeriod.AGGREGATE: RecurrenceDataStackSecondaryInterface.aggregateRecurrenceSetupPrompt,
        }

        try:
            setupPromptMethod = setupPromptMethodDict[recurrencePeriod]
        except KeyError:
            raise NotImplementedError(f"recurrence period {recurrencePeriodName} not handled")

        return setupPromptMethod(indent=indent+1)

    
    @staticmethod
    def generalSaveRecurrencePrompt(recurrence: Recurrence, indent: int=0):
        UserOutput.indentedPrint("recurrence", indent=indent)
        print(recurrence.toText(indent=indent+1))
        save = UserInput.getBoolInput("save the above recurrence?", indent=indent)
        if save: 
            name = UserInput.getStringInput("what would you like to save this recurrence as? ", indent=indent)
            RecurrenceDataStack.addRecurrence(recurrence, name)
        return save


    
    @staticmethod
    def dailyRecurrencesetupPrompt(indent: int=0) -> DailyRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.DAILY.value} recurrence", indent=indent)
        return DailyRecurrence()


    
    @staticmethod
    def weeklyRecurrenceSetupPrompt(indent: int=0) -> WeeklyRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.WEEKLY.value} recurrence", indent=indent)
        dayNames = UserInput.multiSelectString("which weekdays? ", CalendarObjects.WEEKDAY_NAMES, indent=indent+1)
        dayNums = sorted([CalendarObjects.WEEKDAY_NAME_TO_NUM[dayName] for dayName in dayNames])
        weekdays = [CalendarObjects.WEEKDAY_NUM_TO_ID[dayNum] for dayNum in dayNums]
        return WeeklyRecurrence(weekdays)


    @staticmethod
    def monthlyRecurrenceSetupPrompt(indent: int=0) -> MonthlyRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.MONTHLY.value} recurrence", indent=indent)
        days = UserInput.getIntListInput("which month days? ", indent=indent+1)
        return MonthlyRecurrence(days)


    @staticmethod
    def yearlyRecurrenceSetupPrompt(indent: int=0) -> YearlyRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.YEARLY.value} recurrence", indent=indent)
        days = UserInput.getIntListInput("which days of the year? ", minimum=1, maximum=366, indent=indent+1)
        return YearlyRecurrence(days)


    @staticmethod
    def daysOfMonthKRecurrenceSetupPrompt(indent: int=0) -> DaysOfMonthKRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.DAYS_OF_MONTH_K.value} recurrence", indent=indent)
        monthName = UserInput.singleSelectString("which month? ", CalendarObjects.MONTH_NAMES, indent=indent+1)
        month = CalendarObjects.MONTH_NAME_TO_ID[monthName]
        today = dt.date.today()
        daysInMonth = monthrange(today.year, month.value.num)[1]
        days = UserInput.getIntListInput(prompt=f"which days of {monthName}? ", minimum=1, maximum=daysInMonth, indent=indent+1)
        return DaysOfMonthKRecurrence(month, days)


    @staticmethod
    def nthWeekdayOfMonthKRecurrenceSetupPrompt(indent: int=0) -> NthWeekdayMOfMonthKRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K.value} recurrence", indent=indent)
        monthName = UserInput.singleSelectString("which month? ", CalendarObjects.MONTH_NAMES, indent=indent+1)
        weekdayName = UserInput.singleSelectString("which weekday? ", CalendarObjects.WEEKDAY_NAMES, indent=indent+1)
        n = UserInput.getIntInput(f"which (n)th {weekdayName} of {monthName}? ", minimum=1, maximum=5, indent=indent+1)
        month = CalendarObjects.MONTH_NAME_TO_ID[monthName]
        weekday = CalendarObjects.WEEKDAY_NAME_TO_ID[weekdayName]
        return NthWeekdayMOfMonthKRecurrence(month, weekday, n)


    @staticmethod
    def onceRecurrenceSetupPrompt(indent: int=0) -> OnceRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.ONCE.value} recurrence", indent=indent)
        date = UserInput.getDateInput("when? ", indent=indent+1)
        return OnceRecurrence(date)

    
    @staticmethod
    def aggregateRecurrenceSetupPrompt(indent: int=0) -> AggregateRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.AGGREGATE.value} recurrence", indent=indent)
        recurrences = []
        keepAdding = UserInput.getBoolInput("add a recurrence? ", indent=indent+1)
        while keepAdding:
            recurrence = RecurrenceDataStackSecondaryInterface.generalRecurrenceSetupPrompt(indent=indent+1)
            recurrences.append(recurrence)
            keepAdding = UserInput.getBoolInput("add another recurrence? ", indent=indent+1)
        return AggregateRecurrence(recurrences)
