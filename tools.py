# tools.py
"""
Herramientas (Tools) para el agente de soporte
"""

from database import PRODUCTOS, CATEGORIAS, PEDIDOS, INFO_PLATAFORMA
from typing import Dict, Any

# Definición de las herramientas para Claude
TOOLS = [
    {
        "name": "consultar_stock",
        "description": "Consulta el stock disponible de un producto específico en un talle determinado. Retorna la cantidad disponible o un error si el producto o talle no existe.",
        "input_schema": {
            "type": "object",
            "properties": {
                "producto": {
                    "type": "string",
                    "description": "Nombre del producto a consultar. Opciones: 'remera', 'pantalon', 'zapatillas', 'campera', 'gorra'"
                },
                "talle": {
                    "type": "string",
                    "description": "Talle del producto. Los talles varían según el producto (ej: S, M, L, XL para ropa; números para zapatillas)"
                }
            },
            "required": ["producto", "talle"]
        }
    },
    {
        "name": "listar_productos",
        "description": "Lista todos los productos disponibles en la tienda con sus talles y precios. Útil para que el cliente vea qué hay disponible.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "consultar_categorias",
        "description": "Muestra todas las categorías de productos disponibles en la plataforma (ej: Ropa, Calzado, Accesorios).",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "rastrear_pedido",
        "description": "Rastrea el estado de un pedido usando su ID de orden. Retorna información detallada sobre el estado del envío, productos y fechas.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id_orden": {
                    "type": "string",
                    "description": "ID de la orden a rastrear (formato: ORD-XXX)"
                }
            },
            "required": ["id_orden"]
        }
    },
    {
        "name": "explicar_politica_devolucion",
        "description": "Explica la política completa de devoluciones y cambios de la tienda.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "consultar_info_plataforma",
        "description": "Consulta información general sobre la plataforma. Tipos disponibles: 'metodos_pago', 'financiacion', 'envios', 'contacto', 'politica_devolucion'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tipo_info": {
                    "type": "string",
                    "description": "Tipo de información a consultar: 'metodos_pago', 'financiacion', 'envios', 'contacto', 'politica_devolucion'"
                }
            },
            "required": ["tipo_info"]
        }
    },
    {
        "name": "obtener_historial_compras",
        "description": "Obtiene el historial completo de compras de un cliente usando su email. Muestra todos los pedidos anteriores con sus estados, productos y fechas.",
        "input_schema": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "Email del cliente para buscar su historial de compras"
                }
            },
            "required": ["email"]
        }
    }
]


# Implementación de las herramientas
def consultar_stock(producto: str, talle: str) -> Dict[str, Any]:
    """Consulta el stock de un producto en un talle específico"""
    try:
        producto = producto.lower()
        
        if producto not in PRODUCTOS:
            return {
                "error": True,
                "mensaje": f"Producto '{producto}' no encontrado. Productos disponibles: {', '.join(PRODUCTOS.keys())}"
            }
        
        prod_info = PRODUCTOS[producto]
        
        if talle not in prod_info["talles"]:
            talles_disponibles = ", ".join(prod_info["talles"].keys())
            return {
                "error": True,
                "mensaje": f"Talle '{talle}' no disponible para {prod_info['nombre']}. Talles disponibles: {talles_disponibles}"
            }
        
        stock = prod_info["talles"][talle]
        
        return {
            "error": False,
            "producto": prod_info["nombre"],
            "talle": talle,
            "stock": stock,
            "precio": prod_info["precio"],
            "disponible": stock > 0
        }
    except Exception as e:
        return {
            "error": True,
            "mensaje": f"Error al consultar stock: {str(e)}"
        }


def listar_productos() -> Dict[str, Any]:
    """Lista todos los productos disponibles"""
    try:
        productos_lista = []
        
        for key, prod in PRODUCTOS.items():
            talles_stock = {talle: cantidad for talle, cantidad in prod["talles"].items() if cantidad > 0}
            
            productos_lista.append({
                "id": key,
                "nombre": prod["nombre"],
                "categoria": prod["categoria"],
                "precio": prod["precio"],
                "talles_disponibles": list(talles_stock.keys())
            })
        
        return {
            "error": False,
            "productos": productos_lista,
            "total": len(productos_lista)
        }
    except Exception as e:
        return {
            "error": True,
            "mensaje": f"Error al listar productos: {str(e)}"
        }


def consultar_categorias() -> Dict[str, Any]:
    """Consulta las categorías disponibles"""
    try:
        return {
            "error": False,
            "categorias": CATEGORIAS,
            "descripcion": "Estas son todas las categorías de productos disponibles en nuestra tienda"
        }
    except Exception as e:
        return {
            "error": True,
            "mensaje": f"Error al consultar categorías: {str(e)}"
        }


def rastrear_pedido(id_orden: str) -> Dict[str, Any]:
    """Rastrea el estado de un pedido"""
    try:
        id_orden = id_orden.upper()
        
        if id_orden not in PEDIDOS:
            return {
                "error": True,
                "mensaje": f"Orden '{id_orden}' no encontrada. Verifica que el ID sea correcto."
            }
        
        pedido = PEDIDOS[id_orden]
        
        return {
            "error": False,
            **pedido
        }
    except Exception as e:
        return {
            "error": True,
            "mensaje": f"Error al rastrear pedido: {str(e)}"
        }


def explicar_politica_devolucion() -> Dict[str, Any]:
    """Explica la política de devolución"""
    try:
        return {
            "error": False,
            "politica": INFO_PLATAFORMA["politica_devolucion"]
        }
    except Exception as e:
        return {
            "error": True,
            "mensaje": f"Error al obtener política de devolución: {str(e)}"
        }


def consultar_info_plataforma(tipo_info: str) -> Dict[str, Any]:
    """Consulta información general de la plataforma"""
    try:
        if tipo_info not in INFO_PLATAFORMA:
            return {
                "error": True,
                "mensaje": f"Tipo de información '{tipo_info}' no disponible. Tipos válidos: {', '.join(INFO_PLATAFORMA.keys())}"
            }

        return {
            "error": False,
            "tipo": tipo_info,
            "informacion": INFO_PLATAFORMA[tipo_info]
        }
    except Exception as e:
        return {
            "error": True,
            "mensaje": f"Error al consultar información: {str(e)}"
        }


def obtener_historial_compras(email: str) -> Dict[str, Any]:
    """Obtiene el historial completo de compras de un cliente"""
    try:
        email = email.lower().strip()
        historial = []

        for pedido_id, pedido in PEDIDOS.items():
            if pedido.get("email", "").lower() == email:
                pedido_info = {
                    "id_orden": pedido["id"],
                    "fecha": pedido["fecha"],
                    "estado": pedido["estado"],
                    "productos": pedido["productos"],
                    "total_productos": len(pedido["productos"])
                }

                if "direccion" in pedido:
                    pedido_info["direccion"] = pedido["direccion"]

                if "tracking" in pedido:
                    pedido_info["tracking_info"] = pedido["tracking"]

                if "fecha_entrega" in pedido:
                    pedido_info["fecha_entrega"] = pedido["fecha_entrega"]

                historial.append(pedido_info)

        if not historial:
            return {
                "error": True,
                "mensaje": f"No se encontraron compras para el email: {email}. Verifica que el email sea correcto o que hayas realizado compras con nosotros."
            }

        # Ordenamos por fecha (más reciente primero)
        historial.sort(key=lambda x: x["fecha"], reverse=True)

        return {
            "error": False,
            "email": email,
            "total_pedidos": len(historial),
            "historial": historial,
            "resumen": f"Se encontraron {len(historial)} pedido(s) para este cliente"
        }
    except Exception as e:
        return {
            "error": True,
            "mensaje": f"Error al obtener historial de compras: {str(e)}"
        }


# Mapeo de nombres de herramientas a funciones
TOOL_FUNCTIONS = {
    "consultar_stock": consultar_stock,
    "listar_productos": listar_productos,
    "consultar_categorias": consultar_categorias,
    "rastrear_pedido": rastrear_pedido,
    "explicar_politica_devolucion": explicar_politica_devolucion,
    "consultar_info_plataforma": consultar_info_plataforma,
    "obtener_historial_compras": obtener_historial_compras
}


def ejecutar_herramienta(nombre: str, argumentos: Dict[str, Any]) -> Dict[str, Any]:
    """Ejecuta una herramienta con los argumentos proporcionados"""
    if nombre not in TOOL_FUNCTIONS:
        return {
            "error": True,
            "mensaje": f"Herramienta '{nombre}' no encontrada"
        }
    
    func = TOOL_FUNCTIONS[nombre]
    return func(**argumentos)