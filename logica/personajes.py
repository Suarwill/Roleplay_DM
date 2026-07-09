import random

class Personaje:
    def __init__(self, nombre: str, es_npc: bool = False, alineamiento_elegido: str = "NP"):
        self.nombre = nombre
        self.es_npc = es_npc
        
        # --- Las 6 Estadísticas Clásicas ---
        self.STR = random.randint(1, 5)  
        self.DEX = random.randint(1, 5)  
        self.CON = random.randint(1, 5)  
        self.INT = random.randint(1, 5)  
        self.WIS = random.randint(1, 5)  
        self.CHA = random.randint(1, 5)  
        
        # --- Vida ---
        self.vida_max = 40 + (self.CON * 3)  
        self.vida_actual = self.vida_max
        
        self.inventario = []
        self.arma_equipada = None

        self.TODOS_LOS_ALINEAMIENTOS = [
            "LB", "NB", "CB",
            "LP", "NP", "CP",
            "LM", "NM", "CM"
        ]

        # --- Gestión de Alineamiento, Confianza y Traición ---
        if es_npc:
            self.alineamiento = random.choice(self.TODOS_LOS_ALINEAMIENTOS)
            self.confianza = 50
            
            if self.alineamiento == "CM":
                self.umbral_traicion = 65
            elif self.alineamiento in ["NM", "LM"]:
                self.umbral_traicion = 50
            elif self.alineamiento == "CP":
                self.umbral_traicion = 40
            elif self.alineamiento in ["NP", "LP"]:
                self.umbral_traicion = 30
            elif self.alineamiento == "CB":
                self.umbral_traicion = 20
            else:  
                self.umbral_traicion = 10
        else:
            if alineamiento_elegido in self.TODOS_LOS_ALINEAMIENTOS:
                self.alineamiento = alineamiento_elegido
            else:
                self.alineamiento = "NP"
                
            self.confianza = 100
            self.umbral_traicion = 0

    def recibir_daño(self, cantidad: int) -> str:
        self.vida_actual = self.vida_actual - cantidad
        if self.vida_actual <= 0:
            self.vida_actual = 0
            return f"¡{self.nombre} ha caído inconsciente o muerto!"
        return f"{self.nombre} pierde {cantidad} HP. Vida restante: {self.vida_actual}/{self.vida_max}"

    def modificar_confianza(self, cantidad: int):
        if self.es_npc:
            self.confianza = max(0, min(100, self.confianza + cantidad))

    def chequear_traicion(self) -> bool:
        if self.es_npc and self.confianza < self.umbral_traicion:
            return True
        return False

    # =====================================================================
    # SISTEMA DE GUARDADO / CARGA LOCAL
    # =====================================================================
    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "es_npc": self.es_npc,
            "STR": self.STR,
            "DEX": self.DEX,
            "CON": self.CON,
            "INT": self.INT,
            "WIS": self.WIS,
            "CHA": self.CHA,
            "vida_max": self.vida_max,
            "vida_actual": self.vida_actual,
            "alineamiento": self.alineamiento,
            "confianza": self.confianza,
            "umbral_traicion": self.umbral_traicion,
            "inventario": self.inventario,
            "arma_equipada": self.arma_equipada
        }

    @staticmethod
    def from_dict(datos: dict):
        p = Personaje(nombre=datos["nombre"], es_npc=datos["es_npc"])
        p.STR = datos["STR"]
        p.DEX = datos["DEX"]
        p.CON = datos["CON"]
        p.INT = datos["INT"]
        p.WIS = datos["WIS"]
        p.CHA = datos["CHA"]
        p.vida_max = datos["vida_max"]
        p.vida_actual = datos["vida_actual"]
        p.alineamiento = datos["alineamiento"]
        p.confianza = datos["confianza"]
        p.umbral_traicion = datos["umbral_traicion"]
        p.inventario = datos["inventario"]
        p.arma_equipada = datos["arma_equipada"]
        return p