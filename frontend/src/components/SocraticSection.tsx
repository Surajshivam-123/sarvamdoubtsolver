import React, { useState } from 'react';
import { Target, Send, CheckCircle2, AlertCircle, AlertTriangle, Sparkles } from 'lucide-react';
import confetti from 'canvas-confetti';
import { evaluateSocraticReply } from '../services/api';
import { LearnerProfile, SocraticDiagnosisResult } from '../types';
import { VoiceInputButton } from './VoiceInputButton';

interface SocraticSectionProps {
  diagnosis: Record<string, any> | null;
  socraticResult?: SocraticDiagnosisResult | null;
  derailmentStep: number;
  socraticPrompt: string;
  studentId: string;
  onProfileUpdated: (profile: LearnerProfile) => void;
}

export const SocraticSection: React.FC<SocraticSectionProps> = ({
  diagnosis,
  socraticResult,
  derailmentStep,
  socraticPrompt,
  studentId,
  onProfileUpdated,
}) => {
  const [replyText, setReplyText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [isResolved, setIsResolved] = useState<boolean | null>(null);

  // Reset student reply & feedback when problem diagnosis changes
  React.useEffect(() => {
    setReplyText('');
    setFeedback(null);
    setIsResolved(null);
  }, [diagnosis?.canonical_concept]);

  if (!diagnosis) return null;

  const handleSubmit = async () => {
    if (!replyText.trim()) return;
    setIsLoading(true);
    setFeedback(null);
    setIsResolved(null);

    try {
      const res = await evaluateSocraticReply({
        socratic_reply: replyText,
        diagnosis,
        student_id: studentId,
      });

      setFeedback(res.feedback_text);
      setIsResolved(res.is_resolved);

      if (res.is_resolved) {
        confetti({
          particleCount: 90,
          spread: 60,
          origin: { y: 0.7 },
          colors: ['#10B981', '#34D399', '#059669', '#F59E0B', '#8B5CF6'],
        });
        onProfileUpdated(res.profile);
      }
    } catch (err: any) {
      setFeedback(err.message || 'Error evaluating response.');
      setIsResolved(false);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-zinc-900/50 backdrop-blur-md rounded-xl p-4 border border-zinc-800/80 shadow-lg space-y-3">
      {/* Header with Minimal Socratic Label */}
      <div className="flex items-center justify-between pb-2 border-b border-zinc-800/70">
        <div className="flex items-center gap-2">
          <Target className="w-4 h-4 text-violet-400" />
          <span className="text-xs font-semibold text-zinc-100">
            Socratic Guidance
          </span>
        </div>

        {socraticResult?.is_recurring && (
          <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-amber-950/70 border border-amber-500/30 text-amber-300 flex items-center gap-1">
            <AlertTriangle className="w-3 h-3" />
            Adapted from prior error history
          </span>
        )}
      </div>

      {/* Socratic Scaffolding Prompt */}
      <div className="p-2.5 rounded-lg bg-zinc-950/60 border border-zinc-800 text-xs text-zinc-200 leading-relaxed font-sans">
        <p className="font-medium text-emerald-300 mb-0.5">
          💡 {socraticResult?.hinglish_vernacular_hint || socraticPrompt}
        </p>
        <p className="text-zinc-400 text-[11px]">
          {socraticResult?.socratic_hint || socraticPrompt}
        </p>
      </div>

      {/* Student Self-Correction Input */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-[11px] font-medium text-zinc-400">
            Your Correction / Self-Reflection:
          </label>
          <VoiceInputButton
            onTranscriptionComplete={(txt) => setReplyText((prev) => (prev ? `${prev} ${txt}` : txt))}
            title="Dictate your response"
          />
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={replyText}
            onChange={(e) => setReplyText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSubmit();
            }}
            placeholder="e.g. My premise failed because I omitted the governing boundary condition..."
            className="flex-1 text-xs text-zinc-100 placeholder-zinc-500 bg-zinc-950/50 border border-zinc-800 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-500/60 font-sans"
          />

          <button
            onClick={handleSubmit}
            disabled={isLoading || !replyText.trim()}
            className={`px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              isLoading || !replyText.trim()
                ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed'
                : 'bg-violet-600 hover:bg-violet-500 text-white cursor-pointer shadow-sm'
            }`}
          >
            {isLoading ? (
              <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <Send className="w-3.5 h-3.5" />
            )}
            <span className="hidden sm:inline">Submit</span>
          </button>
        </div>
      </div>

      {/* Feedback Banner */}
      {feedback && (
        <div
          className={`p-2.5 rounded-lg border flex items-start gap-2 text-xs leading-relaxed ${
            isResolved
              ? 'bg-emerald-950/30 border-emerald-500/30 text-emerald-300'
              : 'bg-amber-950/30 border-amber-500/30 text-amber-300'
          }`}
        >
          {isResolved ? (
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
          ) : (
            <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
          )}
          <div>
            <span className="font-semibold block text-zinc-100">
              {isResolved ? '✓ Resolution Verified!' : 'Hint:'}
            </span>
            <p className="text-zinc-300 text-[11px]">{feedback}</p>
          </div>
        </div>
      )}
    </div>
  );
};
