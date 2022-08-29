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
    args = sys.argv
    if len(args) >= 3:
        YAML_DIR = sys.argv[2]
    else:
        YAML_DIR = ""
    
    HABITS = f"{YAML_DIR}habits.yml"
    RECURRENCES = f"{YAML_DIR}recurrences.yml"
    SESSION_INFO = f"{YAML_DIR}sessionInfo.yml"
    IMAGES = f"{YAML_DIR}images.yml"
    EXPERIMENTAL = f"{YAML_DIR}experimental.yml"

    