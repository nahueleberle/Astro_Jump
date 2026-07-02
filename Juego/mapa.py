import pytmx
from plataforma import Plataforma
from pincho import Pincho
from tanque_de_oxigeno import Tanque_de_oxigeno
from dispositivo_omega import Dispositivo_omega
from moneda import Moneda


class Mapa:

    def __init__(self, mapa, juego):

        self.tmx = pytmx.load_pygame(mapa)
        self.plataformas = []
        self.tanques_de_oxigeno = []
        self.monedas=[]
        self.cargar_objetos(juego)
    
    def cargar_objetos(self, juego):

        for layer in self.tmx.visible_layers:

            if not hasattr(layer, "data"):
                continue

            for x, y, gid in layer:

                if not gid:
                    continue

                props = self.tmx.get_tile_properties_by_gid(gid)

                if props is None:
                    continue

 
                tipo = props.get("Tipo")

                sprite = self.tmx.get_tile_image_by_gid(gid)
                x_pixel = x * self.tmx.tilewidth
                y_pixel = y * self.tmx.tileheight
    
                if tipo == "plataforma":
                    self.plataformas.append(Plataforma(x_pixel,y_pixel,sprite))

                elif tipo == "pincho":
                    self.plataformas.append(Pincho(x_pixel,y_pixel,sprite))



        for obj in self.tmx.objects:

            tipo = obj.properties.get("type")

            if tipo == "oxigen_tank":
                sprite = self.tmx.get_tile_image_by_gid(obj.gid)
                self.tanques_de_oxigeno.append(Tanque_de_oxigeno(obj.x, obj.y, sprite, juego))

            if tipo == "dispositivo_omega":
                sprite = self.tmx.get_tile_image_by_gid(obj.gid)
                self.tanques_de_oxigeno.append(Dispositivo_omega(obj.x, obj.y, sprite, juego))

            if tipo == "moneda":
                sprite = self.tmx.get_tile_image_by_gid(obj.gid)
                self.monedas.append(Moneda(obj.x, obj.y, sprite, juego))



