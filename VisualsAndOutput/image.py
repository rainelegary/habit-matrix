from DataManagement.DataHelpers.dataEquivalent import DataEquivalent



class Image(DataEquivalent):
    def __init__(self, name: str, letters: list[str], colors: list[str]):
        self.name = name
        self.letters = letters
        self.colors = colors
        self.width = len(letters[0])
        self.height = len(letters)
    

    def toData(self) -> dict:
        return {
            self.name: {
                "letters": self.letters,
                "colors": self.colors,
            }
        }

    
    @staticmethod
    def fromData(data: dict):
        name = list(data.keys())[0]
        details = data[name]
        letters = details["letters"]
        colors = details["colors"]
        return Image(name, letters, colors)
    
    