import string
import re
import datetime as dt
from DateAndTime.calendarObjects import CalendarObjects
from VisualsAndOutput.color import ColorEnum
from VisualsAndOutput.userOutput import UserOutput



class CancelInputException(Exception):
        def __init__(self, message: str):
            self.message = message


class UserInput:
    commaRegex = r"[, ]*,[, ]*"
    doubleSpaceRegex = r"  +"
    singleSpaceRegex = r" +"
    commaOrSpaceRegex = r"[, ]+"
    tabRegex = "\t"
    

    @staticmethod
    def indentedInput(prompt: str, indent: int=0):

        defaultCode = ColorEnum.DEFAULT.value.code
        blueCode = ColorEnum.BLUE.value.code

        userIn = input(f"{UserOutput.indentPadding(indent)}{prompt}")
        if userIn == "cancel":
            raise CancelInputException("input cancelled")
        return userIn


    @staticmethod
    def multiSelectString(prompt: str, options: list[str], indent: int=0) -> list[str]:
        UserOutput.indentedPrint(output=prompt, indent=indent)
        print(UserInputHelper.optionsString(options, indent=indent+1))
        optionsDict = UserInputHelper.stringOptionsDict(options)
        choices = UserInput.getStringListInput(indent=indent)
        selected = UserInputHelper.extractStringChoices(sorted(set(choice.lower() for choice in choices)), optionsDict)
        return selected


    @staticmethod
    def multiSelectInt(prompt: str, options: list[int], indent: int=0) -> list[int]:
        UserOutput.indentedPrint(output=prompt, indent=indent)
        print(UserInputHelper.optionsString(options, indent=indent+1))
        optionsDict = UserInputHelper.intOptionsDict(options)
        choices = UserInput.getIntListInput(indent=indent)
        selected = UserInputHelper.extractIntChoices(sorted(set(choice for choice in choices)), optionsDict)
        return selected


    @staticmethod
    def singleSelectString(prompt: str, options: list, indent: int=0) -> str:
        optionsDict = UserInputHelper.stringOptionsDict(options)
        prompting = True
        while prompting:
            UserOutput.indentedPrint(output=prompt, indent=indent)
            print(UserInputHelper.optionsString(options, indent=indent+1))
            choice = UserInput.getStringInput(indent=indent)
            selected = UserInputHelper.extractStringChoices([choice], optionsDict)
            if len(selected) > 0: 
                prompting = False
            else: 
                UserOutput.indentedPrint(output="invalid input, please try again.", indent=indent)
        return selected[0]


    def singleSelectInt(prompt: str, options: list[int], indent: int=0) -> int:
        optionsDict = UserInputHelper.intOptionsDict(options)
        prompting = True
        while prompting:
            UserOutput.indentedPrint(output=prompt, indent=indent)
            print(UserInputHelper.optionsString(options, indent=indent+1))
            choice = UserInput.getIntInput(indent=indent)
            selected = UserInputHelper.extractIntChoices([choice], optionsDict)
            if len(selected) > 0: 
                prompting = False
            else: 
                UserOutput.indentedPrint(output="invalid input, please try again.", indent=indent)
        return selected[0]

    
    @staticmethod
    def getStringInput(prompt: str="", indent: int=0) -> str:
        return UserInput.indentedInput(prompt, indent=indent)

    
    @staticmethod
    def getIntInput(prompt: str="", minimum: int=None, maximum: int=None, indent: int=0) -> int:
        if minimum == None:
            minString = "negative infinity"
        else:
            minString = str(minimum)

        if maximum == None:
            maxString = "positive infinity"
        else:
            maxString = str(maximum)


        prompting = True
        while prompting:
            choice = UserInput.indentedInput(prompt, indent=indent)
            try:
                choice = int(choice)
                if (minimum != None and choice < minimum) or (maximum != None and choice > maximum):
                    raise ValueError
                prompting = False
            except ValueError:
                UserOutput.indentedPrint(output=f"please enter an integer between {minString} and {maxString}", indent=indent)
        return choice


    @staticmethod
    def getBoolInput(prompt: str="", true: str="yes", false: str="no", indent: int=0) -> bool:
        answerDict = {true: True, false: False}
        prompting = True
        while prompting:
            choice = UserInput.singleSelectString(prompt, [true, false], indent=indent)
            try:
                choice = answerDict[choice]
                prompting = False
            except KeyError:
                UserOutput.indentedPrint(output="invalid answer, please try again.", indent=indent)
        return choice

    
    @staticmethod
    def getTimeInput(prompt: str="", indent: int=0) -> dt.time:
        prompting = True
        while prompting:
            choice = UserInput.indentedInput(prompt, indent=indent)
            try:
                choice = dt.datetime.strptime(choice, CalendarObjects.TIME_STR_TEXT_INPUT_FORMAT).time()
                prompting = False
            except ValueError:
                UserOutput.indentedPrint(
                    output=f"please enter times in the format {CalendarObjects.TIME_STR_TEXT_INPUT_FORMAT_EXAMPLE}", 
                    indent=indent)
        return choice

    
    @staticmethod
    def getDateInput(prompt: str="", indent: int=0) -> dt.date:
        prompting = True
        while prompting:
            choice = UserInput.indentedInput(prompt, indent=indent)
            try:
                choice = dt.datetime.strptime(choice, CalendarObjects.DATE_STR_TEXT_INPUT_FORMAT).date()
                prompting = False
            except ValueError:
                UserOutput.indentedPrint(
                    output=f"please enter dates in the format {CalendarObjects.DATE_STR_TEXT_INPUT_FORMAT_EXAMPLE}", 
                    indent=indent)
        return choice


    @staticmethod
    def getStringListInput(prompt: str="", indent: int=0) -> list[str]:
        userIn = UserInput.indentedInput(prompt, indent=indent).strip()
        if "," in userIn: regExp = UserInput.commaRegex 
        elif "  " in userIn: regExp = UserInput.doubleSpaceRegex
        else: regExp = UserInput.singleSpaceRegex
        items = re.split(regExp, userIn)
        return items

    
    @staticmethod
    def getIntListInput(prompt: str="", minimum: int=None, maximum: int=None, indent: int=0) -> list[int]:
        userIn = UserInput.indentedInput(prompt, indent=indent).strip()
        regExp = UserInput.commaOrSpaceRegex
        items = re.split(regExp, userIn)
        itemsWithNum = list(filter(lambda item: item.isdecimal(), items))
        itemsAsNum = list(map(int, itemsWithNum))


        if minimum == None:
            minString = "negative infinity"
        else:
            minString = str(minimum)

        if maximum == None:
            maxString = "positive infinity"
        else:
            maxString = str(maximum)

        for item in itemsAsNum:
            if (minimum != None and item < minimum) or (maximum != None and item > maximum):
                itemsAsNum.remove(item)
                UserOutput.indentedPrint(f"an integer has been removed as it is not between {minString} and {maxString}", indent=indent)
        return itemsAsNum

    

class UserInputHelper:
    @staticmethod
    def optionsString(options: list, indent: int=0) -> str:
        optionsDict = UserInputHelper.stringOptionsDict(options)
        menu = ""
        for option in optionsDict:
            menu += f"{UserOutput.indentPadding(indent)}{option}. {optionsDict[option]}\n"
        return menu.rstrip("\n")
    

    @staticmethod
    def stringOptionsDict(options: list[str]) -> dict[str, str]:
        optionsDict = {}
        letters = string.ascii_lowercase
        for optionN in range(len(options)):
            optionsDict[letters[optionN]] = options[optionN].lower()
        return optionsDict

    
    @staticmethod
    def intOptionsDict(options: list[int]) -> dict[str, int]:
        optionsDict = {}
        letters = string.ascii_lowercase
        for optionN in range(len(options)):
            optionsDict[letters[optionN]] = options[optionN]
        return optionsDict


    @staticmethod
    def extractStringChoices(choices: list[str], optionsDict: dict[str, str]) -> list[str]:
        selected = []
        lowerKeys = list(map(lambda x: x.lower(), optionsDict.keys()))
        lowerVals = list(map(lambda x: x.lower(), optionsDict.values()))
        for item in choices:
            if item in lowerKeys: selected.append(optionsDict[item])
            if item in lowerVals: selected.append(item)
        return selected


    @staticmethod
    def extractIntChoices(choices: list[str], optionsDict: dict[str, int]) -> list[int]:
        selected = []
        for item in choices:
            if item in optionsDict.keys():
                selected.append(optionsDict[item])
            if item in optionsDict.values():
                selected.append(item)
        return selected


