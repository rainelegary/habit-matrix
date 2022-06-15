from abc import ABC, abstractmethod

class TextEquivalent(ABC):
    @abstractmethod
    def toText(self):
        pass

