import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { ReasoningConsole } from './components/ReasoningConsole';
import { BlackboardStudio } from './components/BlackboardStudio';
import { SocraticSection } from './components/SocraticSection';
import { StudioSettings } from './components/StudioSettings';
import { ProfileModal } from './components/ProfileModal';
import { SettingsModal } from './components/SettingsModal';
import { DeepDiagnosticsModal } from './components/DeepDiagnosticsModal';
import {
  ConfigResponse,
  PresetDoubt,
  LearnerProfile,
  DiagnosisResponse
} from './types';
import {
  fetchConfig,
  fetchPresets,
  fetchProfile,
  fetchAllProfiles,
  diagnoseDoubt,
} from './services/api';
import { getStoredApiKey } from './services/sarvamApi';
import { OnboardingGuide } from './components/OnboardingGuide';

export const App: React.FC = () => {
  // App Config & Settings
  const [config, setConfig] = useState<ConfigResponse | null>(null);
  const [inputLang, setInputLang] = useState('English');
  const [outputLang, setOutputLang] = useState('Hinglish (हिंग्लिश)');
  const [sarvamKey, setSarvamKey] = useState<string>(() => getStoredApiKey());
  const [speaker, setSpeaker] = useState('ritu');
  const [ttsModel, setTtsModel] = useState('bulbul:v3');

  // Learner Profile State
  const [currentProfile, setCurrentProfile] = useState<LearnerProfile | null>(null);
  const [availableProfiles, setAvailableProfiles] = useState<LearnerProfile[]>([]);
  const [studentId, setStudentId] = useState('arjun_01');

  // Presets & Form State
  const [presets, setPresets] = useState<PresetDoubt[]>([]);
  const [activePresetKey, setActivePresetKey] = useState('coding_balanced_parentheses');
  const [doubt, setDoubt] = useState('');
  const [steps, setSteps] = useState('');
  const [breakdown, setBreakdown] = useState('');

  // Diagnosis & Execution State
  const [diagnosisData, setDiagnosisData] = useState<DiagnosisResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Modals & Onboarding State
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isDiagnosticsOpen, setIsDiagnosticsOpen] = useState(false);
  const [isGuideOpen, setIsGuideOpen] = useState(() => {
    try {
      return !localStorage.getItem('sansay_has_seen_guide');
    } catch {
      return true;
    }
  });

  // Initial Load
  useEffect(() => {
    const initialize = async () => {
      try {
        const [cfg, presetList, prof, allProfs] = await Promise.all([
          fetchConfig(),
          fetchPresets(),
          fetchProfile(studentId),
          fetchAllProfiles(),
        ]);

        setConfig(cfg);
        setPresets(presetList);
        setCurrentProfile(prof);
        setAvailableProfiles(allProfs);
        if (cfg.default_sarvam_api_key) {
          setSarvamKey(cfg.default_sarvam_api_key);
        }

        // Set default preset
        const defaultPreset = presetList.find((p) => p.key === 'coding_balanced_parentheses') || presetList[0];
        if (defaultPreset) {
          loadPreset(defaultPreset, false);
          // Auto diagnose default preset so canvas is instantly alive
          runDiagnosis({
            doubt: defaultPreset.problem_statement,
            steps: defaultPreset.student_steps,
            breakdown: defaultPreset.student_breakdown,
            studentId,
            inputLang: 'English',
            outputLang: 'Hinglish (हिंग्लिश)',
            speaker: 'ritu',
            ttsModel: 'bulbul:v3',
            sarvamKey: cfg.default_sarvam_api_key,
          });
        }
      } catch (err) {
        console.error('Initialization error:', err);
      }
    };

    initialize();
  }, []);

  const loadPreset = (preset: PresetDoubt, autoRun: boolean = true) => {
    setActivePresetKey(preset.key);
    const isHi = (inputLang.includes('Hindi') || inputLang.includes('हिंदी')) && !inputLang.includes('Hinglish');

    const d = (isHi && preset.problem_statement_hi) ? preset.problem_statement_hi : preset.problem_statement;
    const s = (isHi && preset.student_steps_hi) ? preset.student_steps_hi : preset.student_steps;
    const b = (isHi && preset.student_breakdown_hi) ? preset.student_breakdown_hi : preset.student_breakdown;

    setDoubt(d);
    setSteps(s);
    setBreakdown(b);

    if (autoRun) {
      runDiagnosis({
        doubt: d,
        steps: s,
        breakdown: b,
        studentId,
        inputLang,
        outputLang,
        speaker,
        ttsModel,
        sarvamKey,
      });
    }
  };

  const handleSelectCustom = () => {
    setActivePresetKey('custom');
    setDoubt('');
    setSteps('');
    setBreakdown('');
    setDiagnosisData(null); // On clearing previous problem, graph & board erase themselves immediately
  };

  const handleDoubtChange = (val: string) => {
    // If user starts editing or writing another problem while a preset was active:
    if (activePresetKey !== 'custom') {
      setActivePresetKey('custom');
      setSteps(''); // Clear previous problem's thinking steps!
      setBreakdown('');
      setDiagnosisData(null); // Erase previous problem's graph!
    } else {
      // If in custom mode, and problem is cleared:
      if (!val.trim()) {
        setSteps(''); // Clear previous problem's thinking steps!
        setBreakdown('');
        setDiagnosisData(null);
      } else if (diagnosisData) {
        // Erase old graph when user starts editing question after a previous diagnosis
        setDiagnosisData(null);
      }
    }
    setDoubt(val);
  };

  const handleStepsChange = (val: string) => {
    setSteps(val);
    if (!doubt.trim() && !val.trim() && activePresetKey === 'custom') {
      setDiagnosisData(null);
    }
  };

  const runDiagnosis = async (params: {
    doubt: string;
    steps: string;
    breakdown: string;
    studentId: string;
    inputLang: string;
    outputLang: string;
    speaker: string;
    ttsModel: string;
    sarvamKey: string;
  }) => {
    setIsLoading(true);
    try {
      const res = await diagnoseDoubt({
        doubt: params.doubt,
        concept: '', // AI autonomously deduces and diagnoses the concept
        steps: params.steps,
        breakdown: params.breakdown,
        student_id: params.studentId,
        input_lang_name: params.inputLang,
        output_lang_name: params.outputLang,
        speaker: params.speaker,
        tts_model: params.ttsModel,
        sarvam_api_key: params.sarvamKey,
      });

      setDiagnosisData(res);
      setCurrentProfile(res.profile);
    } catch (err: any) {
      alert(err.message || 'Diagnosis failed.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleManualDiagnose = () => {
    if (!doubt.trim() || !steps.trim()) {
      alert('Please provide both the problem statement and your derivation steps.');
      return;
    }
    runDiagnosis({
      doubt,
      steps,
      breakdown,
      studentId,
      inputLang,
      outputLang,
      speaker,
      ttsModel,
      sarvamKey,
    });
  };

  const handleProfileSelect = (p: LearnerProfile) => {
    setCurrentProfile(p);
    setStudentId(p.student_id);
  };

  return (
    <div className="min-h-screen bg-[#090D16] flex flex-col font-sans text-zinc-100 antialiased selection:bg-emerald-500/20 selection:text-emerald-300">
      {/* Top Navigation Header */}
      <Header
        inputLang={inputLang}
        outputLang={outputLang}
        onOutputLangChange={(newLang) => {
          setOutputLang(newLang);
          const cfg = config?.language_registry?.[newLang];
          const newSpeaker = cfg?.speaker || speaker;
          if (cfg?.speaker) {
            setSpeaker(cfg.speaker);
          }
          if (doubt.trim() && steps.trim()) {
            runDiagnosis({
              doubt,
              steps,
              breakdown,
              studentId,
              inputLang,
              outputLang: newLang,
              speaker: newSpeaker,
              ttsModel,
              sarvamKey,
            });
          }
        }}
        availableLanguages={config?.languages || [
          'English',
          'Hindi (हिंदी)',
          'Hinglish (हिंग्लिश)',
          'Bengali (বাংলা)',
          'Marathi (मराठी)',
          'Tamil (தமிழ்)',
          'Telugu (తెలుగు)',
          'Gujarati (ગુજરાતી)',
          'Kannada (ಕನ್ನಡ)',
          'Malayalam (മലയാളം)',
          'Punjabi (ਪੰਜਾਬੀ)',
        ]}
        sarvamActive={Boolean(sarvamKey)}
        currentProfile={currentProfile}
        availableProfiles={availableProfiles}
        onSelectProfile={handleProfileSelect}
        onOpenSettings={() => {
          const el = document.getElementById('studio-settings');
          if (el) {
            el.scrollIntoView({ behavior: 'smooth' });
          } else {
            setIsSettingsOpen(true);
          }
        }}
        onOpenProfile={() => setIsProfileOpen(true)}
        onOpenDiagnostics={() => setIsDiagnosticsOpen(true)}
        onOpenGuide={() => setIsGuideOpen(true)}
        hasDiagnosis={Boolean(diagnosisData)}
      />

      {/* Main Studio Container: Unified Stacked Layout (Input at Top, Studio & Guidance Below) */}
      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-5 space-y-5">
        {/* Top: Input & Problem Statement */}
        <ReasoningConsole
          doubt={doubt}
          setDoubt={handleDoubtChange}
          steps={steps}
          setSteps={handleStepsChange}
          breakdown={breakdown}
          setBreakdown={setBreakdown}
          presets={presets}
          activePresetKey={activePresetKey}
          onSelectPreset={(p) => loadPreset(p, true)}
          onSelectCustom={handleSelectCustom}
          inputLang={inputLang}
          outputLang={outputLang}
          profile={currentProfile}
          onDiagnose={handleManualDiagnose}
          isLoading={isLoading}
        />

        {/* Below: Interactive Blackboard Studio & Socratic Guidance */}
        <div className="space-y-4">
          <BlackboardStudio
            boardSolve={diagnosisData?.board_solve || null}
            divergenceGraph={diagnosisData?.divergence_graph || null}
            graphPayload={diagnosisData?.graph_payload || null}
            audioBase64={diagnosisData?.audio_base64 || ''}
            audioMsg={diagnosisData?.audio_msg || ''}
            isRealAudio={diagnosisData?.is_real_audio || false}
            validPct={diagnosisData?.valid_pct || 75}
            derailmentStep={diagnosisData?.derailment_step || 2}
            canonicalTopic={diagnosisData?.canonical_concept || 'Academic Concept'}
            outputLang={outputLang}
          />

          <SocraticSection
            diagnosis={diagnosisData?.diagnosis || null}
            socraticResult={diagnosisData?.socratic_result || null}
            derailmentStep={diagnosisData?.derailment_step || 2}
            socraticPrompt={diagnosisData?.socratic_prompt || 'Apply the core governing constraint.'}
            studentId={studentId}
            onProfileUpdated={setCurrentProfile}
          />

          {/* On-Screen Studio Settings & AI Audio Voice Controls */}
          <div id="studio-settings" className="pt-2">
            <StudioSettings
              config={config}
              sarvamKey={sarvamKey}
              setSarvamKey={setSarvamKey}
              speaker={speaker}
              setSpeaker={setSpeaker}
              ttsModel={ttsModel}
              setTtsModel={setTtsModel}
              currentProfile={currentProfile}
              onSelectProfile={handleProfileSelect}
              outputLang={outputLang}
            />
          </div>
        </div>
      </main>

      {/* Modals */}
      <ProfileModal
        isOpen={isProfileOpen}
        onClose={() => setIsProfileOpen(false)}
        currentProfile={currentProfile}
        onSelectProfile={handleProfileSelect}
      />

      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        config={config}
        inputLang={inputLang}
        setInputLang={setInputLang}
        outputLang={outputLang}
        setOutputLang={setOutputLang}
        sarvamKey={sarvamKey}
        setSarvamKey={setSarvamKey}
        speaker={speaker}
        setSpeaker={setSpeaker}
        ttsModel={ttsModel}
        setTtsModel={setTtsModel}
      />

      <DeepDiagnosticsModal
        isOpen={isDiagnosticsOpen}
        onClose={() => setIsDiagnosticsOpen(false)}
        diagnosis={diagnosisData?.diagnosis || null}
      />

      {/* Interactive Onboarding Guide (Auto-opens on first visit, accessible anytime via header Guide button) */}
      <OnboardingGuide
        isOpen={isGuideOpen}
        onClose={() => setIsGuideOpen(false)}
      />
    </div>
  );
};
