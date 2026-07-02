import pygame
from objeto import Objeto

class Tanque_de_oxigeno(Objeto):

    OXIGENO_RECUPERADO = 20

    def __init__(self, x, y, sprite, juego):
        super().__init__(x, y, sprite, juego)
        self.sonido_oxigeno = pygame.mixer.Sound("assets/oxigeno.mp3")
        self.sonido_oxigeno.set_volume(0.4)

    def activar(self, jugador):
        jugador.oxigeno += self.OXIGENO_RECUPERADO
        self.sonido_oxigeno.play()