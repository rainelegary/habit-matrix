from DataObjectConversion.yamlInteraction import YAMLInteraction, YAMLFiles


class DataStack:
    habits = YAMLInteraction.YAMLtoData(YAMLFiles.HABITS)
    recurrences = YAMLInteraction.YAMLtoData(YAMLFiles.RECURRENCES)
    if habits == None: habits = {}
    if recurrences == None: recurrences = {}


    @classmethod
    def saveChanges(cls):
        YAMLInteraction.dataToYAML(YAMLFiles.HABITS, cls.habits)
        YAMLInteraction.dataToYAML(YAMLFiles.RECURRENCES, cls.recurrences)


    @classmethod
    def addHabit(cls, habit, name):
        cls.habits[name] = habit


    @classmethod
    def removeHabit(cls, name):
        del cls.habits[name]


    @classmethod
    def addRecurrence(cls, recurrence, name):
        cls.recurrences[name] = recurrence


    @classmethod
    def removeRecurrence(cls, name):
        del cls.recurrences[name]