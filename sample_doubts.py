"""
Pre-curated realistic STEM doubts reflecting classic conceptual traps
faced by Indian students in competitive and foundational exams (JEE, NEET, CBSE).
Includes rich natural Hinglish and English pedagogical narratives.
"""

SAMPLE_DOUBTS = {
    "spring_friction_energy": {
        "title": "🏔️ Spring & Incline Friction (Work-Energy)",
        "subject": "Physics - Mechanics",
        "problem_statement": (
            "A 2 kg block slides down a 5 m incline with a rough patch (friction coefficient μ = 0.2 over 3 m). "
            "At the bottom, it hits a spring (k = 400 N/m). Find maximum compression."
        ),
        "student_concept": "Conservation of Mechanical Energy (mgh = 1/2 k x²)",
        "student_steps": (
            "Step 1: Identified initial height h and spring contact.\n"
            "Step 2: Assumed that throughout the entire motion, Total Mechanical Energy is strictly conserved.\n"
            "Step 3: Equated mgh directly to 1/2 k x² without considering the rough patch.\n"
            "Step 4: Solved for compression x and obtained ~0.7 m, which is much higher than the answer key."
        ),
        "student_breakdown": (
            "My calculated compression is roughly 0.7 m, which is much higher than the solution key. "
            "I used conservation of energy, where did my equation derail?"
        ),
        "canonical_concept": "Work-Energy Theorem with Non-Conservative Forces",
        "canonical_root_misconception": "Neglecting Non-Conservative Friction Work during Energy Conservation",
        "derailment_step": 2,
        "derailment_reason": "Treated mechanical energy as strictly conserved despite the presence of non-conservative friction work W_nc = -μ m g d cos(θ).",
        "student_nodes": [
            {"id": "S1", "label": "Initial height h & spring at base", "is_error": False},
            {"id": "S2", "label": "Assumed mechanical energy strictly conserved", "is_error": True, "detail": "Derailment: Friction dissipates mechanical energy into heat!"},
            {"id": "S3", "label": "Equated mgh = 1/2 k x² directly", "is_error": True, "detail": "Omitted friction work term"},
            {"id": "S4", "label": "Calculated compression x ≈ 0.7 m (too high)", "is_error": True, "detail": "Grossly overestimated compression"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Draw Free Body Diagram for rough patch", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Differentiate Conservative (Gravity) vs Non-Conservative (Friction)", "is_pivot": True, "detail": "Breakthrough: Friction does negative work W_f = -μ N d"},
            {"id": "R3", "label": "Apply Work-Energy Theorem: E_initial - Heat Loss = Spring Energy", "is_pivot": False},
            {"id": "R4", "label": "Solve accurate compression with remaining mechanical energy", "is_pivot": False}
        ],
        "narration_en": (
            "You had a great intuition that energy converts between forms. "
            "However, look at Node 2 in your thought map: you assumed mechanical energy is strictly conserved. "
            "Because the track has friction, it does negative work, converting mechanical energy into heat. "
            "As shown in the green remediation map at the Pivot Node, subtract the friction work before equating to spring energy. How much energy remains?"
        ),
        "narration_hi": (
            "आपने यह बिल्कुल सही सोचा कि potential energy spring energy में convert होगी। "
            "लेकिन अपने thought map के Node 2 को ध्यान से देखिए: आपने मान लिया कि mechanical energy strictly conserved है। "
            "क्योंकि track पर एक rough patch है, friction negative work करता है, जिससे कुछ energy heat में lose हो जाती है। "
            "Remediation map के Pivot Node को देखिए: spring energy equate करने से पहले friction के work को subtract करना होगा। "
            "Spring तक पहुँचने पर block के पास actually कितनी mechanical energy बचेगी?"
        ),
        "socratic_prompt": (
            "Rough patch पर friction से lost होने वाली heat energy का formula क्या होगा? "
            "क्या इसे initial energy में add करेंगे या subtract?"
        )
    },

    "newton_third_law_horse_cart": {
        "title": "🐎 Newton's 3rd Law (Horse & Cart Paradox)",
        "subject": "Physics - Dynamics",
        "problem_statement": (
            "A horse pulls a cart forward with acceleration 1.5 m/s². "
            "Explain the forces and find net force if cart mass is 200 kg."
        ),
        "student_concept": "Newton's Third Law (Action and Reaction Forces)",
        "student_steps": (
            "Step 1: Horse pulls cart forward with force F.\n"
            "Step 2: By Newton's Third Law, cart pulls horse backward with equal and opposite force -F.\n"
            "Step 3: Summing the forces gives F + (-F) = 0. Forces cancel each other out.\n"
            "Step 4: Concluded that the net force is zero, so the cart can never accelerate."
        ),
        "student_breakdown": (
            "If action and reaction forces are always equal and opposite, how does the cart ever accelerate? "
            "Why don't the forces simply cancel out to zero?"
        ),
        "canonical_concept": "Newton's Third Law & Isolated Free Body Diagrams",
        "canonical_root_misconception": "Adding Action-Reaction Pairs Acting on Different Bodies",
        "derailment_step": 3,
        "derailment_reason": "Combined forces acting on two distinct physical bodies (horse vs cart) into a single equation, falsely concluding they cancel out.",
        "student_nodes": [
            {"id": "S1", "label": "Forward force F by horse on cart", "is_error": False},
            {"id": "S2", "label": "Backward reaction force -F by cart on horse", "is_error": False},
            {"id": "S3", "label": "Summed forces: F + (-F) = 0 on single body", "is_error": True, "detail": "Derailment: Action-reaction act on distinct bodies, never cancel!"},
            {"id": "S4", "label": "Concluded cart acceleration is impossible", "is_error": True, "detail": "False paradox"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Isolate the Cart exclusively in its Free Body Diagram", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Action and Reaction act on distinct objects and NEVER cancel on one object", "is_pivot": True, "detail": "Breakthrough: Only count forces acting strictly ON the cart"},
            {"id": "R3", "label": "Apply Newton's Second Law to Cart alone: Σ F_cart = m_cart * a", "is_pivot": False},
            {"id": "R4", "label": "Solve forward pull: F_net = 200 kg * 1.5 m/s² = 300 N", "is_pivot": False}
        ],
        "narration_en": (
            "You correctly recalled that action and reaction are equal and opposite. "
            "However, look at Node 3 in your thought map: you canceled forces acting on two completely different bodies. "
            "Action and reaction forces act on separate objects, so they never cancel each other. "
            "Look at the green remediation map: isolate the cart alone in your Free Body Diagram. What external force pulls the cart forward?"
        ),
        "narration_hi": (
            "आपने Newton's Third Law सही याद किया कि action और reaction forces equal and opposite होते हैं। "
            "लेकिन अपने thought map के Node 3 को देखिए: आपने horse पर लगने वाले force को cart पर लगने वाले force से cancel कर दिया। "
            "Action और reaction forces दो अलग-अलग objects पर लगते हैं, इसलिए वे कभी एक दूसरे को cancel नहीं कर सकते। "
            "Remediation map के Pivot Node को देखिए: सिर्फ cart का Free Body Diagram बनाइए। Cart को forward direction में खींचने वाला external force कौन सा है?"
        ),
        "socratic_prompt": (
            "अगर आप सिर्फ cart को isolate करें, तो cart पर forward direction में pull करने वाला external force कौन सा है? "
            "क्या cart पर -F लग रहा है या horse पर?"
        )
    },

    "circular_motion_turn": {
        "title": "🏎️ Circular Motion & Centrifugal Pseudo-Force",
        "subject": "Physics - Dynamics",
        "problem_statement": (
            "A car moves around a flat circular curve of radius 50 m at 20 m/s. "
            "Find the minimum static friction coefficient needed to prevent slipping."
        ),
        "student_concept": "Balancing Centrifugal Outward Force against Friction",
        "student_steps": (
            "Step 1: Identified car turning with radius R = 50 m and v = 20 m/s.\n"
            "Step 2: Assumed an outward centrifugal force m v² / R acts on the car in ground frame.\n"
            "Step 3: Added forward drive force and centrifugal force via vector sum against friction.\n"
            "Step 4: Arrived at an unrealistically large friction coefficient."
        ),
        "student_breakdown": (
            "The friction coefficient comes out unrealistically large, and I am confused about which way friction points. "
            "Why doesn't centrifugal force balance the turn?"
        ),
        "canonical_concept": "Inertial Reference Frame & Centripetal Acceleration",
        "canonical_root_misconception": "Treating Centrifugal Pseudo-Force as a Real Force in Ground Frame",
        "derailment_step": 2,
        "derailment_reason": "Introduced an outward pseudo-force in an inertial (ground) reference frame where only real contact forces exist.",
        "student_nodes": [
            {"id": "S1", "label": "Identified car on circular curve (R=50m, v=20m/s)", "is_error": False},
            {"id": "S2", "label": "Added outward centrifugal force in ground frame", "is_error": True, "detail": "Derailment: Centrifugal force is a pseudo-force, only valid in rotating frame!"},
            {"id": "S3", "label": "Summed drive force + centrifugal force vectorially", "is_error": True, "detail": "Conflated kinematics and dynamics"},
            {"id": "S4", "label": "Obtained impossible friction coefficient", "is_error": True, "detail": "Invalid dynamic balance"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Observe motion strictly from the Ground (Inertial) Frame", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Inward static friction IS the net force providing centripetal acceleration", "is_pivot": True, "detail": "Breakthrough: f_s = m v² / R"},
            {"id": "R3", "label": "Apply no-skidding condition: f_s ≤ μ_s * m * g", "is_pivot": False},
            {"id": "R4", "label": "Equate and solve: μ_s ≥ v² / (g R) = 400 / (9.8 * 50) ≈ 0.82", "is_pivot": False}
        ],
        "narration_en": (
            "You understand the parameters of circular motion. "
            "However, look at Node 2 in your graph: you treated centrifugal force as a real physical force in the ground frame. "
            "From the road's perspective, the car is accelerating toward the center, and only inward static friction supplies this acceleration. "
            "As highlighted at the Pivot Node in the green remediation map, equate static friction directly to m v squared over R."
        ),
        "narration_hi": (
            "आप circular motion के parameters को अच्छी तरह पहचानते हैं। "
            "लेकिन thought map के Node 2 को देखिए: आपने ground frame में centrifugal force को एक real physical force मान लिया। "
            "Road के perspective से, car center की तरफ accelerate कर रही है, और यह centripetal acceleration सिर्फ static friction supply करता है। "
            "Green remediation map के Pivot Node को देखिए: static friction को सीधे m v squared divided by R से equate कीजिए।"
        ),
        "socratic_prompt": (
            "Ground frame से देखने पर, car को circular path में turn कराने के लिए net static friction force किस direction में point करना चाहिए? "
            "क्या केंद्र की ओर या केंद्र से बाहर?"
        )
    },

    "rotational_skater_spin": {
        "title": "⛸️ Rotational Dynamics: Skater Arm Pull",
        "subject": "Physics - Rotational Mechanics",
        "problem_statement": (
            "A skater spins with initial angular velocity ω₀. Pulling arms inward cuts moment of inertia from I₀ to I₀ / 3. "
            "Compare initial and final rotational kinetic energy."
        ),
        "student_concept": "Conservation of Rotational Kinetic Energy (1/2 I ω² = const)",
        "student_steps": (
            "Step 1: Noticed that no external torque acts on the skater.\n"
            "Step 2: Assumed rotational kinetic energy must be conserved: 1/2 I₀ ω₀² = 1/2 I_f ω_f².\n"
            "Step 3: Solved for final angular velocity and found ω_f = √3 ω₀.\n"
            "Step 4: Realized this directly contradicts angular momentum conservation (L = I ω => ω_f = 3 ω₀)."
        ),
        "student_breakdown": (
            "When I use conservation of angular momentum (L = I*ω), I get ω_f = 3*ω₀. "
            "Why are energy conservation and angular momentum conservation giving conflicting results?"
        ),
        "canonical_concept": "Angular Momentum Conservation vs Internal Muscular Work",
        "canonical_root_misconception": "Assuming Kinetic Energy Conservation During Internal Muscular Work",
        "derailment_step": 2,
        "derailment_reason": "Assumed mechanical kinetic energy is conserved when the skater's muscles perform positive internal work pulling arms against centrifugal inertia.",
        "student_nodes": [
            {"id": "S1", "label": "Noticed external torque Σ τ_ext = 0", "is_error": False},
            {"id": "S2", "label": "Assumed rotational kinetic energy is conserved", "is_error": True, "detail": "Derailment: Muscles perform positive internal work, increasing kinetic energy!"},
            {"id": "S3", "label": "Equated 1/2 I₀ ω₀² = 1/2 I_f ω_f² => ω_f = √3 ω₀", "is_error": True, "detail": "Incorrect energy balance"},
            {"id": "S4", "label": "Conflicted with angular momentum conservation", "is_error": True, "detail": "Internal contradiction"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Verify that net external torque is zero: Σ τ_ext = 0", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Conserve Angular Momentum strictly: I₀ ω₀ = I_f ω_f", "is_pivot": True, "detail": "Breakthrough: ω_f = (I₀ / I_f) ω₀ = 3 ω₀"},
            {"id": "R3", "label": "Calculate final kinetic energy: K_final = 1/2 (I₀/3) (3 ω₀)² = 3 K_initial", "is_pivot": False},
            {"id": "R4", "label": "Recognize that ΔK = +2 K_initial equals the positive work done by muscles", "is_pivot": False}
        ],
        "narration_en": (
            "You correctly identified that external torque is zero. "
            "However, look at Node 2 in your thought map: you assumed rotational kinetic energy is conserved. "
            "When the skater pulls their arms inward, their muscles perform positive internal work against inertia, which increases the kinetic energy. "
            "Look at the green remediation map at the Pivot Node: use angular momentum conservation to find the new spin rate, and notice how kinetic energy actually triples."
        ),
        "narration_hi": (
            "आपने बिल्कुल सही पहचाना कि external torque zero है। "
            "लेकिन thought map के Node 2 को देखिए: आपने rotational kinetic energy को conserved मान लिया। "
            "जब skater arms को अंदर खींचता है, तो उसकी muscles inertia के खिलाफ positive work करती हैं, जिससे kinetic energy बढ़ जाती है। "
            "Remediation map के Pivot Node को देखिए: angular momentum conservation use करके नया spin rate निकालिए, और देखिए कि kinetic energy actually 3 times हो जाती है।"
        ),
        "socratic_prompt": (
            "L = I * ω conservation use करके बताइए: अगर moment of inertia one-third (I₀ / 3) हो जाता है, "
            "तो angular velocity कितने गुना बढ़ेगी? और फिर K = 1/2 I ω² का ratio क्या होगा?"
        )
    },

    "kinematics_variable_acc": {
        "title": "🏎️ Kinematics: Acceleration Dependent on Time",
        "subject": "Physics - Mechanics",
        "problem_statement": (
            "A particle starts from rest at t = 0. Its acceleration varies with time as a(t) = 3t m/s². "
            "Find the velocity and position of the particle at t = 4 seconds."
        ),
        "student_concept": "Equations of Motion (v = u + at, s = ut + 0.5at²)",
        "student_steps": (
            "Step 1: The particle starts from rest, so initial velocity u = 0.\n"
            "Step 2: At t = 4, acceleration is a = 3 * 4 = 12 m/s².\n"
            "Step 3: I plugged this acceleration into v = u + at = 0 + (12)(4) = 48 m/s.\n"
            "Step 4: Then I calculated displacement using s = ut + (1/2)at² = 0 + 0.5 * 12 * 4² = 96 m."
        ),
        "student_breakdown": (
            "The textbook answer key says v = 24 m/s and s = 32 m, but my calculation gives 48 m/s and 96 m. "
            "I used the standard kinematic formula, why is it giving double the answer?"
        ),
        "canonical_concept": "Calculus-based Kinematics (Variable Acceleration)",
        "canonical_root_misconception": "Overgeneralized Kinematic Formula to Non-Constant Acceleration",
        "derailment_step": 3,
        "derailment_reason": "Treated time-dependent acceleration a(t)=3t as a constant value (12 m/s²) over the interval [0, 4] s, violating the derivation assumption of v = u + at.",
        "student_nodes": [
            {"id": "S1", "label": "Identified u = 0 at t = 0", "is_error": False},
            {"id": "S2", "label": "Evaluated a(4) = 12 m/s²", "is_error": False},
            {"id": "S3", "label": "Assumed 'a' is constant across interval", "is_error": True, "detail": "Derailment: a is a function of time, not constant!"},
            {"id": "S4", "label": "Applied formula v = u + at = 48 m/s", "is_error": True, "detail": "Invalid equation for non-constant acceleration"},
            {"id": "S5", "label": "Applied s = ut + 0.5 a t² = 96 m", "is_error": True, "detail": "Compounded error"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Recognize a = dv/dt is variable (time-dependent)", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Set up differential definition dv = a(t) dt", "is_pivot": True, "detail": "Breakthrough: Use integration instead of algebraic equations"},
            {"id": "R3", "label": "Integrate: v(t) = ∫ 3t dt = 1.5 t² -> v(4) = 24 m/s", "is_pivot": False},
            {"id": "R4", "label": "Integrate position: s(t) = ∫ v(t) dt = 0.5 t³", "is_pivot": False},
            {"id": "R5", "label": "Evaluate at t = 4: s(4) = 0.5 * (64) = 32 m", "is_pivot": False}
        ],
        "narration_en": (
            "Look at Node 2 and Node 3 in your graph: you correctly calculated the instantaneous acceleration at t=4 as 12 m/s², "
            "but then you treated this 12 m/s² as if it were acting constantly from t=0. "
            "As highlighted in the emerald green remediation map at the Pivot Node, standard kinematic equations only hold when acceleration is constant. "
            "When acceleration varies with time, integrate dv = a(t) dt."
        ),
        "narration_hi": (
            "अपने thought map में Node 2 और Node 3 को ध्यान से देखिए: आपने t=4 पर acceleration तो 12 m/s² सही निकाला, "
            "लेकिन फिर आपने यह मान लिया कि यह acceleration शुरू से ही constant था। "
            "जैसा कि हरे रंग के remediation map में Pivot Node पर दर्शाया गया है, v=u+at equation केवल तभी valid है जब acceleration constant हो। "
            "यहाँ acceleration समय के साथ बदल रहा है, इसलिए हमें integration dv = a(t) dt का use करना होगा।"
        ),
        "socratic_prompt": (
            "Before applying algebraic kinematic equations, how can you test whether acceleration is constant or variable? "
            "If a = dv/dt, what does the integral ∫ 3t dt from 0 to 4 yield for velocity?"
        )
    },

    "chemistry_le_chatelier_catalyst": {
        "title": "🧪 Chemical Equilibrium: Catalyst on Yield",
        "subject": "Chemistry - Physical Chemistry",
        "problem_statement": (
            "For the exothermic Haber process: N₂(g) + 3H₂(g) ⇌ 2NH₃(g) (ΔH = -92 kJ/mol), "
            "how does adding an iron catalyst affect the equilibrium concentration and percentage yield of NH₃?"
        ),
        "student_concept": "Le Chatelier's Principle & Reaction Kinetics",
        "student_steps": (
            "Step 1: An iron catalyst speeds up the reaction.\n"
            "Step 2: Since NH₃ is being formed faster, the forward reaction becomes stronger.\n"
            "Step 3: According to Le Chatelier's principle, anything speeding up product formation shifts equilibrium to the right.\n"
            "Step 4: Therefore, adding a catalyst increases the final equilibrium yield of ammonia."
        ),
        "student_breakdown": (
            "Industrial plants spend so much money on expensive iron catalysts. "
            "Why does my chemistry textbook say the equilibrium yield remains unchanged? If yield doesn't increase, why use a catalyst?"
        ),
        "canonical_concept": "Thermodynamic Equilibrium vs Reaction Kinetics",
        "canonical_root_misconception": "Conflated Rate of Attaining Equilibrium with Equilibrium Position (Yield)",
        "derailment_step": 3,
        "derailment_reason": "Assumed catalyst alters the equilibrium constant K_eq, rather than lowering activation energy equally for both forward and reverse paths.",
        "student_nodes": [
            {"id": "S1", "label": "Noted catalyst speeds up reaction", "is_error": False},
            {"id": "S2", "label": "Assumed only forward reaction accelerates", "is_error": True, "detail": "Catalyst lowers activation barrier for both directions equally"},
            {"id": "S3", "label": "Invoked Le Chatelier to shift equilibrium right", "is_error": True, "detail": "Derailment: Catalyst is not a stress on equilibrium"},
            {"id": "S4", "label": "Concluded yield of NH₃ increases", "is_error": True, "detail": "Thermodynamically false"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Distinguish Kinetics (Rate) from Thermodynamics (Equilibrium Position)", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Catalyst lowers E_a by identical amount for both forward & reverse directions", "is_pivot": True, "detail": "Breakthrough: k_forward and k_reverse increase by exact same ratio"},
            {"id": "R3", "label": "Equilibrium Constant K_eq = k_f / k_r remains strictly unchanged", "is_pivot": False},
            {"id": "R4", "label": "Catalyst simply reduces the time required to reach this state", "is_pivot": False}
        ],
        "narration_en": (
            "Examine Node 2 and Node 3 in your student graph: you assumed the catalyst favors ammonia production over its decomposition. "
            "However, look at the green remediation map at the Pivot Node: a catalyst lowers activation energy equally for both forward and reverse reactions. "
            "Because both rate constants increase by the same factor, their ratio—the equilibrium constant K—remains identical."
        ),
        "narration_hi": (
            "अपने thought map में Node 2 और Node 3 पर ध्यान दीजिए: आपने मान लिया कि catalyst केवल forward reaction को speed up करता है। "
            "लेकिन हरे रंग के remediation map में Pivot Node को देखिए: catalyst forward और reverse दोनों reactions की activation energy को equally reduce करता है। "
            "इसलिए equilibrium constant K_eq नहीं बदलता, और final yield identical रहती है।"
        ),
        "socratic_prompt": (
            "Recall the definition of the equilibrium constant K_eq = k_forward / k_backward. "
            "If a catalyst multiplies both k_forward and k_backward by 1,000, what happens to the value of K_eq?"
        )
    }
}

# Alias for backwards compatibility
SAMPLE_DOUBTS["incline_friction_work_energy"] = SAMPLE_DOUBTS["spring_friction_energy"]
SAMPLE_DOUBTS["vertical_circle_centripetal"] = SAMPLE_DOUBTS["circular_motion_turn"]
