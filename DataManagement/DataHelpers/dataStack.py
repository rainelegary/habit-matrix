from abc import ABC, abstractmethod

from DataManagement.DataHelpers.yamlInteraction import (YAMLFiles,
                                                        YAMLInteraction)



class DataStack(ABC):
    YAML_FILE = None
    __dataStack = None


    @classmethod
    @abstractmethod
    def saveData(cls):
        raise NotImplementedError("method not yet implemented in subclass")
    

    @classmethod
    @abstractmethod
    def getData(cls):
        raise NotImplementedError("method not yet implemented in subclass")


    @classmethod
    @abstractmethod
    def setData(cls, data):
        raise NotImplementedError("method not yet implemented in subclass")


    
