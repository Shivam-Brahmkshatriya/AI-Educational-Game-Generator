import React, { useEffect, useState } from 'react';
import { Gamepad, Play, RefreshCw, X } from 'lucide-react';

export function GameGallery() {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedGame, setSelectedGame] = useState(null);

  const fetchGames = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/games');
      if (res.ok) {
        const data = await res.json();
        setGames(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGames();
  }, []);

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Gamepad style={{ width: '20px', height: '20px', color: '#fbbf24' }} />
          Generated Educational Games Gallery
        </h3>
        <button
          onClick={fetchGames}
          style={{ padding: '6px 12px', background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.15)', color: '#ffffff', borderRadius: '6px', cursor: 'pointer', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '6px' }}
        >
          <RefreshCw className={loading ? 'animate-spin' : ''} style={{ width: '14px', height: '14px' }} /> Refresh List
        </button>
      </div>

      {games.length === 0 ? (
        <p style={{ fontSize: '0.85rem', color: '#64748b', fontStyle: 'italic' }}>No saved games yet. Enter a topic above to build your first game!</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '16px' }}>
          {games.map((g, idx) => (
            <div
              key={idx}
              style={{
                background: '#090d16',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: '12px',
                padding: '16px',
                display: 'flex',
                flexDirection: 'column',
                justify: 'space-between',
                transition: 'all 0.25s ease'
              }}
            >
              <div>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#38bdf8', marginBottom: '6px' }}>{g.title}</h4>
                <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>2D Phaser HTML5 Arcade Game</p>
              </div>
              <button
                onClick={() => setSelectedGame(g)}
                className="glow-btn-primary"
                style={{ marginTop: '14px', padding: '8px 12px', fontSize: '0.8rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}
              >
                <Play style={{ width: '14px', height: '14px' }} /> Play Game
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Modal for viewing selected gallery game */}
      {selectedGame && (
        <div style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.85)',
          backdropFilter: 'blur(10px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 2000,
          padding: '20px'
        }}>
          <div className="glass-panel" style={{ width: '900px', maxWidth: '95vw', padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
              <h3 style={{ fontSize: '1.2rem', color: '#f8fafc' }}>{selectedGame.title}</h3>
              <button
                onClick={() => setSelectedGame(null)}
                style={{ background: 'none', border: 'none', color: '#ffffff', cursor: 'pointer' }}
              >
                <X style={{ width: '24px', height: '24px' }} />
              </button>
            </div>
            <div style={{ width: '100%', height: '600px', background: '#000', borderRadius: '8px', overflow: 'hidden' }}>
              <iframe
                src={`http://localhost:8000${selectedGame.url}`}
                title={selectedGame.title}
                style={{ width: '100%', height: '100%', border: 'none' }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
