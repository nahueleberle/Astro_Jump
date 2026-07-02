import pygame

from config import *
from ui import Texto, Boton

class Menu:
    def __init__(self):

        self.botones = [
        Boton("Jugar", 50, (0, 0, 0), (ANCHO // 2)-10, (ALTO // 2) + 35, 325, 65, "Juego"),
        Boton("Opciones", 50, (0, 0, 0), (ANCHO // 2)-10, (ALTO // 2) + 110, 325, 65, "Opciones"),
        Boton("Créditos", 50, (0, 0, 0), (ANCHO // 2)-10, (ALTO // 2) + 185, 325, 65, "Creditos"),
        Boton("Salir", 50, (0, 0, 0), (ANCHO // 2)-10, (ALTO // 2) + 255, 325, 65, "Salir")


        ]

        self.background = pygame.image.load("assets/Menu.png").convert()
        self.background = pygame.transform.scale(self.background, (ANCHO, ALTO))

    def actualizar(self, eventos, dt):
        for event in eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for boton in self.botones:                 
                    if boton.esta_clickeado(pos):
                        return boton.direccion
        return None

    def dibujar(self, pantalla):


        for boton in self.botones:                 
            boton.dibujar(pantalla)
        pantalla.blit(self.background, (0, 0))
