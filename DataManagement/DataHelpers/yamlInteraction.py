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
        WORKING_DIR = sys.argv[2]
    else:
        WORKING_DIR = ""
    
    HABITS = f"{WORKING_DIR}DataManagement/DataYAML/habits.yml"
    RECURRENCES = f"{WORKING_DIR}DataManagement/DataYAML/recurrences.yml"
    SESSION_INFO = f"{WORKING_DIR}DataManagement/DataYAML/sessionInfo.yml"
    IMAGES = f"{WORKING_DIR}DataManagement/DataYAML/images.yml"
    EXPERIMENTAL = f"{WORKING_DIR}DataManagement/DataYAML/experimental.yml"

    