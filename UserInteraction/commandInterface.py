from UserInteraction.commands import Command, CommandEnum, InvalidCommandArgsException
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput


class CommandInterface:
    @staticmethod
    def getCommand(prompt: str, indent: int=0):
        userInput = UserInput.indentedInput(prompt, indent=indent)
        UserOutput.printWhitespace(2)
        unparsedCommandArgs = userInput.strip().split(UserInput.tabRegex)
        for command in CommandEnum:
            if command.value.SHORTCUT == unparsedCommandArgs[0]:
                commandArgs = CommandInterface.parseCommandArgs(unparsedCommandArgs)
                command.value.executeCommand(commandArgs, indent=indent)
                return
        
        raise InvalidCommandArgsException("Not a recognized command. Use the 'help' command to see a list of commands.", None)


    @staticmethod
    def parseCommandArgs(unparsedCommandArgs):
        unp = unparsedCommandArgs
        for command in CommandEnum:
            if command.value.SHORTCUT == unp[0]:
                cm = command.value
                comd = command
        
        parsed = {}
        ob = cm.OBLIGATE_ARGS
        kw = cm.KEYWORD_ARGS

        if len(unp) < len(ob) + 1:
            raise InvalidCommandArgsException("please supply all obligate arguments.", comd)

        for i in range(len(ob)):
            for kwarg in kw:
                if unp[i + 1].startswith(f"{kwarg}="):
                    raise InvalidCommandArgsException("Please place all keyword arguments after all obligate arguments.", comd)
            parsed[ob[i]] = unp[i + 1]
        
        kwargDefaults = cm.keywordArgDefaults()
        for kwarg in kw:
            parsed[kwarg] = kwargDefaults[kwarg]
            for i in range(len(ob) + 1, len(unp)):
                if unp[i].startswith(f"{kwarg}="):
                    parsed[kwarg] = unp[i].replace(f"{kwarg}=", "")
        
        return parsed



