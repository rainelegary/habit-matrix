import yaml
import sys

class YAMLInteraction:
    @staticmethod
    def dictToYAML(fileName: str, dictionary: dict) -> None:
        with open(fileName, 'w') as file:
            yaml.dump(dictionary, stream=file, sort_keys=False)


    @staticmethod
    def YAMLtoDict(fileName: str) -> dict:
        with open(fileName, "r") as file:
            try:
                dictionary = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                sys.exit(exc)
        return dictionary


    @staticmethod
    def getDictAsYAMLText(dictionary: dict) -> None:
        return yaml.dump(dictionary, sort_keys=False)



class YAMLFiles:
    HABITS = "StoredData/habits.yml"
    RECURRENCES = "StoredData/recurrences.yml"
    