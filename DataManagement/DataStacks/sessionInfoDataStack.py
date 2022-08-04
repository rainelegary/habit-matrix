from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataHelpers.dataStack import DataStack



class SessionInfoDataStack(DataStack):
    YAML_FILE = YAMLFiles.SESSION_INFO
    __dataStack = YAMLInteraction.YAMLtoData(YAMLFiles.SESSION_INFO)
    if __dataStack == None: __dataStack = {}
    
    
    @classmethod
    def saveData(cls):
        YAMLInteraction.dataToYAML(cls.YAML_FILE, cls.__dataStack)
    

    @classmethod
    def getData(cls):
        return cls.__dataStack


    @classmethod
    def setData(cls, data):
        cls.__dataStack = data
    
    