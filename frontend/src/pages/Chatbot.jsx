import React, { useEffect, useRef, useState } from "react";
import { chatStream, getChatHistory } from "@/lib/api";
import { PaperPlaneTilt, Sparkle } from "@phosphor-icons/react";

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const bottomRef = useRef();

  useEffect(() => { getChatHistory().then((d) => setMessages(d.messages || [])); }, []);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const send = async () => {
    const text = input.trim();
    if (!text || streaming) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: text }, { role: "assistant", content: "" }]);
    setStreaming(true);
    await chatStream(text, (delta) => {
      setMessages((m) => {
        const next = [...m];
        next[next.length - 1] = { ...next[next.length - 1], content: next[next.length - 1].content + delta };
        return next;
      });
    }, () => setStreaming(false));
  };

  const suggestions = [
    "What should I learn after React?",
    "Compare ML Engineer vs Data Scientist",
    "How do I prepare for an LLM interview?",
    "Suggest a 3-month plan to switch into AI",
  ];

  return (
    <div className="flex flex-col h-[calc(100vh-160px)]" data-testid="chat-root">
      <div className="mb-6">
        <div className="overline mb-3">AI CAREER MENTOR</div>
        <h1 className="font-display text-3xl lg:text-4xl font-black tracking-display">
          Ask anything. Ship faster.
        </h1>
      </div>

      <div className="flat-card flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 && (
          <div className="space-y-6">
            <div className="text-secondary text-sm">Try one of these to get started:</div>
            <div className="grid sm:grid-cols-2 gap-3">
              {suggestions.map((s) => (
                <button key={s} onClick={() => setInput(s)}
                  className="text-left border border-default p-4 hover:border-[var(--accent)] transition-colors text-sm"
                  data-testid={`suggestion-${s.slice(0, 20)}`}>
                  <Sparkle size={14} className="inline mr-2 text-[var(--accent)]" /> {s}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-3xl px-5 py-3 ${
              m.role === "user"
                ? "bg-accent-yellow text-black"
                : "border border-default bg-elevated"
            } whitespace-pre-wrap text-sm leading-relaxed`}>
              {m.content || (streaming && i === messages.length - 1 ? "•••" : "")}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="mt-4 flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Ask anything career-related..."
          className="flex-1 bg-elevated border border-default px-4 py-3 text-sm outline-none focus:border-[var(--accent)]"
          data-testid="chat-input"
          disabled={streaming}
        />
        <button onClick={send} disabled={streaming} className="btn-yellow" data-testid="chat-send-button">
          <PaperPlaneTilt size={16} weight="bold" /> Send
        </button>
      </div>
    </div>
  );
}
