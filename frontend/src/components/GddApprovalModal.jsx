import React, { useState } from 'react';
import { ShieldAlert, CheckCircle, XCircle, Gamepad2, BookOpen, Sparkles } from 'lucide-react';

export function GddApprovalModal({ gdd, onApprove, onReject }) {
  const [rejectMode, setRejectMode] = useState(false);
  const [feedback, setFeedback] = useState('');

  if (!gdd) return null;

  const narrative = gdd.narrative || {};
  const loop = gdd.gameplay_loop || {};
  const eduRules = gdd.educational_rules || [];

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: 'rgba(5, 8, 15, 0.85)',
      backdropFilter: 'blur(12px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    }}>
      <div className="glass-panel" style={{
        width: '100%',
        maxWidth: '750px',
        maxHeight: '90vh',
        overflowY: 'auto',
        padding: '30px',
        border: '1px solid rgba(251, 191, 36, 0.4)',
        boxShadow: '0 0 50px rgba(245, 158, 11, 0.2)'
      }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
          <div style={{ padding: '10px', background: 'rgba(245, 158, 11, 0.15)', borderRadius: '12px', color: '#fbbf24' }}>
            <ShieldAlert style={{ width: '28px', height: '28px' }} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 700, color: '#f8fafc' }}>Human-In-The-Loop Review Gate</h2>
            <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>State persistent in SQLite. Inspect auto-generated Game Design Document (GDD) before code authoring.</p>
          </div>
        </div>

        {/* GDD Content Card */}
        <div style={{ background: '#090d16', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px', padding: '20px', marginBottom: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '14px' }}>
            <div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#38bdf8' }}>{gdd.game_title || 'Untitled Game'}</h3>
              <p style={{ fontSize: '0.85rem', color: '#cbd5e1', fontStyle: 'italic' }}>{gdd.tagline}</p>
            </div>
            <span style={{ padding: '4px 10px', background: 'rgba(192, 132, 252, 0.2)', border: '1px solid #c084fc', borderRadius: '20px', fontSize: '0.75rem', color: '#c084fc', fontWeight: 600 }}>
              {gdd.genre || 'Arcade Physics'}
            </span>
          </div>

          <hr style={{ borderColor: 'rgba(255,255,255,0.06)', margin: '14px 0' }} />

          {/* Narrative & Gameplay Loop */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
            <div>
              <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                <Sparkles style={{ width: '14px', height: '14px' }} /> Theme & World
              </h4>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8', lineHeight: 1.4 }}>
                <strong>Setting:</strong> {narrative.setting}<br/>
                <strong>Hero:</strong> {narrative.hero_name}
              </p>
            </div>

            <div>
              <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                <Gamepad2 style={{ width: '14px', height: '14px' }} /> Controls & Loop
              </h4>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8', lineHeight: 1.4 }}>
                <strong>Controls:</strong> {loop.controls}<br/>
                <strong>Win:</strong> {loop.win_condition}
              </p>
            </div>
          </div>

          {/* Educational Rules */}
          <div>
            <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: '#4ade80', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
              <BookOpen style={{ width: '14px', height: '14px' }} /> Educational Interaction Rules
            </h4>
            {eduRules.map((rule, idx) => (
              <div key={idx} style={{ background: 'rgba(74, 222, 128, 0.08)', border: '1px solid rgba(74, 222, 128, 0.2)', borderRadius: '8px', padding: '10px', marginBottom: '6px', fontSize: '0.8rem' }}>
                <strong style={{ color: '#f8fafc' }}>Concept:</strong> {rule.concept}<br/>
                <span style={{ color: '#4ade80' }}>✓ Correct: {rule.correct_answer}</span> | <span style={{ color: '#f87171' }}>Effect: {rule.gameplay_effect}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Action Form */}
        {rejectMode ? (
          <div>
            <label style={{ fontSize: '0.85rem', fontWeight: 600, color: '#f87171', display: 'block', marginBottom: '8px' }}>
              Describe what changes or adjustments you want the Master Designer & Sub-Agents to make:
            </label>
            <textarea
              rows={3}
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              placeholder="e.g., Make the character a space cadet, add gravity flips, make facts focus on chemical reactions..."
              style={{
                width: '100%',
                background: '#090d16',
                border: '1px solid rgba(248, 113, 113, 0.4)',
                borderRadius: '8px',
                color: '#ffffff',
                padding: '12px',
                fontSize: '0.85rem',
                marginBottom: '14px',
                outline: 'none'
              }}
            />
            <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
              <button
                onClick={() => setRejectMode(false)}
                style={{ padding: '10px 18px', background: 'transparent', border: '1px solid rgba(255,255,255,0.2)', color: '#ffffff', borderRadius: '8px', cursor: 'pointer' }}
              >
                Cancel
              </button>
              <button
                onClick={() => onReject(feedback)}
                className="glow-btn-danger"
              >
                Submit Feedback & Rewrite GDD
              </button>
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', gap: '14px', justifyContent: 'flex-end' }}>
            <button
              onClick={() => setRejectMode(true)}
              style={{
                padding: '12px 20px',
                background: 'rgba(239, 68, 68, 0.15)',
                border: '1px solid rgba(239, 68, 68, 0.4)',
                color: '#f87171',
                borderRadius: '10px',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <XCircle style={{ width: '18px', height: '18px' }} />
              Reject & Provide Feedback
            </button>
            <button
              onClick={onApprove}
              className="glow-btn-success"
              style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
            >
              <CheckCircle style={{ width: '18px', height: '18px' }} />
              Approve GDD & Proceed to Code Engine
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
