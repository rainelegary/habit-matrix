from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataHelpers.dataStack import DataStack
from HabitsAndChecklists.recurrence import Recurrence



class RecurrenceDataStack(DataStack):
    dataStack = YAMLInteraction.YAMLtoData(YAMLFiles.RECURRENCES)
    if dataStack == None: dataStack = {}
    yamlFile = YAMLFiles.RECURRENCES


    @classmethod
    def addRecurrence(cls, recurrence: Recurrence, name: str):
        cls.dataStack[name] = recurrence.toData()


    @classmethod
    def removeRecurrence(cls, name: str):
        del cls.dataStack[name]


    @classmethod
    def getRecurrence(cls, name: str) -> Recurrence:
        if name not in cls.dataStack:
            raise Exception("recurrence not found")
        recurrenceDict = cls.dataStack[name]
        return Recurrence.fromData(data=recurrenceDict)
    