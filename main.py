__author__ = 'arubtsov'

import pygame
from pygame.locals import *
import sys
import random


class Field():
    def __init__(self, sizeX, sizeY, states):
        """

        :param sizeX: Field width
        :param sizeY: Field height
        :param states: Number of states
        :return : Field
        """
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.numStates = states
        self.colors = []
        for i in range(self.numStates):
            self.colors.append(pygame.Color(*[random.randint(0, 255) for _ in [0, 1, 2]]))
        self.arr = self.generate()

    def generate(self):
        """

        :rtype : List
        """
        return [[random.randint(0, self.numStates - 1) for _ in xrange(self.sizeX)]
                for _ in xrange(self.sizeY)]

    def normalizeCords(self, x, y):
        """


        :rtype : (int, int)
        :param x: Coordinate
        :param y: Coordinate
        :return: Real coords
        """
        realX, realY = x, y
        while realX >= self.sizeX:
            realX -= self.sizeX
        while realX < 0:
            realX += self.sizeX
        while realY >= self.sizeY:
            realY -= self.sizeY
        while realY < 0:
            realY += self.sizeY
        return realX, realY

    def get(self, x, y):
        """

        :param x: X cell
        :param y: Y cell
        :return: Cell content
        """
        realX, realY = self.normalizeCords(x, y)
        return self.arr[realX][realY]

    def getWithOffset(self, x, y, dx, dy):
        """


        :param x: Initial cell X
        :param y: Initial cell Y
        :param dx: X offset
        :param dy: Y offset
        :return: Cell content
        """
        realX, realY = self.normalizeCords(x + dx, y + dy)
        return self.arr[realX][realY]

    def set(self, x, y, val):
        realX, realY = self.normalizeCords(x, y)
        self.arr[realX][realY] = val

    def getColor(self, x, y):
        """

        :rtype : pygame.Color
        :param x: Cell x
        :param y: Cell y
        :return: Cell color
        """
        realX, realY = self.normalizeCords(x, y)
        return self.colors[self.arr[realX][realY]]



class Main():
    def __init__(self):
        """
        stub

        """
        # self.fieldSize = (200, 200)
        # self.numStates = 5
        # self.field = [[random.randint(0, self.numStates - 1) for _ in xrange(self.fieldSize[0])]
        #               for _ in xrange(self.fieldSize[1])]
        self.field = Field(3, 3, 5)
        self.windowSize = (640, 480)

    def draw(self):
        cellSize = min([(lambda i, j: i / j)(a, b) for (a, b) in
                        zip(self.windowSize, (self.field.sizeX, self.field.sizeY))])
        outSurf = pygame.Surface((self.field.sizeX * cellSize, self.field.sizeY * cellSize))
        for x in range(self.field.sizeX):
            for y in range(self.field.sizeY):
                pygame.draw.rect(outSurf, self.field.getColor(x, y),
                                 pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize))
        return outSurf

    def process(self):
        for x in xrange(self.field.sizeX):
            for y in xrange(self.field.sizeY):
                neib = []
                for xOff in [-1, 0, 1]:
                    for yOff in [-1, 1]:
                        neib.append(self.field.get(x + xOff, y + yOff))
                print(neib)


    def go(self):
        fpsClock = pygame.time.Clock()
        pygame.init()
        wndSurf = pygame.display.set_mode(self.windowSize)
        assert isinstance(wndSurf, pygame.Surface)
        pygame.display.set_caption('Simple game')
        while True:
            wndSurf.fill(pygame.Color('white'))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
            wndSurf.blit(self.draw(), (0, 0))
            pygame.display.update()
            fpsClock.tick(30)


if __name__ == "__main__":
    main = Main()
    main.process()
    main.go()
