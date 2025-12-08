import pyautogui

SYSTEM_WIDTH, SYSTEM_HEIGHT = pyautogui.size()
OSU_WIDTH, OSU_HEIGHT = 640, 480

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def scale_position(position: Position):
    xScale = SYSTEM_WIDTH / OSU_WIDTH
    yScale = SYSTEM_HEIGHT / OSU_HEIGHT

    xOut = position.x * xScale
    yOut = position.y * yScale

    newPosition = Position(xOut, yOut)
    return newPosition