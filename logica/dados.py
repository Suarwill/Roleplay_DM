import random

class Dados:
    def __init__(self):
        pass

    # --- Dados de Daño ---
    def d4(self) -> int:
        # Dagas o hechizos menores.
        return random.randint(1, 4)

    def d6(self) -> int:
        # Espadas cortas o arcos.
        return random.randint(1, 6)

    def d8(self) -> int:
        # Espadas largas o hachas.
        return random.randint(1, 8)

    # --- Dados de Efectos / Estados ---
    def d10(self) -> int:
        # Porcentajes o efectos secundarios.
        return random.randint(1, 10)

    def d12(self) -> int:
        # Efectos mayores o daño de armas pesadas.
        return random.randint(1, 12)

    # --- Dado de Éxito, Ataques y Fallos ---
    def d20(self) -> tuple[int, str]:
        """
        Dado de 20 caras. Determina si una acción tiene éxito, falla o es crítica.
        Devuelve una tupla: (el número del dado, el tipo de resultado)
        """
        resultado = random.randint(1, 20)
        
        if resultado == 20:
            tipo = "CRITICO"
        elif resultado == 1:
            tipo = "FALLO"
        else:
            tipo = "NORMAL"
            
        return resultado, tipo