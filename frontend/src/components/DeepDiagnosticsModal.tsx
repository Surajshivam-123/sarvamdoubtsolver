import React, { useState } from 'react';
import { X, BrainCircuit, BookOpen, Layers, CheckCircle2, Copy, Check } from 'lucide-react';

interface DeepDiagnosticsModalProps {
  isOpen: boolean;
  onClose: () => void;
  diagnosis: Record<string, any> | null;
}

export const DeepDiagnosticsModal: React.FC<DeepDiagnosticsModalProps> = ({
  isOpen,
  onClose,
  diagnosis,
}) => {
  const [copiedDot, setCopiedDot] = useState(false);
  const [activeTab, setActiveTab] = useState<'taxonomy' | 'dot'>('taxonomy');

  if (!isOpen || !diagnosis) return null;

  const conceptDiag = diagnosis.concept_diagnostics || {};
  const topicTaxonomy = conceptDiag.topic_taxonomy || {};
  const mentalModel = conceptDiag.student_mental_model || {};
  const masteryAssessment = conceptDiag.mastery_assessment || {};
  const remediationRecs = conceptDiag.remediation_recommendations || {};
  const dotComparative = diagnosis.dot_comparative || '';

  const copyDotToClipboard = () => {
    navigator.clipboard.writeText(dotComparative);
    setCopiedDot(true);
    setTimeout(() => setCopiedDot(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fade-in">
      <div className="bg-zinc-950 rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl border border-zinc-800 text-zinc-100">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-800 bg-zinc-900/40">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 flex items-center justify-center">
              <BrainCircuit className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-zinc-100">
                Deep Pedagogical Diagnostics & Formal Taxonomy
              </h2>
              <p className="text-xs text-zinc-400">
                Cognitive Modeling, Epistemic Classifiers & Graphviz Topology
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Tab Switcher */}
        <div className="flex border-b border-zinc-800 px-6 pt-2 bg-zinc-900/20">
          <button
            onClick={() => setActiveTab('taxonomy')}
            className={`pb-2.5 px-4 text-xs font-medium border-b-2 transition-all duration-150 ${
              activeTab === 'taxonomy'
                ? 'border-emerald-500 text-emerald-400'
                : 'border-transparent text-zinc-400 hover:text-zinc-200'
            }`}
          >
            Cognitive Diagnostics & Taxonomy
          </button>
          <button
            onClick={() => setActiveTab('dot')}
            className={`pb-2.5 px-4 text-xs font-medium border-b-2 transition-all duration-150 ${
              activeTab === 'dot'
                ? 'border-emerald-500 text-emerald-400'
                : 'border-transparent text-zinc-400 hover:text-zinc-200'
            }`}
          >
            Graphviz Dual Map DOT Syntax
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-5">
          {activeTab === 'taxonomy' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Domain Taxonomy */}
              <div className="bg-zinc-900/50 rounded-xl p-4 border border-zinc-800 space-y-2">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-300 flex items-center gap-1.5 pb-1 border-b border-zinc-800">
                  <BookOpen className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Domain Taxonomy</span>
                </h3>
                <pre className="font-mono text-xs text-zinc-300 overflow-x-auto p-3 bg-zinc-950 rounded-lg border border-zinc-800/80 max-h-48">
                  {JSON.stringify(topicTaxonomy, null, 2)}
                </pre>
              </div>

              {/* Student Mental Model */}
              <div className="bg-zinc-900/50 rounded-xl p-4 border border-zinc-800 space-y-2">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-300 flex items-center gap-1.5 pb-1 border-b border-zinc-800">
                  <Layers className="w-3.5 h-3.5 text-violet-400" />
                  <span>Student Mental Model</span>
                </h3>
                <pre className="font-mono text-xs text-zinc-300 overflow-x-auto p-3 bg-zinc-950 rounded-lg border border-zinc-800/80 max-h-48">
                  {JSON.stringify(mentalModel, null, 2)}
                </pre>
              </div>

              {/* Mastery Assessment */}
              <div className="bg-zinc-900/50 rounded-xl p-4 border border-zinc-800 space-y-2">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-300 flex items-center gap-1.5 pb-1 border-b border-zinc-800">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Mastery Assessment</span>
                </h3>
                <pre className="font-mono text-xs text-zinc-300 overflow-x-auto p-3 bg-zinc-950 rounded-lg border border-zinc-800/80 max-h-48">
                  {JSON.stringify(masteryAssessment, null, 2)}
                </pre>
              </div>

              {/* Remediation Recommendations */}
              <div className="bg-zinc-900/50 rounded-xl p-4 border border-zinc-800 space-y-2">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-300 flex items-center gap-1.5 pb-1 border-b border-zinc-800">
                  <BrainCircuit className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Remediation Recommendations</span>
                </h3>
                <pre className="font-mono text-xs text-zinc-300 overflow-x-auto p-3 bg-zinc-950 rounded-lg border border-zinc-800/80 max-h-48">
                  {JSON.stringify(remediationRecs, null, 2)}
                </pre>
              </div>
            </div>
          ) : (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs text-zinc-400 font-medium">
                  Comparative Dual Graphviz Topological Map (DOT format):
                </span>
                <button
                  onClick={copyDotToClipboard}
                  className="flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium bg-zinc-900 hover:bg-zinc-850 text-zinc-300 border border-zinc-800 transition-colors"
                >
                  {copiedDot ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Copied!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5" />
                      <span>Copy DOT Code</span>
                    </>
                  )}
                </button>
              </div>
              <pre className="font-mono text-xs text-emerald-400 bg-zinc-950 p-4 rounded-xl overflow-x-auto max-h-96 border border-zinc-800">
                {dotComparative}
              </pre>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end px-6 py-3.5 border-t border-zinc-800 bg-zinc-900/40">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg text-xs font-medium text-zinc-300 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 transition-all duration-150"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
