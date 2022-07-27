import copy

from HabitsAndChecklists.habit import Habit
from HabitsAndChecklists.recurrence import Recurrence

from DataObjectConversion.yamlInteraction import YAMLFiles, YAMLInteraction



class DataStack:
    habits = YAMLInteraction.YAMLtoData(YAMLFiles.HABITS)
    if habits == None: habits = {}
    recurrences = YAMLInteraction.YAMLtoData(YAMLFiles.RECURRENCES)
    if recurrences == None: recurrences = {}
    sessionInfo = YAMLInteraction.YAMLtoData(YAMLFiles.SESSION_INFO)
    if sessionInfo == None: sessionInfo = {}


    @classmethod
    def saveChanges(cls):
        YAMLInteraction.dataToYAML(YAMLFiles.HABITS, cls.habits)
        YAMLInteraction.dataToYAML(YAMLFiles.RECURRENCES, cls.recurrences)
        YAMLInteraction.dataToYAML(YAMLFiles.SESSION_INFO, cls.sessionInfo)


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

    
    @classmethod
    def getSessionInfo(cls):
        return copy.deepcopy(cls.sessionInfo)


    @classmethod
    def setSessionInfo(cls, info):
        cls.sessionInfo = copy.deepcopy(info)
