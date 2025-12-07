import math
from osu.notes import Position

def bezier_curve(vertices: list[Position]) -> list[Position]:
    numPoints = 50
    result = []

    b0x = vertices[0].x
    b0y = vertices[0].y
    b1x = vertices[1].x
    b1y = vertices[1].y
    b2x = vertices[2].x
    b2y = vertices[2].y
    b3x = vertices[3].x
    b3y = vertices[3].y

    # Compute polynomial coefficients from Bezier points

    ax = -b0x + 3 * b1x + -3 * b2x + b3x
    ay = -b0y + 3 * b1y + -3 * b2y + b3y

    bx = 3 * b0x + -6 * b1x + 3 * b2x
    by = 3 * b0y + -6 * b1y + 3 * b2y

    cx = -3 * b0x + 3 * b1x
    cy = -3 * b0y + 3 * b1y

    dx = b0x
    dy = b0y

    # Set up the number of steps and step size

    numSteps = numPoints - 1  # arbitrary choice
    h = 1.0 / numSteps  # compute our step size

    # Compute forward differences from Bezier points and "h"

    pointX = dx
    pointY = dy

    firstFDX = ax * (h * h * h) + bx * (h * h) + cx * h
    firstFDY = ay * (h * h * h) + by * (h * h) + cy * h

    secondFDX = 6 * ax * (h * h * h) + 2 * bx * (h * h)
    secondFDY = 6 * ay * (h * h * h) + 2 * by * (h * h)

    thirdFDX = 6 * ax * (h * h * h)
    thirdFDY = 6 * ay * (h * h * h)

    # Compute points at each step

    result.append(Position(pointX, pointY))

    for _ in range(numSteps):
        pointX += firstFDX
        pointY += firstFDY

        firstFDX += secondFDX
        firstFDY += secondFDY

        secondFDX += thirdFDX
        secondFDY += thirdFDY

        result.append(Position(pointX, pointY))
    return result

def circle_curve(vertices: list[Position]) -> list[Position]:
    numPoints = 100
    if len(vertices) != 3:
        raise ValueError("Invalid number of vertices")
    result = []

    b0x = vertices[0].x
    b0y = vertices[0].y
    b1x = vertices[1].x
    b1y = vertices[1].y
    b2x = vertices[2].x
    b2y = vertices[2].y

    centerX = (b0x + b1x + b2x) / 3
    centerY = (b0y + b1y + b2y) / 3

    radius = math.sqrt((b0x - b2x) ** 2 + (b0y - b2y) ** 2) / 2

    initialAngle = math.atan2(b1y - b0y, b1x - b0x)
    result.append(
        (
            Position((centerX + math.cos(initialAngle) * radius),
            (centerY + math.sin(initialAngle) * radius)),
        )
    )

    for i in range(numPoints // 2):
        angle = initialAngle + (i * 2 * math.pi / numPoints)
        x = centerX + math.cos(angle) * radius
        y = centerY + math.sin(angle) * radius
        result.append(Position(x, y))
    return result

def linear_curve(vertices: list[Position]) -> list[Position]:
    if len(vertices) < 2:
        return vertices
    numPoints = 50
    result = []
    for i in range(len(vertices) - 1):
        result.append((vertices[i].x, vertices[i].y))
        for j in range(1, numPoints):
            result.append(
                (
                    vertices[i].x + (vertices[i + 1].x - vertices[i].x) * j / numPoints,
                    vertices[i].y + (vertices[i + 1].y - vertices[i].y) * j / numPoints,
                )
            )
    result.append(vertices[-1])
    return result

def centripetal_curve(vertices: list[Position]) -> list[Position]:
    #Feito com IA, não sei se funciona direito
    numPoints = 50
    result = []
    
    points = [vertices[0]] + vertices + [vertices[-1]]
    numSegments = len(points) - 3

    for i in range(1, numSegments + 1):
        
        p0 = points[i - 1]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[i + 2]
        
        t0 = 0.0
        dx = p1.x - p0.x
        dy = p1.y - p0.y
        t1 = pow(math.sqrt(dx * dx + dy * dy), 0.5 / 2.0)
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        t2 = t1 + pow(math.sqrt(dx * dx + dy * dy), 0.5 / 2.0)
        dx = p3.x - p2.x
        dy = p3.y - p2.y
        t3 = t2 + pow(math.sqrt(dx * dx + dy * dy), 0.5 / 2.0)
        
        numStepsPerSegment = numPoints // (len(vertices) - 1)
        
        if i == 1:
            result.append(p1)

        for j in range(1, numStepsPerSegment + 1):

            t = t1 + (t2 - t1) * (j / numStepsPerSegment)

            A = (t1 - t) / (t2 - t0) * (t2 - t) / (t3 - t0) * (t2 - t) / (t2 - t1)
            B = (t - t0) / (t2 - t0) * (t2 - t) / (t3 - t1) * (t2 - t) / (t2 - t1)
            C = (t - t0) / (t3 - t0) * (t - t1) / (t3 - t1) * (t2 - t) / (t2 - t1)
            D = (t - t0) / (t3 - t0) * (t - t1) / (t3 - t1) * (t - t2) / (t3 - t2)
            
            a1 = (t1 - t) / (t1 - t0) * p0.x + (t - t0) / (t1 - t0) * p1.x
            a2 = (t2 - t) / (t2 - t1) * p1.x + (t - t1) / (t2 - t1) * p2.x
            a3 = (t3 - t) / (t3 - t2) * p2.x + (t - t2) / (t3 - t2) * p3.x

            b1 = (t2 - t) / (t2 - t0) * a1 + (t - t0) / (t2 - t0) * a2
            b2 = (t3 - t) / (t3 - t1) * a2 + (t - t1) / (t3 - t1) * a3

            x = (t2 - t) / (t2 - t1) * b1 + (t - t1) / (t2 - t1) * b2

            a1 = (t1 - t) / (t1 - t0) * p0.y + (t - t0) / (t1 - t0) * p1.y
            a2 = (t2 - t) / (t2 - t1) * p1.y + (t - t1) / (t2 - t1) * p2.y
            a3 = (t3 - t) / (t3 - t2) * p2.y + (t - t2) / (t3 - t2) * p3.y

            b1 = (t2 - t) / (t2 - t0) * a1 + (t - t0) / (t2 - t0) * a2
            b2 = (t3 - t) / (t3 - t1) * a2 + (t - t1) / (t3 - t1) * a3

            y = (t2 - t) / (t2 - t1) * b1 + (t - t1) / (t2 - t1) * b2

            result.append(Position(x, y))

    return result