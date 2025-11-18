# 🛍️ Chatbot de E-commerce mcp

Sistema de chatbot para soporte al cliente usando **FastAPI**, **Google Gemini** y el patrón **MCP (Model Context Protocol)**.

## 🚀 Instalación

### 1. Instalar dependencias

 Ejecuta
```bash
uv sync
```

### 2. Configurar API Key

Crea un archivo `.env` con tu API key de Google:
```
GOOGLE_API_KEY=tu_api_key_aqui
```

**Obtener API Key:** https://makersuite.google.com/app/apikey

### 3. Iniciar el servidor

```bash
uvicorn main:app --reload
```

El servidor estará en: `http://localhost:8000`

---

## 📡 Usar con Postman

### 1. **Enviar mensaje al chatbot**

**POST** `http://localhost:8000/chat`

**Body (JSON):**
```json
{
  "session_id": "usuario123",
  "message": "¿Tienen zapatillas talle 40?"
}
```

**Respuesta:**
```json
{
  "session_id": "usuario123",
  "response": "¡Sí! Tenemos 12 unidades de Zapatillas Deportivas en talle 40 disponibles por $15,000...",
  "tool_calls": [
    {
      "tool": "consultar_stock",
      "input": {"producto": "zapatillas", "talle": "40"},
      "result": {"stock": 12, "precio": 15000, "disponible": true}
    }
  ]
}
```

---

### 2. **Ver herramientas disponibles**

**GET** `http://localhost:8000/tools`

---

### 3. **Ver sesiones activas**

**GET** `http://localhost:8000/sessions`

---

### 4. **Limpiar una sesión**

**POST** `http://localhost:8000/clear`

**Body (JSON):**
```json
{
  "session_id": "usuario123"
}
```

---

## 🎯 Herramientas Disponibles

| Herramienta | Qué hace |
|------------|----------|
| `consultar_stock` | Verifica disponibilidad de productos |
| `listar_productos` | Muestra todo el catálogo |
| `consultar_categorias` | Lista categorías disponibles |
| `rastrear_pedido` | Consulta estado de envíos |
| `explicar_politica_devolucion` | Info sobre devoluciones |
| `consultar_info_plataforma` | Info de pagos, envíos, contacto |

---

## 💬 Ejemplos de Mensajes

Prueba estos mensajes en Postman:

- "¿Hay remeras talle M?"
- "¿Qué productos tienen?"
- "¿Dónde está mi pedido ORD-002?"
- "¿Qué métodos de pago aceptan?"
- "Quiero devolver un producto"

---


## 📁 Estructura del Proyecto

```
📁 proyecto/
├── main.py              # API principal
├── tools.py             # Herramientas MCP
├── database.py          # Datos simulados
├── prompts.py           # Instrucciones del bot
├── .env                 # API key (no subir a git)
```

---

## 🎓 Cómo Funciona

1. **Usuario envía mensaje** → FastAPI recibe el request
2. **Gemini analiza** → Decide si necesita usar herramientas
3. **Sistema ejecuta herramientas** → Consulta stock, pedidos, etc.
4. **Gemini genera respuesta** → Con los datos obtenidos
5. **Usuario recibe respuesta** → Natural y completa

---

**Eso es todo.** Instala, configura la API key, y prueba en Postman. 🚀