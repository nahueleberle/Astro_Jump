import pygame

from config import ALTO, ANCHO
from jugador import Jugador
from mapa import Mapa
from ui import Texto
from config import *
# juego1=Objeto()
# numero=2
# numero += 1
# juego1.actualizar(evento, dt)
# el punto significa que estamos tratando de acceder a un metodo dentro de la clase 
# dentro de la variable que se encuentra detras del punto, lo que sigue despues del punto
# es el nombre del metodo, y luego se pone entre parentesis lo que requiera ese metodo 
class Juego:
    def __init__(self):
        self.mapa = Mapa("assets/Mapa.tmx", self)
        self.plataformas = self.mapa.plataformas
        self.tanques_de_oxigeno = self.mapa.tanques_de_oxigeno
        self.monedas=self.mapa.monedas
        self.jugador=Jugador(ANCHO//6, ALTO//1.2, 20, 33)
        self.ganar = False
        #----------Música----------
        pygame.mixer.music.load("assets/Starlit Drift.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        
        #Sonidos
        self.sonido_muerte = pygame.mixer.Sound("assets/muerte.mp3")
        self.sonido_muerte.set_volume(0.3)


        self.background = pygame.image.load("assets/Backgr_1.png").convert()
        self.background = pygame.transform.scale(self.background, (ANCHO, ALTO))

        self.texto_moneda = Texto(f"Monedas:{self.jugador.contador_monedas}", 30, DORADO, 67, 50)
    

    def actualizar(self, eventos, dt):
        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.jugador.pulsar_salto()
                if event.key == pygame.K_ESCAPE:
                    return "Menu"
        teclas = pygame.key.get_pressed()
        self.jugador.actualizar(teclas, dt, self.plataformas)
        
        for tanque in self.tanques_de_oxigeno:
            tanque.actualizar(self.jugador)

        for moneda in self.monedas:
            moneda.actualizar(self.jugador)

        self.texto_moneda.actualizar_texto(f"Monedas:{self.jugador.contador_monedas}")

        if self.jugador.muerto:            
            self.sonido_muerte.play()
            return "Reiniciar"
        
        if self.ganar == True:
            return "Victoria"

    def dibujar(self, pantalla):
        pantalla.blit(self.background, (0, 0))
        for plataforma in self.plataformas:
            plataforma.dibujar(pantalla)
        self.jugador.dibujar(pantalla)
        for tanque in self.tanques_de_oxigeno:
            tanque.dibujar(pantalla)
        for moneda in self.monedas:
            moneda.dibujar(pantalla)
        self.texto_moneda.dibujar(pantalla)

    