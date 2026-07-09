import json
import os
import random
from .dados import Dados

class Mob:
    def __init__(self, nombre: str, vida_max: int, tipo_dado_daño: str, exp_otorgada: int, 
                 habitat: str, porcentaje_aparicion: int, atributo_especial: str, tabla_loot: list[dict]):
        self.nombre = nombre
        self.vida_max = vida_max
        self.vida_actual = vida_max
        self.tipo_dado_daño = tipo_dado_daño
        self.exp_otorgada = exp_otorgada
        self.habitat = habitat
        self.porcentaje_aparicion = porcentaje_aparicion
        self.atributo_especial = atributo_especial
        self.tabla_loot = tabla_loot

    def calcular_daño_ataque(self, dados_instancia: Dados) -> int:
        metodo_dado = getattr(dados_instancia, self.tipo_dado_daño)
        return metodo_dado()

    def recibir_daño(self, cantidad: int) -> tuple[str, bool]:
        self.vida_actual -= cantidad
        if self.vida_actual <= 0:
            self.vida_actual = 0
            return f"☠️ ¡El {self.nombre} ha sido derrotado!", True
        return f"💥 El {self.nombre} recibe {cantidad} de daño. Vida restante: {self.vida_actual}/{self.vida_max}", False

    def procesar_loot(self) -> list[str]:
        items_soltados = []
        for recompensa in self.tabla_loot:
            id_item = recompensa["id_item"]
            probabilidad = recompensa["probabilidad"]
            
            if random.randint(1, 100) <= probabilidad:
                items_soltados.append(id_item)
                
        return items_soltados


def cargar_catalogo_mobs() -> dict:
    ruta_actual = os.path.dirname(__file__)
    ruta_json = os.path.join(ruta_actual, "mobs.json")
    
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def generar_encuentro_por_habitat(habitat: str) -> Mob | None:
    datos_mobs = cargar_catalogo_mobs()
    mobs_candidatos = []
    
    for id_mob, info in datos_mobs.items():
        if info["habitat"] == habitat:
            mobs_candidatos.append((id_mob, info))
            
    random.shuffle(mobs_candidatos)
    
    for id_mob, info in mobs_candidatos:
        if random.randint(1, 100) <= info["porcentaje_aparicion"]:
            return Mob(
                nombre=info["nombre"],
                vida_max=info["vida_max"],
                tipo_dado_daño=info["tipo_dado_daño"],
                exp_otorgada=info["exp_otorgada"],
                habitat=info["habitat"],
                porcentaje_aparicion=info["porcentaje_aparicion"],
                atributo_especial=info["atributo_especial"],
                tabla_loot=info["tabla_loot"]
            )
            
    if mobs_candidatos:
        mobs_candidatos.sort(key=lambda x: x[1]["porcentaje_aparicion"], reverse=True)
        mejor_opcion = mobs_candidatos[0][1]
        return Mob(
            nombre=mejor_opcion["nombre"],
            vida_max=mejor_opcion["vida_max"],
            tipo_dado_daño=mejor_opcion["tipo_dado_daño"],
            exp_otorgada=mejor_opcion["exp_otorgada"],
            habitat=mejor_opcion["habitat"],
            porcentaje_aparicion=mejor_opcion["porcentaje_aparicion"],
            atributo_especial=mejor_opcion["atributo_especial"],
            tabla_loot=mejor_opcion["tabla_loot"]
        )
        
    return None