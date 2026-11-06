import os
import sys
import time
import webbrowser
from pathlib import Path

# Optional Rich terminal boot sequence for Hacker Vibe
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import track
    console = Console()
    console.print(Panel.fit(
        "[bold crimson]🩸 BLOODCONNECT GOD-MODE CYBER-ARCHITECT ENGINE v3.0[/bold crimson]\n"
        "[cyan]Student:[/cyan] Prince Rajput (BCA Sem-7 | Gujarat University | DSC-M-BCA-471P)\n"
        "[emerald]Stack:[/emerald] .NET 10 MVC | EF Core 10 | SignalR WebSockets | SQL Server | Cookie Auth\n"
        "[yellow]Upgrades:[/yellow] 6-Synth Audio Engine | 2-Browser Live SignalR Lab | Auto-Play Packet Tracer | Viva Deck",
        border_style="bright_red"
    ))
    for _ in track(range(25), description="[bold green]Compiling 32 Files, Audio Synthesizers & Animations..."):
        time.sleep(0.02)
except ImportError:
    print("=========================================================================")
    print("🩸 BLOODCONNECT GOD-MODE CYBER-ARCHITECT ENGINE v3.0 (FULL POWER EDITION)")
    print("Student: Prince Rajput | BCA Sem-7 | Gujarat University")
    print("=========================================================================")

HTML_PORTAL = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BLOODCONNECT v3.0 // GOD-MODE INTERACTIVE WORKFLOW & VIVA COMMAND CENTER</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

  :root {
    --bg-deep: #03060d;
    --bg-panel: #080e1e;
    --bg-card: #0e172c;
    --bg-card-hover: #152242;
    --border-dim: #1d2d50;
    --neon-cyan: #00f0ff;
    --neon-crimson: #ff0055;
    --neon-green: #00ff9d;
    --neon-amber: #ffb800;
    --neon-purple: #b537f2;
    --text-main: #f1f5f9;
    --text-muted: #94a3b8;
    --font-mono: 'JetBrains Mono', monospace;
    --font-sans: 'Plus Jakarta Sans', system-ui, sans-serif;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body {
    background-color: var(--bg-deep);
    color: var(--text-main);
    font-family: var(--font-sans);
    line-height: 1.65;
    overflow-x: hidden;
  }

  /* Interactive Particle + RBC Canvas */
  #bg-canvas {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: -2; opacity: 0.32; pointer-events: none;
  }
  .cyber-grid-overlay {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background-image: 
      linear-gradient(rgba(0, 240, 255, 0.035) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0, 240, 255, 0.035) 1px, transparent 1px);
    background-size: 42px 42px;
    z-index: -1; pointer-events: none;
  }

  /* Top Scroll Progress Bar */
  #scroll-bar {
    position: fixed; top: 0; left: 0; height: 4px; width: 0%;
    background: linear-gradient(90deg, var(--neon-crimson), var(--neon-cyan), var(--neon-green));
    z-index: 9999; box-shadow: 0 0 15px var(--neon-cyan);
  }

  /* Sticky Futuristic Top Navigation */
  .cyber-nav {
    position: sticky; top: 0; z-index: 1000;
    background: rgba(3, 6, 13, 0.90);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(0, 240, 255, 0.28);
    padding: 12px 26px;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
  }
  .brand-box { display: flex; align-items: center; gap: 12px; }
  .pulse-dot {
    width: 14px; height: 14px; border-radius: 50%;
    background: var(--neon-crimson);
    box-shadow: 0 0 18px var(--neon-crimson);
    animation: pulseGlow 1.1s infinite alternate;
  }
  @keyframes pulseGlow { from { transform: scale(0.85); opacity: 0.65; } to { transform: scale(1.3); opacity: 1; } }
  .brand-title { font-family: var(--font-mono); font-weight: 800; font-size: 1.08rem; letter-spacing: 0.8px; color: #fff; }
  .brand-title span { color: var(--neon-cyan); }

  .nav-links { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
  .nav-btn {
    font-family: var(--font-mono); font-size: 0.74rem; font-weight: 700;
    color: var(--text-main); text-decoration: none;
    padding: 8px 13px; border-radius: 8px;
    background: rgba(14, 23, 44, 0.9);
    border: 1px solid var(--border-dim);
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1); cursor: pointer;
    display: inline-flex; align-items: center; gap: 6px;
  }
  .nav-btn:hover {
    border-color: var(--neon-cyan); color: var(--neon-cyan);
    box-shadow: 0 0 16px rgba(0, 240, 255, 0.3);
    transform: translateY(-2px);
  }
  .nav-btn.crimson { border-color: var(--neon-crimson); color: #ff99bb; background: rgba(255, 0, 85, 0.14); }
  .nav-btn.crimson:hover { background: var(--neon-crimson); color: #fff; box-shadow: 0 0 22px rgba(255, 0, 85, 0.7); }
  .nav-btn.green { border-color: var(--neon-green); color: var(--neon-green); background: rgba(0, 255, 157, 0.1); }
  .nav-btn.green:hover { background: var(--neon-green); color: #000; box-shadow: 0 0 22px rgba(0, 255, 157, 0.7); }
  .nav-btn.amber { border-color: var(--neon-amber); color: var(--neon-amber); background: rgba(255, 184, 0, 0.1); }

  /* Main Container */
  .container { max-width: 1500px; margin: 0 auto; padding: 36px 24px 120px 24px; }

  /* Section Styling */
  .cyber-section {
    margin-bottom: 75px;
    background: rgba(8, 14, 30, 0.82);
    border: 1px solid var(--border-dim);
    border-radius: 20px;
    padding: 38px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65);
    position: relative;
    overflow: hidden;
  }
  .cyber-section::before {
    content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 3px;
    background: linear-gradient(90deg, var(--neon-crimson), var(--neon-cyan), var(--neon-green));
  }
  .sec-tag {
    font-family: var(--font-mono); font-size: 0.76rem; font-weight: 800;
    color: var(--neon-cyan); text-transform: uppercase; letter-spacing: 2px;
    margin-bottom: 8px; display: inline-block;
    background: rgba(0, 240, 255, 0.08); padding: 4px 10px; border-radius: 6px;
  }
  .sec-title {
    font-size: 1.95rem; font-weight: 800; color: #fff; margin-bottom: 12px;
    display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  }
  .sec-desc { font-size: 1.02rem; color: var(--text-muted); max-width: 1050px; margin-bottom: 28px; }

  /* Hero Telemetry Cards */
  .hero-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 22px;
  }
  .stat-card {
    background: var(--bg-card); border: 1px solid var(--border-dim); border-left: 4px solid var(--neon-cyan);
    padding: 20px; border-radius: 12px; transition: 0.25s; position: relative; overflow: hidden;
  }
  .stat-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0, 240, 255, 0.12); }
  .stat-card.crimson { border-left-color: var(--neon-crimson); }
  .stat-card.green { border-left-color: var(--neon-green); }
  .stat-card.amber { border-left-color: var(--neon-amber); }
  .stat-card.purple { border-left-color: var(--neon-purple); }
  .stat-val { font-family: var(--font-mono); font-size: 1.75rem; font-weight: 800; color: #fff; }
  .stat-lbl { font-size: 0.84rem; color: var(--text-muted); margin-top: 4px; }

  /* Soundboard Strip */
  .soundboard-strip {
    margin-top: 24px; padding: 16px 20px; border-radius: 12px;
    background: rgba(0, 240, 255, 0.05); border: 1px dashed rgba(0, 240, 255, 0.3);
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;
  }

  /* MODULE 1: 2-BROWSER SPLIT-SCREEN LIVE SIGNALR & CACHE LAB */
  .dual-browser-grid {
    display: grid; grid-template-columns: 1fr 260px 1fr; gap: 18px; align-items: stretch;
  }
  @media (max-width: 1150px) { .dual-browser-grid { grid-template-columns: 1fr; } }
  .mock-browser {
    background: #050a16; border: 2px solid var(--border-dim); border-radius: 14px;
    overflow: hidden; display: flex; flex-direction: column;
    box-shadow: 0 12px 35px rgba(0,0,0,0.6);
  }
  .mock-browser.admin-b { border-color: rgba(0, 240, 255, 0.45); }
  .mock-browser.user-b { border-color: rgba(255, 0, 85, 0.45); }
  .browser-topbar {
    background: #0f1930; padding: 10px 16px; display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid var(--border-dim);
  }
  .b-dots { display: flex; gap: 6px; }
  .b-dot { width: 10px; height: 10px; border-radius: 50%; }
  .b-url {
    font-family: var(--font-mono); font-size: 0.72rem; color: var(--neon-cyan);
    background: #060b18; padding: 4px 12px; border-radius: 6px; border: 1px solid var(--border-dim);
  }
  .browser-body { padding: 20px; flex: 1; display: flex; flex-direction: column; gap: 14px; position: relative; }

  .hub-middle-tower {
    background: #060c1b; border: 2px dashed var(--neon-purple); border-radius: 14px;
    padding: 16px; display: flex; flex-direction: column; justify-content: space-between; align-items: center;
    text-align: center; position: relative; overflow: hidden;
  }
  .laser-beam {
    width: 100%; height: 6px; background: #152238; border-radius: 99px; position: relative; overflow: hidden; margin: 12px 0;
  }
  .laser-pulse {
    position: absolute; top: 0; left: -40%; width: 40%; height: 100%;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-crimson));
    box-shadow: 0 0 16px var(--neon-cyan);
    transition: none;
  }
  .laser-pulse.shoot-right { left: 100%; transition: left 0.55s cubic-bezier(0.16, 1, 0.3, 1); }

  /* Bell Ring Animation */
  .bell-wrap {
    position: relative; display: inline-flex; align-items: center; justify-content: center;
    width: 46px; height: 46px; border-radius: 12px; background: #121f3d; border: 1px solid var(--neon-cyan);
    cursor: pointer;
  }
  .bell-svg { width: 24px; height: 24px; stroke: var(--neon-amber); fill: none; stroke-width: 2; }
  .bell-wrap.ringing .bell-svg { animation: ringBell 0.65s ease-in-out; }
  @keyframes ringBell {
    0%, 100% { transform: rotate(0); }
    20% { transform: rotate(22deg); }
    40% { transform: rotate(-20deg); }
    60% { transform: rotate(14deg); }
    80% { transform: rotate(-10deg); }
  }
  .bell-badge-count {
    position: absolute; top: -6px; right: -6px; background: var(--neon-crimson); color: #fff;
    font-family: var(--font-mono); font-size: 0.72rem; font-weight: 800;
    padding: 2px 7px; border-radius: 99px; box-shadow: 0 0 12px var(--neon-crimson);
    transition: transform 0.25s;
  }
  .bell-badge-count.bounce { transform: scale(1.45); }

  /* MODULE 2: HACKER DICTIONARY & ATTACK LAB */
  .concept-layout { display: grid; grid-template-columns: 350px 1fr; gap: 26px; }
  @media (max-width: 1024px) { .concept-layout { grid-template-columns: 1fr; } }
  .concept-list { display: flex; flex-direction: column; gap: 10px; }
  .concept-tab {
    background: var(--bg-card); border: 1px solid var(--border-dim);
    padding: 14px 16px; border-radius: 12px; cursor: pointer; text-align: left;
    color: var(--text-main); transition: 0.2s;
  }
  .concept-tab:hover { border-color: var(--neon-cyan); transform: translateX(5px); }
  .concept-tab.active {
    background: linear-gradient(90deg, rgba(0, 240, 255, 0.14), rgba(14, 23, 44, 0.9));
    border-color: var(--neon-cyan);
    box-shadow: 0 0 22px rgba(0, 240, 255, 0.2);
  }
  .concept-tab strong { display: block; font-family: var(--font-mono); font-size: 0.92rem; color: #fff; }
  .concept-tab span { font-size: 0.78rem; color: var(--text-muted); }

  .concept-stage {
    background: #060b17; border: 1px solid var(--border-dim); border-radius: 16px; padding: 28px;
    display: flex; flex-direction: column; gap: 20px;
  }
  .explain-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  @media (max-width: 800px) { .explain-grid { grid-template-columns: 1fr; } }
  .info-box {
    background: var(--bg-card); border: 1px solid var(--border-dim); border-radius: 12px; padding: 18px;
  }
  .info-box h4 {
    font-family: var(--font-mono); font-size: 0.8rem; text-transform: uppercase;
    letter-spacing: 1px; color: var(--neon-amber); margin-bottom: 8px;
  }
  .info-box.cyan h4 { color: var(--neon-cyan); }
  .info-box.green h4 { color: var(--neon-green); }

  /* Hack Simulator Box */
  .hack-sim-box {
    background: #03060f; border: 1px solid var(--neon-crimson); border-radius: 14px; padding: 22px;
  }
  .hack-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 14px; }
  .shield-toggle { display: flex; align-items: center; gap: 10px; font-family: var(--font-mono); font-size: 0.82rem; flex-wrap: wrap; }
  .toggle-btn {
    padding: 9px 16px; border-radius: 8px; font-family: var(--font-mono); font-weight: 800; cursor: pointer; border: none; transition: 0.2s;
  }
  .toggle-on { background: var(--neon-green); color: #000; box-shadow: 0 0 18px rgba(0, 255, 157, 0.6); }
  .toggle-off { background: var(--neon-crimson); color: #fff; box-shadow: 0 0 18px rgba(255, 0, 85, 0.6); }

  .packet-lane {
    height: 88px; background: #081022; border: 1px dashed var(--border-dim); border-radius: 12px;
    position: relative; display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px; margin: 16px 0; overflow: hidden;
  }
  .packet-endpoint {
    font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700; z-index: 2;
    background: #10192e; padding: 8px 14px; border-radius: 8px; border: 1px solid var(--border-dim);
    text-align: center;
  }
  .shield-barrier {
    position: absolute; left: 52%; top: 8px; bottom: 8px; width: 6px;
    background: var(--neon-green); box-shadow: 0 0 18px var(--neon-green);
    border-radius: 99px; z-index: 3; transition: 0.3s;
  }
  .shield-barrier.off {
    background: rgba(255, 0, 85, 0.2); box-shadow: none; border: 1px dashed var(--neon-crimson);
  }
  .moving-packet {
    position: absolute; left: 150px; padding: 7px 14px; border-radius: 99px;
    font-family: var(--font-mono); font-size: 0.74rem; font-weight: 800;
    background: var(--neon-amber); color: #000; display: none; z-index: 5;
    box-shadow: 0 0 20px var(--neon-amber); white-space: nowrap;
  }
  .terminal-out {
    background: #020409; border: 1px solid #1a2639; border-radius: 10px; padding: 16px;
    font-family: var(--font-mono); font-size: 0.82rem; color: var(--neon-green);
    min-height: 115px; white-space: pre-wrap; line-height: 1.55;
  }

  /* MODULE 3: SPACIOUS ARCHITECTURE MAP & AUTO-PLAY PACKET TRACER */
  .workflow-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
  .wf-btn {
    background: var(--bg-card); border: 1px solid var(--border-dim); color: var(--text-main);
    padding: 12px 16px; border-radius: 10px; cursor: pointer; font-family: var(--font-mono);
    font-size: 0.8rem; font-weight: 700; transition: 0.2s; flex: 1; min-width: 230px; text-align: left;
  }
  .wf-btn:hover { border-color: var(--neon-cyan); }
  .wf-btn.active { border-color: var(--neon-green); background: rgba(0, 255, 157, 0.12); box-shadow: 0 0 22px rgba(0, 255, 157, 0.22); }
  .wf-btn small { display: block; color: var(--text-muted); font-family: var(--font-sans); font-weight: 400; margin-top: 4px; font-size: 0.75rem; }

  .arch-stage-wrap {
    width: 100%; overflow-x: auto; background: #040812; border: 1px solid var(--border-dim);
    border-radius: 16px; padding: 18px; position: relative;
  }
  .arch-canvas { width: 1400px; height: 880px; position: relative; margin: 0 auto; }
  .arch-lane {
    position: absolute; left: 10px; width: 1380px; border: 1px dashed rgba(0, 240, 255, 0.18);
    border-radius: 12px; background: rgba(10, 16, 32, 0.55); padding: 10px 18px;
  }
  .arch-lane-title { font-family: var(--font-mono); font-size: 0.72rem; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; color: var(--neon-cyan); opacity: 0.9; }
  .arch-node {
    position: absolute; width: 205px; background: var(--bg-card); border: 2px solid var(--border-dim);
    border-radius: 12px; padding: 10px 12px; cursor: pointer; z-index: 5; transition: all 0.25s;
  }
  .arch-node:hover { border-color: var(--neon-cyan); transform: translateY(-3px); }
  .arch-node.active-node {
    border-color: var(--neon-green); background: #0d2b22;
    box-shadow: 0 0 32px rgba(0, 255, 157, 0.85); transform: scale(1.07); z-index: 10;
  }
  .arch-node .n-badge { font-family: var(--font-mono); font-size: 0.62rem; font-weight: 800; padding: 2px 6px; border-radius: 4px; background: rgba(0, 240, 255, 0.15); color: var(--neon-cyan); display: inline-block; margin-bottom: 4px; }
  .arch-node .n-name { font-family: var(--font-mono); font-size: 0.82rem; font-weight: 700; color: #fff; }
  .arch-node .n-role { font-size: 0.71rem; color: var(--text-muted); margin-top: 2px; }

  #arch-svg { position: absolute; top: 0; left: 0; width: 1400px; height: 880px; pointer-events: none; z-index: 2; }
  .svg-edge { stroke: #1e2d4d; stroke-width: 2; fill: none; stroke-dasharray: 6 6; }
  .svg-edge.lit { stroke: var(--neon-green); stroke-width: 4; stroke-dasharray: none; filter: drop-shadow(0 0 8px #00ff9d); }
  .svg-orb { fill: var(--neon-cyan); filter: drop-shadow(0 0 12px #00f0ff); }

  .step-console {
    margin-top: 22px; background: #03060c; border: 1px solid var(--neon-cyan);
    border-radius: 14px; padding: 22px; display: grid; grid-template-columns: 1fr 1fr; gap: 22px;
  }
  @media (max-width: 960px) { .step-console { grid-template-columns: 1fr; } }

  /* MODULE 4: BLOOD TRANSFUSION BAG SIMULATOR & TWO-WAY PLEDGE MACHINE */
  .lab-two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
  @media (max-width: 1024px) { .lab-two-col { grid-template-columns: 1fr; } }
  .bg-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 14px 0; }
  .bg-pill {
    background: var(--bg-card); border: 2px solid var(--border-dim); border-radius: 10px;
    padding: 13px 8px; text-align: center; font-family: var(--font-mono); font-size: 1.15rem;
    font-weight: 800; color: #fff; cursor: pointer; transition: 0.2s;
  }
  .bg-pill:hover { border-color: var(--neon-cyan); transform: scale(1.04); }
  .bg-pill.selected-recipient { background: rgba(255, 0, 85, 0.25); border-color: var(--neon-crimson); box-shadow: 0 0 20px rgba(255, 0, 85, 0.5); }
  .bg-pill.compatible-donor { background: rgba(0, 255, 157, 0.2); border-color: var(--neon-green); box-shadow: 0 0 18px rgba(0, 255, 157, 0.4); }
  .bg-pill.incompatible-donor { opacity: 0.45; border-color: #334155; }

  /* Visual Blood Transfusion Tube */
  .transfusion-stage {
    background: #040812; border: 1px solid var(--border-dim); border-radius: 12px;
    padding: 16px; margin-top: 14px; display: flex; align-items: center; justify-content: space-between; gap: 12px;
  }
  .blood-bag {
    width: 95px; height: 110px; border: 3px solid #cbd5e1; border-radius: 16px 16px 24px 24px;
    position: relative; overflow: hidden; background: #0b1326; display: flex; flex-direction: column;
    align-items: center; justify-content: center; font-family: var(--font-mono); font-weight: 800; z-index: 2;
  }
  .bag-fill {
    position: absolute; bottom: 0; left: 0; width: 100%; height: 75%;
    background: linear-gradient(180deg, #ff0055, #990033);
    transition: height 0.5s, background 0.3s; z-index: -1;
  }
  .iv-tube {
    flex: 1; height: 14px; background: #0f172a; border: 2px solid #334155; border-radius: 99px;
    position: relative; overflow: hidden;
  }
  .iv-flow {
    position: absolute; top: 0; left: 0; height: 100%; width: 0%;
    background: repeating-linear-gradient(90deg, #ff0055 0px, #ff0055 18px, #ff6699 18px, #ff6699 30px);
    background-size: 60px 100%;
    animation: flowBlood 0.8s linear infinite;
    transition: width 0.6s ease;
  }
  @keyframes flowBlood { from { background-position: 0 0; } to { background-position: 60px 0; } }

  .state-machine-card {
    background: #060b16; border: 1px solid var(--border-dim); border-radius: 14px; padding: 24px;
  }
  .sm-badges { display: flex; gap: 8px; flex-wrap: wrap; margin: 14px 0; }
  .sm-step {
    padding: 8px 12px; border-radius: 8px; font-family: var(--font-mono); font-size: 0.76rem;
    background: var(--bg-card); border: 1px solid var(--border-dim); color: var(--text-muted); transition: 0.25s;
  }
  .sm-step.current { background: var(--neon-green); color: #000; font-weight: 800; border-color: var(--neon-green); box-shadow: 0 0 18px rgba(0, 255, 157, 0.5); transform: scale(1.05); }

  .privacy-vault {
    padding: 14px 18px; border-radius: 10px; margin: 12px 0;
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;
    font-family: var(--font-mono); font-size: 0.85rem; transition: 0.3s;
  }
  .privacy-vault.locked { background: rgba(255, 0, 85, 0.12); border: 1px solid var(--neon-crimson); color: #fda4af; }
  .privacy-vault.unlocked { background: rgba(0, 255, 157, 0.14); border: 1px solid var(--neon-green); color: var(--neon-green); box-shadow: 0 0 20px rgba(0, 255, 157, 0.2); }

  /* MODULE 5: 32-FILE ENCYCLOPEDIA */
  .filter-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 24px; align-items: center; }
  .search-input {
    flex: 1; min-width: 260px; background: #050a14; border: 1px solid var(--border-dim);
    color: #fff; padding: 12px 18px; border-radius: 10px; font-family: var(--font-mono); font-size: 0.88rem;
  }
  .search-input:focus { outline: none; border-color: var(--neon-cyan); box-shadow: 0 0 15px rgba(0, 240, 255, 0.2); }
  .file-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(430px, 1fr)); gap: 20px; }
  @media (max-width: 600px) { .file-grid { grid-template-columns: 1fr; } }

  .file-card {
    background: var(--bg-card); border: 1px solid var(--border-dim); border-radius: 14px;
    padding: 22px; display: flex; flex-direction: column; gap: 13px; transition: 0.22s;
  }
  .file-card:hover { border-color: var(--neon-cyan); transform: translateY(-3px); box-shadow: 0 12px 30px rgba(0, 240, 255, 0.12); }
  .file-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; border-bottom: 1px solid var(--border-dim); padding-bottom: 10px; }
  .file-path { font-family: var(--font-mono); font-size: 0.96rem; font-weight: 800; color: var(--neon-cyan); word-break: break-all; }
  .file-cat { font-family: var(--font-mono); font-size: 0.66rem; font-weight: 800; padding: 3px 8px; border-radius: 5px; background: rgba(255, 0, 85, 0.16); color: #ff80aa; white-space: nowrap; }
  .file-sec-label { font-family: var(--font-mono); font-size: 0.71rem; text-transform: uppercase; color: var(--neon-amber); font-weight: 700; margin-bottom: 3px; }
  .file-text { font-size: 0.88rem; color: var(--text-main); }
  .code-block {
    background: #03060c; border: 1px solid #1a2540; border-radius: 8px; padding: 12px;
    font-family: var(--font-mono); font-size: 0.75rem; color: #a5f3fc; overflow-x: auto; white-space: pre;
  }
  .break-box {
    background: rgba(255, 0, 85, 0.09); border-left: 3px solid var(--neon-crimson);
    padding: 10px 12px; border-radius: 6px; font-size: 0.82rem; color: #fecdd3;
  }
  .viva-tip {
    background: rgba(0, 255, 157, 0.09); border-left: 3px solid var(--neon-green);
    padding: 10px 12px; border-radius: 6px; font-size: 0.82rem; color: #a7f3d0;
  }

  /* MODULE 6: EXTERNAL VIVA RAPID-FIRE DECK */
  .viva-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 18px; }
  @media (max-width: 600px) { .viva-grid { grid-template-columns: 1fr; } }
  .viva-card {
    background: var(--bg-card); border: 1px solid var(--border-dim); border-radius: 14px;
    padding: 20px; cursor: pointer; transition: 0.25s; position: relative;
  }
  .viva-card:hover { border-color: var(--neon-amber); transform: translateY(-2px); }
  .viva-q { font-weight: 800; color: #fff; font-size: 0.98rem; display: flex; justify-content: space-between; gap: 10px; }
  .viva-a {
    margin-top: 12px; padding-top: 12px; border-top: 1px dashed var(--border-dim);
    font-size: 0.88rem; color: #a7f3d0; display: none;
  }
  .viva-card.open { border-color: var(--neon-green); background: #0c1f24; }
  .viva-card.open .viva-a { display: block; }

  /* Toast Notification Overlay */
  #live-toast {
    position: fixed; bottom: 28px; right: 28px; z-index: 9999;
    background: #0b1326; border: 1px solid var(--neon-cyan); border-left: 6px solid var(--neon-crimson);
    padding: 18px 22px; border-radius: 12px; box-shadow: 0 20px 50px rgba(0,0,0,0.85);
    display: none; max-width: 390px; animation: toastPop 0.3s ease-out;
  }
  @keyframes toastPop { from { transform: translateY(40px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
</style>
</head>
<body>

<div id="scroll-bar"></div>
<canvas id="bg-canvas"></canvas>
<div class="cyber-grid-overlay"></div>

<!-- LIVE SIGNALR TOAST OVERLAY -->
<div id="live-toast">
  <div style="font-family:var(--font-mono); font-size:0.72rem; color:var(--neon-cyan); font-weight:800;">⚡ SIGNALR WEBSOCKET PUSH RECEIVED</div>
  <div id="lt-title" style="font-weight:800; font-size:1rem; color:#fff; margin:4px 0;">New A+ Critical Request</div>
  <div id="lt-body" style="font-size:0.84rem; color:var(--text-muted);">Patient: Rahul Sharma · Ahmedabad, Gujarat</div>
</div>

<!-- STICKY TOP NAVBAR -->
<nav class="cyber-nav">
  <div class="brand-box">
    <div class="pulse-dot"></div>
    <div class="brand-title">BLOODCONNECT <span>// GOD-MODE v3.0</span></div>
  </div>
  <div class="nav-links">
    <a href="#sec-dual" class="nav-btn">1. Live 2-Browser SignalR</a>
    <a href="#sec-glossary" class="nav-btn">2. Desi Security & Hack Lab</a>
    <a href="#sec-arch" class="nav-btn">3. Auto-Play Packet Tracer</a>
    <a href="#sec-domain" class="nav-btn">4. Blood Bag & Pledge Lab</a>
    <a href="#sec-files" class="nav-btn">5. All 32 Files</a>
    <a href="#sec-viva" class="nav-btn amber">6. 🎓 Viva Q&A Deck</a>
    <button class="nav-btn green" id="mute-btn" onclick="toggleAudioMute()">🔊 Sound: ON</button>
    <button class="nav-btn crimson" onclick="triggerSignalRDemo()">🔔 Chime (880+1174Hz)</button>
  </div>
</nav>

<div class="container">

  <!-- HERO SECTION + PROCEDURAL SOUNDBOARD -->
  <section class="cyber-section">
    <span class="sec-tag">// PRINCE RAJPUT · BCA SEM-7 · GUJARAT UNIVERSITY (DSC-M-BCA-471P)</span>
    <h1 class="sec-title">🩸 BloodConnect — Interactive Full-Stack & Viva Command Center</h1>
    <p class="sec-desc">
      Bhai Prince, yeh koi sadharan page nahi hai—yeh tere <b>BloodConnect (.NET 10 + EF Core 10 + SignalR + SQL Server)</b> project ka live playable simulator hai! Har button par asli <b>Web Audio Synthesizer sounds</b> hain, <b>Desi Gawaar-Friendly analogies</b> hain, aur <b>live animations</b> hain taaki External Viva examiner bhi dekh kar dang reh jaaye!
    </p>
    <div class="hero-grid">
      <div class="stat-card">
        <div class="stat-val">.NET 10 + EF 10</div>
        <div class="stat-lbl">MVC + 18 REST APIs + Code-First Migrations</div>
      </div>
      <div class="stat-card crimson">
        <div class="stat-val">SignalR Hub</div>
        <div class="stat-lbl">Zero-Polling WebSocket + 880Hz/1174Hz Chime</div>
      </div>
      <div class="stat-card green">
        <div class="stat-val">32 Source Files</div>
        <div class="stat-lbl">9 Controllers · 12 Models · 2 Services · 1 Hub</div>
      </div>
      <div class="stat-card amber">
        <div class="stat-val">5-Layer Shield</div>
        <div class="stat-lbl">CSRF · XSS · SQLi · IDOR · Instant Ban Eviction</div>
      </div>
      <div class="stat-card purple">
        <div class="stat-val">60s RAM Cache</div>
        <div class="stat-lbl">IMemoryCache Badge + Explicit Write Invalidation</div>
      </div>
    </div>

    <!-- Interactive Procedural Soundboard -->
    <div class="soundboard-strip">
      <div style="font-family:var(--font-mono); font-size:0.8rem; color:var(--neon-cyan); font-weight:800;">
        🎹 LIVE WEB AUDIO SYNTHESIZER SOUNDBOARD (Click to Test Project Sounds):
      </div>
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button class="nav-btn crimson" onclick="triggerSignalRDemo()">🔔 SignalR Chime (880+1174Hz)</button>
        <button class="nav-btn" onclick="playLaserWhoosh()">🚀 Packet Laser Whoosh</button>
        <button class="nav-btn green" onclick="playShieldBlockSound()">🛡️ Shield Block Clang</button>
        <button class="nav-btn amber" onclick="playHackAlarmSound()">🚨 Hack Breach Siren</button>
        <button class="nav-btn" onclick="playHeartbeatSound()">💓 ECG Heartbeat</button>
        <button class="nav-btn green" onclick="playDbCommitSound()">💾 SQL Commit Chime</button>
      </div>
    </div>
  </section>

  <!-- MODULE 01: 2-BROWSER SPLIT-SCREEN LIVE SIGNALR & 60s CACHE LAB -->
  <section class="cyber-section" id="sec-dual">
    <span class="sec-tag">// MODULE 01 : TWO-BROWSER REAL-TIME SIGNALR & HYBRID CACHE SIMULATOR</span>
    <h2 class="sec-title">⚡ Live 2-Browser Test: Patient Action ➔ SignalR Rocket ➔ Admin Bell Ring</h2>
    <p class="sec-desc">
      Tere README mein likha hai: <i>"Test with 2 browsers: Browser B posts a request ➔ Browser A receives toast + sound + bell badge instantly!"</i> Yahan alag-alag browser kholne ki zaroorat nahi—<b>Left Browser (User/Donor)</b> mein koi bhi button daba aur dekh kaise beech ke <b>`NotificationHub.cs`</b> se laser packet ud kar <b>Right Browser (Admin/Owner)</b> ki घंटी bajata hai aur <b>60s `IMemoryCache` timer</b> ko reset karta hai!
    </p>

    <div class="dual-browser-grid">
      <!-- LEFT: BROWSER B (USER / DONOR) -->
      <div class="mock-browser user-b">
        <div class="browser-topbar">
          <div class="b-dots">
            <div class="b-dot" style="background:#ff5f56;"></div>
            <div class="b-dot" style="background:#ffbd2e;"></div>
            <div class="b-dot" style="background:#27c93f;"></div>
          </div>
          <div class="b-url">🌐 Browser B — Logged in as: Rahul (User / Donor)</div>
        </div>
        <div class="browser-body">
          <div style="font-family:var(--font-mono); font-size:0.78rem; color:var(--neon-crimson); font-weight:800;">
            STEP 1: CLICK ANY WRITE ACTION IN BROWSER B
          </div>
          <p style="font-size:0.86rem; color:var(--text-muted);">
            Jaise hi tu neeche koi button dabayega, Controller database mein `SaveChangesAsync()` karega aur `NotificationService.cs` ko trigger karega:
          </p>
          <div style="display:flex; flex-direction:column; gap:10px; margin-top:6px;">
            <button class="nav-btn crimson" style="justify-content:space-between; padding:12px 16px;" onclick="fireDualBrowserEvent('request')">
              <span>🩸 1. Post Emergency A+ Blood Request</span>
              <small style="opacity:0.8;">BloodRequestController.Create</small>
            </button>
            <button class="nav-btn amber" style="justify-content:space-between; padding:12px 16px;" onclick="fireDualBrowserEvent('contact')">
              <span>✉️ 2. Submit Contact Us Message (Invalidates Cache!)</span>
              <small style="opacity:0.8;">HomeController.Contact</small>
            </button>
            <button class="nav-btn green" style="justify-content:space-between; padding:12px 16px;" onclick="fireDualBrowserEvent('pledge')">
              <span>🤝 3. Donor Pledges on Request #42</span>
              <small style="opacity:0.8;">BloodRequestController.Offer</small>
            </button>
            <button class="nav-btn" style="justify-content:space-between; padding:12px 16px;" onclick="fireDualBrowserEvent('accept')">
              <span>✅ 4. Owner Accepts Offer (Unlocks Phone!)</span>
              <small style="opacity:0.8;">BloodRequestController.AcceptOffer</small>
            </button>
          </div>
          <div class="code-block" id="b2-code-log" style="margin-top:auto;">// Waiting for Browser B action...</div>
        </div>
      </div>

      <!-- MIDDLE: SIGNALR HUB & IMEMORYCACHE TOWER -->
      <div class="hub-middle-tower">
        <div>
          <span class="sec-tag" style="font-size:0.65rem;">SERVER ENGINE</span>
          <h4 style="font-family:var(--font-mono); color:#fff; font-size:0.9rem;">NotificationHub.cs</h4>
          <div style="font-family:var(--font-mono); font-size:0.7rem; color:var(--neon-cyan);">/hubs/notifications</div>
        </div>

        <div style="width:100%;">
          <div style="font-family:var(--font-mono); font-size:0.7rem; color:var(--neon-amber);">⚡ WEBSOCKET PIPE</div>
          <div class="laser-beam">
            <div class="laser-pulse" id="ws-laser"></div>
          </div>
          <div id="ws-group-target" style="font-family:var(--font-mono); font-size:0.72rem; color:var(--neon-green);">
            Target: Group("admins")
          </div>
        </div>

        <!-- 60s IMemoryCache Live Box -->
        <div style="background:#0b152b; border:1px solid var(--border-dim); border-radius:10px; padding:10px; width:100%;">
          <div style="font-family:var(--font-mono); font-size:0.68rem; color:var(--neon-amber); font-weight:800;">
            ⏱️ MessageCache.cs (IMemoryCache)
          </div>
          <div style="font-family:var(--font-mono); font-size:1.3rem; font-weight:800; color:#fff; margin:4px 0;" id="cache-ttl-clock">
            TTL: 60s
          </div>
          <div style="font-size:0.7rem; color:var(--text-muted);" id="cache-status-lbl">
            Cached Unread Count: <b style="color:var(--neon-green);" id="cache-val-lbl">2</b> (0 DB Hits)
          </div>
        </div>
      </div>

      <!-- RIGHT: BROWSER A (ADMIN / OWNER) -->
      <div class="mock-browser admin-b">
        <div class="browser-topbar">
          <div class="b-dots">
            <div class="b-dot" style="background:#ff5f56;"></div>
            <div class="b-dot" style="background:#ffbd2e;"></div>
            <div class="b-dot" style="background:#27c93f;"></div>
          </div>
          <div class="b-url">🛡️ Browser A — Admin / Request Owner Screen</div>
          <div class="bell-wrap" id="admin-bell-box" onclick="triggerSignalRDemo()">
            <svg class="bell-svg" viewBox="0 0 24 24"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
            <span class="bell-badge-count" id="admin-bell-count">2</span>
          </div>
        </div>
        <div class="browser-body">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-family:var(--font-mono); font-size:0.78rem; color:var(--neon-cyan); font-weight:800;">
              LIVE NOTIFICATION FEED (notifications.js)
            </span>
            <span style="font-family:var(--font-mono); font-size:0.7rem; color:var(--neon-green);">● WS Connected</span>
          </div>

          <div id="admin-live-feed" style="display:flex; flex-direction:column; gap:8px; max-height:240px; overflow-y:auto;">
            <div style="background:#0c172e; border-left:3px solid var(--neon-cyan); padding:10px 12px; border-radius:6px; font-size:0.82rem;">
              <strong style="color:#fff;">System Ready — Zero Polling Active</strong>
              <div style="color:var(--text-muted); font-size:0.76rem;">Click an action in Browser B on the left to watch real-time push!</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- MODULE 02: ZERO-TO-HERO HACKER GLOSSARY & EXPLOIT SIMULATOR -->
  <section class="cyber-section" id="sec-glossary">
    <span class="sec-tag">// MODULE 02 : "GAWAAR BHI SAMJHE" SECURITY & CONCEPT LAB</span>
    <h2 class="sec-title">🛡️ CSRF, IDOR, RowVersion, SignalR, DTO Kya Hota Hai? (Desi Story + Live Attack Lab)</h2>
    <p class="sec-desc">
      Viva mein jab Examiner puche: <i>"Beta yeh CSRF token kyun lagaya? IDOR kya hota hai? RowVersion ka kya kaam hai?"</i>—toh रट्टा mat maar! Left se topic chun, uski <b>Desi Kahani</b> padh, aur <b>Shield ON vs OFF</b> karke <b>Launch Attack</b> daba!
    </p>

    <div class="concept-layout">
      <div class="concept-list" id="concept-tabs"></div>

      <div class="concept-stage">
        <div>
          <span class="sec-tag" id="c-tag">SECURITY MECHANISM</span>
          <h3 style="font-size:1.55rem; color:#fff; margin-bottom:6px;" id="c-title">Select a Concept</h3>
          <p style="font-family:var(--font-mono); font-size:0.84rem; color:var(--neon-cyan);" id="c-files">Files Involved: ...</p>
        </div>

        <div class="explain-grid">
          <div class="info-box">
            <h4>🧠 Ekdum Desi Kahani (Gawaar Bhi 10 Second Mein Samjhe)</h4>
            <p id="c-desi" style="font-size:0.92rem;"></p>
          </div>
          <div class="info-box cyan">
            <h4>⚙️ Tere BloodConnect Code Mein Kaise Kaam Karta Hai?</h4>
            <p id="c-tech" style="font-size:0.92rem;"></p>
          </div>
        </div>

        <!-- Interactive Attack / Mechanism Simulator -->
        <div class="hack-sim-box">
          <div class="hack-header">
            <div>
              <div style="font-family:var(--font-mono); font-weight:800; color:#fff; font-size:0.95rem;">⚡ LIVE PACKET EXPLOIT & DEFENSE ARENA</div>
              <div style="font-size:0.8rem; color:var(--text-muted);">Shield ko ON ya OFF kar aur "Launch Simulation" daba kar dekh packet ke saath kya hota hai:</div>
            </div>
            <div class="shield-toggle">
              <span>SECURITY SHIELD:</span>
              <button id="shield-btn" class="toggle-btn toggle-on" onclick="toggleShield()">🛡️ SHIELD: ON</button>
              <button class="nav-btn crimson" onclick="runConceptSim()">🚀 Launch Simulation</button>
            </div>
          </div>

          <div class="packet-lane">
            <div class="packet-endpoint" id="sim-origin">💻 Hacker / Browser</div>
            <div class="shield-barrier" id="sim-barrier"></div>
            <div class="moving-packet" id="sim-packet">PAYLOAD</div>
            <div class="packet-endpoint" id="sim-target">🗄️ Controller / SQL DB</div>
          </div>

          <div class="terminal-out" id="sim-terminal">// Click "Launch Simulation" to fire the packet across the pipeline...</div>
        </div>

        <div class="info-box green">
          <h4>🎓 External Viva Examiner Ko Yeh Line Bolna (Full Marks Guaranteed):</h4>
          <p id="c-viva" style="font-size:0.93rem; font-weight:600;"></p>
        </div>
      </div>
    </div>
  </section>

  <!-- MODULE 03: SPACIOUS ARCHITECTURE MAP & AUTO-PLAY PACKET TRACER -->
  <section class="cyber-section" id="sec-arch">
    <span class="sec-tag">// MODULE 03 : 5-LAYER SYSTEM ARCHITECTURE & AUTO-PLAY PACKET TRACER</span>
    <h2 class="sec-title">🚀 End-to-End Animated Workflow Map (Auto-Play + Speed Control)</h2>
    <p class="sec-desc">
      Neeche 5 asli project workflows diye hain. Kisi bhi workflow par click kar aur <b>▶ Auto-Play Full Flow</b> daba de—upar map mein glowing packet laser sound ke saath khud ek file se dusri file mein daudega aur neeche <b>Live Cyber Terminal</b> mein us waqt chalne wala C# code aur SQL query print karega!
    </p>

    <div class="workflow-bar" id="wf-buttons"></div>

    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
      <div style="font-family:var(--font-mono); font-size:0.9rem; color:var(--neon-green);" id="wf-status">ACTIVE SCENARIO: Scenario 1 — Step 1</div>
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button class="nav-btn" onclick="stepWorkflow(-1)">◀ Prev Step</button>
        <button class="nav-btn green" id="autoplay-btn" onclick="toggleAutoPlay()">▶ Auto-Play Full Flow</button>
        <button class="nav-btn crimson" onclick="stepWorkflow(1)">Next Step ▶</button>
      </div>
    </div>

    <div class="arch-stage-wrap">
      <div class="arch-canvas" id="arch-canvas">
        <div class="arch-lane" style="top:15px; height:145px;"><div class="arch-lane-title">LAYER 1 : CLIENT BROWSER, RAZOR VIEWS (.CSHTML), NOTIFICATIONS.JS & POSTMAN</div></div>
        <div class="arch-lane" style="top:180px; height:135px;"><div class="arch-lane-title">LAYER 2 : STARTUP & SECURITY GATEWAY (PROGRAM.CS, CSRF FILTER, COOKIE BAN VALIDATOR)</div></div>
        <div class="arch-lane" style="top:335px; height:195px;"><div class="arch-lane-title">LAYER 3 : MVC CONTROLLERS, REST API CONTROLLERS & SIGNALR WEBSOCKET HUB</div></div>
        <div class="arch-lane" style="top:550px; height:165px;"><div class="arch-lane-title">LAYER 4 : SERVICES & DOMAIN BRAIN (NOTIFICATIONSERVICE, MESSAGECACHE, BLOODCOMPATIBILITY, DTOS)</div></div>
        <div class="arch-lane" style="top:735px; height:130px;"><div class="arch-lane-title">LAYER 5 : DATA PERSISTENCE (APPLICATIONDBCONTEXT, DBSEEDER, ENTITY MODELS & SQL SERVER)</div></div>

        <svg id="arch-svg"></svg>
        <div id="arch-nodes"></div>
      </div>
    </div>

    <div class="step-console">
      <div>
        <div class="sec-tag" id="sc-step-num">STEP 1 OF 8</div>
        <h3 style="font-size:1.3rem; color:#fff; margin-bottom:10px;" id="sc-node-title">Views/BloodRequest/Create.cshtml</h3>
        <p style="font-size:0.95rem; color:var(--text-main);" id="sc-explanation"></p>
      </div>
      <div>
        <div class="sec-tag">// LIVE SERVER / PACKET TRACE</div>
        <div class="code-block" id="sc-code" style="min-height:130px;"></div>
      </div>
    </div>
  </section>

  <!-- MODULE 04: INTERACTIVE BLOOD BAG TRANSFUSION & PLEDGE STATE MACHINE LAB -->
  <section class="cyber-section" id="sec-domain">
    <span class="sec-tag">// MODULE 04 : MEDICAL BLOOD BAG TRANSFUSION & TWO-WAY PLEDGE SIMULATOR</span>
    <h2 class="sec-title">🧬 Live Blood Transfusion Tube Tester & Two-Way Pledge Lock/Unlock Lab</h2>
    <p class="sec-desc">
      Left side mein pehle <b>Patient (Recipient) Blood Group</b> chun, phir kisi bhi <b>Donor Blood Group</b> par click karke dekh ki pipe mein khoon safely chadh raha hai (Green) ya RBC Clumping/Reaction (Red Alarm) ho raha hai! Right side mein <b>Two-Way Pledge State Machine</b> chala kar dekh ki Phone Number kab Lock 🔒 rehta hai aur kab Unlock 🔓 hota hai.
    </p>

    <div class="lab-two-col">
      <!-- Blood Matrix & Transfusion Tube Tester -->
      <div class="state-machine-card">
        <div class="sec-tag">FILE: Models/BloodCompatibility.cs</div>
        <h3 style="color:#fff; font-size:1.15rem; margin-bottom:4px;">1️⃣ Patient Needs Blood Group (Select Recipient):</h3>
        <div class="bg-grid" id="recipient-grid"></div>

        <h3 style="color:var(--neon-green); font-size:1.15rem; margin-top:14px;">2️⃣ Click Any Donor Group to Test Transfusion:</h3>
        <div class="bg-grid" id="donor-grid"></div>

        <!-- Animated Blood Bag Transfusion Tube -->
        <div class="transfusion-stage">
          <div class="blood-bag">
            <div class="bag-fill" id="donor-bag-fill"></div>
            <span style="font-size:0.65rem; color:#cbd5e1;">DONOR</span>
            <span style="font-size:1.3rem; color:#fff;" id="bag-donor-lbl">B+</span>
          </div>
          <div style="flex:1; display:flex; flex-direction:column; align-items:center; gap:6px;">
            <div id="transfusion-verdict" style="font-family:var(--font-mono); font-size:0.78rem; font-weight:800; color:var(--neon-green);">
              ✅ SAFE RBC TRANSFUSION (EXACT MATCH)
            </div>
            <div class="iv-tube">
              <div class="iv-flow" id="iv-tube-flow" style="width:100%;"></div>
            </div>
            <div style="font-family:var(--font-mono); font-size:0.68rem; color:var(--text-muted);">
              BloodCompatibility.CanDonate(donor, recipient)
            </div>
          </div>
          <div class="blood-bag">
            <div class="bag-fill" id="rec-bag-fill" style="height:80%;"></div>
            <span style="font-size:0.65rem; color:#cbd5e1;">PATIENT</span>
            <span style="font-size:1.3rem; color:#fff;" id="bag-rec-lbl">B+</span>
          </div>
        </div>

        <div class="code-block" id="compat-code-out" style="margin-top:14px;"></div>
      </div>

      <!-- Pledge State Machine Simulator -->
      <div class="state-machine-card">
        <div class="sec-tag">FILES: BloodRequestController.cs + DonationOffer.cs</div>
        <h3 style="color:#fff; font-size:1.22rem; margin-bottom:6px;">🤝 Two-Way Pledge & Contact Privacy Vault</h3>
        <p style="font-size:0.85rem; color:var(--text-muted);">
          Neeche 1 se 4 tak buttons daba kar dekh ki Request aur Offer ka status kaise badalta hai, competing offers kaise auto-reject hote hain, aur Donor ka Phone Number kab khulta hai:
        </p>

        <div class="sm-badges" id="sm-states">
          <div class="sm-step current" id="st-active">1. Request: ACTIVE</div>
          <div class="sm-step" id="st-pledged">2. Offer: PLEDGED</div>
          <div class="sm-step" id="st-accepted">3. Offer: ACCEPTED (InProgress)</div>
          <div class="sm-step" id="st-fulfilled">4. Request: FULFILLED</div>
        </div>

        <!-- Live Contact Privacy Vault Indicator -->
        <div class="privacy-vault locked" id="privacy-vault-box">
          <span id="pv-icon">🔒 CONTACT PRIVACY SHIELD: LOCKED</span>
          <span id="pv-phone">Donor Phone: +91-XXXXXXXXXX (Hidden via DTO)</span>
        </div>

        <div style="display:flex; gap:8px; flex-wrap:wrap; margin:14px 0;">
          <button class="nav-btn" onclick="setPledgeState(0)">1️⃣ Post Request</button>
          <button class="nav-btn" onclick="setPledgeState(1)">2️⃣ Donor A & B Pledge</button>
          <button class="nav-btn green" onclick="setPledgeState(2)">3️⃣ Owner Accepts Donor A</button>
          <button class="nav-btn crimson" onclick="setPledgeState(3)">4️⃣ Mark Completed</button>
        </div>

        <div class="terminal-out" id="pledge-terminal" style="min-height:185px;"></div>
      </div>
    </div>
  </section>

  <!-- MODULE 05: ALL 32 FILES DEEP ENCYCLOPEDIA -->
  <section class="cyber-section" id="sec-files">
    <span class="sec-tag">// MODULE 05 : EXHAUSTIVE 32-FILE CODEBASE ENCYCLOPEDIA</span>
    <h2 class="sec-title">📂 Har Ek File Ki Kundali (All 32 Project Files Explained in Hinglish)</h2>
    <p class="sec-desc">
      Yahan tere project ki <b>32 ki 32 files</b> ki poori kundali hai. Search box mein kuch bhi likh (`RowVersion`, `SignalR`, `Cookie`, `DTO`, `DbSeeder`) ya category button daba—har file ka Desi kaam, methods, code snippet, aur Viva answer turant saamne aa jayega!
    </p>

    <div class="filter-bar">
      <input type="text" id="file-search" class="search-input" placeholder="🔍 Search any file, method, or keyword (e.g., Program.cs, NotificationHub, RowVersion, DTO)..." oninput="renderFileCards()">
      <button class="nav-btn" onclick="filterCategory('ALL')">All (32)</button>
      <button class="nav-btn" onclick="filterCategory('BOOT & CONFIG')">Boot & Config (4)</button>
      <button class="nav-btn" onclick="filterCategory('MVC CONTROLLER')">MVC Controllers (6)</button>
      <button class="nav-btn" onclick="filterCategory('REST API')">REST APIs (3)</button>
      <button class="nav-btn" onclick="filterCategory('REALTIME & CACHE')">SignalR & Services (3)</button>
      <button class="nav-btn" onclick="filterCategory('DOMAIN & DB')">Models & DB (12)</button>
      <button class="nav-btn" onclick="filterCategory('FRONTEND UI')">Views, JS & CSS (4)</button>
    </div>

    <div class="file-grid" id="file-cards-container"></div>
  </section>

  <!-- MODULE 06: POSTMAN & COOKIE AUTH LAB -->
  <section class="cyber-section" id="sec-postman">
    <span class="sec-tag">// MODULE 06 : REST API & POSTMAN SECURITY SUITE</span>
    <h2 class="sec-title">📡 Postman Cookie Jar + DTO Privacy + IDOR Testing Simulator</h2>
    <p class="sec-desc">
      Tere project mein <b>JWT Token nahi, Cookie Authentication (`.AspNetCore.Identity.Application`)</b> hai. Neeche ke 4 Postman test scenarios par click kar aur dekh ki 28 Postman tests mein tune kya verify kiya hai:
    </p>

    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:20px;">
      <button class="nav-btn" onclick="runPostmanTest(0)">1. POST /api/auth/login (Get Cookie)</button>
      <button class="nav-btn" onclick="runPostmanTest(1)">2. GET /api/donor/search?bloodGroup=B%2B (DTO Privacy)</button>
      <button class="nav-btn crimson" onclick="runPostmanTest(2)">3. PUT /api/donor/15 (IDOR Attack ➔ 403 Forbidden)</button>
      <button class="nav-btn amber" onclick="runPostmanTest(3)">4. POST /api/donor (SQLi & Regex Validation Test)</button>
    </div>

    <div class="step-console">
      <div>
        <div class="sec-tag">// HTTP REQUEST SENT BY POSTMAN</div>
        <div class="code-block" id="pm-req" style="min-height:190px;"></div>
      </div>
      <div>
        <div class="sec-tag">// ASP.NET CORE API RESPONSE & INTERNAL EXPLANATION</div>
        <div class="code-block" id="pm-res" style="min-height:190px; color:var(--neon-green);"></div>
      </div>
    </div>
  </section>

  <!-- MODULE 07: GUJARAT UNIVERSITY EXTERNAL VIVA RAPID-FIRE FLASHCARDS -->
  <section class="cyber-section" id="sec-viva">
    <span class="sec-tag">// MODULE 07 : GUJARAT UNIVERSITY BCA SEM-7 EXTERNAL VIVA DECK</span>
    <h2 class="sec-title">🎓 12 Most-Asked External Viva Questions (Click Any Card to Reveal Answer)</h2>
    <p class="sec-desc">
      External Examiner (`DSC-M-BCA-471P`) jo sabse tedhe-medhe sawaal puch sakta hai, unke exact to-the-point jawab neeche diye hain. Kisi bhi card par click kar:
    </p>
    <div class="viva-grid" id="viva-deck-container"></div>
  </section>

</div>

<script>
// ============================================================================
// 1. SCROLL PROGRESS & INTERACTIVE RBC + CYBER PARTICLE BACKGROUND CANVAS
// ============================================================================
window.addEventListener('scroll', () => {
  const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  document.getElementById('scroll-bar').style.width = ((winScroll / height) * 100) + "%";
});

const bgCanvas = document.getElementById('bg-canvas');
const bgCtx = bgCanvas.getContext('2d');
function resizeBg() { bgCanvas.width = window.innerWidth; bgCanvas.height = window.innerHeight; }
resizeBg(); window.addEventListener('resize', resizeBg);

const particles = Array.from({length: 60}, () => ({
  x: Math.random() * window.innerWidth,
  y: Math.random() * window.innerHeight,
  r: Math.random() * 3 + 1.2,
  vx: (Math.random() - 0.5) * 0.4,
  vy: Math.random() * 0.75 + 0.2,
  color: Math.random() > 0.45 ? '#ff0055' : '#00f0ff'
}));

function animateBg() {
  bgCtx.clearRect(0, 0, bgCanvas.width, bgCanvas.height);
  particles.forEach(p => {
    p.x += p.vx; p.y += p.vy;
    if (p.y > bgCanvas.height) { p.y = 0; p.x = Math.random() * bgCanvas.width; }
    if (p.x > bgCanvas.width) p.x = 0;
    if (p.x < 0) p.x = bgCanvas.width;
    bgCtx.beginPath();
    bgCtx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    bgCtx.fillStyle = p.color;
    bgCtx.fill();
  });
  requestAnimationFrame(animateBg);
}
animateBg();

// ============================================================================
// 2. 6-CHANNEL WEB AUDIO SYNTHESIZER ENGINE (PROCEDURAL SOUNDS)
// ============================================================================
let audioMuted = false;
function toggleAudioMute() {
  audioMuted = !audioMuted;
  const btn = document.getElementById('mute-btn');
  btn.innerText = audioMuted ? '🔇 Sound: MUTED' : '🔊 Sound: ON';
  btn.className = audioMuted ? 'nav-btn crimson' : 'nav-btn green';
}

function getAudioCtx() {
  if (audioMuted) return null;
  return new (window.AudioContext || window.webkitAudioContext)();
}

function playCyberClick(freq = 560) {
  try {
    const ctx = getAudioCtx(); if (!ctx) return;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(freq, ctx.currentTime);
    gain.gain.setValueAtTime(0.08, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.07);
    osc.connect(gain); gain.connect(ctx.destination);
    osc.start(); osc.stop(ctx.currentTime + 0.08);
  } catch(e) {}
}

function playLaserWhoosh() {
  try {
    const ctx = getAudioCtx(); if (!ctx) return;
    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(280, now);
    osc.frequency.exponentialRampToValueAtTime(1150, now + 0.18);
    osc.frequency.exponentialRampToValueAtTime(420, now + 0.32);
    gain.gain.setValueAtTime(0.12, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.34);
    osc.connect(gain); gain.connect(ctx.destination);
    osc.start(now); osc.stop(now + 0.35);
  } catch(e) {}
}

function playShieldBlockSound() {
  try {
    const ctx = getAudioCtx(); if (!ctx) return;
    const now = ctx.currentTime;
    [523.25, 659.25, 1046.5].forEach((f, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(f, now + i * 0.06);
      gain.gain.setValueAtTime(0.15, now + i * 0.06);
      gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.06 + 0.25);
      osc.connect(gain); gain.connect(ctx.destination);
      osc.start(now + i * 0.06); osc.stop(now + i * 0.06 + 0.26);
    });
  } catch(e) {}
}

function playHackAlarmSound() {
  try {
    const ctx = getAudioCtx(); if (!ctx) return;
    const now = ctx.currentTime;
    [220, 165, 220, 145].forEach((f, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(f, now + i * 0.12);
      gain.gain.setValueAtTime(0.14, now + i * 0.12);
      gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.12 + 0.11);
      osc.connect(gain); gain.connect(ctx.destination);
      osc.start(now + i * 0.12); osc.stop(now + i * 0.12 + 0.12);
    });
  } catch(e) {}
}

function playHeartbeatSound() {
  try {
    const ctx = getAudioCtx(); if (!ctx) return;
    const now = ctx.currentTime;
    [110, 95].forEach((f, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(f, now + i * 0.16);
      gain.gain.setValueAtTime(0.28, now + i * 0.16);
      gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.16 + 0.12);
      osc.connect(gain); gain.connect(ctx.destination);
      osc.start(now + i * 0.16); osc.stop(now + i * 0.16 + 0.14);
    });
  } catch(e) {}
}

function playDbCommitSound() {
  try {
    const ctx = getAudioCtx(); if (!ctx) return;
    const now = ctx.currentTime;
    [587.33, 880].forEach((f, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(f, now + i * 0.08);
      gain.gain.setValueAtTime(0.14, now + i * 0.08);
      gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.08 + 0.22);
      osc.connect(gain); gain.connect(ctx.destination);
      osc.start(now + i * 0.08); osc.stop(now + i * 0.08 + 0.24);
    });
  } catch(e) {}
}

function triggerSignalRDemo(title = "New A+ Critical Request!", body = "Rahul Sharma · Ahmedabad, Gujarat (Pushed via SignalR WebSocket)") {
  try {
    const ctx = getAudioCtx();
    if (ctx) {
      const now = ctx.currentTime;
      [880, 1174.66].forEach((freq, i) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now + i * 0.11);
        gain.gain.setValueAtTime(0.001, now + i * 0.11);
        gain.gain.exponentialRampToValueAtTime(0.24, now + i * 0.11 + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + i * 0.11 + 0.45);
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start(now + i * 0.11); osc.stop(now + i * 0.11 + 0.46);
      });
    }
  } catch(e) {}
  const t = document.getElementById('live-toast');
  document.getElementById('lt-title').innerText = title;
  document.getElementById('lt-body').innerText = body;
  t.style.display = 'block';
  setTimeout(() => { t.style.display = 'none'; }, 4800);
}

// ============================================================================
// 3. MODULE 01: TWO-BROWSER LIVE SIGNALR & 60s CACHE COUNTDOWN
// ============================================================================
let cacheSeconds = 60;
let cachedUnread = 2;
setInterval(() => {
  cacheSeconds = cacheSeconds > 1 ? cacheSeconds - 1 : 60;
  const el = document.getElementById('cache-ttl-clock');
  if (el) el.innerText = `TTL: ${cacheSeconds}s`;
}, 1000);

function fireDualBrowserEvent(type) {
  playLaserWhoosh();
  const laser = document.getElementById('ws-laser');
  laser.classList.remove('shoot-right');
  void laser.offsetWidth;
  laser.classList.add('shoot-right');

  const log = document.getElementById('b2-code-log');
  const groupLbl = document.getElementById('ws-group-target');
  let notifTitle = "", notifBody = "", borderCol = "var(--neon-cyan)";

  if (type === 'request') {
    log.innerText = `// BloodRequestController.Create\n_context.BloodRequests.Add(request);\nawait _context.SaveChangesAsync();\nawait _notifications.PushNewRequestToAdminsAsync(request);`;
    groupLbl.innerText = `Target: Clients.Group("admins")`;
    notifTitle = "🩸 New A+ Critical Blood Request";
    notifBody = "Patient: Rahul Sharma · Civil Hospital, Ahmedabad";
    borderCol = "var(--neon-crimson)";
  } else if (type === 'contact') {
    cachedUnread++;
    cacheSeconds = 60;
    document.getElementById('cache-val-lbl').innerText = cachedUnread;
    document.getElementById('cache-status-lbl').innerHTML = `<span style="color:var(--neon-amber);">⚡ Cache Invalidated & Rebuilt! Count = ${cachedUnread}</span>`;
    log.innerText = `// HomeController.Contact\n_context.ContactMessages.Add(msg);\nawait _context.SaveChangesAsync();\n_messageCache.Invalidate(); // Clears 60s RAM Cache!\nawait _notifications.PushNewContactMessageToAdminsAsync(msg);`;
    groupLbl.innerText = `Target: Clients.Group("admins") + Cache Reset`;
    notifTitle = "✉️ New Contact Message Received";
    notifBody = "Subject: Urgent Blood Camp Inquiry (Unread Badge Updated)";
    borderCol = "var(--neon-amber)";
  } else if (type === 'pledge') {
    log.innerText = `// BloodRequestController.Offer\n_context.DonationOffers.Add(newOffer);\nawait _context.SaveChangesAsync();\nawait _notifications.PushNewOfferToOwnerAsync(request, newOffer);`;
    groupLbl.innerText = `Target: Clients.Group("user_{ownerId}")`;
    notifTitle = "🤝 Donor Pledged on Request #42!";
    notifBody = "Donor: Gaurav (B+) has pledged to donate. Review offer now!";
    borderCol = "var(--neon-green)";
  } else if (type === 'accept') {
    log.innerText = `// BloodRequestController.AcceptOffer\noffer.Status = DomainValues.Accepted;\nforeach(var o in competing) o.Status = DomainValues.Rejected;\nawait _notifications.PushOfferStatusToDonorAsync(donorUserId, "Accepted", 42);`;
    groupLbl.innerText = `Target: Clients.Group("user_{donorId}")`;
    notifTitle = "✅ Offer Accepted — Contact Unlocked!";
    notifBody = "Request Owner accepted your pledge! Phone: +91-9876543210";
    borderCol = "var(--neon-cyan)";
  }

  setTimeout(() => {
    triggerSignalRDemo(notifTitle, notifBody);
    const bellBox = document.getElementById('admin-bell-box');
    const badge = document.getElementById('admin-bell-count');
    bellBox.classList.remove('ringing');
    void bellBox.offsetWidth;
    bellBox.classList.add('ringing');

    const nextCount = parseInt(badge.innerText) + 1;
    badge.innerText = nextCount;
    badge.classList.add('bounce');
    setTimeout(() => badge.classList.remove('bounce'), 300);

    const feed = document.getElementById('admin-live-feed');
    const item = document.createElement('div');
    item.style.cssText = `background:#0c172e; border-left:4px solid ${borderCol}; padding:10px 12px; border-radius:6px; font-size:0.82rem; animation:toastPop 0.25s ease-out;`;
    item.innerHTML = `<div style="display:flex; justify-content:space-between;"><strong style="color:#fff;">${notifTitle}</strong><span style="font-family:var(--font-mono); font-size:0.68rem; color:var(--neon-green);">Just now</span></div><div style="color:var(--text-muted); font-size:0.78rem; margin-top:3px;">${notifBody}</div>`;
    feed.prepend(item);
  }, 520);
}

// ============================================================================
// 4. MODULE 02: ZERO-TO-HERO HACKER GLOSSARY & EXPLOIT LAB DATA
// ============================================================================
const CONCEPTS = [
  {
    id: "csrf",
    name: "1. CSRF (Cross-Site Request Forgery)",
    short: "Nakli website se tere active login ka galat fayda uthana",
    files: "Program.cs (AutoValidateAntiforgeryToken) + All Razor Forms (__RequestVerificationToken)",
    desi: "Maan le tu BloodConnect par Admin ban kar login hai. Ab tune dusre tab mein ek nakli website kholi ('Free iPhone Jeeto'). Us nakli site ke button ke peeche chhupa code tere browser se BloodConnect ko order bhejta hai: 'POST /Admin/DeleteUser/5'. Kyunki browser har request ke saath teri Login Cookie apne aap bhej deta hai, bina CSRF security ke user delete ho jayega! CSRF Token ek 'Secret OTP Stamp' jaisa hai jo sirf asli BloodConnect form ke paas hota hai.",
    tech: "Tere `Program.cs` mein `options.Filters.Add(new AutoValidateAntiforgeryTokenAttribute())` laga hai. Jab bhi Razor View (`@Html.AntiForgeryToken()`) form banata hai, woh ek secret `__RequestVerificationToken` chhupa deta hai jo nakli website ke paas nahi ho sakta. Agar woh token match na ho, toh server `400 Bad Request` maar kar request tod deta hai!",
    viva: "Sir, Cookie authentication mein browser cookies auto-attach karta hai, isliye CSRF ka khatra rehta hai. Humne `Program.cs` mein global `AutoValidateAntiforgeryToken` lagaya hai jo har POST/PUT/DELETE form par cryptographic antiforgery token verify karta hai.",
    packetLabel: "POST /BloodRequest/Delete/10",
    onLog: "[SHIELD ON] Incoming POST /BloodRequest/Delete/10 from evil-lottery-site.com\n[CHECK 1] Cookie '.AspNetCore.Identity.Application' is present.\n[CHECK 2] Validating __RequestVerificationToken field...\n[🛡️ BLOCKED 400 BAD REQUEST] Antiforgery token missing! Attack crushed by Program.cs.",
    offLog: "[SHIELD OFF] Incoming POST /BloodRequest/Delete/10 from evil-lottery-site.com\n[WARNING] No Antiforgery validation active!\n[💥 HACKED 200 OK] Browser sent valid login cookie -> BloodRequest #10 DELETED without user knowing!"
  },
  {
    id: "idor",
    name: "2. IDOR (Insecure Direct Object Reference)",
    short: "URL ya API mein ID badal kar dusre user ka data chhedna",
    files: "DonorController.cs + BloodRequestController.cs + DonorApiController.cs",
    desi: "Maan le hostel mein tere kamre ki chaabi (Login) tere paas hai. Tera kamra number `15` hai (`/Donor/Edit/15`). Ab tune socha 'Main hotel ke andar toh aa hi gaya hoon, chalo kamra number `16` (`/Donor/Edit/16`) ka taala khol kar Gaurav ka samaan badal deta hoon!' Agar gatekeeper sirf yeh dekhe ki 'banda andar hai' aur yeh na check kare ki 'kamra #16 iska hai ya nahi', toh isko IDOR kehte hain!",
    tech: "Tere `DonorController` aur `DonorApiController` mein har Edit/Delete action ke andar **Ownership Check** likha hai: `if (donor.UserId != currentUserId && !User.IsInRole(\"Admin\")) return Forbid();`. Yaani login hona kaafi nahi hai—us record ka `UserId` tere `ClaimTypes.NameIdentifier` se match hona zaroori hai!",
    viva: "Sir, IDOR rokne ke liye humne sirf `[Authorize]` par bharosa nahi kiya, balki har state-changing action mein database entity ka `UserId` current logged-in user ke ID se compare kiya hai. Mismatch hone par `403 Forbidden` return hota hai.",
    packetLabel: "PUT /api/donor/16 (By User #15)",
    onLog: "[SHIELD ON] User #15 sent PUT /api/donor/16\n[DB FETCH] Donor #16 belongs to UserId = 'user-99-gaurav'\n[OWNERSHIP CHECK] donor.UserId != currentUserId ('user-15-prince')\n[🛡️ BLOCKED 403 FORBIDDEN] IDOR attempt stopped by DonorApiController!",
    offLog: "[SHIELD OFF] User #15 sent PUT /api/donor/16\n[WARNING] Only [Authorize] checked, ownership ignored!\n[💥 HACKED 200 OK] User #15 successfully overwrote Donor #16's profile!"
  },
  {
    id: "concurrency",
    name: "3. Optimistic Concurrency (RowVersion)",
    short: "Ek hi millisecond par do logon ke update karne par data bachana",
    files: "Models/Donor.cs ([Timestamp] byte[] RowVersion) + DonorController.cs",
    desi: "Maan le ek joint bank account ke do ATM card hain. Pati aur Patni dono ne 12:00:01 baje alag-alag ATM se paise nikale. Agar bank har transaction par 'Version Number' check na kare, toh ek ka update dusre ke update ko chupke se mita dega! `RowVersion` har row par ek 'Receipt Version Stamp' lagata hai—agar beech mein kisi ne row badal di, toh purani receipt wala save ruk jaata hai!",
    tech: "Tere `Donor.cs` mein `[Timestamp] public byte[]? RowVersion { get; set; }` laga hai. SQL Server har baar row update hone par is `RowVersion` ka binary number (`0x...7D1` -> `0x...7D2`) badal deta hai. Jab EF Core `UPDATE` chalata hai, woh check karta hai `WHERE DonorId = 15 AND RowVersion = @oldVersion`. Mismatch hone par `DbUpdateConcurrencyException` aata hai!",
    viva: "Sir, `Donor.cs` mein humne `[Timestamp] byte[] RowVersion` use kiya hai jo SQL Server mein `rowversion` column banata hai. Update ke waqt EF Core concurrency token match karta hai aur race condition hone par `DbUpdateConcurrencyException` throw karta hai.",
    packetLabel: "UPDATE Donors WHERE RowVersion=0x7D1",
    onLog: "[SHIELD ON] Tab B tries to save Donor #15 with old RowVersion 0x00000000000007D1\n[SQL SERVER] Current RowVersion in DB is already 0x00000000000007D2!\n[🛡️ CAUGHT] DbUpdateConcurrencyException caught in DonorController -> Lost update prevented!",
    offLog: "[SHIELD OFF] Tab B saves Donor #15 without RowVersion check.\n[💥 DATA CORRUPTION] Tab A's changes silently overwritten and lost forever!"
  },
  {
    id: "signalr",
    name: "4. SignalR WebSocket ('Walkie-Talkie Line')",
    short: "Bina page refresh kiye server se browser mein live push bhejna",
    files: "Hubs/NotificationHub.cs + Services/NotificationService.cs + wwwroot/js/notifications.js",
    desi: "Normal HTTP ek **Daakiye (Postman)** jaisa hai—jab tak tu chitthi bhej kar puchta nahi (Page Refresh F5), server samne se kuch nahi bolta. Par SignalR WebSocket ek **Live Walkie-Talkie Line** hai jo browser khulte hi server (`NotificationHub.cs`) aur browser (`notifications.js`) ke beech jud jaati hai. Server jab chahe is taar se 8 millisecond mein घंटी aur popup bhej sakta hai!",
    tech: "Connection judte hi `NotificationHub.OnConnectedAsync()` Admin ko `admins` group mein aur har user ko `user_{userId}` group mein daal deta hai. Jab `BloodRequestController` mein write hota hai, `NotificationService` `IHubContext` se `Clients.Group(\"admins\").SendAsync(\"ReceiveNotification\", payload)` fire karta hai.",
    viva: "Sir, humne polling bilkul use nahi ki. SignalR persistent WebSocket connection banata hai aur Role-based (`admins`) plus User-specific (`user_{id}`) groups mein targeted real-time push bhejta hai.",
    packetLabel: "WS FRAME -> ReceiveNotification",
    onLog: "[SIGNALR ACTIVE] BloodRequest saved to SQL Server.\n[HUB PUSH] NotificationService -> Clients.Group('admins').SendAsync('ReceiveNotification')\n[⚡ LIVE BROWSER] notifications.js received frame in 8ms -> Played 880Hz+1174Hz chime + Toast!",
    offLog: "[SIGNALR DISABLED] BloodRequest saved to SQL Server.\n[💤 SILENCE] Admin screen sits dead. Admin has no idea an emergency request arrived until manual F5 refresh."
  },
  {
    id: "ban_kickout",
    name: "5. Cookie Auth + Instant Ban Kickout",
    short: "Admin ke Ban dabate hi 7-din wali Cookie ko agle click par todna",
    files: "Program.cs (OnValidatePrincipal) + AdminController.cs + Models/AppUser.cs (IsBanned)",
    desi: "Maan le kisi ne 7-din ka Gym Pass (Login Cookie) banwa liya. Ab 2nd din usne gym mein tod-phod ki aur Malik (Admin) ne usko Register mein 'Banned' likh diya. Agar gate par khada Guard sirf uska 7-din wala Pass dekhe aur Register check na kare, toh woh gunda 5 din aur gym aayega! Tere `Program.cs` ka Guard (`OnValidatePrincipal`) har kadam par Register (`IsBanned`) check karke uska Pass turant phaad deta hai!",
    tech: "`Program.cs` ke Cookie Authentication options mein `OnValidatePrincipal` event har HTTP request par chalta hai. Woh `UserManager` se user ka latest `IsBanned` flag check karta hai. Agar `user.IsBanned == true` nikla, toh `context.RejectPrincipal()` aur `SignOutAsync()` chala kar turant session khatam kar deta hai.",
    viva: "Sir, Cookie sliding expiration 7 days hai, par immediate revocation ke liye humne `CookieAuthenticationEvents.OnValidatePrincipal` hook kiya hai jo har request par `AppUser.IsBanned` verify karke banned user ko instant sign-out kar deta hai.",
    packetLabel: "GET /Dashboard (Banned User Cookie)",
    onLog: "[SHIELD ON] Banned user clicks /Dashboard with valid 7-day Cookie.\n[MIDDLEWARE] Program.cs -> OnValidatePrincipal intercepts request.\n[DB CHECK] AppUser.IsBanned == true!\n[🛡️ KICKOUT] context.RejectPrincipal() + SignOutAsync() -> Redirected to /Account/Login!",
    offLog: "[SHIELD OFF] Banned user clicks /Dashboard.\n[💥 BYPASS] Cookie signature is valid for 7 days -> Banned user continues using the site freely!"
  },
  {
    id: "dto_privacy",
    name: "6. DTO Pattern ('Chai Ki Chhanni' Privacy Shield)",
    short: "API aur Search mein Donor ka mobile number chhupa kar rakhna",
    files: "Models/ApiDtos.cs (DonorDto, BloodRequestDto) + DonorApiController.cs",
    desi: "Jab hum chai banate hain toh patti aur adrak pateele (`Donor` Database Table) mein rehte hain, par cup (`API JSON Response`) mein daalte waqt beech mein **Chhanni (`DonorDto`)** lagate hain taaki kachra/patti cup mein na jaaye! Waise hi database mein donor ka `ContactNumber` aur `UserId` hai, par `DonorDto` ki chhanni unko rok leti hai taaki koi scraper saare phone numbers chori na kar sake!",
    tech: "`Models/ApiDtos.cs` mein `DonorDto` class hai jisme sirf `DonorId`, `Name`, `BloodGroup`, `State`, `Location`, `IsAvailable` properties hain—`ContactNumber` aur `UserId` hai hi nahi! Phone number sirf website ke andar tab dikhta hai jab Request Owner kisi Donor ka Pledge **Accept** kar leta hai.",
    viva: "Sir, Entity models ko seedha API mein expose karne se Sensitive Data Exposure aur Over-posting hoti hai. Isliye humne `ApiDtos.cs` banaya hai jo public API responses se `ContactNumber` aur `UserId` ko strip kar deta hai.",
    packetLabel: "GET /api/donor/15",
    onLog: "[SHIELD ON] Client requests GET /api/donor/15\n[MAPPER] DonorApiController maps Donor entity -> DonorDto\n[🛡️ SAFE JSON] { \"donorId\": 15, \"name\": \"Gaurav\", \"bloodGroup\": \"B+\", \"state\": \"Bihar\" } (Phone hidden!)",
    offLog: "[SHIELD OFF] Client requests GET /api/donor/15\n[💥 PII LEAKED] { \"donorId\": 15, \"contactNumber\": \"9876543210\", \"userId\": \"guid-123\", \"rowVersion\": \"...\" }"
  },
  {
    id: "xss_sqli",
    name: "7. XSS & SQL Injection (SQLi) Defense",
    short: "Form mein Hacker Script ya SQL Command daal kar site todna",
    files: "Views/*.cshtml (Razor Encoding) + ApplicationDbContext.cs (EF Core Parameterized SQL)",
    desi: "Hacker do chalaki karta hai: (1) Naam ke dabbe mein `<script>stealCookie()</script>` likh deta hai taaki jab Admin woh naam dekhe toh Admin ke browser mein jasoosi code chal jaaye (XSS). (2) Search box mein `' OR 1=1 --` likhta hai taaki database ka taala toot jaaye (SQLi). Razor View `<script>` ke daant tod kar usko sadharan text bana deta hai, aur EF Core SQL command ko `@p0` pinjre mein band kar deta hai!",
    tech: "1. **XSS Defense:** Razor Views mein jab bhi `@item.RequesterName` likhte hain, ASP.NET Core automatically `<` ko `&lt;` aur `>` ko `&gt;` mein encode kar deta hai. 2. **SQLi Defense:** EF Core kabhi string concatenation nahi karta; woh har LINQ query ko `@p0` parameterized SQL bana kar bhejta hai.",
    viva: "Sir, SQL Injection ko EF Core ke parameterized queries (`sp_executesql` with `@p0`) rokte hain, aur Reflected/Stored XSS ko Razor View Engine ki default HTML output encoding rokti hai.",
    packetLabel: "Input: <script> / ' OR 1=1--",
    onLog: "[SHIELD ON] Hacker submits Name = '<script>steal()</script>' and Search = \"' OR 1=1 --\"\n[EF CORE] Executes: SELECT * FROM Donors WHERE BloodGroup = @p0 (Literal parameter)\n[🛡️ RAZOR VIEW] Renders: &lt;script&gt;steal()&lt;/script&gt; (Harmless text!)",
    offLog: "[SHIELD OFF] Raw SQL concatenation & Html.Raw() used!\n[💥 COMPROMISED] SQL query hijacked + Malicious JavaScript executed in Admin's browser!"
  }
];

let currentConceptIdx = 0;
let shieldOn = true;

function initConcepts() {
  const list = document.getElementById('concept-tabs');
  list.innerHTML = '';
  CONCEPTS.forEach((c, idx) => {
    const btn = document.createElement('button');
    btn.className = 'concept-tab' + (idx === 0 ? ' active' : '');
    btn.innerHTML = `<strong>${c.name}</strong><span>${c.short}</span>`;
    btn.onclick = () => { playCyberClick(640); selectConcept(idx); };
    list.appendChild(btn);
  });
  selectConcept(0);
}

function selectConcept(idx) {
  currentConceptIdx = idx;
  document.querySelectorAll('.concept-tab').forEach((b, i) => b.classList.toggle('active', i === idx));
  const c = CONCEPTS[idx];
  document.getElementById('c-title').innerText = c.name;
  document.getElementById('c-files').innerText = "📂 Files Involved: " + c.files;
  document.getElementById('c-desi').innerText = c.desi;
  document.getElementById('c-tech').innerText = c.tech;
  document.getElementById('c-viva').innerText = `"${c.viva}"`;
  document.getElementById('sim-packet').innerText = c.packetLabel;
  document.getElementById('sim-terminal').innerText = `// Ready to test ${c.name}. Toggle Shield ON/OFF and click "Launch Simulation"...`;
}

function toggleShield() {
  shieldOn = !shieldOn;
  playCyberClick(shieldOn ? 820 : 280);
  const btn = document.getElementById('shield-btn');
  const barrier = document.getElementById('sim-barrier');
  btn.className = 'toggle-btn ' + (shieldOn ? 'toggle-on' : 'toggle-off');
  btn.innerText = shieldOn ? '🛡️ SHIELD: ON' : '⚠️ SHIELD: OFF';
  barrier.classList.toggle('off', !shieldOn);
}

function runConceptSim() {
  playLaserWhoosh();
  const c = CONCEPTS[currentConceptIdx];
  const pkt = document.getElementById('sim-packet');
  const term = document.getElementById('sim-terminal');
  pkt.style.display = 'block';
  pkt.style.left = '140px';
  pkt.style.background = shieldOn ? 'var(--neon-cyan)' : 'var(--neon-crimson)';
  pkt.style.color = shieldOn ? '#000' : '#fff';
  pkt.style.transition = 'none';
  term.innerText = ">>> Firing packet across HTTP/WebSocket pipeline...";

  setTimeout(() => {
    pkt.style.transition = 'left 0.65s cubic-bezier(0.22, 1, 0.36, 1)';
    pkt.style.left = shieldOn ? 'calc(52% - 90px)' : 'calc(100% - 320px)';
  }, 40);

  setTimeout(() => {
    if (shieldOn) {
      playShieldBlockSound();
      term.style.color = 'var(--neon-green)';
      term.innerText = c.onLog;
      if (c.id === 'signalr') triggerSignalRDemo();
    } else {
      playHackAlarmSound();
      term.style.color = '#ff80aa';
      term.innerText = c.offLog;
    }
  }, 720);
}

// ============================================================================
// 5. MODULE 03: ARCHITECTURE MAP & AUTO-PLAY WORKFLOW SIMULATIONS
// ============================================================================
const ARCH_NODES = [
  // Layer 1
  { id: "n_views", x: 30, y: 48, badge: "RAZOR UI", name: "Views/*.cshtml", role: "Forms + @AntiForgeryToken + Bootstrap 5" },
  { id: "n_notifjs", x: 370, y: 48, badge: "WS CLIENT", name: "notifications.js", role: "SignalR JS + Bell + 880Hz/1174Hz Audio" },
  { id: "n_adminui", x: 730, y: 48, badge: "ADMIN VIEW", name: "Views/Admin/*.cshtml", role: "Live Dashboard + Unread Badge" },
  { id: "n_postman", x: 1110, y: 48, badge: "API CLIENT", name: "Postman / Swagger", role: "Cookie Jar + JSON Request Runner" },
  // Layer 2
  { id: "n_program", x: 540, y: 210, badge: "PIPELINE BOSS", name: "Program.cs", role: "DI + Global CSRF + OnValidatePrincipal Ban Gate" },
  // Layer 3
  { id: "n_acc", x: 25, y: 380, badge: "MVC AUTH", name: "AccountController.cs", role: "Register, Login, Logout, 5-Try Lockout" },
  { id: "n_donor", x: 255, y: 380, badge: "MVC DONOR", name: "DonorController.cs", role: "Donor CRUD + Search + Concurrency" },
  { id: "n_req", x: 485, y: 380, badge: "CORE FLOW", name: "BloodRequestController", role: "Request + Pledge/Accept/Complete" },
  { id: "n_admin", x: 725, y: 380, badge: "MODERATION", name: "AdminController.cs", role: "Ban/Unban + Role Hierarchy + Inbox" },
  { id: "n_api", x: 955, y: 380, badge: "REST JSON", name: "DonorApi / AuthApi", role: "18+ Endpoints + IDOR Ownership Guard" },
  { id: "n_hub", x: 1175, y: 380, badge: "SIGNALR ROCKET", name: "NotificationHub.cs", role: "Groups: 'admins' & 'user_{id}'" },
  // Layer 4
  { id: "n_compat", x: 60, y: 585, badge: "RBC LOGIC", name: "BloodCompatibility.cs", role: "8-Group Transfusion Switch Matrix" },
  { id: "n_dtos", x: 420, y: 585, badge: "PRIVACY SHIELD", name: "ApiDtos.cs & ViewModels", role: "Strips ContactNumber & UserId" },
  { id: "n_notifsvc", x: 800, y: 585, badge: "PUSH SERVICE", name: "NotificationService.cs", role: "IHubContext Pusher + Event Builder" },
  { id: "n_cache", x: 1130, y: 585, badge: "RAM CACHE", name: "MessageCache.cs", role: "IMemoryCache (60s TTL + Invalidate)" },
  // Layer 5
  { id: "n_entities", x: 140, y: 765, badge: "ENTITIES", name: "AppUser, Donor, Request, Offer", role: "Validation + RowVersion + Unique Index" },
  { id: "n_dbctx", x: 580, y: 765, badge: "EF CORE 10", name: "ApplicationDbContext.cs", role: "LINQ to Parameterized SQL + DbSeeder" },
  { id: "n_sql", x: 1040, y: 765, badge: "DATABASE", name: "SQL Server (BloodConnectDb)", role: "5 Identity + 4 Domain Tables" }
];

const ARCH_EDGES = [
  ["n_views", "n_program"], ["n_postman", "n_program"], ["n_notifjs", "n_hub"], ["n_adminui", "n_hub"],
  ["n_program", "n_acc"], ["n_program", "n_donor"], ["n_program", "n_req"], ["n_program", "n_admin"], ["n_program", "n_api"],
  ["n_donor", "n_compat"], ["n_req", "n_compat"], ["n_api", "n_compat"], ["n_api", "n_dtos"],
  ["n_req", "n_notifsvc"], ["n_admin", "n_cache"], ["n_notifsvc", "n_cache"], ["n_notifsvc", "n_hub"],
  ["n_acc", "n_dbctx"], ["n_donor", "n_dbctx"], ["n_req", "n_dbctx"], ["n_admin", "n_dbctx"], ["n_api", "n_dbctx"],
  ["n_dbctx", "n_entities"], ["n_dbctx", "n_sql"]
];

const WORKFLOWS = [
  {
    title: "1. Emergency Request + SignalR Rocket Push 🚀",
    sub: "Patient submits A+ Request ➔ Saved to SQL ➔ Live WebSocket alert rings Admin bell",
    steps: [
      { node: "n_views", desc: "Patient 'Views/BloodRequest/Create.cshtml' mein A+ Critical request bharta hai aur Submit dabata hai. Form ke andar hidden '__RequestVerificationToken' lag kar jaata hai.", code: "POST /BloodRequest/Create HTTP/1.1\nContent-Type: application/x-www-form-urlencoded\nRequesterName=Rahul&BloodGroupNeeded=A%2B&UrgencyLevel=Critical&__RequestVerificationToken=CfDJ8..." },
      { node: "n_program", desc: "Request sabse pehle 'Program.cs' ke Middleware gate par aati hai. Global CSRF filter token verify karta hai aur Cookie middleware user ka identity claim load karta hai.", code: "// Program.cs\noptions.Filters.Add(new AutoValidateAntiforgeryTokenAttribute());\napp.UseAuthentication();\napp.UseAuthorization();" },
      { node: "n_req", desc: "'BloodRequestController.Create' action chalta hai. ModelState.IsValid check hota hai aur naya BloodRequest object initialize hota hai.", code: "// BloodRequestController.cs\nrequest.UserId = User.FindFirstValue(ClaimTypes.NameIdentifier);\nrequest.Status = DomainValues.Active;\nrequest.RequestDate = DateTime.UtcNow;" },
      { node: "n_dbctx", desc: "'ApplicationDbContext' C# entity ko parameterized SQL INSERT statement mein convert karta hai.", code: "_context.BloodRequests.Add(request);\nawait _context.SaveChangesAsync();" },
      { node: "n_sql", sqlCommit: true, desc: "'SQL Server' ke BloodRequests table mein row permanent save hoti hai aur naya RequestId milta hai.", code: "INSERT INTO [BloodRequests] ([RequesterName], [BloodGroupNeeded], [UrgencyLevel], [Status])\nVALUES (@p0, @p1, @p2, 'Active');\nSELECT SCOPE_IDENTITY();" },
      { node: "n_notifsvc", desc: "Ab Controller 'NotificationService.PushNewRequestToAdminsAsync(request)' ko call karta hai taaki bina refresh kiye Admins ko khabar mile!", code: "// NotificationService.cs\nawait _hubContext.Clients.Group(\"admins\").SendAsync(\"ReceiveNotification\", new {\n  type = \"request\", title = \"New A+ request\", url = \"/BloodRequest/Index\"\n});" },
      { node: "n_hub", desc: "'NotificationHub.cs' (/hubs/notifications) active WebSocket pipeline ke zariye 'admins' group mein jude saare browsers ko JSON frame shoot karta hai!", code: "WebSocket Frame [TEXT]:\n{\"target\":\"ReceiveNotification\",\"arguments\":[{\"type\":\"request\",\"title\":\"New A+ request\"}]}" },
      { node: "n_notifjs", chime: true, desc: "BOOM! Admin ke browser mein 'notifications.js' ReceiveNotification pakadta hai, Web Audio API se 880Hz+1174Hz chime bajata hai, Bell Badge +1 karta hai aur Toast popup dikhata hai!", code: "// wwwroot/js/notifications.js\nconnection.on('ReceiveNotification', (payload) => {\n  incrementBellBadge();\n  playTwoToneChime(880, 1174.66);\n  showSlideInToast(payload);\n});" }
    ]
  },
  {
    title: "2. Medical Compatibility Search (B+ Needed) 🩸",
    sub: "User searches B+ ➔ BloodCompatibility.cs expands to 4 groups ➔ Exact match ranked first",
    steps: [
      { node: "n_views", desc: "User 'Views/Donor/Index.cshtml' par Blood Group 'B+' aur State 'Gujarat' chun kar Search button dabata hai.", code: "GET /Donor?bloodGroup=B%2B&state=Gujarat HTTP/1.1" },
      { node: "n_donor", desc: "'DonorController.Index' request pakadta hai aur 'BloodCompatibility.GetCompatibleDonorGroups(\"B+\")' ko call karta hai.", code: "var compatibleGroups = BloodCompatibility.GetCompatibleDonorGroups(bloodGroup);\n// Returns: [\"O-\", \"O+\", \"B-\", \"B+\"]" },
      { node: "n_compat", desc: "'BloodCompatibility.cs' ka centralized switch expression RBC medical matrix lagata hai: B+ marij ko O-, O+, B-, aur B+ charon khoon de sakte hain!", code: "\"B+\" => new[] { \"O-\", \"O+\", \"B-\", \"B+\" }" },
      { node: "n_dbctx", desc: "'ApplicationDbContext' SQL query banata hai jo sirf Available donors laati hai aur Exact Match (B+) ko sabse upar sort karti hai.", code: "query.Where(d => d.IsAvailable && compatible.Contains(d.BloodGroup))\n     .OrderByDescending(d => d.BloodGroup == \"B+\");" },
      { node: "n_sql", desc: "'SQL Server' indexed Donors table se matching rows nikal kar wapas deta hai.", code: "SELECT * FROM Donors WHERE IsAvailable = 1 AND State = 'Gujarat' AND BloodGroup IN ('O-','O+','B-','B+')\nORDER BY CASE WHEN BloodGroup = 'B+' THEN 1 ELSE 0 END DESC;" },
      { node: "n_views", desc: "Razor View user ko Exact Match aur Compatible Donors ke cards render karke dikha deta hai!", code: "@foreach (var donor in Model.Donors) { /* Render card with compatibility badge */ }" }
    ]
  },
  {
    title: "3. Two-Way Pledge & Contact Unlock 🤝",
    sub: "Donor Pledges ➔ Unique Index Check ➔ Owner Accepts ➔ Auto-Reject Others ➔ Phone Unlocked",
    steps: [
      { node: "n_views", desc: "Logged-in Donor kisi active request par 'Pledge to Donate' button dabata hai.", code: "POST /BloodRequest/Offer/42 HTTP/1.1" },
      { node: "n_req", desc: "'BloodRequestController.Offer' check karta hai: (1) Request Owner != Donor, (2) Donor BloodGroup is compatible with Request.", code: "if (request.UserId == currentUserId) return BadRequest(\"Cannot pledge on own request\");\nif (!BloodCompatibility.CanDonate(donor.BloodGroup, request.BloodGroupNeeded)) return BadRequest();" },
      { node: "n_entities", sqlCommit: true, desc: "'DonationOffer.cs' entity banti hai (Status = 'Pledged'). Database ka Unique Index (RequestId, DonorId) duplicate pledge rokta hai.", code: "// ApplicationDbContext.cs\nbuilder.Entity<DonationOffer>().HasIndex(o => new { o.RequestId, o.DonorId }).IsUnique();" },
      { node: "n_notifsvc", desc: "'NotificationService' Request ke Owner ('user_{ownerId}') ko live SignalR notification bhejta hai ki Donor ne pledge kiya hai!", code: "await _hubContext.Clients.Group($\"user_{request.UserId}\").SendAsync(\"ReceiveNotification\", payload);" },
      { node: "n_req", chime: true, desc: "Ab Request Owner 'Accept Offer' dabata hai! Controller us offer ko 'Accepted' karta hai, BAAKI SAARE pending offers ko 'Rejected' kar deta hai, aur Donor ka Phone Number unlock kar deta hai!", code: "offer.Status = DomainValues.Accepted;\nforeach (var other in otherPendingOffers) { other.Status = DomainValues.Rejected; }\nawait _notifications.PushOfferStatusToDonorAsync(offer.Donor.UserId, \"Accepted\", request.RequestId);" }
    ]
  },
  {
    title: "4. Contact Inbox + 60s Hybrid Cache Invalidation ⚡",
    sub: "User sends Contact Message ➔ MessageCache invalidated ➔ Admin badge updated instantly",
    steps: [
      { node: "n_views", desc: "User 'Views/Home/Contact.cshtml' form bhar ke message submit karta hai.", code: "POST /Home/Contact HTTP/1.1" },
      { node: "n_dbctx", sqlCommit: true, desc: "HomeController message ko 'ContactMessages' table mein IsRead = false ke saath save karta hai.", code: "_context.ContactMessages.Add(msg);\nawait _context.SaveChangesAsync();" },
      { node: "n_cache", desc: "'MessageCache.cs' jo 60 second ke liye unread count RAM mein rakhta hai, usko turant Invalidate (clear) kiya jaata hai taaki purana count na dikhe!", code: "// MessageCache.cs\n_memoryCache.Remove(\"UnreadContactCount\");" },
      { node: "n_notifsvc", chime: true, desc: "'NotificationService' SignalR Hub ke zariye saare online Admins ko live toast + chime bhejta hai aur unka Unread Badge update kar deta hai!", code: "await _notifications.PushNewContactMessageToAdminsAsync(msg);" }
    ]
  },
  {
    title: "5. Admin Ban + Instant OnValidatePrincipal Kickout 🛡️",
    sub: "Admin bans user ➔ AspNetUsers.IsBanned = 1 ➔ Next user click rejected by Program.cs",
    steps: [
      { node: "n_adminui", desc: "Admin Panel mein Admin ek user ke aage 'Ban User' button click karta hai.", code: "POST /Admin/ToggleBan?userId=user-99 HTTP/1.1" },
      { node: "n_admin", desc: "'AdminController' Role Hierarchy check karta hai (SuperAdmin ko koi chhed nahi sakta) aur target user ka 'IsBanned = true' set karta hai.", code: "if (await _userManager.IsInRoleAsync(targetUser, \"SuperAdmin\")) return Forbid();\ntargetUser.IsBanned = true;\nawait _userManager.UpdateAsync(targetUser);" },
      { node: "n_sql", sqlCommit: true, desc: "SQL Server ke 'AspNetUsers' table mein IsBanned = 1 save ho jaata hai.", code: "UPDATE AspNetUsers SET IsBanned = 1 WHERE Id = 'user-99';" },
      { node: "n_program", desc: "Ab jaise hi woh Banned user apni khuli hui website par agla click karta hai, 'Program.cs' ka 'OnValidatePrincipal' uski Cookie pakad kar turant SignOut maar deta hai!", code: "options.Events.OnValidatePrincipal = async context => {\n  var user = await userManager.GetUserAsync(context.Principal);\n  if (user == null || user.IsBanned) {\n    context.RejectPrincipal();\n    await context.HttpContext.SignOutAsync();\n  }\n};" }
    ]
  }
];

let curWf = 0, curWfStep = 0;
let autoPlayTimer = null;
const archNodeMap = {};

function initArchMap() {
  const wfBar = document.getElementById('wf-buttons');
  WORKFLOWS.forEach((w, i) => {
    const b = document.createElement('button');
    b.className = 'wf-btn' + (i === 0 ? ' active' : '');
    b.id = 'wf-btn-' + i;
    b.innerHTML = `${w.title}<small>${w.sub}</small>`;
    b.onclick = () => { stopAutoPlay(); playCyberClick(700); selectWorkflow(i); };
    wfBar.appendChild(b);
  });

  const container = document.getElementById('arch-nodes');
  ARCH_NODES.forEach(n => {
    archNodeMap[n.id] = n;
    const d = document.createElement('div');
    d.className = 'arch-node';
    d.id = 'arch-' + n.id;
    d.style.left = n.x + 'px';
    d.style.top = n.y + 'px';
    d.innerHTML = `<span class="n-badge">${n.badge}</span><div class="n-name">${n.name}</div><div class="n-role">${n.role}</div>`;
    d.onclick = () => {
      stopAutoPlay();
      playCyberClick(600);
      document.querySelectorAll('.arch-node').forEach(el => el.classList.remove('active-node'));
      d.classList.add('active-node');
      document.getElementById('sc-step-num').innerText = "DIRECT NODE INSPECTION";
      document.getElementById('sc-node-title').innerText = n.name;
      document.getElementById('sc-explanation').innerText = `Role in Architecture: ${n.role}. Niche Module 05 (32-File Encyclopedia) mein iska poora code aur Viva answer dekh!`;
    };
    container.appendChild(d);
  });

  renderWorkflowStep();
}

function selectWorkflow(idx) {
  curWf = idx; curWfStep = 0;
  document.querySelectorAll('.wf-btn').forEach((b, i) => b.classList.toggle('active', i === idx));
  renderWorkflowStep();
}

function stepWorkflow(dir) {
  playLaserWhoosh();
  const w = WORKFLOWS[curWf];
  curWfStep = (curWfStep + dir + w.steps.length) % w.steps.length;
  renderWorkflowStep();
}

function toggleAutoPlay() {
  const btn = document.getElementById('autoplay-btn');
  if (autoPlayTimer) {
    stopAutoPlay();
  } else {
    btn.innerText = "⏸ Pause Auto-Play";
    btn.className = "nav-btn amber";
    stepWorkflow(1);
    autoPlayTimer = setInterval(() => {
      stepWorkflow(1);
    }, 2400);
  }
}

function stopAutoPlay() {
  if (autoPlayTimer) {
    clearInterval(autoPlayTimer);
    autoPlayTimer = null;
    const btn = document.getElementById('autoplay-btn');
    if (btn) {
      btn.innerText = "▶ Auto-Play Full Flow";
      btn.className = "nav-btn green";
    }
  }
}

function renderWorkflowStep() {
  const w = WORKFLOWS[curWf];
  const st = w.steps[curWfStep];
  document.getElementById('wf-status').innerText = `ACTIVE: ${w.title} — Step ${curWfStep + 1} of ${w.steps.length}`;
  document.getElementById('sc-step-num').innerText = `STEP ${curWfStep + 1} OF ${w.steps.length}`;
  const nObj = archNodeMap[st.node];
  document.getElementById('sc-node-title').innerText = nObj.name;
  document.getElementById('sc-explanation').innerText = st.desc;
  document.getElementById('sc-code').innerText = st.code;

  document.querySelectorAll('.arch-node').forEach(el => el.classList.remove('active-node'));
  const activeEl = document.getElementById('arch-' + st.node);
  if (activeEl) activeEl.classList.add('active-node');

  if (st.chime) triggerSignalRDemo();
  else if (st.sqlCommit) playDbCommitSound();

  const svg = document.getElementById('arch-svg');
  svg.innerHTML = '';
  const prevNodeId = curWfStep > 0 ? w.steps[curWfStep - 1].node : null;

  ARCH_EDGES.forEach(([aId, bId]) => {
    const a = archNodeMap[aId], b = archNodeMap[bId];
    const x1 = a.x + 102, y1 = a.y + 42, x2 = b.x + 102, y2 = b.y + 42;
    const midY = (y1 + y2) / 2;
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`);
    const isLit = prevNodeId && ((prevNodeId === aId && st.node === bId) || (prevNodeId === bId && st.node === aId));
    path.setAttribute('class', isLit ? 'svg-edge lit' : 'svg-edge');
    svg.appendChild(path);
  });

  if (prevNodeId && prevNodeId !== st.node) {
    const a = archNodeMap[prevNodeId], b = archNodeMap[st.node];
    const x1 = a.x + 102, y1 = a.y + 42, x2 = b.x + 102, y2 = b.y + 42;
    const midY = (y1 + y2) / 2;
    const pLine = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    pLine.setAttribute('d', `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`);
    pLine.setAttribute('class', 'svg-edge lit');
    svg.appendChild(pLine);

    const orb = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    orb.setAttribute('r', '9');
    orb.setAttribute('class', 'svg-orb');
    const anim = document.createElementNS('http://www.w3.org/2000/svg', 'animateMotion');
    anim.setAttribute('dur', '0.7s');
    anim.setAttribute('repeatCount', 'indefinite');
    anim.setAttribute('path', `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`);
    orb.appendChild(anim);
    svg.appendChild(orb);
  }
}

// ============================================================================
// 6. MODULE 04: BLOOD BAG TRANSFUSION TUBE & TWO-WAY PLEDGE STATE MACHINE LAB
// ============================================================================
const BLOOD_GROUPS = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"];
const COMPAT_MAP = {
  "O-":  ["O-"],
  "O+":  ["O-", "O+"],
  "A-":  ["O-", "A-"],
  "A+":  ["O-", "O+", "A-", "A+"],
  "B-":  ["O-", "B-"],
  "B+":  ["O-", "O+", "B-", "B+"],
  "AB-": ["O-", "A-", "B-", "AB-"],
  "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
};

let currentRecipient = "B+";
let currentDonorTest = "B+";

function initDomainLab() {
  const rGrid = document.getElementById('recipient-grid');
  const dGrid = document.getElementById('donor-grid');
  BLOOD_GROUPS.forEach(bg => {
    const rb = document.createElement('div');
    rb.className = 'bg-pill';
    rb.id = 'rec-' + bg;
    rb.innerText = bg;
    rb.onclick = () => { currentRecipient = bg; selectBloodGroup(bg, currentDonorTest); };
    rGrid.appendChild(rb);

    const db = document.createElement('div');
    db.className = 'bg-pill';
    db.id = 'don-' + bg;
    db.innerText = bg;
    db.onclick = () => { currentDonorTest = bg; selectBloodGroup(currentRecipient, bg); };
    dGrid.appendChild(db);
  });
  selectBloodGroup("B+", "B+");
  setPledgeState(0);
}

function selectBloodGroup(recBg, donBg) {
  const allowed = COMPAT_MAP[recBg];
  const isSafe = allowed.includes(donBg);

  BLOOD_GROUPS.forEach(g => {
    document.getElementById('rec-' + g).classList.toggle('selected-recipient', g === recBg);
    const dEl = document.getElementById('don-' + g);
    dEl.classList.toggle('compatible-donor', allowed.includes(g));
    dEl.classList.toggle('incompatible-donor', !allowed.includes(g));
  });

  document.getElementById('bag-rec-lbl').innerText = recBg;
  document.getElementById('bag-donor-lbl').innerText = donBg;

  const verdict = document.getElementById('transfusion-verdict');
  const flow = document.getElementById('iv-tube-flow');
  const recBag = document.getElementById('rec-bag-fill');

  if (isSafe) {
    playHeartbeatSound();
    verdict.style.color = 'var(--neon-green)';
    verdict.innerText = donBg === recBg
      ? `✅ SAFE TRANSFUSION (${donBg} ➔ ${recBg} EXACT MATCH!)`
      : `✅ SAFE TRANSFUSION (${donBg} is medically compatible with ${recBg})`;
    flow.style.width = '100%';
    flow.style.background = 'repeating-linear-gradient(90deg, #00ff9d 0px, #00ff9d 18px, #00b8ff 18px, #00b8ff 30px)';
    recBag.style.background = 'linear-gradient(180deg, #ff0055, #990033)';
  } else {
    playHackAlarmSound();
    verdict.style.color = 'var(--neon-crimson)';
    verdict.innerText = `🚨 DANGER! ${donBg} CANNOT DONATE TO ${recBg} (Server Rejects Offer!)`;
    flow.style.width = '35%';
    flow.style.background = '#ff0055';
    recBag.style.background = 'linear-gradient(180deg, #475569, #1e293b)';
  }

  document.getElementById('compat-code-out').innerText =
`// Models/BloodCompatibility.cs
GetCompatibleDonorGroups("${recBg}") => [ ${allowed.map(x => `"${x}"`).join(', ')} ]
CanDonate(donor: "${donBg}", recipient: "${recBg}") => ${isSafe.toString().toUpperCase()}

// Server Validation in BloodRequestController.Offer:
if (!BloodCompatibility.CanDonate("${donBg}", "${recBg}"))
    return BadRequest("Incompatible blood group for this request.");`;
}

function setPledgeState(stage) {
  const ids = ["st-active", "st-pledged", "st-accepted", "st-fulfilled"];
  ids.forEach((id, idx) => document.getElementById(id).classList.toggle('current', idx === stage));
  const term = document.getElementById('pledge-terminal');
  const vault = document.getElementById('privacy-vault-box');
  const pvIcon = document.getElementById('pv-icon');
  const pvPhone = document.getElementById('pv-phone');

  if (stage === 0) {
    playCyberClick(580);
    vault.className = 'privacy-vault locked';
    pvIcon.innerText = '🔒 CONTACT PRIVACY SHIELD: LOCKED';
    pvPhone.innerText = 'Donor Phone: +91-XXXXXXXXXX (Hidden via DTO)';
    term.innerText =
`[STATE 1: REQUEST POSTED]
- BloodRequest #42 Status = "Active"
- Offers Count = 0
- Contact Privacy = LOCKED (Phone number hidden from public API & Views)
- SignalR Action = PushNewRequestToAdminsAsync() fired to 'admins' group!`;
  } else if (stage === 1) {
    playDbCommitSound();
    vault.className = 'privacy-vault locked';
    pvIcon.innerText = '🔒 CONTACT PRIVACY SHIELD: STILL LOCKED';
    pvPhone.innerText = '2 Pledges Received — Accept one to reveal phone!';
    term.innerText =
`[STATE 2: TWO DONORS PLEDGE ON REQUEST #42]
- Donor #15 (Gaurav, B+) clicks Pledge ➔ Offer #101 Status = "Pledged"
- Donor #18 (Aman, O-) clicks Pledge  ➔ Offer #102 Status = "Pledged"
- DB Constraint Check = Unique Index (RequestId, DonorId) blocks duplicate clicks!
- Contact Privacy = STILL LOCKED (Until Owner explicitly accepts one donor)
- SignalR Action = PushNewOfferToOwnerAsync() rings Request Owner's bell!`;
  } else if (stage === 2) {
    triggerSignalRDemo("Offer Accepted! 🎉", "Patient accepted Donor #15's pledge. Contact unlocked!");
    vault.className = 'privacy-vault unlocked';
    pvIcon.innerText = '🔓 CONTACT PRIVACY UNLOCKED (MUTUAL AGREEMENT)';
    pvPhone.innerText = 'Donor #15 (Gaurav): +91-9876543210';
    term.innerText =
`[STATE 3: OWNER ACCEPTS DONOR #15 (ATOMIC TRANSACTION)]
- Offer #101 (Gaurav) Status   ➔ "Accepted" (AcceptedAt = DateTime.UtcNow)
- Offer #102 (Aman) Status     ➔ AUTO-REJECTED ("Rejected") by BloodRequestController!
- BloodRequest #42 Status      ➔ "InProgress"
- 🔓 CONTACT PRIVACY UNLOCKED! Patient & Accepted Donor can now see each other's Phone Number!
- SignalR Action = PushOfferStatusToDonorAsync() alerts Donor #15 & Donor #18!`;
  } else if (stage === 3) {
    triggerSignalRDemo("Donation Completed! 🩸", "Request #42 is now marked Fulfilled.");
    vault.className = 'privacy-vault unlocked';
    pvIcon.innerText = '✅ DONATION FULFILLED & VERIFIED';
    pvPhone.innerText = 'FulfilledByDonorId = 15 (Locked from new offers)';
    term.innerText =
`[STATE 4: DONATION COMPLETED & FULFILLED]
- Either Request Owner OR Accepted Donor clicks "Mark Completed"
- Offer #101 Status            ➔ "Completed" (CompletedAt = DateTime.UtcNow)
- BloodRequest #42 Status      ➔ "Fulfilled" (FulfilledByDonorId = 15)
- Guard Rule = Fulfilled request is now locked; no new offers can be pledged or accepted!`;
  }
}

// ============================================================================
// 7. MODULE 05: COMPLETE 32-FILE ENCYCLOPEDIA DATA
// ============================================================================
const ALL_FILES = [
  {
    path: "Program.cs", cat: "BOOT & CONFIG",
    desi: "Poore project ka Main Switchboard aur Security Gatekeeper. App start hote hi sabse pehle yahi file chalti hai. Yeh Database, Identity Login, Cookie settings, Global CSRF protection, SignalR Hub, Memory Cache aur Swagger ko configure karti hai.",
    methods: "WebApplication.CreateBuilder() · AddDbContext<ApplicationDbContext>() · AddIdentity<AppUser, IdentityRole>() · OnValidatePrincipal (Instant Ban Check) · AutoValidateAntiforgeryToken · MapHub<NotificationHub>(\"/hubs/notifications\")",
    code: "builder.Services.AddControllersWithViews(o =>\n    o.Filters.Add(new AutoValidateAntiforgeryTokenAttribute()));\napp.MapHub<NotificationHub>(\"/hubs/notifications\");",
    links: "Connects ALL Controllers, ApplicationDbContext, NotificationHub, DbSeeder, MessageCache, NotificationService",
    breaks: "Agar Program.cs hata di ya tod di, toh application compile ya start hi nahi hogi. Poora server band!",
    viva: "Sir, Program.cs mein humne Dependency Injection container aur HTTP Request Middleware pipeline (`UseAuthentication` -> `UseAuthorization` -> `MapControllerRoute` -> `MapHub`) configure kiya hai."
  },
  {
    path: "BloodConnect.csproj", cat: "BOOT & CONFIG",
    desi: "Project ka Ration Card. Is XML file mein likha hota hai ki hum .NET 10.0 use kar rahe hain aur kaun-kaun se NuGet packages (EF Core 10, SQL Server, Identity, Swashbuckle Swagger) project mein installed hain.",
    methods: "<TargetFramework>net10.0</TargetFramework> · PackageReference: Microsoft.EntityFrameworkCore.SqlServer · Swashbuckle.AspNetCore",
    code: "<Project Sdk=\"Microsoft.NET.Sdk.Web\">\n  <PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup>\n</Project>",
    links: "Used by .NET SDK, MSBuild, and NuGet Restore",
    breaks: "dotnet restore aur dotnet build kaam karna band kar denge.",
    viva: "Sir, .csproj file project dependencies aur target framework (.NET 10.0) define karti hai."
  },
  {
    path: "appsettings.json & appsettings.Development.json", cat: "BOOT & CONFIG",
    desi: "Configuration Diary. Isme SQL Server ka Connection String (`Server=localhost\\SQLEXPRESS04;Database=BloodConnectDb...`) aur Logging levels likhe hote hain. Production wali file `.gitignore` mein chhupi rehti hai taaki live password GitHub par leak na ho.",
    methods: "ConnectionStrings:DefaultConnection · Logging:LogLevel",
    code: "\"ConnectionStrings\": {\n  \"DefaultConnection\": \"Server=localhost\\\\SQLEXPRESS04;Database=BloodConnectDb;Trusted_Connection=True;TrustServerCertificate=True;\"\n}",
    links: "Read by Program.cs via builder.Configuration.GetConnectionString(\"DefaultConnection\")",
    breaks: "Application ko pata hi nahi chalega ki kis SQL Server database se judna hai.",
    viva: "Sir, sensitive production credentials ko source code se alag rakhne ke liye humne environment-specific appsettings aur gitignore use kiya hai."
  },
  {
    path: "Migrations/* (EF Core Migrations)", cat: "BOOT & CONFIG",
    desi: "Database ki Time-Machine. Jab bhi hum C# Models mein koi naya column ya index jodte hain, EF Core Migrations uska C# blueprint (`Up()` aur `Down()` methods) banata hai jo SQL Server mein tables khada karta hai.",
    methods: "Up(MigrationBuilder) · Down(MigrationBuilder) · BloodConnectDbModelSnapshot",
    code: "dotnet ef migrations add InitialCreate\ndotnet ef database update",
    links: "Generated from ApplicationDbContext.cs and Domain Entities",
    breaks: "SQL Server mein tables aur indexes automatically create nahi honge.",
    viva: "Sir, Code-First Migrations se database schema version-controlled rehta hai aur bina manual SQL scripts ke deploy ho jaata hai."
  },
  {
    path: "Controllers/HomeController.cs", cat: "MVC CONTROLLER",
    desi: "Website ka Reception Counter. Homepage (`Index`), About (`Blood Compatibility Chart`), FAQ, Contact Us form (`POST Contact`), aur custom Branded Error pages (404/500) yahi sambhalta hai.",
    methods: "Index() · About() · Faq() · Contact(GET/POST) · Error()",
    code: "public async Task<IActionResult> Contact(ContactMessage model) {\n  _context.ContactMessages.Add(model);\n  await _context.SaveChangesAsync();\n  await _notifications.PushNewContactMessageToAdminsAsync(model);\n}",
    links: "ContactMessage.cs, ApplicationDbContext.cs, NotificationService.cs, MessageCache.cs, Views/Home/*.cshtml",
    breaks: "Homepage, About page aur Contact form khulna band ho jayenge.",
    viva: "Sir, HomeController public landing pages serve karta hai aur Contact submission par MessageCache invalidate karke Admins ko real-time SignalR alert bhejta hai."
  },
  {
    path: "Controllers/AccountController.cs", cat: "MVC CONTROLLER",
    desi: "Security Checkpost aur ID Card Office. User ka Registration, Login, Logout, aur AccessDenied page yahi chalata hai. 5 baar galat password daalne par 5 minute ke liye account lock kar deta hai.",
    methods: "Register(GET/POST) · Login(GET/POST) · Logout(POST) · AccessDenied()",
    code: "var result = await _signInManager.PasswordSignInAsync(\n    model.Email, model.Password, model.RememberMe, lockoutOnFailure: true);",
    links: "AppUser.cs, ViewModels.cs, Views/Account/*.cshtml, ASP.NET Core Identity",
    breaks: "Koi bhi user browser se Login, Register ya Logout nahi kar payega.",
    viva: "Sir, AccountController ASP.NET Core Identity ke UserManager aur SignInManager ka use karke cookie-based authentication aur brute-force lockout enforce karta hai."
  },
  {
    path: "Controllers/DonorController.cs", cat: "MVC CONTROLLER",
    desi: "Donors ka Headquarter. Donor profile banana (18-65 age check ke saath), Compatibility-aware search chalana, apni availability toggle karna, aur Optimistic Concurrency (`RowVersion`) + IDOR check ke saath profile update/delete karna.",
    methods: "Index(bloodGroup, state, searchMode) · Create(GET/POST) · Edit(GET/POST) · Delete(POST) · ToggleAvailability(POST)",
    code: "var compatible = BloodCompatibility.GetCompatibleDonorGroups(bloodGroup);\nquery = query.Where(d => compatible.Contains(d.BloodGroup))\n             .OrderByDescending(d => d.BloodGroup == bloodGroup);",
    links: "Donor.cs, BloodCompatibility.cs, ApplicationDbContext.cs, Views/Donor/*.cshtml",
    breaks: "Na koi donor register ho payega, na hi patient compatible donors search kar payega.",
    viva: "Sir, DonorController mein humne compatibility-aware sorting, IDOR ownership check, aur RowVersion `DbUpdateConcurrencyException` handling implement ki hai."
  },
  {
    path: "Controllers/BloodRequestController.cs", cat: "MVC CONTROLLER",
    desi: "Project ka Heart (Emergency Control Room). Blood request post karna, Donor ka Pledge (`Offer`) lena, Owner ka `AcceptOffer` karna (jisse baaki pending offers auto-reject hote hain aur phone number unlock hota hai), aur donation `Complete` karna.",
    methods: "Index() · Details(id) · Create() · Edit() · Delete() · Offer(requestId) · AcceptOffer(offerId) · RejectOffer(offerId) · CancelOffer(offerId) · CompleteOffer(offerId)",
    code: "// Inside AcceptOffer:\noffer.Status = DomainValues.Accepted;\nforeach (var other in competingOffers) other.Status = DomainValues.Rejected;\nawait _notifications.PushOfferStatusToDonorAsync(offer.Donor.UserId, DomainValues.Accepted, offer.RequestId);",
    links: "BloodRequest.cs, DonationOffer.cs, BloodCompatibility.cs, NotificationService.cs, Views/BloodRequest/*.cshtml",
    breaks: "Blood request posting aur Two-Way Pledge Donation workflow poori tarah band ho jayega.",
    viva: "Sir, BloodRequestController two-way confirmation state machine (`Pledged` -> `Accepted` -> `Completed` -> `Fulfilled`) aur real-time SignalR push triggers ko orchestrate karta hai."
  },
  {
    path: "Controllers/DashboardController.cs", cat: "MVC CONTROLLER",
    desi: "User ka Personal Control Room. Login karne ke baad user yahan apni Donor profile, apni daali hui Blood Requests, aur apne kiye hue Pledges (Offers) ka live status ek hi jagah dekhta hai.",
    methods: "Index() (Aggregates User's Donor Profile + My Requests + My Donation Offers)",
    code: "var myDonor = await _context.Donors.FirstOrDefaultAsync(d => d.UserId == userId);\nvar myRequests = await _context.BloodRequests.Where(r => r.UserId == userId).ToListAsync();",
    links: "Donor.cs, BloodRequest.cs, DonationOffer.cs, Views/Dashboard/Index.cshtml",
    breaks: "User ko apna personal contribution history aur active pledges track karne ki jagah nahi milegi.",
    viva: "Sir, DashboardController logged-in user ke saare domain activities (Donor status, posted requests, pledged offers) ko single viewmodel mein aggregate karta hai."
  },
  {
    path: "Controllers/AdminController.cs", cat: "MVC CONTROLLER",
    desi: "Supreme Court aur Admin Control Room. Users ko Ban/Unban karna, User ko Admin promote/demote karna, Role Hierarchy (`SuperAdmin > Admin > User`) enforce karna, fake donors/requests delete karna, aur Contact Messages inbox manage karna.",
    methods: "Index() · Users() · ToggleBan(userId) · PromoteToAdmin(userId) · DemoteToUser(userId) · DeleteUser(userId) · Messages() · MarkMessageRead(id)",
    code: "if (await _userManager.IsInRoleAsync(target, \"SuperAdmin\"))\n    return Forbid(); // SuperAdmin is immutable & undeletable!",
    links: "AppUser.cs, ContactMessage.cs, MessageCache.cs, Views/Admin/*.cshtml",
    breaks: "Platform par moderation, user ban system, aur role management khatam ho jayega.",
    viva: "Sir, AdminController strict role hierarchy enforce karta hai jahan SuperAdmin immutable hai aur Admin sirf regular Users ko moderate kar sakta hai."
  },
  {
    path: "Controllers/AuthApiController.cs", cat: "REST API",
    desi: "Postman aur API clients ke liye Login Gate (`/api/auth/*`). Yeh JSON mein email/password leta hai aur response mein `.AspNetCore.Identity.Application` Cookie set karta hai.",
    methods: "POST /api/auth/login · POST /api/auth/logout · GET /api/auth/me",
    code: "[Route(\"api/auth\")]\n[ApiController]\n[IgnoreAntiforgeryToken]\npublic class AuthApiController : ControllerBase { ... }",
    links: "AppUser.cs, ApiDtos.cs, Postman, Swagger UI",
    breaks: "Postman ya external API clients login karke protected API endpoints test nahi kar payenge.",
    viva: "Sir, AuthApiController JSON payload accept karke Identity cookie issue karta hai, jisse Postman bina HTML form scrape kiye authenticated endpoints test kar sakta hai."
  },
  {
    path: "Controllers/DonorApiController.cs", cat: "REST API",
    desi: "Donors ka RESTful JSON Engine (`/api/donor`). Paginated listing, single donor fetch, compatibility-aware search (`/api/donor/search`), aur authenticated CRUD deta hai using `DonorDto` (phone number chhupa kar).",
    methods: "GET /api/donor · GET /api/donor/{id} · GET /api/donor/search · POST /api/donor · PUT /api/donor/{id} · DELETE /api/donor/{id}",
    code: "return Ok(new {\n  total, page, pageSize, searchMode = \"compatible\",\n  compatibleGroups, results = donors.Select(d => d.ToDto())\n});",
    links: "Donor.cs, ApiDtos.cs, BloodCompatibility.cs, Swagger UI",
    breaks: "Donor REST APIs aur `/api/donor/search` kaam karna band kar denge.",
    viva: "Sir, DonorApiController REST standards follow karta hai—proper HTTP status codes (200, 201, 400, 401, 403, 404) aur DTO projection ke saath."
  },
  {
    path: "Controllers/BloodRequestApiController.cs", cat: "REST API",
    desi: "Blood Requests ka RESTful JSON Engine (`/api/bloodrequest`). Saari emergency requests ko JSON mein list karne, nayi request banane, aur Owner/Admin check ke saath update ya delete karne ke kaam aata hai.",
    methods: "GET /api/bloodrequest · GET /api/bloodrequest/{id} · POST /api/bloodrequest · PUT /api/bloodrequest/{id} · DELETE /api/bloodrequest/{id}",
    code: "if (request.UserId != currentUserId && !User.IsInRole(\"Admin\"))\n    return Forbid(); // IDOR Protection on API",
    links: "BloodRequest.cs, ApiDtos.cs, NotificationService.cs, Swagger UI",
    breaks: "Blood Request ke REST API endpoints band ho jayenge.",
    viva: "Sir, BloodRequestApiController JSON consumers ke liye full CRUD aur server-side ownership authorization provide karta hai."
  },
  {
    path: "Hubs/NotificationHub.cs", cat: "REALTIME & CACHE",
    desi: "SignalR WebSocket Rocket Launcher (`/hubs/notifications`). Jab bhi kisi user ka browser khulta hai, yeh file uske WebSocket connection ko uske role (`admins`) aur personal ID (`user_{userId}`) group mein jod deti hai.",
    methods: "OnConnectedAsync() · OnDisconnectedAsync(Exception?)",
    code: "public override async Task OnConnectedAsync() {\n  if (Context.User.IsInRole(\"Admin\") || Context.User.IsInRole(\"SuperAdmin\"))\n    await Groups.AddToGroupAsync(Context.ConnectionId, \"admins\");\n  await Groups.AddToGroupAsync(Context.ConnectionId, $\"user_{userId}\");\n}",
    links: "NotificationService.cs, wwwroot/js/notifications.js, Program.cs",
    breaks: "Real-time notifications ka WebSocket connection banega hi nahi; live bell aur toast band ho jayenge.",
    viva: "Sir, NotificationHub SignalR Hub class ko extend karta hai aur connection lifecycle par automatic group subscription manage karta hai."
  },
  {
    path: "Services/NotificationService.cs", cat: "REALTIME & CACHE",
    desi: "Real-Time Push Commander. Controllers jab bhi database mein kuch naya likhte hain, woh is service ko call karte hain. Yeh service `IHubContext<NotificationHub>` ka use karke exact target group ko live alert bhejti hai.",
    methods: "PushNewRequestToAdminsAsync() · PushNewContactMessageToAdminsAsync() · PushNewOfferToOwnerAsync() · PushOfferStatusToDonorAsync()",
    code: "public async Task PushNewOfferToOwnerAsync(BloodRequest req, DonationOffer offer) {\n  await _hub.Clients.Group($\"user_{req.UserId}\")\n            .SendAsync(\"ReceiveNotification\", payload);\n}",
    links: "NotificationHub.cs, MessageCache.cs, BloodRequestController.cs, HomeController.cs",
    breaks: "Controllers aur SignalR Hub ke beech ka bridge toot jayega.",
    viva: "Sir, NotificationService cross-cutting notification logic ko controllers se decouple karta hai (Single Responsibility Principle)."
  },
  {
    path: "Services/MessageCache.cs", cat: "REALTIME & CACHE",
    desi: "60-Second RAM Booster (`IMemoryCache`). Admin navbar mein har page load par unread messages ka badge dikhana hota hai. Bar-bar SQL Server par `COUNT(*)` query na chale, isliye yeh count ko 60 second ke liye RAM mein cache kar leta hai aur naya message aate hi clear (`Invalidate`) kar deta hai.",
    methods: "GetUnreadCountAsync() · Invalidate()",
    code: "return await _cache.GetOrCreateAsync(\"UnreadMessagesCount\", async entry => {\n  entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromSeconds(60);\n  return await _context.ContactMessages.CountAsync(m => !m.IsRead);\n});",
    links: "AdminController.cs, HomeController.cs, NotificationService.cs, Views/Shared/_Layout.cshtml",
    breaks: "Har ek page click par database par extra SQL query chalegi.",
    viva: "Sir, MessageCache read-heavy navbar badge ke liye 60-second TTL caching aur write-time explicit cache invalidation implement karta hai."
  },
  {
    path: "Models/AppUser.cs", cat: "DOMAIN & DB",
    desi: "User Account Model. ASP.NET Core ke default `IdentityUser` ko extend karke usme `FullName`, `IsBanned` (instant ban check ke liye), aur `CreatedAt` jodta hai.",
    methods: "FullName (string) · IsBanned (bool) · CreatedAt (DateTime)",
    code: "public class AppUser : IdentityUser {\n  [Required, StringLength(100)] public string FullName { get; set; }\n  public bool IsBanned { get; set; } = false;\n}",
    links: "ApplicationDbContext.cs, AccountController.cs, AdminController.cs, Program.cs",
    breaks: "User ka FullName aur Ban status store nahi ho payega.",
    viva: "Sir, AppUser IdentityUser ko inherit karta hai taaki authentication schema mein custom domain properties (`FullName`, `IsBanned`) add ho sakein."
  },
  {
    path: "Models/Donor.cs", cat: "DOMAIN & DB",
    desi: "Donor Entity Blueprint. Donor ka naam, blood group (`^(A|B|AB|O)[+-]$`), age (`18-65`), state, availability flag, `UserId` foreign key, aur optimistic concurrency ke liye `[Timestamp] RowVersion` rakhta hai.",
    methods: "DonorId · Name · BloodGroup · Age · State · City · ContactNumber · IsAvailable · UserId · RowVersion",
    code: "[Range(18, 65, ErrorMessage = \"Donor age must be between 18 and 65.\")]\npublic int Age { get; set; }\n[Timestamp] public byte[]? RowVersion { get; set; }",
    links: "ApplicationDbContext.cs, DonorController.cs, DonorApiController.cs, DonationOffer.cs",
    breaks: "Donors table aur donor validation rules khatam ho jayenge.",
    viva: "Sir, Donor entity data annotations ke zariye medical age limits (18-65), blood group regex, aur `[Timestamp] RowVersion` concurrency enforce karti hai."
  },
  {
    path: "Models/BloodRequest.cs", cat: "DOMAIN & DB",
    desi: "Emergency Blood Request Blueprint. Marij ka naam, zaroori blood group, urgency level (`Critical`, `High`, `Medium`, `Low`), current status (`Active`, `InProgress`, `Fulfilled`, `Cancelled`), aur kis donor ne fulfill kiya (`FulfilledByDonorId`) store karta hai.",
    methods: "RequestId · RequesterName · BloodGroupNeeded · UrgencyLevel · Status · RequestDate · UserId · FulfilledByDonorId",
    code: "public string Status { get; set; } = DomainValues.Active;\npublic int? FulfilledByDonorId { get; set; }",
    links: "BloodRequestController.cs, BloodRequestApiController.cs, DonationOffer.cs",
    breaks: "Patients blood requests post ya track nahi kar payenge.",
    viva: "Sir, BloodRequest entity emergency lifecycle ko track karti hai aur AppUser tatha fulfilling Donor ke saath foreign-key relationship rakhti hai."
  },
  {
    path: "Models/DonationOffer.cs", cat: "DOMAIN & DB",
    desi: "Two-Way Pledge Contract Model. Yeh `BloodRequest` aur `Donor` ke beech ka bridge hai. Isme pledge ka status (`Pledged`, `Accepted`, `Rejected`, `Cancelled`, `Completed`) aur timestamps (`CreatedAt`, `AcceptedAt`, `CompletedAt`) rehte hain.",
    methods: "Id · RequestId · DonorId · Status · CreatedAt · AcceptedAt · CompletedAt",
    code: "// Unique Compound Index in DbContext:\nbuilder.Entity<DonationOffer>()\n       .HasIndex(o => new { o.RequestId, o.DonorId }).IsUnique();",
    links: "BloodRequestController.cs, Donor.cs, BloodRequest.cs, ApplicationDbContext.cs",
    breaks: "Pledge workflow, auto-reject competing offers, aur donation history kaam nahi karenge.",
    viva: "Sir, DonationOffer junction entity hai jis par `(RequestId, DonorId)` ka unique compound index laga hai taaki duplicate pledges database level par hi ruk jayein."
  },
  {
    path: "Models/ContactMessage.cs", cat: "DOMAIN & DB",
    desi: "Contact Us Form Model. Public users jo sawaal ya feedback bhejte hain, unka Name, Email, Subject, Message, `SubmittedAt` aur Admin ke liye `IsRead` flag save karta hai.",
    methods: "Id · Name · Email · Subject · Message · IsRead · SubmittedAt",
    code: "public bool IsRead { get; set; } = false;\npublic DateTime SubmittedAt { get; set; } = DateTime.UtcNow;",
    links: "HomeController.cs, AdminController.cs, MessageCache.cs",
    breaks: "Admin Contact Inbox aur unread message badge kaam nahi karenge.",
    viva: "Sir, ContactMessage public inquiries ko persist karta hai aur `IsRead` flag ke zariye Admin inbox workflow drive karta hai."
  },
  {
    path: "Models/BloodCompatibility.cs", cat: "DOMAIN & DB",
    desi: "Project ka Medical Doctor. Is static class mein 8 blood groups ka Red Blood Cell compatibility matrix likha hai. Yeh batata hai ki kis recipient ko kaun-kaun se donor groups khoon de sakte hain.",
    methods: "GetCompatibleDonorGroups(string recipientGroup) · CanDonate(string donorGroup, string recipientGroup)",
    code: "public static IReadOnlyList<string> GetCompatibleDonorGroups(string bg) => bg switch {\n  \"O-\" => [\"O-\"], \"AB+\" => AllGroups, \"B+\" => [\"O-\", \"O+\", \"B-\", \"B+\"], ...\n};",
    links: "DonorController.cs, DonorApiController.cs, BloodRequestController.cs",
    breaks: "Compatibility-aware donor search aur pledge validation fail ho jayenge.",
    viva: "Sir, humne medical rules ko hardcode karne ke bajaye `BloodCompatibility.cs` mein centralize kiya hai taaki Web UI, REST API aur Pledge validation teeno ek hi source of truth use karein."
  },
  {
    path: "Models/DomainValues.cs", cat: "DOMAIN & DB",
    desi: "Constants Tijori. Code mein jagah-jagah typos (`\"Actve\"` ya `\"Pleged\"`) na hon, isliye saare valid Blood Groups (8), Indian States & UTs (36), Urgency Levels, aur Status strings yahan `const` bana kar rakhe gaye hain.",
    methods: "BloodGroups[] · IndianStates[] · UrgencyLevels[] · Active, InProgress, Fulfilled, Pledged, Accepted, Rejected",
    code: "public static class DomainValues {\n  public const string Pledged = \"Pledged\";\n  public const string Accepted = \"Accepted\";\n}",
    links: "Used across all Controllers, Models, and Views",
    breaks: "Magic strings aur spelling mistakes ki wajah se status comparisons toot jayenge.",
    viva: "Sir, DomainValues magic strings ko eliminate karta hai aur compile-time safety deta hai."
  },
  {
    path: "Models/ValidationAttributes.cs", cat: "DOMAIN & DB",
    desi: "Custom Qanoon Checker (`[MustBeTrue]`). Jab donor form bharta hai toh 'I confirm I am medically eligible' checkbox tick karna zaroori hota hai. Yeh custom validation attribute ensure karta hai ki checkbox `true` hi ho.",
    methods: "MustBeTrueAttribute : ValidationAttribute -> IsValid(object? value)",
    code: "public class MustBeTrueAttribute : ValidationAttribute {\n  public override bool IsValid(object? value) => value is bool b && b;\n}",
    links: "ViewModels.cs, Donor.cs",
    breaks: "Bina terms/medical consent tick kiye log form submit kar denge.",
    viva: "Sir, ASP.NET Core ke built-in `[Required]` attribute boolean `false` ko bhi pass kar deta hai, isliye humne custom `MustBeTrueAttribute` banaya."
  },
  {
    path: "Models/ApplicationDbContext.cs", cat: "DOMAIN & DB",
    desi: "EF Core 10 Database Translator. Yeh `IdentityDbContext<AppUser>` ko inherit karta hai, 4 domain `DbSet` tables register karta hai, aur `OnModelCreating` mein foreign keys, indexes aur cascade delete rules lagata hai.",
    methods: "DbSet<Donor> · DbSet<BloodRequest> · DbSet<DonationOffer> · DbSet<ContactMessage> · OnModelCreating()",
    code: "public class ApplicationDbContext : IdentityDbContext<AppUser> {\n  public DbSet<Donor> Donors { get; set; }\n  public DbSet<BloodRequest> BloodRequests { get; set; }\n  public DbSet<DonationOffer> DonationOffers { get; set; }\n}",
    links: "Program.cs, All Controllers, SQL Server",
    breaks: "C# application aur SQL Server ke beech ka saara sampark toot jayega.",
    viva: "Sir, ApplicationDbContext Unit of Work aur Repository patterns ko combine karta hai aur Fluent API se schema constraints enforce karta hai."
  },
  {
    path: "Models/DbSeeder.cs", cat: "DOMAIN & DB",
    desi: "Initial Data Filler. Jab project kisi naye laptop ya server par pehli baar chalta hai, toh `DbSeeder.cs` automatically 3 Roles (`SuperAdmin`, `Admin`, `User`), default Admin account (`admin@bloodconnect.com`), 13 realistic Donors aur 8 Blood Requests database mein seed kar deta hai.",
    methods: "SeedAsync(IServiceProvider)",
    code: "await roleManager.CreateAsync(new IdentityRole(\"SuperAdmin\"));\nawait userManager.CreateAsync(adminUser, \"Admin@123\");",
    links: "Program.cs, ApplicationDbContext.cs",
    breaks: "Naye database par na roles milenge, na default Admin login chalega, aur site bilkul khali dikhegi.",
    viva: "Sir, DbSeeder idempotent startup seeding karta hai—agar roles ya admin pehle se maujood hain toh duplicate nahi banata."
  },
  {
    path: "Models/ApiDtos.cs", cat: "DOMAIN & DB",
    desi: "API Privacy Chhanni (Data Transfer Objects). Public API responses mein Donor ka `ContactNumber`, `UserId`, aur `RowVersion` chhupane ke liye `DonorDto`, `BloodRequestDto`, aur `LoginRequestDto` yahan bane hain.",
    methods: "DonorDto · CreateDonorDto · BloodRequestDto · LoginDto · ToDto() mapping extensions",
    code: "public record DonorDto(int DonorId, string Name, string BloodGroup, string State, string Location, bool IsAvailable);",
    links: "DonorApiController.cs, BloodRequestApiController.cs, AuthApiController.cs",
    breaks: "API mein database entities seedha expose ho jayengi aur saare phone numbers leak ho jayenge.",
    viva: "Sir, ApiDtos internal database schema ko public API contract se alag rakhta hai aur PII data leak hone se bachata hai."
  },
  {
    path: "Models/ViewModels.cs", cat: "DOMAIN & DB",
    desi: "Razor Views ka Custom Tiffin Box. Jab kisi page (jaise Homepage, Dashboard, ya Admin Panel) ko ek se zyada tables ka data ek saath chahiye hota hai, toh `ViewModels.cs` un sabko ek clean class mein pack karke View tak le jaata hai.",
    methods: "RegisterViewModel · LoginViewModel · DashboardViewModel · AdminDashboardViewModel · DonorSearchViewModel",
    code: "public class DashboardViewModel {\n  public Donor? MyDonorProfile { get; set; }\n  public List<BloodRequest> MyRequests { get; set; }\n  public List<DonationOffer> MyOffers { get; set; }\n}",
    links: "AccountController, DashboardController, AdminController, Razor Views",
    breaks: "Complex views (Dashboard, Login, Register, Search) strongly-typed data render nahi kar payenge.",
    viva: "Sir, ViewModels UI-specific validation aur multi-entity aggregation provide karte hain bina domain models ko pollute kiye."
  },
  {
    path: "Views/Shared/_Layout.cshtml & Views/*/*.cshtml", cat: "FRONTEND UI",
    desi: "Website ka Visual Dhaancha (Razor Templates). `_Layout.cshtml` mein top Navbar, Notification Bell badge, Toast container, aur Footer hai jo har page par rehta hai. Baaki folders (`Home`, `Donor`, `BloodRequest`, `Admin`, `Dashboard`, `Account`) mein har page ke forms aur tables hain.",
    methods: "@RenderBody() · @Html.AntiForgeryToken() · User.IsInRole(\"Admin\") conditional UI",
    code: "<button id=\"notif-bell\" class=\"btn position-relative\">\n  <span id=\"notif-badge\" class=\"badge bg-danger\">@await MessageCache.GetUnreadCountAsync()</span>\n</button>",
    links: "All MVC Controllers, wwwroot/css/*, wwwroot/js/*",
    breaks: "Browser mein koi bhi HTML page render nahi hoga.",
    viva: "Sir, Razor Views server-side HTML rendering aur automatic XSS encoding provide karte hain."
  },
  {
    path: "wwwroot/js/notifications.js", cat: "FRONTEND UI",
    desi: "Browser ke andar ka SignalR Receiver aur Sound Engine. Yeh `@microsoft/signalr` client se `/hubs/notifications` par WebSocket jodta hai, `ReceiveNotification` aane par Bell hilaata hai, Web Audio API se 880Hz+1174Hz chime bajata hai aur Toast popup dikhata hai.",
    methods: "HubConnectionBuilder().withUrl('/hubs/notifications').withAutomaticReconnect() · playNotificationChime() · showToast()",
    code: "const connection = new signalR.HubConnectionBuilder()\n  .withUrl(\"/hubs/notifications\")\n  .withAutomaticReconnect()\n  .build();",
    links: "Hubs/NotificationHub.cs, Views/Shared/_Layout.cshtml, wwwroot/css/notifications.css",
    breaks: "Server se SignalR push aane ke bawajood browser mein na घंटी bajegi, na live popup dikhega.",
    viva: "Sir, notifications.js exponential backoff ke saath auto-reconnect karta hai aur Web Audio API oscillators se zero-dependency two-tone sound synthesize karta hai."
  },
  {
    path: "wwwroot/js/site.js & wwwroot/js/animations.js", cat: "FRONTEND UI",
    desi: "UI Polish aur Interactive Helpers. Navbar scroll effects, animated number counters, confirmation modals, password generator/strength helper, aur alert auto-dismissal yahan likha hai.",
    methods: "initCounters() · showConfirmModal() · toggleSoundPreference()",
    code: "localStorage.setItem('bloodconnect_sound', isMuted ? 'off' : 'on');",
    links: "Views/Shared/_Layout.cshtml",
    breaks: "Interactive UI animations aur client-side UX helpers band ho jayenge.",
    viva: "Sir, vanilla JavaScript modules use karke humne lightweight, zero-framework-bloat interactivity achieve ki hai."
  },
  {
    path: "wwwroot/css/site.css, animations.css & notifications.css", cat: "FRONTEND UI",
    desi: "Design System aur Styling. Warm premium palette (Cream, Deep Burgundy, Gold), Inter typography, responsive cards, bell ring keyframe animations (`@keyframes bellRing`), toast slide-in effects, aur `prefers-reduced-motion` accessibility rules.",
    methods: ":root CSS Variables · @keyframes bellRing · .toast-notification",
    code: "@media (prefers-reduced-motion: reduce) {\n  *, ::before, ::after { animation-duration: 0.01ms !important; }\n}",
    links: "Views/Shared/_Layout.cshtml",
    breaks: "Website ka poora warm burgundy theme, animations aur toast styling gayab ho jayega.",
    viva: "Sir, CSS architecture modular hai aur accessibility ke liye `prefers-reduced-motion` media query ko respect karta hai."
  }
];

let currentCat = "ALL";
function filterCategory(cat) {
  playCyberClick(650);
  currentCat = cat;
  renderFileCards();
}

function renderFileCards() {
  const q = document.getElementById('file-search').value.toLowerCase();
  const container = document.getElementById('file-cards-container');
  container.innerHTML = '';

  const filtered = ALL_FILES.filter(f => {
    const matchCat = currentCat === "ALL" || f.cat === currentCat;
    const matchQ = !q || f.path.toLowerCase().includes(q) || f.desi.toLowerCase().includes(q) || f.methods.toLowerCase().includes(q) || f.code.toLowerCase().includes(q);
    return matchCat && matchQ;
  });

  filtered.forEach(f => {
    const card = document.createElement('div');
    card.className = 'file-card';
    card.innerHTML = `
      <div class="file-header">
        <div class="file-path">📄 ${f.path}</div>
        <span class="file-cat">${f.cat}</span>
      </div>
      <div>
        <div class="file-sec-label">💡 Asli Kaam (Desi Bhasha Mein)</div>
        <div class="file-text">${f.desi}</div>
      </div>
      <div>
        <div class="file-sec-label">🔧 Key Methods / Properties Inside</div>
        <div class="file-text" style="font-family:var(--font-mono); font-size:0.78rem; color:#cbd5e1;">${f.methods}</div>
      </div>
      <div>
        <div class="file-sec-label">💻 Core Code Snippet</div>
        <div class="code-block">${f.code.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>
      </div>
      <div>
        <div class="file-sec-label">🔗 Connected To</div>
        <div class="file-text" style="font-size:0.8rem; color:var(--neon-cyan);">${f.links}</div>
      </div>
      <div class="break-box">
        <strong>⚠️ Agar Yeh File Hata Di Toh:</strong> ${f.breaks}
      </div>
      <div class="viva-tip">
        <strong>🎓 Viva Answer:</strong> "${f.viva}"
      </div>
    `;
    container.appendChild(card);
  });
}

// ============================================================================
// 8. MODULE 06: POSTMAN & COOKIE AUTH LAB SIMULATOR
// ============================================================================
const POSTMAN_TESTS = [
  {
    req: `POST https://bloodconnector.runasp.net/api/auth/login HTTP/1.1
Content-Type: application/json

{
  "email": "admin@bloodconnect.com",
  "password": "Admin@123"
}`,
    res: `HTTP/1.1 200 OK
Set-Cookie: .AspNetCore.Identity.Application=CfDJ8N...; path=/; samesite=lax; httponly
Content-Type: application/json

{
  "message": "Login successful",
  "email": "admin@bloodconnect.com",
  "roles": ["SuperAdmin", "Admin"]
}

// 💡 KYA HUA YAHAN?
// AuthApiController ne password verify kiya aur response header mein 'Set-Cookie' bheja.
// Postman ke 'Cookie Jar' ne is HttpOnly cookie ko save kar liya. Ab agle har API call mein Postman yeh cookie khud bhejega!`
  },
  {
    req: `GET https://bloodconnector.runasp.net/api/donor/search?bloodGroup=B%2B&state=Bihar HTTP/1.1
Accept: application/json`,
    res: `HTTP/1.1 200 OK
Content-Type: application/json

{
  "total": 2,
  "searchMode": "compatible",
  "requestedBloodGroup": "B+",
  "compatibleGroups": ["O-", "O+", "B-", "B+"],
  "results": [
    {
      "donorId": 15,
      "name": "Gaurav",
      "bloodGroup": "B+",
      "state": "Bihar",
      "isExactMatch": true
      // 🔒 Notice: 'contactNumber' & 'userId' are STRIPPED by DonorDto (ApiDtos.cs)!
    }
  ]
}`
  },
  {
    req: `PUT https://bloodconnector.runasp.net/api/donor/15 HTTP/1.1
Cookie: .AspNetCore.Identity.Application=CfDJ8_NormalUserCookie...
Content-Type: application/json

{
  "name": "Hacked By Another User",
  "bloodGroup": "O-",
  "age": 25,
  "state": "Gujarat"
}`,
    res: `HTTP/1.1 403 Forbidden
Content-Type: application/problem+json

{
  "status": 403,
  "title": "Forbidden — You do not own this Donor profile (IDOR Protection)"
}

// 💡 KYA HUA YAHAN?
// User login toh tha (isliye 401 Unauthorized nahi aaya), par woh Donor #15 ka malik nahi tha!
// DonorApiController ke 'if (donor.UserId != currentUserId)' check ne IDOR attack pakad liya aur 403 Forbidden maara!`
  },
  {
    req: `POST https://bloodconnector.runasp.net/api/donor HTTP/1.1
Cookie: .AspNetCore.Identity.Application=CfDJ8_ValidUserCookie...
Content-Type: application/json

{
  "name": "Test'; DROP TABLE Donors;--",
  "bloodGroup": "Z+",
  "age": 14,
  "state": "InvalidState"
}`,
    res: `HTTP/1.1 400 Bad Request
Content-Type: application/problem+json

{
  "status": 400,
  "title": "One or more validation errors occurred.",
  "errors": {
    "BloodGroup": ["Invalid blood group. Must be A+, A-, B+, B-, AB+, AB-, O+, or O-."],
    "Age": ["Donor age must be between 18 and 65."],
    "State": ["Please select a valid Indian State or Union Territory."]
  }
}

// 💡 KYA HUA YAHAN?
// Model validation attributes ([RegularExpression], [Range(18,65)]) aur EF Core Parameterized Queries ne kachra data aur SQLi dono rok diye!`
  }
];

function runPostmanTest(idx) {
  if (idx === 2 || idx === 3) playShieldBlockSound();
  else playCyberClick(760);
  document.getElementById('pm-req').innerText = POSTMAN_TESTS[idx].req;
  document.getElementById('pm-res').innerText = POSTMAN_TESTS[idx].res;
}

// ============================================================================
// 9. MODULE 07: GUJARAT UNIVERSITY EXTERNAL VIVA FLASHCARDS
// ============================================================================
const VIVA_QUESTIONS = [
  {
    q: "Q1. Tumne JWT Token ki jagah Cookie Authentication kyun use kiya?",
    a: "Sir, humara primary frontend ASP.NET Core MVC (server-rendered Razor Views) hai. Browser automatically har request par HttpOnly, SameSite=Lax cookies send karta hai aur JavaScript (`document.cookie`) use chura nahi sakta (XSS safe). API testing ke liye humne `/api/auth/login` banaya hai jo Postman ke Cookie Jar ke saath seamlessly kaam karta hai."
  },
  {
    q: "Q2. Agar Admin kisi active user ko Ban kare, toh kya uski 7-din wali Cookie chalti rahegi?",
    a: "Nahi Sir! Humne `Program.cs` mein `CookieAuthenticationEvents.OnValidatePrincipal` hook kiya hai. Jaise hi woh user agla click karega, middleware database se `AppUser.IsBanned` check karega aur `true` milne par turant `RejectPrincipal()` aur `SignOutAsync()` chala kar bahar kar dega."
  },
  {
    q: "Q3. SignalR ka kaam kya hai aur yeh AJAX Polling se kaise behtar hai?",
    a: "Sir, AJAX Polling mein browser har 2-5 second mein server par fokat ki HTTP requests maarta hai jisse database aur CPU load badhta hai. SignalR persistent WebSocket pipeline (`/hubs/notifications`) banata hai—zero polling! Jab koi write operation hota hai, tabhi `NotificationService` targeted group (`admins` ya `user_{id}`) ko instant push bhejta hai."
  },
  {
    q: "Q4. `Donor.cs` mein `[Timestamp] public byte[]? RowVersion` kyun lagaya hai?",
    a: "Sir, yeh Optimistic Concurrency control ke liye hai. SQL Server har update par `RowVersion` badalta hai. Agar do tabs ek saath same Donor ko update karein, toh EF Core `WHERE RowVersion = @old` check karta hai aur mismatch hone par `DbUpdateConcurrencyException` throw karke Lost Update problem rokta hai."
  },
  {
    q: "Q5. Duplicate pledges (ek hi Donor ka bar-bar Pledge dabana) kaise roka gaya hai?",
    a: "Sir, do levels par: (1) Application level par `BloodRequestController.Offer` check karta hai ki offer pehle se maujood toh nahi, aur (2) Database level par `ApplicationDbContext` mein `HasIndex(o => new { o.RequestId, o.DonorId }).IsUnique()` compound unique index laga hai."
  },
  {
    q: "Q6. `IMemoryCache` (`MessageCache.cs`) ka TTL 60 seconds hai—naya message aane par purana count toh nahi dikhta?",
    a: "Nahi Sir! Humne Hybrid Caching + Explicit Invalidation use kiya hai. Read-heavy paths par 60s tak zero DB query hoti hai, par jaise hi naya message aata hai ya Admin message read/delete karta hai, hum `_messageCache.Invalidate()` call karke cache clear kar dete hain."
  },
  {
    q: "Q7. Donor ka mobile number (`ContactNumber`) public API ya search mein kaise chhupaya gaya hai?",
    a: "Sir, DTO Pattern (`Models/ApiDtos.cs`) aur Two-Way Confirmation se. Public API `/api/donor` mein hum `Donor` entity nahi, balki `DonorDto` return karte hain jisme `ContactNumber` property hi nahi hai. Website par bhi phone number tabhi dikhta hai jab Request Owner pledge ko `Accepted` mark karta hai."
  },
  {
    q: "Q8. Jab Request Owner ek Donor ka offer `Accept` karta hai, toh baaki Donors ke offers ka kya hota hai?",
    a: "Sir, `BloodRequestController.AcceptOffer` ek hi transaction mein selected offer ko `Accepted` karta hai, Request status ko `InProgress` karta hai, aur usi request par aaye baaki saare pending (`Pledged`) offers ko automatically `Rejected` mark karke unko SignalR alert bhej deta hai."
  },
  {
    q: "Q9. IDOR (Insecure Direct Object Reference) kya hai aur tumne ise kaise roka?",
    a: "Sir, agar User A URL mein `/Donor/Edit/16` daal kar User B ka record edit karne ki koshish kare toh use IDOR kehte hain. Humne har Edit/Delete action (MVC aur API dono) mein `if (entity.UserId != currentUserId && !User.IsInRole(\"Admin\")) return Forbid();` lagaya hai."
  },
  {
    q: "Q10. Notification bell ki WhatsApp-style chime bina किसी `.mp3` file ke kaise bajti hai?",
    a: "Sir, `wwwroot/js/notifications.js` mein humne browser ka native **Web Audio API** use kiya hai. Do sine-wave oscillators (`880Hz` A5 aur `1174.66Hz` D6) aur `DynamicsCompressorNode` se real-time harmonic chime synthesize hoti hai—isliye zero external audio file dependency hai."
  },
  {
    q: "Q11. Role Hierarchy (`SuperAdmin > Admin > User`) kaise kaam karti hai?",
    a: "Sir, `SuperAdmin` immutable hai—use koi Admin ban, demote ya delete nahi kar sakta. `Admin` sirf regular `User` accounts ko ban ya moderate kar sakta hai, kisi dusre `Admin` ko nahi. Aur koi bhi Admin khud ko (`self`) ban ya delete nahi kar sakta."
  },
  {
    q: "Q12. Blood Compatibility search mein Exact Match aur Compatible Match kaise sort hote hain?",
    a: "Sir, agar patient ko `B+` chahiye, toh `BloodCompatibility.GetCompatibleDonorGroups(\"B+\")` char groups (`O-, O+, B-, B+`) deta hai. Phir EF Core query `.OrderByDescending(d => d.BloodGroup == \"B+\")` lagati hai jisse Exact Match (`B+`) sabse upar aata hai aur baaki compatible groups uske neeche."
  }
];

function initVivaDeck() {
  const container = document.getElementById('viva-deck-container');
  VIVA_QUESTIONS.forEach((item, idx) => {
    const card = document.createElement('div');
    card.className = 'viva-card' + (idx === 0 ? ' open' : '');
    card.innerHTML = `
      <div class="viva-q">
        <span>${item.q}</span>
        <span style="color:var(--neon-cyan); font-family:var(--font-mono);">[Click]</span>
      </div>
      <div class="viva-a">🎯 <strong>Perfect Viva Answer:</strong> ${item.a}</div>
    `;
    card.onclick = () => {
      playCyberClick(690);
      card.classList.toggle('open');
    };
    container.appendChild(card);
  });
}

// Initialize Everything on Load
window.addEventListener('DOMContentLoaded', () => {
  initConcepts();
  initArchMap();
  initDomainLab();
  renderFileCards();
  runPostmanTest(0);
  initVivaDeck();
});
</script>
</body>
</html>
"""

def launch_portal():
    out_path = Path("bloodconnect_godmode_command_center.html").resolve()
    out_path.write_text(HTML_PORTAL, encoding="utf-8")
    print(f"\n[+] Generated GOD-MODE v3.0 Cyber Command Portal: {out_path}")
    print("[+] Launching in your default browser now...")
    webbrowser.open(out_path.as_uri())

if __name__ == "__main__":
    launch_portal()