import React, { useState } from 'react';
import { X, Volume2, Key, Globe, Sparkles, CheckCircle2, AlertCircle } from 'lucide-react';
import { ConfigResponse } from '../types';
import { saveStoredApiKey } from '../services/sarvamApi';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  config: ConfigResponse | null;
  inputLang: string;
  setInputLang: (l: string) => void;
  outputLang: string;
  setOutputLang: (l: string) => void;
  sarvamKey: string;
  setSarvamKey: (k: string) => void;
  speaker: string;
  setSpeaker: (s: string) => void;
  ttsModel: string;
  setTtsModel: (m: string) => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({
  isOpen,
  onClose,
  config,
  inputLang,
  setInputLang,
  outputLang,
  setOutputLang,
  sarvamKey,
  setSarvamKey,
  speaker,
  setSpeaker,
  ttsModel,
  setTtsModel,
}) => {
  if (!isOpen || !config) return null;

  const isHinglish = outputLang.includes('Hinglish') || outputLang.includes('हिंग्लिश');
  const isPureHindi = (outputLang.includes('Hindi') || outputLang.includes('हिंदी')) && !isHinglish;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fade-in">
      <div className="bg-zinc-950 rounded-2xl w-full max-w-xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl border border-zinc-800 text-zinc-100">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-800 bg-zinc-900/40">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 flex items-center justify-center">
              <Globe className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-zinc-100">Translation & Sarvam Voice Engine</h2>
              <p className="text-xs text-zinc-400">Configure Indian Languages, Speech Dictation & API Keys</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto space-y-5">
          {/* 1. Language Matrix */}
          <div className="space-y-3">
            <h3 className="text-xs font-semibold text-zinc-400 uppercase tracking-wider flex items-center gap-1.5">
              <span>01 // Multilingual Translation Matrix</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-zinc-300 mb-1.5">
                  Student Input Language:
                </label>
                <select
                  value={inputLang}
                  onChange={(e) => setInputLang(e.target.value)}
                  className="w-full text-xs font-medium text-zinc-100 bg-zinc-900/70 border border-zinc-800 rounded-xl px-3 py-2.5 focus:border-emerald-500/60 focus:outline-none transition-colors"
                >
                  {config.languages.map((l) => (
                    <option key={l} value={l} className="bg-zinc-900 text-zinc-100">
                      {l}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-zinc-300 mb-1.5">
                  Voice & Remediation Target:
                </label>
                <select
                  value={outputLang}
                  onChange={(e) => {
                    const l = e.target.value;
                    setOutputLang(l);
                    const cfg = config.language_registry[l];
                    if (cfg && cfg.speaker) {
                      setSpeaker(cfg.speaker);
                    }
                  }}
                  className="w-full text-xs font-medium text-zinc-100 bg-zinc-900/70 border border-zinc-800 rounded-xl px-3 py-2.5 focus:border-emerald-500/60 focus:outline-none transition-colors"
                >
                  {config.languages.map((l) => (
                    <option key={l} value={l} className="bg-zinc-900 text-zinc-100">
                      {l}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Mode Explanations */}
            {isHinglish && (
              <div className="p-3 rounded-xl bg-zinc-900/60 border border-zinc-800 text-xs text-zinc-300 leading-relaxed font-sans">
                💡 <b className="text-emerald-400 font-semibold">Hinglish (हिंग्लिश) Active:</b> Technical academic terminology across Law, Economics, History, Literature, Coding, and Science is preserved in conversational English for clarity.
              </div>
            )}
            {isPureHindi && (
              <div className="p-3 rounded-xl bg-zinc-900/60 border border-zinc-800 text-xs text-zinc-300 leading-relaxed font-sans">
                🇮🇳 <b className="text-emerald-400 font-semibold">Hindi (हिंदी) Active:</b> सभी विषयों की मानक शब्दावली हिंदी में प्रस्तुत की जाती है।
              </div>
            )}
          </div>

          <div className="border-t border-zinc-800/80" />

          {/* 2. Sarvam AI Configuration */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-semibold text-zinc-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>02 // Sarvam AI Speech Engine</span>
              </h3>
              {sarvamKey ? (
                <span className="flex items-center gap-1 text-[11px] font-semibold text-emerald-400 bg-emerald-950/40 px-2.5 py-0.5 rounded-full border border-emerald-500/30">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  API Active
                </span>
              ) : (
                <span className="flex items-center gap-1 text-[11px] font-semibold text-amber-400 bg-amber-950/40 px-2.5 py-0.5 rounded-full border border-amber-500/30">
                  <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
                  Harmonic Wave Fallback
                </span>
              )}
            </div>

            {/* API Engine Status (No raw key shown) */}
            <div className="p-3 rounded-xl bg-zinc-900/60 border border-zinc-800 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-medium text-zinc-200">Sarvam Speech & Translation Engine:</span>
                <span className="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                  Active via .env
                </span>
              </div>
              <p className="text-[11px] text-zinc-400 mt-1 font-sans">
                Neural Indic TTS and Speech-to-Text are seamlessly connected from your workspace environment. No manual key entry needed.
              </p>
            </div>

            {/* Speaker & TTS Model */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
              <div>
                <label className="block text-xs font-medium text-zinc-300 mb-1.5">
                  Voice Persona:
                </label>
                <select
                  value={speaker}
                  onChange={(e) => setSpeaker(e.target.value)}
                  className="w-full text-xs font-medium text-zinc-100 bg-zinc-900/70 border border-zinc-800 rounded-xl px-3 py-2.5 focus:border-emerald-500/60 focus:outline-none transition-colors"
                >
                  {config.speakers.map((s) => (
                    <option key={s} value={s} className="bg-zinc-900 text-zinc-100">
                      {s.charAt(0).toUpperCase() + s.slice(1)} (Native)
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-zinc-300 mb-1.5">
                  TTS Architecture:
                </label>
                <select
                  value={ttsModel}
                  onChange={(e) => setTtsModel(e.target.value)}
                  className="w-full text-xs font-medium text-zinc-100 bg-zinc-900/70 border border-zinc-800 rounded-xl px-3 py-2.5 focus:border-emerald-500/60 focus:outline-none transition-colors"
                >
                  {config.tts_models.map((m) => (
                    <option key={m} value={m} className="bg-zinc-900 text-zinc-100">
                      {m}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end px-6 py-3.5 border-t border-zinc-800 bg-zinc-900/40">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg text-xs font-semibold text-zinc-950 bg-emerald-500 hover:bg-emerald-400 shadow-md shadow-emerald-500/20 transition-all duration-150"
          >
            Apply & Close
          </button>
        </div>
      </div>
    </div>
  );
};
