import pygame
from ui import Oxigeno
from config import *

class Jugador:

    # Constantes de movimiento
    FUERZA_SALTO = -350 // 1.4
    ACELERACION = 2500 // 2
    FRICCION = 900 // 2
    VELOCIDAD_MAX = 200 // 2
    VELOCIDAD_MAX_CAIDA = 400 // 2

    # Constante de gravedad
    GRAVEDAD_SUBIDA = 300 
    GRAVEDAD_CORTE = 625 
    GRAVEDAD_CAIDA = 550 
    GRAVEDAD_CAIDA_RAPIDA = 1500 

    # Asistencia al salto
    COYOTE_TIME = 0.15
    JUMP_BUFFER_TIME = 0.15
   
    # Oxigeno
    OXIGENO_MAX = 9
    OXIGENO_VEL_CONSUMO = 1  

    # Animaciones
    DELAY_ANIM_SALTO = 0.1  
    DELAY_ANIM_CORRER = 0.2
    DELAY_ANIM_IDLE = 0.1 


    def __init__(self, x, y, ancho, alto):
        
        #Posición
        self.pos_x = x
        self.pos_y = y

        #Colisiones
        self.hitbox = pygame.Rect(self.pos_x, self.pos_y, ancho, alto)
        self.rect = self.hitbox.copy()
        
        #Cambio de pantalla
        self.cambiar_pantalla = None

        #Velocidad
        self.velocidad_x = 0
        self.velocidad_y = 0

        #Estados de salto
        self.en_suelo = False
        self.coyote_timer = 0
        self.jump_buffer_timer = 0

        #Oxigeno
        self.oxigeno = self.OXIGENO_MAX
        self.barra_oxigeno = Oxigeno(self)

        #Timer y contadores de animacion
        self.frame_saltar = 0
        self.frame_correr = 0
        self.frame_idle = 0
        self.frame_animacion = 0
        self.mirando_derecha = True
        self.estaba_en_suelo = False
        self.timer_pasos = 0

        #Sonidos
        self.sonido_salto = pygame.mixer.Sound("assets/salto.mp3")
        self.sonido_salto.set_volume(0.15)
        self.sonido_caida = pygame.mixer.Sound("assets/caida.mp3")
        self.sonido_caida.set_volume(0.1) 
        self.sonido_pasos = pygame.mixer.Sound("assets/pasos.mp3")
        self.sonido_pasos.set_volume(0.1) 

        #Animaciones
        self.timer_animacion = 0
        self.hoja_correr = pygame.image.load("assets/Correr.png").convert_alpha()
        CELDA_Y = 273
        CELDA_X = 221
        self.sprites_correr = [
            self.hoja_correr.subsurface((0, 0, CELDA_X, CELDA_Y)),
            self.hoja_correr.subsurface((CELDA_X * 1, 0, CELDA_X, CELDA_Y)),
            self.hoja_correr.subsurface((CELDA_X * 2, 0, CELDA_X, CELDA_Y))
        ]

        self.hoja_saltar = pygame.image.load("assets/Saltar.png").convert_alpha()
        CELDA_Y = 207
        CELDA_X = 170
        self.sprites_saltar = [
            self.hoja_saltar.subsurface((0, 0, CELDA_X, CELDA_Y)),
            self.hoja_saltar.subsurface((CELDA_X * 1, 0, CELDA_X, CELDA_Y)),
            self.hoja_saltar.subsurface((CELDA_X * 2, 0, CELDA_X, CELDA_Y))
        ]

        self.idle = pygame.image.load("assets/Idle.png").convert_alpha()
        CELDA_Y = 187
        CELDA_X = 182
        self.sprites_idle = [
            self.idle.subsurface((0, 0, CELDA_X, CELDA_Y)),
            self.idle.subsurface((CELDA_X * 1, 0, CELDA_X, CELDA_Y)),
            self.idle.subsurface((CELDA_X * 2, 0, CELDA_X, CELDA_Y)),
            self.idle.subsurface((CELDA_X * 3, 0, CELDA_X, CELDA_Y)),
            self.idle.subsurface((CELDA_X * 4, 0, CELDA_X, CELDA_Y))
        ]

        for sprites in range(len(self.sprites_correr)):
            self.sprites_correr[sprites] = pygame.transform.scale(self.sprites_correr[sprites], (42,50))

        for sprites in range(len(self.sprites_saltar)):
            self.sprites_saltar[sprites] = pygame.transform.scale(self.sprites_saltar[sprites], (42,50))

        for sprites in range(len(self.sprites_idle)):
            self.sprites_idle[sprites] = pygame.transform.scale(self.sprites_idle[sprites], (50,50))

        self.sprite_actual = self.sprites_idle[self.timer_animacion]

        #Muerte
        self.muerto = False

        self.contador_monedas= 0

    def actualizar(self, teclas, dt, obstaculos):
        self.estaba_en_suelo = self.en_suelo
        self.leer_movimiento_horizontal(dt, teclas)
        self.aplicar_gravedad(dt, teclas)
        self.mover_x(dt, obstaculos)
        self.mover_y(dt, obstaculos)
        self.comprobar_suelo(obstaculos)
        if not self.estaba_en_suelo and self.en_suelo:
            self.sonido_caida.play()
        if self.velocidad_x !=0 and self.en_suelo:
            self.timer_pasos += dt
            if self.timer_pasos >= 0.4:
                self.sonido_pasos.play()
                self.timer_pasos = 0
        self.procesar_salto()
        self.actualizar_timers(dt)
        self.comprobar_oxigeno(dt)
        self.animar(dt)

    def actualizar_timers(self, dt):
        if self.en_suelo:
            self.coyote_timer = self.COYOTE_TIME
        else:
            self.coyote_timer = max(0, self.coyote_timer - dt)

        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer = max(0, self.jump_buffer_timer - dt)

    def leer_movimiento_horizontal(self, dt, teclas):
        direccion = 0
        if teclas[pygame.K_LEFT]:
            direccion = -1
            self.mirando_derecha = False
        if teclas[pygame.K_RIGHT]:
            direccion = 1
            self.mirando_derecha = True
        aceleracion = self.ACELERACION
        if (direccion < 0 and self.velocidad_x > 0) or (direccion > 0 and self.velocidad_x < 0):
            aceleracion *= 1
        if direccion != 0:
            self.velocidad_x += direccion * aceleracion * dt

        else:
            if self.velocidad_x > 0:
                self.velocidad_x = max(0, self.velocidad_x - self.FRICCION * dt)

            elif self.velocidad_x < 0:
                self.velocidad_x = min(0, self.velocidad_x + self.FRICCION * dt)
        
        self.velocidad_x = max(-self.VELOCIDAD_MAX, min(self.velocidad_x, self.VELOCIDAD_MAX))

    def procesar_salto(self):
        puede_saltar = self.en_suelo or self.coyote_timer > 0
        if puede_saltar and self.jump_buffer_timer > 0:
            self.velocidad_y = self.FUERZA_SALTO
            self.en_suelo = False
            self.coyote_timer = 0
            self.jump_buffer_timer = 0
            self.frame_saltar = 0
            self.sonido_salto.play()

    def pulsar_salto(self):
        self.jump_buffer_timer = self.JUMP_BUFFER_TIME

    def mover_x(self, dt, obstaculos):
        self.pos_x += self.velocidad_x * dt
        self.hitbox.x = round(self.pos_x)

        for obstaculo in obstaculos:
            if self.hitbox.colliderect(obstaculo.rect):
                self.resolver_colision_horizontal(obstaculo)
                self.pos_x = self.hitbox.x

                if obstaculo.letal:
                    self.muerto = True

    def mover_y(self, dt, obstaculos):
        self.pos_y += self.velocidad_y * dt
        self.hitbox.y = round(self.pos_y)
        self.en_suelo = False
        for obstaculo in obstaculos:
            if self.hitbox.colliderect(obstaculo.rect):
                self.resolver_colision_vertical(obstaculo)
                self.pos_y = self.hitbox.y                
                if obstaculo.letal:
                    self.muerto = True

    def aplicar_gravedad(self, dt, teclas):
        if self.en_suelo:
            self.velocidad_y = 0
            return
        gravedad = self.gravedad_actual(teclas)
        self.velocidad_y += gravedad * dt
        self.velocidad_y = min(self.velocidad_y, self.VELOCIDAD_MAX_CAIDA)

    def gravedad_actual(self, teclas):
        if self.velocidad_y < 0:
            if teclas[pygame.K_SPACE] or teclas[pygame.K_UP]:
                return self.GRAVEDAD_SUBIDA
            return self.GRAVEDAD_CORTE
        if teclas [pygame.K_DOWN]:
            return self.GRAVEDAD_CAIDA_RAPIDA

        return self.GRAVEDAD_CAIDA

    def comprobar_oxigeno(self, dt):
        self.oxigeno -= dt * self.OXIGENO_VEL_CONSUMO
        if self.oxigeno <= 0:
            self.muerto = True
        if self.oxigeno > self.OXIGENO_MAX:
            self.oxigeno = self.OXIGENO_MAX
        self.barra_oxigeno.actualizar()

    def comprobar_suelo(self, obstaculos):
        self.hitbox.y += 1
        for obstaculo in obstaculos:
            if self.hitbox.colliderect(obstaculo.rect):
                self.en_suelo = True
                if obstaculo.letal:
                    self.muerto = True
                break

        self.hitbox.y -= 1
        if self.en_suelo:
            self.coyote_timer = self.COYOTE_TIME

    def resolver_colision_horizontal(self, obstaculo):
        if self.velocidad_x > 0:
            self.hitbox.right = obstaculo.rect.left
        elif self.velocidad_x < 0:
            self.hitbox.left = obstaculo.rect.right

    def resolver_colision_vertical(self, obstaculo):
        if self.velocidad_y > 0:
            self.hitbox.bottom = obstaculo.rect.top
            self.pos_y = self.hitbox.y
            self.velocidad_y = 0
            self.en_suelo = True
            self.coyote_timer = self.COYOTE_TIME
        elif self.velocidad_y < 0:
            self.hitbox.top = obstaculo.rect.bottom
            self.pos_y = self.hitbox.y
            self.velocidad_y = 0

    def animar(self,dt):
        self.timer_animacion += dt
        if self.velocidad_y >= 30 or self.velocidad_y <= -30:
            if self.timer_animacion > self.DELAY_ANIM_SALTO:
                self.timer_animacion = 0            
                if self.frame_saltar < len(self.sprites_saltar) -1:
                    self.frame_saltar += 1
            self.sprite_actual = self.sprites_saltar[self.frame_saltar]

                
        elif self.velocidad_x != 0:
            if self.timer_animacion > self.DELAY_ANIM_CORRER:
                self.timer_animacion = 0 
                self.frame_correr += 1           
                if self.frame_correr >= len(self.sprites_correr):
                    self.frame_correr = 0
            self.sprite_actual = self.sprites_correr[self.frame_correr]


        else:
            if self.timer_animacion > self.DELAY_ANIM_IDLE:
                self.timer_animacion = 0
                self.frame_idle += 1            
                if self.frame_idle >= len(self.sprites_idle):
                    self.frame_idle = 0    
            self.sprite_actual = self.sprites_idle[self.frame_idle]

        if not self.mirando_derecha:
            self.sprite_actual = pygame.transform.flip(self.sprite_actual, True, False)

        self.rect = self.sprite_actual.get_rect(midbottom = self.hitbox.midbottom)


    def dibujar(self, pantalla):
        if HITBOX:
            pygame.draw.rect(pantalla, (255, 0, 0), self.hitbox)
        else:
            pantalla.blit(self.sprite_actual, self.rect)
        self.barra_oxigeno.dibujar(pantalla)    

    