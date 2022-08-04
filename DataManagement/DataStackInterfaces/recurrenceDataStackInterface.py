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
from UserInteraction.userOutput import UserOutput



class RecurrenceDataStackInterface:
    @staticmethod
    def generalRecurrenceSetupPrompt(indent: int=0):
        UserOutput.indentedPrint("recurrence", indent)
        prompt = f"what kind of recurrence?"
        options = [rp.value for rp in RecurrencePeriod]
        recurrencePeriodName = UserInput.singleSelectString(prompt, options, indent=indent+1)
        recurrencePeriod = Recurrence.RECURRENCE_PERIOD_NAME_TO_ID[recurrencePeriodName]

        setupPromptMethodDict = {
            RecurrencePeriod.DAILY: RecurrenceDataStackInterface.dailyRecurrencesetupPrompt,
            RecurrencePeriod.WEEKLY: RecurrenceDataStackInterface.weeklyRecurrenceSetupPrompt,
            RecurrencePeriod.MONTHLY: RecurrenceDataStackInterface.monthlyRecurrenceSetupPrompt,
            RecurrencePeriod.YEARLY: RecurrenceDataStackInterface.yearlyRecurrenceSetupPrompt,
            RecurrencePeriod.DAYS_OF_MONTH_K: RecurrenceDataStackInterface.daysOfMonthKRecurrenceSetupPrompt,
            RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K: RecurrenceDataStackInterface.nthWeekdayOfMonthKRecurrenceSetupPrompt,
            RecurrencePeriod.ONCE: RecurrenceDataStackInterface.onceRecurrenceSetupPrompt,
            RecurrencePeriod.AGGREGATE: RecurrenceDataStackInterface.aggregateRecurrenceSetupPrompt,
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
        UserOutput.indentedPrint(f"{RecurrencePeriod.DAILY.value} recurrence", indent)
        return DailyRecurrence()


    
    @staticmethod
    def weeklyRecurrenceSetupPrompt(indent: int=0) -> WeeklyRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.WEEKLY.value} recurrence", indent)
        dayNames = UserInput.multiSelectString("which weekdays? ", CalendarObjects.WEEKDAY_NAMES, indent=indent+1)
        dayNums = sorted([CalendarObjects.WEEKDAY_NAME_TO_NUM[dayName] for dayName in dayNames])
        weekdays = [CalendarObjects.WEEKDAY_NUM_TO_ID[dayNum] for dayNum in dayNums]
        return WeeklyRecurrence(weekdays)


    @staticmethod
    def monthlyRecurrenceSetupPrompt(indent: int=0) -> MonthlyRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.MONTHLY.value} recurrence", indent)
        days = UserInput.getIntListInput("which month days? ", indent=indent+1)
        return MonthlyRecurrence(days)


    @staticmethod
    def yearlyRecurrenceSetupPrompt(indent: int=0) -> YearlyRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.YEARLY.value} recurrence", indent)
        days = UserInput.getIntListInput("which days of the year? ", indent=indent+1)
        return YearlyRecurrence(days)


    @staticmethod
    def daysOfMonthKRecurrenceSetupPrompt(indent: int=0) -> DaysOfMonthKRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.DAYS_OF_MONTH_K.value} recurrence", indent)
        monthName = UserInput.singleSelectString("which month? ", CalendarObjects.MONTH_NAMES, indent=indent+1)
        month = CalendarObjects.MONTH_NAME_TO_ID[monthName]
        days = UserInput.getIntListInput(prompt=f"which days of {monthName}? ", indent=indent+1)
        return DaysOfMonthKRecurrence(month, days)


    @staticmethod
    def nthWeekdayOfMonthKRecurrenceSetupPrompt(indent: int=0) -> NthWeekdayMOfMonthKRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.NTH_WEEKDAY_M_OF_MONTH_K.value} recurrence", indent)
        monthName = UserInput.singleSelectString("which month? ", CalendarObjects.MONTH_NAMES, indent=indent+1)
        weekdayName = UserInput.singleSelectString("which weekday? ", CalendarObjects.WEEKDAY_NAMES, indent=indent+1)
        n = UserInput.getIntInput(f"which (n)th {weekdayName} of {monthName}? ", indent=indent+1)
        month = CalendarObjects.MONTH_NAME_TO_ID[monthName]
        weekday = CalendarObjects.WEEKDAY_NAME_TO_ID[weekdayName]
        return NthWeekdayMOfMonthKRecurrence(month, weekday, n)


    @staticmethod
    def onceRecurrenceSetupPrompt(indent: int=0) -> OnceRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.ONCE.value} recurrence", indent)
        year = UserInput.getIntInput("which year? ", indent=indent+1)
        monthName = UserInput.singleSelectString("which month? ", CalendarObjects.MONTH_NAMES, indent=indent+1)
        day = UserInput.getIntInput(f"which day of {monthName}? ", indent=indent+1)
        month = CalendarObjects.MONTH_NAME_TO_NUM[monthName]
        date = dt.date(year, month, day)
        return OnceRecurrence(date)

    
    @staticmethod
    def aggregateRecurrenceSetupPrompt(indent: int=0) -> AggregateRecurrence:
        UserOutput.indentedPrint(f"{RecurrencePeriod.AGGREGATE.value} recurrence", indent)
        recurrences = []
        keepAdding = UserInput.getBoolInput("add a recurrence? ", indent=indent+1)
        while keepAdding:
            recurrence = RecurrenceDataStackInterface.generalRecurrenceSetupPrompt(indent=indent+1)
            recurrences.append(recurrence)
            keepAdding = UserInput.getBoolInput("add another recurrence? ", indent=indent+1)
        return AggregateRecurrence(recurrences)
