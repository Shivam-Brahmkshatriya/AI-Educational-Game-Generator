import React from 'react';
import { Search, Cpu, CheckCircle2, ShieldAlert, Code2, TestTube2, AlertCircle, RefreshCw } from 'lucide-react';

const STAGES = [
  { id: 'researcher', name: 'Compound Research', icon: Search, desc: 'DuckDuckGo + Gemma fact extraction' },
  { id: 'design', name: 'Design Directorate', icon: Cpu, desc: 'Mechanic, Narrative & Edu sub-agents' },
  { id: 'master', name: 'Master GDD & Critic', icon: CheckCircle2, desc: 'Synthesis & quality verification' },
  { id: 'hitl', name: 'Human In The Loop', icon: ShieldAlert, desc: 'User GDD approval checkpoint' },
  { id: 'developer', name: 'Phaser Code Engine', icon: Code2, desc: 'Procedural graphics & Phaser JS author' },
  { id: 'qa', name: 'Playwright QA', icon: TestTube2, desc: 'Headless browser automated QA' },
];

export function PipelineVisualizer({ logs, currentStatus, hitlPending }) {
  // Determine current active index based on logs
  const getStageStatus = (stageId) => {
    if (!logs || logs.length === 0) return 'pending';
    
    const lastLog = logs[logs.length - 1];
    const agentName = (lastLog.agent || '').toLowerCase();
    
    if (stageId === 'researcher') {
      if (logs.some(l => l.agent === 'Researcher')) return 'completed';
      return 'active';
    }
    if (stageId === 'design') {
      if (logs.some(l => l.agent === 'Design Directorate')) return 'completed';
      if (logs.some(l => l.agent === 'Researcher')) return 'active';
      return 'pending';
    }
    if (stageId === 'master') {
      if (logs.some(l => l.agent === 'Critic')) return 'completed';
      if (logs.some(l => l.agent === 'Design Directorate')) return 'active';
      return 'pending';
    }
    if (stageId === 'hitl') {
      if (hitlPending) return 'active_hitl';
      if (logs.some(l => l.agent === 'HITL Gate' && l.message.includes('User action'))) return 'completed';
      if (logs.some(l => l.agent === 'Critic')) return 'active';
      return 'pending';
    }
    if (stageId === 'developer') {
      if (logs.some(l => l.agent === 'Lead Developer')) return 'completed';
      if (logs.some(l => l.agent === 'Asset Artist')) return 'active';
      return 'pending';
    }
    if (stageId === 'qa') {
      if (logs.some(l => l.agent === 'QA Tester')) return 'completed';
      if (logs.some(l => l.agent === 'Lead Developer')) return 'active';
      return 'pending';
    }
    return 'pending';
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
      <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <RefreshCw className={currentStatus === 'running' ? 'animate-spin' : ''} style={{ width: '18px', height: '18px', color: '#38bdf8' }} />
        Multi-Agent Orchestration Flow (Ollama Gemma 4)
      </h3>

      {/* Stage Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px', marginBottom: '20px' }}>
        {STAGES.map((stage) => {
          const Icon = stage.icon;
          const status = getStageStatus(stage.id);

          let borderColor = 'rgba(255, 255, 255, 0.08)';
          let iconColor = '#94a3b8';
          let bg = 'rgba(15, 23, 42, 0.4)';

          if (status === 'completed') {
            borderColor = 'rgba(74, 222, 128, 0.4)';
            iconColor = '#4ade80';
            bg = 'rgba(20, 83, 45, 0.2)';
          } else if (status === 'active') {
            borderColor = 'rgba(56, 189, 248, 0.6)';
            iconColor = '#38bdf8';
            bg = 'rgba(14, 165, 233, 0.15)';
          } else if (status === 'active_hitl') {
            borderColor = 'rgba(251, 191, 36, 0.8)';
            iconColor = '#fbbf24';
            bg = 'rgba(245, 158, 11, 0.2)';
          }

          return (
            <div
              key={stage.id}
              style={{
                background: bg,
                border: `1px solid ${borderColor}`,
                borderRadius: '12px',
                padding: '14px',
                transition: 'all 0.3s ease'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                <Icon style={{ width: '18px', height: '18px', color: iconColor }} />
                <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#f8fafc' }}>{stage.name}</span>
              </div>
              <p style={{ fontSize: '0.75rem', color: '#94a3b8', lineHeight: 1.3 }}>{stage.desc}</p>
            </div>
          );
        })}
      </div>

      {/* Real-time Agent Activity Console */}
      <div style={{ background: '#090d16', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '10px', padding: '14px', maxHeight: '160px', overflowY: 'auto' }}>
        <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'uppercase', marginBottom: '8px' }}>
          Agent Event Log Stream:
        </div>
        {logs.length === 0 ? (
          <p style={{ fontSize: '0.8rem', color: '#475569', fontStyle: 'italic' }}>Waiting for agent execution pipeline to start...</p>
        ) : (
          logs.map((log, index) => (
            <div key={index} style={{ fontSize: '0.8rem', fontFamily: 'JetBrains Mono', marginBottom: '4px', display: 'flex', gap: '8px' }}>
              <span style={{ color: '#38bdf8' }}>[{log.agent}]</span>
              <span style={{ color: '#cbd5e1' }}>{log.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
