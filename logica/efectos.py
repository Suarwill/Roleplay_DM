import json
import os

class Efecto:
    def __init__(self, id_efecto: str, nombre: str, tipo: str, valor: int, descripcion: str, extra: dict = None):
        self.id_efecto = id_efecto
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.descripcion = descripcion
        self.extra = extra if extra else {}

    def aplicar(self, usuario, objetivo) -> str:
        """Aplica la matemática del efecto directamente sobre el objetivo."""
        if self.tipo == "CURACION":
            objetivo.vida_actual = min(objetivo.vida_max, objetivo.vida_actual + self.valor)
            return f"✨ El efecto '{self.nombre}' sana {self.valor} HP a {objetivo.nombre}. (Vida: {objetivo.vida_actual}/{objetivo.vida_max})"
            
        elif self.tipo == "DAÑO":
            resultado_daño = objetivo.recibir_daño(self.valor)
            mensaje = resultado_daño[0] if isinstance(resultado_daño, tuple) else resultado_daño
            return f"💥 El efecto '{self.nombre}' golpea a {objetivo.nombre}.\n   ↳ {mensaje}"
            
        elif self.tipo == "ESTADO_ALTERADO":
            estado = self.extra.get("estado", "AFECTADO")
            turnos = self.extra.get("duracion_turnos", 1)
            return f"❄️ {objetivo.nombre} entra en estado [{estado}] por {turnos} turnos."
            
        return f"❓ El efecto '{self.nombre}' se disipa sin hacer nada."


def cargar_catalogo_efectos() -> dict[str, Efecto]:
    ruta_json = os.path.join(os.path.dirname(__file__), "efectos.json")
    with open(ruta_json, "r", encoding="utf-8") as f:
        datos = json.load(f)
        
    catalogo = {}
    for id_efecto, info in datos.items():
        extra = {k: v for k, v in info.items() if k not in ["nombre", "tipo", "valor", "descripcion"]}
        
        catalogo[id_efecto] = Efecto(
            id_efecto=id_efecto,
            nombre=info["nombre"],
            tipo=info["tipo"],
            valor=info.get("valor", 0),
            descripcion=info["descripcion"],
            extra=extra
        )
    return catalogo

CATALOGO_EFECTOS = cargar_catalogo_efectos()