from logica.dados import Dados
from logica.personajes import Personaje

from logica.armas import CATALOGO_ARMAS

dados_juego = Dados()

# 2. Creamos los personajes (Tu código local define estadísticas y personalidad oculta)
jugador = Personaje(nombre="Ragnar", es_npc=False)
jugador.fuerza = 3
jugador.destreza = 4

companero = Personaje(nombre="Valerius el Pícaro", es_npc=True)

print("⚔️ ¡COMIENZA LA AVENTURA! ⚔️")
print(f"Héroe: {jugador.nombre} (Fuerza: {jugador.fuerza}, Destreza: {jugador.destreza})")
print(f"Compañero: {companero.nombre} (Alineamiento Oculto: {companero.alineamiento})")
print("-" * 50)

arma_equipada = CATALOGO_ARMAS["daga_obsidiana"]
print(f"» Has equipado tu: {arma_equipada.nombre} (+{arma_equipada.bono_arma} de bono)")
print(f"» Descripción: {arma_equipada.descripcion}\n")

print("⚡ UN ORCO SE LANZA DESDE LAS SOMBRAS. Decides atacar.")
print("-" * 50)

# =====================================================================
# FLUJO DEL TURNO (Mecánicas de dados puras en Python)
# =====================================================================

# Paso A: El jugador intenta golpear (Tiramos el D20 de éxito)
numero_sacado, tipo_resultado = dados_juego.d20()
dificultad_orco = 10

# Determinamos si el ataque conecta de forma matemática
ataque_exitoso = tipo_resultado == "CRITICO" or (tipo_resultado == "NORMAL" and numero_sacado >= dificultad_orco)

# Paso B: Calculamos las consecuencias en base a los dados
if tipo_resultado == "CRITICO":
    # Multiplicamos el daño base o sumamos el máximo dado por ser crítico
    daño_base = arma_equipada.calcular_daño_base(dados_juego, jugador)
    daño_final = daño_base * 2
    print(f"🎲 Sacaste un {numero_sacado} Natual. ¡¡GOLPE CRÍTICO!!")
    print(f"💥 Destrozas al enemigo infligiendo {daño_final} de daño.")

elif ataque_exitoso:
    # Ataque normal: El arma se encarga de tirar su dado (D4), sumar destreza y su bono único
    daño_final = arma_equipada.calcular_daño_base(dados_juego, jugador)
    print(f"🎲 Sacaste un {numero_sacado} en el D20 (Supera la dificultad {dificultad_orco}). ¡Impacto!")
    print(f"⚔️ Logras herir al orco infligiendo {daño_final} de daño.")

else:
    # Fallo o Pifia
    print(f"🎲 Sacaste un {numero_sacado} en el D20 (Fallo). El orco esquiva tu ataque.")
    
    # El enemigo contraataca haciendo daño directo al jugador usando un D8
    daño_recibido = dados_juego.d8()
    print(f"🚨 El orco aprovecha tu error y te corta con su cimitarra.")
    
    # Aplicamos la reducción de vida directamente en las variables del objeto personaje
    resultado_vida = jugador.recibir_daño(daño_recibido)
    print(f"↳ {resultado_vida}")

print("-" * 50)

# =====================================================================
# CONTROL DE COMPAÑEROS (Ilusión de libre albedrío / Sistema de Confianza)
# =====================================================================
# Supongamos que durante el caos, no ayudaste a tu compañero para salvar tu pellejo
print(f"Decisión del turno: Dejaste que Valerius luchara solo contra dos trasgos.")
companero.modificar_confianza(-20) # Baja la confianza en el código local

print(f"» Confianza actual de {companero.nombre}: {companero.confianza}/100")

if companero.chequear_traicion():
    print(f"🚨 [SISTEMA]: Se ha activado la flag de TRAICIÓN. {companero.nombre} te mira con desprecio...")
    # AQUÍ es el punto exacto donde meterías el JSON estructurado para enviarle a Gemini/Ollama:
    # "El sistema determinó que el NPC traicionó al jugador. Genera la narrativa."
else:
    print(f"» {companero.nombre} sigue cubriéndote la espalda, aunque con dudas.")