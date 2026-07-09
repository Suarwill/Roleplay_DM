import json
import os
from .efectos import CATALOGO_EFECTOS

class Item:
    def __init__(self, id_item: str, nombre: str, tipo: str, efecto_id: str, descripcion: str):
        self.id_item = id_item
        self.nombre = nombre
        self.tipo = tipo
        self.efecto_id = efecto_id
        self.descripcion = descripcion

    def ejecutar_uso(self, usuario, objetivo) -> str:
        if self.efecto_id not in CATALOGO_EFECTOS:
            return f"❌ El ítem '{self.nombre}' intenta usar un efecto que no existe ({self.efecto_id})."
            
        efecto_objeto = CATALOGO_EFECTOS[self.efecto_id]
        
        cronica_narrativa = efecto_objeto.aplicar(usuario, objetivo)
        
        return f"🎒 {usuario.nombre} utiliza {self.nombre}.\n{cronica_narrativa}"


def cargar_catalogo_items() -> dict[str, Item]:
    ruta_json = os.path.join(os.path.dirname(__file__), "items.json")
    with open(ruta_json, "r", encoding="utf-8") as f:
        datos = json.load(f)
        
    catalogo = {}
    for id_item, info in datos.items():
        catalogo[id_item] = Item(
            id_item=id_item,
            nombre=info["nombre"],
            tipo=info["tipo"],
            efecto_id=info["efecto_id"],
            descripcion=info["descripcion"]
        )
    return catalogo

CATALOGO_ITEMS = cargar_catalogo_items()