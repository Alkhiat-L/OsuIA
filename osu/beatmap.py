from objects.Notes import Note, SimpleNote, SliderNote, SpinnerNote
from enum import Enum
import pyautogui
from utils import scale_position
import pygetwindow

beatmapFile = 'osu\\maps\\Raphlesia & BilliumMoto - My Love (Mao) [Easy].osu'

class Modifier(Enum):
    EASY = 1
    NO_FAIL = 2
    HALF_TIME = 3
    HARD_ROCK = 4
    SUDDEN_DEATH = 5
    PERFECT = 6
    DOUBLE_TIME = 7
    NIGHTCORE = 8
    HIDDEN = 9
    FADE_IN = 10
    FLASHLIGHT = 11
    RELAX = 12
    AUTOPILOT = 13
    SPUN_OUT = 14

class TimingPoint:
    time: int
    beatLength: float
    meter: int
    uninherited: bool

    def load_from_line(line: str):
        parts = line.split(',')
        tp = TimingPoint()
        tp.time = int(parts[0])
        tp.beatLength = float(parts[1])
        tp.meter = int(parts[2])
        tp.uninherited = parts[6] == '1'
        return tp

class Beatmap:
    circleSize: float
    overallDifficulty: float
    approachRate: float
    sliderMultiplier: float
    sliderTickRate: float
    timingPoints: list[TimingPoint]
    notes: list[Note]
    modifiers: list[Modifier]

    def __init__(self, filePath: str):
        self.load_from_file(filePath)

    def load_from_file(self, filePath: str):
        rawFile = open(filePath, 'r', encoding='utf-8').read()
        circleSizeIndex = rawFile.find('CircleSize')
        self.circleSize = rawFile[circleSizeIndex +11: rawFile.find('\n', circleSizeIndex)]

        overallDifficultyIndex = rawFile.find('OverallDifficulty')
        self.overallDifficulty = rawFile[overallDifficultyIndex +18: rawFile.find('\n', overallDifficultyIndex)]
        
        approachRateIndex = rawFile.find('ApproachRate')
        self.approachRate = rawFile[approachRateIndex +13: rawFile.find('\n', approachRateIndex)]

        sliderMultiplierIndex = rawFile.find('SliderMultiplier')
        self.sliderMultiplier = rawFile[sliderMultiplierIndex +17: rawFile.find('\n', sliderMultiplierIndex)]
        
        sliderTickRateIndex = rawFile.find('SliderTickRate')
        self.sliderTickRate = rawFile[sliderTickRateIndex +15: rawFile.find('\n', sliderTickRateIndex)]

        TimingPointSectionStartIndex = rawFile.find('[TimingPoints]')
        TimingPointSectionEndIndex = rawFile.find('\n\n', TimingPointSectionStartIndex)
        timingPointLines = rawFile[TimingPointSectionStartIndex +15: TimingPointSectionEndIndex].split('\n')
        self.timingPoints = []
        for line in timingPointLines:
            self.timingPoints.append(TimingPoint.load_from_line(line))
        
        NoteSectionStartIndex = rawFile.find('[HitObjects]')
        NoteSectionEndIndex = rawFile.find('\n\n', NoteSectionStartIndex)
        noteLines = rawFile[NoteSectionStartIndex +13: NoteSectionEndIndex].split('\n')
        self.notes = []
        for line in noteLines:
            self.notes.append(Note.load_from_line(line))

        self.modifiers = []

map1 = Beatmap(beatmapFile)