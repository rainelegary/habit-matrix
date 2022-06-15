from DataObjectConversion.yamlInteraction import YAMLInteraction

def main():
    dictionary = YAMLInteraction.YAMLtoDict("StoredData/habits.yml")
    YAMLInteraction.dictToYAML("StoredData/yamlDump.yml", dictionary)



if __name__ == "__main__":
    main()