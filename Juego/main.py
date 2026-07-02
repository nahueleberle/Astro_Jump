import pygame
from victoria import Victoria
from juego import Juego
from menu import Menu
from config import *
from opciones import Opciones
from creditos import Creditos

pygame.init()
pantalla=pygame.display.set_mode((ANCHO,ALTO))
ejecutando=True

pantallas = {
    "Juego":Juego(),
    "Victoria":Victoria(),
    "Menu":Menu(),
    "Opciones":Opciones(),
    "Creditos":Creditos()
}
estado_actual = "Menu"
resultado = None

clock=pygame.time.Clock()
while ejecutando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type==pygame.QUIT:
            ejecutando=False

    teclas=pygame.key.get_pressed()
    dt=clock.tick(FPS)/1000
    pantalla.fill(GRIS)
    pantalla_actual = pantallas[estado_actual]
    resultado = pantalla_actual.actualizar(eventos, dt)
    if resultado is not None:
        estado_actual = resultado 
        if resultado == "Reiniciar":
            pantallas["Juego"] = Juego()
            estado_actual = "Juego"
            continue
        if resultado == "Salir":
            ejecutando = False
            continue
        if resultado == "Victoria":
            pantallas["Juego"] = Juego()
            estado_actual = "Victoria"
    pantallas[estado_actual].dibujar(pantalla)
    pygame.display.flip()




pygame.quit()