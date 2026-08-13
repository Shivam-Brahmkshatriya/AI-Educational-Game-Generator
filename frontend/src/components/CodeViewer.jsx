import React, { useState } from 'react';
import { Code2, Copy, Check } from 'lucide-react';

export function CodeViewer({ code }) {
  const [copied, setCopied] = useState(false);

  if (!code) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Code2 style={{ width: '18px', height: '18px', color: '#c084fc' }} />
          Generated Phaser 3 HTML5 Source Code (`index.html`)
        </h3>

        <button
          onClick={handleCopy}
          style={{
            padding: '6px 12px',
            background: 'rgba(192, 132, 252, 0.15)',
            border: '1px solid rgba(192, 132, 252, 0.3)',
            color: '#c084fc',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '0.8rem',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          {copied ? <Check style={{ width: '14px', height: '14px' }} /> : <Copy style={{ width: '14px', height: '14px' }} />}
          {copied ? 'Copied!' : 'Copy Code'}
        </button>
      </div>

      <pre style={{
        background: '#090d16',
        border: '1px solid rgba(255,255,255,0.08)',
        borderRadius: '10px',
        padding: '16px',
        fontSize: '0.8rem',
        maxHeight: '350px',
        overflowY: 'auto',
        color: '#93c5fd',
        lineHeight: 1.4
      }}>
        {code}
      </pre>
    </div>
  );
}
