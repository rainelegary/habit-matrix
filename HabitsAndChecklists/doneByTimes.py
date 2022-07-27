# from DataObjectConversion.textEquivalent import TextEquivalent
# from DataObjectConversion.dataEquivalent import DataEquivalent
# import datetime as dt
# from UserInteraction.userOutput import UserOutput


# class DoneByTimes(TextEquivalent, DataEquivalent):
#     def __init__(self, listOfTimes: list[dt.time]):
#         self.listOfTimes = listOfTimes
#         self.timeIntegers = sorted([t.hour for t in self.listOfTimes])


#     def toText(self, indent: int=0) -> str:
#         return f"{UserOutput.indentPadding(indent)}done by times: {self.timeIntegers}"

    
#     def toData(self) -> list[int]:
#         return self.timeIntegers

    
#     @staticmethod
#     def fromData(data: list[int]):
#         if data is None: return None
#         timeIntegers = data
#         listOfTimes = sorted([dt.time(hour=t) for t in timeIntegers])
#         return DoneByTimes(listOfTimes)