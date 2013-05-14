__author__ = 'arubtsov'

import pygame
from pygame.locals import *
import sys
import random


class Field():
    def __init__(self, sizeX, sizeY, states):
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

        :param x: Coordinate
        :param y: Coordinate
        :return: Real coords
        """
        realX, realY = x, y
        while realX > self.sizeX:
            realX -= self.sizeX
        while realX < 0:
            realX += self.sizeX
        while realY > self.sizeY:
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
        return self.arr[x][y]

    def getWithOffset(self, x, y, dx, dy):
        """


        :param x: Initial cell X
        :param y: Initial cell Y
        :param dx: X offset
        :param dy: Y offset
        :return: Cell content
        """
        realX, realY = x + dx, y + dy
        while realX > self.sizeX:
            realX -= self.sizeX
        while realX < 0:
            realX += self.sizeX
        while realY > self.sizeY:
            realY -= self.sizeY
        while realY < 0:
            realY += self.sizeY
        return self.arr[realX][realY]

    def set(self, x, y, val):
        self.arr[x][y] = val


class Main():
    def __init__(self):
        """
        stub

        """
        self.fieldSize = (200, 200)
        self.windowSize = (640, 480)
        self.numStates = 5
        self.field = [[random.randint(0, self.numStates - 1) for _ in xrange(self.fieldSize[0])]
                      for _ in xrange(self.fieldSize[1])]

    def draw(self):
        cellSize = min([(lambda i, j: i / j)(a, b) for (a, b) in zip(self.windowSize, self.fieldSize)])
        outSurf = pygame.Surface((self.fieldSize[0] * cellSize, self.fieldSize[1] * cellSize))
        for x in self.fieldSize[0]:
            for y in self.fieldSize[1]:
                pygame.draw.rect(outSurf, self.colors[self.field[x][y]],
                                 pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize))
        return outSurf

    def process(self):
        for x in xrange(self.fieldSize[0]):
            for y in xrange(self.fieldSize[1]):
                if x == 0 and y == 0:
                    neib = [self.field[1][0], self.field[0][1], self.field[1][1]]
                elif x == 0:
                    neib = [self.field[0][y + 1], self.field[0][y - 1], self.field[1][1]]

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
    main.go()
