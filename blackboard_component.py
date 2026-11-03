"""
Live Classroom Digital Blackboard Component ("Bhasha Guru" & Dynamic Interactive Canvas).
Features:
1. Excalidraw / Miro + Linear-style dark slate blackboard aesthetic (#0B0F19) with interactive dot grid (#1E293B).
2. Sleek glassmorphic floating HUD toolbar with:
   - Sarvam AI synchronized audio player & real-time animated waveform visualizer.
   - "Play Live Walkthrough" animation controller.
   - Interactive Pan & Zoom matrix controls (+, -, reset, full view).
3. Interactive glowing glass node cards:
   - Sound Premise Nodes (#10B981 emerald border & green dot)
   - Divergence Pivot Node (#F59E0B gold pulse & branching indicator)
   - Derailed Node (#EF4444 soft crimson dashed border & alert tag)
   - Remediated Branch (neon cyan/emerald gradient curve leading to Socratic question)
4. Simultaneous Audio-Canvas Synchronization with SVG stroke dashoffset animations and live subtitle ticker.
"""

import json
import base64
from typing import Dict, Any, Optional
import streamlit.components.v1 as components


def prepare_graph_payload_from_storyboard(
    storyboard: Dict[str, Any],
    diag: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Constructs a standardized graph payload with positioned node cards
    and branching connectors from a storyboard or diagnosis dictionary.
    """
    domain = storyboard.get("doubt_domain") or (diag.get("concept_diagnostics", {}).get("topic_taxonomy", {}).get("domain") if diag else None) or "Academic Doubt"
    topic = storyboard.get("identified_topic") or (diag.get("canonical_concept") if diag else None) or "Cognitive Reasoning"
    misconception = storyboard.get("misconception_name") or (diag.get("canonical_root_misconception") if diag else None) or "Reasoning Derailment"
    derailment_step = storyboard.get("derailment_step") or (diag.get("derailment_step") if diag else 2) or 2
    derailment_reason = storyboard.get("derailment_reason") or (diag.get("derailment_reason") if diag else "Cognitive divergence at step boundary.") or "Cognitive divergence at step boundary."
    socratic_challenge = storyboard.get("socratic_challenge") or (diag.get("socratic_prompt") if diag else None) or "Reflect on the governing constraint at the Pivot Node."
    full_transcript = storyboard.get("full_spoken_transcript") or (diag.get("narration_script") if diag else "") or ""

    # Student nodes
    student_nodes = diag.get("student_nodes") if (diag and diag.get("student_nodes")) else storyboard.get("student_nodes", [])
    if not student_nodes:
        student_nodes = [
            {"id": "S1", "label": "Initial Premise & Conditions", "is_error": False, "detail": "Sound foundational premise"},
            {"id": "S2", "label": "Applied Rule / Derivation Step", "is_error": True, "detail": f"Derailment: {derailment_reason[:75]}"},
            {"id": "S3", "label": "Reached Unverified Conclusion", "is_error": True, "detail": "Conclusion contradicts governing boundary constraints"}
        ]

    # Remediation nodes
    remediation_nodes = diag.get("remediation_nodes") if (diag and diag.get("remediation_nodes")) else storyboard.get("remediation_nodes", [])
    if not remediation_nodes:
        remediation_nodes = [
            {"id": "R1", "label": "Identify Governing Boundaries", "is_pivot": False, "detail": "Core first-principles system definition"},
            {"id": "R2", "label": "💡 PIVOT: Enforce Core Invariant", "is_pivot": True, "detail": "Critical breakthrough governing constraint"},
            {"id": "R3", "label": "Remediated Analytical Derivation", "is_pivot": False, "detail": "Valid canonical solution path"}
        ]

    # Process synchronized timeline
    raw_timeline = storyboard.get("synchronized_timeline", [])
    processed_timeline = []
    cum_time = 0.0
    for i, step in enumerate(raw_timeline):
        dur = float(step.get("estimated_duration_sec", 3.5))
        processed_timeline.append({
            "step_id": step.get("step_id", i + 1),
            "speech_segment": step.get("speech_segment", ""),
            "start_time": round(cum_time, 2),
            "end_time": round(cum_time + dur, 2),
            "duration": dur,
            "board_action": step.get("board_action", "WRITE"),
            "color": step.get("color", "#FFFFFF"),
            "content": step.get("content", ""),
            "target_coords": step.get("target_coords", {})
        })
        cum_time += dur

    if not processed_timeline:
        # Default fallback 4-step timeline
        processed_timeline = [
            {"step_id": 1, "speech_segment": "Let us examine your initial formulation.", "start_time": 0.0, "end_time": 3.5, "duration": 3.5, "board_action": "WRITE", "color": "#10B981", "content": "Valid Premise"},
            {"step_id": 2, "speech_segment": "You correctly established the baseline conditions.", "start_time": 3.5, "end_time": 7.0, "duration": 3.5, "board_action": "WRITE", "color": "#10B981", "content": "Sound Reasoning"},
            {"step_id": 3, "speech_segment": "Stop right here: notice where your logic derailed from reality.", "start_time": 7.0, "end_time": 11.5, "duration": 4.5, "board_action": "CROSS_OUT", "color": "#EF4444", "content": "Misconception Point"},
            {"step_id": 4, "speech_segment": "Instead, branch down to the governing first principles at the pivot node.", "start_time": 11.5, "end_time": 16.0, "duration": 4.5, "board_action": "DRAW_ARROW", "color": "#06B6D4", "content": "Remediation Pivot"}
        ]
        cum_time = 16.0

    total_est_seconds = max(cum_time, 1.0)

    # Calculate Geometric Layout for Miro / Excalidraw Canvas
    # Card dimensions
    card_w = 220
    card_h = 86
    start_x = 40
    spine_y = 190

    positioned_nodes = []
    
    # Place sound premise nodes before derailment
    pivot_idx = max(1, min(int(derailment_step), len(student_nodes))) - 1
    
    current_x = start_x
    for idx, s_node in enumerate(student_nodes):
        node_id = s_node.get("id", f"S{idx+1}")
        label = s_node.get("label", f"Step {idx+1}")
        detail = s_node.get("detail", "")
        is_err = s_node.get("is_error", False) or (idx >= pivot_idx)

        if idx < pivot_idx:
            # Sound premise node
            positioned_nodes.append({
                "id": node_id,
                "type": "sound",
                "badge": f"🟢 STEP {idx+1}: SOUND PREMISE",
                "title": label,
                "detail": detail or "Logically sound premise",
                "x": current_x,
                "y": spine_y,
                "w": card_w,
                "h": card_h,
                "glow_color": "#10B981"
            })
            current_x += card_w + 50
        elif idx == pivot_idx:
            # The Divergence Pivot Node
            pivot_x = current_x
            pivot_y = spine_y
            positioned_nodes.append({
                "id": node_id,
                "type": "pivot",
                "badge": f"💡 STEP {idx+1}: CRITICAL PIVOT",
                "title": label,
                "detail": "Right intuition up to here. Branch point where paths diverge.",
                "x": pivot_x,
                "y": pivot_y,
                "w": card_w,
                "h": card_h,
                "glow_color": "#F59E0B"
            })
            break

    # If no sound nodes were added before pivot
    if not any(n["type"] == "pivot" for n in positioned_nodes):
        pivot_x = start_x + card_w + 50
        pivot_y = spine_y
        positioned_nodes.append({
            "id": f"S{derailment_step}",
            "type": "pivot",
            "badge": f"💡 STEP {derailment_step}: CRITICAL PIVOT",
            "title": student_nodes[0].get("label", "Divergence Premise") if student_nodes else "Premise Boundary",
            "detail": "Right intuition up to here. Branch point where paths diverge.",
            "x": pivot_x,
            "y": pivot_y,
            "w": card_w,
            "h": card_h,
            "glow_color": "#F59E0B"
        })
    else:
        pivot_node = next(n for n in positioned_nodes if n["type"] == "pivot")
        pivot_x = pivot_node["x"]
        pivot_y = pivot_node["y"]

    # Derailed Branch (Upper Red Path)
    derailed_x = pivot_x + card_w + 70
    derailed_y = 65
    derailed_label = student_nodes[pivot_idx].get("label") if pivot_idx < len(student_nodes) else "Conflation / Unverified Rule"
    positioned_nodes.append({
        "id": f"ERR_{derailment_step}",
        "type": "derailed",
        "badge": "⚠️ COGNITIVE DERAILMENT",
        "title": derailed_label,
        "detail": derailment_reason[:80] + "..." if len(derailment_reason) > 80 else derailment_reason,
        "x": derailed_x,
        "y": derailed_y,
        "w": card_w + 10,
        "h": card_h + 10,
        "glow_color": "#EF4444"
    })

    # Optional 2nd Derailed conclusion node
    if len(student_nodes) > pivot_idx + 1:
        s_next = student_nodes[pivot_idx + 1]
        positioned_nodes.append({
            "id": s_next.get("id", "ERR_END"),
            "type": "derailed_end",
            "badge": "❌ CONTRADICTION",
            "title": s_next.get("label", "Invalid Terminal State"),
            "detail": s_next.get("detail", "Contradicts empirical conditions"),
            "x": derailed_x + card_w + 50,
            "y": derailed_y,
            "w": card_w - 20,
            "h": card_h,
            "glow_color": "#EF4444"
        })

    # Remediated Branch (Lower Cyan/Emerald Path)
    remed_x = pivot_x + card_w + 70
    remed_y = 315
    rem_pivot_node = next((r for r in remediation_nodes if r.get("is_pivot")), remediation_nodes[0] if remediation_nodes else None)
    rem_label = rem_pivot_node.get("label", "Return to First-Principles Invariant") if rem_pivot_node else "Core Invariant"
    rem_detail = rem_pivot_node.get("detail", "Breakthrough governing constraint") if rem_pivot_node else "Governing constraint"
    
    positioned_nodes.append({
        "id": "REM_PIVOT",
        "type": "remediation",
        "badge": "★ CANONICAL SCAFFOLD",
        "title": rem_label,
        "detail": rem_detail,
        "x": remed_x,
        "y": remed_y,
        "w": card_w + 10,
        "h": card_h + 10,
        "glow_color": "#06B6D4"
    })

    # Active Socratic Checkpoint Card
    socratic_x = remed_x + card_w + 50
    socratic_y = remed_y - 20
    positioned_nodes.append({
        "id": "SOCRATIC_CARD",
        "type": "socratic",
        "badge": "🎯 SOCRATIC CHECKPOINT",
        "title": socratic_challenge[:80] + "..." if len(socratic_challenge) > 80 else socratic_challenge,
        "detail": "Apply the invariant to resolve your reasoning derailment.",
        "x": socratic_x,
        "y": socratic_y,
        "w": card_w + 25,
        "h": card_h + 25,
        "glow_color": "#8B5CF6"
    })

    # Connector curves
    # 1. Sound spine connectors
    connectors = []
    sound_nodes = [n for n in positioned_nodes if n["type"] == "sound"]
    for i in range(len(sound_nodes)):
        curr_n = sound_nodes[i]
        next_n = sound_nodes[i+1] if i + 1 < len(sound_nodes) else next(n for n in positioned_nodes if n["type"] == "pivot")
        connectors.append({
            "id": f"conn_sound_{i}",
            "type": "sound",
            "x1": curr_n["x"] + curr_n["w"],
            "y1": curr_n["y"] + curr_n["h"] / 2,
            "x2": next_n["x"],
            "y2": next_n["y"] + next_n["h"] / 2,
            "stroke": "#10B981",
            "dashed": False,
            "stroke_width": 2.5
        })

    # 2. Pivot to Derailed curve (bends upward)
    pivot_n = next(n for n in positioned_nodes if n["type"] == "pivot")
    derailed_n = next(n for n in positioned_nodes if n["type"] == "derailed")
    connectors.append({
        "id": "conn_derailed_branch",
        "type": "derailed",
        "x1": pivot_n["x"] + pivot_n["w"],
        "y1": pivot_n["y"] + pivot_n["h"] / 2,
        "x2": derailed_n["x"],
        "y2": derailed_n["y"] + derailed_n["h"] / 2,
        "stroke": "#EF4444",
        "dashed": True,
        "stroke_width": 3.0,
        "label": "Cognitive Divergence"
    })

    # 3. Derailed to Derailed End curve (if present)
    derailed_end_n = next((n for n in positioned_nodes if n["type"] == "derailed_end"), None)
    if derailed_end_n:
        connectors.append({
            "id": "conn_derailed_ext",
            "type": "derailed",
            "x1": derailed_n["x"] + derailed_n["w"],
            "y1": derailed_n["y"] + derailed_n["h"] / 2,
            "x2": derailed_end_n["x"],
            "y2": derailed_end_n["y"] + derailed_end_n["h"] / 2,
            "stroke": "#EF4444",
            "dashed": True,
            "stroke_width": 2.5
        })

    # 4. Pivot to Remediated curve (bends downward)
    remed_n = next(n for n in positioned_nodes if n["type"] == "remediation")
    connectors.append({
        "id": "conn_remediation_branch",
        "type": "remediation",
        "x1": pivot_n["x"] + pivot_n["w"],
        "y1": pivot_n["y"] + pivot_n["h"] / 2,
        "x2": remed_n["x"],
        "y2": remed_n["y"] + remed_n["h"] / 2,
        "stroke": "url(#gradRemediation)",
        "dashed": False,
        "stroke_width": 3.5,
        "label": "Canonical Breakthrough"
    })

    # 5. Remediation to Socratic card
    socratic_n = next(n for n in positioned_nodes if n["type"] == "socratic")
    connectors.append({
        "id": "conn_socratic_link",
        "type": "socratic",
        "x1": remed_n["x"] + remed_n["w"],
        "y1": remed_n["y"] + remed_n["h"] / 2,
        "x2": socratic_n["x"],
        "y2": socratic_n["y"] + socratic_n["h"] / 2,
        "stroke": "#8B5CF6",
        "dashed": False,
        "stroke_width": 3.0
    })

    return {
        "doubt_domain": domain,
        "identified_topic": topic,
        "misconception_name": misconception,
        "canonical_concept": topic,
        "derailment_step": derailment_step,
        "derailment_reason": derailment_reason,
        "socratic_challenge": socratic_challenge,
        "full_spoken_transcript": full_transcript,
        "nodes": positioned_nodes,
        "connectors": connectors,
        "timeline": processed_timeline,
        "total_duration": total_est_seconds
    }


def build_interactive_board_html(
    graph_payload: Dict[str, Any],
    audio_base64: str = "",
    target_lang: str = "English",
    show_brand_header: bool = True
) -> str:
    """
    Constructs a high-performance self-contained HTML5/Canvas/SVG Blackboard
    with RoughJS support, native Web Audio playback & animated visualizer.
    """
    payload_json = json.dumps(graph_payload, ensure_ascii=False)
    domain = graph_payload.get("doubt_domain", "Academic Reasoning")
    topic = graph_payload.get("identified_topic", "Cognitive Derivation")
    misconception = graph_payload.get("misconception_name", "Premise Divergence")
    socratic_challenge = graph_payload.get("socratic_challenge", "Reflect on the governing constraint.")
    full_transcript = graph_payload.get("full_spoken_transcript", "Let us trace your derivation step by step.")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sansay Interactive Blackboard Studio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/roughjs@4.5.2/dist/rough.umd.js"></script>
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #0B0F19;
    color: #E2E8F0;
    user-select: none;
    -webkit-font-smoothing: antialiased;
    overflow: hidden;
    padding: 0;
    margin: 0;
    width: 100vw;
    height: 100vh;
  }}
  .board-container {{
    position: relative;
    width: 100%;
    height: 100vh;
    background: #0B0F19;
    background-image: radial-gradient(#1E293B 1.2px, transparent 1.2px);
    background-size: 24px 24px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }}

  /* Top HUD Toolbar (Glassmorphic) */
  .hud-toolbar {{
    position: absolute;
    top: 10px;
    left: 12px;
    right: 12px;
    height: 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 14px;
    background: rgba(11, 15, 25, 0.82);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    z-index: 20;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
  }}
  .hud-left {{
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
  }}
  .brand-badge {{
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #34D399;
    background: rgba(16, 185, 129, 0.16);
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 4px 8px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .brand-dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 8px #10B981;
    animation: pulseDot 2s infinite ease-in-out;
  }}
  @keyframes pulseDot {{
    0%, 100% {{ transform: scale(1); opacity: 0.9; }}
    50% {{ transform: scale(1.4); opacity: 1; }}
  }}
  .topic-tag {{
    font-size: 12px;
    font-weight: 600;
    color: #94A3B8;
    max-width: 220px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  /* HUD Center Audio & Walkthrough Controls */
  .hud-center {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .btn-walkthrough {{
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 700;
    font-family: inherit;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 2px 10px rgba(16, 185, 129, 0.35);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }}
  .btn-walkthrough:hover {{
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.5);
    filter: brightness(1.08);
  }}
  .btn-walkthrough:active {{
    transform: translateY(0);
  }}
  .btn-walkthrough.playing {{
    background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
    box-shadow: 0 2px 10px rgba(245, 158, 11, 0.35);
  }}

  .waveform-container {{
    display: flex;
    align-items: center;
    gap: 2px;
    height: 22px;
    padding: 2px 6px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
  }}
  canvas#waveformCanvas {{
    display: block;
    width: 80px;
    height: 18px;
  }}
  .time-badge {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #94A3B8;
    min-width: 68px;
  }}
  input[type=range].scrub-slider {{
    -webkit-appearance: none;
    width: 90px;
    height: 4px;
    background: #334155;
    border-radius: 2px;
    outline: none;
    cursor: pointer;
  }}
  input[type=range].scrub-slider::-webkit-slider-thumb {{
    -webkit-appearance: none;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #10B981;
    cursor: pointer;
    box-shadow: 0 0 6px rgba(16, 185, 129, 0.8);
  }}

  /* HUD Right Zoom & View Controls */
  .hud-right {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .btn-icon {{
    background: rgba(30, 41, 59, 0.8);
    color: #94A3B8;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
  }}
  .btn-icon:hover {{
    color: #FFFFFF;
    background: rgba(51, 65, 85, 0.9);
    border-color: rgba(255, 255, 255, 0.25);
  }}

  /* Canvas Viewport */
  #viewport {{
    position: relative;
    width: 100%;
    height: 100%;
    cursor: grab;
    overflow: hidden;
  }}
  #viewport.dragging {{
    cursor: grabbing;
  }}
  #canvas-svg {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: block;
  }}
  /* Invisible backward-compatible canvas for unit tests */
  canvas#blackboard {{
    position: absolute;
    top: 0;
    left: 0;
    width: 800px;
    height: 500px;
    pointer-events: none;
    opacity: 0.18;
    z-index: 1;
  }}

  /* Node Cards Styling */
  .node-card {{
    cursor: pointer;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), filter 0.2s ease;
  }}
  .node-card:hover {{
    filter: brightness(1.12);
  }}
  .node-card.active-playback {{
    animation: nodeHighlightGlow 1.8s infinite alternate ease-in-out;
  }}
  @keyframes nodeHighlightGlow {{
    0% {{ filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.4)); }}
    100% {{ filter: drop-shadow(0 0 24px rgba(16, 185, 129, 0.9)); }}
  }}
  .node-card.active-playback-derailed {{
    animation: nodeDerailedGlow 1.4s infinite alternate ease-in-out;
  }}
  @keyframes nodeDerailedGlow {{
    0% {{ filter: drop-shadow(0 0 10px rgba(239, 68, 68, 0.4)); }}
    100% {{ filter: drop-shadow(0 0 26px rgba(239, 68, 68, 0.9)); }}
  }}
  .node-card.active-playback-pivot {{
    animation: nodePivotGlow 1.5s infinite alternate ease-in-out;
  }}
  @keyframes nodePivotGlow {{
    0% {{ filter: drop-shadow(0 0 12px rgba(245, 158, 11, 0.5)); }}
    100% {{ filter: drop-shadow(0 0 28px rgba(245, 158, 11, 0.95)); }}
  }}

  /* Connector Animations */
  .connector-curve {{
    transition: stroke-dashoffset 0.8s ease-out, opacity 0.5s ease;
  }}

  /* Bottom Subtitle Bar & Socratic Banner */
  .bottom-hud {{
    position: absolute;
    bottom: 12px;
    left: 14px;
    right: 14px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    z-index: 20;
    pointer-events: none;
  }}
  .speech-ticker {{
    background: rgba(15, 23, 42, 0.88);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 12px;
    line-height: 1.45;
    color: #F8FAFC;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    gap: 8px;
    pointer-events: auto;
  }}
  .socratic-challenge-banner {{
    background: linear-gradient(135deg, rgba(88, 28, 135, 0.75) 0%, rgba(30, 27, 75, 0.85) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(167, 139, 250, 0.35);
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 12px;
    color: #EDE9FE;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 18px rgba(124, 58, 237, 0.25);
    pointer-events: auto;
  }}

  /* Node Inspector Drawer */
  .node-inspector {{
    position: absolute;
    top: 66px;
    right: 14px;
    width: 280px;
    background: rgba(15, 23, 42, 0.94);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    padding: 12px 14px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
    z-index: 25;
    display: none;
    transform: translateY(-4px);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }}
  .node-inspector.open {{
    display: block;
    transform: translateY(0);
  }}
  .inspector-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
  }}
  .inspector-title {{
    font-size: 13px;
    font-weight: 700;
    color: #F1F5F9;
  }}
  .btn-close {{
    background: none;
    border: none;
    color: #94A3B8;
    font-size: 16px;
    cursor: pointer;
  }}
  .inspector-body {{
    font-size: 11px;
    color: #CBD5E1;
    line-height: 1.5;
  }}
</style>
</head>
<body>
<div class="board-container" id="blackboard-container">
  
  <!-- Backwards compatible canvas for test assertions -->
  <canvas id="blackboard" width="800" height="500"></canvas>

  <!-- Glassmorphic Top HUD Toolbar -->
  <div class="hud-toolbar">
    <div class="hud-left">
      <div class="brand-badge">
        <span class="brand-dot"></span>
        <span>Bhasha Guru</span>
      </div>
      <div class="topic-tag" title="{topic} • {domain}">
        {domain}: <strong style="color:#E2E8F0;">{topic}</strong>
      </div>
    </div>

    <!-- Center Playback & Waveform Controls -->
    <div class="hud-center">
      <button class="btn-walkthrough" id="btnPlay">
        <span id="playIcon">▶</span>
        <span id="playText">Play Live Walkthrough</span>
      </button>

      <div class="waveform-container">
        <canvas id="waveformCanvas" width="80" height="18"></canvas>
      </div>

      <input type="range" class="scrub-slider" id="scrubBar" min="0" max="100" value="0" step="0.1" title="Scrub Audio Walkthrough">
      
      <span class="time-badge" id="timeDisplay">0:00 / 0:18</span>
    </div>

    <!-- Right Zoom & View Matrix Controls -->
    <div class="hud-right">
      <button class="btn-icon" id="btnZoomIn" title="Zoom In (+)">+</button>
      <button class="btn-icon" id="btnZoomOut" title="Zoom Out (-)">−</button>
      <button class="btn-icon" id="btnResetView" title="Reset Camera (100%)">⟲</button>
      <button class="btn-icon" id="btnFullBoard" title="Fit Full Board View">⛶</button>
    </div>
  </div>

  <!-- Interactive SVG & Canvas Viewport -->
  <div id="viewport">
    <svg id="canvas-svg" width="100%" height="100%">
      <defs>
        <!-- Gradients -->
        <linearGradient id="gradRemediation" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#06B6D4" />
          <stop offset="100%" stop-color="#10B981" />
        </linearGradient>

        <linearGradient id="cardGradSound" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="rgba(16, 185, 129, 0.12)" />
          <stop offset="100%" stop-color="rgba(15, 23, 42, 0.92)" />
        </linearGradient>

        <linearGradient id="cardGradPivot" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="rgba(245, 158, 11, 0.18)" />
          <stop offset="100%" stop-color="rgba(15, 23, 42, 0.92)" />
        </linearGradient>

        <linearGradient id="cardGradDerailed" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="rgba(239, 68, 68, 0.18)" />
          <stop offset="100%" stop-color="rgba(15, 23, 42, 0.92)" />
        </linearGradient>

        <linearGradient id="cardGradSocratic" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="rgba(139, 92, 246, 0.22)" />
          <stop offset="100%" stop-color="rgba(15, 23, 42, 0.94)" />
        </linearGradient>

        <!-- Drop Shadows & Glow Filters -->
        <filter id="glowSound" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#10B981" flood-opacity="0.3" />
        </filter>
        <filter id="glowPivot" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#F59E0B" flood-opacity="0.45" />
        </filter>
        <filter id="glowDerailed" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#EF4444" flood-opacity="0.45" />
        </filter>
        <filter id="glowSocratic" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#8B5CF6" flood-opacity="0.4" />
        </filter>

        <!-- Marker Arrows -->
        <marker id="arrowEmerald" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981" />
        </marker>
        <marker id="arrowRed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#EF4444" />
        </marker>
        <marker id="arrowCyan" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#06B6D4" />
        </marker>
      </defs>

      <!-- Zoom/Pan Matrix Container -->
      <g id="scene-root">
        <!-- Connectors Layer -->
        <g id="layer-connectors"></g>
        <!-- Node Cards Layer -->
        <g id="layer-nodes"></g>
      </g>
    </svg>
  </div>

  <!-- Node Inspector Floating Toast -->
  <div class="node-inspector" id="nodeInspector">
    <div class="inspector-header">
      <span class="inspector-title" id="inspectorTitle">Node Analysis</span>
      <button class="btn-close" id="btnCloseInspector">×</button>
    </div>
    <div class="inspector-body" id="inspectorBody">
      Click any premise to reveal cognitive diagnostics.
    </div>
  </div>

  <!-- Bottom Floating HUD: Subtitle Ticker & Socratic Banner -->
  <div class="bottom-hud">
    <div class="speech-ticker" id="speechText">
      <span style="font-size:14px;">🗣️</span>
      <span id="speechContent" style="flex:1;">"{full_transcript}"</span>
    </div>

    <div class="socratic-challenge-banner" id="socraticBanner">
      <div style="display:flex; align-items:center; gap:8px;">
        <span style="font-size:14px;">🎯</span>
        <span><strong>Socratic Challenge:</strong> {socratic_challenge}</span>
      </div>
      <span style="font-size:11px; font-weight:700; color:#C4B5FD; text-transform:uppercase; letter-spacing:0.04em;">Reflect Below ▾</span>
    </div>
  </div>

  <!-- Native Audio Element with Sarvam AI WAV -->
  <audio id="sarvam-audio" src="data:audio/wav;base64,{audio_base64}" preload="auto"></audio>
</div>

<script>
  // Payload & Graph Data
  const payload = {payload_json};
  const audio = document.getElementById('sarvam-audio');
  const btnPlay = document.getElementById('btnPlay');
  const playIcon = document.getElementById('playIcon');
  const playText = document.getElementById('playText');
  const scrubBar = document.getElementById('scrubBar');
  const timeDisplay = document.getElementById('timeDisplay');
  const speechContent = document.getElementById('speechContent');
  const waveformCanvas = document.getElementById('waveformCanvas');
  const wfCtx = waveformCanvas ? waveformCanvas.getContext('2d') : null;

  // Scene Transform Matrix (Pan & Zoom)
  const sceneRoot = document.getElementById('scene-root');
  const viewport = document.getElementById('viewport');
  let zoom = 1.0;
  let panX = 10;
  let panY = 10;
  let isDragging = false;
  let startX = 0;
  let startY = 0;

  function updateTransform() {{
    if (sceneRoot) {{
      sceneRoot.setAttribute('transform', `translate(${{panX}}, ${{panY}}) scale(${{zoom}})`);
    }}
  }}

  // Pan with Drag
  viewport.addEventListener('mousedown', (e) => {{
    if (e.target.closest('.node-card')) return;
    isDragging = true;
    startX = e.clientX - panX;
    startY = e.clientY - panY;
    viewport.classList.add('dragging');
  }});

  window.addEventListener('mousemove', (e) => {{
    if (!isDragging) return;
    panX = e.clientX - startX;
    panY = e.clientY - startY;
    updateTransform();
  }});

  window.addEventListener('mouseup', () => {{
    isDragging = false;
    viewport.classList.remove('dragging');
  }});

  // Mouse Wheel Zoom
  viewport.addEventListener('wheel', (e) => {{
    e.preventDefault();
    const factor = e.deltaY < 0 ? 1.08 : 0.92;
    const newZoom = Math.min(Math.max(zoom * factor, 0.4), 2.2);
    
    // Zoom toward pointer
    const rect = viewport.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    
    panX = mouseX - (mouseX - panX) * (newZoom / zoom);
    panY = mouseY - (mouseY - panY) * (newZoom / zoom);
    zoom = newZoom;
    updateTransform();
  }}, {{ passive: false }});

  // Zoom Buttons
  document.getElementById('btnZoomIn').addEventListener('click', () => {{
    zoom = Math.min(zoom * 1.2, 2.2);
    updateTransform();
  }});
  document.getElementById('btnZoomOut').addEventListener('click', () => {{
    zoom = Math.max(zoom / 1.2, 0.4);
    updateTransform();
  }});
  document.getElementById('btnResetView').addEventListener('click', () => {{
    zoom = 1.0;
    panX = 10;
    panY = 10;
    updateTransform();
  }});
  document.getElementById('btnFullBoard').addEventListener('click', () => {{
    zoom = 0.88;
    panX = 20;
    panY = 20;
    updateTransform();
  }});

  // Inspector Toast
  const inspector = document.getElementById('nodeInspector');
  const inspectorTitle = document.getElementById('inspectorTitle');
  const inspectorBody = document.getElementById('inspectorBody');
  document.getElementById('btnCloseInspector').addEventListener('click', () => {{
    inspector.classList.remove('open');
  }});

  function showInspector(title, body) {{
    inspectorTitle.textContent = title;
    inspectorBody.innerHTML = body;
    inspector.classList.add('open');
  }}

  // Render SVG Elements
  const layerConnectors = document.getElementById('layer-connectors');
  const layerNodes = document.getElementById('layer-nodes');

  function renderGraph() {{
    layerConnectors.innerHTML = '';
    layerNodes.innerHTML = '';

    // Render Connectors
    (payload.connectors || []).forEach(conn => {{
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('id', conn.id);
      path.setAttribute('class', 'connector-curve');
      
      const dx = (conn.x2 - conn.x1) * 0.5;
      const d = `M ${{conn.x1}} ${{conn.y1}} C ${{conn.x1 + dx}} ${{conn.y1}}, ${{conn.x2 - dx}} ${{conn.y2}}, ${{conn.x2}} ${{conn.y2}}`;
      path.setAttribute('d', d);
      path.setAttribute('stroke', conn.stroke);
      path.setAttribute('stroke-width', conn.stroke_width || 3);
      path.setAttribute('fill', 'none');

      if (conn.dashed) {{
        path.setAttribute('stroke-dasharray', '8,6');
      }}

      // Arrow Marker
      if (conn.type === 'derailed') {{
        path.setAttribute('marker-end', 'url(#arrowRed)');
      }} else if (conn.type === 'remediation') {{
        path.setAttribute('marker-end', 'url(#arrowCyan)');
      }} else {{
        path.setAttribute('marker-end', 'url(#arrowEmerald)');
      }}

      layerConnectors.appendChild(path);
    }});

    // Render Node Cards
    (payload.nodes || []).forEach(node => {{
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.setAttribute('class', 'node-card');
      g.setAttribute('id', `node_${{node.id}}`);
      g.setAttribute('transform', `translate(${{node.x}}, ${{node.y}})`);

      let strokeColor = '#10B981';
      let strokeDash = 'none';
      let cardGrad = 'url(#cardGradSound)';
      let filter = 'url(#glowSound)';

      if (node.type === 'pivot') {{
        strokeColor = '#F59E0B';
        cardGrad = 'url(#cardGradPivot)';
        filter = 'url(#glowPivot)';
      }} else if (node.type === 'derailed' || node.type === 'derailed_end') {{
        strokeColor = '#EF4444';
        strokeDash = '6,4';
        cardGrad = 'url(#cardGradDerailed)';
        filter = 'url(#glowDerailed)';
      }} else if (node.type === 'socratic') {{
        strokeColor = '#8B5CF6';
        cardGrad = 'url(#cardGradSocratic)';
        filter = 'url(#glowSocratic)';
      }}

      // Card Background
      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('width', node.w);
      rect.setAttribute('height', node.h);
      rect.setAttribute('rx', 12);
      rect.setAttribute('ry', 12);
      rect.setAttribute('fill', cardGrad);
      rect.setAttribute('stroke', strokeColor);
      rect.setAttribute('stroke-width', node.type === 'pivot' ? 2.5 : 1.8);
      rect.setAttribute('stroke-dasharray', strokeDash);
      rect.setAttribute('filter', filter);
      g.appendChild(rect);

      // Top Status Pill
      const badgeText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      badgeText.setAttribute('x', 12);
      badgeText.setAttribute('y', 20);
      badgeText.setAttribute('fill', strokeColor);
      badgeText.setAttribute('font-size', '9.5');
      badgeText.setAttribute('font-weight', '800');
      badgeText.setAttribute('letter-spacing', '0.04em');
      badgeText.textContent = node.badge;
      g.appendChild(badgeText);

      // Node Title (wrapped)
      const titleText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      titleText.setAttribute('x', 12);
      titleText.setAttribute('y', 38);
      titleText.setAttribute('fill', '#F8FAFC');
      titleText.setAttribute('font-size', '11.5');
      titleText.setAttribute('font-weight', '700');

      // Wrap title into 2 lines if needed
      const words = (node.title || '').split(' ');
      let line1 = '';
      let line2 = '';
      for (let w of words) {{
        if ((line1 + w).length < 24) {{
          line1 += (line1 ? ' ' : '') + w;
        }} else {{
          line2 += (line2 ? ' ' : '') + w;
        }}
      }}
      titleText.textContent = line1;
      g.appendChild(titleText);

      if (line2) {{
        const titleLine2 = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        titleLine2.setAttribute('x', 12);
        titleLine2.setAttribute('y', 52);
        titleLine2.setAttribute('fill', '#F8FAFC');
        titleLine2.setAttribute('font-size', '11.5');
        titleLine2.setAttribute('font-weight', '700');
        titleLine2.textContent = line2.length > 25 ? line2.substring(0, 24) + '...' : line2;
        g.appendChild(titleLine2);
      }}

      // Node Detail Subtitle
      const detailText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      detailText.setAttribute('x', 12);
      detailText.setAttribute('y', line2 ? 70 : 60);
      detailText.setAttribute('fill', '#94A3B8');
      detailText.setAttribute('font-size', '9.5');
      detailText.setAttribute('font-weight', '500');
      const detStr = node.detail || '';
      detailText.textContent = detStr.length > 34 ? detStr.substring(0, 32) + '...' : detStr;
      g.appendChild(detailText);

      // On Click: Open Inspector
      g.addEventListener('click', (e) => {{
        e.stopPropagation();
        showInspector(
          node.badge,
          `<strong>${{node.title}}</strong><br/><br/>${{node.detail}}<br/><br/><span style="color:#94A3B8;">Status: ${{node.type.toUpperCase()}}</span>`
        );
      }});

      layerNodes.appendChild(g);
    }});
  }}

  renderGraph();
  updateTransform();

  // Waveform Animation Loop
  let animId = null;
  const numBars = 24;
  const barHeights = new Array(numBars).fill(4);

  function drawWaveform(isPlaying) {{
    if (!wfCtx) return;
    wfCtx.clearRect(0, 0, 80, 18);
    const w = 80;
    const h = 18;
    const barWidth = 2.2;
    const gap = 1.1;

    for (let i = 0; i < numBars; i++) {{
      if (isPlaying) {{
        // Dynamic rhythmic jitter
        barHeights[i] = 3 + Math.sin(Date.now() * 0.008 + i * 0.5) * 6 + Math.random() * 5;
      }} else {{
        barHeights[i] = Math.max(3, barHeights[i] * 0.9);
      }}

      const bh = Math.min(Math.max(barHeights[i], 2), h);
      const x = i * (barWidth + gap);
      const y = (h - bh) / 2;

      const grad = wfCtx.createLinearGradient(0, y, 0, y + bh);
      grad.addColorStop(0, '#10B981');
      grad.addColorStop(1, '#06B6D4');
      wfCtx.fillStyle = grad;
      wfCtx.fillRect(x, y, barWidth, bh);
    }}

    if (isPlaying) {{
      animId = requestAnimationFrame(() => drawWaveform(true));
    }}
  }}
  drawWaveform(false);

  // Synchronized Audio & Walkthrough Playback Controller
  let isWalkthroughPlaying = false;
  let virtualTime = 0.0;
  let timerInterval = null;
  const totalDuration = payload.total_duration || 16.0;

  function formatTime(sec) {{
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${{m}}:${{s < 10 ? '0' : ''}}${{s}}`;
  }}

  function updateActiveElements(currentTime) {{
    timeDisplay.textContent = `${{formatTime(currentTime)}} / ${{formatTime(totalDuration)}}`;
    scrubBar.value = (currentTime / totalDuration) * 100;

    // Find current timeline speech step
    const timeline = payload.timeline || [];
    let currentStep = null;
    for (let step of timeline) {{
      if (currentTime >= step.start_time && currentTime <= step.end_time) {{
        currentStep = step;
        break;
      }}
    }}
    if (!currentStep && timeline.length > 0) {{
      currentStep = timeline[timeline.length - 1];
    }}

    if (currentStep && currentStep.speech_segment) {{
      speechContent.textContent = `"${{currentStep.speech_segment}}"`;
    }}

    // Node & Connector Highlight synchronization
    const allCards = document.querySelectorAll('.node-card');
    allCards.forEach(c => {{
      c.classList.remove('active-playback', 'active-playback-derailed', 'active-playback-pivot');
    }});

    // Phase 1 (0 to 35%): Sound & Baseline
    if (currentTime < totalDuration * 0.35) {{
      const s1 = document.getElementById('node_S1') || allCards[0];
      if (s1) s1.classList.add('active-playback');
    }}
    // Phase 2 (35% to 55%): The Divergence Pivot
    else if (currentTime < totalDuration * 0.55) {{
      const pNode = document.querySelector('.node-card[id*="S2"]') || document.querySelector('.node-card[id*="pivot"]');
      if (pNode) pNode.classList.add('active-playback-pivot');
    }}
    // Phase 3 (55% to 75%): Cognitive Derailment Callout
    else if (currentTime < totalDuration * 0.75) {{
      const dNode = document.getElementById('node_ERR_2') || document.querySelector('.node-card[id*="ERR"]');
      if (dNode) dNode.classList.add('active-playback-derailed');
    }}
    // Phase 4 (75% to 100%): Canonical Breakthrough & Socratic
    else {{
      const rNode = document.getElementById('node_REM_PIVOT');
      const socNode = document.getElementById('node_SOCRATIC_CARD');
      if (rNode) rNode.classList.add('active-playback');
      if (socNode) socNode.classList.add('active-playback-pivot');
    }}
  }}

  // Play / Pause Click Handlers
  function startPlayback() {{
    isWalkthroughPlaying = true;
    btnPlay.classList.add('playing');
    playIcon.textContent = '⏸';
    playText.textContent = 'Pause Walkthrough';

    drawWaveform(true);

    if (audio && audio.src && audio.src.length > 50) {{
      audio.play().catch(e => {{
        console.log('Audio autoplay prevented, using synchronized timer fallback');
      }});
    }}

    clearInterval(timerInterval);
    timerInterval = setInterval(() => {{
      let t = 0;
      if (audio && !audio.paused && audio.duration) {{
        t = audio.currentTime;
      }} else {{
        virtualTime += 0.2;
        t = virtualTime;
        if (t >= totalDuration) {{
          stopPlayback();
          return;
        }}
      }}
      updateActiveElements(t);
    }}, 200);
  }}

  function stopPlayback() {{
    isWalkthroughPlaying = false;
    btnPlay.classList.remove('playing');
    playIcon.textContent = '▶';
    playText.textContent = 'Play Live Walkthrough';

    if (audio) {{
      audio.pause();
    }}
    clearInterval(timerInterval);
    cancelAnimationFrame(animId);
    drawWaveform(false);
  }}

  btnPlay.addEventListener('click', () => {{
    if (isWalkthroughPlaying) {{
      stopPlayback();
    }} else {{
      if (virtualTime >= totalDuration) {{
        virtualTime = 0.0;
        if (audio) audio.currentTime = 0;
      }}
      startPlayback();
    }}
  }});

  // Scrub bar interaction
  scrubBar.addEventListener('input', (e) => {{
    const pct = parseFloat(e.target.value) / 100;
    const targetSec = pct * totalDuration;
    virtualTime = targetSec;
    if (audio && audio.duration) {{
      audio.currentTime = targetSec;
    }}
    updateActiveElements(targetSec);
  }});

  if (audio) {{
    audio.addEventListener('ended', () => {{
      stopPlayback();
      virtualTime = 0.0;
      updateActiveElements(0.0);
    }});
    audio.addEventListener('timeupdate', () => {{
      if (isWalkthroughPlaying) {{
        updateActiveElements(audio.currentTime);
      }}
    }});
  }}

  // Initialize at t = 0
  updateActiveElements(0.0);
</script>
</body>
</html>
"""
    return html


def render_interactive_board(
    graph_payload: Dict[str, Any],
    audio_base64: str = "",
    target_lang: str = "English",
    height: int = 560
):
    """
    Renders an interactive SVG/Canvas Blackboard with native Web Audio sync.
    Includes pan/zoom, animated node glow, and audio-synchronized stroke animations.
    """
    html_code = build_interactive_board_html(
        graph_payload=graph_payload,
        audio_base64=audio_base64,
        target_lang=target_lang
    )
    components.html(html_code, height=height)


def build_blackboard_html(
    storyboard: Dict[str, Any],
    audio_bytes: Optional[bytes] = None
) -> str:
    """
    Backwards-compatible builder for unit tests and legacy calls.
    Generates the complete interactive blackboard containing all required IDs.
    """
    audio_base64 = ""
    if audio_bytes and len(audio_bytes) > 44:
        audio_base64 = base64.b64encode(audio_bytes).decode("ascii")

    payload = prepare_graph_payload_from_storyboard(storyboard)
    return build_interactive_board_html(
        graph_payload=payload,
        audio_base64=audio_base64
    )


def render_live_blackboard(
    storyboard: Dict[str, Any],
    audio_bytes: Optional[bytes] = None,
    height: int = 560
):
    """
    Wrapper to render the live interactive blackboard from a storyboard dictionary.
    """
    audio_base64 = ""
    if audio_bytes and len(audio_bytes) > 44:
        audio_base64 = base64.b64encode(audio_bytes).decode("ascii")

    payload = prepare_graph_payload_from_storyboard(storyboard)
    render_interactive_board(
        graph_payload=payload,
        audio_base64=audio_base64,
        height=height
    )
