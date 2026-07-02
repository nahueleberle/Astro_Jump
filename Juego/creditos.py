import pygame

from config import *
from ui import Texto, Boton

class Creditos:
    def __init__(self):
        self.fuente = pygame.font.SysFont(None, 72)
        self.boton_atras = Boton("Atrás", 50, (0, 0, 0), ANCHO // 2 + 5 , ALTO - 95, 345, 70, "Menu")
        self.background = pygame.image.load("assets/Creditos.png").convert()
        self.background = pygame.transform.scale(self.background, (ANCHO, ALTO))

    def actualizar(self, eventos, dt):
        for event in eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.boton_atras.esta_clickeado(pos):
                    return self.boton_atras.direccion
                    
        return None

    def dibujar(self, pantalla):        

        self.boton_atras.dibujar(pantalla)
        pantalla.blit(self.background, (0, 0))
