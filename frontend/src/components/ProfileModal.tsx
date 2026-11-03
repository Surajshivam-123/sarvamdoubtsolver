import React, { useState, useEffect } from 'react';
import {
  X,
  User,
  RotateCcw,
  Download,
  Upload,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Clock,
  Sparkles
} from 'lucide-react';
import { LearnerProfile } from '../types';
import { fetchProfiles, fetchProfile, resetProfile, exportProfileJson, importProfileJson } from '../services/api';

interface ProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentProfile: LearnerProfile | null;
  onSelectProfile: (profile: LearnerProfile) => void;
}

export const ProfileModal: React.FC<ProfileModalProps> = ({
  isOpen,
  onClose,
  currentProfile,
  onSelectProfile,
}) => {
  const [profileList, setProfileList] = useState<{ student_id: string; student_name: string }[]>([]);
  const [selectedStudentId, setSelectedStudentId] = useState<string>(currentProfile?.student_id || 'arjun_01');
  const [activeProfile, setActiveProfile] = useState<LearnerProfile | null>(currentProfile);
  const [importJsonText, setImportJsonText] = useState('');
  const [showImportBox, setShowImportBox] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');

  useEffect(() => {
    if (isOpen) {
      fetchProfiles().then(setProfileList).catch(console.error);
    }
  }, [isOpen]);

  useEffect(() => {
    if (currentProfile) {
      setActiveProfile(currentProfile);
      setSelectedStudentId(currentProfile.student_id);
    }
  }, [currentProfile]);

  if (!isOpen || !activeProfile) return null;

  const handleSwitchStudent = async (id: string) => {
    setSelectedStudentId(id);
    try {
      const p = await fetchProfile(id);
      setActiveProfile(p);
      onSelectProfile(p);
      setStatusMsg(`Switched to ${p.student_name}`);
      setTimeout(() => setStatusMsg(''), 2500);
    } catch (e) {
      console.error(e);
    }
  };

  const handleReset = async () => {
    if (window.confirm(`Are you sure you want to reset ${activeProfile.student_name}'s profile?`)) {
      try {
        const p = await resetProfile(activeProfile.student_id);
        setActiveProfile(p);
        onSelectProfile(p);
        setStatusMsg('Learner profile reset to defaults.');
        setTimeout(() => setStatusMsg(''), 2500);
      } catch (e) {
        console.error(e);
      }
    }
  };

  const handleExport = async () => {
    try {
      const res = await exportProfileJson(activeProfile.student_id);
      const blob = new Blob([res.profile_json], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${activeProfile.student_id}_profile.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error(e);
    }
  };

  const handleImport = async () => {
    if (!importJsonText.trim()) return;
    try {
      const res = await importProfileJson(importJsonText);
      setActiveProfile(res.profile);
      onSelectProfile(res.profile);
      setShowImportBox(false);
      setImportJsonText('');
      setStatusMsg('Profile imported successfully!');
      setTimeout(() => setStatusMsg(''), 2500);
    } catch (e: any) {
      alert(e.message || 'Failed to import JSON');
    }
  };

  const solidCount = Object.values(activeProfile.mastery_map || {}).filter((v) => v === 'solid').length;
  const fragileCount = Object.values(activeProfile.mastery_map || {}).filter((v) => v === 'fragile').length;
  const errorCount = Object.values(activeProfile.mastery_map || {}).filter((v) => v === 'misconception_prone').length;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fade-in">
      <div className="bg-zinc-950 rounded-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl border border-zinc-800 text-zinc-100">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-800 bg-zinc-900/40">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 flex items-center justify-center">
              <User className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-zinc-100">Longitudinal Learner Model</h2>
              <p className="text-xs text-zinc-400">Persistent Cognitive Trace Across Problem Sessions</p>
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
          {/* Status Message */}
          {statusMsg && (
            <div className="p-2.5 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 text-xs font-medium text-center">
              {statusMsg}
            </div>
          )}

          {/* Student Profile Switcher */}
          <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-xl bg-zinc-900/50 border border-zinc-800">
            <label className="text-xs font-semibold uppercase tracking-wider text-zinc-400">
              Active Student Profile:
            </label>
            <div className="flex flex-wrap gap-2">
              {profileList.map((p) => (
                <button
                  key={p.student_id}
                  onClick={() => handleSwitchStudent(p.student_id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-150 ${
                    selectedStudentId === p.student_id
                      ? 'bg-emerald-500 text-zinc-950 font-semibold shadow-md shadow-emerald-500/20'
                      : 'bg-zinc-900 text-zinc-300 border border-zinc-800 hover:border-zinc-700 hover:text-white'
                  }`}
                >
                  {p.student_name.split(' ')[0]}
                </button>
              ))}
            </div>
          </div>

          {/* Trajectory Banner */}
          <div className="p-4 rounded-xl bg-zinc-900/60 border border-zinc-800 space-y-1.5">
            <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-400 uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Pedagogical Trajectory</span>
            </div>
            <p className="text-xs text-zinc-300 leading-relaxed font-sans">
              "{activeProfile.pedagogical_trajectory}"
            </p>
          </div>

          {/* Mastery Map Distribution */}
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-2.5">
              Concept Mastery Map
            </h3>
            <div className="grid grid-cols-3 gap-2.5 mb-3">
              <div className="p-3 rounded-xl bg-emerald-950/25 border border-emerald-500/20 text-center">
                <span className="block text-xl font-bold text-emerald-400">{solidCount}</span>
                <span className="text-[11px] font-medium text-emerald-300">Solid Retention</span>
              </div>
              <div className="p-3 rounded-xl bg-amber-950/25 border border-amber-500/20 text-center">
                <span className="block text-xl font-bold text-amber-400">{fragileCount}</span>
                <span className="text-[11px] font-medium text-amber-300">Fragile Invariants</span>
              </div>
              <div className="p-3 rounded-xl bg-red-950/25 border border-red-500/20 text-center">
                <span className="block text-xl font-bold text-red-400">{errorCount}</span>
                <span className="text-[11px] font-medium text-red-300">Misconception Prone</span>
              </div>
            </div>

            <div className="max-h-36 overflow-y-auto space-y-1.5 pr-1">
              {Object.entries(activeProfile.mastery_map || {}).map(([concept, status]) => (
                <div
                  key={concept}
                  className="flex items-center justify-between text-xs px-3 py-1.5 rounded-lg bg-zinc-900/50 border border-zinc-800/70"
                >
                  <span className="font-medium text-zinc-200">{concept}</span>
                  <span
                    className={`text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider ${
                      status === 'solid'
                        ? 'bg-emerald-950/80 text-emerald-300 border border-emerald-500/30'
                        : status === 'fragile'
                        ? 'bg-amber-950/80 text-amber-300 border border-amber-500/30'
                        : 'bg-red-950/80 text-red-300 border border-red-500/30'
                    }`}
                  >
                    {status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Chronological Error History */}
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-2 flex items-center justify-between">
              <span>Error History Audit Trail</span>
              <span className="text-[11px] text-zinc-500 font-normal">
                {activeProfile.error_history?.length || 0} Records
              </span>
            </h3>

            <div className="max-h-48 overflow-y-auto space-y-2 pr-1">
              {(activeProfile.error_history || []).slice().reverse().map((item, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-xl bg-zinc-900/40 border border-zinc-800/70 text-xs space-y-1"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-zinc-200">{item.concept}</span>
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                        item.resolved
                          ? 'bg-emerald-950/80 text-emerald-300 border border-emerald-500/30'
                          : 'bg-red-950/80 text-red-300 border border-red-500/30'
                      }`}
                    >
                      {item.resolved ? '✓ Resolved' : '⚠ Active Misconception'}
                    </span>
                  </div>
                  <p className="text-zinc-400 font-sans">{item.details}</p>
                  <div className="text-[10px] text-zinc-500 flex items-center gap-2 pt-1">
                    <span>Severity: <b className="text-zinc-400">{item.severity}</b></span>
                    <span>•</span>
                    <span>{new Date(item.timestamp).toLocaleDateString()}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Import JSON Box */}
          {showImportBox && (
            <div className="p-4 rounded-xl bg-zinc-900/60 border border-zinc-800 space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-zinc-400">
                Paste Learner Profile JSON:
              </label>
              <textarea
                rows={4}
                value={importJsonText}
                onChange={(e) => setImportJsonText(e.target.value)}
                placeholder='{"student_id": "...", "student_name": "...", "mastery_map": {...}}'
                className="w-full font-mono text-xs bg-zinc-950 border border-zinc-800 rounded-xl p-2.5 text-zinc-200 focus:outline-none focus:border-emerald-500/60"
              />
              <div className="flex justify-end gap-2">
                <button
                  onClick={() => setShowImportBox(false)}
                  className="px-3 py-1.5 text-xs text-zinc-400 hover:text-white rounded-lg"
                >
                  Cancel
                </button>
                <button
                  onClick={handleImport}
                  className="px-3 py-1.5 text-xs font-semibold text-zinc-950 bg-emerald-500 hover:bg-emerald-400 rounded-lg shadow-sm"
                >
                  Import Profile
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between px-6 py-3.5 border-t border-zinc-800 bg-zinc-900/40">
          <button
            onClick={handleReset}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-red-400 hover:text-red-300 hover:bg-red-950/30 rounded-lg border border-red-500/20 transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset Profile</span>
          </button>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowImportBox(!showImportBox)}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-zinc-300 bg-zinc-900 border border-zinc-800 hover:bg-zinc-800 hover:text-white rounded-lg transition-colors"
            >
              <Upload className="w-3.5 h-3.5" />
              <span>Import JSON</span>
            </button>
            <button
              onClick={handleExport}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-zinc-300 bg-zinc-900 border border-zinc-800 hover:bg-zinc-800 hover:text-white rounded-lg transition-colors"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export JSON</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
