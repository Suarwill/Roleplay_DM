import json
import os
from logica.personajes import Personaje

ARCHIVO_GUARDADO = "partida.json"

def guardar_partida(jugador: Personaje, companero: Personaje):
    datos_partida = {
        "jugador": jugador.to_dict(),
        "companero": companero.to_dict()
    }
    with open(ARCHIVO_GUARDADO, "w", encoding="utf-8") as archivo:
        json.dump(datos_partida, archivo, indent=4, ensure_ascii=False)
    print("💾 [SISTEMA] Partida guardada de forma local.")

def inicializar_o_cargar_juego() -> tuple[Personaje, Personaje]:
    if os.path.exists(ARCHIVO_GUARDADO):
        try:
            with open(ARCHIVO_GUARDADO, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                
            jugador = Personaje.from_dict(datos["jugador"])
            companero = Personaje.from_dict(datos["companero"])
            print("📂 [SISTEMA] Partida detectada y cargada con éxito.")
            return jugador, companero
        except (json.JSONDecodeError, KeyError):
            print("⚠️ [SISTEMA] Archivo de guardado corrupto. Generando nueva partida...")
    
    print("✨ [SISTEMA] No se encontró partida previa. Creando personajes nuevos...")  
    nuevo_jugador = Personaje(nombre="Ragnar", es_npc=False, alineamiento_elegido="CB")
    nuevo_companero = Personaje(nombre="Valerius", es_npc=True)
    
    nuevo_jugador.arma_equipada = "espada_larga"
    
    guardar_partida(nuevo_jugador, nuevo_companero)
    print("📁 [SISTEMA] Archivo 'partida.json' creado automáticamente para futuras sesiones.")
    
    return nuevo_jugador, nuevo_companero
