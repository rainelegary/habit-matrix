from enum import Enum
from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction

from DataManagement.DataStacks.habitDataStack import HabitDataStack
from DataManagement.DataStacks.recurrenceDataStack import RecurrenceDataStack
from DataManagement.DataStacks.sessionInfoDataStack import SessionInfoDataStack



class DataStackEnum(Enum):
    HABITS = HabitDataStack
    RECURRENCES = RecurrenceDataStack
    SESSION_INFO = SessionInfoDataStack



class DataStackActivator:
    @staticmethod
    def saveData():
        for dataStack in DataStackEnum:
            YAMLInteraction.dataToYAML(dataStack.value.yamlFile, dataStack.value.dataStack)

    
    

