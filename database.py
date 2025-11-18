# database.py
"""
Base de datos simulada para el e-commerce
"""

# Catálogo de productos
PRODUCTOS = {
    "remera": {
        "nombre": "Remera Básica",
        "categoria": "Ropa",
        "talles": {
            "S": 15,
            "M": 20,
            "L": 10,
            "XL": 5
        },
        "precio": 3500
    },
    "pantalon": {
        "nombre": "Pantalón Jean",
        "categoria": "Ropa",
        "talles": {
            "28": 8,
            "30": 12,
            "32": 15,
            "34": 10,
            "36": 6
        },
        "precio": 8500
    },
    "zapatillas": {
        "nombre": "Zapatillas Deportivas",
        "categoria": "Calzado",
        "talles": {
            "38": 5,
            "39": 8,
            "40": 12,
            "41": 10,
            "42": 7,
            "43": 4
        },
        "precio": 15000
    },
    "campera": {
        "nombre": "Campera de Abrigo",
        "categoria": "Ropa",
        "talles": {
            "S": 6,
            "M": 10,
            "L": 8,
            "XL": 4
        },
        "precio": 12000
    },
    "gorra": {
        "nombre": "Gorra Deportiva",
        "categoria": "Accesorios",
        "talles": {
            "Unico": 25
        },
        "precio": 2500
    }
}

# Categorías disponibles
CATEGORIAS = ["Ropa", "Calzado", "Accesorios"]

# Pedidos simulados
PEDIDOS = {
    "ORD-001": {
        "id": "ORD-001",
        "cliente": "Juan Pérez",
        "productos": ["Remera Básica (M)", "Pantalón Jean (32)"],
        "estado": "En preparación",
        "fecha": "2024-11-15",
        "direccion": "Av. Corrientes 1234, CABA"
    },
    "ORD-002": {
        "id": "ORD-002",
        "cliente": "María García",
        "productos": ["Zapatillas Deportivas (40)"],
        "estado": "En camino",
        "fecha": "2024-11-14",
        "direccion": "Calle Falsa 456, Rosario",
        "tracking": "Llegará mañana antes de las 18hs"
    },
    "ORD-003": {
        "id": "ORD-003",
        "cliente": "Carlos López",
        "productos": ["Campera de Abrigo (L)", "Gorra Deportiva"],
        "estado": "Entregado",
        "fecha": "2024-11-10",
        "fecha_entrega": "2024-11-13"
    }
}

# Información de la plataforma
INFO_PLATAFORMA = {
    "politica_devolucion": """
    POLÍTICA DE DEVOLUCIÓN:
    - Tienes 30 días corridos desde la recepción del producto para realizar cambios o devoluciones.
    - El producto debe estar sin uso, con etiquetas y en su empaque original.
    - El costo del envío de devolución corre por cuenta del cliente, excepto si el producto tiene defectos de fábrica.
    - El reembolso se procesa en 5-10 días hábiles una vez recibido el producto.
    - Para iniciar una devolución, contacta a soporte@tienda.com con tu número de orden.
    """,
    
    "metodos_pago": """
    MÉTODOS DE PAGO ACEPTADOS:
    - Tarjetas de crédito: Visa, Mastercard, American Express
    - Tarjetas de débito: Todas las tarjetas de débito
    - Mercado Pago
    - Transferencia bancaria
    - Efectivo contra entrega (solo CABA y GBA)
    """,
    
    "financiacion": """
    OPCIONES DE FINANCIACIÓN:
    - 3 cuotas sin interés con tarjetas de crédito seleccionadas
    - 6 cuotas con interés (15% anual)
    - 12 cuotas con interés (25% anual)
    - Plan Ahora 12 y Ahora 18 disponibles
    - Consulta disponibilidad según tu banco emisor
    """,
    
    "envios": """
    INFORMACIÓN DE ENVÍOS:
    - Envío gratis en compras superiores a $50,000
    - CABA y GBA: 24-48 horas hábiles ($2,500)
    - Interior del país: 3-7 días hábiles ($3,500)
    - Seguimiento en tiempo real disponible
    - Retiro gratis en nuestro local (Av. Santa Fe 2020, CABA)
    """,
    
    "contacto": """
    CONTACTO Y SOPORTE:
    - Email: soporte@tienda.com
    - WhatsApp: +54 9 11 1234-5678
    - Teléfono: 0800-555-TIENDA
    - Horario de atención: Lunes a Viernes 9-18hs, Sábados 10-14hs
    """
}