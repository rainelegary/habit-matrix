from abc import ABC, abstractmethod
import copy

from DataManagement.DataHelpers.yamlInteraction import (YAMLFiles,
                                                        YAMLInteraction)


class DataStack(ABC):
    dataStack = None

    @classmethod
    @abstractmethod
    def saveData(cls):
        raise NotImplementedError("method not yet implemented in subclass")


    
