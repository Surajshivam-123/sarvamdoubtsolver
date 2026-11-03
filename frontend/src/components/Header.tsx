import React, { useState, useRef, useEffect } from 'react';
import {
  Sparkles,
  User,
  Settings,
  Globe,
  ChevronDown,
  Check,
  HelpCircle,
  Users,
} from 'lucide-react';
import { LearnerProfile } from '../types';

interface HeaderProps {
  inputLang: string;
  outputLang: string;
  onOutputLangChange: (lang: string) => void;
  availableLanguages: string[];
  sarvamActive: boolean;
  currentProfile: LearnerProfile | null;
  availableProfiles: LearnerProfile[];
  onSelectProfile: (p: LearnerProfile) => void;
  onOpenSettings: () => void;
  onOpenProfile: () => void;
  onOpenDiagnostics: () => void;
  onOpenGuide: () => void;
  hasDiagnosis: boolean;
}

const LANGUAGE_DETAILS: Record<string, { native: string; script: string }> = {
  'English': { native: 'English', script: 'Latin' },
  'Hindi (हिंदी)': { native: 'हिंदी', script: 'Devanagari' },
  'Hinglish (हिंग्लिश)': { native: 'Hinglish', script: 'Code-Switched' },
  'Bengali (বাংলা)': { native: 'বাংলা', script: 'Bengali' },
  'Marathi (मराठी)': { native: 'मराठी', script: 'Devanagari' },
  'Tamil (தமிழ்)': { native: 'தமிழ்', script: 'Tamil' },
  'Telugu (తెలుగు)': { native: 'తెలుగు', script: 'Telugu' },
  'Gujarati (ગુજરાતી)': { native: 'ગુજરાતી', script: 'Gujarati' },
  'Kannada (ಕನ್ನಡ)': { native: 'ಕನ್ನಡ', script: 'Kannada' },
  'Malayalam (മലയാളം)': { native: 'മലയാളം', script: 'Malayalam' },
  'Punjabi (ਪੰਜਾਬੀ)': { native: 'ਪੰਜਾਬੀ', script: 'Gurmukhi' },
};

export const Header: React.FC<HeaderProps> = ({
  outputLang,
  onOutputLangChange,
  availableLanguages,
  currentProfile,
  availableProfiles,
  onSelectProfile,
  onOpenSettings,
  onOpenProfile,
  onOpenGuide,
}) => {
  const [langMenuOpen, setLangMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const langDropdownRef = useRef<HTMLDivElement | null>(null);
  const userDropdownRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (langDropdownRef.current && !langDropdownRef.current.contains(e.target as Node)) {
        setLangMenuOpen(false);
      }
      if (userDropdownRef.current && !userDropdownRef.current.contains(e.target as Node)) {
        setUserMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <header className="sticky top-0 z-40 bg-[#090D16]/90 backdrop-blur-md border-b border-zinc-800/80 px-4 lg:px-8 h-14 flex items-center transition-all duration-200">
      <div className="w-full max-w-6xl mx-auto flex items-center justify-between gap-3">
        {/* Left: Branding (Clean title, no Hindi word "संशय") */}
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center flex-shrink-0">
            <svg width="18" height="18" viewBox="0 0 36 36" fill="none">
              <path
                d="M10.5 13C10.5 10.79 12.29 9 14.5 9H21.5C23.98 9 26 11.01 26 13.5C26 15.98 23.98 18 21.5 18H14.5C12.01 18 10 20.01 10 22.5C10 24.98 12.01 27 14.5 27H21.5C23.7 27 25.5 25.2 25.5 23"
                stroke="#10B981"
                strokeWidth="2.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <circle cx="18" cy="18" r="2.2" fill="#34D399" />
            </svg>
          </div>

          <span className="text-sm font-semibold tracking-tight text-zinc-100 font-sans">
            Bhasha Doubt Solver
          </span>
        </div>

        {/* Center: UI-Pleasing Floating Language Selector Popover */}
        <div className="relative" ref={langDropdownRef}>
          <button
            type="button"
            onClick={() => setLangMenuOpen(!langMenuOpen)}
            className="h-8 flex items-center gap-2 px-3 rounded-lg text-xs font-medium bg-zinc-900/80 hover:bg-zinc-850 border border-zinc-800 hover:border-zinc-700/90 text-zinc-200 transition-all cursor-pointer shadow-sm"
          >
            <Globe className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
            <span>{outputLang}</span>
            <ChevronDown className={`w-3 h-3 text-zinc-400 transition-transform duration-150 ${langMenuOpen ? 'rotate-180' : ''}`} />
          </button>

          {langMenuOpen && (
            <div className="absolute top-10 left-1/2 -translate-x-1/2 z-50 w-64 bg-zinc-950/95 backdrop-blur-2xl border border-zinc-800/90 rounded-xl shadow-2xl p-1.5 space-y-0.5 animate-in fade-in zoom-in-95 duration-150 max-h-80 overflow-y-auto">
              <div className="px-2.5 py-1 text-[10px] font-semibold text-zinc-500 uppercase tracking-wider border-b border-zinc-850/80 mb-1">
                Select Vernacular Output
              </div>

              {availableLanguages.map((lang) => {
                const isSelected = outputLang === lang;
                const details = LANGUAGE_DETAILS[lang] || { native: lang, script: 'Indic' };
                return (
                  <button
                    key={lang}
                    type="button"
                    onClick={() => {
                      onOutputLangChange(lang);
                      setLangMenuOpen(false);
                    }}
                    className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer ${
                      isSelected
                        ? 'bg-emerald-500/15 text-emerald-300 font-semibold border border-emerald-500/20'
                        : 'text-zinc-300 hover:bg-zinc-900 hover:text-white'
                    }`}
                  >
                    <div className="flex items-center gap-2 truncate">
                      {isSelected ? (
                        <Check className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                      ) : (
                        <div className="w-3.5 h-3.5" />
                      )}
                      <span className="truncate">{lang}</span>
                    </div>

                    <span className="text-[10px] font-mono text-zinc-500 bg-zinc-900 px-1.5 py-0.5 rounded border border-zinc-850">
                      {details.script}
                    </span>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Right: User Switcher Dropdown & Onboarding Guide Action Button */}
        <div className="flex items-center gap-2">
          {/* Guide / How-to Button */}
          <button
            type="button"
            onClick={onOpenGuide}
            className="h-8 flex items-center gap-1.5 px-2.5 rounded-lg text-xs font-medium bg-zinc-900/60 hover:bg-zinc-800 border border-zinc-800 hover:border-zinc-700/80 text-zinc-300 hover:text-emerald-300 transition-all cursor-pointer"
            title="How to Use Bhasha Doubt Solver"
          >
            <HelpCircle className="w-3.5 h-3.5 text-emerald-400" />
            <span className="hidden sm:inline">Guide</span>
          </button>

          {/* User Switcher Dropdown */}
          <div className="relative" ref={userDropdownRef}>
            <button
              type="button"
              onClick={() => setUserMenuOpen(!userMenuOpen)}
              className="h-8 flex items-center gap-2 px-2.5 rounded-lg text-xs font-medium bg-zinc-900/80 hover:bg-zinc-850 border border-zinc-800 hover:border-zinc-700 text-zinc-200 transition-all cursor-pointer shadow-sm"
              title="Switch Active Learner Profile"
            >
              <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center justify-center text-[10px] font-bold">
                {currentProfile?.student_name ? currentProfile.student_name[0] : 'A'}
              </div>
              <span className="hidden sm:inline max-w-[110px] truncate text-xs text-zinc-200 font-medium">
                {currentProfile?.student_name || 'Switch User'}
              </span>
              <ChevronDown className={`w-3 h-3 text-zinc-400 transition-transform ${userMenuOpen ? 'rotate-180' : ''}`} />
            </button>

            {userMenuOpen && (
              <div className="absolute right-0 top-10 z-50 w-72 bg-zinc-950/95 backdrop-blur-2xl border border-zinc-800/90 rounded-xl shadow-2xl p-1.5 space-y-1 animate-in fade-in zoom-in-95 duration-150">
                <div className="px-2.5 py-1 text-[10px] font-semibold text-zinc-400 uppercase tracking-wider border-b border-zinc-850/80 flex items-center justify-between">
                  <span className="flex items-center gap-1.5">
                    <Users className="w-3 h-3 text-emerald-400" />
                    <span>Switch Active Learner</span>
                  </span>
                  <span className="text-[10px] text-zinc-500 font-mono">
                    {availableProfiles.length} Students
                  </span>
                </div>

                <div className="max-h-64 overflow-y-auto space-y-0.5">
                  {availableProfiles.map((p) => {
                    const isSelected = p.student_id === currentProfile?.student_id;
                    return (
                      <button
                        key={p.student_id}
                        type="button"
                        onClick={() => {
                          onSelectProfile(p);
                          setUserMenuOpen(false);
                        }}
                        className={`w-full flex items-center justify-between p-2 rounded-lg text-left transition-colors cursor-pointer ${
                          isSelected
                            ? 'bg-emerald-500/15 border border-emerald-500/30 text-emerald-300'
                            : 'text-zinc-300 hover:bg-zinc-900 hover:text-white'
                        }`}
                      >
                        <div className="flex items-center gap-2.5 min-w-0">
                          <div
                            className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold border flex-shrink-0 ${
                              isSelected
                                ? 'bg-emerald-500/30 text-emerald-200 border-emerald-400/50'
                                : 'bg-zinc-850 text-zinc-300 border-zinc-750'
                            }`}
                          >
                            {p.student_name[0]}
                          </div>
                          <div className="min-w-0">
                            <div className="text-xs font-medium truncate">{p.student_name}</div>
                            <div className="text-[10px] text-zinc-500 truncate">
                              {p.preferred_language.split(' ')[0]} • {p.session_count} sessions
                            </div>
                          </div>
                        </div>

                        {isSelected && <Check className="w-4 h-4 text-emerald-400 flex-shrink-0 ml-2" />}
                      </button>
                    );
                  })}
                </div>

                <div className="pt-1.5 border-t border-zinc-850/80">
                  <button
                    type="button"
                    onClick={() => {
                      setUserMenuOpen(false);
                      onOpenProfile();
                    }}
                    className="w-full py-1.5 px-2 text-center text-[11px] text-zinc-400 hover:text-emerald-300 font-medium transition-colors cursor-pointer block rounded-md hover:bg-zinc-900"
                  >
                    View Full Longitudinal Map →
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};