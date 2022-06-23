import string
import re

class UserIO:
    @staticmethod
    def multiSelectString(prompt: str, options: list[str]) -> list[str]:
        print(prompt)
        print(UserIO.optionsString(options))
        optionsDict = UserIO.stringOptionsDict(options)
        choices = UserIO.getStringListInput()
        selected = UserIO.extractStringChoices(list(set(choice.lower() for choice in choices)), optionsDict)
        return selected


    @staticmethod
    def multiSelectInt(prompt: str, options: list[int]) -> list[int]:
        print(prompt)
        print(UserIO.optionsString(options))
        optionsDict = UserIO.intOptionsDict(options)
        choices = UserIO.getIntListInput()
        selected = UserIO.extractIntChoices(list(set(choice for choice in choices)), optionsDict)
        return selected


    @staticmethod
    def singleSelectString(prompt: str, options: list) -> str:
        optionsDict = UserIO.stringOptionsDict(options)
        prompting = True
        while prompting:
            print(prompt)
            print(UserIO.optionsString(options))
            choice = UserIO.getStringInput()
            selected = UserIO.extractStringChoices([choice], optionsDict)
            if len(selected) > 0: prompting = False
            else: print("invalid input, please try again.")
        return selected[0]


    def singleSelectInt(prompt: str, options: list[int]) -> int:
        optionsDict = UserIO.intOptionsDict(options)
        prompting = True
        while prompting:
            print(prompt)
            print(UserIO.optionsString(options))
            choice = UserIO.getIntInput()
            selected = UserIO.extractIntChoices([choice], optionsDict)
            if len(selected) > 0: prompting = False
            else: print("invalid input, please try again.")
        return selected[0]

    
    @staticmethod
    def optionsString(options: list) -> str:
        optionsDict = UserIO.stringOptionsDict(options)
        menu = ""
        for option in optionsDict:
            menu += f"{option}. {optionsDict[option]}\n"
        return menu.strip()

    
    @staticmethod
    def getStringInput(prompt: str="") -> str:
        return input(prompt)

    
    @staticmethod
    def getIntInput(prompt: str="") -> int:
        prompting = True
        while prompting:
            choice = input(prompt)
            try:
                choice = int(choice)
                prompting = False
            except ValueError:
                print("invalid integer, please try again.")
        return choice


    @staticmethod
    def getBoolInput(prompt: str="", true="yes", false="no") -> bool:
        answerDict = {true: True, false: False}
        prompting = True
        while prompting:
            choice = UserIO.singleSelectString(prompt, [true, false])
            try:
                choice = answerDict[choice]
                prompting = False
            except KeyError:
                print("invalid answer, please try again.")
        return choice


    @staticmethod
    def getStringListInput(prompt: str="") -> list[str]:
        userIn = input(prompt).strip()
        # regex represents:
        # - any amount of commas and spaces (at least one of either)
        regExp = "[, ]+" 
        items = re.split(regExp, userIn)
        return items

    
    @staticmethod
    def getIntListInput(prompt: str="") -> list[int]:
        userIn = input(prompt).strip()
        # regex represents:
        # - any amount of commas and spaces (at least one of either)
        regExp = "[, ]+"
        items = re.split(regExp, userIn)
        return items

    
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
        for item in choices:
            if item in optionsDict.keys():
                selected.append(optionsDict[item])
            if item in optionsDict.values():
                selected.append(item)
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
