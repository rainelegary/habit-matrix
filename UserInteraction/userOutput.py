
class UserOutput:
    @staticmethod
    def numberSuffix(num: int) -> str:
        num = abs(num)
        lastDigit = num % 10
        secondLastDigit = (num % 100) - lastDigit
        if secondLastDigit == 1: return "th"
        suffixDict = {1: "st", 2: "nd", 3: "rd"}
        if lastDigit in suffixDict: return suffixDict[lastDigit]
        else: return "th"


