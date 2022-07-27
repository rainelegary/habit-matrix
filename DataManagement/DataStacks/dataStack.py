import copy

from DataManagement.DataHelpers.yamlInteraction import (YAMLFiles,
                                                        YAMLInteraction)
from DataManagement.DataStacks.habitDataStack import HabitDataStack
from DataManagement.DataStacks.recurrenceDataStack import RecurrenceDataStack
from DataManagement.DataStacks.sessionInfoDataStack import SessionInfoDataStack


class DataStack:
    @classmethod
    def saveChanges(cls):
        YAMLInteraction.dataToYAML(YAMLFiles.HABITS, HabitDataStack.habits)
        YAMLInteraction.dataToYAML(YAMLFiles.RECURRENCES, RecurrenceDataStack.recurrences)
        YAMLInteraction.dataToYAML(YAMLFiles.SESSION_INFO, SessionInfoDataStack.sessionInfo)


    
