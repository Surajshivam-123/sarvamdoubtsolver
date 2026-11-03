"""
Comprehensive Unit Tests for Bhasha Doubt Solver.
Tests:
1. Learner Profile Model & Longitudinal Context Injection
2. Pedagogical Diagnosis & Comparative Graphviz Thought Maps
3. Sarvam AI TTS Text Chunking & Resilient Audio Fallback
4. Socratic Active Retrieval Evaluation
"""

import os
import json
import unittest
import tempfile

import learner_model
import pedagogy_engine
import sarvam_tts
from sample_doubts import SAMPLE_DOUBTS


class TestBhashaDoubtSolver(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def test_learner_profile_lifecycle(self):
        """Test profile creation, saving, loading, and context injection."""
        profile = learner_model.create_default_profile(
            student_id="test_student_01",
            student_name="Test Student",
            preferred_language="hi-IN"
        )
        self.assertEqual(profile["student_id"], "test_student_01")
        self.assertIn("mastery_map", profile)
        self.assertIn("error_history", profile)

        # Save profile
        filepath = learner_model.save_profile(profile, self.test_dir)
        self.assertTrue(os.path.exists(filepath))

        # Load profile
        loaded = learner_model.load_profile("test_student_01", self.test_dir)
        self.assertEqual(loaded["student_name"], "Test Student")

        # Record new misconception
        updated = learner_model.record_misconception(
            profile=loaded,
            concept="Calculus-based Kinematics (Variable a)",
            misconception_type="Assumed Constant Acceleration",
            severity="High",
            details="Integrated incorrectly by assuming constant a",
            problem_topic="Kinematics a(t)=3t"
        )
        self.assertEqual(updated["mastery_map"]["Calculus-based Kinematics (Variable a)"], "misconception_prone")
        self.assertGreaterEqual(len(updated["error_history"]), 3)

        # Check context injection string
        context_str = learner_model.build_pedagogical_context(updated)
        self.assertIn("LONGITUDINAL LEARNER PROFILE", context_str)
        self.assertIn("Test Student", context_str)
        self.assertIn("Assumed Constant Acceleration", context_str)

        # Resolve misconception through Socratic success
        resolved = learner_model.resolve_misconception(updated, "Calculus-based Kinematics (Variable a)")
        self.assertEqual(resolved["mastery_map"]["Calculus-based Kinematics (Variable a)"], "fragile")

        # Export & Import
        json_export = learner_model.export_profile_json(resolved)
        reimported = learner_model.import_profile_json(json_export, self.test_dir)
        self.assertEqual(reimported["student_id"], "test_student_01")

    def test_graphviz_dot_generation(self):
        """Verify Graphviz DOT syntax and styling for Map A, Map B, and Comparative Map."""
        sample = SAMPLE_DOUBTS["kinematics_variable_acc"]
        
        # Map A (Student Path)
        dot_a = pedagogy_engine.generate_map_a_dot(sample["student_nodes"])
        self.assertTrue(dot_a.startswith("digraph"))
        self.assertIn("#EF4444", dot_a)  # Coral/Red error color
        self.assertIn("#F8FAFC", dot_a)  # Muted Gray premise color
        self.assertIn("DERAILMENT", dot_a)

        # Map B (Remediation Path)
        dot_b = pedagogy_engine.generate_map_b_dot(sample["remediation_nodes"])
        self.assertTrue(dot_b.startswith("digraph"))
        self.assertIn("#10B981", dot_b)  # Emerald green color
        self.assertIn("CRITICAL PIVOT", dot_b)

        # Comparative Dual Map
        dot_comp = pedagogy_engine.generate_comparative_dual_dot(
            sample["student_nodes"], sample["remediation_nodes"]
        )
        self.assertTrue(dot_comp.startswith("digraph"))
        self.assertIn("cluster_student", dot_comp)
        self.assertIn("cluster_remediation", dot_comp)
        self.assertIn("Pedagogy Pivot", dot_comp)

    def test_pedagogy_diagnosis_and_multilingual_scripts(self):
        """Verify diagnostic logic and multilingual node-referencing scripts."""
        sample = SAMPLE_DOUBTS["incline_friction_work_energy"]
        diag = pedagogy_engine.diagnose_doubt_semantic(
            doubt=sample["problem_statement"],
            student_concept=sample["student_concept"],
            student_steps=sample["student_steps"],
            student_breakdown=sample["student_breakdown"],
            preferred_language="hi-IN",
            student_name="Arjun"
        )

        self.assertEqual(diag["canonical_concept"], "Work-Energy Theorem with Non-Conservative Forces")
        self.assertIn("Non-Conservative", diag["canonical_root_misconception"])
        self.assertEqual(diag["derailment_step"], 2)
        
        # Check that audio script directly mentions Node 2
        self.assertTrue("नोड 2" in diag["narration_script"] or "Node 2" in diag["narration_script"])
        self.assertTrue("पिवट नोड" in diag["narration_script"] or "Pivot Node" in diag["narration_script"])

        # Check English script
        script_en = pedagogy_engine.synthesize_multilingual_narration(diag, "en-IN")
        self.assertIn("Node 2", script_en)
        self.assertIn("Pivot Node", script_en)

    def test_sarvam_tts_chunking_and_fallback(self):
        """Verify text chunking for Sarvam API and harmonic WAV synthesis."""
        long_text = "This is a sentence. " * 30
        chunks = sarvam_tts.chunk_text(long_text, max_chars=100)
        self.assertGreater(len(chunks), 1)
        for c in chunks:
            self.assertLessEqual(len(c), 100)

        # Fallback audio generation
        audio_bytes = sarvam_tts.generate_synthesized_fallback_audio()
        self.assertIsInstance(audio_bytes, bytes)
        self.assertGreater(len(audio_bytes), 1000)
        # Verify valid WAV header
        self.assertEqual(audio_bytes[:4], b"RIFF")
        self.assertEqual(audio_bytes[8:12], b"WAVE")

        # Mock synthesis call (explicitly empty key)
        audio, msg, is_real = sarvam_tts.synthesize_speech_sarvam(
            text="Hello student",
            target_language_code="hi-IN",
            api_key="your_sarvam_api_key_here"
        )
        self.assertFalse(is_real)
        self.assertIsNotNone(audio)
        self.assertIn("acoustic", msg.lower())

    def test_socratic_reply_evaluation(self):
        """Verify active retrieval evaluation of student Socratic replies."""
        diag = {"canonical_concept": "Calculus-based Kinematics", "canonical_root_misconception": "Constant a assumption"}
        
        # Good answer mentioning key concept
        resolved, feedback, level = pedagogy_engine.evaluate_student_socratic_reply(
            "I realize that acceleration is variable, so I must integrate dv = 3t dt rather than using v=u+at.",
            diag
        )
        self.assertTrue(resolved)
        self.assertEqual(level, "solid")

        # Superficial answer without conceptual reasoning
        resolved_bad, feedback_bad, level_bad = pedagogy_engine.evaluate_student_socratic_reply(
            "I don't know, maybe use another formula?",
            diag
        )
        self.assertFalse(resolved_bad)
        self.assertEqual(level_bad, "fragile")


if __name__ == "__main__":
    unittest.main()
