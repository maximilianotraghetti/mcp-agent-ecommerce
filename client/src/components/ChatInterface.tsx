import { useState, useEffect, useRef } from "react";
import { chatRepository, type ToolCall } from "../repositories/ChatRepository";
import { SendHorizonal, Loader2, Bot, User, Terminal } from "lucide-react";
import ReactMarkdown from "react-markdown";

interface Message {
  role: "user" | "assistant";
  content: string;
  toolCalls?: ToolCall[];
}

interface ChatInterfaceProps {
  sessionId: string;
}

export function ChatInterface({ sessionId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMessages([]);
  }, [sessionId]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");

    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await chatRepository.sendMessage(sessionId, userMessage);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.response,
          toolCalls: response.tool_calls,
        },
      ]);
    } catch (error) {
      console.error("Failed to send message", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Lo siento, algo salió mal. Por favor, intenta de nuevo.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-base-100">
      {/* Header */}
      <div className="navbar bg-base-100 border-b border-base-200 px-4 lg:px-8">
        <div className="flex-1">
          <h2 className="text-lg font-bold">
            {sessionId.replace("session_", "Conversación ")}
          </h2>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 lg:p-8 space-y-6">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-base-content/80 space-y-4">
            <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center text-primary">
              <Bot size={32} />
            </div>
            <h3 className="text-xl font-semibold">
              ¡Bienvenido a K-Tienda! 👋
            </h3>
            <p className="max-w-md text-center">
              Soy tu asistente virtual. Puedo ayudarte con consultas sobre
              stock, productos, seguimiento de pedidos y políticas de la tienda.
            </p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-4 ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {msg.role === "assistant" && (
                <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary shrink-0 mt-1">
                  <Bot size={18} />
                </div>
              )}

              <div className={`flex flex-col gap-2 max-w-[80%]`}>
                <div
                  className={`
                  p-4 rounded-2xl shadow-sm
                  ${
                    msg.role === "user"
                      ? "bg-primary text-primary-content rounded-tr-none"
                      : "bg-base-200 text-base-content rounded-tl-none"
                  }
                `}
                >
                  <div className="prose prose-sm max-w-none dark:prose-invert">
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  </div>
                </div>

                {/* Tool Calls Display */}
                {msg.toolCalls && msg.toolCalls.length > 0 && (
                  <div className="space-y-2">
                    {msg.toolCalls.map((tool, tIdx) => (
                      <div
                        key={tIdx}
                        className="collapse collapse-arrow bg-base-200/50 border border-base-300 rounded-lg"
                      >
                        <input type="checkbox" />
                        <div className="collapse-title text-xs font-mono flex items-center gap-2 py-2 min-h-0">
                          <Terminal size={14} className="text-secondary" />
                          <span className="font-bold text-secondary">
                            Herramienta usada:
                          </span>{" "}
                          {tool.tool}
                        </div>
                        <div className="collapse-content text-xs">
                          <div className="bg-base-300 p-2 rounded mt-2 overflow-x-auto">
                            <p className="font-bold text-base-content/70 mb-1">
                              Entrada:
                            </p>
                            <pre className="font-mono text-base-content/60">
                              {JSON.stringify(tool.input, null, 2)}
                            </pre>
                          </div>
                          <div className="bg-base-300 p-2 rounded mt-2 overflow-x-auto">
                            <p className="font-bold text-base-content/70 mb-1">
                              Resultado:
                            </p>
                            <pre className="font-mono text-success/80">
                              {JSON.stringify(tool.result, null, 2)}
                            </pre>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {msg.role === "user" && (
                <div className="w-8 h-8 rounded-full bg-base-300 flex items-center justify-center text-base-content shrink-0 mt-1">
                  <User size={18} />
                </div>
              )}
            </div>
          ))
        )}

        {isLoading && (
          <div className="flex gap-4 justify-start">
            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary shrink-0">
              <Bot size={18} />
            </div>
            <div className="bg-base-200 p-4 rounded-2xl rounded-tl-none flex items-center gap-2">
              <Loader2
                size={16}
                className="animate-spin text-base-content/50"
              />
              <span className="text-sm text-base-content/50">Pensando...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-base-100 border-t border-base-200">
        <form
          onSubmit={handleSubmit}
          className="max-w-4xl mx-auto flex gap-2 items-center"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe tu mensaje..."
            className="input input-bordered rounded-full flex-1 focus:outline-none focus:border-primary shadow-sm"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="btn btn-circle btn-primary"
          >
            <SendHorizonal size={16} />
          </button>
        </form>
        <div className="text-center mt-2">
          <p className="text-xs text-base-content/40">
            La IA puede cometer errores. Por favor, verifica la información
            importante.
          </p>
        </div>
      </div>
    </div>
  );
}
