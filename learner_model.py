"""
Longitudinal Learner Model for Bhasha Doubt Solver.
Tracks student profiles, mastery maps, error histories, and pedagogical trajectories.
Persists to local JSON and synchronizes with Streamlit session state.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

DEFAULT_PROFILES_DIR = os.path.join(os.path.dirname(__file__), "data", "learner_profiles")


def ensure_profiles_dir(directory: str = DEFAULT_PROFILES_DIR) -> str:
    """Ensure profiles directory exists."""
    os.makedirs(directory, exist_ok=True)
    return directory


def create_default_profile(
    student_id: str = "arjun_01",
    student_name: str = "Arjun Sharma",
    preferred_language: str = "hi-IN",
    preferred_voice: str = "meera"
) -> Dict[str, Any]:
    """Generates a structured default learner profile."""
    return {
        "student_id": student_id,
        "student_name": student_name,
        "preferred_language": preferred_language,
        "preferred_voice": preferred_voice,
        "created_at": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat(),
        "session_count": 1,
        "mastery_map": {
            "Equations of Motion (Constant a)": "solid",
            "Calculus-based Kinematics (Variable a)": "fragile",
            "Work-Energy Theorem with Friction": "misconception_prone",
            "Centripetal Force & Inertial Frames": "misconception_prone",
            "Chemical Equilibrium & Catalysts": "fragile",
            "Conservation of Momentum": "solid"
        },
        "error_history": [
            {
                "timestamp": "2026-10-28T14:22:00",
                "problem_topic": "Inclined Plane & Pulley Dynamics",
                "concept": "Newton's Laws & Friction",
                "type": "Ignored Normal Reaction Component",
                "severity": "High",
                "details": "Assumed N = mg instead of N = mg cos(theta) on a 30° incline.",
                "resolved": False
            },
            {
                "timestamp": "2026-10-31T09:40:00",
                "problem_topic": "Spring Mass Oscillation",
                "concept": "Work-Energy Theorem with Friction",
                "type": "Ignored Non-Conservative Dissipation",
                "severity": "Medium",
                "details": "Equated initial potential energy directly to maximum kinetic energy despite rough surface.",
                "resolved": False
            }
        ],
        "pedagogical_trajectory": (
            "Arjun has strong algebraic manipulation skills but exhibits two recurring cognitive blind spots: "
            "(1) over-generalizing scalar conservation laws while ignoring dissipative/friction work terms, and "
            "(2) treating time-dependent dynamical vectors as static constants."
        )
    }


def save_profile(profile: Dict[str, Any], directory: str = DEFAULT_PROFILES_DIR) -> str:
    """Persists learner profile to a JSON file."""
    ensure_profiles_dir(directory)
    profile["last_active"] = datetime.now().isoformat()
    filename = f"{profile['student_id']}.json"
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    return filepath


def load_profile(student_id: str, directory: str = DEFAULT_PROFILES_DIR) -> Dict[str, Any]:
    """Loads a learner profile from JSON, or creates a default one if not found."""
    ensure_profiles_dir(directory)
    filepath = os.path.join(directory, f"{student_id}.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # If not found or error, create and save default
    profile = create_default_profile(student_id=student_id)
    save_profile(profile, directory)
    return profile


def list_available_profiles(directory: str = DEFAULT_PROFILES_DIR) -> List[Dict[str, str]]:
    """Lists all available student profiles in the directory."""
    ensure_profiles_dir(directory)
    profiles = []
    for f in os.listdir(directory):
        if f.endswith(".json"):
            path = os.path.join(directory, f)
            try:
                with open(path, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    profiles.append({
                        "student_id": data.get("student_id", f.replace(".json", "")),
                        "student_name": data.get("student_name", "Unknown Learner"),
                        "preferred_language": data.get("preferred_language", "hi-IN")
                    })
            except Exception:
                continue
    if not profiles:
        # Seed initial profiles
        seed_profiles = [
            create_default_profile("arjun_01", "Arjun Sharma (Class 12 - JEE)", "hi-IN", "meera"),
            create_default_profile("priya_02", "Priya Nair (B.Tech Year 1)", "en-IN", "arvind"),
            create_default_profile("rohan_03", "Rohan Patil (Class 11 - NEET)", "mr-IN", "amol"),
            create_default_profile("ananya_04", "Ananya Chatterjee (Higher Secondary)", "bn-IN", "amartya"),
            create_default_profile("karthik_05", "Karthik Subramanian (JEE Advanced)", "ta-IN", "pavithra")
        ]
        for p in seed_profiles:
            save_profile(p, directory)
            profiles.append({
                "student_id": p["student_id"],
                "student_name": p["student_name"],
                "preferred_language": p["preferred_language"]
            })
    return profiles


def record_misconception(
    profile: Dict[str, Any],
    concept: str,
    misconception_type: str,
    severity: str,
    details: str,
    problem_topic: str = ""
) -> Dict[str, Any]:
    """Appends an identified misconception to the profile and recalibrates the mastery map."""
    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "problem_topic": problem_topic or concept,
        "concept": concept,
        "type": misconception_type,
        "severity": severity,
        "details": details,
        "resolved": False
    }
    profile.setdefault("error_history", []).append(new_entry)
    
    # Recalibrate concept mastery status
    mastery = profile.setdefault("mastery_map", {})
    current_status = mastery.get(concept, "fragile")
    if severity == "High":
        mastery[concept] = "misconception_prone"
    elif severity == "Medium" and current_status == "solid":
        mastery[concept] = "fragile"
    elif concept not in mastery:
        mastery[concept] = "fragile"

    # Update pedagogical trajectory summary
    update_pedagogical_trajectory(profile)
    return profile


def resolve_misconception(profile: Dict[str, Any], concept: str) -> Dict[str, Any]:
    """Marks recent misconceptions for a concept as resolved after successful Socratic dialogue."""
    for entry in reversed(profile.get("error_history", [])):
        if entry.get("concept") == concept and not entry.get("resolved", False):
            entry["resolved"] = True
            entry["resolved_at"] = datetime.now().isoformat()
            break
            
    # Upgrade mastery status
    mastery = profile.setdefault("mastery_map", {})
    if mastery.get(concept) == "misconception_prone":
        mastery[concept] = "fragile"
    elif mastery.get(concept) == "fragile":
        mastery[concept] = "solid"

    update_pedagogical_trajectory(profile)
    return profile


def update_pedagogical_trajectory(profile: Dict[str, Any]) -> None:
    """Dynamically updates the longitudinal summary based on error frequency."""
    errors = profile.get("error_history", [])
    if not errors:
        profile["pedagogical_trajectory"] = "No diagnostic errors logged yet. Baseline learner model."
        return

    unresolved = [e for e in errors if not e.get("resolved", False)]
    recent_types = [e.get("type", "") for e in unresolved[-4:]]
    concepts = list(set([e.get("concept", "") for e in unresolved]))

    summary_parts = []
    if len(unresolved) > 0:
        summary_parts.append(
            f"Active friction areas across {len(concepts)} key domain(s): {', '.join(concepts[:3])}."
        )
    if recent_types:
        summary_parts.append(f"Recurring pattern of errors: {'; '.join(recent_types[-2:])}.")

    profile["pedagogical_trajectory"] = " ".join(summary_parts)


def build_pedagogical_context(profile: Dict[str, Any]) -> str:
    """
    Constructs a rich prompt-injection string containing the learner's past blind spots.
    Enables Socratic explanations to explicitly contrast new doubts against past pitfalls.
    """
    student_name = profile.get("student_name", "Student")
    lang = profile.get("preferred_language", "en-IN")
    trajectory = profile.get("pedagogical_trajectory", "None logged yet.")
    
    # Extract unresolved high/medium severity past errors
    past_errors = profile.get("error_history", [])
    error_bullets = []
    for e in past_errors[-4:]:
        status = "Resolved" if e.get("resolved") else "Open Blind Spot"
        error_bullets.append(
            f"- [{e.get('severity', 'Med')}] {e.get('concept')}: {e.get('type')} ({e.get('details', '')[:90]}) [{status}]"
        )
    error_summary = "\n".join(error_bullets) if error_bullets else "No prior recorded misconceptions."

    # Identify mastery weaknesses
    mastery = profile.get("mastery_map", {})
    fragile_concepts = [c for c, s in mastery.items() if s in ("fragile", "misconception_prone")]

    context = (
        f"--- LONGITUDINAL LEARNER PROFILE (Context Injection) ---\n"
        f"Learner Name: {student_name}\n"
        f"Target Language Code: {lang}\n"
        f"Learner Trajectory Summary: {trajectory}\n"
        f"Vulnerable Concepts Tracked: {', '.join(fragile_concepts) if fragile_concepts else 'All baseline'}\n"
        f"Recent Misconception History:\n{error_summary}\n"
        f"INSTRUCTION: When diagnosing the current doubt, actively cross-reference these historical misconceptions "
        f"if the student's breakdown mirrors their past thinking traps.\n"
        f"---------------------------------------------------------"
    )
    return context


def reset_profile(student_id: str, directory: str = DEFAULT_PROFILES_DIR) -> Dict[str, Any]:
    """Resets the learner profile to clean slate baseline."""
    fresh = create_default_profile(student_id=student_id)
    save_profile(fresh, directory)
    return fresh


def export_profile_json(profile: Dict[str, Any]) -> str:
    """Exports learner profile as pretty-printed JSON string."""
    return json.dumps(profile, indent=2, ensure_ascii=False)


def import_profile_json(json_str: str, directory: str = DEFAULT_PROFILES_DIR) -> Dict[str, Any]:
    """Imports learner profile from JSON string and saves it."""
    data = json.loads(json_str)
    if "student_id" not in data:
        raise ValueError("Invalid profile format: 'student_id' missing.")
    save_profile(data, directory)
    return data
