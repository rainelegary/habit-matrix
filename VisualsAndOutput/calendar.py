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
            x = i * (emptyBoxImage.width - 1)
            calendarDisplay.addImage(voidBoxImage, x, headerImage.height - 1)


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

            calendarDisplay.addImage(modifiedBoxImage, x, y)
        

        

        
            

        







