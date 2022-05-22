import pygame
import sys
from math import sin, cos, tan, atan2, pi, degrees

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_SIZE = width, height = 720, 480
SCREEN_CENTER_X = width / 2
SCREEN_CENTER_Y = height / 2
SCREEN_CENTER = SCREEN_CENTER_X, SCREEN_CENTER_Y

CIRCLE_RADIUS = 150

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Unit Circle Toy")
fontSize = 24
font = pygame.font.SysFont("Noto Sans", fontSize)
smallFontSize = 16
smallFont = pygame.font.SysFont("Noto Sans", smallFontSize)


def render_math_info(radians, degrees, sin_val, cos_val, tan_val, position, font_size):
    lines = [
        "Radians: " + str(radians),
        "Degrees: " + str(degrees),
        "sin(θ): " + str(sin_val),
        "cos(θ): " + str(cos_val),
        "tan(θ): " + str(tan_val),
    ]

    if degrees == 90 or degrees == 270:
        lines[4] = "tan(θ): undefined"

    for i, l in enumerate(lines):
        textcolor = WHITE
        if i == 2:
            textcolor = GREEN
        elif i == 3:
            textcolor = RED
        elif i == 4:
            textcolor = BLUE
        # Ripped this line from a helper function from this website
        # https://cmsdk.com/python/rendering-text-with-multiple-lines-in-pygame.html
        screen.blit(font.render(l, True, textcolor), (position[0], position[1] + font_size * i))


def sec(theta):
    return 1 / cos(theta)


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

            # We will be creating a right triangle using the SCREEN_CENTER, circleOutLinePos, and triangleRightPoint as
            # the vertexes of the triangle. mouseRadiansAngle is the angle of the hypotenuse. triangleRightPoint will
            # be the vertex of the triangle's 90-degree angle

            # Don't know why circleOutLineY needs to have a minus instead of a plus but this is how it works
            circleOutLineX = SCREEN_CENTER_X + (CIRCLE_RADIUS * cosValue)
            circleOutLineY = SCREEN_CENTER_Y - (CIRCLE_RADIUS * sinValue)
            circleOutLinePos = circleOutLineX, circleOutLineY

            triangleRightPointX = circleOutLineX
            triangleRightPointY = SCREEN_CENTER_Y
            triangleRightPoint = triangleRightPointX, triangleRightPointY

            # Start drawing the diagram
            screen.fill(BLACK)
            render_math_info(
                round(radiansAngle, 4),
                round(degreeAngle, 4),
                round(sinValue, 4),
                round(cosValue, 4),
                round(tanValue, 4),
                (5, 2), fontSize
            )
            # circle and guide lines
            pygame.draw.circle(screen, WHITE, SCREEN_CENTER, CIRCLE_RADIUS, 1)
            pygame.draw.line(screen, GRAY, SCREEN_CENTER, (SCREEN_CENTER_X + CIRCLE_RADIUS, SCREEN_CENTER_Y))
            pygame.draw.line(screen, GRAY, SCREEN_CENTER, (SCREEN_CENTER_X - CIRCLE_RADIUS, SCREEN_CENTER_Y))
            pygame.draw.line(screen, GRAY, SCREEN_CENTER, (SCREEN_CENTER_X, SCREEN_CENTER_Y + CIRCLE_RADIUS))
            pygame.draw.line(screen, GRAY, SCREEN_CENTER, (SCREEN_CENTER_X, SCREEN_CENTER_Y - CIRCLE_RADIUS))

            # adjacent side of the right triangle
            pygame.draw.line(screen, RED, SCREEN_CENTER, triangleRightPoint)
            textCenter = SCREEN_CENTER_X - (SCREEN_CENTER_X - triangleRightPointX) / 2, SCREEN_CENTER_Y
            screen.blit(smallFont.render(str(round(cosValue, 4)), True, RED), textCenter)

            # opposite side of the right triangle
            pygame.draw.line(screen, GREEN, triangleRightPoint, circleOutLinePos)
            textCenter = circleOutLineX, SCREEN_CENTER_Y - (SCREEN_CENTER_Y - circleOutLineY) / 2
            screen.blit(smallFont.render(str(round(sinValue, 4)), True, GREEN), textCenter)

            # tangent line
            tangentEndPointX = SCREEN_CENTER_X + CIRCLE_RADIUS * sec(radiansAngle)
            tangentEndPointY = SCREEN_CENTER_Y
            tangentEndPoint = (tangentEndPointX, tangentEndPointY)
            pygame.draw.line(screen, BLUE, circleOutLinePos, tangentEndPoint)
            if sinValue > 0:
                textCenter = circleOutLineX, circleOutLineY - smallFontSize
            else:
                textCenter = circleOutLineX, circleOutLineY
            screen.blit(smallFont.render(str(round(tanValue, 4)), True, BLUE), textCenter)

            # This line is the hypotenuse of the right triangle that follows the mouse's position
            # It is drawn last, so it can be visible over everything else
            pygame.draw.line(screen, WHITE, SCREEN_CENTER, circleOutLinePos)

            pygame.display.update()
