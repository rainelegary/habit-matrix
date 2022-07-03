from UserInteraction.commands import Command, CommandScope, CommandEnum, CommandScopeEnum


class CommandInterface:
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


