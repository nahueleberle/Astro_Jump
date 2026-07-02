import pygame
from objeto import Objeto

class Moneda(Objeto):
    def __init__(self, x, y, sprite, juego):
        super().__init__(x, y, sprite, juego)
        self.sonido_moneda = pygame.mixer.Sound("assets/moneda_sonido.mp3")
        self.sonido_moneda.set_volume(0.4)
    
    def activar(self, jugador):
        jugador.contador_monedas +=1
        self.sonido_moneda.play()


