from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataHelpers.dataStack import DataStack
from HabitsAndChecklists.recurrence import Recurrence



class RecurrenceDataStack(DataStack):
    YAML_FILE = YAMLFiles.RECURRENCES
    __dataStack = YAMLInteraction.YAMLtoData(YAMLFiles.RECURRENCES)
    if __dataStack == None: __dataStack = {}


    @classmethod
    def addRecurrence(cls, recurrence: Recurrence, name: str):
        cls.__dataStack[name] = recurrence.toData()


    @classmethod
    def removeRecurrence(cls, name: str):
        del cls.__dataStack[name]

    
    @classmethod 
    def updateRecurrence(cls, name: str, recurrence: Recurrence):
        cls.__dataStack[name] = recurrence.toData()


    @classmethod
    def getRecurrence(cls, name: str) -> Recurrence:
        if name not in cls.__dataStack:
            raise KeyError("no recurrence found with this name.")
        
        recurrenceDict = cls.__dataStack[name]
        return Recurrence.fromData(data=recurrenceDict)

    
    @classmethod
    def saveData(cls):
        YAMLInteraction.dataToYAML(cls.YAML_FILE, cls.__dataStack)
    

    @classmethod
    def getData(cls):
        return cls.__dataStack


    @classmethod
    def setData(cls, data):
        cls.__dataStack = data
    