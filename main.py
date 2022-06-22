from DataObjectConversion.yamlInteraction import YAMLInteraction
from HabitsAndChecklists.recurrence import Recurrence, RecurrencePeriod
from HabitsAndChecklists.recurrence import DailyRecurrence, WeeklyRecurrence, MonthlyRecurrence
from HabitsAndChecklists.habit import Habit
import datetime as dt
import calendar as cal
import yaml
from UserInteraction.userIO import UserIO


def main():
    dictionary = YAMLInteraction.YAMLtoDict("StoredData/habits.yml")
    recurrenceInYaml = WeeklyRecurrence([1, 2, 4])
    dictionary["recurrence in yaml"] = str(recurrenceInYaml)
    dictionary["list"] = [6, 4, 38]
    YAMLInteraction.dictToYAML("StoredData/yamlDump.yml", dictionary)

    recurrence = MonthlyRecurrence([2, 17])
    print(recurrence.isToday())


    tim = dt.time(1, 1, 1)
    habit = Habit("walk chippy", True, 2, recurrence, [tim])

    nextOccurrence = recurrence.nextOccurrence()
    print(nextOccurrence)

    print(dt.datetime.now().weekday())

    print(UserIO.multiSelectString("options:", ["hello", "world"]))


    recurrence2 = Recurrence.setupPrompt()
    print(recurrence2.toText())



if __name__ == "__main__":
    main()