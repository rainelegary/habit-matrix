from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataStacks.dataStack import DataStack



class SessionInfoDataStack(DataStack):
    sessionInfo = YAMLInteraction.YAMLtoData(YAMLFiles.SESSION_INFO)
    if sessionInfo == None: sessionInfo = {}


    @classmethod
    def getSessionInfo(cls):
        return cls.sessionInfo


    @classmethod
    def setSessionInfo(cls, info):
        cls.sessionInfo = info
    
    