import textwrap

from VisualsAndOutput.color import ANSIEscapeSequenceEnum, ColorEnum


class UserOutput:
    indentStyle = ")> "
    currentTextColor = ColorEnum.DEFAULT
    currentIndentColor = ColorEnum.DEFAULT
    currentBoldText = False


    @classmethod
    def indentPadding(cls, indent: int, indentColor: ColorEnum=None) -> str:
        indentColorCode = cls.currentIndentColor.value.code
        if indentColor != None:
            indentColorCode = indentColor.value.code
        return indentColorCode + UserOutput.indentStyle * indent + cls.currentTextColor.value.code

    
    @staticmethod
    def indentTextBlock(text: str, indent: int=0) -> str:
        prefix = UserOutput.indentStyle * indent
        return textwrap.indent(text, prefix)

    
    @classmethod
    def indentedPrint(cls, output: str, indent: int=0, textColor: ColorEnum=None, 
    indentColor: ColorEnum=None, bold: bool=None):
        textColorCode = cls.currentTextColor.value.code
        indentColorCode = cls.currentIndentColor.value.code

        if textColor != None:
            textColorCode = textColor.value.code
        if indentColor != None:
            indentColorCode = indentColor.value.code

        if bold == None:
            bold = cls.currentBoldText
        
        boldCode = ANSIEscapeSequenceEnum.BOLD.value.code * bold
        resetCode = ANSIEscapeSequenceEnum.RESET.value.code

        ind = UserOutput.indentPadding(indent)

        print(f"{boldCode}{indentColorCode}{ind}{textColorCode}{output}{resetCode}")


    @staticmethod
    def printWhitespace(lines: int=1):
        if lines >= 1:
            print("\n"*(lines - 1))


    @staticmethod
    def numberSuffix(num: int) -> str:
        num = abs(num)
        lastDigit = num % 10
        secondLastDigit = (num % 100) - lastDigit
        if secondLastDigit == 1: 
            return "th"
        suffixDict = {1: "st", 2: "nd", 3: "rd"}
        if lastDigit in suffixDict: 
            return suffixDict[lastDigit]
        else: 
            return "th"


    @staticmethod
    def sIfPlural(num: int=1) -> str:
        s = ""
        if num != 1:
            s = "s"
        
        return s

