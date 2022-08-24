from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataHelpers.dataStack import DataStack
from HabitsAndChecklists.habit import Habit



class HabitDataStack(DataStack):
    YAML_FILE = YAMLFiles.HABITS
    __dataStack = YAMLInteraction.YAMLtoData(YAMLFiles.HABITS)
    if __dataStack == None: __dataStack = {}
    

    @classmethod
    def addHabit(cls, habit: Habit):
        cls.__dataStack = cls.__dataStack | habit.toData()


    @classmethod
    def removeHabit(cls, name: str):
        del cls.__dataStack[name]


    @classmethod 
    def updateHabit(cls, habit: Habit):
        cls.__dataStack = cls.__dataStack | habit.toData()

    
    @classmethod
    def getHabit(cls, name: str) -> Habit:
        if name not in cls.__dataStack:
            raise KeyError("no habit found with this name")
        
        habitDict = cls.__dataStack[name]
        return Habit.fromData(data={name: habitDict})

    
    @classmethod
    def saveData(cls):
        YAMLInteraction.dataToYAML(cls.YAML_FILE, cls.__dataStack)
    

    @classmethod
    def getData(cls):
        return cls.__dataStack


    @classmethod
    def setData(cls, data):
        cls.__dataStack = data

    
