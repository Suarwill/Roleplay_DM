from logica.dados import Dados

dados_juego = Dados()

print("⚔️ ¡Comienza el combate! ⚔️")

# 1. El jugador intenta una acción (Tiramos el D20 de éxito)
numero_sacado, tipo_resultado = dados_juego.d20()
print(f"🎲 Sacaste un {numero_sacado} en el D20. Tipo de resultado: {tipo_resultado}")

# 2. Evaluamos el resultado en base a lo que dictaminó el D20
if tipo_resultado == "CRITICO":
    # Si es crítico, el daño de tu espada (D8) se duplica o se maximiza
    daño = dados_juego.d8() + 8 
    print(f"💥 ¡GOLPE CRÍTICO! Haces {daño} de daño al enemigo.")
    
elif tipo_resultado == "NORMAL" and numero_sacado >= 10: # Suponiendo dificultad 10
    # Ataque normal exitoso
    daño = dados_juego.d8()
    print(f"⚔️ Logras golpear al enemigo. Daño infligido: {daño}")
    
else:
    # El ataque falló. El enemigo contraataca y te aplica un efecto con el D10
    efecto = dados_juego.d10()
    print(f"❌ Fallaste el ataque. El enemigo te golpea y activa el efecto número {efecto} en ti.")