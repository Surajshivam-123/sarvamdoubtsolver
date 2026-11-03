import React, { useState } from 'react';
import {
  Sparkles,
  BookOpen,
  GitBranch,
  Volume2,
  Users,
  CheckCircle2,
  ArrowRight,
  ArrowLeft,
  X,
  Compass,
  Lightbulb,
} from 'lucide-react';

interface OnboardingGuideProps {
  isOpen: boolean;
  onClose: () => void;
}

const GUIDE_STEPS = [
  {
    step: 1,
    badge: 'Welcome to Bhasha Doubt Solver',
    title: 'A Vernacular Socratic Digital Teacher',
    desc: 'Unlike standard AI bots that spoil the answer, Bhasha Doubt Solver works like a real teacher: it uncovers how you think, detects hidden conceptual flaws, and guides you to solve it yourself.',
    icon: <Sparkles className="w-6 h-6 text-emerald-400" />,
    features: [
      'Pure Client-Side Architecture powered by Sarvam AI Indic Models.',
      'Covers 11 Diverse Academic Domains (Algorithms, Calculus, Genetics, Economics, Law, Mechanics, History, etc.).',
      'Never hands out raw answers; scaffolds your mental model.',
    ],
  },
  {
    step: 2,
    badge: 'Step 1: Problem Input',
    title: 'Pick a Sample Doubt or Enter Your Own',
    desc: 'Choose from quick sample chips across diverse disciplines, dictate your problem using Indic speech-to-text, or snap a photo of equations using OCR.',
    icon: <BookOpen className="w-6 h-6 text-cyan-400" />,
    features: [
      'Click any field chip to instantly populate the problem.',
      'Click "Clear / Custom Problem" anytime to start from scratch.',
      'The AI autonomously detects your academic domain without manual tagging.',
    ],
  },
  {
    step: 3,
    badge: 'Step 2: Mental Model Elicitation',
    title: 'Explain Your Step-by-Step Thinking',
    desc: 'Before evaluating, the system asks you to share your initial premise or attempted derivation steps.',
    icon: <Compass className="w-6 h-6 text-amber-400" />,
    features: [
      'Share where you started or which step felt confusing.',
      'Helps the pedagogical engine pinpoint the exact logical branch that derailed.',
      'Builds deep cognitive invariants rather than shallow rote memorization.',
    ],
  },
  {
    step: 4,
    badge: 'Step 3: Interactive Visual Studio',
    title: 'Digital Chalkboard & Divergence Graph',
    desc: 'Explore the step-by-step chalkboard derivation or switch to the interactive Mind Map to visualize the critical pivot point.',
    icon: <GitBranch className="w-6 h-6 text-violet-400" />,
    features: [
      'Chalkboard View: Step-by-step KaTeX mathematical and logical derivation.',
      'Mind Map View: Pan and zoom across premise, pivot, and canonical invariant nodes.',
      'Press Spacebar anytime to re-center and align the divergence graph.',
    ],
  },
  {
    step: 5,
    badge: 'Step 4: Detailed Indic Voice Narration',
    title: 'Listen to Detailed Teacher Explanations',
    desc: 'Listen to a structured 4-part teacher masterclass in Hindi, Hinglish, Bengali, Marathi, Tamil, Telugu, and more.',
    icon: <Volume2 className="w-6 h-6 text-rose-400" />,
    features: [
      'Synthesized using Sarvam AI Bulbul neural voices.',
      'Explains premise validation, derailment breakdown, counterexamples, and reflection hints.',
      'Respond to the Socratic reflection box below to resolve the misconception!',
    ],
  },
  {
    step: 6,
    badge: 'Step 5: Longitudinal Tracking',
    title: 'Switch Learners & Track Conceptual Growth',
    desc: 'Use the user switcher on the top right to switch between learners and view persistent error histories across sessions.',
    icon: <Users className="w-6 h-6 text-emerald-400" />,
    features: [
      'Top-Right User Switcher: Instantly toggle between Arjun, Priya, Rohan, Ananya, and Karthik.',
      'Longitudinal Profiles: Tracks misconception tags and mastery trajectories.',
      'Adapts future hints based on what concepts previously confused each student.',
    ],
  },
];

export const OnboardingGuide: React.FC<OnboardingGuideProps> = ({
  isOpen,
  onClose,
}) => {
  const [currentStep, setCurrentStep] = useState(0);

  if (!isOpen) return null;

  const stepData = GUIDE_STEPS[currentStep];
  const isFirst = currentStep === 0;
  const isLast = currentStep === GUIDE_STEPS.length - 1;

  const handleNext = () => {
    if (isLast) {
      handleComplete();
    } else {
      setCurrentStep((prev) => prev + 1);
    }
  };

  const handlePrev = () => {
    if (!isFirst) {
      setCurrentStep((prev) => prev - 1);
    }
  };

  const handleComplete = () => {
    try {
      localStorage.setItem('sansay_has_seen_guide', 'true');
    } catch {}
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="bg-zinc-950 border border-zinc-800 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden flex flex-col text-zinc-100 animate-in zoom-in-95 duration-200">
        {/* Header Bar */}
        <div className="px-5 py-3.5 border-b border-zinc-800/80 flex items-center justify-between bg-zinc-900/40">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
              User Guide • {currentStep + 1} of {GUIDE_STEPS.length}
            </span>
          </div>

          <button
            onClick={handleComplete}
            className="p-1 rounded-lg text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 transition-colors cursor-pointer"
            title="Close Guide"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-4">
          <div className="flex items-start gap-3.5">
            <div className="w-12 h-12 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-center flex-shrink-0 shadow-lg">
              {stepData.icon}
            </div>

            <div>
              <span className="text-[11px] font-mono font-medium text-emerald-400 uppercase tracking-wider block mb-1">
                {stepData.badge}
              </span>
              <h3 className="text-base font-semibold text-zinc-100 leading-snug">
                {stepData.title}
              </h3>
            </div>
          </div>

          <p className="text-xs text-zinc-300 leading-relaxed font-sans">
            {stepData.desc}
          </p>

          {/* Feature List */}
          <div className="p-3 rounded-xl bg-zinc-900/60 border border-zinc-800/80 space-y-2">
            {stepData.features.map((feat, idx) => (
              <div key={idx} className="flex items-start gap-2 text-xs text-zinc-300">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span className="leading-snug">{feat}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Footer Navigation */}
        <div className="px-6 py-3.5 border-t border-zinc-800/80 bg-zinc-900/40 flex items-center justify-between">
          {/* Progress dots */}
          <div className="flex items-center gap-1.5">
            {GUIDE_STEPS.map((_, idx) => (
              <button
                key={idx}
                onClick={() => setCurrentStep(idx)}
                className={`h-1.5 rounded-full transition-all cursor-pointer ${
                  idx === currentStep
                    ? 'w-5 bg-emerald-400'
                    : 'w-1.5 bg-zinc-800 hover:bg-zinc-700'
                }`}
                title={`Go to step ${idx + 1}`}
              />
            ))}
          </div>

          <div className="flex items-center gap-2">
            {!isFirst && (
              <button
                type="button"
                onClick={handlePrev}
                className="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-zinc-200 hover:bg-zinc-850 transition-colors flex items-center gap-1 cursor-pointer"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Back</span>
              </button>
            )}

            <button
              type="button"
              onClick={handleNext}
              className="px-4 py-1.5 rounded-lg text-xs font-semibold text-zinc-950 bg-emerald-500 hover:bg-emerald-400 shadow-md shadow-emerald-500/20 transition-all flex items-center gap-1.5 cursor-pointer active:scale-[0.98]"
            >
              <span>{isLast ? 'Get Started' : 'Next'}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
