/**
 * Pure Client-Side Service (No Python Backend Server Needed)
 * Operates autonomously in the browser and connects directly to Sarvam AI.
 */

import {
  ConfigResponse,
  PresetDoubt,
  LearnerProfile,
  DiagnosisResponse,
  SocraticEvalResponse,
} from '../types';
import { SAMPLE_DOUBTS } from '../data/sampleDoubts';
import {
  loadProfile as lmLoadProfile,
  saveProfile as lmSaveProfile,
  listProfiles as lmListProfiles,
  getAllProfiles as lmGetAllProfiles,
  recordMisconception as lmRecordMisconception,
  resolveMisconception as lmResolveMisconception,
  resetProfile as lmResetProfile,
  exportProfileJson as lmExportProfileJson,
  importProfileJson as lmImportProfileJson,
} from './learnerModel';
import {
  diagnoseDoubtSemantic,
  prepareGraphPayload,
  evaluateStudentSocraticReply,
  generateBoardSolveSchedule,
  generateDivergenceGraphTopology,
  diagnoseSocraticMisconception,
} from './pedagogyEngine';
import {
  synthesizeSpeechSarvam,
  transcribeAudioSarvam,
  translateTextSarvam,
  LANGUAGE_REGISTRY,
  ALL_SPEAKERS,
  MODEL_OPTIONS,
  getStoredApiKey,
} from './sarvamApi';

export async function fetchHealth(): Promise<{ status: string; sarvam_api_configured: boolean; sarvam_api_key_masked: string }> {
  const key = getStoredApiKey();
  return {
    status: 'healthy (client-side)',
    sarvam_api_configured: Boolean(key),
    sarvam_api_key_masked: key ? `${key.slice(0, 4)}...${key.slice(-4)}` : '',
  };
}

export async function fetchConfig(): Promise<ConfigResponse> {
  const key = getStoredApiKey();
  return {
    languages: Object.keys(LANGUAGE_REGISTRY),
    language_registry: LANGUAGE_REGISTRY as any,
    tts_models: MODEL_OPTIONS,
    speakers: ALL_SPEAKERS,
    default_sarvam_api_key: key,
    domains: [
      { id: 'cs', name: '💻 Computer Science & Algorithms' },
      { id: 'law', name: '⚖️ Constitutional Law & Civics' },
      { id: 'econ', name: '📉 Microeconomics & Markets' },
      { id: 'physics', name: '🏔️ Classical Mechanics & Physics' },
      { id: 'history', name: '📜 Modern World History' },
      { id: 'lit', name: '📖 Classical Literature & Drama' },
      { id: 'custom', name: '✏️ Custom Academic Field' },
    ],
  };
}

export async function fetchPresets(): Promise<PresetDoubt[]> {
  const list: PresetDoubt[] = [];
  for (const [key, data] of Object.entries(SAMPLE_DOUBTS)) {
    list.push({
      key,
      title: data.title || key,
      subject: data.subject || 'Academic',
      problem_statement: data.problem_statement || '',
      problem_statement_hi: data.problem_statement_hi || '',
      student_concept: data.student_concept || '',
      student_concept_hi: data.student_concept_hi || '',
      student_steps: data.student_steps || '',
      student_steps_hi: data.student_steps_hi || '',
      student_breakdown: data.student_breakdown || '',
      student_breakdown_hi: data.student_breakdown_hi || '',
      canonical_concept: data.canonical_concept || '',
      derailment_step: data.derailment_step || 2,
    });
  }
  return list;
}

export async function fetchProfiles(): Promise<{ student_id: string; student_name: string }[]> {
  return lmListProfiles();
}

export async function fetchAllProfiles(): Promise<LearnerProfile[]> {
  return lmGetAllProfiles();
}

export async function fetchProfile(studentId: string): Promise<LearnerProfile> {
  return lmLoadProfile(studentId);
}

export async function resetProfile(studentId: string): Promise<LearnerProfile> {
  return lmResetProfile(studentId);
}

export async function exportProfileJson(studentId: string): Promise<{ profile_json: string }> {
  return { profile_json: lmExportProfileJson(studentId) };
}

export async function importProfileJson(profileJson: string): Promise<{ status: string; profile: LearnerProfile }> {
  const prof = lmImportProfileJson(profileJson);
  return { status: 'success', profile: prof };
}

export async function diagnoseDoubt(payload: {
  doubt: string;
  concept?: string;
  steps: string;
  breakdown: string;
  student_id: string;
  input_lang_name: string;
  output_lang_name: string;
  speaker?: string;
  tts_model?: string;
  sarvam_api_key?: string;
}): Promise<DiagnosisResponse> {
  const profile = lmLoadProfile(payload.student_id);

  // 1. Semantic Cognitive Diagnosis (Client-Side)
  const diagnosis = diagnoseDoubtSemantic(
    payload.doubt,
    payload.steps,
    payload.breakdown,
    payload.output_lang_name,
    profile.student_name
  );

  // 2. Record Misconception in Longitudinal Model
  lmRecordMisconception(
    profile,
    diagnosis.canonical_concept,
    diagnosis.canonical_root_misconception,
    diagnosis.severity,
    diagnosis.derailment_reason,
    payload.doubt.slice(0, 60)
  );

  // 3. Prepare Graph Layout
  const graphPayload = prepareGraphPayload(diagnosis);

  // 4. Synthesize Audio directly using Sarvam AI REST API
  const targetCfg = LANGUAGE_REGISTRY[payload.output_lang_name] || LANGUAGE_REGISTRY['Hinglish (हिंग्लिश)'];
  const langCode = targetCfg.code;
  const speaker = payload.speaker || targetCfg.speaker || 'ritu';
  const ttsModel = payload.tts_model || 'bulbul:v3';

  const spokenScript = graphPayload.full_spoken_transcript || diagnosis.narration_script;
  const { audioBase64, statusMsg, isReal } = await synthesizeSpeechSarvam(
    spokenScript,
    langCode,
    speaker,
    ttsModel,
    payload.sarvam_api_key
  );

  // 5. Validity score calculation
  const derailmentStep = diagnosis.derailment_step || 2;
  const totalSteps = Math.max((diagnosis.student_nodes || []).length, derailmentStep, 2);
  let validPct = Math.round(((derailmentStep - 1) / totalSteps) * 100);
  validPct = Math.max(35, Math.min(validPct, 85));

  // 6. Generate Digital Teacher Blackboard Schedule & Divergence Graph Topology
  const boardSolve = generateBoardSolveSchedule(
    payload.doubt,
    payload.steps,
    payload.output_lang_name,
    profile
  );

  const divergenceGraph = generateDivergenceGraphTopology(
    payload.doubt,
    payload.steps,
    payload.output_lang_name,
    profile
  );

  const socraticResult = diagnoseSocraticMisconception(
    payload.doubt,
    payload.steps,
    profile
  );

  return {
    diagnosis,
    graph_payload: graphPayload,
    board_solve: boardSolve,
    divergence_graph: divergenceGraph,
    socratic_result: socraticResult,
    audio_base64: audioBase64,
    audio_msg: statusMsg,
    is_real_audio: isReal,
    valid_pct: validPct,
    derailment_step: derailmentStep,
    canonical_concept: diagnosis.canonical_concept,
    socratic_prompt: diagnosis.socratic_prompt,
    profile,
  };
}

export async function evaluateSocraticReply(payload: {
  socratic_reply: string;
  diagnosis: Record<string, any>;
  student_id: string;
}): Promise<SocraticEvalResponse> {
  const profile = lmLoadProfile(payload.student_id);
  const { is_resolved, feedback_text, badge_level } = evaluateStudentSocraticReply(
    payload.socratic_reply,
    payload.diagnosis
  );

  if (is_resolved) {
    const concept = payload.diagnosis.canonical_concept || '';
    lmResolveMisconception(profile, concept);
  }

  return {
    is_resolved,
    feedback_text,
    badge_level,
    profile,
  };
}

/**
 * Direct API endpoint handler mapping for /api/doubt/board-solve
 */
export async function fetchBoardSolve(
  problem: string,
  steps: string,
  outputLangName: string = 'Hinglish (हिंग्लिश)'
) {
  return generateBoardSolveSchedule(problem, steps, outputLangName);
}

/**
 * Direct API endpoint handler mapping for /api/doubt/divergence-graph
 */
export async function fetchDivergenceGraph(
  problem: string,
  steps: string,
  outputLangName: string = 'Hinglish (हिंग्लिश)'
) {
  return generateDivergenceGraphTopology(problem, steps, outputLangName);
}

/**
 * Speech-to-text pipeline caller via Sarvam Saaras
 */
export async function transcribeStudentVoice(audioBlob: Blob, targetLangCode?: string) {
  return transcribeAudioSarvam(audioBlob, targetLangCode);
}
