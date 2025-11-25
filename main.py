# main.py - Versión para Gemini (Corregida)
"""
API FastAPI para el sistema de chat con MCP usando Gemini
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

from tools import TOOLS, ejecutar_herramienta
from prompts import SYSTEM_PROMPT

# Cargar variables de entorno
load_dotenv()

# Inicializar FastAPI
app = FastAPI(
    title="E-commerce MCP API (Gemini)",
    description="Sistema de chat con herramientas para soporte de e-commerce usando Gemini",
    version="1.0.0"
)

# ==================== CONFIGURAR CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Configurar Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# CAMBIO IMPORTANTE: Usar el nombre correcto del modelo
MODEL_NAME = "gemini-2.5-flash"  # ← Agregar -latest

# Almacenamiento en memoria de conversaciones (por sesión)
conversaciones: Dict[str, Any] = {}


# Convertir herramientas al formato de Gemini
def convertir_tools_a_gemini(tools):
    """Convierte las herramientas del formato Anthropic al formato Gemini"""
    gemini_tools = []
    
    for tool in tools:
        # Convertir el schema de input
        parameters = tool["input_schema"]["properties"]
        required = tool["input_schema"].get("required", [])
        
        # Construir el schema en formato Gemini
        gemini_parameters = {}
        for param_name, param_info in parameters.items():
            gemini_parameters[param_name] = {
                "type": param_info["type"].upper(),
                "description": param_info["description"]
            }
        
        gemini_tool = {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": {
                "type": "OBJECT",
                "properties": gemini_parameters,
                "required": required
            }
        }
        
        gemini_tools.append(gemini_tool)
    
    return gemini_tools


# Convertir tools
GEMINI_TOOLS = convertir_tools_a_gemini(TOOLS)


# Modelos Pydantic
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    tool_calls: Optional[List[Dict[str, Any]]] = None


class ClearSessionRequest(BaseModel):
    session_id: str


# Endpoints
@app.get("/")
def read_root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "E-commerce MCP API (Gemini)",
        "version": "1.0.0",
        "model": MODEL_NAME,
        "endpoints": {
            "POST /chat": "Enviar un mensaje al asistente",
            "POST /clear": "Limpiar una sesión de chat",
            "GET /sessions": "Listar sesiones activas",
            "GET /tools": "Listar herramientas disponibles"
        }
    }


@app.get("/tools")
def get_tools():
    """Retorna la lista de herramientas disponibles"""
    return {
        "tools": TOOLS,
        "gemini_format": GEMINI_TOOLS,
        "count": len(TOOLS)
    }


@app.get("/sessions")
def get_sessions():
    """Retorna las sesiones activas"""
    return {
        "sessions": list(conversaciones.keys()),
        "count": len(conversaciones)
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal de chat usando Gemini
    Procesa un mensaje del usuario y retorna la respuesta del asistente
    """
    try:
        session_id = request.session_id
        user_message = request.message
        
        # Inicializar conversación si no existe
        if session_id not in conversaciones:
            # Crear modelo con configuración - USAR MODEL_NAME
            model = genai.GenerativeModel(
                model_name=MODEL_NAME,  # ← Usar la constante con -latest
                tools=GEMINI_TOOLS,
                system_instruction=SYSTEM_PROMPT
            )
            # Iniciar chat
            conversaciones[session_id] = {
                "chat": model.start_chat(enable_automatic_function_calling=False),
                "history": []
            }
        
        chat = conversaciones[session_id]["chat"]
        history = conversaciones[session_id]["history"]
        
        # Agregar mensaje del usuario al historial
        history.append({
            "role": "user",
            "content": user_message
        })
        
        # Enviar mensaje a Gemini
        response = chat.send_message(user_message)
        
        tool_calls_info = []
        max_iterations = 10  # Prevenir loops infinitos
        iteration = 0
        
        # Procesar la respuesta y manejar llamadas a herramientas
        while response.candidates[0].content.parts[0].function_call and iteration < max_iterations:
            iteration += 1
            
            # Obtener la llamada a la función
            function_call = response.candidates[0].content.parts[0].function_call
            tool_name = function_call.name
            tool_args = dict(function_call.args)
            
            # Ejecutar la herramienta
            result = ejecutar_herramienta(tool_name, tool_args)
            
            # Guardar información para el cliente
            tool_calls_info.append({
                "tool": tool_name,
                "input": tool_args,
                "result": result
            })
            
            # Enviar el resultado de vuelta a Gemini
            response = chat.send_message(
                genai.protos.Content(
                    parts=[
                        genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=tool_name,
                                response={"result": result}
                            )
                        )
                    ]
                )
            )
        
        # Extraer texto de la respuesta final
        response_text = ""
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_text += part.text
        
        # Si no hay texto, usar un mensaje por defecto
        if not response_text:
            response_text = "Lo siento, no pude generar una respuesta adecuada."
        
        # Agregar respuesta al historial
        history.append({
            "role": "assistant",
            "content": response_text
        })
        
        return ChatResponse(
            session_id=session_id,
            response=response_text,
            tool_calls=tool_calls_info if tool_calls_info else None
        )
        
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.post("/clear")
def clear_session(request: ClearSessionRequest):
    """
    Limpia el historial de una sesión
    """
    session_id = request.session_id
    
    if session_id in conversaciones:
        del conversaciones[session_id]
        return {
            "message": f"Sesión {session_id} limpiada exitosamente",
            "success": True
        }
    else:
        return {
            "message": f"Sesión {session_id} no encontrada (creando nueva)",
            "success": True
        }


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    """
    Elimina una sesión específica
    """
    if session_id in conversaciones:
        del conversaciones[session_id]
        return {
            "message": f"Sesión {session_id} eliminada",
            "success": True
        }
    else:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")


# Ejecutar con: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)