from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataHelpers.dataStack import DataStack



class SessionInfoDataStack(DataStack):
    dataStack = YAMLInteraction.YAMLtoData(YAMLFiles.SESSION_INFO)
    if dataStack == None: dataStack = {}
    yamlFile = YAMLFiles.SESSION_INFO


    @classmethod
    def getSessionInfo(cls):
        return cls.dataStack


    @classmethod
    def setSessionInfo(cls, info):
        cls.dataStack = info
    
    