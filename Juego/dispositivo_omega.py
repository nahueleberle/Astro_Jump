import pygame
from objeto import Objeto

class Dispositivo_omega(Objeto):

    def __init__(self, x, y, sprite, juego):
        super().__init__(x, y, sprite, juego)
        self.juego = juego
        self.sonido_victoria = pygame.mixer.Sound("assets/Victoria.mp3")
        self.sonido_victoria.set_volume(0.3)

    def activar(self, jugador):
        self.sonido_victoria.play()
        self.juego.ganar = True