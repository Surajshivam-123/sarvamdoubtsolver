export interface PresetDoubt {
  key: string;
  title: string;
  subject: string;
  problem_statement: string;
  problem_statement_hi?: string;
  student_concept: string;
  student_concept_hi?: string;
  student_steps: string;
  student_steps_hi?: string;
  student_breakdown: string;
  student_breakdown_hi?: string;
  canonical_concept: string;
  derailment_step: number;
}

// ---------------------------------------------------------------------------
// Digital Teacher Blackboard Derivation Schemas
// ---------------------------------------------------------------------------
export interface BoardStep {
  stepIndex: number;
  title: string;
  latexContent: string;        // e.g. "N = m \\cdot g \\cos(\\theta)"
  annotation?: string;         // e.g. "Perpendicular to incline"
  speechScript: string;        // e.g. "Ab yahan dhyan dein: normal force pure mg ke barabar nahi hogi..."
  audioUrl?: string;           // Pre-generated or streaming Sarvam Bulbul TTS audio URL
  highlightTarget?: string;    // Element ID or term to illuminate on board
  chalkColor?: 'emerald' | 'amber' | 'cyan' | 'violet' | 'white';
  durationEstimateMs: number;
}

export interface BoardSolveResponse {
  problemSummary: string;
  identifiedMisconception?: string;
  steps: BoardStep[];
  canonicalConcept: string;
  derailmentStep: number;
}

// ---------------------------------------------------------------------------
// Divergence & Reasoning Graph Engine Schemas
// ---------------------------------------------------------------------------
export type SemanticNodeType =
  | 'SOUND_PREMISE'
  | 'CRITICAL_PIVOT'
  | 'DERAILED_BRANCH'
  | 'CANONICAL_PATH'
  | 'SOCRATIC_CHECKPOINT';

export interface GraphNode {
  id: string;
  type: SemanticNodeType;
  label: string;
  mathLatex?: string;
  description: string;
  badge?: string;
  misconceptionDetails?: {
    tag: string;
    identifiedFlaw: string;
    correctionHint: string;
  };
  audioScriptIndic: string;    // Hinglish/Indic script for Sarvam Bulbul TTS
  audioUrl?: string;           // Synthesized audio clip URL
  position: { x: number; y: number };
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  status: 'valid' | 'derailed' | 'scaffold';
  animated?: boolean;
}

export interface DivergenceGraphResponse {
  problemSummary: string;
  divergenceNodeId: string;
  summarySpeechScript: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
}

// Legacy node structure for backward compatibility
export interface NodeCard {
  id: string;
  type: 'sound' | 'pivot' | 'derailed' | 'derailed_end' | 'remediation' | 'socratic';
  badge: string;
  title: string;
  detail: string;
  mathLatex?: string;
  x: number;
  y: number;
  w: number;
  h: number;
  glow_color: string;
}

export interface Connector {
  id: string;
  type: 'sound' | 'pivot' | 'derailed' | 'remediation' | 'socratic';
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  stroke: string;
  dashed?: boolean;
  stroke_width?: number;
  label?: string;
}

export interface TimelineStep {
  step_id: number;
  speech_segment: string;
  start_time: number;
  end_time: number;
  duration: number;
  board_action: string;
  color: string;
  content: string;
  target_coords?: Record<string, any>;
}

export interface GraphPayload {
  doubt_domain: string;
  identified_topic: string;
  misconception_name: string;
  canonical_concept: string;
  derailment_step: number;
  derailment_reason: string;
  socratic_challenge: string;
  full_spoken_transcript: string;
  nodes: NodeCard[];
  connectors: Connector[];
  timeline: TimelineStep[];
  total_duration: number;
}

// ---------------------------------------------------------------------------
// Longitudinal Learner Model & Error History
// ---------------------------------------------------------------------------
export interface ErrorHistoryItem {
  timestamp: string;
  problem_topic: string;
  concept: string;
  type: string;
  severity: string;
  details: string;
  resolved: boolean;
}

export interface LearnerProfile {
  student_id: string;
  student_name: string;
  preferred_language: string;
  preferred_voice: string;
  created_at: string;
  last_active: string;
  session_count: number;
  mastery_map: Record<string, 'solid' | 'fragile' | 'misconception_prone'>;
  error_history: ErrorHistoryItem[];
  pedagogical_trajectory: string;
  recurrent_misconceptions?: string[];
}

// ---------------------------------------------------------------------------
// Socratic Diagnostic Engine Output
// ---------------------------------------------------------------------------
export interface SocraticDiagnosisResult {
  identified_misconception: string;
  concept_tag: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  is_recurring: boolean;
  socratic_hint: string;
  hinglish_vernacular_hint: string;
}

export interface DiagnosisResponse {
  diagnosis: Record<string, any>;
  graph_payload: GraphPayload;
  board_solve: BoardSolveResponse;
  divergence_graph: DivergenceGraphResponse;
  socratic_result: SocraticDiagnosisResult;
  audio_base64: string;
  audio_msg: string;
  is_real_audio: boolean;
  valid_pct: number;
  derailment_step: number;
  canonical_concept: string;
  socratic_prompt: string;
  profile: LearnerProfile;
}

export interface ConfigResponse {
  languages: string[];
  language_registry: Record<string, { code: string; speaker: string; script: string; font_hint?: string }>;
  tts_models: string[];
  speakers: string[];
  default_sarvam_api_key: string;
  domains: { id: string; name: string }[];
}

export interface SocraticEvalResponse {
  is_resolved: boolean;
  feedback_text: string;
  badge_level: string;
  profile: LearnerProfile;
}
