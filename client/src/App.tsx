import { useState, useEffect } from "react";
import { ChatInterface } from "./components/ChatInterface";
import { Sidebar } from "./components/Sidebar";

function App() {
  const [sessionId, setSessionId] = useState<string>(() => {
    return localStorage.getItem("chat_session_id") || `session_${Date.now()}`;
  });
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  useEffect(() => {
    localStorage.setItem("chat_session_id", sessionId);
  }, [sessionId]);

  const handleSessionSelect = (id: string) => {
    setSessionId(id);
  };

  const handleNewSession = () => {
    const newId = `session_${Date.now()}`;
    setSessionId(newId);
  };

  return (
    <div className="flex h-screen bg-base-200 text-base-content overflow-hidden font-sans">
      <Sidebar
        isOpen={isSidebarOpen}
        currentSessionId={sessionId}
        onSessionSelect={handleSessionSelect}
        onNewSession={handleNewSession}
        onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
      />
      <main className="flex-1 flex flex-col h-full relative">
        <ChatInterface sessionId={sessionId} />
      </main>
    </div>
  );
}

export default App;
