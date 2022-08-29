import copy
import datetime as dt
import calendar as cal
from DataManagement.DataStacks.imageDataStack import ImageDataStack
from VisualsAndOutput.image import Image

from DataManagement.DataStacks.sessionInfoDataStack import SessionInfoDataStack
from VisualsAndOutput.visualDisplay import VisualDisplay



class Calendar:
    @staticmethod
    def display(referenceDate: dt.date=dt.date.today()):
        calendarDisplay = VisualDisplay(150, 150)

        headerImage = ImageDataStack.getImage("header")
        Calendar.addFillerBoxes(calendarDisplay)
        Calendar.addDayBoxes(calendarDisplay, referenceDate)
        calendarDisplay.addImage(headerImage, 0, 0)

        calendarDisplay.display()

    
    @staticmethod
    def addFillerBoxes(calendarDisplay: VisualDisplay):
        headerImage = ImageDataStack.getImage("header")
        emptyBoxImage = ImageDataStack.getImage("empty box")

        l = emptyBoxImage.letters
        l = [i.replace("DD", "  ") for i in l]
        voidBoxImage = Image("void box", l, emptyBoxImage.colors)

        for i in range(7):
            xPos = i * (emptyBoxImage.width - 1)
            modifiedBoxImage = Calendar.overwriteBoxCorners(voidBoxImage, i, 0)
            calendarDisplay.addImage(modifiedBoxImage, xPos, headerImage.height - 1)


    @staticmethod
    def addDayBoxes(calendarDisplay: VisualDisplay, referenceDate: dt.date):
        DAYS_PER_WEEK = 7
        completedDays = SessionInfoDataStack.getCompletedDatesInMonth(referenceDate)
        year, month = referenceDate.year, referenceDate.month
        firstOfMonth = dt.date(year, month, 1)
        weekdayOfFirst = firstOfMonth.weekday()
        dayOffset = (weekdayOfFirst + 1) % DAYS_PER_WEEK
        daysInMonth = cal.monthrange(year, month)[1]

        headerImage = ImageDataStack.getImage("header")
        emptyBoxImage = ImageDataStack.getImage("empty box")
        checkedBoxImage = ImageDataStack.getImage("checked box")
        
        for day in range(1, daysInMonth + 1):
            dayStr = " " * (day < 10) + str(day)
            column = (day + dayOffset - 1) % DAYS_PER_WEEK
            row = (day + dayOffset - 1) // DAYS_PER_WEEK
            x = column * (emptyBoxImage.width - 1)
            y = (headerImage.height - 1) + row * (emptyBoxImage.height - 1)

            if day in completedDays:
                boxImage = checkedBoxImage
            else:
                boxImage = emptyBoxImage

            l = boxImage.letters
            l = [i.replace("DD", dayStr) for i in l]

            modifiedBoxImage = Image("modifed box image", l, boxImage.colors)
            modifiedBoxImage = Calendar.overwriteBoxCorners(modifiedBoxImage, column, row, day, daysInMonth)

            calendarDisplay.addImage(modifiedBoxImage, x, y)
    

    @staticmethod
    def overwriteBoxCorners(boxImage: Image, col, row, day=None, daysInMonth=None):
        charDict = {
            "": "\u256c",
            "tl": "\u2554",
            "t": "\u2566",
            "tr": "\u2557",
            "r": "\u2563",
            "br": "\u255d",
            "b": "\u2569",
            "bl": "\u255a",
            "l": "\u255f",
        }

        # z--y
        # |  |
        # x--w

        zt = (row == 0)
        zl = (col == 0)

        yt = (row == 0)
        yr = (col == 6)
        
        if (day == None or daysInMonth == None):
            xb = False
            xl = (col == 0)

            wb = False
            wr = (col == 6)
        else:
            DAYS_PER_WEEK = 7
            colOfLast = (col + daysInMonth - day) % DAYS_PER_WEEK
            rowOfLast = row + (col + daysInMonth - day) // DAYS_PER_WEEK

            xb = (col > colOfLast + 1 and row == rowOfLast - 1) or (row == rowOfLast)
            xl = (col == 0)
            
            wb = (col > colOfLast and row == rowOfLast - 1) or (row == rowOfLast)
            wr = (col == 6) or (row == rowOfLast and col == colOfLast)

        z = charDict["t" * zt + "l" * zl]
        y = charDict["t" * yt + "r" * yr]
        x = charDict["b" * xb + "l" * xl]
        w = charDict["b" * wb + "r" * wr]

        l = copy.deepcopy(boxImage.letters)
        width = len(l[0])
        height = len(l)
        l[0] = z + l[0][1:width - 1] + y
        l[height - 1] = x + l[height - 1][1:width -1 ] + w

        modifiedBoxImage = Image("modifed box image", l, boxImage.colors)

        return modifiedBoxImage