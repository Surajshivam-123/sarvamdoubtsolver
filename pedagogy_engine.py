"""
Core Pedagogical Diagnostic & Socratic Engine.
Enforces:
1. No Direct Solutions (Pedagogical Guardrails)
2. Diagnostic Evaluation of Derailment Points
3. Dual Comparative Thought Map generation (Graphviz DOT)
   - Map A: Student's Actual Path (Red/Coral for errors, Muted Gray for premises)
   - Map B: Remediated Conceptual Path (Emerald Green, Pivot Node highlighted)
4. Multilingual Auditory Scripting referencing map nodes
5. Targeted Socratic Elicitation
"""

import json
import re
import importlib
from typing import Dict, List, Any, Optional, Tuple
import sample_doubts
from sample_doubts import SAMPLE_DOUBTS


def get_sample_doubt_entry(key: Optional[str]) -> Optional[Dict[str, Any]]:
    """Safe getter that reloads sample_doubts if key is missing (stale module cache on cloud hot-reload)."""
    if not key:
        return None
    if key not in sample_doubts.SAMPLE_DOUBTS:
        importlib.reload(sample_doubts)
    return sample_doubts.SAMPLE_DOUBTS.get(key)


def clean_label(text: str, max_chars_per_line: int = 32) -> str:
    """Wraps text cleanly for Graphviz node labels, removes brackets, and escapes quotes."""
    text = text.replace('"', '\\"').replace('[', '').replace(']', '').strip()
    words = text.split()
    lines = []
    current_line = []
    current_len = 0

    for word in words:
        if current_len + len(word) + 1 > max_chars_per_line:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_len = len(word)
        else:
            current_line.append(word)
            current_len += len(word) + 1

    if current_line:
        lines.append(" ".join(current_line))

    return "\\n".join(lines)


def generate_map_a_dot(student_nodes: List[Dict[str, Any]], title: str = "Student's Actual Path") -> str:
    """
    Renders Map A (Student's Actual Reasoning Path).
    - Erroneous nodes rendered in Coral/Red (#E63946 / #FEE2E2 / #EF4444)
    - Valid premises rendered in Muted Gray/Slate (#64748B / #F8FAFC)
    """
    dot_lines = [
        'digraph StudentPath {',
        '  graph [rankdir=TB, bgcolor="transparent", margin="0.1", compound=true];',
        '  node [fontname="Helvetica, Arial, sans-serif", fontsize=10, shape=box, style="rounded,filled", penwidth=1.5];',
        '  edge [color="#94A3B8", penwidth=1.5, arrowsize=0.8];',
        f'  labelloc="t"; label="{title}"; fontname="Helvetica-Bold"; fontsize=12; fontcolor="#334155";',
        ''
    ]

    for i, node in enumerate(student_nodes):
        node_id = node.get("id", f"S{i+1}")
        raw_label = node.get("label", f"Step {i+1}")
        is_error = node.get("is_error", False)
        
        if is_error:
            # Coral / Red highlight for cognitive breakdown
            formatted_label = f"⚠️ Node {i+1}: DERAILMENT\\n{clean_label(raw_label)}"
            if node.get("detail"):
                formatted_label += f"\\n• {clean_label(node['detail'], 28)}"
            dot_lines.append(
                f'  {node_id} [label="{formatted_label}", color="#EF4444", fillcolor="#FEE2E2", fontcolor="#991B1B", penwidth=2.2];'
            )
        else:
            # Muted Slate Gray for sound premises
            formatted_label = f"Node {i+1}: Premise\\n{clean_label(raw_label)}"
            dot_lines.append(
                f'  {node_id} [label="{formatted_label}", color="#94A3B8", fillcolor="#F8FAFC", fontcolor="#334155"];'
            )

    dot_lines.append('')
    # Connect sequential nodes
    for i in range(len(student_nodes) - 1):
        src = student_nodes[i].get("id", f"S{i+1}")
        dst = student_nodes[i+1].get("id", f"S{i+2}")
        is_error_transition = student_nodes[i+1].get("is_error", False)
        edge_style = 'color="#EF4444", style="dashed", label=" intuitive breakdown", fontcolor="#B91C1C", fontsize=9' if is_error_transition and not student_nodes[i].get("is_error") else 'color="#94A3B8"'
        dot_lines.append(f'  {src} -> {dst} [{edge_style}];')

    dot_lines.append('}')
    return "\n".join(dot_lines)


def generate_map_b_dot(remediation_nodes: List[Dict[str, Any]], title: str = "Remediated Conceptual Path") -> str:
    """
    Renders Map B (Canonical Remediated Reasoning Path).
    - Standard steps rendered in Emerald Green (#10B981 / #ECFDF5)
    - Pivot Node highlighted with bold emerald border, star badge, and breakthrough indicator (#047857 / #D1FAE5)
    """
    dot_lines = [
        'digraph RemediationPath {',
        '  graph [rankdir=TB, bgcolor="transparent", margin="0.1", compound=true];',
        '  node [fontname="Helvetica, Arial, sans-serif", fontsize=10, shape=box, style="rounded,filled", penwidth=1.5];',
        '  edge [color="#10B981", penwidth=1.6, arrowsize=0.8];',
        f'  labelloc="t"; label="{title}"; fontname="Helvetica-Bold"; fontsize=12; fontcolor="#065F46";',
        ''
    ]

    for i, node in enumerate(remediation_nodes):
        node_id = node.get("id", f"R{i+1}")
        raw_label = node.get("label", f"Concept Step {i+1}")
        is_pivot = node.get("is_pivot", False)

        if is_pivot:
            # High-impact Emerald Pivot Node
            formatted_label = f"💡 CRITICAL PIVOT: Step {i+1}\\n{clean_label(raw_label)}"
            if node.get("detail"):
                formatted_label += f"\\n★ {clean_label(node['detail'], 28)}"
            dot_lines.append(
                f'  {node_id} [label="{formatted_label}", color="#047857", fillcolor="#A7F3D0", fontcolor="#064E3B", penwidth=2.8];'
            )
        else:
            formatted_label = f"Step {i+1}: Canonical Step\\n{clean_label(raw_label)}"
            dot_lines.append(
                f'  {node_id} [label="{formatted_label}", color="#10B981", fillcolor="#ECFDF5", fontcolor="#065F46"];'
            )

    dot_lines.append('')
    # Connect sequential nodes
    for i in range(len(remediation_nodes) - 1):
        src = remediation_nodes[i].get("id", f"R{i+1}")
        dst = remediation_nodes[i+1].get("id", f"R{i+2}")
        is_pivot_edge = remediation_nodes[i+1].get("is_pivot", False) or remediation_nodes[i].get("is_pivot", False)
        edge_style = 'color="#047857", penwidth=2.2, label=" scaffolded shift", fontcolor="#065F46", fontsize=9' if is_pivot_edge else 'color="#10B981"'
        dot_lines.append(f'  {src} -> {dst} [{edge_style}];')

    dot_lines.append('}')
    return "\n".join(dot_lines)


def generate_comparative_dual_dot(
    student_nodes: List[Dict[str, Any]],
    remediation_nodes: List[Dict[str, Any]],
    derailment_step_idx: int = 1
) -> str:
    """
    Renders both Map A and Map B side-by-side in a single unified Graphviz canvas
    with a cross-link illustrating the cognitive intervention bridge.
    """
    dot_lines = [
        'digraph ComparativeThoughtMap {',
        '  graph [rankdir=LR, bgcolor="transparent", compound=true, splines=ortho];',
        '  node [fontname="Helvetica, Arial, sans-serif", fontsize=10, shape=box, style="rounded,filled", penwidth=1.6];',
        '  edge [penwidth=1.5, arrowsize=0.8];',
        '',
        '  subgraph cluster_student {',
        '    label="Map A: Student\'s Actual Thinking (Identified Misconceptions)";',
        '    style="rounded,filled"; color="#FECACA"; fillcolor="#FFF1F2";',
        '    fontname="Helvetica-Bold"; fontsize=11; fontcolor="#991B1B";',
        ''
    ]

    for i, node in enumerate(student_nodes):
        node_id = f"st_{node.get('id', i+1)}"
        raw_label = node.get("label", f"Step {i+1}")
        is_error = node.get("is_error", False)
        if is_error:
            lbl = f"⚠️ Node {i+1}: Flawed\\n{clean_label(raw_label)}"
            dot_lines.append(f'    {node_id} [label="{lbl}", color="#EF4444", fillcolor="#FEE2E2", fontcolor="#991B1B", penwidth=2.2];')
        else:
            lbl = f"Node {i+1}: Valid\\n{clean_label(raw_label)}"
            dot_lines.append(f'    {node_id} [label="{lbl}", color="#94A3B8", fillcolor="#FFFFFF", fontcolor="#334155"];')

    for i in range(len(student_nodes) - 1):
        s1 = f"st_{student_nodes[i].get('id', i+1)}"
        s2 = f"st_{student_nodes[i+1].get('id', i+2)}"
        dot_lines.append(f'    {s1} -> {s2} [color="#94A3B8"];')

    dot_lines.extend([
        '  }',
        '',
        '  subgraph cluster_remediation {',
        '    label="Map B: Remediated Conceptual Path (Canonical Scaffold)";',
        '    style="rounded,filled"; color="#A7F3D0"; fillcolor="#F0FDF4";',
        '    fontname="Helvetica-Bold"; fontsize=11; fontcolor="#065F46";',
        ''
    ])

    for i, node in enumerate(remediation_nodes):
        node_id = f"rem_{node.get('id', i+1)}"
        raw_label = node.get("label", f"Step {i+1}")
        is_pivot = node.get("is_pivot", False)
        if is_pivot:
            lbl = f"💡 Pivot Node {i+1}\\n{clean_label(raw_label)}"
            dot_lines.append(f'    {node_id} [label="{lbl}", color="#047857", fillcolor="#A7F3D0", fontcolor="#064E3B", penwidth=2.6];')
        else:
            lbl = f"Step {i+1}: Canonical\\n{clean_label(raw_label)}"
            dot_lines.append(f'    {node_id} [label="{lbl}", color="#10B981", fillcolor="#FFFFFF", fontcolor="#065F46"];')

    for i in range(len(remediation_nodes) - 1):
        r1 = f"rem_{remediation_nodes[i].get('id', i+1)}"
        r2 = f"rem_{remediation_nodes[i+1].get('id', i+2)}"
        dot_lines.append(f'    {r1} -> {r2} [color="#10B981"];')

    dot_lines.extend([
        '  }',
        ''
    ])

    # Bridge edge between student's first error node and remediation pivot node
    error_node_id = None
    for n in student_nodes:
        if n.get("is_error"):
            error_node_id = f"st_{n.get('id')}"
            break
    if not error_node_id and student_nodes:
        error_node_id = f"st_{student_nodes[-1].get('id')}"

    pivot_node_id = None
    for n in remediation_nodes:
        if n.get("is_pivot"):
            pivot_node_id = f"rem_{n.get('id')}"
            break
    if not pivot_node_id and remediation_nodes:
        pivot_node_id = f"rem_{remediation_nodes[0].get('id')}"

    if error_node_id and pivot_node_id:
        dot_lines.append(
            f'  {error_node_id} -> {pivot_node_id} [label=" Pedagogy Pivot", color="#F59E0B", style="dashed", penwidth=2.0, fontcolor="#B45309", fontsize=10];'
        )

    dot_lines.append('}')
    return "\n".join(dot_lines)


def synthesize_multilingual_narration(
    diagnosis: Dict[str, Any],
    target_language: str = "hi-IN",
    is_pure_hindi: bool = False
) -> str:
    """
    Constructs a node-referencing auditory script tailored for Sarvam AI TTS.
    References the student's derailed node and contrasts it with the remediation pivot node.
    Supports both formal Hindi (हिंदी) and hybrid Hinglish (हिंग्लिश).
    """
    concept = diagnosis.get("canonical_concept", "the core concept")
    derailment_step = diagnosis.get("derailment_step", 2)
    misconception = diagnosis.get("canonical_root_misconception", "an intuitive assumption")
    derailment_reason = diagnosis.get("derailment_reason", "the condition was misapplied")
    student_name = diagnosis.get("student_name", "Learner")

    if target_language == "hi-IN":
        if is_pure_hindi:
            return (
                f"नमस्ते {student_name}। अपने विचार मानचित्र के नोड {derailment_step} को ध्यानपूर्वक देखिए। "
                f"यहाँ आपकी सोच मुख्य अवधारणा से विचलित हुई: {misconception}। "
                f"आपने माना कि {derailment_reason[:110]}। "
                f"अब हरे रंग के समाधान मानचित्र में मुख्य पिवट नोड को देखिए: "
                f"जब हम {concept} के बुनियादी नियमों को लागू करते हैं, तो हमें प्रत्यक्ष समीकरणों के बजाय मूल सिद्धांतों से शुरुआत करनी होती है। "
                f"सोचिए, नोड {derailment_step} पर आपकी प्रारंभिक पूर्वधारणा किस तरह असंगत सिद्ध हो रही है?"
            )
        else:
            return (
                f"नमस्ते {student_name}। अपने thought map के Node {derailment_step} को ध्यान से देखिए। "
                f"यहाँ आपकी सोच मुख्य concept से deviate हुई: {misconception}। "
                f"आपने assume किया कि {derailment_reason[:110]}। "
                f"अब green remediation map में Pivot Node को देखिए: "
                f"जब हम {concept} के foundational principles apply करते हैं, तो superficial assumptions के बजाय core rules से start करना होता है। "
                f"सोचिए, Node {derailment_step} पर आपका reasoning किस तरह derail हुआ?"
            )
    elif target_language == "bn-IN":
        return (
            f"নমস্কার {student_name}। আপনার ধারণার মানচিত্রে নোড {derailment_step}-এর দিকে লক্ষ্য করুন। "
            f"এখানে একটি মৌলিক ভুল ঘটেছে: {misconception}। "
            f"সবুজ প্রতিকার মানচিত্রে পিভট নোডটি দেখুন, যা মূল বৈজ্ঞানিক নীতিকে স্পষ্ট করে। "
            f"আপনি কি বুঝতে পারছেন কেন এই ধাপে সরাসরি সূত্র প্রয়োগ কাজ করেনি?"
        )
    elif target_language == "mr-IN":
        return (
            f"नमस्कार {student_name}। आपल्या विचार नकाशातील नोड {derailment_step} कडे काळजीपूर्वक पहा. "
            f"येथे आपली विचारसरणी विचलित झाली आहे: {misconception}। "
            f"हिरव्या उपायाच्या नकाशातील पिव्हट नोड दाखवतो की {concept} मध्ये मूळ भौतिक नियमांचा वापर करणे आवश्यक आहे. "
            f"या नोडवर आपण कोणत्या गृहितकामध्ये चूक केली, याचा पुनर्विचार करा."
        )
    elif target_language == "ta-IN":
        return (
            f"வணக்கம் {student_name}. உங்கள் சிந்தனை வரைபடத்தில் நோட் {derailment_step}-ஐ கவனியுங்கள். "
            f"இங்கே ஒரு முக்கியமான தவறான கருத்து ஏற்பட்டுள்ளது: {misconception}. "
            f"பச்சை நிற தீர்வு வரைபடத்தில் உள்ள முக்கிய மாற்றுக் குறிப்பை பாருங்கள். "
            f"இந்த மாற்றுக் கட்டத்தில் உங்கள் ஆரம்ப அணுகுமுறை எவ்வாறு மாற வேண்டும் என்பதை யோசியுங்கள்."
        )
    elif target_language == "te-IN":
        return (
            f"నమస్కారం {student_name}. మీ కాన్సెప్ట్ మ్యాప్‌లోని నోడ్ {derailment_step} ను గమనించండి. "
            f"ఇక్కడ ప్రాథమిక లోపం జరిగింది: {misconception}. "
            f"ఆకుపచ్చ రంగు పరిష్కార మ్యాప్‌లోని పివట్ నోడ్ సరైన మార్గాన్ని సూచిస్తుంది. "
            f"ఈ దశలో మీరు చేసిన తప్పును ఎలా సరిదిద్దవచ్చో ఒకసారి ఆలోచించండి."
        )
    else:  # en-IN or default
        return (
            f"Look at Node {derailment_step} in your graph: you encountered a misconception regarding {misconception}. "
            f"Specifically: {derailment_reason[:120]}. "
            f"However, as highlighted in the emerald green remediation map at the Pivot Node, "
            f"we must examine {concept} through foundational principles and governing constraints. "
            f"Notice how this directly pivots your reasoning towards sound analysis."
        )


def diagnose_doubt_semantic(
    doubt: str,
    student_concept: str,
    student_steps: str,
    student_breakdown: str,
    learner_context: str = "",
    preferred_language: str = "hi-IN",
    student_name: str = "Learner",
    output_lang_name: str = "Hinglish (हिंग्लिश)"
) -> Dict[str, Any]:
    """
    Intelligent pedagogical diagnostic engine.
    Matches predefined curricular concepts or dynamically analyzes custom doubts.
    Strictly forbids direct solutions, providing scaffolded Graphviz maps,
    misconception taxonomy, and Socratic guidance.
    Supports pure Hindi (हिंदी) and hybrid Hinglish (हिंग्लिश) separately.
    """
    # Check if this matches one of our curated sample doubts
    doubt_lower = (doubt + " " + student_concept + " " + student_steps).lower()

    matched_key = None
    if any(k in doubt_lower for k in ["speech", "article 19", "auditorium", "incitement", "public order", "वाक्", "अभिव्यक्ति", "भाषण"]):
        matched_key = "law_freedom_of_speech"
    elif any(k in doubt_lower for k in ["sarajevo", "ferdinand", "world war", "ww1", "wwi", "alliances", "हत्याकांड", "विश्व युद्ध"]):
        matched_key = "history_ww1_causality"
    elif any(k in doubt_lower for k in ["macbeth", "hamartia", "shakespeare", "witches", "duncan", "tragic flaw", "मैकबेथ"]):
        matched_key = "literature_macbeth_tragic_flaw"
    elif any(k in doubt_lower for k in ["rent control", "price ceiling", "housing", "किराया", "आवास", "deadweight"]) or bool(re.search(r"\brent\b", doubt_lower)):
        matched_key = "economics_rent_control"
    elif any(k in doubt_lower for k in ["parentheses", "bracket", "balanced", "कोष्ठक"]):
        matched_key = "coding_balanced_parentheses"
    elif any(k in doubt_lower for k in ["rough", "friction", "spring", "घर्षण", "स्प्रिंग"]):
        matched_key = "spring_friction_energy"
    elif any(k in doubt_lower for k in ["horse", "cart", "action", "घोड़ा"]):
        matched_key = "newton_third_law_horse_cart"
    elif any(k in doubt_lower for k in ["circular", "centrifugal", "turn", "curve", "loop"]):
        matched_key = "circular_motion_turn"
    elif any(k in doubt_lower for k in ["skater", "spin", "angular momentum", "torque", "moment of inertia"]):
        matched_key = "rotational_skater_spin"
    elif any(k in doubt_lower for k in ["a(t)", "variable", "v = u + at", "3t"]):
        matched_key = "kinematics_variable_acc"
    elif any(k in doubt_lower for k in ["haber", "catalyst", "le chatelier", "nh3"]):
        matched_key = "chemistry_le_chatelier_catalyst"

    sample = get_sample_doubt_entry(matched_key)
    if sample:
        student_nodes = sample.get("student_nodes", [])
        remediation_nodes = sample.get("remediation_nodes", [])
        derailment_step = sample.get("derailment_step", 2)
        root_misconception = sample.get("canonical_root_misconception", "")
        canonical_concept = sample.get("canonical_concept", "")
        derailment_reason = sample.get("derailment_reason", "")
        socratic_prompt = sample.get("socratic_prompt", "")
    else:
        # Dynamic Heuristic Decomposition for custom student queries
        canonical_concept = student_concept if student_concept else "Core Analytical Principle"
        root_misconception = "Unverified Premise or Overgeneralization at Step 2"
        derailment_step = 2
        derailment_reason = (
            f"Applied general rules or heuristics without verifying underlying constraints. "
            f"Intuition broke down at: {student_breakdown[:100] if student_breakdown else 'reasoning boundary'}."
        )
        
        # Build dynamic student nodes from their input
        raw_lines = [l.strip() for l in student_steps.split("\n") if l.strip()]
        if not raw_lines:
            raw_lines = ["Premise: Stated initial conditions", "Formulated approach", "Reached stuck point"]
            
        student_nodes = []
        for i, line in enumerate(raw_lines[:5]):
            is_err = (i >= 1)  # Flag subsequent steps as containing the misconception
            student_nodes.append({
                "id": f"S{i+1}",
                "label": line[:60],
                "is_error": is_err,
                "detail": "Cognitive derailment: unverified assumption" if is_err else "Initial premise"
            })

        remediation_nodes = [
            {"id": "R1", "label": f"Identify System Boundaries & Constraints for {canonical_concept[:25]}", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Return to First-Principles Definition & Core Constraints", "is_pivot": True, "detail": "Breakthrough: Isolate independent and dependent variables or constraints"},
            {"id": "R3", "label": "Formulate Remediated Argument with Governing Conditions", "is_pivot": False},
            {"id": "R4", "label": "Verify Logical Consistency & Check Edge Conditions", "is_pivot": False}
        ]
        socratic_prompt = (
            f"Look back at your Step {derailment_step}: Under what exact assumptions or governing conditions does that premise hold true? "
            f"Does your scenario satisfy those conditions, or is a critical constraint overlooked?"
        )

    # Build Graphviz DOT strings
    dot_map_a = generate_map_a_dot(student_nodes, "Map A: Student's Actual Reasoning Path")
    dot_map_b = generate_map_b_dot(remediation_nodes, "Map B: Remediated Conceptual Path")
    dot_comparative = generate_comparative_dual_dot(student_nodes, remediation_nodes, derailment_step)

    # Package diagnosis
    diag_summary = {
        "student_name": student_name,
        "canonical_concept": canonical_concept,
        "canonical_root_misconception": root_misconception,
        "derailment_step": derailment_step,
        "derailment_reason": derailment_reason,
        "severity": "High" if derailment_step <= 2 else "Medium",
        "student_nodes": student_nodes,
        "remediation_nodes": remediation_nodes,
        "dot_map_a": dot_map_a,
        "dot_map_b": dot_map_b,
        "dot_comparative": dot_comparative,
        "socratic_prompt": socratic_prompt,
    }

    # Detect if user specifically chose pure Hindi (हिंदी) vs Hinglish (हिंग्लिश)
    is_pure_hindi = ("Hindi" in output_lang_name or "हिंदी" in output_lang_name) and ("Hinglish" not in output_lang_name and "हिंग्लिश" not in output_lang_name)

    # Generate multilingual voice script tailored to student's language
    if sample:
        if is_pure_hindi and sample.get("socratic_prompt_hi"):
            diag_summary["socratic_prompt"] = sample["socratic_prompt_hi"]

        if is_pure_hindi and sample.get("narration_pure_hi"):
            narration_script = sample["narration_pure_hi"]
        elif (preferred_language == "hi-IN" or "Hinglish" in output_lang_name or "हिंग्लिश" in output_lang_name) and sample.get("narration_hi"):
            narration_script = sample["narration_hi"]
        elif preferred_language == "en-IN" and sample.get("narration_en"):
            narration_script = sample["narration_en"]
        else:
            base_script = sample.get("narration_en", "")
            try:
                import sarvam_tts
                narration_script = sarvam_tts.translate_with_sarvam_hybrid(base_script, preferred_language)
            except Exception:
                narration_script = synthesize_multilingual_narration(diag_summary, preferred_language, is_pure_hindi=is_pure_hindi)
    else:
        narration_script = synthesize_multilingual_narration(diag_summary, preferred_language, is_pure_hindi=is_pure_hindi)

    diag_summary["narration_script"] = narration_script
    diag_summary["concept_diagnostics"] = generate_concept_diagnostician_profile(
        diag_summary,
        doubt=doubt,
        student_concept=student_concept,
        student_steps=student_steps,
        matched_key=matched_key
    )
    diag_summary["board_storyboard"] = generate_live_board_storyboard(
        diag_summary,
        doubt=doubt,
        student_concept=student_concept,
        student_steps=student_steps,
        matched_key=matched_key,
        output_lang_name=output_lang_name
    )

    return diag_summary


def generate_concept_diagnostician_profile(
    diag_summary: Dict[str, Any],
    doubt: str = "",
    student_concept: str = "",
    student_steps: str = "",
    matched_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Constructs a strict cognitive-profiling and learning-analytics record
    as 'Bhasha Concept Diagnostician'.
    Adheres strictly to the 4-step diagnostic protocol and taxonomy schema.
    """
    if matched_key == "spring_friction_energy":
        return {
            "topic_taxonomy": {
                "domain": "Physics",
                "primary_topic": "Classical Mechanics (Work & Energy)",
                "micro_concept_fault_line": "Non-conservative dissipative work during spring compression",
                "concept_tags": ["Work-Energy Theorem", "Friction Dissipation", "Conservation of Mechanical Energy"]
            },
            "student_mental_model": {
                "flawed_opinion_summary": "The student equates initial gravitational potential energy directly to elastic spring energy, assuming mechanical energy is strictly conserved across a dissipative rough surface.",
                "cognitive_fallacy_type": "Over-Generalization",
                "root_cause_explanation": "The student has internalized the mechanical energy conservation formula mgh = 0.5 k x^2 from idealized frictionless examples, leading them to overlook the dissipative work done by friction along the incline."
            },
            "mastery_assessment": {
                "status": "INTUITIVELY_CLOSE",
                "solid_foundations_demonstrated": [
                    "Correct identification of initial gravitational potential energy converting into terminal spring compression",
                    "Accurate formulation of elastic spring potential energy (1/2 k x^2)"
                ],
                "vulnerable_prerequisites": [
                    "Work-Energy theorem for non-conservative dissipative forces (Delta E = W_nc)",
                    "Free Body Diagram decomposition of normal force and friction on an inclined plane"
                ]
            },
            "remediation_recommendations": {
                "mental_model_reframe": "Think of mechanical energy as money in a wallet. Moving across a rough surface is a mandatory toll fee that deducts cash. The spring only receives whatever balance remains after the friction toll is paid.",
                "suggested_study_topics": [
                    "Work-Energy Theorem with dissipative forces: Delta K + Delta U = W_friction",
                    "Path-dependent non-conservative work: W_f = -mu * m * g * d * cos(theta)"
                ],
                "diagnostic_self_check": "If a block with 100 J of potential energy slides down an incline where friction dissipates 30 J of thermal work before hitting an ideal spring, how much energy is stored in the spring?"
            },
            "sarvam_narration_script": "You had a sound intuition that potential energy transfers into spring compression. But notice where reality diverged: because the surface has friction, it performs negative work and dissipates energy as heat. Instead of equating mgh directly to spring energy, subtract friction work first. Review the work-energy theorem for non-conservative systems in your next study session."
        }
    elif matched_key == "economics_rent_control":
        return {
            "topic_taxonomy": {
                "domain": "Economics",
                "primary_topic": "Microeconomics (Price Controls & Market Equilibrium)",
                "micro_concept_fault_line": "Supply elasticity and deadweight loss under binding price ceilings",
                "concept_tags": ["Price Ceilings", "Deadweight Loss", "Supply Elasticity"]
            },
            "student_mental_model": {
                "flawed_opinion_summary": "The student assumes legally capping rent below equilibrium price increases the total quantity of affordable housing supplied.",
                "cognitive_fallacy_type": "Contextual Blindspot",
                "root_cause_explanation": "The student focuses solely on the demand side (lower rent means more tenants can afford housing) while ignoring supplier incentive response (landlords exit the market or defer maintenance when marginal revenue drops below operating costs)."
            },
            "mastery_assessment": {
                "status": "INTUITIVELY_CLOSE",
                "solid_foundations_demonstrated": [
                    "Understanding that price ceilings make units more affordable for tenants who manage to secure them",
                    "Recognition of the basic downward slope of the consumer demand curve"
                ],
                "vulnerable_prerequisites": [
                    "Price elasticity of supply across short vs long run horizons",
                    "Graphical analysis of shortage and deadweight loss under price ceilings"
                ]
            },
            "remediation_recommendations": {
                "mental_model_reframe": "Setting a price ceiling does not force sellers to produce more; it only makes it illegal to pay more. When selling is capped below cost, producers stop selling, creating a shortage.",
                "suggested_study_topics": [
                    "Market Equilibrium with government price interventions (Ceilings vs Floors)",
                    "Deadweight loss and rationing mechanisms beyond price signals"
                ],
                "diagnostic_self_check": "If the equilibrium rent is $1,000 and the city caps rent at $700, what happens to the quantity of rental units supplied if supply is elastic?"
            },
            "sarvam_narration_script": "Your intuition that lower prices help tenants is completely understandable. But notice where economic reality diverged: price ceilings only cap what buyers pay; they do not compel landlords to maintain supply. In the long run, lower rents reduce the quantity supplied, resulting in housing shortages. In your next review, study supply elasticity under price controls."
        }
    elif matched_key == "coding_balanced_parentheses":
        return {
            "topic_taxonomy": {
                "domain": "Computer Science",
                "primary_topic": "Data Structures & Algorithms (Stack Invariants)",
                "micro_concept_fault_line": "Stack non-emptiness invariant and unclosed opening delimiter detection",
                "concept_tags": ["Stack Data Structure", "LIFO Invariant", "Delimiter Matching"]
            },
            "student_mental_model": {
                "flawed_opinion_summary": "The student concludes that because every closing bracket had a valid matching opening bracket, the string is balanced, neglecting unmatched remaining open brackets.",
                "cognitive_fallacy_type": "Boundary Condition Blindness",
                "root_cause_explanation": "The student tested only the matching trigger condition inside the iteration loop without verifying the post-loop stack invariant (stack.isEmpty())."
            },
            "mastery_assessment": {
                "status": "INTUITIVELY_CLOSE",
                "solid_foundations_demonstrated": [
                    "Correct selection of a LIFO Stack data structure for nested delimiter tracking",
                    "Accurate bracket pairing and type-matching logic during traversal"
                ],
                "vulnerable_prerequisites": [
                    "Loop invariants and post-condition assertions",
                    "Boundary cases with asymmetric delimiter counts"
                ]
            },
            "remediation_recommendations": {
                "mental_model_reframe": "A stack is like an open tab at a diner. Paying for every item you ordered is necessary, but the bill is only settled if the tab is completely zero at checkout.",
                "suggested_study_topics": [
                    "Stack invariants: pre-condition, in-loop condition, and terminal condition",
                    "Edge case testing: asymmetric strings with remaining open tokens"
                ],
                "diagnostic_self_check": "What does a balanced parentheses parser return for the input string '((())' if it only checks bracket matches inside the loop?"
            },
            "sarvam_narration_script": "Great job choosing a stack for nested bracket matching. Your logic correctly paired every closing token. Where it derailed was at the boundary: you forgot to verify that the stack was completely empty after the loop ended. Unclosed opening brackets must also be caught. Focus on stack terminal conditions and invariants during your next practice session."
        }
    elif matched_key == "law_freedom_of_speech":
        return {
            "topic_taxonomy": {
                "domain": "Law",
                "primary_topic": "Constitutional Law (Fundamental Rights & State Limits)",
                "micro_concept_fault_line": "Reasonable restrictions under Article 19(2) and the incitement / proximate causation test",
                "concept_tags": ["Article 19(1)(a)", "Reasonable Restrictions", "Public Order Exception"]
            },
            "student_mental_model": {
                "flawed_opinion_summary": "The student assumes Article 19(1)(a) freedom of speech is an absolute immunity, exempt from police intervention regardless of context or imminent public disorder.",
                "cognitive_fallacy_type": "Over-Generalization",
                "root_cause_explanation": "The student learned the broad constitutional guarantee of free expression but treated it in isolation, ignoring that fundamental rights in the Indian Constitution are subject to reasonable restrictions under Article 19(2)."
            },
            "mastery_assessment": {
                "status": "INTUITIVELY_CLOSE",
                "solid_foundations_demonstrated": [
                    "Accurate identification of Article 19(1)(a) as the primary constitutional shield for expression",
                    "Sound recognition that critical or dissenting viewpoints enjoy constitutional protection"
                ],
                "vulnerable_prerequisites": [
                    "Constitutional limitations under Article 19(2): public order, incitement, and sovereignty",
                    "Judicial doctrine of proximate relation: speech vs imminent lawless action"
                ]
            },
            "remediation_recommendations": {
                "mental_model_reframe": "Fundamental rights are not blank checks. Free speech protects expression, but stops at the boundary where words directly and proximately incite imminent violence or breach public order.",
                "suggested_study_topics": [
                    "Article 19(2) enumerated grounds for reasonable restrictions",
                    "Landmark judicial precedents: Ramji Lal Modi and Shreya Singhal on proximate nexus"
                ],
                "diagnostic_self_check": "Under Article 19(2), can the State restrict speech that merely offends someone, or must there be a clear and proximate danger to public order?"
            },
            "sarvam_narration_script": "You rightly recognized that Article 19 protects robust freedom of speech and dissent. But notice where legal interpretation diverged: constitutional rights are not absolute. Under Article 19 clause 2, speech that directly incites imminent violence or breaches public order can be reasonably restricted. In your next study session, explore the judicial tests balancing free expression with public safety."
        }
    elif matched_key == "history_ww1_causality":
        return {
            "topic_taxonomy": {
                "domain": "History",
                "primary_topic": "Modern World History (World War I & Diplomatic Systems)",
                "micro_concept_fault_line": "Monocausal teleology conflating proximate spark with structural M-A-I-N causation",
                "concept_tags": ["Causes of World War I", "M-A-I-N Framework", "July Crisis", "Alliance Systems"]
            },
            "student_mental_model": {
                "flawed_opinion_summary": "The student concludes that the Sarajevo assassination of Franz Ferdinand was the sole sufficient cause that forced Europe into total war.",
                "cognitive_fallacy_type": "Causality Inversion",
                "root_cause_explanation": "The student focuses exclusively on the chronological trigger event while failing to recognize the systemic powder keg of rigid alliance treaties, militarism, and imperial competition."
            },
            "mastery_assessment": {
                "status": "INTUITIVELY_CLOSE",
                "solid_foundations_demonstrated": [
                    "Accurate recall of the June 1914 Sarajevo assassination as the trigger of the July Crisis",
                    "Understanding that diplomatic ultimatums set military mobilizations in motion"
                ],
                "vulnerable_prerequisites": [
                    "Differentiating immediate catalysts from long-term structural preconditions in historical analysis",
                    "The European alliance structure (Triple Entente vs Triple Alliance) and mobilization timetables"
                ]
            },
            "remediation_recommendations": {
                "mental_model_reframe": "Think of a forest fire during an extreme drought. A single dropped match sparks the flame, but the disaster is determined by miles of dry timber accumulated over years.",
                "suggested_study_topics": [
                    "The M-A-I-N framework: Militarism, Alliances, Imperialism, and Nationalism leading to 1914",
                    "The Schlieffen Plan and European railway mobilization schedules"
                ],
                "diagnostic_self_check": "If the Sarajevo crisis had been diplomatically defused, why did the structural tensions in Europe make general conflict highly likely in the 1910s?"
            },
            "sarvam_narration_script": "You correctly identified the Sarajevo assassination as the immediate catalyst of the July Crisis. But notice where historical analysis diverged: a single murder was only the match. Decades of militarism, entangling secret treaties, and imperial rivalry created the combustible fuel. In your next study session, focus on how structural causes turned a localized dispute into a world war."
        }
    elif matched_key == "literature_macbeth_tragic_flaw":
        return {
            "topic_taxonomy": {
                "domain": "Literature",
                "primary_topic": "Dramatic Theory & Shakespearean Tragedy (Macbeth)",
                "micro_concept_fault_line": "Denial of moral agency and misattribution of tragic hamartia to external catalysts",
                "concept_tags": ["Shakespearean Tragedy", "Hamartia", "Moral Agency", "Vaulting Ambition"]
            },
            "student_mental_model": {
                "flawed_opinion_summary": "The student views Macbeth as an innocent victim wholly manipulated by the supernatural Weird Sisters and Lady Macbeth, with no personal tragic culpability.",
                "cognitive_fallacy_type": "Term Conflation",
                "root_cause_explanation": "The student conflates external temptation and psychological persuasion with irresistible physical coercion, stripping the tragic hero of voluntary moral agency."
            },
            "mastery_assessment": {
                "status": "INTUITIVELY_CLOSE",
                "solid_foundations_demonstrated": [
                    "Textual analysis of the witches' prophecies and Lady Macbeth's rhetorical persuasion",
                    "Recognition of Macbeth's moral distress and psychological terror before the murder"
                ],
                "vulnerable_prerequisites": [
                    "The Aristotelian definition of the tragic hero: hamartia requires conscious moral choice",
                    "Contrasting character foils: Banquo's moral restraint versus Macbeth's complicity"
                ]
            },
            "remediation_recommendations": {
                "mental_model_reframe": "External catalysts are mirrors, not puppeteers. The witches and Lady Macbeth held up the mirror, but it was Macbeth's own vaulting ambition that drew the dagger.",
                "suggested_study_topics": [
                    "Hamartia in Shakespearean tragedy: Fatal flaw versus external fate",
                    "Macbeth's soliloquies in Act 1: The anatomy of conscious ambition"
                ],
                "diagnostic_self_check": "Why does Banquo, who heard the exact same supernatural prophecy, choose not to scheme or murder to fulfill it?"
            },
            "sarvam_narration_script": "You accurately captured the intense persuasion of the witches and Lady Macbeth. But notice where literary analysis diverged: in classical tragedy, external temptation does not absolve the hero of moral agency. Macbeth acknowledges his own driving motive: vaulting ambition. Contrast him with Banquo, who chose moral restraint. Focus on tragic hamartia and free will in your next review."
        }
    else:
        # Dynamic fallback for arbitrary queries
        return {
            "topic_taxonomy": {
                "domain": "Cross-Disciplinary Academic Reasoning",
                "primary_topic": diag_summary.get("canonical_concept", "Core Analytical Concept"),
                "micro_concept_fault_line": diag_summary.get("canonical_root_misconception", "Boundary Condition Misapplication"),
                "concept_tags": [diag_summary.get("canonical_concept", "Concept"), "Conceptual Diagnostics", "First Principles"]
            },
            "student_mental_model": {
                "flawed_opinion_summary": f"The student applies general rules without verifying underlying constraints: {diag_summary.get('derailment_reason', '')[:120]}",
                "cognitive_fallacy_type": "Over-Generalization",
                "root_cause_explanation": f"The student relied on an intuitive shortcut at Step {diag_summary.get('derailment_step', 2)}, missing key contextual boundary conditions."
            },
            "mastery_assessment": {
                "status": "INTUITIVELY_CLOSE",
                "solid_foundations_demonstrated": [
                    "Formulated a structured initial approach",
                    "Identified the relevant primary domain laws"
                ],
                "vulnerable_prerequisites": [
                    "Verification of boundary conditions and governing assumptions",
                    "System boundary isolation"
                ]
            },
            "remediation_recommendations": {
                "mental_model_reframe": "Anchor reasoning in governing constraints before applying formulas or doctrines.",
                "suggested_study_topics": [
                    f"Foundational principles of {diag_summary.get('canonical_concept', 'this topic')}",
                    "Boundary conditions and constraint verification"
                ],
                "diagnostic_self_check": "Before applying your formula or rule, what specific preconditions must the system satisfy?"
            },
            "sarvam_narration_script": f"You made a strong start articulating your reasoning on {diag_summary.get('canonical_concept', 'this topic')}. Notice that at step {diag_summary.get('derailment_step', 2)}, an unverified assumption caused your logic to branch away from reality. Check the core governing constraints in your next review."
        }


STORYBOARD_LOCALIZED_SEGMENTS: Dict[str, Dict[str, Any]] = {
    "spring_friction_energy": {
        "hinglish": [
            "Pehle dekhte hain aapne kya sahi socha: block height h se release hota hai.",
            "Aapne bilkul theek pehchana ki gravity positive work karti hai downward motion mein.",
            "Ab yahan dekhiye: aapne assume kiya ki total mechanical energy strictly conserve rahegi.",
            "Stop right there! Track par ek rough patch hai jahan friction energy ko dissipate kar deta hai.",
            "Iske bajaye, is branch par aaiye jahan hum friction ka work subtract karenge.",
            "Hamara corrected path banega: m g h minus mu times m times g times distance equals half k x squared."
        ],
        "hi": [
            "आइए पहले देखें कि आपने क्या सही सोचा: गुटका ऊंचाई h से गति आरंभ करता है।",
            "आपने बिल्कुल सही पहचाना कि नीचे आते समय गुरुत्वाकर्षण धनात्मक कार्य करता है।",
            "अब यहाँ ध्यान दीजिए: आपने माना कि कुल यांत्रिक ऊर्जा पूर्णतः संरक्षित रहती है।",
            "यहाँ रुकिए! ट्रैक पर घर्षण मौजूद है, जो ऊर्जा को ऊष्मा के रूप में क्षय कर देता है।",
            "इसके बजाय, इस शाखा पर आइए जहाँ हम घर्षण द्वारा किए गए कार्य को घटाते हैं।",
            "हमारा संशोधित समीकरण होगा: m g h ऋण mu times m times g times d = half k x squared।"
        ],
        "challenge_hinglish": "Spring ko touch karne se pehle 3-meter ke rough patch par friction kitni mechanical energy dissipate karta hai?",
        "challenge_hi": "स्प्रिंग को स्पर्श करने से पहले 3 मीटर के खुरदरे तल पर घर्षण कितनी यांत्रिक ऊर्जा का क्षय करता है?"
    },
    "economics_rent_control": {
        "hinglish": [
            "Pehle market setup dekhte hain: equilibrium rent ek hazaar dollars hai paanch hazaar apartments ke liye.",
            "Aapne theek identify kiya ki price drop hone par tenants zyada demand karenge.",
            "Ab yahan dekhiye: aapne assume kiya ki is rent ceiling ke baad total supply badh jayegi.",
            "Stop right there! Jab rent operating cost se kam ho jaye, toh landlords supply kam kar dete hain.",
            "Iske bajaye, supply curve par aaiye jahan price ceiling ek severe shortage create karti hai.",
            "Corrected path: rent control se supply drop hoti hai aur deadweight loss create hota hai."
        ],
        "hi": [
            "आइए बाज़ार का संतुलन देखें: साम्य किराया एक हज़ार डॉलर है पाँच हज़ार आवासों के लिए।",
            "आपने सही समझा कि किराया घटने पर किरायेदार अधिक आवासों की मांग करेंगे।",
            "अब यहाँ ध्यान दीजिए: आपने माना कि इस मूल्य सीमा के बाद कुल आपूर्ति बढ़ जाएगी।",
            "यहाँ रुकिए! जब किराया लागत से कम हो जाता है, तब मकान मालिक आपूर्ति घटा देते हैं।",
            "इसके बजाय, आपूर्ति वक्र पर आइए जहाँ मूल्य सीमा से गंभीर अभाव उत्पन्न होता है।",
            "संशोधित मार्ग: किराया नियंत्रण से आपूर्ति में भारी कमी और मृतभार हानि होती है।"
        ],
        "challenge_hinglish": "Agar rental supply long run mein elastic hai, toh time ke sath housing shortage par kya effect padega?",
        "challenge_hi": "यदि दीर्घावधि में किराये की आपूर्ति लोचदार है, तो समय के साथ आवासों की कमी के आकार पर क्या प्रभाव पड़ेगा?"
    },
    "law_freedom_of_speech": {
        "hinglish": [
            "Pehle constitutional basis dekhte hain: Article 19(1)(a) speech aur expression ki azaadi deta hai.",
            "Aapne theek note kiya ki Article 19(2) ke under reasonable restrictions lag sakti hain.",
            "Ab yahan dekhiye: aapne assume kiya ki closed hall mein provocative opinion public disorder hai.",
            "Stop right there! Supreme Court kehti hai ki speech aur disorder ke beech direct spark in a powder keg jaisa proximate nexus hona chahiye.",
            "Iske bajaye, Ram Manohar Lohia case ke proximate nexus test par aaiye.",
            "Corrected path: closed private meeting ko tab tak curtail nahi kar sakte jab tak imminent violence ka khatra na ho."
        ],
        "hi": [
            "आइए संवैधानिक आधार देखें: अनुच्छेद 19(1)(क) विचार और अभिव्यक्ति की स्वतंत्रता प्रदान करता है।",
            "आपने सही पहचाना कि अनुच्छेद 19(2) के तहत लोक व्यवस्था पर युक्तियुक्त निर्बंधन लगाए जा सकते हैं।",
            "अब यहाँ ध्यान दीजिए: आपने माना कि बंद सभागार में विवादास्पद विचार लोक व्यवस्था का उल्लंघन है।",
            "यहाँ रुकिए! उच्चतम न्यायालय के अनुसार भाषण और अव्यवस्था के बीच बारूद में चिंगारी जैसा प्रत्यक्ष संबंध होना चाहिए।",
            "इसके बजाय, राम मनोहर लोहिया मामले के सन्निकट संबंध परीक्षण पर आइए।",
            "संशोधित मार्ग: किसी बंद निजी बैठक को तब तक नहीं रोका जा सकता जब तक हिंसा का आसन्न खतरा न हो।"
        ],
        "challenge_hinglish": "Ek ordinary law and order issue aur public order ke grave threat ke beech crucial legal difference kya hai?",
        "challenge_hi": "एक सामान्य कानून-व्यवस्था के मुद्दे और लोक व्यवस्था के गंभीर खतरे के बीच क्या विधिक अंतर है?"
    },
    "history_ww1_causality": {
        "hinglish": [
            "Pehle historical evidence dekhte hain: Archduke Franz Ferdinand ka assassination Sarajevo mein 28 June ko hua tha.",
            "Aapne theek note kiya ki yeh assassination July diplomatic crisis ka immediate spark tha.",
            "Ab yahan dekhiye: aapne conclude kar liya ki sirf is ek assassination ne poora world war kara diya.",
            "Stop right there! Assassination sirf ek matchstick thi; bina structural tinderbox ke world war ignite nahi ho sakta tha.",
            "Iske bajaye, structural alliance networks aur imperial rivalries par aaiye.",
            "Corrected path: M-A-I-N framework - militarism, alliances, imperialism aur nationalism ne war create kiya."
        ],
        "hi": [
            "आइए ऐतिहासिक साक्ष्य देखें: साराजेवो में 28 जून 1914 को आर्चड्यूक फ्रांज फर्डिनेंड की हत्या हुई।",
            "आपने सही पहचाना कि यह घटना जुलाई के राजनयिक संकट की तात्कालिक चिंगारी थी।",
            "अब यहाँ ध्यान दीजिए: आपने निष्कर्ष निकाला कि केवल इस एक हत्या ने पूरे विश्व युद्ध को जन्म दिया।",
            "यहाँ रुकिए! यह हत्या केवल एक माचिस की तीली थी; बिना संरचनात्मक बारूद के विश्व युद्ध नहीं भड़क सकता था।",
            "इसके बजाय, गुप्त संधियों, सैन्यीकरण और साम्राज्यवादी प्रतिद्वंद्विता पर आइए।",
            "संशोधित मार्ग: सैन्यवाद, गठबंधन, साम्राज्यवाद और राष्ट्रवाद ने युद्ध की पृष्ठभूमि तैयार की।"
        ],
        "challenge_hinglish": "Rigid railway mobilization timetables aur secret treaties ne localized Balkan crisis ko world war mein kaise convert kiya?",
        "challenge_hi": "रेलवे लामबंदी की कठोर समय-सारिणी और गुप्त संधियों ने बाल्कन के स्थानीय संघर्ष को विश्व युद्ध में कैसे बदल दिया?"
    },
    "literature_macbeth_tragic_flaw": {
        "hinglish": [
            "Pehle dramatic setup dekhte hain: Weird Sisters Macbeth ko king banne ki prophecy sunati hain.",
            "Aapne theek identify kiya ki external prophecy aur Lady Macbeth ka manipulation kaafi powerful tha.",
            "Ab yahan dekhiye: aapne claim kiya ki Macbeth ek innocent victim tha jiske paas koi moral agency nahi thi.",
            "Stop right there! Aristotelian tragedy mein external prophecy hero ki free will aur moral responsibility ko khatam nahi karti.",
            "Iske bajaye, Macbeth ke apne confession aur internal flaw par aaiye.",
            "Corrected path: Aristotelian Hamartia - tragedy ka root cause Macbeth ka vaulting ambition aur deliberate choice hai."
        ],
        "hi": [
            "आइए नाटक का संदर्भ देखें: तीन रहस्यमयी बहनें मैकबेथ के राजा बनने की भविष्यवाणी करती हैं।",
            "आपने सही पहचाना कि बाहरी भविष्यवाणी और लेडी मैकबेथ का प्रभाव अत्यंत प्रबल था।",
            "अब यहाँ ध्यान दीजिए: आपने माना कि मैकबेथ परिस्थितियों का असहाय शिकार था और उसके पास कोई नैतिक स्वतंत्रता नहीं थी।",
            "यहाँ रुकिए! अरस्तू की त्रासदी में बाहरी परिस्थितियां नायक के स्वतंत्र नैतिक चयन को समाप्त नहीं करती हैं।",
            "इसके बजाय, मैकबेथ के आंतरिक दोष और उसकी स्वीकारोक्ति पर ध्यान दीजिए।",
            "संशोधित मार्ग: ट्रैजिक फ्लॉ (हमारशिया) - त्रासदी का मूल कारण मैकबेथ की अनियंत्रित महत्वाकांक्षा और उसका स्वेच्छा से लिया गया निर्णय है।"
        ],
        "challenge_hinglish": "Same supernatural prophecy sunne ke baad bhi Banquo ne moral control rakha jabki Macbeth ne regicide plot kyun kiya?",
        "challenge_hi": "समान अलौकिक भविष्यवाणी सुनने के बाद भी बैंको ने नैतिक संयम रखा, जबकि मैकबेथ ने राजा की हत्या क्यों की?"
    },
    "coding_balanced_parentheses": {
        "hinglish": [
            "Pehle aapka algorithmic design dekhte hain: aap delimiters ko track karne ke liye LIFO stack use kar rahe hain.",
            "Aapne matching closing delimiter aane par stack se top bracket ko correctly pop kiya.",
            "Ab yahan dekhiye: loop finish hote hi aapne directly return true kar diya.",
            "Stop right there! Agar string ke baad stack mein unclosed opening brackets bache reh gaye toh kya hoga?",
            "Iske bajaye, traversal ke baad terminal stack invariant enforce karne par aaiye.",
            "Corrected invariant: balanced string ke liye exit point par stack completely empty hona chahiye, yaani return stack.isEmpty()."
        ],
        "hi": [
            "आइए आपका एल्गोरिदम देखें: आप कोष्ठकों की जांच के लिए स्टैक (LIFO) का उपयोग कर रहे हैं।",
            "आपने बंद कोष्ठक आने पर शीर्ष तत्व को सही ढंग से पॉप और सुमेलित किया।",
            "अब यहाँ ध्यान दीजिए: लूप समाप्त होते ही आपने सीधे सत्य (true) लौटा दिया।",
            "यहाँ रुकिए! यदि स्ट्रिंग समाप्त होने के बाद भी स्टैक में खुले कोष्ठक शेष रह जाएं तो क्या होगा?",
            "इसके बजाय, लूप के बाद स्टैक के अंतिम नियम का सत्यापन करने पर आइए।",
            "संशोधित नियम: संतुलित स्ट्रिंग के लिए अंत में स्टैक का पूर्णतः रिक्त होना अनिवार्य है।"
        ],
        "challenge_hinglish": "Teen opening aur do closing brackets jaise asymmetric string ke liye aapka code kya return karega?",
        "challenge_hi": "तीन खुले और दो बंद कोष्ठकों जैसी असममित स्ट्रिंग के लिए आपका कोड क्या मान लौटाएगा?"
    }
}


def generate_live_board_storyboard(
    diag_summary: Dict[str, Any],
    doubt: str = "",
    student_concept: str = "",
    student_steps: str = "",
    matched_key: Optional[str] = None,
    output_lang_name: str = "Hinglish (हिंग्लिश)"
) -> Dict[str, Any]:
    """
    Constructs a synchronized live blackboard & audio tutor storyboard ('Bhasha Guru').
    Every spoken thought maps to an active stroke on the 800x500 chalkboard:
    - WRITE (White/Cyan chalk)
    - DRAW_BOX (Green chalk for sound premises)
    - CROSS_OUT (Red chalk strike for derailment)
    - DRAW_ARROW (Cyan chalk connecting vector to pivot)
    - HIGHLIGHT (Gold chalk for active attention)
    """
    if matched_key == "spring_friction_energy":
        timeline = [
            {
                "step_id": 1,
                "speech_segment": "Let us start by mapping what you got right: the block starts at height h.",
                "estimated_duration_sec": 3.5,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 80},
                "color": "#FFFFFF",
                "content": "Step 1: Release from Height h (m = 2 kg, h = 5 m)",
                "element_style": "chalk_text"
            },
            {
                "step_id": 2,
                "speech_segment": "You recognized that gravity does positive work on the way down, which is completely sound.",
                "estimated_duration_sec": 3.0,
                "board_action": "DRAW_BOX",
                "target_coords": {"x": 60, "y": 55, "w": 420, "h": 45},
                "color": "#4ADE80",
                "content": "VALID PREMISE",
                "element_style": "green_box"
            },
            {
                "step_id": 3,
                "speech_segment": "Now look right here: you wrote that total mechanical energy is strictly conserved throughout.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 180},
                "color": "#FFFFFF",
                "content": "Step 2: Assumed E_initial = E_final (mgh = 1/2 k x^2)",
                "element_style": "chalk_text"
            },
            {
                "step_id": 4,
                "speech_segment": "Stop right there! The track has a rough patch, so friction takes a bite out of that energy.",
                "estimated_duration_sec": 4.5,
                "board_action": "CROSS_OUT",
                "target_coords": {"x": 60, "y": 155, "w": 440, "h": 45},
                "color": "#F87171",
                "content": "NON-CONSERVATIVE WORK IGNORED",
                "element_style": "red_strike"
            },
            {
                "step_id": 5,
                "speech_segment": "Instead, branch over to this new equation where we subtract the work done by friction.",
                "estimated_duration_sec": 4.0,
                "board_action": "DRAW_ARROW",
                "target_coords": {"x1": 250, "y1": 215, "x2": 250, "y2": 305},
                "color": "#38BDF8",
                "content": "Divergence Branch",
                "element_style": "arrow"
            },
            {
                "step_id": 6,
                "speech_segment": "Our true energy equation must include minus mu times m times g times distance.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 330},
                "color": "#38BDF8",
                "content": "Corrected Path: mgh - (μ * m * g * d) = 1/2 k x^2",
                "element_style": "bold_chalk"
            }
        ]
        full_transcript = " ".join(t["speech_segment"] for t in timeline)
        result = {
            "doubt_domain": "Physics",
            "identified_topic": "Work-Energy Theorem & Friction Dissipation",
            "misconception_name": "Neglecting Non-Conservative Friction Work in Energy Conservation",
            "full_spoken_transcript": full_transcript,
            "synchronized_timeline": timeline,
            "socratic_challenge": "How much mechanical energy does friction dissipate across the rough 3-meter patch before the block touches the spring?"
        }
    elif matched_key == "economics_rent_control":
        timeline = [
            {
                "step_id": 1,
                "speech_segment": "Let us look at your market setup: equilibrium rent is one thousand dollars for five thousand apartments.",
                "estimated_duration_sec": 3.5,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 80},
                "color": "#FFFFFF",
                "content": "Step 1: Market Equilibrium (P_eq = $1000, Q_eq = 5000 units)",
                "element_style": "chalk_text"
            },
            {
                "step_id": 2,
                "speech_segment": "You correctly identified that tenants want more apartments when price drops to seven hundred dollars.",
                "estimated_duration_sec": 3.0,
                "board_action": "DRAW_BOX",
                "target_coords": {"x": 60, "y": 55, "w": 440, "h": 45},
                "color": "#4ADE80",
                "content": "VALID PREMISE",
                "element_style": "green_box"
            },
            {
                "step_id": 3,
                "speech_segment": "Now look right here: you wrote that total available apartments will increase under this cap.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 180},
                "color": "#FFFFFF",
                "content": "Step 2: Assumed Q_supplied Increases under $700 Rent Ceiling",
                "element_style": "chalk_text"
            },
            {
                "step_id": 4,
                "speech_segment": "Stop right there! When rent is capped below operating costs, landlords exit the market and supply drops.",
                "estimated_duration_sec": 4.5,
                "board_action": "CROSS_OUT",
                "target_coords": {"x": 60, "y": 155, "w": 460, "h": 45},
                "color": "#F87171",
                "content": "SUPPLIER INCENTIVES IGNORED",
                "element_style": "red_strike"
            },
            {
                "step_id": 5,
                "speech_segment": "Instead, branch down to the supply response curve to trace the true market outcome.",
                "estimated_duration_sec": 3.5,
                "board_action": "DRAW_ARROW",
                "target_coords": {"x1": 250, "y1": 215, "x2": 250, "y2": 305},
                "color": "#38BDF8",
                "content": "Divergence Branch",
                "element_style": "arrow"
            },
            {
                "step_id": 6,
                "speech_segment": "The price ceiling creates a massive shortage and deadweight loss instead of surplus.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 330},
                "color": "#38BDF8",
                "content": "Corrected Path: Binding Ceiling -> Shortage (Q_d > Q_s) + Deadweight Loss",
                "element_style": "bold_chalk"
            }
        ]
        full_transcript = " ".join(t["speech_segment"] for t in timeline)
        result = {
            "doubt_domain": "Economics",
            "identified_topic": "Price Ceilings & Supply Elasticity",
            "misconception_name": "Assuming Price Ceilings Increase Total Housing Supply",
            "full_spoken_transcript": full_transcript,
            "synchronized_timeline": timeline,
            "socratic_challenge": "If rental supply is elastic in the long run, what happens to the size of the housing shortage over time?"
        }
    elif matched_key == "law_freedom_of_speech":
        timeline = [
            {
                "step_id": 1,
                "speech_segment": "Let us check your legal basis: Article 19 clause 1 grants fundamental freedom of speech.",
                "estimated_duration_sec": 3.5,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 80},
                "color": "#FFFFFF",
                "content": "Step 1: Article 19(1)(a) Fundamental Freedom of Expression",
                "element_style": "chalk_text"
            },
            {
                "step_id": 2,
                "speech_segment": "You accurately noted that speech is subject to reasonable restrictions under clause 2, which is sound.",
                "estimated_duration_sec": 3.5,
                "board_action": "DRAW_BOX",
                "target_coords": {"x": 60, "y": 55, "w": 440, "h": 45},
                "color": "#4ADE80",
                "content": "VALID PREMISE",
                "element_style": "green_box"
            },
            {
                "step_id": 3,
                "speech_segment": "Now look right here: you assumed controversial opinions in a closed auditorium equal a breach of public order.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 180},
                "color": "#FFFFFF",
                "content": "Step 2: Concluded Provocative Speech = Threat to Public Order",
                "element_style": "chalk_text"
            },
            {
                "step_id": 4,
                "speech_segment": "Stop right there! The Supreme Court holds that speech must be like a spark in a powder keg, not remote annoyance.",
                "estimated_duration_sec": 4.5,
                "board_action": "CROSS_OUT",
                "target_coords": {"x": 60, "y": 155, "w": 460, "h": 45},
                "color": "#F87171",
                "content": "PROXIMATE NEXUS OMITTED",
                "element_style": "red_strike"
            },
            {
                "step_id": 5,
                "speech_segment": "Instead, branch down to the proximate nexus doctrine laid down in Ram Manohar Lohia.",
                "estimated_duration_sec": 3.5,
                "board_action": "DRAW_ARROW",
                "target_coords": {"x1": 250, "y1": 215, "x2": 250, "y2": 305},
                "color": "#38BDF8",
                "content": "Divergence Branch",
                "element_style": "arrow"
            },
            {
                "step_id": 6,
                "speech_segment": "A closed private meeting cannot be curtailed without proof of imminent incitement to violence.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 330},
                "color": "#38BDF8",
                "content": "Corrected Path: Ram Manohar Lohia Test: Direct & Imminent Danger Required",
                "element_style": "bold_chalk"
            }
        ]
        full_transcript = " ".join(t["speech_segment"] for t in timeline)
        result = {
            "doubt_domain": "Law",
            "identified_topic": "Article 19(1)(a) Free Speech & Article 19(2) Public Order",
            "misconception_name": "Conflating Private Disapproval with Public Disorder",
            "full_spoken_transcript": full_transcript,
            "synchronized_timeline": timeline,
            "socratic_challenge": "What is the crucial legal distinction between an ordinary law and order issue and a grave threat to public order?"
        }
    elif matched_key == "history_ww1_causality":
        timeline = [
            {
                "step_id": 1,
                "speech_segment": "Let us map your historical evidence: Archduke Franz Ferdinand was assassinated in Sarajevo on June 28.",
                "estimated_duration_sec": 3.5,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 80},
                "color": "#FFFFFF",
                "content": "Step 1: Sarajevo Assassination of Franz Ferdinand (June 28, 1914)",
                "element_style": "chalk_text"
            },
            {
                "step_id": 2,
                "speech_segment": "You correctly recognized this terrorist incident as the immediate spark of the July diplomatic crisis.",
                "estimated_duration_sec": 3.0,
                "board_action": "DRAW_BOX",
                "target_coords": {"x": 60, "y": 55, "w": 440, "h": 45},
                "color": "#4ADE80",
                "content": "VALID PREMISE",
                "element_style": "green_box"
            },
            {
                "step_id": 3,
                "speech_segment": "Now look right here: you concluded that this single assassination caused the entire world war.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 180},
                "color": "#FFFFFF",
                "content": "Step 2: Inferred WWI Would Not Occur without Gavrilo Princip",
                "element_style": "chalk_text"
            },
            {
                "step_id": 4,
                "speech_segment": "Stop right there! An assassination was merely the matchstick; it could not ignite war without fuel.",
                "estimated_duration_sec": 4.5,
                "board_action": "CROSS_OUT",
                "target_coords": {"x": 60, "y": 155, "w": 460, "h": 45},
                "color": "#F87171",
                "content": "SYSTEMIC TINDERBOX IGNORED",
                "element_style": "red_strike"
            },
            {
                "step_id": 5,
                "speech_segment": "Instead, branch down to the structural alliance networks that turned a local crisis into a global war.",
                "estimated_duration_sec": 3.5,
                "board_action": "DRAW_ARROW",
                "target_coords": {"x1": 250, "y1": 215, "x2": 250, "y2": 305},
                "color": "#38BDF8",
                "content": "Divergence Branch",
                "element_style": "arrow"
            },
            {
                "step_id": 6,
                "speech_segment": "Decades of militarism, secret treaties, and imperial rivalry created the combustible powder keg.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 330},
                "color": "#38BDF8",
                "content": "Corrected Path: M-A-I-N Framework (Militarism, Alliances, Imperialism, Nationalism)",
                "element_style": "bold_chalk"
            }
        ]
        full_transcript = " ".join(t["speech_segment"] for t in timeline)
        result = {
            "doubt_domain": "History",
            "identified_topic": "Origins of World War I (Spark vs Systemic M-A-I-N)",
            "misconception_name": "Monocausal Attribution of WWI to Sarajevo Assassination",
            "full_spoken_transcript": full_transcript,
            "synchronized_timeline": timeline,
            "socratic_challenge": "Why did rigid railway mobilization timetables and secret alliances turn a localized Balkan conflict into a global war?"
        }
    elif matched_key == "literature_macbeth_tragic_flaw":
        timeline = [
            {
                "step_id": 1,
                "speech_segment": "Let us trace your textual reading: the Weird Sisters prophesy that Macbeth will become king.",
                "estimated_duration_sec": 3.5,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 80},
                "color": "#FFFFFF",
                "content": "Step 1: Prophecy of the Weird Sisters & Lady Macbeth's Persuasion",
                "element_style": "chalk_text"
            },
            {
                "step_id": 2,
                "speech_segment": "You accurately identified the intense psychological manipulation exerted by external forces.",
                "estimated_duration_sec": 3.0,
                "board_action": "DRAW_BOX",
                "target_coords": {"x": 60, "y": 55, "w": 440, "h": 45},
                "color": "#4ADE80",
                "content": "VALID PREMISE",
                "element_style": "green_box"
            },
            {
                "step_id": 3,
                "speech_segment": "Now look right here: you claimed Macbeth was an innocent victim with zero moral agency or responsibility.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 180},
                "color": "#FFFFFF",
                "content": "Step 2: Concluded External Prophecy Stripped Macbeth of Moral Agency",
                "element_style": "chalk_text"
            },
            {
                "step_id": 4,
                "speech_segment": "Stop right there! In Aristotelian tragedy, external catalysts never strip a hero of voluntary free will.",
                "estimated_duration_sec": 4.5,
                "board_action": "CROSS_OUT",
                "target_coords": {"x": 60, "y": 155, "w": 460, "h": 45},
                "color": "#F87171",
                "content": "MORAL AGENCY DENIED",
                "element_style": "red_strike"
            },
            {
                "step_id": 5,
                "speech_segment": "Instead, branch down to Macbeth's own confession in Act One where he names his true driving flaw.",
                "estimated_duration_sec": 3.5,
                "board_action": "DRAW_ARROW",
                "target_coords": {"x1": 250, "y1": 215, "x2": 250, "y2": 305},
                "color": "#38BDF8",
                "content": "Divergence Branch",
                "element_style": "arrow"
            },
            {
                "step_id": 6,
                "speech_segment": "The tragedy stems from his own internal fatal flaw: vaulting ambition that overleaps itself.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 330},
                "color": "#38BDF8",
                "content": "Corrected Path: Aristotelian Hamartia: Vaulting Ambition & Complicit Choice",
                "element_style": "bold_chalk"
            }
        ]
        full_transcript = " ".join(t["speech_segment"] for t in timeline)
        result = {
            "doubt_domain": "Literature",
            "identified_topic": "Dramatic Theory & Shakespeare's Macbeth",
            "misconception_name": "Absolution of Protagonist Moral Agency (Fate vs Hamartia)",
            "full_spoken_transcript": full_transcript,
            "synchronized_timeline": timeline,
            "socratic_challenge": "Why did Banquo, hearing the same supernatural prophecies, exercise moral restraint while Macbeth plotted regicide?"
        }
    elif matched_key == "coding_balanced_parentheses":
        timeline = [
            {
                "step_id": 1,
                "speech_segment": "Let us check your algorithmic design: you traverse the string with a last-in-first-out stack.",
                "estimated_duration_sec": 3.5,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 80},
                "color": "#FFFFFF",
                "content": "Step 1: Traverse Delimiters with LIFO Stack",
                "element_style": "chalk_text"
            },
            {
                "step_id": 2,
                "speech_segment": "You correctly popped and paired every closing delimiter against its opening partner.",
                "estimated_duration_sec": 3.0,
                "board_action": "DRAW_BOX",
                "target_coords": {"x": 60, "y": 55, "w": 440, "h": 45},
                "color": "#4ADE80",
                "content": "VALID PREMISE",
                "element_style": "green_box"
            },
            {
                "step_id": 3,
                "speech_segment": "Now look right here: you returned true immediately after the traversal loop finished.",
                "estimated_duration_sec": 3.5,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 180},
                "color": "#FFFFFF",
                "content": "Step 2: Returned True Directly at Loop Termination",
                "element_style": "chalk_text"
            },
            {
                "step_id": 4,
                "speech_segment": "Stop right there! What if unclosed opening brackets remain inside the stack?",
                "estimated_duration_sec": 4.5,
                "board_action": "CROSS_OUT",
                "target_coords": {"x": 60, "y": 155, "w": 460, "h": 45},
                "color": "#F87171",
                "content": "UNCLOSED TOKENS UNCHECKED",
                "element_style": "red_strike"
            },
            {
                "step_id": 5,
                "speech_segment": "Instead, branch down to enforce the terminal stack invariant before returning.",
                "estimated_duration_sec": 3.5,
                "board_action": "DRAW_ARROW",
                "target_coords": {"x1": 250, "y1": 215, "x2": 250, "y2": 305},
                "color": "#38BDF8",
                "content": "Divergence Branch",
                "element_style": "arrow"
            },
            {
                "step_id": 6,
                "speech_segment": "A balanced string requires that the stack must be completely empty at checkout.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 330},
                "color": "#38BDF8",
                "content": "Corrected Invariant: return stack.isEmpty() at terminal exit",
                "element_style": "bold_chalk"
            }
        ]
        full_transcript = " ".join(t["speech_segment"] for t in timeline)
        result = {
            "doubt_domain": "Computer Science",
            "identified_topic": "Stack Invariants & Delimiter Balancing",
            "misconception_name": "Neglecting Terminal Stack Emptiness Invariant",
            "full_spoken_transcript": full_transcript,
            "synchronized_timeline": timeline,
            "socratic_challenge": "What does your code return for an asymmetric string like three opening and two closing brackets?"
        }
    else:
        # Dynamic fallback storyboard for custom queries
        concept_title = diag_summary.get("canonical_concept", "Governing Principle")
        derail_reason = diag_summary.get("derailment_reason", "Unverified premise applied without constraints")
        derail_step = diag_summary.get("derailment_step", 2)
        timeline = [
            {
                "step_id": 1,
                "speech_segment": f"Let us map what you got right in Step 1: you identified the core problem setup.",
                "estimated_duration_sec": 3.5,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 80},
                "color": "#FFFFFF",
                "content": f"Step 1: Stated Initial System Conditions & Relevant Context",
                "element_style": "chalk_text"
            },
            {
                "step_id": 2,
                "speech_segment": "You selected sound foundational premises to start your reasoning path.",
                "estimated_duration_sec": 3.0,
                "board_action": "DRAW_BOX",
                "target_coords": {"x": 60, "y": 55, "w": 440, "h": 45},
                "color": "#4ADE80",
                "content": "VALID PREMISE",
                "element_style": "green_box"
            },
            {
                "step_id": 3,
                "speech_segment": f"Now look right here at Step {derail_step}: you made an unverified assumption.",
                "estimated_duration_sec": 3.5,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 180},
                "color": "#FFFFFF",
                "content": f"Step {derail_step}: Applied Standard Rules without Checking Boundaries",
                "element_style": "chalk_text"
            },
            {
                "step_id": 4,
                "speech_segment": f"Stop right there! {derail_reason[:75]}.",
                "estimated_duration_sec": 4.5,
                "board_action": "CROSS_OUT",
                "target_coords": {"x": 60, "y": 155, "w": 460, "h": 45},
                "color": "#F87171",
                "content": "BOUNDARY CONDITION OMITTED",
                "element_style": "red_strike"
            },
            {
                "step_id": 5,
                "speech_segment": "Instead, branch down to the governing first-principles constraint.",
                "estimated_duration_sec": 3.5,
                "board_action": "DRAW_ARROW",
                "target_coords": {"x1": 250, "y1": 215, "x2": 250, "y2": 305},
                "color": "#38BDF8",
                "content": "Divergence Branch",
                "element_style": "arrow"
            },
            {
                "step_id": 6,
                "speech_segment": f"Our corrected path must be anchored in {concept_title}.",
                "estimated_duration_sec": 4.0,
                "board_action": "WRITE",
                "target_coords": {"x": 80, "y": 330},
                "color": "#38BDF8",
                "content": f"Corrected Path: {concept_title} with Verified Constraints",
                "element_style": "bold_chalk"
            }
        ]
        full_transcript = " ".join(t["speech_segment"] for t in timeline)
        result = {
            "doubt_domain": "Cross-Disciplinary Academic Reasoning",
            "identified_topic": concept_title,
            "misconception_name": diag_summary.get("canonical_root_misconception", "Boundary Condition Misapplication"),
            "full_spoken_transcript": full_transcript,
            "synchronized_timeline": timeline,
            "socratic_challenge": f"Under what exact governing conditions does your initial Step {derail_step} premise hold true?"
        }

    # Apply Language Localization (Pure Hindi vs Hinglish vs English)
    is_pure_hindi = ("Hindi" in output_lang_name or "हिंदी" in output_lang_name) and ("Hinglish" not in output_lang_name and "हिंग्लिश" not in output_lang_name)
    is_hinglish = ("Hinglish" in output_lang_name or "हिंग्लिश" in output_lang_name)

    if is_pure_hindi and matched_key in STORYBOARD_LOCALIZED_SEGMENTS:
        loc = STORYBOARD_LOCALIZED_SEGMENTS[matched_key]
        for idx, seg in enumerate(loc.get("hi", [])):
            if idx < len(result["synchronized_timeline"]):
                result["synchronized_timeline"][idx]["speech_segment"] = seg
        if loc.get("challenge_hi"):
            result["socratic_challenge"] = loc["challenge_hi"]
    elif is_hinglish and matched_key in STORYBOARD_LOCALIZED_SEGMENTS:
        loc = STORYBOARD_LOCALIZED_SEGMENTS[matched_key]
        for idx, seg in enumerate(loc.get("hinglish", [])):
            if idx < len(result["synchronized_timeline"]):
                result["synchronized_timeline"][idx]["speech_segment"] = seg
        if loc.get("challenge_hinglish"):
            result["socratic_challenge"] = loc["challenge_hinglish"]
    elif not matched_key:
        derail_step_val = diag_summary.get("derailment_step", 2)
        derail_reason_val = diag_summary.get("derailment_reason", "unverified premise")
        concept_title_val = diag_summary.get("canonical_concept", "Core Principle")
        if is_pure_hindi:
            tl = result["synchronized_timeline"]
            if len(tl) >= 6:
                tl[0]["speech_segment"] = "आइए देखें कि आपने चरण 1 में क्या सही सोचा: आपने मूल समस्या को पहचाना।"
                tl[1]["speech_segment"] = "आपने अपने तर्क के लिए मजबूत आधारभूत पूर्वधारणाओं का चयन किया।"
                tl[2]["speech_segment"] = f"अब चरण {derail_step_val} पर ध्यान दीजिए: आपने सीमाओं की पुष्टि किए बिना नियम लागू किए।"
                tl[3]["speech_segment"] = f"यहाँ रुकिए! {derail_reason_val[:75]}।"
                tl[4]["speech_segment"] = "इसके बजाय, मूल सिद्धांतों की सीमांत शर्तों पर आइए।"
                tl[5]["speech_segment"] = f"हमारा संशोधित मार्ग {concept_title_val} की वास्तविक शर्तों पर आधारित होना चाहिए।"
            result["socratic_challenge"] = f"किन विशिष्ट नियमों और सीमाओं के अंतर्गत आपका चरण {derail_step_val} का प्रारंभिक तर्क सही होगा?"
        elif is_hinglish:
            tl = result["synchronized_timeline"]
            if len(tl) >= 6:
                tl[0]["speech_segment"] = "Pehle dekhte hain aapne Step 1 mein kya sahi socha: aapne core problem setup identify kiya."
                tl[1]["speech_segment"] = "Aapne reasoning ke liye sound foundational premises select kiye."
                tl[2]["speech_segment"] = f"Ab Step {derail_step_val} par dekhiye: aapne boundaries verify kiye bina rule apply kiya."
                tl[3]["speech_segment"] = f"Stop right there! {derail_reason_val[:75]}."
                tl[4]["speech_segment"] = "Iske bajaye, first-principles governing constraints par aaiye."
                tl[5]["speech_segment"] = f"Hamara corrected path {concept_title_val} ke verified constraints par based hona chahiye."
            result["socratic_challenge"] = f"Kin governing conditions aur constraints ke under aapka initial Step {derail_step_val} premise hold karega?"

    # Update full_spoken_transcript from localized segments
    result["full_spoken_transcript"] = " ".join(t["speech_segment"] for t in result["synchronized_timeline"])
    return result


def evaluate_student_socratic_reply(
    reply: str,
    diagnosis: Dict[str, Any]
) -> Tuple[bool, str, str]:
    """
    Evaluates whether the student has successfully self-corrected the derailed node
    in response to the Socratic prompt.
    
    Returns:
        (is_resolved, feedback_text, badge_level)
    """
    reply_clean = reply.lower().strip()
    concept = diagnosis.get("canonical_concept", "").lower()
    misconception = diagnosis.get("canonical_root_misconception", "").lower()

    # Look for key conceptual breakthrough keywords across disciplines
    keywords_kinematics = ["integrate", "integration", "calculus", "variable", "dv/dt", "not constant", "changes with time"]
    keywords_energy = ["friction", "work done", "heat", "thermal", "non-conservative", "loss", "dissipate", "w_nc"]
    keywords_circle = ["gravity", "tension", "net force", "toward center", "real force", "inertial", "inward"]
    keywords_equilibrium = ["rate", "both", "equal", "activation energy", "k_eq", "forward and reverse", "speed up both"]
    keywords_law = ["proximity", "proximate", "nexus", "incitement", "spark", "powder keg", "lohia", "imminent", "violence", "reasonable restriction"]
    keywords_econ = ["elasticity", "shortage", "ceiling", "supply", "landlord", "incentive", "deadweight", "unintended"]
    keywords_coding = ["empty", "isempty", "stack", "unclosed", "invariant", "post-condition", "remaining", "pop"]
    keywords_history = ["alliances", "treaties", "militarism", "imperialism", "schlieffen", "mobilization", "spark", "trigger", "tinderbox", "structural", "main"]
    keywords_literature = ["ambition", "hamartia", "agency", "moral", "free will", "flaw", "internal", "choice", "banquo", "catalyst", "soliloquy"]

    all_breakthrough_keywords = (
        keywords_kinematics + keywords_energy + keywords_circle + keywords_equilibrium +
        keywords_law + keywords_econ + keywords_coding + keywords_history + keywords_literature
    )

    matched = False
    if any(k in reply_clean for k in all_breakthrough_keywords):
        matched = True
    elif len(reply_clean) > 25 and ("because" in reply_clean or "since" in reply_clean or "means" in reply_clean):
        matched = True

    if matched:
        feedback = (
            "🎉 **Excellent Active Retrieval!** You accurately pinpointed the conceptual limitation in your original logic. "
            "By identifying the foundational constraint or pivot principle, you transformed a fragile intuitive heuristic into a solid conceptual anchor. "
            "Your longitudinal mastery map has been updated accordingly!"
        )
        return True, feedback, "solid"
    else:
        feedback = (
            "🤔 **Good Attempt, but look deeper at the Pivot Node.** "
            "Remember: what fundamental assumption, systemic constraint, or governing boundary did your initial reasoning overlook? "
            "Try re-reading the green remediation map's Pivot Node and articulate the key distinguishing principle."
        )
        return False, feedback, "fragile"
