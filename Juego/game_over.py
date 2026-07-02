import pygame

from config import *
from ui import Texto, Boton

class Victoria:
    def __init__(self):
        self.fuente = pygame.font.SysFont(None, 72)
        self.boton_menu = Boton("Menú", 50, (0, 0, 0), ANCHO // 2 - 100, ALTO // 2 + 100, 200, 50, "Menu")
        self.background = pygame.image.load("assets/Game_over.png").convert()
        self.background = pygame.transform.scale(self.background, (ANCHO, ALTO))

    def actualizar(self, eventos, dt):
        for event in eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.boton_menu.esta_clickeado(pos):
                    return self.boton_menu.direccion
        return None

    def dibujar(self, pantalla):
        self.boton_reiniciar.dibujar(pantalla)
        pantalla.blit(self.background, (0, 0))
