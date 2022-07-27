from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataStacks.dataStack import DataStack
from HabitsAndChecklists.recurrence import Recurrence



class RecurrenceDataStack(DataStack):
    recurrences = YAMLInteraction.YAMLtoData(YAMLFiles.RECURRENCES)
    if recurrences == None: recurrences = {}

    
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
    