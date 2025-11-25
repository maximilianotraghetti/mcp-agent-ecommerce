import axios from "axios";

const API_URL = "http://localhost:8000";

export interface ChatRequest {
  session_id: string;
  message: string;
}

export interface ToolCall {
  tool: string;
  input: Record<string, unknown>;
  result: Record<string, unknown>;
}

export interface ChatResponse {
  session_id: string;
  response: string;
  tool_calls?: ToolCall[];
}

export interface Session {
  id: string;
  name: string;
}

export interface SessionListResponse {
  sessions: Session[];
  count: number;
}

export interface Tool {
  [key: string]: unknown;
}

export interface ToolsResponse {
  tools: Tool[];
  gemini_format: Tool[];
  count: number;
}

export const chatRepository = {
  async sendMessage(
    session_id: string,
    message: string
  ): Promise<ChatResponse> {
    const response = await axios.post<ChatResponse>(`${API_URL}/chat`, {
      session_id,
      message,
    });
    return response.data;
  },

  async getSessions(): Promise<SessionListResponse> {
    const response = await axios.get<SessionListResponse>(
      `${API_URL}/sessions`
    );
    return response.data;
  },

  async clearSession(session_id: string): Promise<void> {
    await axios.post(`${API_URL}/clear`, { session_id });
  },

  async deleteSession(session_id: string): Promise<void> {
    await axios.delete(`${API_URL}/sessions/${session_id}`);
  },

  async getTools(): Promise<ToolsResponse> {
    const response = await axios.get<ToolsResponse>(`${API_URL}/tools`);
    return response.data;
  },

  async getSessionHistory(session_id: string): Promise<{
    session_id: string;
    history: Array<{ role: string; content: string }>;
    exists: boolean;
  }> {
    const response = await axios.get(
      `${API_URL}/sessions/${session_id}/history`
    );
    return response.data;
  },
};
