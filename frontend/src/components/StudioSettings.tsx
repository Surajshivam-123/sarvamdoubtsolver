import React from 'react';
import {
  Volume2,
  Sparkles,
  CheckCircle2,
  Sliders,
  Radio,
  User,
  ShieldCheck,
  BrainCircuit,
  Zap,
} from 'lucide-react';
import { ConfigResponse, LearnerProfile } from '../types';

interface StudioSettingsProps {
  config: ConfigResponse | null;
  sarvamKey: string;
  setSarvamKey: (k: string) => void;
  speaker: string;
  setSpeaker: (s: string) => void;
  ttsModel: string;
  setTtsModel: (m: string) => void;
  currentProfile: LearnerProfile | null;
  onSelectProfile: (p: LearnerProfile) => void;
  outputLang: string;
}

const VOICE_PRESETS = [
  { id: 'ritu', name: 'Ritu / Meera', desc: 'Hindi & Hinglish Natural', lang: 'Hindi/Hinglish' },
  { id: 'aditya', name: 'Aditya', desc: 'Hindi Expressive Male', lang: 'Hindi' },
  { id: 'simran', name: 'Simran', desc: 'Indian English Female', lang: 'English' },
  { id: 'soham', name: 'Soham', desc: 'Marathi Expressive', lang: 'Marathi' },
  { id: 'roopa', name: 'Roopa', desc: 'Bengali Melodic', lang: 'Bengali' },
  { id: 'gokul', name: 'Gokul', desc: 'Tamil / Malayalam', lang: 'Tamil' },
  { id: 'kavitha', name: 'Kavitha', desc: 'Telugu Expressive', lang: 'Telugu' },
];

export const StudioSettings: React.FC<StudioSettingsProps> = ({
  speaker,
  setSpeaker,
  ttsModel,
  setTtsModel,
  currentProfile,
  outputLang,
}) => {
  return (
    <section id="studio-settings" className="bg-zinc-900/50 backdrop-blur-md rounded-xl p-4 sm:p-5 border border-zinc-800/80 shadow-xl space-y-4">
      {/* Top Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-zinc-800/70">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 flex items-center justify-center">
            <Sliders className="w-3.5 h-3.5" />
          </div>
          <div>
            <h3 className="text-xs font-semibold text-zinc-100 flex items-center gap-2">
              <span>Voice & Model Controls</span>
            </h3>
          </div>
        </div>
      </div>

      {/* Grid: 2 Main Columns */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Left Column: Voice & Model Selection */}
        <div className="space-y-3">
          <div>
            <label className="text-[11px] font-semibold text-zinc-300 uppercase tracking-wider block mb-1.5">
              Teacher Voice Persona ({outputLang.split(' ')[0]}):
            </label>

            <div className="grid grid-cols-2 gap-1.5">
              {VOICE_PRESETS.map((v) => {
                const isSelected = speaker.toLowerCase() === v.id || (v.id === 'ritu' && speaker.toLowerCase() === 'meera');
                return (
                  <button
                    key={v.id}
                    type="button"
                    onClick={() => setSpeaker(v.id)}
                    className={`flex flex-col text-left px-2.5 py-1.5 rounded-lg border transition-all cursor-pointer ${
                      isSelected
                        ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-300 shadow-sm'
                        : 'bg-zinc-950/50 hover:bg-zinc-900 border-zinc-800/80 text-zinc-400 hover:text-zinc-200'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium text-zinc-200">{v.name}</span>
                      <span className="text-[9px] font-mono text-zinc-500">{v.lang}</span>
                    </div>
                    <span className="text-[10px] text-zinc-500 truncate">{v.desc}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Model Selection */}
          <div className="pt-2 border-t border-zinc-800/60 flex items-center justify-between">
            <span className="text-xs text-zinc-300 font-medium">TTS Synthesis Engine:</span>
            <div className="flex gap-1.5">
              <button
                type="button"
                onClick={() => setTtsModel('bulbul:v3')}
                className={`text-xs px-2.5 py-1 rounded-lg border transition-all cursor-pointer ${
                  ttsModel === 'bulbul:v3'
                    ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-300 font-medium'
                    : 'bg-zinc-950/60 border-zinc-800 text-zinc-400 hover:text-zinc-200'
                }`}
              >
                bulbul:v3 (Expressive)
              </button>
              <button
                type="button"
                onClick={() => setTtsModel('bulbul:v4-flash')}
                className={`text-xs px-2.5 py-1 rounded-lg border transition-all cursor-pointer ${
                  ttsModel === 'bulbul:v4-flash'
                    ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-300 font-medium'
                    : 'bg-zinc-950/60 border-zinc-800 text-zinc-400 hover:text-zinc-200'
                }`}
              >
                bulbul:v4-flash (Fast)
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Engine Status & Learner Trajectory */}
        <div className="space-y-3">
          {/* Engine Status Card (No API Key shown) */}
          <div className="p-3 rounded-lg bg-zinc-950/60 border border-zinc-800/80 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="text-zinc-300 font-medium flex items-center gap-1.5">
                <BrainCircuit className="w-3.5 h-3.5 text-emerald-400" />
                <span>Sarvam AI Speech Engine</span>
              </span>
              <span className="text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                Online & Ready
              </span>
            </div>

            <p className="text-[11px] text-zinc-400 leading-relaxed font-sans">
              Vernacular audio narration is directly synthesized using Sarvam AI Bulbul neural models with automatic multi-chunk WAV buffer concatenation.
            </p>

            <div className="flex items-center gap-3 pt-1 text-[11px] font-mono text-zinc-500">
              <span className="flex items-center gap-1 text-zinc-400">
                <Zap className="w-3 h-3 text-amber-400" />
                High Fidelity Indic TTS
              </span>
              <span>•</span>
              <span className="text-zinc-400">Environment Configured</span>
            </div>
          </div>

          {/* Active Learner Profile Info */}
          <div className="p-3 rounded-lg bg-zinc-950/40 border border-zinc-800/60 space-y-1.5">
            <div className="flex items-center justify-between text-xs">
              <span className="text-zinc-400 flex items-center gap-1.5">
                <User className="w-3.5 h-3.5 text-emerald-400" />
                <span>Active Learner:</span>
              </span>
              <span className="font-semibold text-zinc-200">
                {currentProfile?.student_name || 'Arjun Sharma'}
              </span>
            </div>
            <p className="text-[11px] text-zinc-500 line-clamp-2">
              Trajectory: "{currentProfile?.pedagogical_trajectory || 'Developing cognitive invariance'}"
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};