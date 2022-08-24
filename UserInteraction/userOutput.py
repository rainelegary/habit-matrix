
import textwrap


class UserOutput:
    indentStyle = ")> "

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
        

    
    @staticmethod
    def indentPadding(indent: int) -> str:
        return UserOutput.indentStyle * indent

    
    @staticmethod
    def indentTextBlock(text: str, indent: int=0) -> str:
        prefix = UserOutput.indentStyle * indent
        return textwrap.indent(text, prefix)

    
    @staticmethod
    def indentedPrint(output: str, indent: int=0):
        print(f"{UserOutput.indentPadding(indent)}{output}")


    @staticmethod
    def printWhitespace(lines: int=1):
        if lines >= 1:
            print("\n"*(lines - 1))

    



