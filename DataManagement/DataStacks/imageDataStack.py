


from DataManagement.DataHelpers.yamlInteraction import YAMLFiles, YAMLInteraction
from DataManagement.DataHelpers.dataStack import DataStack
from VisualsAndOutput.image import Image


class ImageDataStack(DataStack):
    YAML_FILE = YAMLFiles.IMAGES
    __dataStack = YAMLInteraction.YAMLtoData(YAML_FILE)
    if __dataStack == None: __dataStack = {}


    @classmethod
    def getImage(cls, name: str) -> Image:
        if name not in cls.__dataStack:
            raise KeyError("no image found with this name")
        
        imageDict = cls.__dataStack[name]
        return Image.fromData(data={name: imageDict})


    @classmethod
    def saveData(cls):
        YAMLInteraction.dataToYAML(cls.YAML_FILE, cls.__dataStack)
    

    @classmethod
    def getData(cls):
        return cls.__dataStack


    @classmethod
    def setData(cls, data):
        cls.__dataStack = data
