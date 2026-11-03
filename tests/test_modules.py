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

        # Check separate Hindi (हिंदी) vs Hinglish (हिंग्लिश) outputs
        diag_hindi = pedagogy_engine.diagnose_doubt_semantic(
            doubt=sample["problem_statement"],
            student_concept=sample["student_concept"],
            student_steps=sample["student_steps"],
            student_breakdown=sample["student_breakdown"],
            preferred_language="hi-IN",
            student_name="Arjun",
            output_lang_name="Hindi (हिंदी)"
        )
        self.assertIn("विचार मानचित्र", diag_hindi["narration_script"])

        diag_hinglish = pedagogy_engine.diagnose_doubt_semantic(
            doubt=sample["problem_statement"],
            student_concept=sample["student_concept"],
            student_steps=sample["student_steps"],
            student_breakdown=sample["student_breakdown"],
            preferred_language="hi-IN",
            student_name="Arjun",
            output_lang_name="Hinglish (हिंग्लिश)"
        )
        self.assertTrue("thought map" in diag_hinglish["narration_script"] or "Node 2" in diag_hinglish["narration_script"])

        # Verify LANGUAGE_REGISTRY has both Hindi and Hinglish
        self.assertIn("Hindi (हिंदी)", sarvam_tts.LANGUAGE_REGISTRY)
        self.assertIn("Hinglish (हिंग्लिश)", sarvam_tts.LANGUAGE_REGISTRY)

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

    def test_concept_diagnostician_schema(self):
        """Verify strict concept diagnostician JSON schema generation."""
        sample = SAMPLE_DOUBTS["spring_friction_energy"]
        diag = pedagogy_engine.diagnose_doubt_semantic(
            doubt=sample["problem_statement"],
            student_concept=sample["student_concept"],
            student_steps=sample["student_steps"],
            student_breakdown=sample["student_breakdown"]
        )
        self.assertIn("concept_diagnostics", diag)
        cd = diag["concept_diagnostics"]
        # Schema assertions
        self.assertIn("topic_taxonomy", cd)
        self.assertIn("student_mental_model", cd)
        self.assertIn("mastery_assessment", cd)
        self.assertIn("remediation_recommendations", cd)
        self.assertIn("sarvam_narration_script", cd)

        # Check subfields
        self.assertEqual(cd["topic_taxonomy"]["domain"], "Physics")
        self.assertEqual(cd["student_mental_model"]["cognitive_fallacy_type"], "Over-Generalization")
        self.assertEqual(cd["mastery_assessment"]["status"], "INTUITIVELY_CLOSE")
        self.assertIsInstance(cd["mastery_assessment"]["solid_foundations_demonstrated"], list)
        self.assertIsInstance(cd["remediation_recommendations"]["suggested_study_topics"], list)
        self.assertLessEqual(len(cd["sarvam_narration_script"].split()), 100)

    def test_cross_disciplinary_multi_domain_demos(self):
        """Verify all 6 diverse multi-domain demo fields diagnose accurately."""
        domains_to_test = [
            ("law_freedom_of_speech", "Law"),
            ("economics_rent_control", "Economics"),
            ("history_ww1_causality", "History"),
            ("literature_macbeth_tragic_flaw", "Literature"),
            ("coding_balanced_parentheses", "Computer Science"),
            ("spring_friction_energy", "Physics")
        ]

        for sample_key, expected_domain in domains_to_test:
            self.assertIn(sample_key, SAMPLE_DOUBTS)
            sample = SAMPLE_DOUBTS[sample_key]
            diag = pedagogy_engine.diagnose_doubt_semantic(
                doubt=sample["problem_statement"],
                student_concept=sample["student_concept"],
                student_steps=sample["student_steps"],
                student_breakdown=sample["student_breakdown"]
            )
            self.assertIn("concept_diagnostics", diag)
            cd = diag["concept_diagnostics"]
            self.assertEqual(cd["topic_taxonomy"]["domain"], expected_domain)
            self.assertGreater(len(cd["topic_taxonomy"]["concept_tags"]), 1)
            self.assertIn("flawed_opinion_summary", cd["student_mental_model"])
            self.assertIn("remediation_recommendations", cd)
            self.assertLessEqual(len(cd["sarvam_narration_script"].split()), 100)

    def test_live_classroom_storyboard_schema_and_audio_compliance(self):
        """Verify Bhasha Guru live blackboard storyboard schema, coordinates, and LaTeX-free audio compliance."""
        import re
        latex_regex = re.compile(r'(\\[a-zA-Z]+|\^2|\_\{|\})')

        all_keys = list(SAMPLE_DOUBTS.keys()) + [None]
        for key in all_keys:
            sb = pedagogy_engine.generate_live_board_storyboard(
                {"canonical_concept": "Test", "derailment_step": 2, "derailment_reason": "Test fault"},
                matched_key=key,
                output_lang_name="Hinglish (हिंग्लिश)"
            )
            # Schema checks
            self.assertIn("doubt_domain", sb)
            self.assertIn("identified_topic", sb)
            self.assertIn("misconception_name", sb)
            self.assertIn("full_spoken_transcript", sb)
            self.assertIn("synchronized_timeline", sb)
            self.assertIn("socratic_challenge", sb)
            self.assertGreaterEqual(len(sb["synchronized_timeline"]), 4)

            # Frame compliance checks
            for frame in sb["synchronized_timeline"]:
                self.assertIn(frame["board_action"], ["WRITE", "DRAW_BOX", "CROSS_OUT", "DRAW_ARROW", "HIGHLIGHT", "CLEAR_SECTION"])
                self.assertIn("color", frame)
                self.assertIn("target_coords", frame)
                # Verify coordinate boundaries are within 800x500 slate
                coords = frame["target_coords"]
                if "x" in coords:
                    self.assertGreaterEqual(coords["x"], 0)
                    self.assertLessEqual(coords["x"], 800)
                if "y" in coords:
                    self.assertGreaterEqual(coords["y"], 0)
                    self.assertLessEqual(coords["y"], 500)

                # Strict audio compliance: No raw LaTeX symbols
                self.assertEqual(
                    latex_regex.findall(frame["speech_segment"]),
                    [],
                    f"LaTeX symbol found in audio speech segment: {frame['speech_segment']}"
                )

        # Check Hindi and Hinglish localizations
        sb_hi = pedagogy_engine.generate_live_board_storyboard({}, matched_key="spring_friction_energy", output_lang_name="Hindi (हिंदी)")
        self.assertIn("घर्षण", sb_hi["full_spoken_transcript"])

        sb_hinglish = pedagogy_engine.generate_live_board_storyboard({}, matched_key="spring_friction_energy", output_lang_name="Hinglish (हिंग्लिश)")
        self.assertIn("Pehle", sb_hinglish["full_spoken_transcript"])

    def test_blackboard_component_html_generation(self):
        """Verify HTML5 blackboard canvas generation, SVG/Canvas slate, base64 audio and responsive controls."""
        import blackboard_component

        sb = pedagogy_engine.generate_live_board_storyboard({}, matched_key="economics_rent_control")
        dummy_wav = b"RIFF" + b"\x00" * 36 + b"WAVEfmt " + b"\x00" * 20

        html = blackboard_component.build_blackboard_html(sb, audio_bytes=dummy_wav)
        self.assertIn('<canvas id="blackboard" width="800" height="500"></canvas>', html)
        self.assertIn('data:audio/wav;base64,', html)
        self.assertIn('Bhasha Guru', html)
        self.assertIn('Economics', html)
        self.assertIn('btnPlay', html)
        self.assertIn('btnFullBoard', html)
        self.assertIn('scrubBar', html)
        self.assertIn('speechText', html)
        self.assertIn('socraticBanner', html)

    def test_sample_doubt_lookup_resilience(self):
        """Verify that sample doubt lookups handle newly added keys and missing keys safely without KeyErrors."""
        coding_sample = pedagogy_engine.get_sample_doubt_entry("coding_balanced_parentheses")
        self.assertIsNotNone(coding_sample)
        self.assertEqual(coding_sample["subject"], "Computer Science - Data Structures & Algorithms")
        self.assertIn("problem_statement", coding_sample)
        self.assertIn("problem_statement_hi", coding_sample)

        # Non-existent key must return None without raising KeyError
        missing_sample = pedagogy_engine.get_sample_doubt_entry("completely_unknown_key_xyz")
        self.assertIsNone(missing_sample)

        none_sample = pedagogy_engine.get_sample_doubt_entry(None)
        self.assertIsNone(none_sample)



if __name__ == "__main__":
    unittest.main()
