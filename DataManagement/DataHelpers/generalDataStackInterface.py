from enum import Enum
from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataObjects.sessionInfo import SessionInfo
from DataManagement.DataStackInterfaces.habitDataStackInterface import HabitDataStackInterface
from DataManagement.DataStackInterfaces.sessionInfoDataStackInterface import SessionInfoDataStackInterface

from DataManagement.DataStacks.habitDataStack import HabitDataStack
from DataManagement.DataStacks.recurrenceDataStack import RecurrenceDataStack
from DataManagement.DataStacks.sessionInfoDataStack import SessionInfoDataStack



class DataStackEnum(Enum):
    HABITS = HabitDataStack
    RECURRENCES = RecurrenceDataStack
    SESSION_INFO = SessionInfoDataStack



class GeneralDataStackInterface:
    @staticmethod
    def saveData():
        for dataStack in DataStackEnum:
            YAMLInteraction.dataToYAML(dataStack.value.YAML_FILE, dataStack.value.getData())

    
    @staticmethod
    def sessionStartupDataUpdates():
        # must happen before updating session info
        HabitDataStackInterface.timeElapsedUpdateAllQuotaStates()
        # must happen after updating quotas due to time elapsing
        SessionInfoDataStackInterface.updateSessionInfo()


    @staticmethod
    def sessionClosingDataUpdates():
        # must happen before updating session info
        HabitDataStackInterface.timeElapsedUpdateAllQuotaStates()
        # must happen after updating quotas due to time elapsing
        SessionInfoDataStackInterface.updateSessionInfo()
