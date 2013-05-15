from __future__ import division
import copy
import pygame
from pygame.locals import *
import sys
import random


__author__ = 'arubtsov'


class Field():
    def __init__(self, sizeX=100, sizeY=100, states=5, tresh=0.5, prob=0.5):
        """


        :param prob: Move probability
        :param tresh: Move threshold
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
        self.colors[0] = pygame.Color('white')
        self.arr = self.generate()
        self.shadowArr = copy.deepcopy(self.arr)
        self.tresh = tresh
        self.prob = prob

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

    def get(self, x, y, shadow=False):
        """

        :param x: X cell
        :param y: Y cell
        :return: Cell content
        """
        realX, realY = self.normalizeCords(x, y)
        if shadow:
            return self.shadowArr[realX][realY]
        return self.arr[realX][realY]

    def getWithOffset(self, x, y, dx, dy):
        """


        :param x: Initial cell X
        :param y: Initial cell Y
        :param dx: X offset
        :param dy: Y offset
        :return: Cell content
        """

        return self.get(x + dx, y + dy)

    def set(self, x, y, val, shadow=False):
        realX, realY = self.normalizeCords(x, y)
        if shadow:
            self.shadowArr[realX][realY] = val
        else:
            self.arr[realX][realY] = val

    def getColor(self, x, y):
        """

        :rtype : pygame.Color
        :param x: Cell x
        :param y: Cell y
        :return: Cell color
        """
        # realX, realY = self.normalizeCords(x, y)
        return self.colors[self.get(x, y)]

    def process(self):
        for x in xrange(self.sizeX):
            for y in xrange(self.sizeY):
                neib = []
                for xOff in [-1, 0, 1]:
                    for yOff in [-1, 0, 1]:
                        if xOff == 0 and yOff == 0:
                            pass
                        else:
                            neib.append(self.get(x + xOff, y + yOff))
                percent = neib.count(self.get(x, y)) / len(neib)
                if percent < self.tresh:
                    swapX, swapY = random.randint(0, self.sizeX), random.randint(0, self.sizeY)
                    while self.get(swapX, swapY, True) != 0:
                        swapX, swapY = random.randint(0, self.sizeX), random.randint(0, self.sizeY)
                    t1, t2 = self.get(swapX, swapY, True), self.get(x, y, True)
                    self.set(x, y, t1, True)
                    self.set(swapX, swapY, t2, True)
        self.arr = copy.deepcopy(self.shadowArr)


class Main():
    def __init__(self):
        """
        stub

        """
        self.field = Field(100, 100, 4, 0.5)
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
        self.field.process()

    def go(self):
        fpsClock = pygame.time.Clock()
        pygame.init()
        wndSurf = pygame.display.set_mode(self.windowSize)
        assert isinstance(wndSurf, pygame.Surface)
        pygame.display.set_caption('Insert name')
        while True:
            wndSurf.fill(pygame.Color('white'))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
            self.process()
            wndSurf.blit(self.draw(), (0, 0))
            pygame.display.update()
            fpsClock.tick(10)


if __name__ == "__main__":
    main = Main()
    main.process()
    main.go()
