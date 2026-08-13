import React, { useState, useEffect } from 'react';
import { Sparkles, Gamepad2, Zap, Terminal, CheckCircle } from 'lucide-react';
import { PipelineVisualizer } from './components/PipelineVisualizer';
import { GddApprovalModal } from './components/GddApprovalModal';
import { GamePreview } from './components/GamePreview';
import { CodeViewer } from './components/CodeViewer';
import { GameGallery } from './components/GameGallery';

const QUICK_TOPICS = [
  "Fractions & Decimals",
  "Photosynthesis & Plant Biology",
  "Pythagorean Theorem",
  "Cybersecurity Basics",
  "Solar System & Gravity"
];

export default function App() {
  const [topicInput, setTopicInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [status, setStatus] = useState("idle"); // idle, running, hitl_pending, completed, failed
  const [logs, setLogs] = useState([]);
  const [gdd, setGdd] = useState(null);
  const [hitlPending, setHitlPending] = useState(false);
  const [outputUrl, setOutputUrl] = useState(null);
  const [generatedCode, setGeneratedCode] = useState(null);
  const [ws, setWs] = useState(null);

  const startGeneration = async (topicToUse) => {
    const topic = topicToUse || topicInput;
    if (!topic.trim()) return;

    setLogs([]);
    setGdd(null);
    setHitlPending(false);
    setOutputUrl(null);
    setGeneratedCode(null);
    setStatus("running");

    try {
      const res = await fetch("http://localhost:8000/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic })
      });

      if (!res.ok) throw new Error("Failed to initialize session");
      const data = await res.json();
      setSessionId(data.session_id);

      // Connect WebSocket
      const websocket = new WebSocket(`ws://localhost:8000/ws/pipeline/${data.session_id}`);
      
      websocket.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.type === "state_update") {
          if (msg.logs) setLogs(msg.logs);
          if (msg.gdd) setGdd(msg.gdd);
          if (msg.output_url) setOutputUrl(msg.output_url);
        } else if (msg.type === "hitl_required") {
          setHitlPending(true);
          setStatus("hitl_pending");
          if (msg.gdd) setGdd(msg.gdd);
        } else if (msg.type === "generation_completed") {
          setStatus("completed");
          setHitlPending(false);
          if (msg.output_url) setOutputUrl(msg.output_url);
        } else if (msg.type === "error") {
          setStatus("failed");
          console.error("Pipeline error:", msg.message);
        }
      };

      setWs(websocket);
    } catch (err) {
      console.error(err);
      setStatus("failed");
    }
  };

  const handleHitlResume = async (action, feedback = "") => {
    if (!sessionId) return;
    setHitlPending(false);
    setStatus("running");

    try {
      await fetch("http://localhost:8000/api/hitl/resume", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          action,
          feedback
        })
      });
    } catch (err) {
      console.error("Error resuming HITL:", err);
    }
  };

  return (
    <div style={{ maxWidth: '1240px', margin: '0 auto', padding: '30px 20px' }}>
      {/* Header Banner */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '36px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
            <Gamepad2 style={{ width: '32px', height: '32px', color: '#38bdf8' }} />
            <h1 style={{ fontSize: '1.8rem', fontWeight: 800, background: 'linear-gradient(135deg, #38bdf8, #c084fc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              AI Educational Game Generator
            </h1>
          </div>
          <p style={{ fontSize: '0.9rem', color: '#94a3b8' }}>
            LangGraph Multi-Agent Architecture | 100% Local Intelligence & Offline Procedural Graphics
          </p>
        </div>

        <div style={{ background: 'rgba(56, 189, 248, 0.1)', border: '1px solid rgba(56, 189, 248, 0.3)', borderRadius: '20px', padding: '6px 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Zap style={{ width: '16px', height: '16px', color: '#38bdf8' }} />
          <span style={{ fontSize: '0.8rem', color: '#38bdf8', fontWeight: 600 }}>Ollama: gemma4:latest</span>
        </div>
      </header>

      {/* Hero Topic Generator Input */}
      <div className="glass-panel" style={{ padding: '30px', marginBottom: '32px' }}>
        <h2 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '14px', color: '#f8fafc' }}>
          What Educational Topic should we turn into a game?
        </h2>

        <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
          <input
            type="text"
            value={topicInput}
            onChange={(e) => setTopicInput(e.target.value)}
            placeholder="e.g. Chemical Bonding, Fractions, Photosynthesis, Ancient Rome..."
            style={{
              flex: 1,
              background: '#090d16',
              border: '1px solid rgba(255, 255, 255, 0.15)',
              borderRadius: '12px',
              padding: '14px 18px',
              color: '#ffffff',
              fontSize: '0.95rem',
              outline: 'none'
            }}
            onKeyDown={(e) => e.key === 'Enter' && startGeneration()}
          />
          <button
            onClick={() => startGeneration()}
            disabled={status === 'running'}
            className="glow-btn-primary"
            style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
          >
            <Sparkles style={{ width: '18px', height: '18px' }} />
            {status === 'running' ? 'Agents Generating...' : 'Generate Game'}
          </button>
        </div>

        {/* Quick Suggestion Pills */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600 }}>Quick Topics:</span>
          {QUICK_TOPICS.map((t, idx) => (
            <button
              key={idx}
              onClick={() => {
                setTopicInput(t);
                startGeneration(t);
              }}
              style={{
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '16px',
                padding: '4px 12px',
                color: '#cbd5e1',
                fontSize: '0.75rem',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Multi-Agent Orchestration Visualizer */}
      {status !== 'idle' && (
        <PipelineVisualizer logs={logs} currentStatus={status} hitlPending={hitlPending} />
      )}

      {/* HITL Breakpoint Modal */}
      {hitlPending && (
        <GddApprovalModal
          gdd={gdd}
          onApprove={() => handleHitlResume('approved')}
          onReject={(feedback) => handleHitlResume('rejected', feedback)}
        />
      )}

      {/* Live Phaser Game Sandbox Preview */}
      {outputUrl && (
        <GamePreview outputUrl={outputUrl} gameTitle={gdd?.game_title} />
      )}

      {/* Code Inspector */}
      {generatedCode && (
        <CodeViewer code={generatedCode} />
      )}

      {/* Saved Games Showcase */}
      <GameGallery />
    </div>
  );
}
