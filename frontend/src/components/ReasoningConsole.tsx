import React, { useState, useRef } from 'react';
import {
  Sparkles,
  Bot,
  Search,
  Camera,
  X,
  Code2,
  Calculator,
  TrendingDown,
  Dna,
  FlaskConical,
  Scale,
  Compass,
  Scroll,
  BookOpen,
  HeartPulse,
  Zap,
  RotateCcw,
} from 'lucide-react';
import { LearnerProfile, PresetDoubt } from '../types';
import { VoiceInputButton } from './VoiceInputButton';
import { MathRenderer } from './MathRenderer';
import { processImageOcr } from '../services/multimodalOcr';
import { detectUniversalDomain } from '../services/pedagogyEngine';

interface ReasoningConsoleProps {
  doubt: string;
  setDoubt: (val: string) => void;
  steps: string;
  setSteps: (val: string) => void;
  breakdown: string;
  setBreakdown: (val: string) => void;
  presets: PresetDoubt[];
  activePresetKey: string;
  onSelectPreset: (preset: PresetDoubt) => void;
  onSelectCustom: () => void;
  inputLang: string;
  outputLang: string;
  profile: LearnerProfile | null;
  onDiagnose: () => void;
  isLoading: boolean;
}

const CHIP_ICONS: Record<string, React.ReactNode> = {
  coding_balanced_parentheses: <Code2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />,
  calculus_chain_rule: <Calculator className="w-3.5 h-3.5 text-cyan-400 flex-shrink-0" />,
  economics_rent_control: <TrendingDown className="w-3.5 h-3.5 text-amber-400 flex-shrink-0" />,
  biology_genetics_linkage: <Dna className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />,
  chemistry_le_chatelier_catalyst: <FlaskConical className="w-3.5 h-3.5 text-pink-400 flex-shrink-0" />,
  law_freedom_of_speech: <Scale className="w-3.5 h-3.5 text-blue-400 flex-shrink-0" />,
  logic_affirming_consequent: <Compass className="w-3.5 h-3.5 text-indigo-400 flex-shrink-0" />,
  history_ww1_causality: <Scroll className="w-3.5 h-3.5 text-orange-400 flex-shrink-0" />,
  literature_macbeth_tragic_flaw: <BookOpen className="w-3.5 h-3.5 text-violet-400 flex-shrink-0" />,
  medicine_pharmacology_kinetics: <HeartPulse className="w-3.5 h-3.5 text-rose-400 flex-shrink-0" />,
  physics_incline_friction: <Zap className="w-3.5 h-3.5 text-teal-400 flex-shrink-0" />,
};

export const ReasoningConsole: React.FC<ReasoningConsoleProps> = ({
  doubt,
  setDoubt,
  steps,
  setSteps,
  presets,
  activePresetKey,
  onSelectPreset,
  onSelectCustom,
  inputLang,
  outputLang,
  onDiagnose,
  isLoading,
}) => {
  const [showElicitationPrompt, setShowElicitationPrompt] = useState(false);
  const [ocrMathEquations, setOcrMathEquations] = useState<string[]>([]);
  const [scannedFileName, setScannedFileName] = useState<string | null>(null);
  const [isProcessingOcr, setIsProcessingOcr] = useState(false);

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const isPureHindi = (inputLang.includes('Hindi') || inputLang.includes('हिंदी')) && (!inputLang.includes('Hinglish') && !inputLang.includes('हिंग्लिश'));

  const lblDoubt = isPureHindi ? 'समस्या या प्रश्न' : 'Your Problem';
  const phDoubt = isPureHindi
    ? 'यहाँ किसी भी विषय का प्रश्न लिखें, बोलें या फ़ोटो अपलोड करें...'
    : 'Type, dictate, or upload a photo of your problem in any field...';

  const lblSteps = isPureHindi ? 'आपका प्रारंभिक तर्क / विचार' : 'Your Initial Thinking & Attempt';
  const phSteps = isPureHindi
    ? 'बताइए आपने इस प्रश्न को कैसे शुरू किया, या कौन सा चरण समझ नहीं आ रहा...'
    : 'Explain how you started thinking about it, or which step feels confusing...';

  // AI Autonomous Field Detection (No user domain selection needed)
  const detectedDomain = doubt.trim() ? detectUniversalDomain(doubt, steps) : null;

  const handlePhotoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setIsProcessingOcr(true);
      try {
        const result = await processImageOcr(file);
        setDoubt(result.problemStatement);
        setSteps(''); // Clear previous problem's thinking steps
        setOcrMathEquations(result.latexEquations || []);
        setScannedFileName(result.fileName);
        setShowElicitationPrompt(true);
      } catch (err) {
        alert('Failed to scan image equations.');
      } finally {
        setIsProcessingOcr(false);
        if (fileInputRef.current) fileInputRef.current.value = '';
      }
    }
  };

  const handleTriggerDiagnose = () => {
    if (!doubt.trim()) {
      alert('Please enter or dictate a question first.');
      return;
    }
    // Socratic Rule: prompt student to explain their thought process first
    if (!steps.trim()) {
      setShowElicitationPrompt(true);
      return;
    }
    onDiagnose();
  };

  const handleApplyQuickIntuition = (intuitionSnippet: string) => {
    setSteps(intuitionSnippet);
    setShowElicitationPrompt(false);
  };

  return (
    <div className="space-y-3">
      {/* Hidden File Input for Photo OCR */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handlePhotoUpload}
        className="hidden"
      />

      {/* Quick Sample Choosing Options Across Different Fields (No dropdown menu) */}
      <div className="p-3 rounded-xl bg-zinc-900/50 border border-zinc-800/80 shadow-sm space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-zinc-300 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
            <span>Sample Doubts from Different Fields:</span>
          </span>

          <button
            type="button"
            onClick={() => {
              onSelectCustom();
              setShowElicitationPrompt(false);
            }}
            className={`flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-md border transition-all cursor-pointer ${
              activePresetKey === 'custom'
                ? 'bg-violet-500/15 border-violet-500/50 text-violet-300 font-medium'
                : 'bg-zinc-950/50 hover:bg-zinc-900 border-zinc-800 hover:border-zinc-700 text-zinc-400'
            }`}
            title="Clear inputs to ask your own custom question"
          >
            <RotateCcw className="w-3 h-3" />
            <span>Clear / Custom Problem</span>
          </button>
        </div>

        {/* Choosing Chips */}
        <div className="flex flex-wrap gap-1.5">
          {presets.map((preset) => {
            const isSelected = activePresetKey === preset.key;
            return (
              <button
                key={preset.key}
                type="button"
                onClick={() => {
                  onSelectPreset(preset);
                  setShowElicitationPrompt(false);
                }}
                className={`flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-lg border transition-all cursor-pointer text-left ${
                  isSelected
                    ? 'bg-emerald-500/15 border-emerald-500/50 text-emerald-300 font-medium shadow-sm'
                    : 'bg-zinc-950/60 hover:bg-zinc-900 border-zinc-800 hover:border-zinc-700 text-zinc-300'
                }`}
              >
                {CHIP_ICONS[preset.key] || <Sparkles className="w-3.5 h-3.5 text-zinc-400" />}
                <span className="truncate">{preset.title}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Input Card (Clean, minimal, no char/token/step metrics) */}
      <div className="bg-zinc-900/50 backdrop-blur-md border border-zinc-800/80 rounded-xl p-4 shadow-xl space-y-3.5">
        {/* Field 1: Question / Doubt */}
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <div className="flex items-center gap-2">
              <label className="text-xs font-semibold text-zinc-200">
                {lblDoubt}
              </label>
              {doubt && (
                <button
                  type="button"
                  onClick={() => {
                    onSelectCustom();
                    setDoubt('');
                    setSteps('');
                  }}
                  className="text-[10px] text-zinc-400 hover:text-rose-400 px-1.5 py-0.5 rounded bg-zinc-950 border border-zinc-800 transition-colors cursor-pointer"
                  title="Clear problem and thinking"
                >
                  Clear
                </button>
              )}
            </div>

            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                disabled={isProcessingOcr}
                className="p-1 rounded-md text-zinc-400 hover:text-emerald-400 hover:bg-zinc-800/80 transition-colors cursor-pointer"
                title="Upload homework photo (Math, Code, Biology, Chemistry)"
              >
                <Camera className={`w-3.5 h-3.5 ${isProcessingOcr ? 'animate-pulse text-emerald-400' : ''}`} />
              </button>

              <VoiceInputButton
                onTranscriptionComplete={(txt) => {
                  if (activePresetKey !== 'custom') {
                    onSelectCustom();
                    setSteps('');
                    setDoubt(txt);
                  } else {
                    setDoubt(doubt ? `${doubt} ${txt}` : txt);
                  }
                }}
                languageCode={outputLang.includes('Hindi') ? 'hi-IN' : 'en-IN'}
                title="Dictate problem statement via Sarvam Saaras ASR"
              />
            </div>
          </div>

          <textarea
            rows={3}
            value={doubt}
            onChange={(e) => setDoubt(e.target.value)}
            placeholder={phDoubt}
            className="w-full text-xs text-zinc-100 bg-zinc-950/60 border border-zinc-800 rounded-lg p-2.5 focus:outline-none focus:border-emerald-500/60 placeholder-zinc-600 transition-all resize-y font-sans leading-relaxed"
          />

          {/* Scanned Image Tag / Formulas */}
          {scannedFileName && (
            <div className="mt-1.5 flex items-center justify-between px-2 py-1 rounded-md bg-zinc-950 border border-emerald-500/30 text-[11px] text-emerald-300">
              <div className="flex items-center gap-1.5 truncate">
                <Camera className="w-3 h-3 text-emerald-400 flex-shrink-0" />
                <span className="truncate">{scannedFileName} (Scanned)</span>
              </div>
              <button
                type="button"
                onClick={() => {
                  setScannedFileName(null);
                  setOcrMathEquations([]);
                }}
                className="text-zinc-400 hover:text-white ml-2 cursor-pointer"
              >
                <X className="w-3 h-3" />
              </button>
            </div>
          )}

          {ocrMathEquations.length > 0 && (
            <div className="mt-1 flex flex-wrap gap-1 items-center">
              {ocrMathEquations.slice(0, 2).map((eq, i) => (
                <span key={i} className="px-1.5 py-0.5 rounded bg-zinc-950 border border-zinc-800 text-zinc-300 text-[10px]">
                  <MathRenderer math={eq} />
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Stage 1: Socratic Elicitation Reminder */}
        {showElicitationPrompt && (
          <div className="p-2.5 rounded-lg bg-amber-950/20 border border-amber-500/30 text-xs space-y-1.5 animate-in fade-in duration-150">
            <div className="flex items-start gap-2">
              <Bot className="w-3.5 h-3.5 text-amber-400 flex-shrink-0 mt-0.5" />
              <p className="text-[11px] text-amber-200">
                Pehle batao aapne is problem ko shuru kaise kiya ya kahan confusion hai?
              </p>
            </div>

            <div className="flex flex-wrap gap-1 pt-1">
              <button
                type="button"
                onClick={() => handleApplyQuickIntuition('Applied direct formula without checking boundary constraints.')}
                className="text-[10px] px-2 py-0.5 rounded bg-zinc-900 border border-amber-500/20 text-zinc-300 hover:text-white cursor-pointer"
              >
                "Applied formula without checking bounds"
              </button>
              <button
                type="button"
                onClick={() => handleApplyQuickIntuition('Stuck on identifying the governing rule for this state.')}
                className="text-[10px] px-2 py-0.5 rounded bg-zinc-900 border border-amber-500/20 text-zinc-300 hover:text-white cursor-pointer"
              >
                "Stuck on governing rule"
              </button>
            </div>
          </div>
        )}

        {/* Field 2: Thought Process / Steps */}
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <div className="flex items-center gap-2">
              <label className="text-xs font-semibold text-zinc-200">
                {lblSteps}
              </label>
              {steps && (
                <button
                  type="button"
                  onClick={() => setSteps('')}
                  className="text-[10px] text-zinc-400 hover:text-rose-400 px-1.5 py-0.5 rounded bg-zinc-950 border border-zinc-800 transition-colors cursor-pointer"
                  title="Clear previous thinking steps"
                >
                  Clear thinking
                </button>
              )}
            </div>

            <VoiceInputButton
              onTranscriptionComplete={(txt) => setSteps(steps ? `${steps}\n${txt}` : txt)}
              languageCode={outputLang.includes('Hindi') ? 'hi-IN' : 'en-IN'}
              title="Speak your intuition via Sarvam Saaras ASR"
            />
          </div>

          <textarea
            rows={3}
            value={steps}
            onChange={(e) => {
              setSteps(e.target.value);
              if (e.target.value.trim()) setShowElicitationPrompt(false);
            }}
            placeholder={phSteps}
            className="w-full font-mono text-xs text-zinc-100 bg-zinc-950/60 border border-zinc-800 rounded-lg p-2.5 focus:outline-none focus:border-emerald-500/60 placeholder-zinc-600 transition-all resize-y leading-relaxed"
          />
        </div>

        {/* Action Button */}
        <button
          onClick={handleTriggerDiagnose}
          disabled={isLoading || !doubt.trim()}
          className={`w-full h-8 rounded-lg font-medium text-xs flex items-center justify-center gap-2 transition-all cursor-pointer ${
            isLoading || !doubt.trim()
              ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed'
              : 'bg-emerald-500 hover:bg-emerald-400 text-zinc-950 shadow-md shadow-emerald-500/20 active:scale-[0.99]'
          }`}
        >
          {isLoading ? (
            <>
              <div className="w-3.5 h-3.5 border-2 border-zinc-950/30 border-t-zinc-950 rounded-full animate-spin" />
              <span>Analyzing Your Thinking...</span>
            </>
          ) : (
            <>
              <Search className="w-3.5 h-3.5" />
              <span>Analyze Thinking</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};