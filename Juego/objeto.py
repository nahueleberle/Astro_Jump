import pygame
from config import *


class Objeto:
    def __init__(self, x, y, sprite, juego):
        self.hitbox = pygame.Rect(x, y, 20, 20)
        self.rect = self.hitbox.copy()
        self.sprite = sprite
        self.recogido = False
    
    def actualizar(self, jugador):
        self.detectar_jugador(jugador)

        if self.recogido:
            self.activar(jugador)
            self.despawnear()
            self.recogido = False

    def despawnear(self):
            self.hitbox = pygame.Rect(-200, 0, 0, 0)
            self.rect = self.hitbox.copy()

    def detectar_jugador(self, jugador):
        if self.hitbox.colliderect(jugador.hitbox):
            self.recogido = True
            
    def activar(self, jugador):
        pass

    def dibujar(self, pantalla):
        if HITBOX:
            pygame.draw.rect(pantalla, CIAN, self.rect)
        else:
            pantalla.blit(self.sprite, self.rect)