import yaml

class YAMLInteraction:
    @staticmethod
    def dictToYAML(fileName: str, dictionary: dict) -> None:
        with open(fileName, 'w') as file:
            yaml.dump(dictionary, file)


    @staticmethod
    def YAMLtoDict(fileName: str) -> dict:
        with open(fileName, "r") as file:
            try:
                dictionary = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
        return dictionary


class YAMLFiles:
    HABITS = "StoredData/habits.yml"
    