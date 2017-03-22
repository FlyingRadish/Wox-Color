from wox import Wox
import os
from PIL import Image


def clamp(min, max, x):
    if x > max:
        return max
    if x < min:
        return min
    return x


def createColorThumb(red, green, blue):
    red = clamp(0, 255, red)
    green = clamp(0, 255, green)
    blue = clamp(0, 255, blue)
    baseDir = getThumbDir()
    thumbPath = getColorThumbPath(red, green, blue)
    if not os.path.exists(baseDir):
        os.makedirs(baseDir)
    if not os.path.exists(thumbPath):
        with open(thumbPath, 'a'):
            img = Image.new('RGB', (100, 100), (red, green, blue))
            img.save(thumbPath)
    return thumbPath


def getColorThumbPath(red, green, blue):
    thumbPath = getThumbDir() + "\\" + hex((red << 16) + (green << 8) + blue) + ".png"
    return thumbPath


def getThumbDir():
    return os.getcwd() + "\colors"


def getErrorMessage():
    results = []
    results.append({
        "Title": "Invalid parameters",
        "SubTitle": "Please try again",
        "IcoPath": 'Images/app.png'
    })
    return results


class Color(Wox):
    def query(self, query):
        params = query.split(" ")
        color = "Query: {}".format(query)
        icon = "Images/app.png"
        if len(params) == 3 or len(params) == 4:
            try:
                color = 0
                for item in params:
                    color = color << 8
                    color += clamp(0, 255, int(item))
                color = "#{color:0{padding}x}".format(
                    color=color, padding=len(params) * 2)
                params.reverse()
                icon = createColorThumb(
                    int(params[2]), int(params[1]), int(params[0]))
                icon.replace(os.getcwd(), "")
            except Exception as e:
                return getErrorMessage()
        results = []
        results.append({
            "Title": color,
            "SubTitle": "Copy to clipboard",
            "IcoPath": icon,
            'JsonRPCAction': {
                'method': 'copy_colorHex',
                'parameters': [color],
                'dontHideAfterAction': False
            }
        })
        return results

    def copy_colorHex(self, color):
        command = 'echo ' + color.strip() + '| clip'
        os.system(command)


if __name__ == "__main__":
    Color()
