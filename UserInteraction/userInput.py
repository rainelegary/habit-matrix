import string
import re
from UserInteraction.userOutput import UserOutput
from UserInteraction.inputCancel import CancelInputException



class UserInput:
    commaRegex = r"[, ]*,[, ]*"
    doubleSpaceRegex = r"  +"
    commaOrSpaceRegex = r"[, ]+"
    

    @staticmethod
    def indentedInput(prompt: str, indent: int=0):
        userIn = input(f"{UserOutput.indentPadding(indent)}{prompt}")
        if userIn == "cancel":
            raise CancelInputException("inpiut cancelled")
        return userIn


    @staticmethod
    def multiSelectString(prompt: str, options: list[str], indent: int=0) -> list[str]:
        UserOutput.indentedPrint(output=prompt, indent=indent)
        print(UserInput.optionsString(options, indent=indent+1))
        optionsDict = UserInput.stringOptionsDict(options)
        choices = UserInput.getStringListInput(indent=indent)
        selected = UserInput.extractStringChoices(sorted(set(choice.lower() for choice in choices)), optionsDict)
        return selected


    @staticmethod
    def multiSelectInt(prompt: str, options: list[int], indent: int=0) -> list[int]:
        UserOutput.indentedPrint(output=prompt, indent=indent)
        print(UserInput.optionsString(options, indent=indent+1))
        optionsDict = UserInput.intOptionsDict(options)
        choices = UserInput.getIntListInput(indent=indent)
        selected = UserInput.extractIntChoices(sorted(set(choice for choice in choices)), optionsDict)
        return selected


    @staticmethod
    def singleSelectString(prompt: str, options: list, indent: int=0) -> str:
        optionsDict = UserInput.stringOptionsDict(options)
        prompting = True
        while prompting:
            UserOutput.indentedPrint(output=prompt, indent=indent)
            print(UserInput.optionsString(options, indent=indent+1))
            choice = UserInput.getStringInput(indent=indent)
            selected = UserInput.extractStringChoices([choice], optionsDict)
            if len(selected) > 0: 
                prompting = False
            else: 
                UserOutput.indentedPrint(output="invalid input, please try again.", indent=indent)
        return selected[0]


    def singleSelectInt(prompt: str, options: list[int], indent: int=0) -> int:
        optionsDict = UserInput.intOptionsDict(options)
        prompting = True
        while prompting:
            UserOutput.indentedPrint(output=prompt, indent=indent)
            print(UserInput.optionsString(options, indent=indent+1))
            choice = UserInput.getIntInput(indent=indent)
            selected = UserInput.extractIntChoices([choice], optionsDict)
            if len(selected) > 0: 
                prompting = False
            else: 
                UserOutput.indentedPrint(output="invalid input, please try again.", indent=indent)
        return selected[0]

    
    @staticmethod
    def optionsString(options: list, indent: int=0) -> str:
        optionsDict = UserInput.stringOptionsDict(options)
        menu = ""
        for option in optionsDict:
            menu += f"{UserOutput.indentPadding(indent)}{option}. {optionsDict[option]}\n"
        return menu.rstrip("\n")

    
    @staticmethod
    def getStringInput(prompt: str="", indent: int=0) -> str:
        return UserInput.indentedInput(prompt, indent=indent)

    
    @staticmethod
    def getIntInput(prompt: str="", indent: int=0) -> int:
        prompting = True
        while prompting:
            choice = UserInput.indentedInput(prompt, indent=indent)
            try:
                choice = int(choice)
                prompting = False
            except ValueError:
                UserOutput.indentedPrint(output="invalid integer, please try again.", indent=indent)
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
    def getStringListInput(prompt: str="", indent: int=0) -> list[str]:
        userIn = UserInput.indentedInput(prompt, indent=indent).strip()
        if "," in userIn: regExp = UserInput.commaRegex 
        else: regExp = UserInput.doubleSpaceRegex
        items = re.split(regExp, userIn)
        return items

    
    @staticmethod
    def getIntListInput(prompt: str="", indent: int=0) -> list[int]:
        userIn = UserInput.indentedInput(prompt, indent=indent).strip()
        regExp = UserInput.commaOrSpaceRegex
        items = re.split(regExp, userIn)
        itemsWithNum = list(filter(lambda item: item.isdecimal(), items))
        itemsAsNum = list(map(int, itemsWithNum))
        return itemsAsNum

    
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
