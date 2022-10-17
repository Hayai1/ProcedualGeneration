import unittest
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((700, 500))

class Test01(unittest.TestCase):
    def test_it(self):
        global mapGenerator,mapGen
        from world import mapGenerator
        mapGen = mapGenerator('ProcedualGeneration/SpriteSheet.png','ProcedualGeneration/rooms/1.txt', 'ProcedualGeneration/rooms/2Top.txt', 'ProcedualGeneration/rooms/2NoTop.txt', 'ProcedualGeneration/rooms/3.txt')
class Test02(Test01):
    def test_it(self):
        super().test_it()
        mapGen.generateNewLevel()
        


