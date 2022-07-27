from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataStacks.dataStack import DataStack
from HabitsAndChecklists.habit import Habit



class HabitDataStack(DataStack):
    habits = YAMLInteraction.YAMLtoData(YAMLFiles.HABITS)
    if habits == None: habits = {}

    
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