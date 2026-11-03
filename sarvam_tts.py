"""
Sarvam AI Text-to-Speech (TTS) & Hybrid Translation Engine.
Includes:
1. 10 Indian Language Matrix with bulbul:v3 native voice profiles
2. Phonetic LaTeX-to-Speech Sanitization
3. Natural Hinglish / Regional STEM Glossary Preservation
4. Sarvam Translation (mayura:v1) with STEM keyword shielding
5. Robust Acoustic Wave Audio Fallback for offline / demo resilience
"""

import base64
import io
import math
import os
import re
import struct
import wave
import requests
from typing import Dict, Any, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

SARVAM_TTS_URL = "https://api.sarvam.ai/text-to-speech"
SARVAM_TRANSLATE_URL = "https://api.sarvam.ai/translate"

LANGUAGE_REGISTRY = {
    "English": {"code": "en-IN", "speaker": "simran", "name": "English (Indian)"},
    "Hindi (Hinglish)": {"code": "hi-IN", "speaker": "ritu", "name": "Hindi (Hinglish)"},
    "Bengali (বাংলা)": {"code": "bn-IN", "speaker": "roopa", "name": "Bengali (বাংলা)"},
    "Marathi (मराठी)": {"code": "mr-IN", "speaker": "soham", "name": "Marathi (मराठी)"},
    "Tamil (தமிழ்)": {"code": "ta-IN", "speaker": "gokul", "name": "Tamil (தமிழ்)"},
    "Telugu (తెలుగు)": {"code": "te-IN", "speaker": "kavitha", "name": "Telugu (తెలుగు)"},
    "Gujarati (ગુજરાતી)": {"code": "gu-IN", "speaker": "pooja", "name": "Gujarati (ગુજરાતી)"},
    "Kannada (ಕನ್ನಡ)": {"code": "kn-IN", "speaker": "chaitra", "name": "Kannada (ಕನ್ನಡ)"},
    "Malayalam (മലയാളം)": {"code": "ml-IN", "speaker": "gokul", "name": "Malayalam (മലയാളം)"},
    "Punjabi (ਪੰਜਾਬੀ)": {"code": "pa-IN", "speaker": "anand", "name": "Punjabi (ਪੰਜਾਬੀ)"},
}

# Backward compatible language code lookup
LANGUAGE_OPTIONS = {
    cfg["code"]: {"name": cfg["name"], "default_speaker": cfg["speaker"], "speakers": [cfg["speaker"], "ritu", "aditya"]}
    for cfg in LANGUAGE_REGISTRY.values()
}

SPEAKER_ALIASES = {
    "meera": "ritu",
    "arvind": "aditya",
    "amol": "soham",
    "amartya": "roopa",
    "pavithra": "gokul",
}

MODEL_OPTIONS = ["bulbul:v3", "bulbul:v4-flash", "bulbul:v1"]


def get_configured_api_key(api_key: Optional[str] = None) -> str:
    """Retrieves API key with priority: explicit arg > st.secrets > os.environ."""
    if api_key and api_key.strip():
        return api_key.strip()

    # Try Streamlit secrets first (used in Streamlit Cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "SARVAM_API_KEY" in st.secrets:
            sec = str(st.secrets["SARVAM_API_KEY"]).strip()
            if sec:
                return sec
    except Exception:
        pass

    return os.getenv("SARVAM_API_KEY", "").strip()


def sanitize_latex_for_speech(text: str) -> str:
    """Converts formulas, symbols, and mathematical notation into speakable words."""
    replacements = [
        (r"\\frac\{([^}]+)\}\{([^}]+)\}", r"\1 divided by \2"),
        (r"\\sqrt\{([^}]+)\}", r"square root of \1"),
        (r"\^2", " squared"),
        (r"\^3", " cubed"),
        (r"\^([a-zA-Z0-9]+)", r" to the power \1"),
        (r"_", " "),
        (r"\\Delta", "delta"),
        (r"\\theta", "theta"),
        (r"\\omega", "omega"),
        (r"\\alpha", "alpha"),
        (r"\\mu", "mu"),
        (r"\\pi", "pi"),
        (r"\+", " plus "),
        (r"-(?!\w)", " minus "),
        (r"=", " equals "),
        (r">=", " is greater than or equal to "),
        (r"<=", " is less than or equal to "),
        (r">", " is greater than "),
        (r"<", " is less than "),
        (r"\*", " times "),
        (r"%", " percent"),
        (r"\$", ""),
    ]
    clean_text = text
    for pattern, replacement in replacements:
        clean_text = re.sub(pattern, replacement, clean_text)
    clean_text = re.sub(r"\\[a-zA-Z]+", "", clean_text)
    return re.sub(r"\s+", " ", clean_text).strip()


def apply_hinglish_glossary(text: str) -> str:
    """
    Restores common classroom English STEM phrases in formal Hindi text
    so explanations sound natural and intuitive rather than archaic.
    """
    hinglish_replacements = [
        ("यांत्रिक ऊर्जा", "mechanical energy"),
        ("गतिज ऊर्जा", "kinetic energy"),
        ("स्थितिज ऊर्जा", "potential energy"),
        ("ऊर्जा संरक्षण", "energy conservation"),
        ("संरक्षित", "conserved"),
        ("घर्षण बल", "friction force"),
        ("घर्षण", "friction"),
        ("संपीड़न", "spring compression"),
        ("मुक्त पिंड आरेख", "Free Body Diagram"),
        ("क्रिया और प्रतिक्रिया", "action-reaction"),
        ("परिणामी बल", "net force"),
        ("अभिकेंद्री त्वरण", "centripetal acceleration"),
        ("अपकेंद्री बल", "centrifugal force"),
        ("कोणीय संवेग", "angular momentum"),
        ("जड़त्व आघूर्ण", "moment of inertia"),
        ("प्रत्यानयन बल", "restoring force"),
        ("अवरोध", "barrier"),
        ("त्वरण", "acceleration"),
        ("वेग", "velocity"),
    ]
    result = text
    for pure_hindi, hinglish_word in hinglish_replacements:
        result = result.replace(pure_hindi, hinglish_word)
    return result


def translate_with_sarvam_hybrid(
    text: str,
    target_lang_code: str,
    api_key: Optional[str] = None,
    source_lang_code: str = "en-IN",
) -> str:
    """Translates text via Sarvam AI while keeping STEM terms in natural Hinglish/hybrid phrasing."""
    key = get_configured_api_key(api_key)
    if not key or not text.strip() or target_lang_code == source_lang_code:
        return text

    payload = {
        "input": text[:800],
        "target_language_code": target_lang_code,
        "speaker_gender": "Female",
        "mode": "formal",
        "model": "mayura:v1",
        "source_language_code": source_lang_code,
    }
    headers = {
        "api-subscription-key": key,
        "Content-Type": "application/json",
    }

    try:
        res = requests.post(SARVAM_TRANSLATE_URL, json=payload, headers=headers, timeout=12)
        if res.status_code == 200:
            raw_translation = res.json().get("translated_text", text)
            if target_lang_code == "hi-IN":
                return apply_hinglish_glossary(raw_translation)
            return raw_translation
        return text
    except Exception:
        return text


def chunk_text(text: str, max_chars: int = 450) -> list[str]:
    """Splits long narration text into sentences or chunks that fit within Sarvam API limits."""
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
    Ensures the audio player always functions gracefully without throwing errors in offline or demo modes.
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
                envelope = math.exp(-3.0 * (float(i) / n_samples))
                val = envelope * (0.6 * math.sin(2 * math.pi * freq * t) + 0.4 * math.sin(4 * math.pi * freq * t))
                sample = int(val * 32767.0 * 0.5)
                wav_file.writeframesraw(struct.pack('<h', max(-32768, min(32767, sample))))
                
    buf.seek(0)
    return buf.read()


def synthesize_speech_sarvam(
    text: str,
    target_language_code: str = "hi-IN",
    speaker: str = "ritu",
    model: str = "bulbul:v3",
    api_key: Optional[str] = None,
    timeout: int = 15
) -> Tuple[Optional[bytes], str, bool]:
    """
    Calls Sarvam AI Text-to-Speech REST endpoint to convert pedagogical feedback into speech.
    
    Returns:
        (audio_bytes, status_message, is_real_api)
    """
    key = get_configured_api_key(api_key)

    if not key or key == "your_sarvam_api_key_here":
        mock_audio = generate_synthesized_fallback_audio()
        return (
            mock_audio,
            "⚠️ Sarvam AI API Key not provided. Rendered harmonic acoustic audio preview. Enter your Sarvam key in the sidebar for live Indian language voice narration.",
            False
        )

    # Sanitize formulas and chunk input text
    clean_speech_text = sanitize_latex_for_speech(text)
    chunks = chunk_text(clean_speech_text)
    primary_text = chunks[0] if chunks else clean_speech_text[:450]

    headers = {
        "api-subscription-key": key,
        "Content-Type": "application/json"
    }

    # Normalize speaker alias (e.g. meera -> ritu, arvind -> aditya, amol -> soham)
    effective_speaker = SPEAKER_ALIASES.get(speaker.lower(), speaker.lower())

    models_to_try = [model]
    for alt in MODEL_OPTIONS:
        if alt not in models_to_try:
            models_to_try.append(alt)

    last_error = ""
    for try_model in models_to_try:
        speakers_to_try = [effective_speaker]
        if speaker.lower() not in speakers_to_try:
            speakers_to_try.append(speaker.lower())

        for spk in speakers_to_try:
            payload = {
                "inputs": [primary_text],
                "target_language_code": target_language_code,
                "speaker": spk,
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
                            f"✅ Sarvam AI TTS synthesized live audio ({try_model}, speaker: {spk}, lang: {target_language_code})",
                            True
                        )
                    else:
                        last_error = f"Empty audio array in Sarvam response: {data}"
                else:
                    last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                    if response.status_code in (401, 403):
                        break
            except requests.exceptions.RequestException as e:
                last_error = f"Network request exception: {str(e)}"
                break

    fallback_audio = generate_synthesized_fallback_audio()
    msg = (
        f"⚠️ Sarvam TTS Note ({last_error}). "
        f"Delivered simulated pedagogical audio fallback so your workflow is uninterrupted."
    )
    return (fallback_audio, msg, False)
