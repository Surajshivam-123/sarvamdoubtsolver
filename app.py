"""
Bhasha Doubt Solver (भाषा डाउट सॉल्वर)
A pedagogical Streamlit web application that:
1. Enforces active student retrieval (No direct solutions)
2. Pinpoints root conceptual misconceptions via diagnostic evaluation
3. Persists a longitudinal learner profile across questions
4. Renders thought processes as interactive Graphviz comparative concept/flow maps
   - Map A: Student's Actual Path (Coral/Red error nodes)
   - Map B: Remediated Conceptual Path (Emerald Green pivot nodes)
5. Delivers multilingual auditory narration using Sarvam AI Text-to-Speech (TTS)
   - Supports 10 Indian languages with native bulbul:v3 speakers
   - Natural classroom Hinglish STEM terminology preservation
   - Streamlit Cloud & local zero-friction deployment
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
from sample_doubts import SAMPLE_DOUBTS

# ---------------------------------------------------------
# Page Configuration & Modern Theme Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Universal Bhasha Doubt Solver (Hinglish/Hybrid)",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main-title-container {
        padding: 1.5rem 1.8rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #064e3b 100%);
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.025em;
        background: linear-gradient(to right, #ffffff, #a7f3d0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .main-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        margin-top: 0.4rem;
        font-weight: 400;
    }

    .badge-pill {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 9999px;
        margin-right: 0.4rem;
        margin-top: 0.4rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-green { background-color: #d1fae5; color: #065f46; border: 1px solid #10b981; }
    .badge-amber { background-color: #fef3c7; color: #92400e; border: 1px solid #f59e0b; }
    .badge-coral { background-color: #fee2e2; color: #991b1b; border: 1px solid #ef4444; }
    .badge-blue  { background-color: #dbeafe; color: #1e40af; border: 1px solid #3b82f6; }
    .badge-purple{ background-color: #f3e8ff; color: #6b21a8; border: 1px solid #a855f7; }

    .step-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }

    .misconception-callout {
        border-left: 5px solid #ef4444;
        background: #fff1f2;
        padding: 1rem 1.25rem;
        border-radius: 0 10px 10px 0;
        margin: 1rem 0;
    }

    .remediation-callout {
        border-left: 5px solid #10b981;
        background: #f0fdf4;
        padding: 1rem 1.25rem;
        border-radius: 0 10px 10px 0;
        margin: 1rem 0;
    }

    .longitudinal-callout {
        border-left: 5px solid #f59e0b;
        background: #fffbeb;
        padding: 0.85rem 1.15rem;
        border-radius: 0 10px 10px 0;
        margin: 0.75rem 0;
        font-size: 0.92rem;
    }

    .socratic-box {
        border: 2px dashed #059669;
        background: #ecfdf5;
        border-radius: 12px;
        padding: 1.25rem;
        margin-top: 1rem;
    }

    .stGraphvizChart {
        display: flex;
        justify-content: center;
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #e2e8f0;
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
# Sidebar: Identity, Profile, Settings & Mastery Graph
# ---------------------------------------------------------
with st.sidebar:
    st.title("🌐 Language Matrix")
    st.caption("Pedagogical Hybrid / Hinglish Support")

    input_lang_name = st.selectbox(
        "Input Language (Student types):",
        options=list(sarvam_tts.LANGUAGE_REGISTRY.keys()),
        index=0,
    )

    output_lang_name = st.selectbox(
        "Output Language (Thought Maps & Voice):",
        options=list(sarvam_tts.LANGUAGE_REGISTRY.keys()),
        index=1,  # Default to Hindi (Hinglish)
    )
    target_cfg = sarvam_tts.LANGUAGE_REGISTRY[output_lang_name]
    lang_code = target_cfg["code"]
    default_speaker = target_cfg["speaker"]

    st.divider()

    st.subheader("🔑 Sarvam AI API")
    detected_key = sarvam_tts.get_configured_api_key()
    sarvam_key = st.text_input(
        "API Subscription Key",
        value=detected_key,
        type="password",
        placeholder="Enter your api-subscription-key",
        help="Loaded automatically from st.secrets or .env. Used for translation and speech dictation."
    )

    speaker = st.selectbox(
        "Speaker Voice:",
        options=[default_speaker, "ritu", "aditya", "priya", "simran", "soham", "gokul", "kavitha", "pooja", "chaitra", "anand"],
        index=0
    )

    tts_model = st.selectbox("TTS Model:", options=sarvam_tts.MODEL_OPTIONS, index=0)

    if sarvam_key:
        st.markdown("<span class='badge-pill badge-green'>✓ Sarvam API Key Active</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='badge-pill badge-amber'>ℹ Acoustic Preview Mode Active</span>", unsafe_allow_html=True)

    if "Hindi" in output_lang_name:
        st.info("💡 **Hinglish Mode Active:** Scientific terms (Friction, Energy, Conservation, FBD) are kept in natural conversational English for pedagogical clarity.")

    st.divider()

    # Longitudinal Learner Identity & Profile
    st.subheader("🎓 Longitudinal Profile")
    profiles_list = learner_model.list_available_profiles()
    profile_options = {p["student_id"]: f"{p['student_name']} ({p['student_id']})" for p in profiles_list}
    
    current_idx = list(profile_options.keys()).index(st.session_state.selected_student_id) if st.session_state.selected_student_id in profile_options else 0
    selected_id = st.selectbox(
        "Active Learner:",
        options=list(profile_options.keys()),
        index=current_idx,
        format_func=lambda x: profile_options.get(x, x),
        help="Select a student to load their persistent longitudinal misconception history."
    )

    if selected_id != st.session_state.selected_student_id:
        st.session_state.selected_student_id = selected_id
        st.session_state.current_profile = learner_model.load_profile(selected_id)
        st.session_state.diagnosis_result = None
        st.session_state.audio_bytes = None
        st.session_state.socratic_response_msg = None
        st.session_state.socratic_solved = False
        st.rerun()

    profile = st.session_state.current_profile

    # Longitudinal Profile Actions (Reset / Export / Import)
    col_reset, col_exp = st.columns(2)
    with col_reset:
        if st.button("🔄 Reset Profile", use_container_width=True):
            st.session_state.current_profile = learner_model.reset_profile(st.session_state.selected_student_id)
            st.session_state.diagnosis_result = None
            st.session_state.audio_bytes = None
            st.toast("Profile reset to clean baseline!", icon="🔄")
            st.rerun()
    with col_exp:
        export_str = learner_model.export_profile_json(profile)
        st.download_button(
            "📥 Export JSON",
            data=export_str,
            file_name=f"learner_profile_{profile.get('student_id')}.json",
            mime="application/json",
            use_container_width=True
        )

    # Import JSON uploader
    with st.expander("📤 Import Profile JSON"):
        uploaded_profile = st.file_uploader("Upload student profile JSON", type=["json"], key="profile_uploader")
        if uploaded_profile is not None:
            try:
                content = uploaded_profile.read().decode("utf-8")
                imported = learner_model.import_profile_json(content)
                st.session_state.selected_student_id = imported["student_id"]
                st.session_state.current_profile = imported
                st.success(f"Loaded profile: {imported.get('student_name')}")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to import: {str(e)}")

    st.divider()

    # Persistent Knowledge Graph / Mastery Dashboard
    st.subheader("📊 Mastery Dashboard")
    mastery = profile.get("mastery_map", {})
    
    solid_count = sum(1 for s in mastery.values() if s == "solid")
    fragile_count = sum(1 for s in mastery.values() if s == "fragile")
    prone_count = sum(1 for s in mastery.values() if s == "misconception_prone")

    m_c1, m_c2, m_c3 = st.columns(3)
    m_c1.metric("Solid", solid_count)
    m_c2.metric("Fragile", fragile_count)
    m_c3.metric("Prone", prone_count)

    for concept_name, status in mastery.items():
        if status == "solid":
            st.markdown(f"🟢 **{concept_name}** `Solid`")
        elif status == "fragile":
            st.markdown(f"🟡 **{concept_name}** `Fragile`")
        else:
            st.markdown(f"🔴 **{concept_name}** `Misconception-Prone`")

    with st.expander("📜 Historical Error Log & Trajectory"):
        st.markdown(f"**Longitudinal Trajectory:**\n*{profile.get('pedagogical_trajectory', 'Baseline') }*")
        st.markdown("---")
        errors = profile.get("error_history", [])
        if not errors:
            st.caption("No misconceptions logged yet.")
        else:
            for idx, err in enumerate(reversed(errors[-6:])):
                badge_cls = "badge-coral" if err.get("severity") == "High" else "badge-amber"
                status_icon = "✅ Resolved" if err.get("resolved") else "⚠️ Active"
                st.markdown(
                    f"<span class='badge-pill {badge_cls}'>{err.get('severity', 'Med')}</span> "
                    f"**{err.get('concept')}** ({status_icon})<br>"
                    f"<small><i>{err.get('type')}</i> — {err.get('details', '')[:80]}</small>",
                    unsafe_allow_html=True
                )

    with st.expander("🔍 Injected Pedagogical Context"):
        st.caption("This context string is injected into every diagnostic turn:")
        st.code(learner_model.build_pedagogical_context(profile), language="markdown")


# ---------------------------------------------------------
# Main Application Content
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="main-title-container">
        <div class="main-title">Universal Bhasha Doubt Solver <span style="font-size:1.4rem; font-weight:500;">(भाषा डाउट सॉल्वर)</span></div>
        <div class="main-subtitle">Input in <b>{input_lang_name}</b> ➡️ Natural Pedagogical Remediation & Audio in <b>{output_lang_name}</b></div>
        <div style="margin-top: 0.8rem;">
            <span class="badge-pill badge-green">Pedagogical Guardrails (No Direct Answers)</span>
            <span class="badge-pill badge-blue">Longitudinal Learner Profile</span>
            <span class="badge-pill badge-coral">Dual Thought Maps (Graphviz)</span>
            <span class="badge-pill badge-purple">Sarvam AI Indian Language TTS</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# 1-Click Instant Demos (With Natural Hinglish Terminology)
# ---------------------------------------------------------
st.markdown("#### ⚡ 1-Click Demos (With Natural Hinglish Terminology):")
demo_cols = st.columns(4)

def load_sample(key: str):
    s = SAMPLE_DOUBTS[key]
    st.session_state.form_doubt = s["problem_statement"]
    st.session_state.form_concept = s["student_concept"]
    st.session_state.form_steps = s["student_steps"]
    st.session_state.form_breakdown = s["student_breakdown"]
    st.session_state.diagnosis_result = None
    st.session_state.audio_bytes = None
    st.session_state.socratic_response_msg = None
    st.session_state.socratic_solved = False

with demo_cols[0]:
    if st.button("🏔️ Spring & Friction", use_container_width=True):
        load_sample("spring_friction_energy")
        st.rerun()

with demo_cols[1]:
    if st.button("🐎 Newton's 3rd Law", use_container_width=True):
        load_sample("newton_third_law_horse_cart")
        st.rerun()

with demo_cols[2]:
    if st.button("🏎️ Circular Turn", use_container_width=True):
        load_sample("circular_motion_turn")
        st.rerun()

with demo_cols[3]:
    if st.button("⛸️ Skater Spin", use_container_width=True):
        load_sample("rotational_skater_spin")
        st.rerun()


# ---------------------------------------------------------
# STAGE 1: Socratic Elicitation (No Direct Answers Guardrail)
# ---------------------------------------------------------
st.markdown(f"### 📝 Stage 1: Problem Articulation & Mental Model ({input_lang_name})")
st.markdown(
    "> 🛡️ **Pedagogical Guardrail:** The system enforces active cognitive retrieval. "
    "To diagnose the exact derailment point, articulate your current understanding rather than seeking formula plugs."
)

with st.container():
    doubt_input = st.text_area(
        f"1. Problem Statement or Question Doubt ({input_lang_name}):",
        value=st.session_state.form_doubt,
        height=85,
        placeholder="Enter the STEM question or doubt here..."
    )

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        concept_input = st.text_input(
            f"2. What concept / law do you believe applies? ({input_lang_name})",
            value=st.session_state.form_concept,
            placeholder="e.g. Conservation of Mechanical Energy, Action-Reaction, Centripetal Force"
        )
    with col_e2:
        breakdown_input = st.text_input(
            f"4. Where do you feel your reasoning breaks down or gets stuck? ({input_lang_name})",
            value=st.session_state.form_breakdown,
            placeholder="e.g. The compression is too large, or forces cancel out..."
        )

    steps_input = st.text_area(
        f"3. Your Step-by-Step Logic / Attempted Derivation So Far ({input_lang_name}):",
        value=st.session_state.form_steps,
        height=110,
        placeholder="Step 1: ...\nStep 2: ...\nStep 3: ..."
    )

    diagnose_btn = st.button(f"🔍 Diagnose Reasoning in {output_lang_name}", type="primary", use_container_width=True)

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
                student_name=profile.get("student_name", "Learner")
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

            # Synthesize Sarvam AI TTS speech
            with st.spinner(f"Synthesizing speech via Sarvam AI ({output_lang_name}, speaker: {speaker})..."):
                audio_bytes, audio_msg, is_real = sarvam_tts.synthesize_speech_sarvam(
                    text=diagnosis["narration_script"],
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

    st.divider()
    st.markdown(f"### 🗺️ Stage 2: Mental Model Diagnosis & Dual Thought Maps ({output_lang_name})")

    # Diagnostic Summary Box
    col_d1, col_d2 = st.columns([3, 2])
    with col_d1:
        st.markdown(
            f"""
            <div class="misconception-callout">
                <div style="font-weight:700; color:#991b1b; font-size:1.15rem;">
                    ⚠️ Identified Cognitive Derailment Point: Step {diag.get('derailment_step', 2)}
                </div>
                <div style="margin-top:0.4rem; color:#7f1d1d; font-weight:600;">
                    Root Misconception: {diag.get('canonical_root_misconception')}
                </div>
                <div style="margin-top:0.35rem; color:#450a0a; font-size:0.95rem;">
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
                <div class="longitudinal-callout">
                    <b>🧠 Longitudinal Learner Memory Cross-Reference:</b><br>
                    <i>"Notice how in your previous session on '{same_concept_errors[-1].get('problem_topic', 'this topic')}', you also encountered friction: {prior_detail[:100]}."</i>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="remediation-callout">
                    <div style="font-weight:700; color:#065f46; font-size:1.05rem;">
                        💡 Canonical Scaffolded Concept: {diag.get('canonical_concept')}
                    </div>
                    <div style="margin-top:0.3rem; color:#064e3b; font-size:0.92rem;">
                        The breakthrough requires pivoting from formula plugging to first-principles constraint checking.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Interactive Graphviz Visualization Tabs
    map_tabs = st.tabs([
        "📊 Dual Comparative Thought Map",
        "🔴 Map A: Student's Actual Path",
        "🟢 Map B: Remediated Conceptual Path",
        "💻 Graphviz DOT Code"
    ])

    with map_tabs[0]:
        st.caption("Visualizing the student's derailed reasoning flow (left, Coral) alongside the canonical scaffolded pathway (right, Emerald Green) with the Pedagogy Pivot bridge.")
        try:
            st.graphviz_chart(diag["dot_comparative"], use_container_width=True)
        except Exception as e:
            st.error(f"Graphviz render error: {str(e)}")

    with map_tabs[1]:
        st.caption("Map A: Your submitted logic steps. Erroneous branches are highlighted in Coral/Red, while valid premises remain in Muted Slate.")
        col_ga, col_ta = st.columns([3, 2])
        with col_ga:
            st.graphviz_chart(diag["dot_map_a"], use_container_width=True)
        with col_ta:
            st.markdown("#### Node Breakdown (Student Path):")
            for n in diag.get("student_nodes", []):
                icon = "❌" if n.get("is_error") else "✔️"
                badge = "<span class='badge-pill badge-coral'>Derailment</span>" if n.get("is_error") else "<span class='badge-pill badge-blue'>Premise</span>"
                st.markdown(f"{icon} **Node {n.get('id')}:** {n.get('label')} {badge}", unsafe_allow_html=True)
                if n.get("detail"):
                    st.caption(f"↳ *{n['detail']}*")

    with map_tabs[2]:
        st.caption("Map B: Scaffolded canonical reasoning journey. The Critical Pivot Node where the conceptual breakthrough occurs is highlighted in bold Emerald Green.")
        col_gb, col_tb = st.columns([3, 2])
        with col_gb:
            st.graphviz_chart(diag["dot_map_b"], use_container_width=True)
        with col_tb:
            st.markdown("#### Canonical Scaffold Steps:")
            for n in diag.get("remediation_nodes", []):
                icon = "💡" if n.get("is_pivot") else "➡️"
                badge = "<span class='badge-pill badge-green'>Critical Pivot</span>" if n.get("is_pivot") else "<span class='badge-pill badge-blue'>Canonical</span>"
                st.markdown(f"{icon} **Step {n.get('id')}:** {n.get('label')} {badge}", unsafe_allow_html=True)
                if n.get("detail"):
                    st.caption(f"↳ *{n['detail']}*")

    with map_tabs[3]:
        st.caption("Raw Graphviz DOT strings generated dynamically for the thought maps:")
        st.code(diag["dot_comparative"], language="dot")


    # ---------------------------------------------------------
    # STAGE 3: Sarvam AI Multilingual Audio & Socratic Guidance
    # ---------------------------------------------------------
    st.divider()
    st.markdown(f"### 🎙️ Stage 3: Sarvam AI Voice Dictation & Socratic Checkpoint ({output_lang_name})")

    audio_col1, audio_col2 = st.columns([2, 3])
    with audio_col1:
        st.markdown(f"#### 🔊 Audio Walkthrough ({output_lang_name}):")
        if st.session_state.audio_bytes:
            st.audio(st.session_state.audio_bytes, format="audio/wav")
            if st.session_state.audio_status_msg:
                st.caption(st.session_state.audio_status_msg)
        else:
            st.info("Audio generation in progress or unavailable.")

        if st.button("🔄 Re-synthesize Audio", use_container_width=True):
            with st.spinner("Regenerating Sarvam TTS audio..."):
                audio_bytes, audio_msg, is_real = sarvam_tts.synthesize_speech_sarvam(
                    text=diag["narration_script"],
                    target_language_code=lang_code,
                    speaker=speaker,
                    model=tts_model,
                    api_key=sarvam_key
                )
                st.session_state.audio_bytes = audio_bytes
                st.session_state.audio_status_msg = audio_msg
                st.rerun()

    with audio_col2:
        st.markdown(f"#### 📜 Spoken Narration Script ({output_lang_name}):")
        st.info(f"🗣️ **Script:**\n\n\"{diag.get('narration_script')}\"")

    # Socratic Checkpoint & Active Self-Correction
    st.markdown(
        f"""
        <div class="socratic-box">
            <div style="font-weight:700; color:#065f46; font-size:1.1rem; margin-bottom:0.5rem;">
                🎯 Socratic Checkpoint: Self-Correct Node {diag.get('derailment_step', 2)}
            </div>
            <div style="font-size:1.02rem; color:#044e39; line-height:1.5;">
                {diag.get('socratic_prompt')}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("##### ✍️ Your Self-Correction Turn:")
    socratic_reply = st.text_area(
        "Reflect on the green Pivot Node and explain how you would correct your logic:",
        height=85,
        placeholder="e.g. In step 2, mechanical energy is not conserved because friction does negative work, so W_friction must be subtracted before equating to spring energy...",
        key="socratic_student_reply"
    )

    col_sub, col_skip = st.columns([2, 4])
    with col_sub:
        submit_socratic = st.button("🚀 Submit Socratic Correction", type="primary", use_container_width=True)

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
                f"<span class='badge-pill badge-green'>🎉 Mastery Updated: '{diag.get('canonical_concept')}' upgraded!</span>",
                unsafe_allow_html=True
            )
        else:
            st.warning(st.session_state.socratic_response_msg)
