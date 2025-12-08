from enum import Enum
from curves import bezier_curve, circle_curve, linear_curve, centripetal_curve
from utils import Position, scale_position

class NoteType(Enum):
    SIMPLE = 0
    SPINNER = 1
    SLIDER = 2

class SliderType(Enum):
    BEZIER = 0
    CIRCLE = 1
    LINEAR = 2
    CENTRIPETAL = 3

is_simple_note = 0b0001
is_slider = 0b0010
is_new_combo = 0b0100
is_spinner = 0b1000

class Note:
    def __init__(self, position: Position, startTime: int):
        self.position: Position = position
        self.startTime: int = startTime
    note_type: NoteType

    def get_position(self):
        newPosition = scale_position(self.position)
        return newPosition.x, newPosition.y
    
    def load_from_line(line: str):
        parts = line.split(',')

        if int(parts[3]) & is_simple_note:
            return SimpleNote.load_from_line(line)
        if int(parts[3]) & is_slider:
            return SliderNote.load_from_line(line)
        if int(parts[3]) & is_spinner:
            return SpinnerNote.load_from_line(line)
        

class SimpleNote(Note):
    def __init__(self, position: Position, startTime: int):
        super().__init__(position, startTime)
    noteType = NoteType.SIMPLE
    hit: bool = False
    def load_from_line(line):
        parts = line.split(',')
        x = int(parts[0])
        y = int(parts[1])
        startTime = int(parts[2])
        position = Position(x, y)
        return SimpleNote(position, startTime)

class SpinnerNote(Note):
    def __init__(self, position: Position, startTime: int):
        super().__init__(position, startTime)
    noteType = NoteType.SPINNER
    endTime: int
    started: bool = False
    finished: bool = False
    def load_from_line(line):
        parts = line.split(',')
        x = int(parts[0])
        y = int(parts[1])
        startTime = int(parts[2])
        position = Position(x, y)
        spinner = SpinnerNote(position, startTime)
        spinner.endTime = int(parts[5])
        return spinner

class SliderNote(Note):
    def __init__(self, position: Position, startTime: int, curvePoints: list[Position], sliderType: SliderType):
        super().__init__(position, startTime)
        if sliderType == SliderType.BEZIER:
            self.controlPoints = bezier_curve(curvePoints)
        if sliderType == SliderType.CIRCLE:
            self.controlPoints = circle_curve(curvePoints)
        if sliderType == SliderType.LINEAR:
            self.controlPoints = linear_curve(curvePoints)
        if sliderType == SliderType.CENTRIPETAL:
            self.controlPoints = centripetal_curve(curvePoints)     
    noteType = NoteType.SLIDER
    length: float
    repeats: int
    started: bool = False
    finished: bool = False
    def load_from_line(line):
        parts = line.split(',')
        x = int(parts[0])
        y = int(parts[1])
        startTime = int(parts[2])
        position = Position(x, y)

        curveData = parts[5].split('|')
        if curveData[0] == 'B':
            sliderType = SliderType.BEZIER
        if curveData[0] == 'C':
            sliderType = SliderType.CENTRIPETAL
        if curveData[0] == 'L':
            sliderType = SliderType.LINEAR
        if curveData[0] == 'P':
            sliderType = SliderType.CIRCLE

        curvePoints = []
        curvePoints.append(Position(x, y))
        for i in range(1, len(curveData)):
            pointParts = curveData[i].split(':')
            pointX = int(pointParts[0])
            pointY = int(pointParts[1])
            curvePoints.append(Position(pointX, pointY))

        slider = SliderNote(position, startTime, curvePoints, sliderType)
        slider.repeats = int(parts[6])
        slider.length = float(parts[7])        
        return slider