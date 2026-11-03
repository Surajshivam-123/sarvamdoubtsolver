/**
 * Sarvam AI REST Client (Pure Client-Side Browser Implementation)
 * Direct integration with Sarvam AI Text-to-Speech & Translation APIs.
 */

export const SARVAM_TTS_URL = 'https://api.sarvam.ai/text-to-speech';
export const SARVAM_TRANSLATE_URL = 'https://api.sarvam.ai/translate';
export const SARVAM_ASR_URL = 'https://api.sarvam.ai/speech-to-text';

export interface LanguageConfig {
  code: string;
  speaker: string;
  name: string;
  mode?: string;
}

export const LANGUAGE_REGISTRY: Record<string, LanguageConfig> = {
  'English': { code: 'en-IN', speaker: 'simran', name: 'English (Indian)' },
  'Hindi (हिंदी)': { code: 'hi-IN', speaker: 'aditya', name: 'Hindi (हिंदी)', mode: 'hindi' },
  'Hinglish (हिंग्लिश)': { code: 'hi-IN', speaker: 'ritu', name: 'Hinglish (हिंग्लिश)', mode: 'hinglish' },
  'Bengali (বাংলা)': { code: 'bn-IN', speaker: 'roopa', name: 'Bengali (বাংলা)' },
  'Marathi (मराठी)': { code: 'mr-IN', speaker: 'soham', name: 'Marathi (मराठी)' },
  'Tamil (தமிழ்)': { code: 'ta-IN', speaker: 'gokul', name: 'Tamil (தமிழ்)' },
  'Telugu (తెలుగు)': { code: 'te-IN', speaker: 'kavitha', name: 'Telugu (తెలుగు)' },
  'Gujarati (ગુજરાતી)': { code: 'gu-IN', speaker: 'pooja', name: 'Gujarati (ગુજરાતી)' },
  'Kannada (ಕನ್ನಡ)': { code: 'kn-IN', speaker: 'chaitra', name: 'Kannada (ಕನ್ನಡ)' },
  'Malayalam (മലയാളം)': { code: 'ml-IN', speaker: 'gokul', name: 'Malayalam (മലയാളം)' },
  'Punjabi (ਪੰਜਾਬੀ)': { code: 'pa-IN', speaker: 'anand', name: 'Punjabi (ਪੰਜਾਬੀ)' },
};

export const SPEAKER_ALIASES: Record<string, string> = {
  meera: 'ritu',
  arvind: 'aditya',
  amol: 'soham',
  amartya: 'roopa',
  pavithra: 'gokul',
};

export const MODEL_OPTIONS = ['bulbul:v3', 'bulbul:v4-flash', 'bulbul:v1'];

export const ALL_SPEAKERS = [
  'ritu', 'aditya', 'simran', 'soham', 'roopa', 'gokul', 'kavitha', 'pooja', 'chaitra', 'anand', 'priya'
];

declare const __SARVAM_API_KEY__: string | undefined;

export function getStoredApiKey(): string {
  // 1. Injected from .env via Vite define / import.meta.env
  let envKey = '';
  try {
    if (typeof __SARVAM_API_KEY__ !== 'undefined' && __SARVAM_API_KEY__) {
      envKey = __SARVAM_API_KEY__;
    } else if (typeof import.meta !== 'undefined' && (import.meta as any).env) {
      envKey =
        (import.meta as any).env.VITE_SARVAM_API_KEY ||
        (import.meta as any).env.SARVAM_API_KEY ||
        '';
    } else {
      const g = globalThis as any;
      if (g && g.process && g.process.env) {
        envKey = g.process.env.SARVAM_API_KEY || '';
      }
    }
  } catch {}

  if (envKey && envKey.trim()) {
    return envKey.trim();
  }

  // 2. Default workspace .env key fallback
  const hardcodedEnvFallback = 'sk_0vr9gnzo_1deURIBWS66KDr30XVDBOmBw';

  // 3. localStorage override (if user modified in settings)
  try {
    const local = localStorage.getItem('sansay_sarvam_api_key');
    if (local && local.trim()) return local.trim();
  } catch {}

  return hardcodedEnvFallback;
}

export function saveStoredApiKey(key: string): void {
  try {
    localStorage.setItem('sansay_sarvam_api_key', key.trim());
  } catch {}
}

export function sanitizeLatexForSpeech(text: string): string {
  let clean = text
    .replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, '$1 divided by $2')
    .replace(/\\boxed\{([^}]+)\}/g, 'Answer: $1')
    .replace(/\\implies/g, ' implies ')
    .replace(/\\approx/g, ' is approximately ')
    .replace(/\\neq/g, ' is not equal to ')
    .replace(/\\cdot/g, ' times ')
    .replace(/\\times/g, ' times ')
    .replace(/\\sqrt\{([^}]+)\}/g, 'square root of $1')
    .replace(/\^2/g, ' squared')
    .replace(/\^3/g, ' cubed')
    .replace(/\^([a-zA-Z0-9]+)/g, ' to the power $1')
    .replace(/_/g, ' ')
    .replace(/\\Delta/g, 'delta')
    .replace(/\\theta/g, 'theta')
    .replace(/\\omega/g, 'omega')
    .replace(/\\alpha/g, 'alpha')
    .replace(/\\mu/g, 'mu')
    .replace(/\\pi/g, 'pi')
    .replace(/\\lambda/g, 'lambda')
    .replace(/\\rho/g, 'rho')
    .replace(/\\sigma/g, 'sigma')
    .replace(/\\epsilon/g, 'epsilon')
    .replace(/\+/g, ' plus ')
    .replace(/-(?!\w)/g, ' minus ')
    .replace(/=/g, ' equals ')
    .replace(/>=/g, ' is greater than or equal to ')
    .replace(/<=/g, ' is less than or equal to ')
    .replace(/>/g, ' is greater than ')
    .replace(/</g, ' is less than ')
    .replace(/\*/g, ' times ')
    .replace(/%/g, ' percent')
    .replace(/\$/g, '')
    .replace(/\\[a-zA-Z]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  return clean;
}

export function applyHinglishGlossary(text: string): string {
  const replacements: [string, string][] = [
    ['यांत्रिक ऊर्जा', 'mechanical energy'],
    ['गतिज ऊर्जा', 'kinetic energy'],
    ['स्थितिज ऊर्जा', 'potential energy'],
    ['ऊर्जा संरक्षण', 'energy conservation'],
    ['संरक्षित', 'conserved'],
    ['घर्षण बल', 'friction force'],
    ['घर्षण', 'friction'],
    ['संपीड़न', 'spring compression'],
    ['मुक्त पिंड आरेख', 'Free Body Diagram'],
    ['क्रिया और प्रतिक्रिया', 'action-reaction'],
    ['परिणामी बल', 'net force'],
    ['अभिकेंद्री त्वरण', 'centripetal acceleration'],
    ['अपकेंद्री बल', 'centrifugal force'],
    ['कोणीय संवेग', 'angular momentum'],
    ['जड़त्व आघूर्ण', 'moment of inertia'],
    ['प्रत्यानयन बल', 'restoring force'],
    ['त्वरण', 'acceleration'],
    ['वेग', 'velocity'],
  ];

  let result = text;
  for (const [hindi, hinglish] of replacements) {
    result = result.split(hindi).join(hinglish);
  }
  return result;
}

/**
 * Generates an acoustic harmonic WAV audio string (base64) entirely in client-side JS.
 * Ensures the audio player and walkthrough are 100% functional without an API key or when offline.
 */
export function generateFallbackAudioBase64(): string {
  const sampleRate = 22050;
  const durationPerTone = 0.35;
  const frequencies = [440.0, 554.37, 659.25, 880.0]; // A-major harmonic arpeggio
  const totalSamples = Math.floor(sampleRate * durationPerTone * frequencies.length);
  const buffer = new ArrayBuffer(44 + totalSamples * 2);
  const view = new DataView(buffer);

  // RIFF Chunk Descriptor
  writeString(view, 0, 'RIFF');
  view.setUint32(4, 36 + totalSamples * 2, true);
  writeString(view, 8, 'WAVE');

  // "fmt " Sub-chunk
  writeString(view, 12, 'fmt ');
  view.setUint32(16, 16, true); // Subchunk1Size (16 for PCM)
  view.setUint16(20, 1, true); // AudioFormat (1 = PCM)
  view.setUint16(22, 1, true); // NumChannels (1 = Mono)
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true); // ByteRate (SampleRate * NumChannels * BitsPerSample/8)
  view.setUint16(32, 2, true); // BlockAlign
  view.setUint16(34, 16, true); // BitsPerSample (16 bits)

  // "data" Sub-chunk
  writeString(view, 36, 'data');
  view.setUint32(40, totalSamples * 2, true);

  // PCM Sample generation
  let offset = 44;
  for (const freq of frequencies) {
    const numSamples = Math.floor(sampleRate * durationPerTone);
    for (let i = 0; i < numSamples; i++) {
      const t = i / sampleRate;
      const envelope = Math.exp(-3.0 * (i / numSamples));
      const val = envelope * (0.6 * Math.sin(2 * Math.PI * freq * t) + 0.4 * Math.sin(4 * Math.PI * freq * t));
      const sample = Math.max(-32768, Math.min(32767, Math.floor(val * 32767 * 0.5)));
      view.setInt16(offset, sample, true);
      offset += 2;
    }
  }

  // Convert buffer to base64
  let binary = '';
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

function writeString(view: DataView, offset: number, string: string): void {
  for (let i = 0; i < string.length; i++) {
    view.setUint8(offset + i, string.charCodeAt(i));
  }
}

export function concatenateWavBase64(base64Audios: string[]): string {
  if (base64Audios.length === 0) return '';
  if (base64Audios.length === 1) return base64Audios[0];

  const buffers: Uint8Array[] = [];
  let totalDataLength = 0;
  let header: Uint8Array | null = null;

  for (const b64 of base64Audios) {
    try {
      const binary = atob(b64);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
      }

      if (bytes.length > 44) {
        if (!header) {
          header = bytes.slice(0, 44);
        }
        const dataPart = bytes.slice(44);
        buffers.push(dataPart);
        totalDataLength += dataPart.length;
      }
    } catch (e) {
      console.warn('Error decoding WAV chunk:', e);
    }
  }

  if (!header || buffers.length === 0) return base64Audios[0];

  const combined = new Uint8Array(44 + totalDataLength);
  combined.set(header, 0);

  // Update WAV ChunkSize at byte 4 (totalDataLength + 36)
  const view = new DataView(combined.buffer);
  view.setUint32(4, 36 + totalDataLength, true);
  // Update WAV Subchunk2Size at byte 40 (totalDataLength)
  view.setUint32(40, totalDataLength, true);

  let offset = 44;
  for (const buf of buffers) {
    combined.set(buf, offset);
    offset += buf.length;
  }

  let resultBinary = '';
  const batchSize = 8192;
  for (let i = 0; i < combined.length; i += batchSize) {
    resultBinary += String.fromCharCode(...combined.subarray(i, i + batchSize));
  }
  return btoa(resultBinary);
}

export function splitIntoAudioChunks(text: string, maxLen: number = 380): string[] {
  if (!text) return [];
  const clean = sanitizeLatexForSpeech(text);
  if (clean.length <= maxLen) return [clean];

  // Tokenize by sentence ends (. ! ? । ; or newline)
  const tokens = clean.split(/(?<=[.!?।;\n])\s+/);
  const chunks: string[] = [];
  let current = '';

  for (const token of tokens) {
    if (token.length > maxLen) {
      if (current.trim()) {
        chunks.push(current.trim());
        current = '';
      }
      const words = token.split(/\s+/);
      let sub = '';
      for (const w of words) {
        if ((sub + ' ' + w).length <= maxLen) {
          sub = (sub + ' ' + w).trim();
        } else {
          if (sub.trim()) chunks.push(sub.trim());
          sub = w;
        }
      }
      if (sub.trim()) current = sub.trim();
      continue;
    }

    if ((current + ' ' + token).length <= maxLen) {
      current = (current + ' ' + token).trim();
    } else {
      if (current.trim()) chunks.push(current.trim());
      current = token.trim();
    }
  }
  if (current.trim()) chunks.push(current.trim());
  return chunks.slice(0, 5);
}

/**
 * Direct Client-Side Sarvam AI Text-to-Speech synthesis with multi-sentence masterclass chunking.
 */
export async function synthesizeSpeechSarvam(
  text: string,
  targetLanguageCode: string = 'hi-IN',
  speaker: string = 'ritu',
  model: string = 'bulbul:v3',
  apiKey?: string
): Promise<{ audioBase64: string; statusMsg: string; isReal: boolean }> {
  const effectiveKey = (apiKey && apiKey.trim()) || getStoredApiKey();

  if (!effectiveKey) {
    const fallback = generateFallbackAudioBase64();
    return {
      audioBase64: fallback,
      statusMsg: 'ℹ Acoustic Wave Synthesizer active. Add your Sarvam API Key in Settings for live Indian language bulbul voice narration.',
      isReal: false,
    };
  }

  const cleanText = sanitizeLatexForSpeech(text);
  const chunks = splitIntoAudioChunks(cleanText, 420);
  const normalizedSpeaker = SPEAKER_ALIASES[speaker.toLowerCase()] || speaker.toLowerCase();

  try {
    const res = await fetch(SARVAM_TTS_URL, {
      method: 'POST',
      headers: {
        'api-subscription-key': effectiveKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        inputs: chunks,
        target_language_code: targetLanguageCode,
        speaker: normalizedSpeaker,
        model: model,
      }),
    });

    if (res.ok) {
      const data = await res.json();
      if (data.audios && data.audios.length > 0) {
        const unifiedAudio = concatenateWavBase64(data.audios);
        return {
          audioBase64: unifiedAudio,
          statusMsg: `✓ Sarvam AI Audio Synthesized (${targetLanguageCode}, ${normalizedSpeaker}) • ${chunks.length} segments joined`,
          isReal: true,
        };
      }
    } else {
      const err = await res.json().catch(() => ({}));
      console.warn('Sarvam API response error:', err);
    }
  } catch (err) {
    console.warn('Sarvam API fetch failed, falling back to harmonic synthesizer:', err);
  }

  // Graceful harmonic fallback if API returns error or is unreachable
  return {
    audioBase64: generateFallbackAudioBase64(),
    statusMsg: '⚠️ Sarvam API error or rate limit. Rendered harmonic wave fallback.',
    isReal: false,
  };
}

/**
 * Speech-to-Text via Sarvam Saaras ASR API
 * Transcribes student voice input across Indic languages, English, and mixed code-switched Hinglish.
 */
export async function transcribeAudioSarvam(
  audioBlob: Blob,
  targetLanguageCode: string = 'unknown',
  apiKey?: string
): Promise<{ text: string; languageCode: string; statusMsg: string }> {
  const effectiveKey = (apiKey && apiKey.trim()) || getStoredApiKey();

  if (!effectiveKey) {
    return {
      text: '',
      languageCode: targetLanguageCode || 'en-IN',
      statusMsg: '⚠️ Sarvam API Key missing. Please configure your API key in Settings to use Voice Input.',
    };
  }

  try {
    // Sanitize MIME type against Sarvam's strict whitelist:
    // Browser MediaRecorder emits 'audio/webm;codecs=opus', which must be cleaned to 'audio/webm'
    const rawType = (audioBlob.type || '').split(';')[0].trim().toLowerCase();
    let cleanMimeType = 'audio/webm';
    let filename = 'student_voice_input.webm';

    if (rawType.includes('wav')) {
      cleanMimeType = 'audio/wav';
      filename = 'student_voice_input.wav';
    } else if (rawType.includes('mp4') || rawType.includes('m4a')) {
      cleanMimeType = 'audio/mp4';
      filename = 'student_voice_input.mp4';
    } else if (rawType.includes('ogg')) {
      cleanMimeType = 'audio/ogg';
      filename = 'student_voice_input.ogg';
    } else if (rawType.includes('opus')) {
      cleanMimeType = 'audio/opus';
      filename = 'student_voice_input.opus';
    } else if (rawType.includes('mp3') || rawType.includes('mpeg')) {
      cleanMimeType = 'audio/mp3';
      filename = 'student_voice_input.mp3';
    } else if (rawType.includes('aac')) {
      cleanMimeType = 'audio/aac';
      filename = 'student_voice_input.aac';
    } else {
      cleanMimeType = 'audio/webm';
      filename = 'student_voice_input.webm';
    }

    // Wrap Blob with normalized MIME type so the multipart Content-Type header matches Sarvam's whitelist
    const uploadBlob = audioBlob.type === cleanMimeType ? audioBlob : new Blob([audioBlob], { type: cleanMimeType });

    const formData = new FormData();
    formData.append('file', uploadBlob, filename);
    formData.append('model', 'saaras:v4');

    // 'unknown' enables Sarvam's automatic language detection across all 23 languages
    const langCode = targetLanguageCode && targetLanguageCode !== 'auto' ? targetLanguageCode : 'unknown';
    formData.append('language_code', langCode);

    const res = await fetch(SARVAM_ASR_URL, {
      method: 'POST',
      headers: {
        'api-subscription-key': effectiveKey,
      },
      body: formData,
    });

    if (res.ok) {
      const data = await res.json();
      const transcript = (data.transcript || '').trim();
      if (transcript) {
        return {
          text: transcript,
          languageCode: data.language_code || langCode,
          statusMsg: `✓ Transcribed via Sarvam Saaras (${data.language_code || langCode})`,
        };
      } else {
        return {
          text: '',
          languageCode: data.language_code || langCode,
          statusMsg: '⚠️ No audible speech detected in recording. Please try speaking closer to the microphone.',
        };
      }
    } else {
      const err = await res.json().catch(() => ({}));
      const errMsg = err?.error?.message || err?.message || `HTTP ${res.status}`;
      console.warn('Sarvam ASR error response:', err);
      return {
        text: '',
        languageCode: langCode,
        statusMsg: `⚠️ Voice transcription error: ${errMsg}`,
      };
    }
  } catch (e: any) {
    console.warn('Sarvam ASR network call failed:', e);
    return {
      text: '',
      languageCode: targetLanguageCode || 'en-IN',
      statusMsg: `⚠️ Network error connecting to Sarvam ASR: ${e?.message || e}`,
    };
  }
}

/**
 * Text Translation via Sarvam Translate API
 */
export async function translateTextSarvam(
  text: string,
  targetLangCode: string,
  sourceLangCode: string = 'en-IN',
  apiKey?: string
): Promise<string> {
  const effectiveKey = (apiKey && apiKey.trim()) || getStoredApiKey();
  if (!effectiveKey) return text;

  try {
    const res = await fetch(SARVAM_TRANSLATE_URL, {
      method: 'POST',
      headers: {
        'api-subscription-key': effectiveKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        input: text,
        source_language_code: sourceLangCode,
        target_language_code: targetLangCode,
        mode: 'formal',
      }),
    });

    if (res.ok) {
      const data = await res.json();
      return data.translated_text || text;
    }
  } catch (e) {
    console.warn('Sarvam Translate failed:', e);
  }
  return text;
}
