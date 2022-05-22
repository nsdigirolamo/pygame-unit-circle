# Author: Nicholas DiGirolamo
# Created: May 5, 2022

import pygame
import sys
from math import sin, cos, tan, atan2, pi, degrees

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GRAY = 128, 128, 128
RED = 255, 85, 85
GREEN = 85, 255, 85
BLUE = 85, 85, 255
PINK = 255, 85, 255
YELLOW = 255, 255, 85
ORANGE = 255, 170, 85

SCREEN_SIZE = WIDTH, HEIGHT = 720, 480
SCREEN_CENTER = SCREEN_CENTER_X, SCREEN_CENTER_Y = WIDTH / 2, HEIGHT / 2

CIRCLE_RADIUS = WIDTH * 0.2
LARGE_FONT_SIZE = int(WIDTH * 0.03)
SMALL_FONT_SIZE = int(WIDTH * 0.02)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Unit Circle Toy")
largeFont = pygame.font.SysFont("Noto Sans", LARGE_FONT_SIZE)
smallFont = pygame.font.SysFont("Noto Sans", SMALL_FONT_SIZE)


def render_math_info(radians, degrees, sin_val, cos_val, tan_val, cot_val, csc_val, sec_val, position, font_size):

    lines = [
        "Radians: " + str(radians),
        "Degrees: " + str(degrees),
        "sin(θ): " + str(sin_val),
        "cos(θ): " + str(cos_val),
        "tan(θ): " + str(tan_val),
        "cot(θ): " + str(cot_val),
        "csc(θ): " + str(csc_val),
        "sec(θ): " + str(sec_val),
    ]

    if degrees == 0 or degrees == 180:
        lines[5] = "cot(θ): DNE"
        lines[6] = "csc(θ): DNE"

    if degrees == 90 or degrees == 270:
        lines[4] = "tan(θ): DNE"
        lines[7] = "sec(θ): DNE"

    for i, l in enumerate(lines):
        textcolor = WHITE
        if i == 2:
            textcolor = GREEN
        elif i == 3:
            textcolor = RED
        elif i == 4:
            textcolor = BLUE
        elif i == 5:
            textcolor = PINK
        elif i == 6:
            textcolor = ORANGE
        elif i == 7:
            textcolor = YELLOW
        # Ripped this line from a helper function from this website
        # https://cmsdk.com/python/rendering-text-with-multiple-lines-in-pygame.html
        screen.blit(largeFont.render(l, True, textcolor), (position[0], position[1] + 1.6 * font_size * i))


def midpoint(point1, point2):
    return (point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2


def sec(theta):
    if cos(theta) == 0:
        return 0
    else:
        return 1 / cos(theta)


def csc(theta):
    if sin(theta) == 0:
        return 0
    else:
        return 1 / sin(theta)


def cot(theta):
    if tan(theta) == 0:
        return 0
    else:
        return 1 / tan(theta)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            mousePos = pygame.mouse.get_pos()
            mousePosX = mousePos[0]
            mousePosY = mousePos[1]

            # Subtract pi and take absolute value of atan2's result to get an angle between 0 and 2pi. This might not
            # necessarily be the best way to do this but it works properly so I'm leaving it as is.
            radiansAngle = abs(atan2(SCREEN_CENTER_Y - mousePosY, SCREEN_CENTER_X - mousePosX) - pi)
            degreeAngle = degrees(radiansAngle)
            sinValue = sin(radiansAngle)
            cosValue = cos(radiansAngle)
            tanValue = tan(radiansAngle)
            cotValue = cot(radiansAngle)
            cscValue = csc(radiansAngle)
            secValue = sec(radiansAngle)

            # We will be creating a right triangle using the SCREEN_CENTER, circleOutLinePos, and triangleRightPoint as
            # the vertexes of the triangle. mouseRadiansAngle is the angle of the hypotenuse. triangleRightPoint will
            # be the vertex of the triangle's 90-degree angle

            circleOutLinePos = \
                circleOutLineX, circleOutLineY = \
                SCREEN_CENTER_X + (CIRCLE_RADIUS * cosValue), SCREEN_CENTER_Y - (CIRCLE_RADIUS * sinValue)
            triangleRightPoint = \
                triangleRightPointX, triangleRightPointY = \
                circleOutLineX, SCREEN_CENTER_Y

            # Now we start drawing the diagram
            
            # math information
            screen.fill(BLACK)
            render_math_info(
                round(radiansAngle, 4),
                round(degreeAngle, 4),
                round(sinValue, 4),
                round(cosValue, 4),
                round(tanValue, 4),
                round(cotValue, 4),
                round(cscValue, 4),
                round(secValue, 4),
                (5, 2), SMALL_FONT_SIZE
            )
            
            # circle and guide lines
            pygame.draw.circle(screen, WHITE, SCREEN_CENTER, CIRCLE_RADIUS, 1)
            pygame.draw.line(screen, GRAY, SCREEN_CENTER, (SCREEN_CENTER_X + CIRCLE_RADIUS, SCREEN_CENTER_Y))
            pygame.draw.line(screen, GRAY, SCREEN_CENTER, (SCREEN_CENTER_X - CIRCLE_RADIUS, SCREEN_CENTER_Y))
            pygame.draw.line(screen, GRAY, SCREEN_CENTER, (SCREEN_CENTER_X, SCREEN_CENTER_Y + CIRCLE_RADIUS))
            pygame.draw.line(screen, GRAY, SCREEN_CENTER, (SCREEN_CENTER_X, SCREEN_CENTER_Y - CIRCLE_RADIUS))

            # cosine line (adjacent face of triangle)
            pygame.draw.line(screen, RED, SCREEN_CENTER, triangleRightPoint)
            screen.blit(smallFont.render(str(round(cosValue, 4)), True, RED),
                        midpoint(triangleRightPoint, SCREEN_CENTER))

            # sine line (opposite face of triangle)
            pygame.draw.line(screen, GREEN, triangleRightPoint, circleOutLinePos)
            screen.blit(smallFont.render(str(round(sinValue, 4)), True, GREEN),
                        midpoint(triangleRightPoint, circleOutLinePos))

            # tangent line
            tangentEndPoint = \
                tangentEndPointX, tangentEndPointY = \
                SCREEN_CENTER_X + CIRCLE_RADIUS * sec(radiansAngle), SCREEN_CENTER_Y
            pygame.draw.line(screen, BLUE, circleOutLinePos, tangentEndPoint)
            if degrees != 90 and degrees != 270:
                screen.blit(smallFont.render(str(round(tanValue, 4)), True, BLUE),
                            midpoint(circleOutLinePos, tangentEndPoint))

            # cotangent line
            cotangentEndPoint = \
                cotangentEndPointX, cotangentEndPointY = \
                SCREEN_CENTER_X, SCREEN_CENTER_Y - CIRCLE_RADIUS * csc(radiansAngle)
            pygame.draw.line(screen, PINK, circleOutLinePos, cotangentEndPoint)
            if degrees != 0 and degrees != 180:
                screen.blit(smallFont.render(str(round(cotValue, 4)), True, PINK),
                            midpoint(circleOutLinePos, cotangentEndPoint))

            # cosecant line
            cosecantEndPoint = cotangentEndPoint
            pygame.draw.line(screen, ORANGE, SCREEN_CENTER, cosecantEndPoint)
            if degrees != 0 and degrees != 180:
                screen.blit(smallFont.render(str(round(cscValue, 4)), True, ORANGE),
                            midpoint(SCREEN_CENTER, cosecantEndPoint))

            # secant line
            secantEndPoint = tangentEndPoint
            # lower the line by 2 pixels so the red cosine line is still visible
            raisedCenter = SCREEN_CENTER_X, SCREEN_CENTER_Y + 2
            raisedSecantEndPoint = secantEndPoint[0], secantEndPoint[1] + 2
            pygame.draw.line(screen, YELLOW, raisedCenter, raisedSecantEndPoint)
            if degrees != 90 and degrees != 270:
                screen.blit(smallFont.render(str(round(secValue, 4)), True, YELLOW),
                            midpoint(SCREEN_CENTER, secantEndPoint))

            # This line is the hypotenuse of the right triangle that follows the mouse's position
            # It is drawn last, so it can be visible over everything else
            pygame.draw.line(screen, WHITE, SCREEN_CENTER, circleOutLinePos)

            pygame.display.update()
