import { useState, useEffect, useCallback } from "react";
import type { MouseEvent } from "react";
import { chatRepository } from "../repositories/ChatRepository";
import {
  MessageSquare,
  Plus,
  Trash2,
  Menu,
  X,
  AlertTriangle,
} from "lucide-react";

interface SidebarProps {
  isOpen: boolean;
  currentSessionId: string;
  onSessionSelect: (id: string) => void;
  onNewSession: () => void;
  onToggle: () => void;
}

export function Sidebar({
  isOpen,
  currentSessionId,
  onSessionSelect,
  onNewSession,
  onToggle,
}: SidebarProps) {
  const [sessions, setSessions] = useState<string[]>([]);
  const [sessionToDelete, setSessionToDelete] = useState<string | null>(null);

  const loadSessions = useCallback(async () => {
    try {
      const data = await chatRepository.getSessions();
      setSessions(data.sessions);
    } catch (error) {
      console.error("Failed to load sessions", error);
    }
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadSessions(); // Initial load is intentional
    // Poll for sessions every 10 seconds to keep in sync
    const interval = setInterval(loadSessions, 10000);
    return () => clearInterval(interval);
  }, [loadSessions]);

  const handleDeleteClick = (e: MouseEvent, id: string) => {
    e.stopPropagation();
    setSessionToDelete(id);
  };
  const handleConfirmDelete = async () => {
    if (!sessionToDelete) return;

    try {
      await chatRepository.deleteSession(sessionToDelete);
      await loadSessions();
      if (currentSessionId === sessionToDelete) {
        onNewSession();
      }
      setSessionToDelete(null);
    } catch (error) {
      console.error("Failed to delete session", error);
    }
  };

  const handleCancelDelete = () => {
    setSessionToDelete(null);
  };
  return (
    <>
      {/* Mobile overlay */}
      <div
        className={`fixed inset-0 bg-black/50 z-20 lg:hidden transition-opacity ${
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        }`}
        onClick={onToggle}
      />

      {/* Sidebar */}
      <div
        className={`
        fixed lg:static inset-y-0 left-0 z-30
        w-64 bg-base-300 flex flex-col transition-transform duration-300 ease-in-out
        ${
          isOpen
            ? "translate-x-0"
            : "-translate-x-full lg:w-0 lg:-translate-x-0 lg:overflow-hidden"
        }
      `}
      >
        <div className="p-4 flex items-center justify-between border-b border-base-100">
          <h1 className="font-bold text-xl flex items-center ">
            <span className="text-primary">K</span> -Tienda Chatbot
          </h1>
          <button
            onClick={onToggle}
            className="lg:hidden btn btn-ghost btn-sm btn-square"
          >
            <X size={20} />
          </button>
        </div>

        <div className="p-4">
          <button
            onClick={onNewSession}
            className="btn btn-primary w-full gap-2 shadow-lg"
          >
            <Plus size={18} />
            Nueva Conversación
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1">
          {sessions.map((session) => (
            <div
              key={session}
              onClick={() => onSessionSelect(session)}
              className={`
                group flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all
                ${
                  currentSessionId === session
                    ? "bg-base-100 shadow-sm"
                    : "hover:bg-base-100/50"
                }
              `}
            >
              <div className="flex items-center gap-3 overflow-hidden">
                <MessageSquare
                  size={18}
                  className={
                    currentSessionId === session
                      ? "text-primary"
                      : "text-base-content/50"
                  }
                />
                <span className="truncate text-sm font-medium">
                  {session.replace("session_", "Conversación ")}
                </span>
              </div>
              <button
                onClick={(e) => handleDeleteClick(e, session)}
                className="btn btn-ghost btn-xs btn-square opacity-0 group-hover:opacity-100 transition-opacity text-error"
              >
                <Trash2 size={14} />
              </button>
            </div>
          ))}

          {sessions.length === 0 && (
            <div className="text-center py-10 text-base-content/50 text-sm">
              No hay conversaciones activas
            </div>
          )}
        </div>

        <div className="p-4 border-t border-base-100 text-xs text-center text-base-content/50">
          Desarrollado con Gemini 2.5
        </div>
      </div>

      {/* Toggle button for desktop when closed */}
      {!isOpen && (
        <button
          onClick={onToggle}
          className="absolute top-4 left-4 z-10 btn btn-circle btn-ghost bg-base-100 shadow-md hidden lg:flex"
        >
          <Menu size={20} />
        </button>
      )}
      {/* Delete Confirmation Modal - DaisyUI */}
      <input
        type="checkbox"
        id="delete_modal"
        className="modal-toggle"
        checked={sessionToDelete !== null}
        onChange={() => {}}
      />
      <div className="modal modal-bottom sm:modal-middle">
        <div className="modal-box">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-full bg-error/10 flex items-center justify-center">
              <AlertTriangle className="text-error" size={24} />
            </div>
            <h3 className="font-bold text-lg">Eliminar Conversación</h3>
          </div>

          <p className="py-4 text-base-content/80">
            ¿Estás seguro de que quieres eliminar esta conversación?
            <br />
            <span className="font-semibold text-base-content">
              {sessionToDelete?.replace("session_", "Conversación ")}
            </span>
          </p>

          <div className="modal-action">
            <button onClick={handleCancelDelete} className="btn btn-ghost">
              Cancelar
            </button>
            <button onClick={handleConfirmDelete} className="btn btn-error">
              <Trash2 size={16} />
              Eliminar
            </button>
          </div>
        </div>
        <label
          className="modal-backdrop"
          htmlFor="delete_modal"
          onClick={handleCancelDelete}
        >
          Close
        </label>
      </div>
    </>
  );
}
