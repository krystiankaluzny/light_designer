import numpy as np
import board
import neopixel
from renderer.renderer import Renderer


class NeoPixelRenderer(Renderer):

    def __init__(self):
        self.__pixelPin = board.D21
        self.__pixelCount = 500
        self.__pixelOrder = neopixel.GRB
        self.__pixels = neopixel.NeoPixel(self.__pixelPin, self.__pixelCount, brightness=0.2, auto_write=False, pixel_order=self.__pixelOrder)

    def __round(self, a):
        x = max(0.0, min(1.0, a))
        return int(255 if x == 1.0 else x * 256)

    def __scaleColor(self, color):
        return [self.__round(color[0]), self.__round(color[1]), self.__round(color[2])]

    def render(self, points: np.ndarray, colors: np.ndarray):

        for i in range(self.__pixelCount):
            self.__pixels[i] = self.__scaleColor(colors[i])

        self.__pixels.show()
