import React, { useEffect } from 'react';
import { Play, RotateCcw, ExternalLink, Download } from 'lucide-react';
import confetti from 'canvas-confetti';

export function GamePreview({ outputUrl, gameTitle }) {
  useEffect(() => {
    if (outputUrl) {
      try {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
      } catch(e) {}
    }
  }, [outputUrl]);

  if (!outputUrl) return null;

  const fullUrl = `http://localhost:8000${outputUrl}`;

  const reloadIframe = () => {
    const iframe = document.getElementById('phaser-game-iframe');
    if (iframe) iframe.src = iframe.src;
  };

  const handleDownload = async () => {
    try {
      const res = await fetch(fullUrl);
      const htmlText = await res.text();
      const blob = new Blob([htmlText], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const filename = (gameTitle || 'educational_game').toLowerCase().replace(/[^a-z0-9]/g, '_') + '.html';
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Error downloading game:", err);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#4ade80', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Play style={{ width: '20px', height: '20px' }} />
            Live Game Sandbox: {gameTitle || 'Generated Game'}
          </h3>
          <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>100% Procedural Phaser.js 2D HTML5 game with WebAudio SFX & Playwright QA pass</p>
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={reloadIframe}
            style={{ padding: '8px 14px', background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.15)', color: '#ffffff', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}
          >
            <RotateCcw style={{ width: '14px', height: '14px' }} /> Restart
          </button>
          <button
            onClick={handleDownload}
            style={{ padding: '8px 14px', background: 'rgba(74,222,128,0.15)', border: '1px solid rgba(74,222,128,0.3)', color: '#4ade80', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', fontWeight: 600 }}
          >
            <Download style={{ width: '14px', height: '14px' }} /> Download .HTML
          </button>
          <a
            href={fullUrl}
            target="_blank"
            rel="noreferrer"
            style={{ textDecoration: 'none', padding: '8px 14px', background: 'rgba(56,189,248,0.15)', border: '1px solid rgba(56,189,248,0.3)', color: '#38bdf8', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}
          >
            <ExternalLink style={{ width: '14px', height: '14px' }} /> Open Tab
          </a>
        </div>
      </div>

      <div style={{
        position: 'relative',
        width: '100%',
        height: '620px',
        background: '#05080f',
        borderRadius: '12px',
        border: '1px solid rgba(255,255,255,0.1)',
        overflow: 'hidden'
      }}>
        <iframe
          id="phaser-game-iframe"
          src={fullUrl}
          title="Generated Phaser Game"
          style={{ width: '100%', height: '100%', border: 'none' }}
        />
      </div>
    </div>
  );
}
