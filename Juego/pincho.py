import pygame

from plataforma import Plataforma

class Pincho(Plataforma):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)
        self.letal = True
        self.sprite = sprite