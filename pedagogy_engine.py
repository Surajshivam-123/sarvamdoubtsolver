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
from typing import Dict, List, Any, Optional, Tuple
from sample_doubts import SAMPLE_DOUBTS


def clean_label(text: str, max_chars_per_line: int = 32) -> str:
    """Wraps text cleanly for Graphviz node labels and escapes quotes."""
    text = text.replace('"', '\\"').strip()
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
            formatted_label = f"⚠️ [Node {i+1}] DERAILMENT\\n{clean_label(raw_label)}"
            if node.get("detail"):
                formatted_label += f"\\n• {clean_label(node['detail'], 28)}"
            dot_lines.append(
                f'  {node_id} [label="{formatted_label}", color="#EF4444", fillcolor="#FEE2E2", fontcolor="#991B1B", penwidth=2.2];'
            )
        else:
            # Muted Slate Gray for sound premises
            formatted_label = f"[Node {i+1}] Premise\\n{clean_label(raw_label)}"
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
            formatted_label = f"💡 [CRITICAL PIVOT]\\n{clean_label(raw_label)}"
            if node.get("detail"):
                formatted_label += f"\\n★ {clean_label(node['detail'], 28)}"
            dot_lines.append(
                f'  {node_id} [label="{formatted_label}", color="#047857", fillcolor="#A7F3D0", fontcolor="#064E3B", penwidth=2.8];'
            )
        else:
            formatted_label = f"[Step {i+1}] Canonical Law\\n{clean_label(raw_label)}"
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
            lbl = f"⚠️ Node {i+1} [Flawed]\\n{clean_label(raw_label)}"
            dot_lines.append(f'    {node_id} [label="{lbl}", color="#EF4444", fillcolor="#FEE2E2", fontcolor="#991B1B", penwidth=2.2];')
        else:
            lbl = f"Node {i+1} [Valid]\\n{clean_label(raw_label)}"
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
            lbl = f"Step {i+1} [Canonical]\\n{clean_label(raw_label)}"
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
    target_language: str = "hi-IN"
) -> str:
    """
    Constructs a node-referencing auditory script tailored for Sarvam AI TTS.
    References the student's derailed node and contrasts it with the remediation pivot node.
    """
    concept = diagnosis.get("canonical_concept", "the physics concept")
    derailment_step = diagnosis.get("derailment_step", 2)
    misconception = diagnosis.get("canonical_root_misconception", "an intuitive assumption")
    derailment_reason = diagnosis.get("derailment_reason", "the condition was misapplied")
    student_name = diagnosis.get("student_name", "Learner")

    if target_language == "hi-IN":
        return (
            f"नमस्ते {student_name}। अपने ग्राफ़ में नोड {derailment_step} को ध्यान से देखिए। "
            f"यहाँ आपकी सोच मुख्य अवधारणा से भटक गई: {misconception}। "
            f"आपने माना कि {derailment_reason[:110]}। "
            f"अब हरे रंग के रेमेडिएशन मैप में पिवट नोड को देखिए: "
            f"जब हम {concept} के बुनियादी नियमों को लागू करते हैं, तो हमें प्रत्यक्ष समीकरणों के बजाय मूल सिद्धांतों से शुरुआत करनी होती है। "
            f"सोचिए, नोड {derailment_step} पर आपका प्रारंभिक पूर्वधारणा किस तरह गलत साबित हो रही है?"
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
            f"we must look at {concept} through foundational principles rather than plugging formulas blindly. "
            f"Notice how this directly pivots your reasoning towards the true physical behavior."
        )


def diagnose_doubt_semantic(
    doubt: str,
    student_concept: str,
    student_steps: str,
    student_breakdown: str,
    learner_context: str = "",
    preferred_language: str = "hi-IN",
    student_name: str = "Learner"
) -> Dict[str, Any]:
    """
    Intelligent pedagogical diagnostic engine.
    Matches predefined curricular concepts or dynamically analyzes custom doubts.
    Strictly forbids direct solutions, providing scaffolded Graphviz maps,
    misconception taxonomy, and Socratic guidance.
    """
    # Check if this matches one of our curated sample doubts
    doubt_lower = (doubt + " " + student_concept + " " + student_steps).lower()

    matched_key = None
    if "a(t)" in doubt_lower or "variable" in doubt_lower or "v = u + at" in doubt_lower or "3t" in doubt_lower:
        matched_key = "kinematics_variable_acc"
    elif "incline" in doubt_lower or "friction" in doubt_lower or "work-energy" in doubt_lower or "rough" in doubt_lower:
        matched_key = "incline_friction_work_energy"
    elif "vertical circle" in doubt_lower or "slack" in doubt_lower or "centrifugal" in doubt_lower or "whirled" in doubt_lower:
        matched_key = "vertical_circle_centripetal"
    elif "haber" in doubt_lower or "catalyst" in doubt_lower or "le chatelier" in doubt_lower or "nh3" in doubt_lower:
        matched_key = "chemistry_le_chatelier_catalyst"

    if matched_key and matched_key in SAMPLE_DOUBTS:
        sample = SAMPLE_DOUBTS[matched_key]
        student_nodes = sample["student_nodes"]
        remediation_nodes = sample["remediation_nodes"]
        derailment_step = sample["derailment_step"]
        root_misconception = sample["canonical_root_misconception"]
        canonical_concept = sample["canonical_concept"]
        derailment_reason = sample["derailment_reason"]
        socratic_prompt = sample["socratic_prompt"]
    else:
        # Dynamic Heuristic Decomposition for custom student queries
        canonical_concept = student_concept if student_concept else "Core Physical/Mathematical Law"
        root_misconception = "Unverified Premise or Overgeneralization in Step 2"
        derailment_step = 2
        derailment_reason = (
            f"Assumed standard equilibrium/kinematic formulas applied without verifying constraints. "
            f"Intuition broke down at: {student_breakdown[:100] if student_breakdown else 'derivation boundary'}."
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
            {"id": "R2", "label": "💡 PIVOT: Return to First-Principles Definition rather than formula plugs", "is_pivot": True, "detail": "Breakthrough: Isolate independent and dependent variables"},
            {"id": "R3", "label": "Set up Conservation / Differential Equation with All Terms", "is_pivot": False},
            {"id": "R4", "label": "Check Boundary Conditions & Dimensional Consistency", "is_pivot": False}
        ]
        socratic_prompt = (
            f"Look back at your Step {derailment_step}: Under what exact physical assumptions does that formula hold true? "
            f"Does your problem satisfy those assumptions, or is one of the parameters changing?"
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

    # Generate multilingual voice script tailored to student's language
    narration_script = synthesize_multilingual_narration(diag_summary, preferred_language)
    diag_summary["narration_script"] = narration_script

    return diag_summary


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

    # Look for key conceptual breakthrough keywords
    keywords_kinematics = ["integrate", "integration", "calculus", "variable", "dv/dt", "not constant", "changes with time"]
    keywords_energy = ["friction", "work done", "heat", "thermal", "non-conservative", "loss", "dissipate", "w_nc"]
    keywords_circle = ["gravity", "tension", "net force", "toward center", "real force", "inertial", "inward"]
    keywords_equilibrium = ["rate", "both", "equal", "activation energy", "k_eq", "forward and reverse", "speed up both"]

    matched = False
    if any(k in reply_clean for k in keywords_kinematics + keywords_energy + keywords_circle + keywords_equilibrium):
        matched = True
    elif len(reply_clean) > 25 and ("because" in reply_clean or "since" in reply_clean or "means" in reply_clean):
        matched = True

    if matched:
        feedback = (
            "🎉 **Excellent Active Retrieval!** You accurately pinpointed the conceptual limitation in your original logic. "
            "By recognizing the boundary conditions, you transformed a fragile rule into a solid conceptual anchor. "
            "Your longitudinal mastery map has been updated accordingly!"
        )
        return True, feedback, "solid"
    else:
        feedback = (
            "🤔 **Good Attempt, but look deeper at the Pivot Node.** "
            "Remember: what fundamental assumption does your initial formula make that doesn't match this physical setup? "
            "Try re-reading the green remediation map's Pivot Node and articulate what force, variable, or rate is acting."
        )
        return False, feedback, "fragile"
