from abc import ABC, abstractmethod

class DictionaryEquivalent(ABC):
    @abstractmethod
    def toDict(self):
        pass


    @abstractmethod
    def fromDict(self):
        pass
