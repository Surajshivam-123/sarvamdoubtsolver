"""
Live Classroom Digital Blackboard Component ("Bhasha Guru").
Renders a synchronized interactive HTML5 Chalkboard (800x500 slate)
with simultaneous audio speech playback from Sarvam AI.
"""

import json
import base64
from typing import Dict, Any, Optional


def build_blackboard_html(
    storyboard: Dict[str, Any],
    audio_bytes: Optional[bytes] = None
) -> str:
    """
    Constructs an interactive self-contained HTML5 digital chalkboard
    synchronized with Sarvam AI audio.
    """
    # Safe fallback if empty storyboard
    if not storyboard:
        storyboard = {
            "doubt_domain": "Academic Reasoning",
            "identified_topic": "First Principles Derivation",
            "misconception_name": "Cognitive Divergence",
            "full_spoken_transcript": "Let us trace your derivation step by step.",
            "synchronized_timeline": [],
            "socratic_challenge": "What is the key governing constraint?"
        }

    timeline = storyboard.get("synchronized_timeline", [])
    
    # Calculate cumulative timeline timestamps
    cum_time = 0.0
    processed_timeline = []
    for step in timeline:
        dur = float(step.get("estimated_duration_sec", 3.5))
        processed_timeline.append({
            "step_id": step.get("step_id", len(processed_timeline) + 1),
            "speech_segment": step.get("speech_segment", ""),
            "start_time": round(cum_time, 2),
            "end_time": round(cum_time + dur, 2),
            "duration": dur,
            "board_action": step.get("board_action", "WRITE"),
            "target_coords": step.get("target_coords", {}),
            "color": step.get("color", "#FFFFFF"),
            "content": step.get("content", ""),
            "element_style": step.get("element_style", "chalk_text")
        })
        cum_time += dur

    total_est_seconds = max(cum_time, 1.0)
    storyboard_json = json.dumps({
        "doubt_domain": storyboard.get("doubt_domain", "Academic Doubt"),
        "identified_topic": storyboard.get("identified_topic", "Cognitive Derivation"),
        "misconception_name": storyboard.get("misconception_name", "Premise Divergence"),
        "full_spoken_transcript": storyboard.get("full_spoken_transcript", ""),
        "socratic_challenge": storyboard.get("socratic_challenge", ""),
        "timeline": processed_timeline,
        "total_duration": total_est_seconds
    })

    audio_base64 = ""
    has_audio = False
    if audio_bytes and len(audio_bytes) > 44:
        audio_base64 = base64.b64encode(audio_bytes).decode("ascii")
        has_audio = True

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bhasha Guru Blackboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: transparent;
    color: #f1f5f9;
    user-select: none;
    -webkit-font-smoothing: antialiased;
    padding: 4px;
  }}
  .board-container {{
    background: #1c1611;
    border-radius: 14px;
    padding: 12px 14px 14px;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45), inset 0 2px 4px rgba(255, 255, 255, 0.08);
    border: 3px solid #3d2f21;
    max-width: 820px;
    margin: 0 auto;
  }}
  .board-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
    padding: 0 4px;
    flex-wrap: wrap;
    gap: 6px;
  }}
  .board-title {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.03em;
    color: #e2e8f0;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .badge-tag {{
    background: rgba(16, 185, 129, 0.2);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.4);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
  }}
  .chalkboard-wrap {{
    position: relative;
    background: #131f17;
    border-radius: 8px 8px 0 0;
    overflow: hidden;
    box-shadow: inset 0 0 50px rgba(0, 0, 0, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-bottom: none;
  }}
  canvas#blackboard {{
    display: block;
    width: 100%;
    height: auto;
    aspect-ratio: 800 / 500;
    background: radial-gradient(circle at 45% 35%, #16241b 0%, #101913 90%);
  }}
  .chalk-tray {{
    height: 14px;
    background: linear-gradient(180deg, #2b2118 0%, #17110c 100%);
    border-top: 1px solid #4a3826;
    border-radius: 0 0 8px 8px;
    display: flex;
    align-items: center;
    padding-left: 24px;
    gap: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
  }}
  .chalk-piece {{
    width: 26px;
    height: 6px;
    border-radius: 3px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.6);
  }}
  .chalk-eraser {{
    width: 36px;
    height: 8px;
    background: #4a3b32;
    border: 1px solid #6b5546;
    border-radius: 2px;
    margin-left: auto;
    margin-right: 24px;
  }}
  /* Toolbar controls */
  .controls-bar {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
    padding: 4px 2px 0;
    flex-wrap: wrap;
  }}
  .btn-ctrl {{
    background: #273549;
    color: #f1f5f9;
    border: 1px solid #3e4f66;
    border-radius: 8px;
    padding: 6px 13px;
    font-size: 12px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.15s ease;
  }}
  .btn-ctrl:hover {{
    background: #33445c;
    border-color: #64748b;
    transform: translateY(-1px);
  }}
  .btn-ctrl:active {{
    transform: translateY(0);
  }}
  .btn-ctrl.btn-primary {{
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border-color: #34d399;
    color: #ffffff;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  }}
  .timeline-scrub {{
    flex: 1;
    min-width: 140px;
    height: 6px;
    accent-color: #10b981;
    cursor: pointer;
    background: #334155;
    border-radius: 3px;
  }}
  .time-display {{
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    color: #94a3b8;
    white-space: nowrap;
  }}
  /* Teacher Speech Banner */
  .teacher-speech-box {{
    background: #0d1522;
    border: 1px solid #1e293b;
    border-radius: 9px;
    padding: 10px 14px;
    margin-top: 10px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.3);
  }}
  .teacher-avatar {{
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
    box-shadow: 0 2px 6px rgba(16, 185, 129, 0.4);
  }}
  .speech-content {{
    flex: 1;
  }}
  .speech-step-tag {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #38bdf8;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .speech-text {{
    font-size: 13px;
    line-height: 1.5;
    color: #f1f5f9;
  }}
  .socratic-challenge-banner {{
    margin-top: 8px;
    background: rgba(250, 204, 21, 0.1);
    border: 1px solid rgba(250, 204, 21, 0.3);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    color: #fde047;
    display: none;
    align-items: center;
    gap: 8px;
  }}
</style>
</head>
<body>

<div class="board-container">
  <!-- Header -->
  <div class="board-header">
    <div class="board-title">
      <span>🧑‍🏫 Bhasha Guru • Live Classroom Tutor</span>
      <span class="badge-tag">{storyboard.get("doubt_domain", "Academic")}</span>
    </div>
    <div style="font-size:11px; color:#94a3b8; font-weight:500;">
      Topic: <span style="color:#f1f5f9; font-weight:600;">{storyboard.get("identified_topic", "")[:35]}</span>
    </div>
  </div>

  <!-- Chalkboard Canvas & Tray -->
  <div class="chalkboard-wrap">
    <canvas id="blackboard" width="800" height="500"></canvas>
  </div>
  <div class="chalk-tray">
    <div class="chalk-piece" style="background:#FFFFFF;"></div>
    <div class="chalk-piece" style="background:#4ADE80;"></div>
    <div class="chalk-piece" style="background:#F87171;"></div>
    <div class="chalk-piece" style="background:#38BDF8;"></div>
    <div class="chalk-piece" style="background:#FACC15;"></div>
    <div class="chalk-eraser"></div>
  </div>

  <!-- Toolbar Controls -->
  <div class="controls-bar">
    <button id="btnPlay" class="btn-ctrl btn-primary">
      <span id="playIcon">▶</span> <span id="playLabel">Play Lesson</span>
    </button>
    <button id="btnReplay" class="btn-ctrl">
      <span>🔄</span> Replay
    </button>
    <button id="btnFullBoard" class="btn-ctrl">
      <span>⚡</span> Full Board
    </button>
    <input id="scrubBar" class="timeline-scrub" type="range" min="0" max="{total_est_seconds}" step="0.1" value="0">
    <span id="timeLabel" class="time-display">0:00 / {int(total_est_seconds // 60)}:{int(total_est_seconds % 60):02d}</span>
  </div>

  <!-- Real-time Speech Subtitles -->
  <div class="teacher-speech-box">
    <div class="teacher-avatar">🎙️</div>
    <div class="speech-content">
      <div id="speechTag" class="speech-step-tag">Ready • Press Play to Begin Synchronized Derivation</div>
      <div id="speechText" class="speech-text">Welcome! Watch the board as Bhasha Guru walks through your reasoning step-by-step.</div>
      <div id="socraticBanner" class="socratic-challenge-banner">
        <span>🎯 <b>Student Checkpoint:</b></span>
        <span id="socraticText">{storyboard.get("socratic_challenge", "")}</span>
      </div>
    </div>
  </div>
</div>

<!-- Embedded Audio Element -->
<audio id="tutorAudio" {"src='data:audio/wav;base64," + audio_base64 + "'" if has_audio else ""} preload="auto"></audio>

<script>
(function() {{
  const DATA = {storyboard_json};
  const canvas = document.getElementById('blackboard');
  const ctx = canvas.getContext('2d');
  const btnPlay = document.getElementById('btnPlay');
  const btnReplay = document.getElementById('btnReplay');
  const btnFullBoard = document.getElementById('btnFullBoard');
  const scrubBar = document.getElementById('scrubBar');
  const timeLabel = document.getElementById('timeLabel');
  const speechTag = document.getElementById('speechTag');
  const speechText = document.getElementById('speechText');
  const socraticBanner = document.getElementById('socraticBanner');
  const audio = document.getElementById('tutorAudio');

  const HAS_AUDIO = {str(has_audio).lower()};
  const TOTAL_EST = DATA.total_duration;
  let isPlaying = false;
  let currentTime = 0;
  let virtualTimer = null;
  let lastTimestamp = null;
  let scaledTimeline = [...DATA.timeline];

  // Helper: format seconds to M:SS
  function fmtTime(sec) {{
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  }}

  // Adjust timing to actual audio duration when metadata loads
  function syncAudioDurations() {{
    if (HAS_AUDIO && audio.duration && !isNaN(audio.duration) && audio.duration > 1) {{
      const scale = audio.duration / TOTAL_EST;
      scrubBar.max = audio.duration;
      timeLabel.textContent = fmtTime(currentTime) + ' / ' + fmtTime(audio.duration);
      scaledTimeline = DATA.timeline.map(step => ({{
        ...step,
        start_time: +(step.start_time * scale).toFixed(2),
        end_time: +(step.end_time * scale).toFixed(2),
        duration: +(step.duration * scale).toFixed(2)
      }}));
    }}
  }}

  if (HAS_AUDIO) {{
    audio.addEventListener('loadedmetadata', syncAudioDurations);
    audio.addEventListener('timeupdate', () => {{
      if (isPlaying && HAS_AUDIO) {{
        currentTime = audio.currentTime;
        updateUI();
      }}
    }});
    audio.addEventListener('ended', () => {{
      pausePlayback();
      currentTime = (audio.duration && !isNaN(audio.duration)) ? audio.duration : TOTAL_EST;
      updateUI();
    }});
  }}

  // Canvas drawing helpers
  function drawRoundedRect(ctx, x, y, w, h, r) {{
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }}

  function drawArrow(ctx, x1, y1, x2, y2, headLength) {{
    const angle = Math.atan2(y2 - y1, x2 - x1);
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - headLength * Math.cos(angle - Math.PI / 6), y2 - headLength * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(x2 - headLength * Math.cos(angle + Math.PI / 6), y2 - headLength * Math.sin(angle + Math.PI / 6));
    ctx.lineTo(x2, y2);
    ctx.fillStyle = ctx.strokeStyle;
    ctx.fill();
  }}

  // Main Render Function
  function renderBoard(t) {{
    // Clear slate
    ctx.clearRect(0, 0, 800, 500);

    // Subtle chalk dust atmosphere
    ctx.save();
    ctx.fillStyle = 'rgba(255, 255, 255, 0.015)';
    ctx.fillRect(0, 0, 800, 500);

    // Grid lines (faint slate lines)
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.025)';
    ctx.lineWidth = 1;
    for (let y = 50; y < 500; y += 50) {{
      ctx.beginPath();
      ctx.moveTo(30, y);
      ctx.lineTo(770, y);
      ctx.stroke();
    }}
    ctx.restore();

    // Render all frames where frame.start_time <= t
    scaledTimeline.forEach(step => {{
      if (t < step.start_time) return;

      const action = step.board_action;
      const color = step.color || '#FFFFFF';
      const coords = step.target_coords || {{}};

      ctx.save();
      ctx.shadowColor = color;
      ctx.shadowBlur = 1.5;

      if (action === 'WRITE') {{
        ctx.fillStyle = color;
        const isBold = (step.element_style === 'bold_chalk');
        ctx.font = (isBold ? 'bold 16px' : '500 15px') + " 'Plus Jakarta Sans', sans-serif";
        const x = coords.x || 80;
        const y = coords.y || 80;
        ctx.fillText(step.content || '', x, y);
      }}
      else if (action === 'DRAW_BOX') {{
        const x = coords.x || 60;
        const y = coords.y || 55;
        const w = coords.w || 420;
        const h = coords.h || 45;
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.2;
        drawRoundedRect(ctx, x, y, w, h, 8);
        ctx.stroke();

        if (step.content) {{
          ctx.fillStyle = color;
          ctx.font = "bold 11px 'Plus Jakarta Sans', sans-serif";
          ctx.fillText("✓ " + step.content, x + w - 110, y - 6);
        }}
      }}
      else if (action === 'CROSS_OUT') {{
        const x = coords.x || 60;
        const y = coords.y || 155;
        const w = coords.w || 440;
        const h = coords.h || 45;
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.8;

        // Vigorous strike line through center
        ctx.beginPath();
        ctx.moveTo(x + 10, y + h / 2);
        ctx.lineTo(x + w - 10, y + h / 2);
        ctx.stroke();

        // Cross accents
        ctx.beginPath();
        ctx.moveTo(x + 15, y + 8);
        ctx.lineTo(x + w - 15, y + h - 8);
        ctx.stroke();

        if (step.content) {{
          ctx.fillStyle = color;
          ctx.font = "bold 11px 'Plus Jakarta Sans', sans-serif";
          ctx.fillText("✖ " + step.content, x + 12, y + h + 16);
        }}
      }}
      else if (action === 'DRAW_ARROW') {{
        const x1 = coords.x1 || 250;
        const y1 = coords.y1 || 215;
        const x2 = coords.x2 || 250;
        const y2 = coords.y2 || 305;
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.4;
        ctx.setLineDash([4, 3]);
        drawArrow(ctx, x1, y1, x2, y2, 10);
        ctx.setLineDash([]);

        if (step.content) {{
          ctx.fillStyle = color;
          ctx.font = "italic 12px 'Plus Jakarta Sans', sans-serif";
          ctx.fillText("↳ " + step.content, x1 + 14, (y1 + y2) / 2 + 4);
        }}
      }}
      else if (action === 'HIGHLIGHT') {{
        const x = coords.x || 60;
        const y = coords.y || 55;
        const w = coords.w || 420;
        const h = coords.h || 45;
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.5;
        ctx.setLineDash([5, 4]);
        drawRoundedRect(ctx, x, y, w, h, 8);
        ctx.stroke();
        ctx.setLineDash([]);
      }}
      else if (action === 'CLEAR_SECTION') {{
        const x = coords.x || 0;
        const y = coords.y || 0;
        const w = coords.w || 800;
        const h = coords.h || 500;
        ctx.clearRect(x, y, w, h);
      }}

      ctx.restore();
    }});
  }}

  // Update UI & Subtitles
  function updateUI() {{
    const total = (HAS_AUDIO && audio.duration && !isNaN(audio.duration)) ? audio.duration : TOTAL_EST;
    scrubBar.value = currentTime;
    timeLabel.textContent = fmtTime(currentTime) + ' / ' + fmtTime(total);

    // Active frame lookup
    let activeStep = null;
    let stepIndex = -1;
    for (let i = 0; i < scaledTimeline.length; i++) {{
      const s = scaledTimeline[i];
      if (currentTime >= s.start_time && currentTime < s.end_time) {{
        activeStep = s;
        stepIndex = i;
        break;
      }}
    }}

    // When ended or past last frame
    if (!activeStep && currentTime >= (scaledTimeline[scaledTimeline.length - 1]?.end_time || 0)) {{
      activeStep = scaledTimeline[scaledTimeline.length - 1];
      stepIndex = scaledTimeline.length - 1;
      socraticBanner.style.display = 'flex';
    }} else {{
      socraticBanner.style.display = 'none';
    }}

    if (activeStep) {{
      speechTag.innerHTML = `<span>Step ${{stepIndex + 1}} of ${{scaledTimeline.length}}</span> • <span style="color:${{activeStep.color || '#38BDF8'}}">${{activeStep.board_action}}</span>`;
      speechText.textContent = `"${{activeStep.speech_segment}}"`;
    }}

    renderBoard(currentTime);
  }}

  // Playback Control
  function startPlayback() {{
    isPlaying = true;
    btnPlay.classList.add('btn-primary');
    document.getElementById('playIcon').textContent = '⏸';
    document.getElementById('playLabel').textContent = 'Pause';

    if (HAS_AUDIO) {{
      audio.currentTime = currentTime;
      audio.play().catch(e => console.warn('Audio play notice:', e));
    }}

    lastTimestamp = performance.now();
    cancelAnimationFrame(virtualTimer);

    function loop(now) {{
      if (!isPlaying) return;
      if (!HAS_AUDIO) {{
        const dt = (now - lastTimestamp) / 1000;
        currentTime += dt;
        lastTimestamp = now;
        if (currentTime >= TOTAL_EST) {{
          currentTime = TOTAL_EST;
          pausePlayback();
          updateUI();
          return;
        }}
        updateUI();
      }}
      virtualTimer = requestAnimationFrame(loop);
    }}
    virtualTimer = requestAnimationFrame(loop);
  }}

  function pausePlayback() {{
    isPlaying = false;
    document.getElementById('playIcon').textContent = '▶';
    document.getElementById('playLabel').textContent = 'Play Lesson';
    if (HAS_AUDIO) {{
      audio.pause();
    }}
    cancelAnimationFrame(virtualTimer);
  }}

  btnPlay.addEventListener('click', () => {{
    if (isPlaying) {{
      pausePlayback();
    }} else {{
      const total = (HAS_AUDIO && audio.duration && !isNaN(audio.duration)) ? audio.duration : TOTAL_EST;
      if (currentTime >= total - 0.2) {{
        currentTime = 0;
      }}
      startPlayback();
    }}
  }});

  btnReplay.addEventListener('click', () => {{
    pausePlayback();
    currentTime = 0;
    if (HAS_AUDIO) audio.currentTime = 0;
    startPlayback();
  }});

  btnFullBoard.addEventListener('click', () => {{
    pausePlayback();
    const total = (HAS_AUDIO && audio.duration && !isNaN(audio.duration)) ? audio.duration : TOTAL_EST;
    currentTime = total;
    if (HAS_AUDIO) audio.currentTime = total;
    updateUI();
  }});

  scrubBar.addEventListener('input', (e) => {{
    currentTime = parseFloat(e.target.value);
    if (HAS_AUDIO) audio.currentTime = currentTime;
    updateUI();
  }});

  // Initial render: immediately display full board so user has zero wait time
  currentTime = TOTAL_EST;
  updateUI();
}})();
</script>
</body>
</html>"""
    return html


def render_live_blackboard(
    storyboard: Dict[str, Any],
    audio_bytes: Optional[bytes] = None,
    height: int = 660
):
    """
    Renders the live blackboard directly into Streamlit via components.html.
    """
    import streamlit.components.v1 as components
    html_content = build_blackboard_html(storyboard, audio_bytes=audio_bytes)
    components.html(html_content, height=height, scrolling=False)
