# https://surajshivam-123-sarvamdoubtsolver-app-l9gqc5.streamlit.app/
"""
Sansay (संशय) - Socratic Cross-Disciplinary Academic Doubt Solver
A cross-disciplinary pedagogical web application across:
- Humanities, Law, and Constitutional Jurisprudence
- Economics, Business, and Social Sciences
- World History and International Relations
- Literature, Philosophy, and Dramatic Theory
- Computer Science, Algorithms, and Logic
- STEM, Physics, and Natural Sciences

Features:
1. Enforces active student retrieval (No direct solutions)
2. Pinpoints root conceptual misconceptions via diagnostic evaluation
3. Persists a longitudinal learner profile across questions
4. Renders thought processes as interactive Graphviz comparative concept/flow maps
   - Map A: Student's Actual Path (Coral/Red error nodes)
   - Map B: Remediated Conceptual Path (Emerald Green pivot nodes)
5. Delivers multilingual auditory narration using Sarvam AI Text-to-Speech (TTS)
   - Supports Indian languages with native bulbul:v3 speakers
   - Dedicated separate Hindi (हिंदी) and Hinglish (हिंग्लिश) modes
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

import learner_model
import pedagogy_engine
import sarvam_tts
import blackboard_component
from sample_doubts import SAMPLE_DOUBTS

# ---------------------------------------------------------
# Page Configuration & Modern Theme Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sansay (संशय) | AI Socratic Academic Doubt Solver",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    /* =========================================================
       Design Tokens & Typography Reset (Plus Jakarta Sans)
       ========================================================= */
    html, body, .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: #0f172a;
    }

    /* Apply typography to text elements while preserving icon fonts */
    h1, h2, h3, h4, h5, h6, p, label, input, textarea, select, 
    .stMarkdown, .stText, [data-testid="stMarkdownContainer"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    code, kbd, samp, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* SaaS Dashboard Slate Canvas */
    .stApp {
        background-color: #f8fafc !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.04) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.04) 0px, transparent 50%) !important;
    }

    /* Glassmorphism Header */
    header[data-testid="stHeader"] {
        background: rgba(248, 250, 252, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid rgba(226, 232, 240, 0.8) !important;
    }

    div[data-testid="stDecoration"] {
        display: none !important;
    }

    footer {
        display: none !important;
    }

    /* Responsive Main Block Container */
    [data-testid="stMainBlockContainer"], section.main .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 5rem !important;
        max-width: 1280px !important;
    }

    /* Sleek Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* =========================================================
       SaaS Dashboard Components (Linear / Vercel / shadcn inspired)
       ========================================================= */
    .saas-hero {
        position: relative;
        background: linear-gradient(180deg, #09090b 0%, #18181b 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 1.25rem 1.6rem;
        margin-bottom: 1.5rem;
        box-shadow: 
            0 10px 15px -3px rgba(0, 0, 0, 0.15),
            0 4px 6px -4px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .saas-hero::before {
        content: "";
        position: absolute;
        top: -60%;
        left: -30%;
        width: 160%;
        height: 160%;
        background: radial-gradient(circle at 40% 10%, rgba(16, 185, 129, 0.12), transparent 60%);
        pointer-events: none;
    }

    .status-pill-pulse {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.25rem 0.75rem;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 600;
        color: #34d399;
        letter-spacing: 0.03em;
    }

    .pulse-dot {
        width: 6px;
        height: 6px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse-ring 2s infinite cubic-bezier(0.66, 0, 0, 1);
    }

    @keyframes pulse-ring {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.15;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 60%, #a7f3d0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
        z-index: 1;
    }

    .bridge-chip {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #e2e8f0;
        padding: 0.2rem 0.65rem;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* SaaS White Container Card */
    .saas-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.4rem 1.65rem;
        margin-bottom: 1.35rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
    }

    .saas-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 0.85rem;
        margin-bottom: 1.15rem;
        border-bottom: 1px solid #f1f5f9;
    }

    .saas-card-title {
        font-size: 1.12rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0;
    }

    .step-badge {
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        color: #475569;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
    }

    /* Section Kicker */
    .presets-section-title {
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Socratic Guardrail Banner */
    .guardrail-callout {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 4.5px solid #10b981;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.35rem;
        font-size: 0.91rem;
        color: #065f46;
        display: flex;
        align-items: flex-start;
        gap: 0.85rem;
        line-height: 1.5;
        box-shadow: 0 1px 2px 0 rgba(16, 185, 129, 0.04);
    }

    /* Diagnostic Callout Banners */
    .derailment-banner {
        background: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 4.5px solid #ef4444;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px 0 rgba(239, 68, 68, 0.06);
    }

    .derailment-title {
        font-size: 1.08rem;
        font-weight: 700;
        color: #991b1b;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .derailment-concept {
        font-size: 0.95rem;
        font-weight: 600;
        color: #7f1d1d;
        margin-top: 0.35rem;
    }

    .derailment-desc {
        font-size: 0.9rem;
        color: #450a0a;
        margin-top: 0.35rem;
        line-height: 1.5;
    }

    .remediation-banner {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 4.5px solid #10b981;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px 0 rgba(16, 185, 129, 0.06);
    }

    .longitudinal-banner {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 4.5px solid #f59e0b;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px 0 rgba(245, 158, 11, 0.06);
        font-size: 0.91rem;
        color: #92400e;
        line-height: 1.5;
    }

    /* Socratic Active Retrieval Challenge Box */
    .socratic-challenge-box {
        background: linear-gradient(180deg, #ecfdf5 0%, #f0fdf4 100%);
        border: 1.5px dashed #059669;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-top: 1.25rem;
        margin-bottom: 1.25rem;
    }

    .socratic-prompt-text {
        font-size: 1.02rem;
        font-weight: 500;
        color: #064e3b;
        line-height: 1.55;
        margin-top: 0.5rem;
    }

    /* Canvas Frame & Toolbar for Graphviz */
    .canvas-toolbar {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-bottom: none;
        border-radius: 12px 12px 0 0;
        padding: 0.65rem 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.78rem;
        font-weight: 600;
        color: #64748b;
    }

    /* Node Breakdown List Cards */
    .node-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
        transition: all 0.15s ease;
    }

    .node-card:hover {
        border-color: #cbd5e1;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.04);
    }

    .node-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.9rem;
        font-weight: 600;
        color: #1e293b;
    }

    .node-card-detail {
        font-size: 0.82rem;
        color: #64748b;
        margin-top: 0.35rem;
        line-height: 1.45;
    }

    /* Auditory & Spoken Narration Script Card */
    .audio-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.3rem 1.4rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
    }

    .narration-quote {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        font-size: 0.94rem;
        line-height: 1.6;
        color: #334155;
        font-style: italic;
        margin-top: 0.6rem;
        box-shadow: inset 0 1px 2px 0 rgba(0, 0, 0, 0.02);
    }

    /* Badges */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.25rem 0.65rem;
        font-size: 0.72rem;
        font-weight: 600;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        line-height: 1;
    }

    .badge-green { background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
    .badge-amber { background-color: #fffbeb; color: #b45309; border: 1px solid #fde68a; }
    .badge-coral { background-color: #fff1f2; color: #be123c; border: 1px solid #fecdd3; }
    .badge-blue  { background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
    .badge-purple{ background-color: #faf5ff; color: #7e22ce; border: 1px solid #e9d5ff; }
    .badge-slate { background-color: #f8fafc; color: #475569; border: 1px solid #e2e8f0; }

    /* =========================================================
       Streamlit Native Component Overrides (Tactile Web Styling)
       ========================================================= */

    /* Primary Button: Gradient emerald with elevation */
    div[data-testid="stButton"] button[kind="primary"],
    button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05), 0 4px 14px 0 rgba(16, 185, 129, 0.28) !important;
        padding: 0.65rem 1.25rem !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        letter-spacing: -0.01em !important;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover,
    button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #34d399 0%, #059669 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px 0 rgba(16, 185, 129, 0.38) !important;
    }

    div[data-testid="stButton"] button[kind="primary"]:active,
    button[data-testid="stBaseButton-primary"]:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 6px 0 rgba(16, 185, 129, 0.25) !important;
    }

    /* Secondary / Preset Buttons / Download Button */
    div[data-testid="stButton"] button[kind="secondary"],
    button[data-testid="stBaseButton-secondary"],
    div[data-testid="stDownloadButton"] button {
        background: #ffffff !important;
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03) !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    div[data-testid="stButton"] button[kind="secondary"]:hover,
    button[data-testid="stBaseButton-secondary"]:hover,
    div[data-testid="stDownloadButton"] button:hover {
        background: #f8fafc !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 8px -1px rgba(0, 0, 0, 0.08) !important;
    }

    /* Inputs & Textareas */
    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-testid="stTextInputRootElement"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02) !important;
        transition: all 0.18s ease-in-out !important;
    }

    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within,
    div[data-testid="stTextInputRootElement"]:focus-within {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15), 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }

    input, textarea {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.92rem !important;
        color: #0f172a !important;
    }

    /* =========================================================
       Password Visibility Toggle & Material Symbols Icon Fix
       ========================================================= */
    [data-testid*="Icon"],
    [class*="material-symbols"],
    [class*="e1vmumty"],
    span[data-testid="stIconMaterial"],
    div[data-testid="stTextInput"] button span,
    div[data-testid="stTextInput"] [class*="e1vmumty"],
    .material-symbols-rounded {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 1.25rem !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        font-feature-settings: 'liga' 1 !important;
        -webkit-font-feature-settings: 'liga' 1 !important;
        -webkit-font-smoothing: antialiased !important;
        color: #64748b !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    div[data-testid="stTextInput"] button {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        padding: 0 0.5rem !important;
        cursor: pointer !important;
        color: #64748b !important;
        visibility: visible !important;
        opacity: 0.8 !important;
    }

    div[data-testid="stTextInput"] button:hover {
        opacity: 1 !important;
        color: #0f172a !important;
        background: transparent !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* Selectboxes */
    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02) !important;
        transition: all 0.18s ease !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15) !important;
    }

    /* Segmented Control Tabs (shadcn/ui style) */
    div[data-baseweb="tab-list"] {
        background: #f1f5f9 !important;
        padding: 4px !important;
        border-radius: 12px !important;
        gap: 4px !important;
        border: 1px solid #e2e8f0 !important;
        margin-bottom: 1.25rem !important;
    }

    button[data-baseweb="tab"] {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        color: #64748b !important;
        padding: 7px 16px !important;
        background: transparent !important;
        border: none !important;
        transition: all 0.15s ease-in-out !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #0f172a !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.08), 0 1px 2px -1px rgba(0, 0, 0, 0.08) !important;
    }

    div[data-baseweb="tab-highlight"],
    div[data-baseweb="tab-border"] {
        display: none !important;
    }

    /* KPI Metric Cards */
    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.15rem !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stMetric"]:hover {
        border-color: #cbd5e1 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px -2px rgba(0, 0, 0, 0.06) !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: #64748b !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.65rem !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        letter-spacing: -0.02em !important;
    }

    /* Expanders */
    details[data-testid="stExpander"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02) !important;
        margin-bottom: 0.75rem !important;
        overflow: hidden !important;
        transition: border-color 0.18s ease !important;
    }

    details[data-testid="stExpander"]:hover {
        border-color: #cbd5e1 !important;
    }

    summary[data-testid="stExpanderSummary"] {
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        color: #334155 !important;
        padding: 0.75rem 1rem !important;
    }

    /* Graphviz Chart Container */
    div[data-testid="stGraphvizChart"] {
        display: flex !important;
        justify-content: center !important;
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 1.25rem !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03) !important;
    }

    /* Sidebar Custom Styling */
    section[data-testid="stSidebar"] {
        background-color: #fbfcfd !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.8rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }

    .sidebar-brand-box {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        padding: 0.8rem 0.95rem;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        margin-bottom: 1.4rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }

    .sidebar-section-kicker {
        font-size: 0.68rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        margin-top: 1.1rem;
        margin-bottom: 0.45rem;
    }

    .student-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }

    .student-card-header {
        display: flex;
        align-items: center;
        gap: 0.65rem;
    }

    .student-avatar {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #10b981 0%, #047857 100%);
        color: #ffffff;
        font-weight: 700;
        font-size: 0.88rem;
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 4px 0 rgba(16, 185, 129, 0.2);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------
if "selected_student_id" not in st.session_state:
    st.session_state.selected_student_id = "arjun_01"

if "current_profile" not in st.session_state:
    st.session_state.current_profile = learner_model.load_profile(st.session_state.selected_student_id)

profile = st.session_state.current_profile

if "diagnosis_result" not in st.session_state:
    st.session_state.diagnosis_result = None

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if "audio_status_msg" not in st.session_state:
    st.session_state.audio_status_msg = ""

if "socratic_response_msg" not in st.session_state:
    st.session_state.socratic_response_msg = None

if "socratic_solved" not in st.session_state:
    st.session_state.socratic_solved = False

# Form text fields
for key in ["form_doubt", "form_concept", "form_steps", "form_breakdown"]:
    if key not in st.session_state:
        st.session_state[key] = ""


# ---------------------------------------------------------
# Sidebar: Modern SaaS Control Panel
# ---------------------------------------------------------
with st.sidebar:
    # Sidebar Brand Header with Sansay SVG Logo
    st.markdown(
        """
        <div class="sidebar-brand-box">
            <div style="flex-shrink:0;">
                <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="36" height="36" rx="10" fill="url(#sb-sansay-grad)"/>
                    <path d="M10.5 13C10.5 10.7909 12.2909 9 14.5 9H21.5C23.9853 9 26 11.0147 26 13.5C26 15.9853 23.9853 18 21.5 18H14.5C12.0147 18 10 20.0147 10 22.5C10 24.9853 12.0147 27 14.5 27H21.5C23.7091 27 25.5 25.2091 25.5 23" stroke="white" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="18" cy="18" r="2.2" fill="#A7F3D0"/>
                    <defs>
                        <linearGradient id="sb-sansay-grad" x1="0" y1="0" x2="36" y2="36" gradientUnits="userSpaceOnUse">
                            <stop stop-color="#10B981"/>
                            <stop offset="1" stop-color="#047857"/>
                        </linearGradient>
                    </defs>
                </svg>
            </div>
            <div>
                <div style="font-weight:800; font-size:1.15rem; letter-spacing:-0.03em; color:#0f172a; line-height:1.1;">
                    Sansay <span style="font-size:0.88rem; font-weight:600; color:#059669;">(संशय)</span>
                </div>
                <div style="font-size:0.72rem; color:#64748b; font-weight:600; letter-spacing:0.02em;">Socratic Engine v2.4</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1. Language Matrix
    st.markdown("<div class='sidebar-section-kicker'>01 // Translation & Voice Matrix</div>", unsafe_allow_html=True)

    input_lang_name = st.selectbox(
        "Student Input Language:",
        options=list(sarvam_tts.LANGUAGE_REGISTRY.keys()),
        index=0,
        help="Language used for student question and reasoning formulation."
    )

    output_lang_name = st.selectbox(
        "Voice & Remediation Target:",
        options=list(sarvam_tts.LANGUAGE_REGISTRY.keys()),
        index=2,  # Default to Hinglish (हिंग्लिश) with Hindi (हिंदी) available
        help="Language used for thought maps narration and Sarvam TTS synthesis."
    )
    target_cfg = sarvam_tts.LANGUAGE_REGISTRY[output_lang_name]
    lang_code = target_cfg["code"]
    default_speaker = target_cfg["speaker"]

    if "Hinglish" in output_lang_name or "हिंग्लिश" in output_lang_name:
        st.markdown(
            """
            <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:0.5rem 0.75rem; font-size:0.76rem; color:#065f46; margin-top:0.35rem; line-height:1.4;">
                💡 <b>Hinglish (हिंग्लिश) Mode:</b> Technical terminology across Law, Economics, History, Literature, Coding, and Science is preserved in conversational English for clarity.
            </div>
            """,
            unsafe_allow_html=True
        )
    elif "Hindi" in output_lang_name or "हिंदी" in output_lang_name:
        st.markdown(
            """
            <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:0.5rem 0.75rem; font-size:0.76rem; color:#1e40af; margin-top:0.35rem; line-height:1.4;">
                🇮🇳 <b>Hindi (हिंदी) Mode:</b> सभी क्षेत्रों (विधि, अर्थशास्त्र, इतिहास, साहित्य, कोडिंग, विज्ञान) की मानक शब्दावली हिंदी में प्रस्तुत की जाती है।
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # 2. Sarvam AI Configuration
    st.markdown("<div class='sidebar-section-kicker'>02 // Sarvam AI API Engine</div>", unsafe_allow_html=True)
    detected_key = sarvam_tts.get_configured_api_key()
    sarvam_key = st.text_input(
        "API Subscription Key",
        value=detected_key,
        type="password",
        placeholder="Enter your api-subscription-key",
        help="Loaded automatically from st.secrets or .env. Used for translation and speech dictation."
    )

    speaker = st.selectbox(
        "Voice Persona:",
        options=[default_speaker, "ritu", "aditya", "priya", "simran", "soham", "gokul", "kavitha", "pooja", "chaitra", "anand"],
        index=0,
        help="Native Indian language speaker profile."
    )

    tts_model = st.selectbox("TTS Architecture:", options=sarvam_tts.MODEL_OPTIONS, index=0)

    if sarvam_key:
        st.markdown("<span class='badge-pill badge-green'>✓ Sarvam API Key Active</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='badge-pill badge-amber'>ℹ Acoustic Wave Fallback</span>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Main Application Content: SaaS Hero Banner
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="saas-hero">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; position:relative; z-index:1;">
            <div style="display:flex; align-items:center; gap:1rem;">
                <div style="flex-shrink:0;">
                    <svg width="44" height="44" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 2px 10px rgba(16, 185, 129, 0.35));">
                        <rect width="48" height="48" rx="12" fill="url(#hero-sansay-grad)"/>
                        <path d="M14 17C14 13.6863 16.6863 11 20 11H28C31.866 11 35 14.134 35 18C35 21.866 31.866 25 28 25H20C16.134 25 13 28.134 13 32C13 35.866 16.134 39 20 39H28C31.3137 39 34 36.3137 34 33" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                        <circle cx="24" cy="25" r="3" fill="#A7F3D0"/>
                        <circle cx="24" cy="25" r="6.5" stroke="#A7F3D0" stroke-width="1.2" stroke-dasharray="2 2" opacity="0.8"/>
                        <defs>
                            <linearGradient id="hero-sansay-grad" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#34D399"/>
                                <stop offset="0.5" stop-color="#10B981"/>
                                <stop offset="1" stop-color="#047857"/>
                            </linearGradient>
                        </defs>
                    </svg>
                </div>
                <div>
                    <div style="display:flex; align-items:baseline; gap:0.5rem; flex-wrap:wrap;">
                        <span class="hero-title">Sansay</span>
                        <span style="font-size:1.35rem; font-weight:700; color:#34d399;">(संशय)</span>
                    </div>
                    <div style="font-size:0.86rem; color:#94a3b8; margin-top:0.15rem; font-weight:400;">
                        Cognitive Derailment Diagnostics & Multilingual Socratic Remediation
                    </div>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:0.6rem; flex-wrap:wrap;">
                <span class="bridge-chip">{input_lang_name} ➔ {output_lang_name}</span>
                <div class="status-pill-pulse">
                    <span class="pulse-dot"></span>
                    Sarvam AI Active
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# 1-Click Multi-Domain Demos
# ---------------------------------------------------------
st.markdown("<div class='presets-section-title'>⚡ Curated Multi-Domain Demos (1-Click Load):</div>", unsafe_allow_html=True)
demo_cols = st.columns(6)

def load_sample(key: str):
    import importlib
    import sample_doubts
    # Bust stale module cache if key missing (common after Streamlit hot-reloads on Cloud)
    if key not in sample_doubts.SAMPLE_DOUBTS:
        importlib.reload(sample_doubts)
        global SAMPLE_DOUBTS
        SAMPLE_DOUBTS = sample_doubts.SAMPLE_DOUBTS

    s = sample_doubts.SAMPLE_DOUBTS.get(key)
    if not s:
        st.warning(f"⚠️ Demo doubt '{key}' could not be loaded. If you recently updated the app, please reboot the app via Streamlit Cloud menu ('Manage app' ➔ ⋮ ➔ 'Reboot app').")
        return

    is_hi = ("Hindi" in input_lang_name or "हिंदी" in input_lang_name) and ("Hinglish" not in input_lang_name and "हिंग्लिश" not in input_lang_name)
    st.session_state.form_doubt = s.get("problem_statement_hi") if (is_hi and s.get("problem_statement_hi")) else s.get("problem_statement", "")
    st.session_state.form_concept = s.get("student_concept_hi") if (is_hi and s.get("student_concept_hi")) else s.get("student_concept", "")
    st.session_state.form_steps = s.get("student_steps_hi") if (is_hi and s.get("student_steps_hi")) else s.get("student_steps", "")
    st.session_state.form_breakdown = s.get("student_breakdown_hi") if (is_hi and s.get("student_breakdown_hi")) else s.get("student_breakdown", "")
    st.session_state.diagnosis_result = None
    st.session_state.audio_bytes = None
    st.session_state.socratic_response_msg = None
    st.session_state.socratic_solved = False

with demo_cols[0]:
    if st.button("⚖️ Law & Civics", use_container_width=True, help="Freedom of Speech & Public Order (Art 19)"):
        load_sample("law_freedom_of_speech")
        st.rerun()

with demo_cols[1]:
    if st.button("📉 Economics", use_container_width=True, help="Rent Control & Supply Elasticity Deadweight Loss"):
        load_sample("economics_rent_control")
        st.rerun()

with demo_cols[2]:
    if st.button("📜 History", use_container_width=True, help="Origins of WWI: Trigger vs Structural M-A-I-N Causes"):
        load_sample("history_ww1_causality")
        st.rerun()

with demo_cols[3]:
    if st.button("📖 Literature", use_container_width=True, help="Shakespeare's Macbeth: Fatal Flaw (Hamartia) vs Fate"):
        load_sample("literature_macbeth_tragic_flaw")
        st.rerun()

with demo_cols[4]:
    if st.button("💻 Coding", use_container_width=True, help="Balanced Parentheses & Stack Invariant"):
        load_sample("coding_balanced_parentheses")
        st.rerun()

with demo_cols[5]:
    if st.button("🏔️ Physics", use_container_width=True, help="Work-Energy & Friction Dissipation"):
        load_sample("spring_friction_energy")
        st.rerun()

st.markdown("<div style='margin-bottom: 1.25rem;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# STAGE 1: Socratic Elicitation (No Direct Answers Guardrail)
# ---------------------------------------------------------
is_input_pure_hindi = ("Hindi" in input_lang_name or "हिंदी" in input_lang_name) and ("Hinglish" not in input_lang_name and "हिंग्लिश" not in input_lang_name)
is_input_hinglish = ("Hinglish" in input_lang_name or "हिंग्लिश" in input_lang_name)

if is_input_pure_hindi:
    lbl_doubt = "1. समस्या या अकादमिक संशय का विवरण (हिंदी):"
    ph_doubt = "यहाँ किसी भी विषय (विधि, अर्थशास्त्र, इतिहास, साहित्य, कोडिंग, विज्ञान) का संशय दर्ज करें..."
    lbl_concept = "2. लागू होने वाला सिद्धांत / नियम / अवधारणा (हिंदी):"
    ph_concept = "उदा. अनुच्छेद 19(2), मूल्य सीमा, M-A-I-N कारणता, हमारशिया, स्टैक, यांत्रिक ऊर्जा"
    lbl_breakdown = "4. आपके अनुसार तर्क कहाँ अटक रहा है? (हिंदी):"
    ph_breakdown = "उदा. निष्कर्ष गलत आ रहा है, या सीमांत शर्त समझ नहीं आ रही..."
    lbl_steps = "3. आपका चरणबद्ध तर्क / हल करने का प्रयास (हिंदी):"
    ph_steps = "चरण 1: ...\nचरण 2: ...\nचरण 3: ..."
    guardrail_badge = "चरण 01 • सक्रिय अन्वेषण"
    guardrail_msg = "सक्रिय पुनरुत्थान: सीधे उत्तर देने के बजाय आपकी सोच के सटीक विचलन बिंदु की पहचान की जाएगी।"
elif is_input_hinglish:
    lbl_doubt = "1. Problem Statement / Academic Doubt (हिंग्लिश):"
    ph_doubt = "Apna academic question ya doubt yahan enter karein (Law, Econ, History, Lit, CS, Science)..."
    lbl_concept = "2. Core Concept / Law / Principle (हिंग्लिश):"
    ph_concept = "e.g. Article 19(2), Rent Control, WWI M-A-I-N Causality, Hamartia, Stack Invariant, Energy"
    lbl_breakdown = "4. Reasoning Kahan Breakdown Ya Stuck Ho Rahi Hai? (हिंग्लिश):"
    ph_breakdown = "e.g. Conclusion contradict ho raha hai, ya boundary condition clear nahi hai..."
    lbl_steps = "3. Aapka Step-by-Step Logic / Attempted Derivation (हिंग्लिश):"
    ph_steps = "Step 1: ...\nStep 2: ...\nStep 3: ..."
    guardrail_badge = "Stage 01 • Active Elicitation"
    guardrail_msg = "Active Retrieval: Isolating your exact cognitive derailment node without direct answer leakage."
else:
    lbl_doubt = f"1. Problem Statement or Academic Doubt ({input_lang_name}):"
    ph_doubt = "Enter your question or doubt here (Law, Economics, History, Literature, CS, Science)..."
    lbl_concept = f"2. Core Concept / Law / Principle ({input_lang_name}):"
    ph_concept = "e.g. Free Speech Limits, Price Elasticity, Structural Causality, Tragic Flaw, Stack Invariants, Work-Energy"
    lbl_breakdown = f"4. Where Reasoning Breaks Down or Feels Stuck ({input_lang_name}):"
    ph_breakdown = "e.g. The conclusion contradicts assumptions, or boundary conditions fail..."
    lbl_steps = f"3. Your Step-by-Step Logic / Attempted Derivation So Far ({input_lang_name}):"
    ph_steps = "Step 1: ...\nStep 2: ...\nStep 3: ..."
    guardrail_badge = "Stage 01 • Active Elicitation"
    guardrail_msg = "Active Retrieval: Isolating your exact cognitive derailment node without direct answer leakage."

st.markdown(
    f"""
    <div class="saas-card">
        <div class="saas-card-header">
            <div>
                <div class="saas-card-title">
                    <span>📝 Stage 1: Problem Articulation & Mental Model</span>
                </div>
                <div style="font-size:0.8rem; color:#64748b; margin-top:0.25rem;">
                    {guardrail_msg}
                </div>
            </div>
            <span class="step-badge">{guardrail_badge}</span>
        </div>
    """,
    unsafe_allow_html=True
)

doubt_input = st.text_area(
    lbl_doubt,
    value=st.session_state.form_doubt,
    height=85,
    placeholder=ph_doubt
)

col_e1, col_e2 = st.columns(2)
with col_e1:
    concept_input = st.text_input(
        lbl_concept,
        value=st.session_state.form_concept,
        placeholder=ph_concept
    )
with col_e2:
    breakdown_input = st.text_input(
        lbl_breakdown,
        value=st.session_state.form_breakdown,
        placeholder=ph_breakdown
    )

steps_input = st.text_area(
    lbl_steps,
    value=st.session_state.form_steps,
    height=105,
    placeholder=ph_steps
)

diagnose_btn = st.button(
    f"🔍 Diagnose Reasoning & Generate Dual Maps ({output_lang_name})",
    type="primary",
    use_container_width=True
)

st.markdown("</div>", unsafe_allow_html=True)

if diagnose_btn:
    if not doubt_input.strip() or not steps_input.strip():
        st.error("Please provide both the problem statement and your attempted step-by-step reasoning so we can diagnose your mental path!")
    else:
        with st.spinner(f"Analyzing mental model, detecting cognitive derailment point in {output_lang_name}..."):
            st.session_state.form_doubt = doubt_input
            st.session_state.form_concept = concept_input
            st.session_state.form_steps = steps_input
            st.session_state.form_breakdown = breakdown_input

            pedagogical_context = learner_model.build_pedagogical_context(profile)

            diagnosis = pedagogy_engine.diagnose_doubt_semantic(
                doubt=doubt_input,
                student_concept=concept_input,
                student_steps=steps_input,
                student_breakdown=breakdown_input,
                learner_context=pedagogical_context,
                preferred_language=lang_code,
                student_name=profile.get("student_name", "Learner"),
                output_lang_name=output_lang_name
            )

            # Record identified misconception into longitudinal learner model
            learner_model.record_misconception(
                profile=profile,
                concept=diagnosis["canonical_concept"],
                misconception_type=diagnosis["canonical_root_misconception"],
                severity=diagnosis["severity"],
                details=diagnosis["derailment_reason"],
                problem_topic=concept_input or diagnosis["canonical_concept"]
            )
            learner_model.save_profile(profile)
            st.session_state.current_profile = profile

            # Synthesize Sarvam AI TTS speech (synchronized with Bhasha Guru Blackboard)
            with st.spinner(f"Synthesizing speech via Sarvam AI ({output_lang_name}, speaker: {speaker})..."):
                spoken_script = (
                    diagnosis.get("board_storyboard", {}).get("full_spoken_transcript")
                    or diagnosis["narration_script"]
                )
                audio_bytes, audio_msg, is_real = sarvam_tts.synthesize_speech_sarvam(
                    text=spoken_script,
                    target_language_code=lang_code,
                    speaker=speaker,
                    model=tts_model,
                    api_key=sarvam_key
                )
                st.session_state.audio_bytes = audio_bytes
                st.session_state.audio_status_msg = audio_msg

            st.session_state.diagnosis_result = diagnosis
            st.session_state.socratic_response_msg = None
            st.session_state.socratic_solved = False
            st.rerun()


# ---------------------------------------------------------
# STAGE 2: Diagnosis & Comparative Thought Map Visualizer
# ---------------------------------------------------------
if st.session_state.diagnosis_result:
    diag = st.session_state.diagnosis_result

    st.markdown(
        f"""
        <div class="saas-card">
            <div class="saas-card-header">
                <div class="saas-card-title">
                    <span>🗺️ Stage 2: Mental Model Diagnosis & Comparative Flow Maps</span>
                </div>
                <span class="step-badge">Stage 02 • Visual Remediation ({output_lang_name})</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    # Diagnostic Summary Bento Box
    col_d1, col_d2 = st.columns([3, 2])
    with col_d1:
        st.markdown(
            f"""
            <div class="derailment-banner">
                <div class="derailment-title">
                    <span>⚠️ Cognitive Derailment Point: Step {diag.get('derailment_step', 2)}</span>
                </div>
                <div class="derailment-concept">
                    Root Misconception: {diag.get('canonical_root_misconception')}
                </div>
                <div class="derailment-desc">
                    {diag.get('derailment_reason')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_d2:
        past_errors = profile.get("error_history", [])
        same_concept_errors = [e for e in past_errors[:-1] if e.get("concept") == diag.get("canonical_concept")]
        if same_concept_errors:
            prior_detail = same_concept_errors[-1].get("details", "")
            st.markdown(
                f"""
                <div class="longitudinal-banner">
                    <div style="font-weight:700; display:flex; align-items:center; gap:0.4rem; margin-bottom:0.35rem;">
                        <span>🧠 Longitudinal Memory Cross-Reference:</span>
                    </div>
                    <div>
                        "Notice how in your previous session on '{same_concept_errors[-1].get('problem_topic', 'this topic')}', you also encountered: {prior_detail[:110]}."
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="remediation-banner">
                    <div style="font-weight:700; color:#065f46; font-size:1.05rem; display:flex; align-items:center; gap:0.4rem;">
                        <span>💡 Canonical Scaffolded Concept</span>
                    </div>
                    <div style="font-weight:600; color:#047857; margin-top:0.35rem; font-size:0.95rem;">
                        {diag.get('canonical_concept')}
                    </div>
                    <div style="color:#064e3b; margin-top:0.35rem; font-size:0.9rem; line-height:1.45;">
                        The breakthrough requires pivoting from superficial heuristics to foundational principles and constraints.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Segmented Tabbed Visualization
    map_tabs = st.tabs([
        "🧑‍🏫 Live Classroom Blackboard",
        "📊 Comparative View",
        "🔴 Student Path (Map A)",
        "🟢 Remediated Path (Map B)"
    ])

    with map_tabs[0]:
        storyboard = diag.get("board_storyboard")
        if not storyboard:
            # Generate storyboard instantaneously (0.03ms) so there is zero delay
            storyboard = pedagogy_engine.generate_live_board_storyboard(
                diag,
                doubt=st.session_state.get("form_doubt", ""),
                student_concept=st.session_state.get("form_concept", ""),
                student_steps=st.session_state.get("form_steps", ""),
                output_lang_name=output_lang_name
            )
            diag["board_storyboard"] = storyboard

        blackboard_component.render_live_blackboard(
            storyboard=storyboard,
            audio_bytes=st.session_state.audio_bytes
        )

    with map_tabs[1]:
        try:
            st.graphviz_chart(diag["dot_comparative"], use_container_width=True)
        except Exception as e:
            st.error(f"Graphviz render error: {str(e)}")

    with map_tabs[2]:
        col_ga, col_ta = st.columns([3, 2])
        with col_ga:
            st.graphviz_chart(diag["dot_map_a"], use_container_width=True)
        with col_ta:
            st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#475569; margin-bottom:0.5rem;'>Student Reasoning Path:</div>", unsafe_allow_html=True)
            for n in diag.get("student_nodes", []):
                badge_html = "<span class='badge-pill badge-coral'>Derailment</span>" if n.get("is_error") else "<span class='badge-pill badge-blue'>Premise</span>"
                detail_html = f"<div class='node-card-detail'>↳ {n['detail']}</div>" if n.get("detail") else ""
                st.markdown(
                    f"""
                    <div class="node-card">
                        <div class="node-card-header">
                            <span>Node {n.get('id')}: {n.get('label')}</span>
                            {badge_html}
                        </div>
                        {detail_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with map_tabs[3]:
        col_gb, col_tb = st.columns([3, 2])
        with col_gb:
            st.graphviz_chart(diag["dot_map_b"], use_container_width=True)
        with col_tb:
            st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#475569; margin-bottom:0.5rem;'>Canonical Scaffold Steps:</div>", unsafe_allow_html=True)
            for n in diag.get("remediation_nodes", []):
                badge_html = "<span class='badge-pill badge-green'>Critical Pivot</span>" if n.get("is_pivot") else "<span class='badge-pill badge-blue'>Canonical</span>"
                detail_html = f"<div class='node-card-detail'>★ {n['detail']}</div>" if n.get("detail") else ""
                st.markdown(
                    f"""
                    <div class="node-card">
                        <div class="node-card-header">
                            <span>Step {n.get('id')}: {n.get('label')}</span>
                            {badge_html}
                        </div>
                        {detail_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("</div>", unsafe_allow_html=True)


    # ---------------------------------------------------------
    # STAGE 3: Sarvam AI Multilingual Audio & Socratic Guidance
    # ---------------------------------------------------------
    st.markdown(
        f"""
        <div class="saas-card">
            <div class="saas-card-header">
                <div class="saas-card-title">
                    <span>🎙️ Stage 3: Voice Walkthrough & Socratic Checkpoint</span>
                </div>
                <span class="step-badge">Stage 03 • Remediation ({output_lang_name})</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    audio_col1, audio_col2 = st.columns([2, 3])
    with audio_col1:
        st.markdown(
            f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                <span style="font-weight:700; font-size:0.95rem; color:#0f172a;">🔊 Audio Walkthrough</span>
                <span class="badge-pill badge-green">Speaker: {speaker.capitalize()}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.session_state.audio_bytes:
            st.audio(st.session_state.audio_bytes, format="audio/wav")
            if st.session_state.audio_status_msg:
                st.caption(st.session_state.audio_status_msg)
        else:
            st.info("Audio generation in progress or unavailable.")

        if st.button("🔄 Re-synthesize Audio", use_container_width=True):
            with st.spinner("Regenerating Sarvam TTS audio..."):
                spoken_script = (
                    diag.get("board_storyboard", {}).get("full_spoken_transcript")
                    or diag["narration_script"]
                )
                audio_bytes, audio_msg, is_real = sarvam_tts.synthesize_speech_sarvam(
                    text=spoken_script,
                    target_language_code=lang_code,
                    speaker=speaker,
                    model=tts_model,
                    api_key=sarvam_key
                )
                st.session_state.audio_bytes = audio_bytes
                st.session_state.audio_status_msg = audio_msg
                st.rerun()

    with audio_col2:
        st.markdown(
            """
            <div style="font-weight:700; font-size:0.95rem; color:#0f172a; margin-bottom:0.3rem;">
                📜 Spoken Classroom Script (Bhasha Guru):
            </div>
            """,
            unsafe_allow_html=True
        )
        display_script = (
            diag.get("board_storyboard", {}).get("full_spoken_transcript")
            or diag.get("narration_script", "")
        )
        st.markdown(
            f"""
            <div class="narration-quote">
                🗣️ "{display_script}"
            </div>
            """,
            unsafe_allow_html=True
        )

    # Socratic Checkpoint & Active Self-Correction
    st.markdown(
        f"""
        <div class="socratic-challenge-box">
            <div style="display:flex; align-items:center; justify-content:space-between;">
                <div style="font-weight:700; color:#065f46; font-size:1.08rem; display:flex; align-items:center; gap:0.4rem;">
                    <span>🎯 Socratic Self-Correction Challenge: Resolve Node {diag.get('derailment_step', 2)}</span>
                </div>
                <span class="badge-pill badge-green">Active Retrieval</span>
            </div>
            <div class="socratic-prompt-text">
                {diag.get('socratic_prompt')}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    is_output_pure_hindi = ("Hindi" in output_lang_name or "हिंदी" in output_lang_name) and ("Hinglish" not in output_lang_name and "हिंग्लिश" not in output_lang_name)
    is_output_hinglish = ("Hinglish" in output_lang_name or "हिंग्लिश" in output_lang_name)

    if is_output_pure_hindi:
        lbl_turn = "##### ✍️ आपका स्व-सुधार प्रयास (हिंदी):"
        lbl_socratic_reply = "हरे पिवट नोड पर विचार करें और बताएं कि आप अपने तर्क को कैसे सुधारेंगे:"
        ph_socratic_reply = "उदा. पिवट नोड के अनुसार, मेरी प्रारंभिक पूर्वधारणा सीमांत शर्तों को पूरा नहीं करती थी क्योंकि..."
        btn_socratic_reply = "🚀 समाधान सबमिट करें (हिंदी)"
    elif is_output_hinglish:
        lbl_turn = "##### ✍️ Your Self-Correction Turn (हिंग्लिश):"
        lbl_socratic_reply = "Green Pivot Node par reflect karein aur explain karein ki aap logic kaise correct karenge:"
        ph_socratic_reply = "e.g. Pivot node ke according, meri initial assumption governing conditions ko satisfy nahi kar rahi thi kyunki..."
        btn_socratic_reply = "🚀 Submit Socratic Correction (हिंग्लिश)"
    else:
        lbl_turn = "##### ✍️ Your Self-Correction Turn:"
        lbl_socratic_reply = "Reflect on the green Pivot Node and explain how you would correct your logic:"
        ph_socratic_reply = "e.g. Based on the pivot node, my initial assumption overlooked the core constraint because..."
        btn_socratic_reply = "🚀 Submit Socratic Correction"

    st.markdown(lbl_turn)
    socratic_reply = st.text_area(
        lbl_socratic_reply,
        height=90,
        placeholder=ph_socratic_reply,
        key="socratic_student_reply"
    )

    col_sub, col_skip = st.columns([2, 4])
    with col_sub:
        submit_socratic = st.button(btn_socratic_reply, type="primary", use_container_width=True)

    if submit_socratic:
        if not socratic_reply.strip():
            st.warning("Please articulate your corrected reasoning before submitting.")
        else:
            is_resolved, feedback_text, badge_level = pedagogy_engine.evaluate_student_socratic_reply(
                socratic_reply, diag
            )
            st.session_state.socratic_response_msg = feedback_text
            st.session_state.socratic_solved = is_resolved

            if is_resolved:
                learner_model.resolve_misconception(profile, diag.get("canonical_concept", ""))
                learner_model.save_profile(profile)
                st.session_state.current_profile = profile
                st.balloons()
            st.rerun()

    if st.session_state.socratic_response_msg:
        if st.session_state.socratic_solved:
            st.success(st.session_state.socratic_response_msg)
            st.markdown(
                f"<span class='badge-pill badge-green'>🎉 Longitudinal Mastery Updated: '{diag.get('canonical_concept')}' upgraded!</span>",
                unsafe_allow_html=True
            )
        else:
            st.warning(st.session_state.socratic_response_msg)

    st.markdown("</div>", unsafe_allow_html=True)
