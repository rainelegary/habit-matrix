from DataObjectConversion.yamlInteraction import YAMLInteraction, YAMLFiles
from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.recurrence import Recurrence


class DataStack:
    habits = YAMLInteraction.YAMLtoData(YAMLFiles.HABITS)
    recurrences = YAMLInteraction.YAMLtoData(YAMLFiles.RECURRENCES)
    if habits == None: habits = {}
    if recurrences == None: recurrences = {}


    @classmethod
    def saveChanges(cls):
        YAMLInteraction.dataToYAML(YAMLFiles.HABITS, cls.habits)
        YAMLInteraction.dataToYAML(YAMLFiles.RECURRENCES, cls.recurrences)


    @classmethod
    def addHabit(cls, habit: Habit):
        cls.habits = cls.habits | habit.toData()


    @classmethod
    def removeHabit(cls, name):
        del cls.habits[name]


    @classmethod
    def addRecurrence(cls, recurrence: Recurrence, name):
        cls.recurrences[name] = recurrence.toData()


    @classmethod
    def removeRecurrence(cls, name):
        del cls.recurrences[name]