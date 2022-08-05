from UserInteraction.commands import Command, CommandScope, CommandEnum, CommandScopeEnum, InvalidCommandArgsException
from UserInteraction.userInput import UserInput
from UserInteraction.userOutput import UserOutput


class CommandInterface:
    @staticmethod
    def getCommand(prompt: str, commandScopeID: CommandScopeEnum, indent: int=0):
        commandScope = commandScopeID.value
        availableCommands = CommandInterface.getAvailableCommands(commandScope)
        userInput = UserInput.indentedInput(prompt, indent=indent)
        commandArgs = userInput.strip().split(UserInput.tabRegex)
        for command in CommandEnum:
            if command.value.SHORTCUT == commandArgs[0] and command in availableCommands:
                command.value.executeCommand(commandArgs, commandScopeID)
                return
        
        raise InvalidCommandArgsException("Not a recognized command.")
        


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


