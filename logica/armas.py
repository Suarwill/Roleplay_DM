import json
import os

class Arma:
    def __init__(self, nombre: str, tipo_dado: str, atributo_clave: str, bono_arma: int, descripcion: str):
        self.nombre = nombre
        self.tipo_dado = tipo_dado
        self.atributo_clave = atributo_clave
        self.bono_arma = bono_arma
        self.descripcion = descripcion

    def calcular_daño_base(self, dados_instancia, personaje_instancia) -> int:
        metodo_dado = getattr(dados_instancia, self.tipo_dado)
        resultado_dado = metodo_dado()
        
        modificador_personaje = getattr(personaje_instancia, self.atributo_clave, 0)
        
        daño_total = resultado_dado + modificador_personaje + self.bono_arma
        
        return max(1, daño_total)


def cargar_catalogo_armas() -> dict[str, Arma]:
    ruta_actual = os.path.dirname(__file__)
    ruta_json = os.path.join(ruta_actual, "armas.json")
    
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    
    catalogo = {}
    for id_arma, info in datos.items():
        catalogo[id_arma] = Arma(
            nombre=info["nombre"],
            tipo_dado=info["tipo_dado"],
            atributo_clave=info["atributo_clave"],
            bono_arma=info["bono_arma"],
            descripcion=info["descripcion"]
        )
        
    return catalogo

CATALOGO_ARMAS = cargar_catalogo_armas()