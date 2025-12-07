from enum import Enum
from osu.curves import bezier_curve, circle_curve, linear_curve, centripetal_curve

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class NoteType(Enum):
    SIMPLE = 0
    COMBO = 1
    SPINNER = 2
    SLIDER = 3

class SliderType(Enum):
    BEZIER = 0
    CIRCLE = 1
    LINEAR = 2
    CENTRIPETAL = 3

class Note:
    def __init__(self, position: Position, startTime: int):
        position: Position = position
        startTime: int = startTime
    note_type: NoteType

class SimpleNote(Note):
    def __init__(self, position: Position, startTime: int):
        super().__init__(position, startTime)
    noteType = NoteType.SIMPLE
    hit: bool = False

class ComboNote(Note):
    def __init__(self, position: Position, startTime: int):
        super().__init__(position, startTime)
    noteType = NoteType.COMBO
    comboNumber: int

class SpinnerNote(Note):
    def __init__(self, position: Position, startTime: int):
        super().__init__(position, startTime)
    noteType = NoteType.SPINNER
    endTime: int
    started: bool = False
    finished: bool = False

class SliderNote(Note):
    def __init__(self, position: Position, startTime: int, curvePoints: list[Position], sliderType: SliderType):
        super().__init__(position, startTime)
        if sliderType == SliderType.BEZIER:
            self.control_points = bezier_curve(curvePoints)
        if sliderType == SliderType.CIRCLE:
            self.control_points = circle_curve(curvePoints)
        if sliderType == SliderType.LINEAR:
            self.control_points = linear_curve(curvePoints)
        if sliderType == SliderType.CENTRIPETAL:
            self.control_points = centripetal_curve(curvePoints)     
    noteType = NoteType.SLIDER
    length: float
    repeats: int
    started: bool = False
    finished: bool = False