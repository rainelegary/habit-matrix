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
    def removeHabit(cls, name: str):
        del cls.habits[name]

    
    @classmethod
    def getHabit(cls, name: str) -> Habit:
        if name not in cls.habits:
            raise Exception("habit not found")
        habitDict = cls.habits[name]
        return Habit.fromData(data={name: habitDict})


    @classmethod
    def addRecurrence(cls, recurrence: Recurrence, name: str):
        cls.recurrences[name] = recurrence.toData()


    @classmethod
    def removeRecurrence(cls, name: str):
        del cls.recurrences[name]


    @classmethod
    def getRecurrence(cls, name: str) -> Recurrence:
        if name not in cls.recurrences:
            raise Exception("recurrence not found")
        recurrenceDict = cls.recurrences[name]
        return Recurrence.fromData(data=recurrenceDict)
