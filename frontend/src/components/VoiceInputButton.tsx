import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Loader2, Radio } from 'lucide-react';
import { transcribeStudentVoice } from '../services/api';

interface VoiceInputButtonProps {
  onTranscriptionComplete: (text: string) => void;
  languageCode?: string;
  className?: string;
  title?: string;
}

export const VoiceInputButton: React.FC<VoiceInputButtonProps> = ({
  onTranscriptionComplete,
  languageCode = 'unknown',
  className = '',
  title = 'Speak your doubt in Indic or Hinglish',
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [recordSeconds, setRecordSeconds] = useState(0);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerIntervalRef = useRef<any>(null);

  useEffect(() => {
    return () => {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
    };
  }, []);

  const startRecording = async () => {
    audioChunksRef.current = [];
    setRecordSeconds(0);

    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Microphone access is not supported in this browser.');
        return;
      }

      // Enhanced audio capture constraints for crisp speech separation
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      // Probe browser supported audio container/codecs
      let selectedMimeType = '';
      const candidateMimeTypes = [
        'audio/webm;codecs=opus',
        'audio/webm',
        'audio/ogg;codecs=opus',
        'audio/mp4',
      ];
      for (const mt of candidateMimeTypes) {
        if (typeof MediaRecorder !== 'undefined' && MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(mt)) {
          selectedMimeType = mt;
          break;
        }
      }

      const recorderOptions = selectedMimeType ? { mimeType: selectedMimeType } : undefined;
      const mediaRecorder = recorderOptions ? new MediaRecorder(stream, recorderOptions) : new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        const totalBytes = audioChunksRef.current.reduce((acc, chunk) => acc + chunk.size, 0);
        if (totalBytes < 500) {
          alert('Recording was too short or empty. Please speak clearly into your microphone.');
          return;
        }
        const rawMime = mediaRecorder.mimeType || selectedMimeType || 'audio/webm';
        // Strip codec parameters (e.g. 'audio/webm;codecs=opus' -> 'audio/webm') for API compliance
        const cleanMime = rawMime.split(';')[0].trim().toLowerCase() || 'audio/webm';
        const audioBlob = new Blob(audioChunksRef.current, { type: cleanMime });
        await handleTranscribe(audioBlob);
      };

      mediaRecorder.start(200);
      setIsRecording(true);

      timerIntervalRef.current = setInterval(() => {
        setRecordSeconds((s) => s + 1);
      }, 1000);
    } catch (err: any) {
      console.warn('Microphone permission or hardware error:', err);
      alert('Could not access microphone: ' + (err.message || 'Permission denied'));
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    if (timerIntervalRef.current) {
      clearInterval(timerIntervalRef.current);
    }
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    setIsRecording(false);
  };

  const handleTranscribe = async (blob: Blob) => {
    setIsTranscribing(true);
    try {
      const res = await transcribeStudentVoice(blob, languageCode);
      if (res.text) {
        onTranscriptionComplete(res.text);
      } else if (res.statusMsg) {
        alert(res.statusMsg);
      }
    } catch (err: any) {
      console.warn('Transcription error:', err);
      alert('Voice transcription error: ' + (err?.message || 'Failed to transcribe audio.'));
    } finally {
      setIsTranscribing(false);
    }
  };

  const formatTimer = (sec: number) => {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  if (isTranscribing) {
    return (
      <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-zinc-900 border border-zinc-800 text-zinc-300 text-xs font-medium">
        <Loader2 className="w-3.5 h-3.5 animate-spin text-emerald-400" />
        <span className="text-[11px]">Transcribing voice...</span>
      </div>
    );
  }

  if (isRecording) {
    return (
      <button
        type="button"
        onClick={stopRecording}
        className="flex items-center gap-2 px-2.5 py-1 rounded-lg bg-red-950/80 hover:bg-red-900/90 border border-red-500/40 text-red-300 text-xs font-semibold animate-pulse transition-all shadow-md"
        title="Click to stop recording and transcribe"
      >
        <span className="w-2 h-2 rounded-full bg-red-400 animate-ping" />
        <Square className="w-3 h-3 fill-current" />
        <span className="font-mono text-[11px]">{formatTimer(recordSeconds)}</span>
        <span className="text-[11px] hidden sm:inline">Done</span>
      </button>
    );
  }

  return (
    <button
      type="button"
      onClick={startRecording}
      className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-zinc-900/70 hover:bg-zinc-800 border border-zinc-800 hover:border-zinc-700 text-zinc-300 hover:text-white text-xs font-medium transition-all duration-150 cursor-pointer ${className}`}
      title={title}
    >
      <Mic className="w-3.5 h-3.5 text-emerald-400" />
      <span className="text-[11px] hidden sm:inline">Voice Input</span>
    </button>
  );
};
