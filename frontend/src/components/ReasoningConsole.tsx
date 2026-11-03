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
  const [isDragOver, setIsDragOver] = useState(false);

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const isPureHindi = (inputLang.includes('Hindi') || inputLang.includes('हिंदी')) && (!inputLang.includes('Hinglish') && !inputLang.includes('हिंग्लिश'));

  const lblDoubt = isPureHindi ? 'समस्या या प्रश्न' : 'Your Problem';
  const phDoubt = isPureHindi
    ? 'यहाँ किसी भी विषय का प्रश्न लिखें, बोलें, पेस्ट करें (Ctrl+V) या फ़ोटो अपलोड करें...'
    : 'Type, dictate, paste image (Ctrl+V), or upload photo of problem/figure...';

  const lblSteps = isPureHindi ? 'आपका प्रारंभिक तर्क / विचार' : 'Your Initial Thinking & Attempt';
  const phSteps = isPureHindi
    ? 'बताइए आपने इस प्रश्न को कैसे शुरू किया, या कौन सा चरण समझ नहीं आ रहा...'
    : 'Explain how you started thinking about it, or which step feels confusing...';

  // AI Autonomous Field Detection (No user domain selection needed)
  const detectedDomain = doubt.trim() ? detectUniversalDomain(doubt, steps) : null;

  const processUploadedImage = async (file: File) => {
    setIsProcessingOcr(true);
    // 1. Immediately break away from Computer Science demo preset & clear old canvas
    onSelectCustom();
    setDoubt('🔍 Scanning problem figure & equations with Vision Model...');
    try {
      const result = await processImageOcr(file);
      // 2. Fill "Your Problem" textarea with text understood from figure!
      setDoubt(result.problemStatement);
      setSteps(''); // Clear previous problem's thinking steps
      setOcrMathEquations(result.latexEquations || []);
      setScannedFileName(result.fileName || file.name);
      setShowElicitationPrompt(true);
    } catch (err) {
      alert('Failed to scan image. Please enter your problem statement.');
      setDoubt('');
    } finally {
      setIsProcessingOcr(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handlePhotoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      await processUploadedImage(e.target.files[0]);
    }
  };

  const handlePaste = (e: React.ClipboardEvent<HTMLTextAreaElement>) => {
    const items = e.clipboardData?.items;
    if (!items) return;
    for (let i = 0; i < items.length; i++) {
      if (items[i].type.startsWith('image/')) {
        const file = items[i].getAsFile();
        if (file) {
          processUploadedImage(file);
          e.preventDefault();
          break;
        }
      }
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processUploadedImage(e.dataTransfer.files[0]);
    }
  };

  const handleTriggerDiagnose = () => {
    if (!doubt.trim()) {
      alert('Please enter or dictate a question first.');
      return;
    }
    // If student did not provide an intuition, request first-principles derivation without polluting with dummy assumptions
    if (!steps.trim()) {
      const defaultAttempt = 'Formulate step-by-step resolution from first principles.';
      setSteps(defaultAttempt);
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

            <div className="flex items-center gap-1.5">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                disabled={isProcessingOcr}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium border transition-all cursor-pointer ${
                  isProcessingOcr
                    ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50 animate-pulse'
                    : 'bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 hover:text-emerald-300 border-emerald-500/30'
                }`}
                title="Upload or snap photo of homework problem or figure"
              >
                <Camera className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                <span>{isProcessingOcr ? 'Scanning Figure...' : 'Scan Figure / Photo'}</span>
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

          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`relative rounded-lg transition-all ${
              isDragOver ? 'ring-2 ring-emerald-400 bg-emerald-950/20' : ''
            }`}
          >
            <textarea
              rows={4}
              value={doubt}
              onChange={(e) => setDoubt(e.target.value)}
              onPaste={handlePaste}
              placeholder={phDoubt}
              disabled={isProcessingOcr}
              className="w-full text-xs text-zinc-100 bg-zinc-950/60 border border-zinc-800 rounded-lg p-2.5 focus:outline-none focus:border-emerald-500/60 placeholder-zinc-600 transition-all resize-y font-sans leading-relaxed"
            />
            {isDragOver && (
              <div className="absolute inset-0 bg-emerald-950/80 border-2 border-dashed border-emerald-400 rounded-lg flex items-center justify-center text-xs text-emerald-300 pointer-events-none font-medium">
                Drop problem photo or diagram here to scan
              </div>
            )}
          </div>

          {/* Scanned Figure Understanding Badge */}
          {scannedFileName && (
            <div className="mt-1.5 p-2 rounded-lg bg-emerald-950/30 border border-emerald-500/40 text-[11px] text-emerald-300 space-y-1">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1.5 truncate">
                  <Sparkles className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                  <span className="font-semibold text-emerald-200">
                    Figure Understood by AI Model ({scannedFileName})
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    setScannedFileName(null);
                    setOcrMathEquations([]);
                  }}
                  className="text-zinc-400 hover:text-white ml-2 cursor-pointer"
                  title="Dismiss figure badge"
                >
                  <X className="w-3 h-3" />
                </button>
              </div>

              {ocrMathEquations.length > 0 && (
                <div className="pt-0.5 flex flex-wrap gap-1.5 items-center">
                  {ocrMathEquations.map((eq, i) => (
                    <span key={i} className="px-2 py-0.5 rounded bg-zinc-950/80 border border-emerald-500/30 text-zinc-200 text-[10px]">
                      <MathRenderer math={eq} />
                    </span>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Stage 1: Socratic Elicitation Reminder */}
        {showElicitationPrompt && (
          <div className="p-2.5 rounded-lg bg-amber-950/20 border border-amber-500/30 text-xs space-y-1.5 animate-in fade-in duration-150">
            <div className="flex items-start gap-2">
              <Bot className="w-3.5 h-3.5 text-amber-400 flex-shrink-0 mt-0.5" />
              <p className="text-[11px] text-amber-200">
                {scannedFileName
                  ? `Problem understood from "${scannedFileName}"! Tell us how you started thinking about it, or select a starter:`
                  : 'Tell us how you started thinking about it, or select a starter:'}
              </p>
            </div>

            <div className="flex flex-wrap gap-1 pt-1">
              <button
                type="button"
                onClick={() => handleApplyQuickIntuition('Applied the standard formula directly, but calculated answer conflicts with options.')}
                className="text-[10px] px-2 py-0.5 rounded bg-zinc-900 border border-amber-500/20 text-emerald-300 hover:text-white cursor-pointer"
              >
                "Applied standard formula directly"
              </button>
              <button
                type="button"
                onClick={() => handleApplyQuickIntuition('Confused about the initial/boundary conditions and which parameters to substitute.')}
                className="text-[10px] px-2 py-0.5 rounded bg-zinc-900 border border-amber-500/20 text-zinc-300 hover:text-white cursor-pointer"
              >
                "Confused about initial / boundary conditions"
              </button>
              <button
                type="button"
                onClick={() => handleApplyQuickIntuition('Not sure which fundamental law or formula governs this system.')}
                className="text-[10px] px-2 py-0.5 rounded bg-zinc-900 border border-amber-500/20 text-zinc-300 hover:text-white cursor-pointer"
              >
                "Uncertain about governing law"
              </button>
              <button
                type="button"
                onClick={() => handleApplyQuickIntuition('Attempted step-by-step resolution but got stuck at the intermediate algebraic step.')}
                className="text-[10px] px-2 py-0.5 rounded bg-zinc-900 border border-amber-500/20 text-zinc-300 hover:text-white cursor-pointer"
              >
                "Stuck at intermediate step"
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