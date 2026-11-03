"""
Sarvam AI Text-to-Speech (TTS) Integration Engine.
Handles REST calls to https://api.sarvam.ai/text-to-speech,
base64 decoding, language/speaker mappings, chunking, and resilient fallbacks.
"""

import base64
import io
import math
import os
import struct
import wave
import requests
from typing import Dict, Any, Optional, Tuple

SARVAM_TTS_URL = "https://api.sarvam.ai/text-to-speech"

LANGUAGE_OPTIONS = {
    "hi-IN": {"name": "Hindi (हिन्दी)", "default_speaker": "meera", "speakers": ["meera", "arvind"]},
    "en-IN": {"name": "English (Indian)", "default_speaker": "meera", "speakers": ["meera", "arvind"]},
    "bn-IN": {"name": "Bengali (বাংলা)", "default_speaker": "amartya", "speakers": ["amartya", "meera"]},
    "mr-IN": {"name": "Marathi (मराठी)", "default_speaker": "amol", "speakers": ["amol", "meera"]},
    "ta-IN": {"name": "Tamil (தமிழ்)", "default_speaker": "pavithra", "speakers": ["pavithra", "arvind"]},
    "te-IN": {"name": "Telugu (తెలుగు)", "default_speaker": "pavithra", "speakers": ["pavithra", "arvind"]},
    "kn-IN": {"name": "Kannada (ಕನ್ನಡ)", "default_speaker": "pavithra", "speakers": ["pavithra", "arvind"]},
    "gu-IN": {"name": "Gujarati (ગુજરાતી)", "default_speaker": "amol", "speakers": ["amol", "meera"]},
}

MODEL_OPTIONS = ["bulbul:v1", "bulbul:v2", "bulbul:v3"]


def chunk_text(text: str, max_chars: int = 450) -> list[str]:
    """
    Splits long narration text into sentences or chunks that fit within Sarvam API limits.
    """
    text = text.strip()
    if len(text) <= max_chars:
        return [text]

    sentences = text.replace("।", ". ").replace("?", ". ").replace("!", ". ").split(". ")
    chunks = []
    current_chunk = ""

    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if len(current_chunk) + len(s) + 2 <= max_chars:
            current_chunk = f"{current_chunk}. {s}" if current_chunk else s
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = s[:max_chars]

    if current_chunk:
        chunks.append(current_chunk)

    return chunks if chunks else [text[:max_chars]]


def generate_synthesized_fallback_audio(message: str = "Bhasha Doubt Solver Feedback") -> bytes:
    """
    Synthesizes a pleasant multi-tone harmonic WAV audio stream using Python's built-in wave module.
    Used when Sarvam API Key is not set or network is offline, ensuring the audio player
    always functions gracefully without throwing errors.
    """
    sample_rate = 22050
    duration_per_tone = 0.35
    frequencies = [440.0, 554.37, 659.25, 880.0]  # A major chord arpeggio
    
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        for freq in frequencies:
            n_samples = int(sample_rate * duration_per_tone)
            for i in range(n_samples):
                t = float(i) / sample_rate
                # Harmonic wave with envelope decay
                envelope = math.exp(-3.0 * (float(i) / n_samples))
                val = envelope * (0.6 * math.sin(2 * math.pi * freq * t) + 0.4 * math.sin(4 * math.pi * freq * t))
                sample = int(val * 32767.0 * 0.5)
                wav_file.writeframesraw(struct.pack('<h', max(-32768, min(32767, sample))))
                
    buf.seek(0)
    return buf.read()


def synthesize_speech_sarvam(
    text: str,
    target_language_code: str = "hi-IN",
    speaker: str = "meera",
    model: str = "bulbul:v1",
    api_key: Optional[str] = None,
    timeout: int = 15
) -> Tuple[Optional[bytes], str, bool]:
    """
    Calls Sarvam AI Text-to-Speech REST endpoint to convert pedagogical feedback into speech.
    
    Returns:
        (audio_bytes, status_message, is_real_api)
    """
    key = api_key or os.getenv("SARVAM_API_KEY", "").strip()

    if not key or key == "your_sarvam_api_key_here":
        mock_audio = generate_synthesized_fallback_audio()
        return (
            mock_audio,
            "⚠️ Sarvam AI API Key not provided. Rendered harmonic acoustic audio preview. Enter your Sarvam key in the sidebar for live Indian language voice narration.",
            False
        )

    # Clean and chunk input text
    chunks = chunk_text(text)
    primary_text = chunks[0] if chunks else text[:450]

    headers = {
        "api-subscription-key": key,
        "Content-Type": "application/json"
    }

    # Attempt primary model, fallback to alternative models if rejected
    models_to_try = [model]
    for alt in MODEL_OPTIONS:
        if alt not in models_to_try:
            models_to_try.append(alt)

    last_error = ""
    for try_model in models_to_try:
        payload = {
            "inputs": [primary_text],
            "target_language_code": target_language_code,
            "speaker": speaker,
            "model": try_model
        }

        try:
            response = requests.post(SARVAM_TTS_URL, headers=headers, json=payload, timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                audios = data.get("audios", [])
                if audios and len(audios) > 0:
                    base64_audio = audios[0]
                    audio_bytes = base64.b64decode(base64_audio)
                    return (
                        audio_bytes,
                        f"✅ Sarvam AI TTS synthesized successfully ({try_model}, speaker: {speaker}, lang: {target_language_code}).",
                        True
                    )
                else:
                    last_error = f"Empty audio array returned in Sarvam response: {data}"
            else:
                last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                # If 401 or 403, key is bad; don't hammer other models
                if response.status_code in (401, 403):
                    break
        except requests.exceptions.RequestException as e:
            last_error = f"Network request exception: {str(e)}"
            break

    # If Sarvam call failed, return fallback audio with informative explanation
    fallback_audio = generate_synthesized_fallback_audio()
    msg = (
        f"⚠️ Sarvam TTS Request Note ({last_error}). "
        f"Delivered simulated pedagogical audio fallback so your workflow is uninterrupted."
    )
    return (fallback_audio, msg, False)
