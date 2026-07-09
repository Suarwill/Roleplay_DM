from logica.dados import Dados
from logica.armas import CATALOGO_ARMAS
from logica.mobs import generar_encuentro_por_habitat
from config.configuracion import inicializar_o_cargar_juego, guardar_partida

# --- INICIO DEL JUEGO ---
dados_juego = Dados()
jugador, companero = inicializar_o_cargar_juego()
lugar_actual = "bosque"

# =====================================================================
# SIMULACIÓN DE ENCUENTRO Y COMBATE CONTRA UN MOB
# =====================================================================

enemigo = generar_encuentro_por_habitat(lugar_actual)

print(f"🏕️ Exploras la zona: '{lugar_actual.upper()}'")
print(f"⚔️ ¡UN ENMIGO APARECE! Un {enemigo.nombre} bloquea el camino.")
print(f"✨ Atributo único del rival: [{enemigo.atributo_especial}]")
print(f"❤️ Vida del enemigo: {enemigo.vida_actual}/{enemigo.vida_max} HP\n")

# 2. El jugador ataca usando su arma equipada
arma_jugador = CATALOGO_ARMAS[jugador.arma_equipada] if jugador.arma_equipada else None

if arma_jugador:
    print(f"» Atacas al {enemigo.nombre} blandiendo tu {arma_jugador.nombre}...")
    
    # Tiramos el D20 de impacto
    num_d20, resultado_d20 = dados_juego.d20()
    dificultad_defensa_mob = 10  # El trasgo requiere un 10+ para ser golpeado
    
    if resultado_d20 == "CRITICO" or (resultado_d20 == "NORMAL" and num_d20 >= dificultad_defensa_mob):
        # ¡Impacto exitoso! Calculamos el daño del arma
        daño_hecho = arma_jugador.calcular_daño_base(dados_juego, jugador)
        if resultado_d20 == "CRITICO":
            daño_hecho *= 2
            print(f"🎲 ¡GOLPE CRÍTICO (20 Natural)! El daño se duplica.")
            
        # Aplicamos el daño al Mob usando el nuevo método
        mensaje_daño, enemigo_muerto = enemigo.recibir_daño(daño_hecho)
        print(mensaje_daño)
        
        # --- CONTROL DE VICTORIA Y LOOT ---
        if enemigo_muerto:
            print(f"🎉 ¡Has ganado! Obtienes {enemigo.exp_otorgada} puntos de experiencia.")
            
            # Procesamos si el enemigo soltó items
            items_obtenidos = enemigo.procesar_loot()
            
            if items_obtenidos:
                print("🎁 El enemigo dejó caer botín:")
                for item_id in items_obtenidos:
                    arma_loot = CATALOGO_ARMAS[item_id]
                    # Añadimos el ID al inventario del personaje de Python
                    jugador.inventario.append(item_id)
                    print(f"   - ¡Recogiste: {arma_loot.nombre}! (Añadido a tu inventario)")
            else:
                print("📭 Buscas en sus bolsillos pero no encuentras nada de valor.")
                
    else:
        print(f"🎲 Sacaste un {num_d20} en el D20. ¡Fallaste el golpe!")
        
        # El enemigo sigue vivo y contraataca
        daño_mob = enemigo.calcular_daño_ataque(dados_juego)
        print(f"🚨 El {enemigo.nombre} contraataca velozmente.")
        mensaje_vida_jugador = jugador.recibir_daño(daño_mob)
        print(f"   - {mensaje_vida_jugador}")

print("\n" + "-"*50)
# Guardamos el progreso final (por si el jugador obtuvo items en su inventario)
guardar_partida(jugador, companero)