import yaml
import sys



class YAMLInteraction:
    @staticmethod
    def dataToYAML(fileName: str, data) -> None:
        with open(fileName, 'w') as file:
            yaml.dump(data, stream=file, sort_keys=False)


    @staticmethod
    def YAMLtoData(fileName: str) -> dict:
        with open(fileName, "r") as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                sys.exit(exc)
        return data


    @staticmethod
    def getDataAsYAMLText(data) -> None:
        return yaml.dump(data, sort_keys=False)



class YAMLFiles:
    HABITS = "StoredData/habits.yml"
    RECURRENCES = "StoredData/recurrences.yml"
    SESSION_INFO = "StoredData/sessionInfo.yml"
    