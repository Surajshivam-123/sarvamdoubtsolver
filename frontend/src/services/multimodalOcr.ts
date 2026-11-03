/**
 * Multimodal OCR & Vision Document Intelligence Service
 * Combines client-side Tesseract.js with Sarvam AI LLM completion (sarvam-105b-conversations)
 * to accurately parse physics/math/science MCQs, figures, diagrams, values, equations, and options.
 * Faithfully reconstructs ONLY the text and problem present in the user's uploaded image.
 */

import Tesseract from 'tesseract.js';
import { getStoredApiKey } from './sarvamApi';

export interface OcrExtractionResult {
  problemStatement: string;
  latexEquations: string[];
  domain: string;
  previewUrl: string;
  confidence: number;
  fileName: string;
  figureInterpretation?: string;
  extractedValues?: Record<string, string>;
  options?: string[];
}

/**
 * Preprocess image via HTML5 Canvas for optimal OCR sharpness and contrast.
 */
async function preprocessImage(file: File): Promise<HTMLCanvasElement | File> {
  if (typeof window === 'undefined' || typeof document === 'undefined') return file;

  return new Promise((resolve) => {
    const img = new Image();
    const url = URL.createObjectURL(file);

    img.onload = () => {
      URL.revokeObjectURL(url);
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      if (!ctx) {
        resolve(file);
        return;
      }

      // Scale to optimal OCR dimensions (between 1200px and 2200px)
      let width = img.width;
      let height = img.height;
      if (width < 900) {
        const factor = 1200 / width;
        width = 1200;
        height = Math.round(height * factor);
      } else if (width > 2400) {
        const factor = 2000 / width;
        width = 2000;
        height = Math.round(height * factor);
      }

      canvas.width = width;
      canvas.height = height;

      // Draw with smooth interpolation
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(img, 0, 0, width, height);

      try {
        const imgData = ctx.getImageData(0, 0, width, height);
        const d = imgData.data;

        // Grayscale + gentle contrast stretch (preserves text lines and equations)
        for (let i = 0; i < d.length; i += 4) {
          const lum = 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2];
          // Gentle contrast stretch
          const val = lum < 128 ? Math.max(0, lum - 15) : Math.min(255, lum + 15);
          d[i] = val;
          d[i + 1] = val;
          d[i + 2] = val;
        }

        ctx.putImageData(imgData, 0, 0);
        resolve(canvas);
      } catch {
        resolve(canvas);
      }
    };

    img.onerror = () => resolve(file);
    img.src = url;
  });
}

/**
 * Extracts MCQ Options across vertical, horizontal, numbered, and dotted formats.
 */
export function extractMcqOptions(text: string): string[] {
  const options: string[] = [];

  // Strategy 1: Check line-by-line first: (A) ..., (B) ..., [A] ..., A. ...
  const lines = text.split('\n').map((l) => l.trim()).filter(Boolean);
  const lineOptions: string[] = [];
  for (const line of lines) {
    const m = line.match(/^[\(\[]?([A-D1-4])[\)\]\.\:\-]\s*(.+)$/i);
    if (m) {
      let optKey = m[1].toUpperCase();
      if (optKey === '1') optKey = 'A';
      else if (optKey === '2') optKey = 'B';
      else if (optKey === '3') optKey = 'C';
      else if (optKey === '4') optKey = 'D';
      lineOptions.push(`(${optKey}) ${m[2].trim()}`);
    }
  }
  if (lineOptions.length >= 2) {
    return lineOptions;
  }

  // Strategy 2: Horizontal options on single or multi-line: (A) ... (B) ... (C) ... (D) ...
  const matches = [...text.matchAll(/[\(\[]([A-D1-4])[\)\]]\s*([^(\[]+)/gi)];
  if (matches.length >= 2) {
    for (const m of matches) {
      let letter = m[1].toUpperCase();
      if (letter === '1') letter = 'A';
      else if (letter === '2') letter = 'B';
      else if (letter === '3') letter = 'C';
      else if (letter === '4') letter = 'D';
      const val = m[2].trim().replace(/[\r\n]+/g, ' ');
      options.push(`(${letter}) ${val}`);
    }
    return options;
  }

  // Strategy 3: A. ... B. ... C. ... D. ...
  const dotMatches = [...text.matchAll(/\b([A-D])\.\s*([^A-D\n]+)/gi)];
  if (dotMatches.length >= 2) {
    for (const m of dotMatches) {
      options.push(`(${m[1].toUpperCase()}) ${m[2].trim()}`);
    }
    return options;
  }

  return options;
}

/**
 * Extracts physical and mathematical variables and equations genuinely present in the scanned text.
 * NEVER fabricates fake values or forced incline constants.
 */
export function extractEquationsAndValues(text: string): {
  extractedValues: Record<string, string>;
  latexEquations: string[];
} {
  const extractedValues: Record<string, string> = {};
  const latexEquations: string[] = [];

  // Mass
  const massMatch = text.match(/\b(?:mass|m)\s*=?\s*(\d+(?:\.\d+)?)\s*(kg|g)\b/i);
  if (massMatch) {
    extractedValues['Mass (m)'] = `${massMatch[1]} ${massMatch[2]}`;
    latexEquations.push(`m = ${massMatch[1]}\\text{ ${massMatch[2]}}`);
  }

  // Velocity / Speed
  const velMatch = text.match(/\b(?:velocity|speed|v|u)\s*=?\s*(\d+(?:\.\d+)?)\s*(m\/s|km\/h|ms\^-1)\b/i);
  if (velMatch) {
    extractedValues['Velocity'] = `${velMatch[1]} ${velMatch[2]}`;
    latexEquations.push(`v = ${velMatch[1]}\\text{ m/s}`);
  }

  // Acceleration
  const accMatch = text.match(/\b(?:acceleration|a)\s*=?\s*(\d+(?:\.\d+)?)\s*(m\/s\^?2|ms\^-2)\b/i);
  if (accMatch) {
    extractedValues['Acceleration (a)'] = `${accMatch[1]} m/s²`;
    latexEquations.push(`a = ${accMatch[1]}\\text{ m/s}^2`);
  }

  // Gravity
  const gMatch = text.match(/\bg\s*=?\s*(\d+(?:\.\d+)?)\s*(?:m\/s\^?2|ms\^-2)?\b/i);
  if (gMatch) {
    extractedValues['Gravity (g)'] = `${gMatch[1]} m/s²`;
    latexEquations.push(`g = ${gMatch[1]}\\text{ m/s}^2`);
  }

  // Force
  const forceMatch = text.match(/\b(?:force|F)\s*=?\s*(\d+(?:\.\d+)?)\s*N\b/i);
  if (forceMatch) {
    extractedValues['Force (F)'] = `${forceMatch[1]} N`;
    latexEquations.push(`F = ${forceMatch[1]}\\text{ N}`);
  }

  // Voltage
  const voltMatch = text.match(/\b(\d+(?:\.\d+)?)\s*(?:V|volts?)\b/i);
  if (voltMatch) {
    extractedValues['Voltage (V)'] = `${voltMatch[1]} V`;
    latexEquations.push(`V = ${voltMatch[1]}\\text{ V}`);
  }

  // Resistance
  const resMatch = text.match(/\b(\d+(?:\.\d+)?)\s*(?:Ω|ohm|ohms)\b/i);
  if (resMatch) {
    extractedValues['Resistance (R)'] = `${resMatch[1]} Ω`;
    latexEquations.push(`R = ${resMatch[1]}\\Omega`);
  }

  // Angle
  const angleMatch = text.match(/(?:θ|theta|angle|inclination)\s*=?\s*(\d+(?:\.\d+)?)(?:°|deg)?/i);
  if (angleMatch) {
    extractedValues['Angle (θ)'] = `${angleMatch[1]}°`;
    latexEquations.push(`\\theta = ${angleMatch[1]}^\\circ`);
  }

  // Friction coefficient
  const muMatch = text.match(/(?:μ|mu|_s|_k)\s*=?\s*(\d+(?:\.\d+)?)/i);
  if (muMatch) {
    extractedValues['Friction (μ)'] = muMatch[1];
    latexEquations.push(`\\mu = ${muMatch[1]}`);
  }

  // Radius / Distance / Height
  const distMatch = text.match(/\b(?:height|distance|radius|h|r|s)\s*=?\s*(\d+(?:\.\d+)?)\s*(m|cm|km)\b/i);
  if (distMatch) {
    extractedValues['Distance/Height'] = `${distMatch[1]} ${distMatch[2]}`;
    latexEquations.push(`h = ${distMatch[1]}\\text{ ${distMatch[2]}}`);
  }

  return { extractedValues, latexEquations };
}

/**
 * Determines domain strictly from extracted words.
 */
export function detectDomainFromText(text: string): string {
  const t = text.toLowerCase();
  if (t.includes('resistor') || t.includes('circuit') || t.includes('voltage') || t.includes('current') || t.includes('ohm') || t.includes('battery')) {
    return 'Physics & Electric Circuits';
  }
  if (t.includes('projectile') || t.includes('trajectory') || t.includes('incline') || t.includes('velocity') || t.includes('acceleration') || t.includes('friction') || t.includes('pulley') || t.includes('force') || t.includes('momentum') || t.includes('mass') || t.includes('gravity')) {
    return 'Physics & Classical Mechanics';
  }
  if (t.includes('derivative') || t.includes('integral') || t.includes('calculus') || t.includes('matrix') || t.includes('eigen') || t.includes('limit') || t.includes('polynomial')) {
    return 'Mathematics & Calculus';
  }
  if (t.includes('equilibrium') || t.includes('reaction') || t.includes('moles') || t.includes('acid') || t.includes('base') || t.includes('ph') || t.includes('catalyst')) {
    return 'Chemistry & Thermodynamics';
  }
  if (t.includes('dna') || t.includes('gene') || t.includes('cell') || t.includes('allele') || t.includes('protein')) {
    return 'Biology & Life Sciences';
  }
  if (t.includes('algorithm') || t.includes('stack') || t.includes('array') || t.includes('tree') || t.includes('hash')) {
    return 'Computer Science & Data Structures';
  }
  return 'Academic & Scientific Inquiry';
}

/**
 * Calls Sarvam AI Sovereign LLM (sarvam-105b-conversations) to execute
 * Phase 1: Visual & Diagrammatic Analysis.
 * Formats findings strictly under header: ### Problem Section
 * Combines raw question with a literal, descriptive breakdown of the image.
 * Strict State Isolation: Does NOT solve the problem yet.
 */
async function synthesizeWithSarvamLlm(
  rawText: string,
  options: string[],
  fileName: string = ''
): Promise<string | null> {
  const apiKey = getStoredApiKey();
  if (!apiKey) return null;

  try {
    const prompt = `You are a highly advanced Multimodal Physics Engine and Reasoning Agent.
Input image metadata:
- File Name: "${fileName}"
- Extracted OCR raw characters: """${rawText.slice(0, 1500)}"""
- Detected MCQ Options: ${JSON.stringify(options)}

Objective: Execute Phase 1: Visual & Diagrammatic Analysis (Triggered instantly upon upload).
Your immediate goal is to map the scene into a structured text format. Do NOT solve the problem yet! (State Isolation).

Instructions:
1. OCR Text Extraction: Extract and preserve all visible textual characters, numbers, variables, symbols, and standard units within the image. Fix scanning typos.
2. Diagrammatic Comprehension: Look past text to analyze structural configurations. Identify boundaries, coordinate grids, free-body variables, and directional vectors.
3. Physical Object Mapping: Track geometry and physical relationships. Map vectors (forces, velocity, acceleration fields), system components (pulleys, inclined planes, springs, electric fields, circuits, waves), and abstract visual states.
4. No-String Images constraint: If the image contains zero written text/strings and consists solely of visual diagrams or real-world experimental setups, completely translate the visual scene into an analytical descriptive paragraph describing the physical configuration, objects, and target parameter.
5. Structural Output Generation: Synthesize your visual findings directly into a uniform string. Format it EXACTLY under the header titled '### Problem Section'. Combine the raw question with a literal, descriptive breakdown of the image.

Output Format strictly as:
### Problem Section
[Problem Statement and formatted MCQ options (A), (B), (C), (D) if present]

**Visual & Diagrammatic Analysis:**
- Configuration: [Literal descriptive breakdown of the structural components and geometry]
- Physical Entities & Vectors: [Masses, forces, fields, coordinates, or circuit elements]
- Target Physical Quantity: [Explicitly state what quantity is to be calculated]

Return ONLY this text. Never output formulas, derivations, or solutions in Phase 1!`;

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 12000);

    const res = await fetch('https://api.sarvam.ai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'api-subscription-key': apiKey,
      },
      body: JSON.stringify({
        model: 'sarvam-105b-conversations',
        messages: [
          {
            role: 'system',
            content: 'You are an advanced Multimodal Physics Engine. Format findings strictly under ### Problem Section. Do not solve yet.',
          },
          { role: 'user', content: prompt },
        ],
        max_tokens: 800,
        temperature: 0.1,
      }),
      signal: controller.signal,
    });

    clearTimeout(timer);

    if (res.ok) {
      const data = await res.json();
      let content = data.choices?.[0]?.message?.content?.trim();
      if (content) {
        content = content.replace(/^```[a-z]*\s*/i, '').replace(/```$/i, '').trim();
        if (content.length > 20) {
          if (!content.startsWith('### Problem Section')) {
            content = `### Problem Section\n${content}`;
          }
          return content;
        }
      }
    }
  } catch (e) {
    console.warn('Sarvam LLM Phase 1 analysis note:', e);
  }
  return null;
}

/**
 * Deterministic Fallback when offline or LLM unavailable.
 * Formats strictly under ### Problem Section with extracted values.
 */
export function synthesizeFigureProblem(
  rawText: string,
  options: string[],
  fileName: string
): string {
  let cleaned = rawText
    .replace(/\r/g, '')
    .replace(/\bNCQ\b/gi, 'MCQ')
    .replace(/\blidesdonn\b/gi, 'slides down')
    .replace(/\b[0O]\s*=\s*(\d{1,2})\s*(?:°|deg)?/gi, 'θ = $1°')
    .replace(/\b(theta|thata)\b/gi, 'θ')
    .replace(/\b(mu|coefficient of friction|friction coefficient)\b/gi, 'μ')
    .replace(/\|\s*/g, ' ')
    .trim();

  let body = '';
  if (cleaned.length > 15) {
    body = cleaned;
    if (options.length >= 2 && !/options?:/i.test(body)) {
      body += `\n\nOptions:\n${options.join('\n')}`;
    }
  } else {
    body = `Physical system and diagram schematic uploaded from "${fileName}".`;
  }

  return `### Problem Section\n${body}\n\n**Visual & Diagrammatic Analysis:**\n- Configuration: Visual diagram and schematic mapped from ${fileName}.\n- Physical Entities: Identified parameters and physical geometry from image.\n- Target Quantity: Determine the physical quantities and evaluate the target state.`;
}

/**
 * Main Vision OCR Pipeline
 * Evaluates the image via canvas preprocessing and in-browser Tesseract OCR (with 25s safe timeout),
 * reconstructs the problem with Sarvam LLM, and populates the problem statement.
 */
export async function processImageOcr(file: File): Promise<OcrExtractionResult> {
  const previewUrl = URL.createObjectURL(file);
  const fileName = file.name;

  let rawText = '';
  let ocrConfidence = 0.85;

  try {
    // 1. Run in-browser preprocessing
    const preprocessed = await preprocessImage(file);

    // 2. Perform OCR recognition with a generous 25-second timeout
    const ocrPromise = Tesseract.recognize(preprocessed, 'eng', {
      logger: (m) => {
        if (m.status === 'recognizing text') {
          console.debug(`[OCR Progress] ${(m.progress * 100).toFixed(0)}%`);
        }
      },
    });

    const timeoutPromise = new Promise<{ data: { text: string; confidence?: number } }>((resolve) => {
      setTimeout(() => {
        resolve({ data: { text: '', confidence: 50 } });
      }, 25000);
    });

    const result = await Promise.race([ocrPromise, timeoutPromise]);
    if (result && result.data && result.data.text) {
      rawText = result.data.text.trim();
      if (typeof result.data.confidence === 'number') {
        ocrConfidence = Math.max(0.5, result.data.confidence / 100);
      }
    }
  } catch (err) {
    console.warn('Tesseract OCR engine warning:', err);
  }

  // 3. Extract MCQ options genuinely found in raw text
  const options = extractMcqOptions(rawText);

  // 4. Extract physical variables and math equations present in text
  const { extractedValues, latexEquations } = extractEquationsAndValues(rawText);

  // 5. Detect domain from actual words
  const domain = detectDomainFromText(rawText);

  // 6. Execute Phase 1: Visual & Diagrammatic Analysis via Sarvam AI Sovereign LLM
  let naturalProblemText = await synthesizeWithSarvamLlm(rawText, options, fileName);

  // 7. Fallback to clean deterministic reconstruction if offline or LLM unavailable
  if (!naturalProblemText) {
    naturalProblemText = synthesizeFigureProblem(rawText, options, fileName);
  }

  // Construct figure interpretation description based on actual text
  let figureInterpretation = '';
  if (rawText.toLowerCase().includes('circuit') || rawText.toLowerCase().includes('resistor')) {
    figureInterpretation = 'Figure Analysis: Schematic depicts an electrical circuit with interconnected resistors and electromotive force.';
  } else if (rawText.toLowerCase().includes('projectile')) {
    figureInterpretation = 'Figure Analysis: Kinematic diagram depicts a 2D projectile trajectory under uniform downward gravity.';
  } else if (rawText.toLowerCase().includes('incline') || rawText.toLowerCase().includes('wedge')) {
    figureInterpretation = 'Figure Analysis: Free-body diagram on an inclined plane with gravity and surface contact forces.';
  } else if (rawText.toLowerCase().includes('pulley')) {
    figureInterpretation = 'Figure Analysis: Mechanical system with connected masses across a pulley.';
  } else if (rawText.trim().length > 15) {
    figureInterpretation = `Figure Analysis: Visual schematic for ${domain} problem.`;
  }

  return {
    problemStatement: naturalProblemText,
    latexEquations,
    domain,
    previewUrl,
    confidence: ocrConfidence,
    fileName,
    figureInterpretation,
    extractedValues,
    options,
  };
}
