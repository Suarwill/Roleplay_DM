import random

class Personaje:
    def __init__(self, nombre: str, es_npc: bool = False, alineamiento_elegido: str = "NP"):
        self.nombre = nombre
        self.es_npc = es_npc
        
        # --- Las 6 Estadísticas Clásicas (Rango 1 a 5 para el juego base) ---
        self.STR = random.randint(1, 5)  # Fuerza / Strength
        self.DEX = random.randint(1, 5)  # Destreza / Dexterity
        self.CON = random.randint(1, 5)  # Constitución / Constitution
        self.INT = random.randint(1, 5)  # Inteligencia / Intelligence
        self.WIS = random.randint(1, 5)  # Sabiduría / Wisdom
        self.CHA = random.randint(1, 5)  # Carisma / Charisma
        
        # --- Vida (Afectada de forma lógica por tu Constitución) ---
        self.vida_max = 40 + (self.CON * 3)  # Ej: CON 5 da 55 HP, CON 1 da 43 HP
        self.vida_actual = self.vida_max
        
        self.inventario = []

        # L: Legal, N: Neutral, C: Caótico, B: Bueno, P: Puro, M: Malvado
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
            else:  # Legal Bueno y Neutral Bueno
                self.umbral_traicion = 10
        else:
            if alineamiento_elegido in self.TODOS_LOS_ALINEAMIENTOS:
                self.alineamiento = alineamiento_elegido
            else:
                self.alineamiento = "NP"
                
            self.confianza = 100
            self.umbral_traicion = 0

    def recibir_daño(self, cantidad: int) -> str:
        self.vida_actual -= cantidad
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