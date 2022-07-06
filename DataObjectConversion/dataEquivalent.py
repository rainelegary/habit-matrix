from abc import ABC, abstractmethod

class DataEquivalent(ABC):
    @abstractmethod
    def toData(self):
        raise NotImplementedError("method not yet implemented in subclass.")

    
    @staticmethod
    @abstractmethod
    def fromData():
        raise NotImplementedError("method not yet implemented in subclass.")

