from abc import ABC, abstractmethod
import textwrap

from UserInteraction.userOutput import UserOutput

class TextEquivalent(ABC):
    @abstractmethod
    def toText(self, indent: int=0) -> str:
        pass

    
    @staticmethod
    def indentText(text: str, indent: int=0) -> str:
        return UserOutput.indentTextBlock(text, indent=indent)
        


