from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataHelpers.dataStack import DataStack
from HabitsAndChecklists.habit import Habit



class HabitDataStack(DataStack):
    dataStack = YAMLInteraction.YAMLtoData(YAMLFiles.HABITS)
    if dataStack == None: dataStack = {}
    yamlFile = YAMLFiles.HABITS

    
    @classmethod
    def addHabit(cls, habit: Habit):
        cls.dataStack = cls.dataStack | habit.toData()


    @classmethod
    def removeHabit(cls, name: str):
        del cls.dataStack[name]

    
    @classmethod
    def getHabit(cls, name: str) -> Habit:
        if name not in cls.dataStack:
            raise Exception("habit not found")
        habitDict = cls.dataStack[name]
        return Habit.fromData(data={name: habitDict})