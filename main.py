from DataObjectConversion.yamlInteraction import YAMLInteraction
from HabitsAndChecklists.recurrence import Recurrence, RecurrencePeriod
from HabitsAndChecklists.recurrence import DailyRecurrence, WeeklyRecurrence, MonthlyRecurrence
from HabitsAndChecklists.habit import Habit
import datetime as dt
import calendar as cal
import yaml
from UserInteraction.userIO import UserIO
from DateAndTime.calendarObjects import CalendarObjects
import pprint


def main():
    habit = Habit.setupPrompt()
    isUpcoming = habit.isUpcoming()
    print(isUpcoming)


if __name__ == "__main__":
    main()