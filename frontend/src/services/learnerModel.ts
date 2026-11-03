import { LearnerProfile, ErrorHistoryItem } from '../types';

const PROFILE_STORAGE_PREFIX = 'sansay_profile_';

const DEFAULT_PROFILES: Record<string, LearnerProfile> = {
  arjun_01: {
    student_id: 'arjun_01',
    student_name: 'Arjun Sharma',
    preferred_language: 'Hinglish (हिंग्लिश)',
    preferred_voice: 'ritu',
    created_at: new Date(Date.now() - 14 * 86400000).toISOString(),
    last_active: new Date().toISOString(),
    session_count: 7,
    mastery_map: {
      'Balanced Parentheses & LIFO Invariant': 'misconception_prone',
      'Article 19(2) Reasonable Restrictions': 'solid',
      'Price Ceilings & Deadweight Loss': 'fragile',
      'Work-Energy Theorem in Non-Conservative Systems': 'fragile',
      'Causality Chains in World War I': 'solid',
      'Hamartia vs Hubris in Macbeth': 'solid',
    },
    error_history: [
      {
        timestamp: new Date(Date.now() - 2 * 86400000).toISOString(),
        problem_topic: 'Coding & Algorithms',
        concept: 'Balanced Parentheses & LIFO Invariant',
        type: 'State Space Counter Inadequacy',
        severity: 'High',
        details: 'Assumed an integer balance counter >= 0 is sufficient for multiple bracket types ((), [], {}), missing interleaving violations.',
        resolved: false,
      },
      {
        timestamp: new Date(Date.now() - 5 * 86400000).toISOString(),
        problem_topic: 'Microeconomics',
        concept: 'Price Ceilings & Deadweight Loss',
        type: 'Equilibrium Distortion Neglect',
        severity: 'Medium',
        details: 'Treated artificial price cap as increase in real consumer surplus without accounting for non-price rationing queues.',
        resolved: true,
      },
    ],
    pedagogical_trajectory: 'Excels at historical causality and constitutional balancing; tends to use scalar counters for bracket LIFO matching.',
  },
  priya_02: {
    student_id: 'priya_02',
    student_name: 'Priya Patel',
    preferred_language: 'English',
    preferred_voice: 'rohan',
    created_at: new Date(Date.now() - 30 * 86400000).toISOString(),
    last_active: new Date().toISOString(),
    session_count: 12,
    mastery_map: {
      'Balanced Parentheses & LIFO Invariant': 'solid',
      'Article 19(2) Reasonable Restrictions': 'fragile',
      'Price Ceilings & Deadweight Loss': 'solid',
      'Work-Energy Theorem in Non-Conservative Systems': 'solid',
    },
    error_history: [
      {
        timestamp: new Date(Date.now() - 3 * 86400000).toISOString(),
        problem_topic: 'Constitutional Law',
        concept: 'Article 19(2) Reasonable Restrictions',
        type: 'Absolutist Free Speech Conflation',
        severity: 'High',
        details: 'Treated Article 19(1)(a) as an uninhibited natural right without cross-referencing Article 19(2) statutory grounds.',
        resolved: false,
      },
    ],
    pedagogical_trajectory: 'Strong algorithmic rigor; requires occasional socratic reminders on proportional constitutional constraints.',
  },
  rohan_03: {
    student_id: 'rohan_03',
    student_name: 'Rohan Deshmukh',
    preferred_language: 'Hindi (हिंदी)',
    preferred_voice: 'aditya',
    created_at: new Date(Date.now() - 20 * 86400000).toISOString(),
    last_active: new Date().toISOString(),
    session_count: 5,
    mastery_map: {
      'Balanced Parentheses & LIFO Invariant': 'fragile',
      'Work-Energy Theorem in Non-Conservative Systems': 'misconception_prone',
    },
    error_history: [
      {
        timestamp: new Date(Date.now() - 1 * 86400000).toISOString(),
        problem_topic: 'Classical Mechanics',
        concept: 'Work-Energy Theorem in Non-Conservative Systems',
        type: 'Mechanical Energy Conservation Fallacy',
        severity: 'Critical',
        details: 'Equated mechanical energy conservation in the presence of kinetic sliding friction without non-conservative path integrals.',
        resolved: false,
      },
    ],
    pedagogical_trajectory: 'Enthusiastic experimentalist; benefits from explicit system boundary formulations prior to equation setup.',
  },
  ananya_04: {
    student_id: 'ananya_04',
    student_name: 'Ananya Iyer',
    preferred_language: 'Tamil (தமிழ்)',
    preferred_voice: 'gokul',
    created_at: new Date(Date.now() - 40 * 86400000).toISOString(),
    last_active: new Date().toISOString(),
    session_count: 18,
    mastery_map: {
      'Price Ceilings & Deadweight Loss': 'misconception_prone',
      'Hamartia vs Hubris in Macbeth': 'solid',
    },
    error_history: [],
    pedagogical_trajectory: 'Deep literary insight; developing nuanced market equilibrium diagnostics.',
  },
  karthik_05: {
    student_id: 'karthik_05',
    student_name: 'Karthik Nair',
    preferred_language: 'Malayalam (മലയാളം)',
    preferred_voice: 'rohan',
    created_at: new Date(Date.now() - 10 * 86400000).toISOString(),
    last_active: new Date().toISOString(),
    session_count: 3,
    mastery_map: {
      'Causality Chains in World War I': 'misconception_prone',
    },
    error_history: [],
    pedagogical_trajectory: 'Methodical thinker; transitioning from mono-causal narratives to multi-polar structural analysis.',
  },
};

export function listProfiles(): { student_id: string; student_name: string }[] {
  return Object.values(DEFAULT_PROFILES).map((p) => ({
    student_id: p.student_id,
    student_name: p.student_name,
  }));
}

export function getAllProfiles(): LearnerProfile[] {
  return Object.keys(DEFAULT_PROFILES).map((id) => loadProfile(id));
}

export function loadProfile(studentId: string): LearnerProfile {
  try {
    const raw = localStorage.getItem(PROFILE_STORAGE_PREFIX + studentId);
    if (raw) {
      return JSON.parse(raw);
    }
  } catch (e) {
    console.warn('Error reading learner profile from localStorage:', e);
  }

  const fallback = DEFAULT_PROFILES[studentId] || DEFAULT_PROFILES['arjun_01'];
  // Clone to avoid mutation of constant
  const copy = JSON.parse(JSON.stringify(fallback));
  saveProfile(copy);
  return copy;
}

export function saveProfile(profile: LearnerProfile): void {
  try {
    profile.last_active = new Date().toISOString();
    localStorage.setItem(PROFILE_STORAGE_PREFIX + profile.student_id, JSON.stringify(profile));
  } catch (e) {
    console.warn('Failed to save profile to localStorage:', e);
  }
}

export function resetProfile(studentId: string): LearnerProfile {
  const base = DEFAULT_PROFILES[studentId] || DEFAULT_PROFILES['arjun_01'];
  const fresh = JSON.parse(JSON.stringify(base));
  saveProfile(fresh);
  return fresh;
}

export function exportProfileJson(studentId: string): string {
  const profile = loadProfile(studentId);
  return JSON.stringify(profile, null, 2);
}

export function importProfileJson(jsonStr: string): LearnerProfile {
  const parsed = JSON.parse(jsonStr);
  if (!parsed.student_id) throw new Error('Invalid profile: missing student_id');
  saveProfile(parsed);
  return parsed;
}

export function recordMisconception(
  profile: LearnerProfile,
  concept: string,
  misconceptionType: string,
  severity: string,
  details: string,
  problemTopic: string = ''
): LearnerProfile {
  const newErr: ErrorHistoryItem = {
    timestamp: new Date().toISOString(),
    problem_topic: problemTopic || concept,
    concept: concept,
    type: misconceptionType,
    severity: severity,
    details: details,
    resolved: false,
  };

  profile.error_history.push(newErr);
  profile.mastery_map[concept] = 'misconception_prone';
  profile.session_count = (profile.session_count || 1) + 1;
  saveProfile(profile);
  return profile;
}

export function resolveMisconception(profile: LearnerProfile, concept: string): LearnerProfile {
  for (const err of profile.error_history) {
    if (
      err.concept.toLowerCase().includes(concept.toLowerCase()) ||
      concept.toLowerCase().includes(err.concept.toLowerCase())
    ) {
      err.resolved = true;
    }
  }

  profile.mastery_map[concept] = 'solid';
  saveProfile(profile);
  return profile;
}
