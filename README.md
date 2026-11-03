sk_0vr9gnzo_1deURIBWS66KDr30XVDBOmBw
# 💡 Bhasha Doubt Solver (भाषा डाउट सॉल्वर)

> **Socratic Cognitive Remediation & Longitudinal Indian Language Audio Tutoring for STEM Education**

Bhasha Doubt Solver is a pedagogical Streamlit web application designed for Indian students tackling conceptual STEM doubts (JEE, NEET, CBSE, and Undergraduate Engineering/Science). Rather than serving as an answer dispenser, it enforces **active cognitive retrieval**, detects the precise step where a student's intuition derailed, maintains a **longitudinal learner profile** across problem-solving sessions, renders comparative Graphviz **thought process maps**, and delivers node-anchored auditory walkthroughs using **Sarvam AI's Indian language Text-to-Speech (TTS)** engine.

---

## 🌟 Key Architectural Pillars

### 1. Pedagogical Guardrails (No Direct Solutions)
- **Strict Prohibition on Answers:** The application never hands out numerical solutions, plugged formula results, or unearned answers.
- **Socratic Elicitation:** Requires the student to articulate:
  1. The problem statement or doubt.
  2. The concept/law they believe applies.
  3. Their step-by-step logic attempted so far.
  4. Where they feel their reasoning breaks down.
- **Diagnostic Derailment Detection:** Pinpoints the exact node where intuition decoupled from canonical principles (e.g. overgeneralizing $v = u + at$ to variable acceleration, ignoring frictional work in energy conservation, or treating centripetal acceleration as an independent outward force).

### 2. Persistent Longitudinal Learner Model (`st.session_state` & Local JSON)
- Tracks each learner's cumulative journey in `data/learner_profiles/<student_id>.json`.
- Maintains:
  - `mastery_map`: Tracks concepts across three states: 🟢 `solid`, 🟡 `fragile`, and 🔴 `misconception_prone`.
  - `error_history`: Chronological audit trail logging timestamp, concept, misconception type, severity, and resolution status.
  - `pedagogical_trajectory`: Dynamic narrative summary of recurring cognitive blind spots.
- **Context Injection:** In every turn, the learner's longitudinal profile is formatted and injected into the diagnostic context, allowing explanations to reference past errors:
  > *"Notice how in last week's problem on pulleys you also forgot the normal reaction force..."*
- Includes **Reset Profile**, **Export JSON**, and **Import JSON** capabilities.

### 3. Dual Comparative Thought Map Visualizer (Graphviz)
- Renders side-by-side or sequential topological reasoning graphs:
  - **Map A (Student's Actual Path):** Highlights erroneous branches in **Coral/Red** (`#EF4444`, `⚠️ DERAILMENT`) and valid premises in **Muted Slate Gray** (`#64748B`).
  - **Map B (Remediated Conceptual Path):** Maps the canonical scaffolded journey in **Emerald Green** (`#10B981`), labeling the critical **Pivot Node** (`💡 CRITICAL PIVOT`, `#047857`) where the breakthrough occurs.
  - **Comparative Dual Map:** Shows both mental models side-by-side with a cross-cutting **Pedagogy Pivot bridge** edge.

### 4. Sarvam AI Voice Dictation Engine
- Calls `POST https://api.sarvam.ai/text-to-speech` with:
  ```json
  {
    "inputs": ["Look at Node 2 in your graph: you treated acceleration as constant..."],
    "target_language_code": "hi-IN",
    "speaker": "meera",
    "model": "bulbul:v1"
  }
  ```
- **Supported Languages:** Hindi (`hi-IN`), Indian English (`en-IN`), Bengali (`bn-IN`), Marathi (`mr-IN`), Tamil (`ta-IN`), Telugu (`te-IN`), Kannada (`kn-IN`), Gujarati (`gu-IN`).
- **Speakers:** `meera`, `pavithra`, `arvind`, `amol`, `amartya`.
- **Node-Referencing Scripts:** Auditory feedback directly guides the student through the graph:
  > *"Look at Node 2 in your graph: you treated acceleration as constant. However, as shown in the green remediation map at the Pivot Node..."*
- **Acoustic Fallback:** When no Sarvam API key is supplied, a pleasant synthesized harmonic WAV stream is generated via Python's standard library so the audio player remains 100% interactive in all environments.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Virtual environment (recommended)

### 2. Setup Environment
```bash
# Clone or navigate to the directory
cd sarvam

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt # or pip install streamlit requests python-dotenv graphviz
```

### 3. Configure API Keys (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your Sarvam AI subscription key:
```env
SARVAM_API_KEY=your_key_here
```
*(You can also enter the key directly in the Streamlit sidebar UI at runtime!)*

### 4. Launch the Application
```bash
streamlit run app.py
```

---

## 🧪 Running Tests

Run the comprehensive unit test suite:
```bash
python3 -m unittest tests/test_modules.py -v
```

---

## 📂 Project Structure

```
sarvam/
├── app.py                   # Main Streamlit interface & 3-stage interactive workflow
├── learner_model.py         # Longitudinal learner model & JSON persistence
├── pedagogy_engine.py       # Diagnostic engine, Graphviz DOT generators, Socratic evaluator
├── sarvam_tts.py            # Sarvam AI REST TTS client & fallback wave synthesizer
├── sample_doubts.py         # Curated classic Indian STEM pitfalls for 1-click testing
├── .env.example             # Environment variable template
├── README.md                # Documentation & architecture guide
├── data/
│   └── learner_profiles/    # Seeded student profiles (Arjun, Priya, Rohan, Ananya, Karthik)
└── tests/
    └── test_modules.py      # Automated test suite
```
