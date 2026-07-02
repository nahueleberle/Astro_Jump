import pygame

from config import *

class Texto:
    def __init__(self, texto, tamaño, color, x, y):
        self.fuente = pygame.font.SysFont(None, tamaño)
        self.texto = self.fuente.render(texto, True, color)
        self.color = color
        self.x = x
        self.y = y

    def actualizar_texto(self, nuevo_texto):
        self.texto = self.fuente.render(nuevo_texto, True, self.color)
        

    def dibujar(self, pantalla):
        rect = self.texto.get_rect(center=(self.x, self.y))
        pantalla.blit(self.texto, rect)

class Boton:
    def __init__(self, texto, tamaño, color, x, y, ancho, alto, direccion):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.rect = pygame.Rect(x-(ancho//2), y-(alto//2), ancho, alto)
        self.direccion = direccion
        self.texto = Texto(texto, tamaño, color, self.rect.centerx, self.rect.centery)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (200, 200, 200), self.rect)
        self.texto.dibujar(pantalla)

    def esta_clickeado(self, pos):
        return self.rect.collidepoint(pos)   
    

class Oxigeno:
    TAM_BARRA_OXIGENO = 50
    COLOR_BARRA_OXIGENO_ALTA = CELESTE_FUERTE
    COLOR_BARRA_OXIGENO_MEDIA = CELESTE_MEDIO
    COLOR_BARRA_OXIGENO_BAJA = CELESTE_BAJO

    def __init__(self, jugador):
        self.ancho = self.TAM_BARRA_OXIGENO
        self.alto = 6
        self.jugador = jugador
        self.x = self.jugador.hitbox.centerx - self.ancho / 2
        self.y = self.jugador.hitbox.top - 25
        self.porcentaje = self.jugador.oxigeno / self.jugador.OXIGENO_MAX
        self.rect_vida = pygame.Rect(self.x, self.y, self.ancho * self.porcentaje, self.alto)
        self.rect_fondo = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def actualizar(self):
        self.x = self.jugador.hitbox.centerx - self.ancho / 2
        self.y = self.jugador.hitbox.top - 25
        self.porcentaje = self.jugador.oxigeno / self.jugador.OXIGENO_MAX
        self.rect_vida = pygame.Rect(self.x, self.y, self.ancho * self.porcentaje, self.alto)
        self.rect_fondo = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
    def dibujar(self, pantalla):
        self.rect_fondo = pygame.draw.rect(pantalla, NEGRO, self.rect_fondo)
        if self.porcentaje >= 0.66:
            self.rect_vida = pygame.draw.rect(pantalla, CELESTE_FUERTE, self.rect_vida)
        elif 0.33 <= self.porcentaje < 0.66:
            self.rect_vida = pygame.draw.rect(pantalla, CELESTE_MEDIO, self.rect_vida)
        else:
            self.rect_vida = pygame.draw.rect(pantalla, CELESTE_BAJO, self.rect_vida)