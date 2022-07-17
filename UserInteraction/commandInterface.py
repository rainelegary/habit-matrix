from UserInteraction.commands import Command, CommandScope, CommandEnum, CommandScopeEnum
from UserInteraction.userInput import UserInput


class CommandInterface:
    @staticmethod
    def getInputOrCommand(prompt: str, commandScopeID: CommandScopeEnum, indent: int=0, userInputMethod=UserInput.indentedInput):
        commandScope = commandScopeID.value
        availableCommands = CommandInterface.getAvailableCommands(commandScope)
        userInput = userInputMethod(prompt, indent)
        commandArgs = userInput.strip().split()
        if len(commandArgs) == 0:
            return userInput
        for command in CommandEnum:
            if command.value.SHORTCUT == commandArgs[0] and command in availableCommands:
                return command.value.executeCommand(commandArgs, commandScopeID)
        return userInput


    @staticmethod
    def getAvailableCommands(commandScope: CommandScope):
        if commandScope.parent != None:
            commands = CommandInterface.getAvailableCommands(commandScope.parent)
        else:
            commands = []
        for w in commandScope.whitelist: 
            if w in commandScope.blacklist:
                raise Exception("whitelist overlaps with blacklist")
        
        for w in commandScope.whitelist:
            if w not in commands:
                commands.append(w)
        
        for b in commandScope.blacklist:
            if b in commands:
                commands.remove(b)

        commands = list(filter(lambda c: c in commands, CommandEnum))
        return commands

    
    @staticmethod
    def getAllowedScopes(command: Command):
        raise NotImplementedError("method not yet implemented")


