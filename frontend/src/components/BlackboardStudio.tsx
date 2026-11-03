import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
  Play,
  Pause,
  RotateCcw,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Sparkles,
  AlertTriangle,
  Lightbulb,
  X,
  Radio,
  ChevronUp,
  ChevronDown,
  Layers,
  ChevronLeft,
  ChevronRight,
  BookOpen,
  GitBranch,
  Volume2,
  Crosshair,
  Network,
} from 'lucide-react';
import {
  GraphPayload,
  NodeCard,
  BoardSolveResponse,
  DivergenceGraphResponse,
  GraphNode,
  GraphEdge
} from '../types';
import { MathRenderer } from './MathRenderer';

interface BlackboardStudioProps {
  isLoading?: boolean;
  boardSolve: BoardSolveResponse | null;
  divergenceGraph: DivergenceGraphResponse | null;
  graphPayload: GraphPayload | null;
  audioBase64: string;
  audioMsg: string;
  isRealAudio: boolean;
  validPct: number;
  derailmentStep: number;
  canonicalTopic: string;
  outputLang: string;
}

export const BlackboardStudio: React.FC<BlackboardStudioProps> = ({
  isLoading = false,
  boardSolve,
  divergenceGraph,
  graphPayload,
  audioBase64,
  audioMsg,
  isRealAudio,
  validPct,
  derailmentStep,
  canonicalTopic,
  outputLang,
}) => {
  // Mode: Chalkboard Step-by-Step Derivation vs Divergence Graph
  const [activeTab, setActiveTab] = useState<'board' | 'graph'>('board');

  // Chalkboard Derivation State (Strictly reset whenever new problem output arrives)
  const [currentBoardStepIndex, setCurrentBoardStepIndex] = useState(0);

  // Audio state
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [playbackRate, setPlaybackRate] = useState(1.0);
  const [activeSubtitle, setActiveSubtitle] = useState('');
  const [activeStepId, setActiveStepId] = useState<number | null>(null);
  const [showFullTranscript, setShowFullTranscript] = useState(false);

  // Reset chalkboard step, subtitles, and stop previous problem audio when problem changes
  useEffect(() => {
    setCurrentBoardStepIndex(0);
    setActiveStepId(null);
    setActiveSubtitle('');
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsPlaying(false);
    }
  }, [boardSolve, canonicalTopic]);

  // Pan & Zoom Canvas State (for Graph)
  const [scale, setScale] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [selectedNode, setSelectedNode] = useState<GraphNode | NodeCard | null>(null);
  const [showZoneBTree, setShowZoneBTree] = useState(false);

  const containerRef = useRef<HTMLDivElement | null>(null);

  // Initialize or update audio when audioBase64 changes
  useEffect(() => {
    if (audioBase64 && audioRef.current) {
      audioRef.current.src = `data:audio/wav;base64,${audioBase64}`;
      audioRef.current.load();
      setIsPlaying(false);
      setCurrentTime(0);
    } else if (!audioBase64 && audioRef.current) {
      audioRef.current.pause();
      audioRef.current.removeAttribute('src');
      audioRef.current.load();
      setIsPlaying(false);
      setCurrentTime(0);
    }
  }, [audioBase64]);

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration || graphPayload?.total_duration || 16);
    }
  };

  const handleTimeUpdate = () => {
    if (!audioRef.current) return;
    const cur = audioRef.current.currentTime;
    setCurrentTime(cur);

    if (graphPayload?.timeline && graphPayload.timeline.length > 0) {
      const match = graphPayload.timeline.find(
        (t) => cur >= t.start_time && cur <= t.end_time
      );
      if (match) {
        setActiveSubtitle(match.speech_segment);
        setActiveStepId(match.step_id);
        // Sync chalkboard step
        const stepIdx = Math.min(match.step_id - 1, (boardSolve?.steps.length || 1) - 1);
        if (stepIdx >= 0) {
          setCurrentBoardStepIndex(stepIdx);
        }
      } else if (cur > (graphPayload.timeline[graphPayload.timeline.length - 1]?.end_time || 0)) {
        setActiveSubtitle(graphPayload.socratic_challenge || 'Reflect on the governing constraint.');
      }
    }
  };

  const handleAudioEnded = () => {
    setIsPlaying(false);
    setActiveStepId(null);
  };

  const togglePlay = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play().then(() => setIsPlaying(true)).catch((e) => {
        console.warn('Playback error:', e);
      });
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = parseFloat(e.target.value);
    if (audioRef.current) {
      audioRef.current.currentTime = time;
      setCurrentTime(time);
    }
  };

  const cyclePlaybackRate = () => {
    const rates = [1.0, 1.25, 1.5, 0.75];
    const nextRate = rates[(rates.indexOf(playbackRate) + 1) % rates.length];
    setPlaybackRate(nextRate);
    if (audioRef.current) {
      audioRef.current.playbackRate = nextRate;
    }
  };

  // Canvas Pan & Zoom handlers
  const handleWheel = (e: React.WheelEvent) => {
    if (activeTab !== 'graph') return;
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.08 : 0.92;
    setScale((prev) => Math.min(Math.max(prev * zoomFactor, 0.5), 2.5));
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (activeTab !== 'graph') return;
    if ((e.target as HTMLElement).closest('.hud-toolbar') || (e.target as HTMLElement).closest('.node-card') || (e.target as HTMLElement).closest('.transcript-card')) {
      return;
    }
    setIsDragging(true);
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    setPan({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y,
    });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Align and Center Divergence Graph smoothly on spacebar or button
  const alignGraph = useCallback(() => {
    const nodes = divergenceGraph?.nodes || [];
    if (!containerRef.current || nodes.length === 0) {
      setPan({ x: 0, y: 0 });
      setScale(1);
      return;
    }

    const rect = containerRef.current.getBoundingClientRect();
    const containerW = rect.width || 800;
    const containerH = rect.height || 640;

    const nodeWidth = 230;
    const nodeHeight = 110;

    let minX = Infinity;
    let maxX = -Infinity;
    let minY = Infinity;
    let maxY = -Infinity;

    for (const n of nodes) {
      if (n.position.x < minX) minX = n.position.x;
      if (n.position.x + nodeWidth > maxX) maxX = n.position.x + nodeWidth;
      if (n.position.y < minY) minY = n.position.y;
      if (n.position.y + nodeHeight > maxY) maxY = n.position.y + nodeHeight;
    }

    const graphW = maxX - minX;
    const graphH = maxY - minY;

    const paddingX = 40;
    const paddingTop = 70;
    const paddingBottom = 40;

    const scaleX = (containerW - paddingX * 2) / (graphW || 1);
    const scaleY = (containerH - paddingTop - paddingBottom) / (graphH || 1);
    const optimalScale = Math.min(Math.max(Math.min(scaleX, scaleY), 0.55), 1.05);

    const graphCenterX = minX + graphW / 2;
    const graphCenterY = minY + graphH / 2;

    const targetPanX = containerW / 2 - graphCenterX * optimalScale;
    const targetPanY = (containerH + paddingTop - paddingBottom) / 2 - graphCenterY * optimalScale;

    setScale(optimalScale);
    setPan({ x: targetPanX, y: targetPanY });
  }, [divergenceGraph]);

  // Global spacebar listener to align graph
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === 'INPUT' ||
          target.tagName === 'TEXTAREA' ||
          target.isContentEditable)
      ) {
        return;
      }

      if (e.code === 'Space' || e.key === ' ') {
        e.preventDefault();
        if (activeTab !== 'graph') {
          setActiveTab('graph');
        }
        setTimeout(alignGraph, 50);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [alignGraph, activeTab]);

  // Auto align on graph tab switch or graph update
  useEffect(() => {
    if (activeTab === 'graph') {
      alignGraph();
    }
  }, [activeTab, divergenceGraph, alignGraph]);

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  // Chalkboard step navigation
  const boardSteps = boardSolve?.steps || [];
  const activeBoardStep = boardSteps[currentBoardStepIndex] || boardSteps[0];

  const handleNextBoardStep = () => {
    if (currentBoardStepIndex < boardSteps.length - 1) {
      const nextIdx = currentBoardStepIndex + 1;
      setCurrentBoardStepIndex(nextIdx);
      seekToStepAudio(nextIdx);
    }
  };

  const handlePrevBoardStep = () => {
    if (currentBoardStepIndex > 0) {
      const prevIdx = currentBoardStepIndex - 1;
      setCurrentBoardStepIndex(prevIdx);
      seekToStepAudio(prevIdx);
    }
  };

  const seekToStepAudio = (stepIdx: number) => {
    const targetSegment = graphPayload?.timeline?.[stepIdx];
    if (targetSegment && audioRef.current && isPlaying) {
      audioRef.current.currentTime = targetSegment.start_time;
      setCurrentTime(targetSegment.start_time);
    }
  };

  const playStepAudio = (stepIdx: number) => {
    if (!audioRef.current) return;
    const targetSegment = graphPayload?.timeline?.[stepIdx];
    if (targetSegment) {
      audioRef.current.currentTime = targetSegment.start_time;
      setCurrentTime(targetSegment.start_time);
      audioRef.current.play().then(() => setIsPlaying(true)).catch((e) => console.warn('Play error:', e));
    } else {
      audioRef.current.currentTime = 0;
      audioRef.current.play().then(() => setIsPlaying(true)).catch((e) => console.warn('Play error:', e));
    }
  };

  if (isLoading) {
    return (
      <div className="w-full h-[600px] blackboard-grid rounded-2xl border border-zinc-800 shadow-2xl flex flex-col items-center justify-center text-zinc-400 p-8 text-center relative overflow-hidden backdrop-blur-md">
        <div className="relative mb-4">
          <div className="w-16 h-16 rounded-2xl bg-zinc-900/90 border border-emerald-500/40 flex items-center justify-center text-emerald-400 shadow-2xl shadow-emerald-500/10">
            <Sparkles className="w-8 h-8 text-emerald-400 animate-pulse" />
          </div>
          <div className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-emerald-500 animate-ping" />
        </div>
        <h3 className="text-base font-semibold text-zinc-100 mb-1.5 flex items-center gap-2">
          <span>🧹 Chalkboard Erased & Re-Deriving Solution...</span>
        </h3>
        <p className="text-xs text-zinc-400 max-w-md leading-relaxed font-sans mb-3">
          Analyzing your newly provided problem, diagnosing conceptual divergence points, and writing fresh chalk derivations on the board.
        </p>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-zinc-950/80 border border-zinc-800 text-[11px] text-emerald-300 font-mono">
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span>Generating Board Schedule & Divergence Mind Map...</span>
        </div>
      </div>
    );
  }

  if (!graphPayload && !boardSolve) {
    return (
      <div className="w-full h-[600px] blackboard-grid rounded-2xl border border-zinc-800 shadow-2xl flex flex-col items-center justify-center text-zinc-400 p-8 text-center relative overflow-hidden">
        <div className="w-14 h-14 rounded-2xl bg-zinc-900/90 border border-zinc-800 flex items-center justify-center text-emerald-400 mb-3 shadow-xl">
          <RotateCcw className="w-6 h-6 text-zinc-400" />
        </div>
        <h3 className="text-sm font-semibold text-zinc-200 mb-1">
          Chalkboard Clean & Ready
        </h3>
        <p className="text-xs text-zinc-400 max-w-sm leading-relaxed">
          Previous problem erased. Provide your problem statement and click &quot;Analyze Thinking&quot; to begin fresh step-by-step board derivation.
        </p>
      </div>
    );
  }

  const divergenceNodes = divergenceGraph?.nodes || [];
  const divergenceEdges = divergenceGraph?.edges || [];

  return (
    <div
      ref={containerRef}
      onWheel={handleWheel}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      className={`relative w-full h-[640px] bg-[#070A12] blackboard-grid rounded-2xl border border-zinc-800/90 shadow-2xl overflow-hidden select-none transition-all duration-200 ${
        isDragging && activeTab === 'graph' ? 'cursor-grabbing' : ''
      }`}
    >
      {/* Hidden Native Audio Element */}
      <audio
        ref={audioRef}
        onLoadedMetadata={handleLoadedMetadata}
        onTimeUpdate={handleTimeUpdate}
        onEnded={handleAudioEnded}
      />

      {/* Docked Top Glassmorphic Utility Bar */}
      <div className="hud-toolbar absolute top-3 left-3 right-3 z-30 flex items-center justify-between gap-3 px-3 py-2 rounded-xl bg-zinc-900/80 backdrop-blur-xl border border-zinc-800 shadow-xl transition-all duration-200">
        {/* Left: Dual View Mode Switcher */}
        <div className="flex items-center gap-1.5 flex-shrink-0">
          <button
            type="button"
            onClick={() => setActiveTab('board')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold transition-all duration-150 cursor-pointer ${
              activeTab === 'board'
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/60 border border-transparent'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 text-emerald-400" />
            <span>Board</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('graph')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold transition-all duration-150 cursor-pointer ${
              activeTab === 'graph'
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/60 border border-transparent'
            }`}
          >
            <GitBranch className="w-3.5 h-3.5 text-amber-400" />
            <span>Mind Map</span>
          </button>
        </div>

        {/* Center: Audio Controls Bar */}
        <div className="flex items-center gap-2.5 flex-shrink-0">
          <button
            onClick={togglePlay}
            className="w-7 h-7 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-zinc-950 flex items-center justify-center font-bold shadow-[0_0_12px_rgba(16,185,129,0.25)] transition-all duration-150 hover:scale-105 active:scale-95 cursor-pointer"
            title={isPlaying ? 'Pause Socratic Audio' : 'Play Socratic Audio'}
          >
            {isPlaying ? (
              <Pause className="w-3.5 h-3.5 fill-current" />
            ) : (
              <Play className="w-3.5 h-3.5 ml-0.5 fill-current" />
            )}
          </button>

          <div className="hidden md:flex items-center gap-2">
            <span className="font-mono text-xs text-zinc-400 w-8 text-right">
              {formatTime(currentTime)}
            </span>
            <input
              type="range"
              min={0}
              max={duration || 16}
              step={0.1}
              value={currentTime}
              onChange={handleSeek}
              className="w-24 lg:w-32 h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-400"
            />
            <span className="font-mono text-xs text-zinc-500 w-8">
              {formatTime(duration || 16)}
            </span>
          </div>

          <button
            onClick={cyclePlaybackRate}
            className="px-2 py-0.5 rounded-md bg-zinc-950/60 border border-zinc-800 hover:border-zinc-700 text-zinc-300 font-mono text-xs font-medium transition-colors"
            title="Audio Playback Speed"
          >
            {playbackRate}x
          </button>
        </div>

        {/* Right: Topic & Divergence indicator */}
        <div className="flex items-center gap-2">
          <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-zinc-950/70 border border-zinc-800 text-xs font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-zinc-200 font-semibold truncate max-w-[150px]">
              {canonicalTopic}
            </span>
          </div>

          {activeTab === 'graph' && (
            <div className="flex items-center gap-1.5">
              {divergenceGraph?.zoneBMindMap && (
                <button
                  type="button"
                  onClick={() => setShowZoneBTree((prev) => !prev)}
                  className={`flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium transition-colors cursor-pointer ${
                    showZoneBTree
                      ? 'bg-amber-500/20 text-amber-300 border border-amber-500/50 shadow-sm'
                      : 'bg-zinc-950/80 hover:bg-zinc-800 text-zinc-300 border border-zinc-800'
                  }`}
                  title="Toggle Zone B: Mind Map Conceptual Hierarchy"
                >
                  <Network className="w-3.5 h-3.5 text-amber-400" />
                  <span className="hidden sm:inline">Zone B Tree</span>
                </button>
              )}

              <button
                onClick={alignGraph}
                className="flex items-center gap-1 px-2 py-1 rounded-md bg-zinc-950/80 hover:bg-zinc-800 text-emerald-400 border border-emerald-500/30 text-[11px] font-medium transition-colors cursor-pointer"
                title="Align & Center Graph (Spacebar)"
              >
                <Crosshair className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Center (Space)</span>
              </button>

              <button
                onClick={() => setScale((s) => Math.min(s + 0.15, 2.5))}
                className="p-1 rounded-md bg-zinc-950/60 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/80 border border-zinc-800 transition-colors cursor-pointer"
                title="Zoom In"
              >
                <ZoomIn className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setScale((s) => Math.max(s - 0.15, 0.5))}
                className="p-1 rounded-md bg-zinc-950/60 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/80 border border-zinc-800 transition-colors cursor-pointer"
                title="Zoom Out"
              >
                <ZoomOut className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => {
                  setScale(1);
                  setPan({ x: 0, y: 0 });
                }}
                className="px-1.5 py-0.5 rounded-md bg-zinc-950/60 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/80 border border-zinc-800 font-mono text-[10px] font-medium transition-colors cursor-pointer"
                title="Reset Zoom (100%)"
              >
                100%
              </button>
            </div>
          )}
        </div>
      </div>

      {/* ========================================================================= */}
      {/* TAB 1: DIGITAL TEACHER CHALKBOARD DERIVATION VIEW */}
      {/* ========================================================================= */}
      {activeTab === 'board' && activeBoardStep && (
        <div className="absolute inset-0 pt-14 pb-3 px-3 sm:px-6 flex flex-col items-center justify-center overflow-hidden">
          {/* Slate Board Container with Chalkboard Framing (strictly bounded within container) */}
          <div className="w-full max-w-2xl max-h-[520px] bg-[#090E1A]/95 border border-zinc-800/90 rounded-2xl p-4 sm:p-5 shadow-2xl relative flex flex-col justify-between overflow-hidden backdrop-blur-xl">
            {/* Top Chalk Label */}
            <div className="flex items-center justify-between pb-2 mb-1 border-b border-zinc-800/80 flex-shrink-0">
              <div className="flex items-center gap-2 truncate">
                <span className="w-2 h-2 rounded-full bg-emerald-400 flex-shrink-0" />
                <span className="text-xs text-emerald-400 font-semibold font-mono truncate">
                  {activeBoardStep.title.replace(/^Step \d+:\s*/i, '')}
                </span>
              </div>

              {activeBoardStep.annotation && (
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-amber-300 max-w-[220px] truncate flex-shrink-0 ml-2">
                  {activeBoardStep.annotation}
                </span>
              )}
            </div>

            {/* Blackboard KaTeX Math Rendering with Chalk Typography (strictly bounded) */}
            <div className="my-2 py-2.5 px-3 rounded-xl bg-zinc-950/70 border border-zinc-800/60 text-zinc-100 shadow-inner flex items-center justify-center min-h-[90px] max-h-[220px] max-w-full overflow-x-auto overflow-y-auto flex-1">
              <div className="text-base sm:text-xl text-emerald-300 font-serif leading-normal animate-in fade-in duration-300 max-w-full overflow-x-auto text-center px-1">
                <MathRenderer math={activeBoardStep.latexContent} displayMode={true} />
              </div>
            </div>

            {/* Synchronized Vernacular Spoken Script Banner with Speak Step Button */}
            <div className="p-2.5 rounded-xl bg-zinc-950/50 border border-zinc-800 text-xs text-zinc-300 flex items-center justify-between gap-2 leading-relaxed font-sans max-h-20 flex-shrink-0">
              <div className="flex items-start gap-2 overflow-y-auto flex-1">
                <Volume2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
                <p className="line-clamp-3 text-[11px]">
                  <b className="text-zinc-200 font-semibold">Teacher Narration ({outputLang.split(' ')[0]}): </b>
                  {activeBoardStep.speechScript}
                </p>
              </div>

              <button
                type="button"
                onClick={() => playStepAudio(currentBoardStepIndex)}
                className="px-2.5 py-1 rounded-md bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/30 text-emerald-300 text-[10px] font-semibold flex items-center gap-1 flex-shrink-0 transition-colors cursor-pointer"
                title="Play teacher narration for this step"
              >
                <Play className="w-3 h-3 fill-current" />
                <span>Play Step</span>
              </button>
            </div>

            {/* Navigation Controls along Board Bottom */}
            <div className="flex items-center justify-between pt-2.5 mt-2 border-t border-zinc-800/80 flex-shrink-0">
              <button
                type="button"
                onClick={handlePrevBoardStep}
                disabled={currentBoardStepIndex === 0}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  currentBoardStepIndex === 0
                    ? 'text-zinc-600 bg-zinc-900/40 border border-zinc-900 cursor-not-allowed'
                    : 'text-zinc-300 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 hover:text-white cursor-pointer'
                }`}
              >
                <ChevronLeft className="w-3.5 h-3.5" />
                <span>Previous</span>
              </button>

              {/* Progress Indicator Dots */}
              <div className="flex items-center gap-1.5">
                {boardSteps.map((s, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setCurrentBoardStepIndex(idx);
                      seekToStepAudio(idx);
                    }}
                    className={`h-2 rounded-full transition-all ${
                      idx === currentBoardStepIndex
                        ? 'w-6 bg-emerald-400 shadow-[0_0_8px_#34d399]'
                        : 'w-2 bg-zinc-800 hover:bg-zinc-700'
                    }`}
                    title={s.title}
                  />
                ))}
              </div>

              <button
                type="button"
                onClick={handleNextBoardStep}
                disabled={currentBoardStepIndex === boardSteps.length - 1}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  currentBoardStepIndex === boardSteps.length - 1
                    ? 'text-zinc-600 bg-zinc-900/40 border border-zinc-900 cursor-not-allowed'
                    : 'text-zinc-300 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 hover:text-white cursor-pointer'
                }`}
              >
                <span>Next</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 2: DIVERGENCE & REASONING GRAPH ENGINE VIEW */}
      {/* ========================================================================= */}
      {activeTab === 'graph' && (
        <div
          className="absolute inset-0 origin-top-left transition-transform duration-75 cursor-grab active:cursor-grabbing"
          style={{
            transform: `translate(${pan.x}px, ${pan.y}px) scale(${scale})`,
          }}
        >
          {/* SVG Connectors */}
          <svg className="w-[1800px] h-[900px] pointer-events-none overflow-visible">
            <defs>
              <marker
                id="arrowEmerald"
                viewBox="0 0 10 10"
                refX="8"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path d="M 0 1 L 9 5 L 0 9 z" fill="#10B981" />
              </marker>
              <marker
                id="arrowCrimson"
                viewBox="0 0 10 10"
                refX="8"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path d="M 0 1 L 9 5 L 0 9 z" fill="#EF4444" />
              </marker>
              <marker
                id="arrowCyan"
                viewBox="0 0 10 10"
                refX="8"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path d="M 0 1 L 9 5 L 0 9 z" fill="#06B6D4" />
              </marker>
              <marker
                id="arrowViolet"
                viewBox="0 0 10 10"
                refX="8"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path d="M 0 1 L 9 5 L 0 9 z" fill="#8B5CF6" />
              </marker>
            </defs>

            {/* Render Divergence Edges */}
            {divergenceEdges.map((edge) => {
              const srcNode = divergenceNodes.find((n) => n.id === edge.source);
              const tgtNode = divergenceNodes.find((n) => n.id === edge.target);
              if (!srcNode || !tgtNode) return null;

              const x1 = srcNode.position.x + 110;
              const y1 = srcNode.position.y + 40;
              const x2 = tgtNode.position.x;
              const y2 = tgtNode.position.y + 40;
              const dx = Math.abs(x2 - x1) * 0.5;
              const pathD = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;

              let stroke = '#10B981';
              let marker = 'url(#arrowEmerald)';
              let isDerailed = edge.status === 'derailed';

              if (isDerailed) {
                stroke = '#EF4444';
                marker = 'url(#arrowCrimson)';
              } else if (edge.status === 'scaffold') {
                stroke = '#06B6D4';
                marker = 'url(#arrowCyan)';
              }

              return (
                <g key={edge.id}>
                  <path
                    d={pathD}
                    fill="none"
                    stroke={stroke}
                    strokeWidth={2.5}
                    strokeDasharray={isDerailed ? '6 6' : 'none'}
                    markerEnd={marker}
                    className={`transition-all duration-300 ${isDerailed ? 'animate-dash-travel' : ''}`}
                  />
                  {edge.label && (
                    <foreignObject
                      x={(x1 + x2) / 2 - 55}
                      y={(y1 + y2) / 2 - 12}
                      width={120}
                      height={28}
                    >
                      <div
                        className={`text-[9px] font-semibold px-2 py-0.5 rounded-full text-center border backdrop-blur-md shadow-md ${
                          isDerailed
                            ? 'bg-red-950/80 text-red-300 border-red-500/30'
                            : 'bg-emerald-950/80 text-emerald-300 border-emerald-500/30'
                        }`}
                      >
                        {edge.label}
                      </div>
                    </foreignObject>
                  )}
                </g>
              );
            })}
          </svg>

          {/* Render Divergence Nodes */}
          <div className="absolute inset-0 pointer-events-auto">
            {divergenceNodes.map((node) => {
              let borderStyle = 'border-emerald-500/40 bg-zinc-900/85';
              let badgeBg = 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30';
              let glowClass = 'glow-emerald';

              if (node.type === 'CRITICAL_PIVOT') {
                borderStyle = 'border-amber-500/50 bg-zinc-900/90';
                badgeBg = 'bg-amber-500/15 text-amber-300 border-amber-500/40';
                glowClass = 'glow-amber';
              } else if (node.type === 'DERAILED_BRANCH') {
                borderStyle = 'border-red-500/50 border-dashed bg-zinc-900/85';
                badgeBg = 'bg-red-500/15 text-red-300 border-red-500/30';
                glowClass = 'glow-crimson';
              } else if (node.type === 'CANONICAL_PATH') {
                borderStyle = 'border-cyan-500/40 bg-zinc-900/85';
                badgeBg = 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30';
                glowClass = '';
              } else if (node.type === 'SOCRATIC_CHECKPOINT') {
                borderStyle = 'border-violet-500/40 bg-zinc-900/85';
                badgeBg = 'bg-violet-500/15 text-violet-300 border-violet-500/30';
                glowClass = 'glow-violet';
              }

              return (
                <div
                  key={node.id}
                  onClick={() => setSelectedNode(node)}
                  style={{
                    left: `${node.position.x}px`,
                    top: `${node.position.y}px`,
                    width: '240px',
                    minHeight: '90px',
                  }}
                  className={`node-card absolute p-3 rounded-xl border backdrop-blur-md shadow-xl transition-all duration-200 ease-out cursor-pointer hover:scale-[1.02] active:scale-[0.99] overflow-hidden ${borderStyle} ${glowClass}`}
                >
                  <div className="flex items-center justify-between gap-1 mb-1.5">
                    <span className={`text-[9px] font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded-md border truncate ${badgeBg}`}>
                      {node.badge || node.type}
                    </span>
                    {node.type === 'CRITICAL_PIVOT' && (
                      <Lightbulb className="w-3.5 h-3.5 text-amber-400 animate-pulse flex-shrink-0" />
                    )}
                    {node.type === 'DERAILED_BRANCH' && (
                      <AlertTriangle className="w-3.5 h-3.5 text-red-400 flex-shrink-0" />
                    )}
                    {node.type === 'SOCRATIC_CHECKPOINT' && (
                      <Sparkles className="w-3.5 h-3.5 text-violet-400 flex-shrink-0" />
                    )}
                  </div>

                  <h4 className="text-xs font-semibold text-zinc-100 leading-snug line-clamp-2 mb-1">
                    {node.label}
                  </h4>

                  {node.mathLatex && (
                    <div className="my-1 text-emerald-300 text-xs overflow-x-auto max-w-full scrollbar-none">
                      <MathRenderer math={node.mathLatex} />
                    </div>
                  )}

                  <p className="text-[11px] text-zinc-400 line-clamp-2 leading-relaxed font-sans overflow-hidden break-words">
                    {node.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Docked Frosted-Glass Live Transcript Card / Drawer (Graph Mode Only) */}
      {activeTab === 'graph' && (
        <div className="transcript-card absolute bottom-3 left-4 right-4 z-20 pointer-events-none transition-all duration-200">
          <div className="mx-auto max-w-2xl px-3.5 py-2.5 rounded-xl bg-zinc-900/85 backdrop-blur-md border border-zinc-700/50 shadow-2xl text-zinc-200 pointer-events-auto transition-all duration-200">
            <div className="flex items-center justify-between gap-2.5">
              <div className="flex items-center gap-2 flex-shrink-0">
                <div className="w-6 h-6 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 flex items-center justify-center">
                  <Radio className={`w-3.5 h-3.5 ${isPlaying ? 'animate-pulse' : ''}`} />
                </div>
                <span className="text-[10px] font-semibold uppercase tracking-wider text-emerald-400">
                  Sarvam Voice
                </span>
              </div>

              <p className="text-xs font-normal text-zinc-300 truncate max-w-[340px] sm:max-w-[460px] leading-snug">
                {activeSubtitle || (boardSolve?.problemSummary ? `Derivation: ${boardSolve.problemSummary}` : 'Listening for audio playback...')}
              </p>

              <button
                onClick={() => setShowFullTranscript((prev) => !prev)}
                className="p-1 rounded text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/80 transition-colors"
                title={showFullTranscript ? 'Collapse Transcript' : 'Expand Full Transcript'}
              >
                {showFullTranscript ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronUp className="w-3.5 h-3.5" />}
              </button>
            </div>

            {showFullTranscript && (
              <div className="mt-2.5 pt-2.5 border-t border-zinc-800 max-h-32 overflow-y-auto pr-1">
                <p className="text-xs text-zinc-300 leading-relaxed font-sans">
                  {graphPayload?.full_spoken_transcript || boardSolve?.steps.map((s) => s.speechScript).join(' ') || ''}
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Node Detail Inspector Popover (for Graph nodes) */}
      {selectedNode && (
        <div className="absolute top-16 right-4 z-40 w-80 bg-zinc-950/95 backdrop-blur-xl border border-zinc-800 rounded-xl p-4 shadow-2xl text-zinc-200 transition-all duration-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-emerald-400">
              {selectedNode.badge || (selectedNode as any).type}
            </span>
            <button
              onClick={() => setSelectedNode(null)}
              className="p-1 rounded-md text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <h3 className="text-sm font-semibold text-zinc-100 mb-2 leading-snug">
            {(selectedNode as any).label || (selectedNode as any).title}
          </h3>
          {(selectedNode as any).mathLatex && (
            <div className="p-2 mb-2 rounded bg-zinc-900 border border-zinc-800 text-emerald-300 text-xs">
              <MathRenderer math={(selectedNode as any).mathLatex} displayMode={true} />
            </div>
          )}
          <p className="text-xs text-zinc-300 leading-relaxed mb-3 font-sans">
            {(selectedNode as any).description || (selectedNode as any).detail}
          </p>
          {(selectedNode as any).misconceptionDetails && (
            <div className="p-2.5 rounded-lg bg-amber-950/30 border border-amber-500/30 text-xs text-amber-200 space-y-1">
              <span className="font-semibold block text-[11px] text-amber-300 uppercase">
                Diagnostic Flaw:
              </span>
              <p className="text-[11px]">{(selectedNode as any).misconceptionDetails.identifiedFlaw}</p>
              <span className="font-semibold block text-[11px] text-emerald-300 uppercase pt-1">
                Correction Hint:
              </span>
              <p className="text-[11px] text-emerald-200">{(selectedNode as any).misconceptionDetails.correctionHint}</p>
            </div>
          )}
        </div>
      )}

      {/* Zone B: Mind Map Conceptual Hierarchy Overlay (Graph Tab) */}
      {activeTab === 'graph' && divergenceGraph?.zoneBMindMap && showZoneBTree && (
        <div className="absolute top-16 left-4 z-40 w-80 sm:w-96 bg-zinc-950/95 backdrop-blur-xl border border-amber-500/40 rounded-xl p-4 shadow-2xl text-zinc-200 transition-all duration-200 animate-in fade-in">
          <div className="flex items-center justify-between pb-2 mb-3 border-b border-zinc-800">
            <div className="flex items-center gap-1.5">
              <Network className="w-4 h-4 text-amber-400" />
              <span className="text-xs font-semibold text-amber-300 uppercase tracking-wider">
                Zone B: Mind Map Hierarchy
              </span>
            </div>
            <button
              onClick={() => setShowZoneBTree(false)}
              className="p-1 rounded-md text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 transition-colors cursor-pointer"
              title="Close Zone B Hierarchy"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="space-y-2.5 text-xs">
            {/* Root Node */}
            <div className="p-2.5 rounded-lg bg-amber-950/30 border border-amber-500/30">
              <span className="text-[10px] font-mono text-amber-400 block font-semibold uppercase">
                Root Node (Core Topic)
              </span>
              <p className="text-zinc-100 font-semibold text-xs mt-0.5">
                {divergenceGraph.zoneBMindMap.root_topic}
              </p>
            </div>

            {/* Branch 1 */}
            <div className="p-2.5 rounded-lg bg-emerald-950/30 border border-emerald-500/30">
              <span className="text-[10px] font-mono text-emerald-400 block font-semibold uppercase">
                Branch 1: Givens / Visual Inputs
              </span>
              <p className="text-zinc-200 text-[11px] mt-0.5 leading-relaxed font-sans">
                {divergenceGraph.zoneBMindMap.branch_1_givens}
              </p>
            </div>

            {/* Branch 2 */}
            <div className="p-2.5 rounded-lg bg-cyan-950/30 border border-cyan-500/30">
              <span className="text-[10px] font-mono text-cyan-400 block font-semibold uppercase">
                Branch 2: Interim Formulas & Connections
              </span>
              <p className="text-zinc-200 text-[11px] mt-0.5 leading-relaxed font-sans">
                {divergenceGraph.zoneBMindMap.branch_2_interim}
              </p>
            </div>

            {/* Branch 3 */}
            <div className="p-2.5 rounded-lg bg-violet-950/30 border border-violet-500/30">
              <span className="text-[10px] font-mono text-violet-400 block font-semibold uppercase">
                Branch 3: Final Evaluation Target
              </span>
              <p className="text-zinc-100 text-[11px] mt-0.5 leading-relaxed font-sans font-medium">
                {divergenceGraph.zoneBMindMap.branch_3_target}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
