import string
import re
from UserInteraction.commandInterface import CommandInterface
from UserInteraction.commands import CommandScopeEnum, CommandEnum
from UserInteraction.userOutput import UserOutput



class UserInput:
    commaRegex = r"[, ]*,[, ]*"
    doubleSpaceRegex = r"  +"
    commaOrSpaceRegex = r"[, ]+"



    @staticmethod
    def getInputOrCommand(prompt: str, commandScopeID: CommandScopeEnum, indent: int=0):
        commandScope = commandScopeID.value
        availableCommands = CommandInterface.getAvailableCommands(commandScope)
        userInput = UserInput.indentedInput(prompt, indent)
        commandArgs = userInput.strip().split()
        if len(commandArgs) == 0:
            return userInput
        for command in CommandEnum:
            if command.value.SHORTCUT == commandArgs[0] and command in availableCommands:
                return command.value.executeCommand(commandArgs, commandScopeID)
        return userInput

    

    @staticmethod
    def indentedInput(prompt: str, indent: int=0):
        return input(f"{UserOutput.indentPadding(indent)}{prompt}")


    @staticmethod
    def multiSelectString(prompt: str, options: list[str], commandScopeID: CommandScopeEnum, indent: int=0) -> list[str]:
        UserOutput.indentedPrint(output=prompt, indent=indent)
        print(UserInput.optionsString(options, indent=indent+1))
        optionsDict = UserInput.stringOptionsDict(options)
        choices = UserInput.getStringListInput(commandScopeID=commandScopeID, indent=indent)
        selected = UserInput.extractStringChoices(sorted(set(choice.lower() for choice in choices)), optionsDict)
        return selected


    @staticmethod
    def multiSelectInt(prompt: str, options: list[int], commandScopeID: CommandScopeEnum, indent: int=0) -> list[int]:
        UserOutput.indentedPrint(output=prompt, indent=indent)
        print(UserInput.optionsString(options, indent=indent+1))
        optionsDict = UserInput.intOptionsDict(options)
        choices = UserInput.getIntListInput(commandScopeID=commandScopeID, indent=indent)
        selected = UserInput.extractIntChoices(sorted(set(choice for choice in choices)), optionsDict)
        return selected


    @staticmethod
    def singleSelectString(prompt: str, options: list, commandScopeID: CommandScopeEnum, indent: int=0) -> str:
        optionsDict = UserInput.stringOptionsDict(options)
        prompting = True
        while prompting:
            UserOutput.indentedPrint(output=prompt, indent=indent)
            print(UserInput.optionsString(options, indent=indent+1))
            choice = UserInput.getStringInput(commandScopeID=commandScopeID, indent=indent)
            selected = UserInput.extractStringChoices([choice], optionsDict)
            if len(selected) > 0: 
                prompting = False
            else: 
                UserOutput.indentedPrint(output="invalid input, please try again.", indent=indent)
        return selected[0]


    def singleSelectInt(prompt: str, options: list[int], commandScopeID: CommandScopeEnum, indent: int=0) -> int:
        optionsDict = UserInput.intOptionsDict(options)
        prompting = True
        while prompting:
            UserOutput.indentedPrint(output=prompt, indent=indent)
            print(UserInput.optionsString(options, indent=indent+1))
            choice = UserInput.getIntInput(commandScopeID=commandScopeID, indent=indent)
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
    def getStringInput(commandScopeID: CommandScopeEnum, prompt: str="", indent: int=0) -> str:
        return CommandInterface.getInputOrCommand(prompt, commandScopeID=commandScopeID, indent=indent)

    
    @staticmethod
    def getIntInput(commandScopeID: CommandScopeEnum, prompt: str="", indent: int=0) -> int:
        prompting = True
        while prompting:
            choice = CommandInterface.getInputOrCommand(prompt, commandScopeID=commandScopeID, indent=indent)
            try:
                choice = int(choice)
                prompting = False
            except ValueError:
                UserOutput.indentedPrint(output="invalid integer, please try again.", indent=indent)
        return choice


    @staticmethod
    def getBoolInput(commandScopeID: CommandScopeEnum, prompt: str="", true: str="yes", false: str="no", indent: int=0) -> bool:
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
    def getStringListInput(commandScopeID: CommandScopeEnum, prompt: str="", indent: int=0) -> list[str]:
        userIn = CommandInterface.getInputOrCommand(prompt, commandScopeID=commandScopeID, indent=indent).strip()
        if "," in userIn: regExp = UserInput.commaRegex 
        else: regExp = UserInput.doubleSpaceRegex
        items = re.split(regExp, userIn)
        return items

    
    @staticmethod
    def getIntListInput(commandScopeID: CommandScopeEnum, prompt: str="", indent: int=0) -> list[int]:
        userIn = CommandInterface.getInputOrCommand(prompt, commandScopeID=commandScopeID, indent=indent).strip()
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
