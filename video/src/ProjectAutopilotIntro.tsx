import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const accent = '#34d399';
const amber = '#fbbf24';
const ink = '#0a0f1f';
const panel = 'rgba(255,255,255,0.08)';

const ease = Easing.bezier(0.16, 1, 0.3, 1);

const clamp = {
  extrapolateLeft: 'clamp' as const,
  extrapolateRight: 'clamp' as const,
  easing: ease,
};

const SceneShell: React.FC<{children: React.ReactNode; label: string}> = ({
  children,
  label,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 18], [0, 1], clamp);
  return (
    <AbsoluteFill
      style={{
        opacity,
        background:
          'radial-gradient(circle at 10% 12%, #1d4ed8 0, transparent 28%), radial-gradient(circle at 85% 18%, #065f46 0, transparent 26%), linear-gradient(135deg, #030712 0%, #111827 52%, #020617 100%)',
        color: 'white',
        fontFamily:
          'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif',
      }}
    >
      <div
        style={{
          position: 'absolute',
          top: 54,
          left: 68,
          fontSize: 24,
          color: '#a7f3d0',
          letterSpacing: 0,
          fontWeight: 700,
        }}
      >
        project-autopilot
      </div>
      <div
        style={{
          position: 'absolute',
          top: 58,
          right: 68,
          fontSize: 18,
          color: '#cbd5e1',
          letterSpacing: 0,
        }}
      >
        {label}
      </div>
      {children}
    </AbsoluteFill>
  );
};

const TitleScene: React.FC = () => {
  const frame = useCurrentFrame();
  const y = interpolate(frame, [0, 32], [40, 0], clamp);
  const scale = interpolate(frame, [0, 36], [0.96, 1], clamp);
  const scan = interpolate(frame, [18, 160], [-180, 1920], clamp);
  return (
    <SceneShell label="30s intro">
      <div
        style={{
          position: 'absolute',
          left: 140,
          top: 230,
          transform: `translateY(${y}px) scale(${scale})`,
          width: 1160,
        }}
      >
        <div style={{fontSize: 104, fontWeight: 820, lineHeight: 1.02}}>
          Low-interaction
          <br />
          project control
        </div>
        <div
          style={{
            marginTop: 34,
            fontSize: 34,
            lineHeight: 1.32,
            color: '#dbeafe',
            width: 950,
          }}
        >
          A Codex Skill that plans, coordinates, verifies, and reports
          non-trivial project work end to end.
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 1260,
          top: 244,
          width: 430,
          height: 430,
          borderRadius: 28,
          background: panel,
          border: '1px solid rgba(255,255,255,0.16)',
          boxShadow: '0 30px 80px rgba(0,0,0,0.36)',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            position: 'absolute',
            left: scan,
            top: 0,
            width: 70,
            height: '100%',
            background: 'rgba(52,211,153,0.36)',
            filter: 'blur(18px)',
          }}
        />
        {['scope', 'spec', 'tasks', 'tests', 'review'].map((item, i) => (
          <div
            key={item}
            style={{
              margin: '30px 34px 0',
              padding: '20px 22px',
              borderRadius: 12,
              background: 'rgba(15,23,42,0.72)',
              fontSize: 28,
              fontWeight: 700,
              color: i === 3 ? amber : '#f8fafc',
            }}
          >
            {item}
          </div>
        ))}
      </div>
    </SceneShell>
  );
};

const ModeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const modes = [
    ['Small', 'direct fix'],
    ['Medium', 'light spec + 2 agents'],
    ['Large', 'OpenSpec lifecycle'],
  ];
  return (
    <SceneShell label="right amount of process">
      <div style={{position: 'absolute', left: 110, top: 170}}>
        <h1 style={{fontSize: 74, margin: 0}}>Automatic task sizing</h1>
        <p style={{fontSize: 31, color: '#cbd5e1', width: 780}}>
          No ceremony for small edits. Full governance only when risk justifies
          it.
        </p>
      </div>
      <div style={{position: 'absolute', left: 120, right: 120, top: 440}}>
        <div style={{display: 'flex', gap: 32}}>
          {modes.map(([name, desc], i) => {
            const local = frame - i * 14;
            const y = interpolate(local, [0, 26], [50, 0], clamp);
            const opacity = interpolate(local, [0, 22], [0, 1], clamp);
            return (
              <div
                key={name}
                style={{
                  flex: 1,
                  opacity,
                  transform: `translateY(${y}px)`,
                  minHeight: 260,
                  borderRadius: 18,
                  padding: 34,
                  background: panel,
                  border: `1px solid ${i === 2 ? accent : 'rgba(255,255,255,0.14)'}`,
                }}
              >
                <div style={{fontSize: 48, fontWeight: 820}}>{name}</div>
                <div style={{fontSize: 28, marginTop: 24, color: '#dbeafe'}}>
                  {desc}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </SceneShell>
  );
};

const WorkflowScene: React.FC = () => {
  const frame = useCurrentFrame();
  const steps = ['Proposal', 'Tasks', 'Implement', 'Verify', 'Archive'];
  return (
    <SceneShell label="OpenSpec-driven">
      <div style={{position: 'absolute', left: 110, top: 150}}>
        <h1 style={{fontSize: 72, margin: 0}}>One source of truth</h1>
        <p style={{fontSize: 30, color: '#cbd5e1', width: 840}}>
          Specs, task claims, validation evidence, and final status stay
          synchronized.
        </p>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 130,
          right: 130,
          top: 500,
          height: 8,
          background: 'rgba(255,255,255,0.18)',
        }}
      />
      {steps.map((step, i) => {
        const progress = interpolate(frame, [20, 210], [0, 1], clamp);
        const active = progress >= i / (steps.length - 1);
        return (
          <div
            key={step}
            style={{
              position: 'absolute',
              left: 130 + i * 410,
              top: 450,
              width: 160,
              textAlign: 'center',
            }}
          >
            <div
              style={{
                width: 88,
                height: 88,
                margin: '0 auto 22px',
                borderRadius: 44,
                background: active ? accent : 'rgba(255,255,255,0.14)',
                color: active ? ink : '#e5e7eb',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 34,
                fontWeight: 900,
              }}
            >
              {i + 1}
            </div>
            <div style={{fontSize: 25, fontWeight: 760}}>{step}</div>
          </div>
        );
      })}
    </SceneShell>
  );
};

const DepartmentsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const deps = [
    ['Requirements', 'clarify + design'],
    ['Development', 'bounded implementation'],
    ['QA', 'tests + evidence'],
    ['Review', 'independent check'],
  ];
  return (
    <SceneShell label="bounded departments">
      <div style={{position: 'absolute', left: 118, top: 150}}>
        <h1 style={{fontSize: 70, margin: 0}}>Agents only when useful</h1>
        <p style={{fontSize: 30, color: '#cbd5e1', width: 860}}>
          Parallel work is limited to clear, non-overlapping scopes.
        </p>
      </div>
      <div style={{position: 'absolute', left: 160, top: 405, right: 160}}>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 28}}>
          {deps.map(([name, desc], i) => {
            const local = frame - i * 12;
            const opacity = interpolate(local, [0, 22], [0, 1], clamp);
            const x = interpolate(local, [0, 26], [i % 2 === 0 ? -42 : 42, 0], clamp);
            return (
              <div
                key={name}
                style={{
                  opacity,
                  transform: `translateX(${x}px)`,
                  borderRadius: 18,
                  padding: 34,
                  minHeight: 150,
                  background: panel,
                  border: '1px solid rgba(255,255,255,0.15)',
                }}
              >
                <div style={{fontSize: 39, fontWeight: 850}}>{name}</div>
                <div style={{fontSize: 25, color: '#d1fae5', marginTop: 12}}>
                  {desc}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </SceneShell>
  );
};

const CloseScene: React.FC = () => {
  const frame = useCurrentFrame();
  const done = interpolate(frame, [40, 130], [0, 100], clamp);
  return (
    <SceneShell label="ship with evidence">
      <div style={{position: 'absolute', left: 130, top: 180, width: 940}}>
        <h1 style={{fontSize: 86, margin: 0}}>Completion means verified.</h1>
        <p style={{fontSize: 32, color: '#cbd5e1', lineHeight: 1.35}}>
          project-autopilot blocks duplicate work, repairs failing checks, and
          refuses to call unfinished work done.
        </p>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 1280,
          top: 270,
          width: 420,
          height: 420,
          borderRadius: 210,
          background: `conic-gradient(${accent} ${done}%, rgba(255,255,255,0.16) ${done}% 100%)`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <div
          style={{
            width: 310,
            height: 310,
            borderRadius: 155,
            background: '#06111f',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: 'column',
          }}
        >
          <div style={{fontSize: 86, fontWeight: 900}}>{Math.round(done)}%</div>
          <div style={{fontSize: 24, color: '#a7f3d0'}}>acceptance gate</div>
        </div>
      </div>
    </SceneShell>
  );
};

export const ProjectAutopilotIntro: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#020617'}}>
      <Sequence from={0} durationInFrames={180}>
        <TitleScene />
      </Sequence>
      <Sequence from={180} durationInFrames={180}>
        <ModeScene />
      </Sequence>
      <Sequence from={360} durationInFrames={180}>
        <WorkflowScene />
      </Sequence>
      <Sequence from={540} durationInFrames={180}>
        <DepartmentsScene />
      </Sequence>
      <Sequence from={720} durationInFrames={180}>
        <CloseScene />
      </Sequence>
    </AbsoluteFill>
  );
};
