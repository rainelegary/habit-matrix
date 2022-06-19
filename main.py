from DataObjectConversion.yamlInteraction import YAMLInteraction
from HabitsAndChecklists.recurrence import RecurrencePeriod
from HabitsAndChecklists.recurrence import DailyRecurrence, WeeklyRecurrence, MonthlyRecurrence
import datetime as dt
import calendar as cal

def main():
    dictionary = YAMLInteraction.YAMLtoDict("StoredData/habits.yml")
    recurrence = MonthlyRecurrence([2, 17])
    print(recurrence.isToday())

    nextOccurrence = recurrence.nextOccurrence()
    print(nextOccurrence)



if __name__ == "__main__":
    main()