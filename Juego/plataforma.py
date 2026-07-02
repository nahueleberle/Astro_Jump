import pygame
from config import *

class Plataforma:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.ancho = 32
        self.alto = 32
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.solido = True
        self.letal = False
        self.sprite = sprite.copy()

    def dibujar(self, pantalla):
        if HITBOX:
            pygame.draw.rect(pantalla, (0, 255, 0), self.rect)
        else:
            pantalla.blit(self.sprite, self.rect)

    