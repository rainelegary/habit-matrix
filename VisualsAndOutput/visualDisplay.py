from VisualsAndOutput.color import ColorEnum
from VisualsAndOutput.image import Image
from VisualsAndOutput.userOutput import UserOutput



class VisualDisplay:
    def __init__(self, maxWidth: int, maxHeight: int):
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self.letters = [" " * maxWidth] * maxHeight
        self.colors = ["d" * maxWidth] * maxHeight
        self.width = 0
        self.height = 0
        self.horizontalBuffer = 0
        self.verticalBuffer = 0


    def addImage(self, image: Image, x: int, y: int):
        xp = x + image.width
        yp = y + image.height

        horizontalOutcrop = max(-x, xp - self.maxWidth)
        verticalOutcrop = max(-y, yp - self.maxHeight)
        horizontalBuffer = max(self.horizontalBuffer, horizontalOutcrop)
        verticalBuffer = max(self.verticalBuffer, verticalOutcrop)
        horizontalAdditionLetters = " " * (horizontalBuffer - self.horizontalBuffer)
        verticalAdditionLetters = [" " * (self.maxWidth + 2 * horizontalBuffer)] * (verticalBuffer - self.verticalBuffer)
        horizontalAdditionColors = "d" * (horizontalBuffer - self.horizontalBuffer)
        verticalAdditionColors = ["d" * (self.maxWidth + 2 * horizontalBuffer)] * (verticalBuffer - self.verticalBuffer)

        widthRequirement = max(self.width, xp)
        heightRequirement = max(self.height, yp)
        width = min(self.maxWidth, widthRequirement)
        height = min(self.maxHeight, heightRequirement)

        l = self.letters
        c = self.colors

        hal = horizontalAdditionLetters
        val = verticalAdditionLetters
        hac = horizontalAdditionColors
        vac = verticalAdditionColors

        l = [hal + row + hal for row in l]
        l = val + l + val

        c = [hac + row + hac for row in c]
        c = vac + c + vac

        hb = horizontalBuffer
        vb = verticalBuffer

        l = l[:y + vb] + [l[y + vb + i][:x + hb] + image.letters[i] + l[y + vb + i][xp + hb:] for i in range(len(image.letters))] + l[yp + vb:]
        c = c[:y + vb] + [c[y + vb + i][:x + hb] + image.colors[i] + c[y + vb + i][xp + hb:] for i in range(len(image.colors))] + c[yp + vb:]

        self.letters = l
        self.colors = c
        self.width = width
        self.height = height
        self.horizontalBuffer = hb
        self.verticalBuffer = vb


    def display(self):
        l = self.letters
        c = self.colors

        w = self.width
        h = self.height

        hb = self.horizontalBuffer
        vb = self.verticalBuffer

        l = l[vb:vb + h]
        l = [row[hb:hb + w] for row in l]
        c = c[vb:vb + h]
        c = [row[hb:hb + w] for row in c]

        c = [[j + "~" for j in i] for i in c]

        for color in ColorEnum:
            colorLetter = color.value.letter
            colorCode = color.value.code
            c = [[col.replace(colorLetter + "~", colorCode) for col in row] for row in c]

        display = ["".join(c[i][j] + l[i][j] for j in range(w)) for i in range(h)]
        for line in display:
            UserOutput.indentedPrint(line)

        # UserOutput.indentedPrint(display[3])