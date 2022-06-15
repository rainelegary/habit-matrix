import yaml

class YAMLInteraction:
    @staticmethod
    def dictToYAML(fileName: str, dictionary: dict) -> None:
        with open(fileName, 'w') as file:
            yaml.dump(dictionary, file)


    @staticmethod
    def YAMLtoDict(fileName: str) -> dict:
        with open(fileName, "r") as stream:
            try:
                dictionary = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return dictionary