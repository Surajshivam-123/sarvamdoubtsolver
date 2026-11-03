# 💡 Sansay (संशय) - AI Socratic Academic Doubt Solver

> **Pure Client-Side React SPA with Direct Sarvam AI Indian Voice Engine**
> **No Python Backend Server Needed • Zero-Latency Cognitive Derailment Diagnostics**

Sansay (संशय) is a standalone, browser-based pedagogical application designed for students tackling conceptual doubts across STEM, Law, Economics, World History, Literature, and Computer Science. It enforces **active cognitive retrieval**, detects the exact node where a student's intuition derailed, maintains a **longitudinal learner profile** in browser storage, renders dynamic **thought process maps** on an interactive digital blackboard, and delivers node-anchored auditory walkthroughs directly via **Sarvam AI's REST Text-to-Speech (TTS)** engine.

---

## 🌟 Key Architecture & Highlights

### 1. 100% Pure Client-Side Architecture (No Python Server Required)
- **Zero Backend Dependencies:** Everything runs in the browser via React 18, TypeScript, and Vite.
- **Direct Sarvam AI API Integration:** Connects directly from the browser to Sarvam AI (`https://api.sarvam.ai/text-to-speech`) for Indian regional language voice synthesis.
- **Harmonic Acoustic Fallback:** Synthesizes harmonic chord audio in JavaScript so the blackboard player remains 100% interactive even without an API key or offline.
- **Local Storage Longitudinal Learner Profiles:** Tracks misconceptions, concept mastery maps (🟢 Solid, 🟡 Fragile, 🔴 Misconception-Prone), and error histories persistent in browser `localStorage`.
- **Import / Export JSON:** Easily back up and restore learner profiles directly from the UI.

### 2. Multilingual Flexibility
- **Any Language as Input:** Students can enter their doubts, attempted steps, and stuck points in **any language** (English, Hindi, Hinglish, Marathi, Bengali, Tamil, Telugu, Kannada, Gujarati, etc.).
- **Interactive Output Language Selector:** Select output voice dictation and remediation directly from the Header:
  - English
  - Hindi (हिंदी)
  - Hinglish (हिंग्लिश)
  - Bengali (বাংলা)
  - Marathi (मराठी)
  - Tamil (தமிழ்)
  - Telugu (తెలుగు)
  - Gujarati (ગુજરાતી)
  - Kannada (ಕನ್ನಡ)
  - Malayalam (മലയാളം)
  - Punjabi (ਪੰਜਾਬੀ)

### 3. Socratic Cognitive Derailment & Interactive Blackboard Studio
- **Autonomous AI Concept Diagnosis:** Students do not need to guess or enter the core law/principle. The AI analyzes the problem statement and derivation steps to autonomously determine the governing law.
- **1-Click Demo Samples:** Select any benchmark case study (Law, Economics, History, Literature, Coding, Physics, or Custom) to pre-fill all input fields instantly via Raycast-style command popover.
- **Collapsible Sidebar Layout:** Collapse or expand the left reasoning console with a single click to grant the diagnostic graph full-screen canvas focus.
- **Linear/Raycast Dark Canvas Aesthetics:**
  - Cohesive neutral dark base (`#090D16`) with softened dot grid (`rgba(255, 255, 255, 0.04)`).
  - Ambient rim lights on nodes based on semantic state:
    - 🟢 Sound Premise (`glow-emerald`)
    - 🟡 Critical Pivot (`glow-amber`)
    - 🔴 Cognitive Derailment (`glow-crimson`)
    - 🟣 Socratic Checkpoint (`glow-violet`)
  - Directional animated dash strokes on divergence connectors (`animate-dash-travel`).
  - Docked glassmorphism controls bar with play/pause, timecode scrubber, frequency wave visualizer, and speed controls.
  - Docked frosted-glass live transcript card with waveform avatar indicator and collapsible drawer.
- **Socratic Self-Correction Challenge:**
  - Resolves cognitive derailment at the critical pivot step.
  - Celebratory confetti effects upon successful retrieval (`canvas-confetti`).

---

## 🚀 Quick Start

### 1. Prerequisites
- Node.js 18+ & npm

### 2. Launch the Application
Run the startup script:
```bash
./start.sh
```
Or with npm:
```bash
npm start
# or for hot-reloading development:
npm run dev
```

Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

## 📂 Project Structure

```
sarvam/
├── start.sh                 # Single-command launcher
├── package.json             # Root runner scripts
├── README.md                # Documentation & architecture guide
└── frontend/                # Standalone React Application
    ├── package.json         # React & UI dependencies
    ├── vite.config.ts       # Vite build configuration
    ├── tailwind.config.js   # Tailwind CSS styling tokens
    └── src/
        ├── components/      # BlackboardStudio, ReasoningConsole, SocraticSection, Header, Modals
        ├── data/            # Curated demo case studies & seeded learner profiles
        ├── services/
        │   ├── pedagogyEngine.ts  # Client-side cognitive diagnosis & graph layout
        │   ├── sarvamApi.ts       # Direct Sarvam AI REST API client & audio synth
        │   ├── learnerModel.ts    # localStorage profile persistence & mastery tracking
        │   └── api.ts             # Unified client-side service interface
        ├── types/           # TypeScript data interfaces
        ├── App.tsx          # Main React studio application
        └── main.tsx         # React DOM entrypoint
```
