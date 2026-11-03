"""
Pre-curated realistic STEM doubts reflecting classic conceptual traps
faced by Indian students in competitive and foundational exams (JEE, NEET, CBSE).
"""

SAMPLE_DOUBTS = {
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
            {"id": "S4", "label": "Applied standard formula v = u + at = 48 m/s", "is_error": True, "detail": "Invalid equation for non-constant acceleration"},
            {"id": "S5", "label": "Applied s = ut + 0.5 a t² = 96 m", "is_error": True, "detail": "Compounded error from constant-acceleration formula"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Recognize a = dv/dt is variable (time-dependent)", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Set up differential definition dv = a(t) dt", "is_pivot": True, "detail": "Breakthrough: Use integration instead of algebraic equations"},
            {"id": "R3", "label": "Integrate: v(t) = ∫ 3t dt = 1.5 t² -> v(4) = 24 m/s", "is_pivot": False},
            {"id": "R4", "label": "Integrate position: s(t) = ∫ v(t) dt = ∫ 1.5 t² dt = 0.5 t³", "is_pivot": False},
            {"id": "R5", "label": "Evaluate at t = 4: s(4) = 0.5 * (64) = 32 m", "is_pivot": False}
        ],
        "narration_en": (
            "Look at Node 2 and Node 3 in your graph: you correctly calculated the instantaneous acceleration at t=4 as 12 m/s², "
            "but then you treated this 12 m/s² as if it were acting constantly from t=0. "
            "As highlighted in the emerald green remediation map at the Pivot Node, standard kinematic equations like v=u+at only hold when acceleration is constant. "
            "When acceleration is a function of time, we must return to first principles and integrate dv = a(t) dt."
        ),
        "narration_hi": (
            "अपने ग्राफ़ में नोड 2 और नोड 3 को ध्यान से देखिए: आपने t=4 पर त्वरण तो 12 m/s² सही निकाला, "
            "लेकिन फिर आपने यह मान लिया कि यह त्वरण शुरू से ही स्थिर था। "
            "जैसा कि हरे रंग के रेमेडिएशन मैप में पिवट नोड पर दर्शाया गया है, v=u+at समीकरण केवल तभी लागू होता है जब त्वरण नियत (constant) हो। "
            "यहाँ त्वरण समय के साथ बदल रहा है, इसलिए हमें समाकलन (integration) dv = a(t) dt का उपयोग करना होगा।"
        ),
        "socratic_prompt": (
            "Before applying algebraic kinematic equations, how can you test whether acceleration is constant or variable? "
            "If a = dv/dt, what does the integral ∫ 3t dt from 0 to 4 yield for velocity?"
        )
    },

    "incline_friction_work_energy": {
        "title": "🏔️ Work-Energy Theorem: Incline with Friction",
        "subject": "Physics - Mechanics",
        "problem_statement": (
            "A block of mass m = 2 kg slides down a rough incline of angle θ = 30° and length L = 10 m. "
            "The coefficient of kinetic friction is μ = 0.2. Find its velocity at the bottom using energy principles."
        ),
        "student_concept": "Conservation of Mechanical Energy (E_initial = E_final)",
        "student_steps": (
            "Step 1: At the top of the ramp, the block has gravitational potential energy: U = m * g * h = 2 * 9.8 * (10 * sin 30°) = 98 J.\n"
            "Step 2: By conservation of energy, all potential energy transforms into kinetic energy at the bottom: E_initial = E_final.\n"
            "Step 3: So 98 J = 0.5 * m * v² = 0.5 * 2 * v² = v².\n"
            "Step 4: Therefore, v = √98 ≈ 9.9 m/s."
        ),
        "student_breakdown": (
            "My friend used Newton's second law and got v ≈ 8.0 m/s. "
            "I thought energy conservation always works regardless of the path. Where did my energy balance go wrong?"
        ),
        "canonical_concept": "Work-Energy Theorem with Non-Conservative Forces",
        "canonical_root_misconception": "Ignored Work Done by Non-Conservative (Frictional) Forces",
        "derailment_step": 2,
        "derailment_reason": "Equated mechanical energy E_initial = E_final while ignoring dissipated thermal energy due to friction W_nc = -f_k * L.",
        "student_nodes": [
            {"id": "S1", "label": "Computed U_initial = m g h = 98 J", "is_error": False},
            {"id": "S2", "label": "Stated E_initial = E_final (Pure Conservation)", "is_error": True, "detail": "Derailment: Friction does negative work, dissipating mechanical energy"},
            {"id": "S3", "label": "Equated m g h = 0.5 m v²", "is_error": True, "detail": "Omitted friction work term"},
            {"id": "S4", "label": "Obtained v = 9.9 m/s (Frictionless speed)", "is_error": True, "detail": "Overestimated speed by ignoring energy loss"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Draw Free-Body Diagram: Normal Force N = mg cos θ", "is_pivot": False},
            {"id": "R2", "label": "Calculate Friction Force: f_k = μ N = μ mg cos θ", "is_pivot": False},
            {"id": "R3", "label": "💡 PIVOT: Apply Work-Energy Theorem: ΔK = W_conservative + W_friction", "is_pivot": True, "detail": "Breakthrough: Include W_nc = -f_k * d"},
            {"id": "R4", "label": "Substitute: 0.5 m v² = m g h - f_k * L", "is_pivot": False},
            {"id": "R5", "label": "Solve for v: v = √(2(gh - μ g cos θ * L)) ≈ 8.0 m/s", "is_pivot": False}
        ],
        "narration_en": (
            "Take a close look at Node 2 in your graph: you declared that initial mechanical energy equals final mechanical energy. "
            "However, as shown in the green remediation map at the Pivot Node, friction is a non-conservative force that removes energy from the mechanical system. "
            "You cannot equate potential energy directly to kinetic energy when friction does work along the 10-meter incline."
        ),
        "narration_hi": (
            "अपने ग्राफ़ में नोड 2 को देखिए: आपने मान लिया कि प्रारंभिक यांत्रिक ऊर्जा अंतिम यांत्रिक ऊर्जा के बराबर है। "
            "लेकिन जैसा कि हरे रंग के रेमेडिएशन मैप में पिवट नोड पर दिखाया गया है, घर्षण (friction) एक गैर-संरक्षी बल (non-conservative force) है। "
            "जब 10 मीटर की ढलान पर घर्षण कार्य कर रहा हो, तो संभावित ऊर्जा सीधे गतिज ऊर्जा में नहीं बदलेगी।"
        ),
        "socratic_prompt": (
            "Notice how in your free-body diagram, friction opposes the sliding motion. "
            "What is the sign of the work done by friction, and how does that modify the equation ΔK = W_total?"
        )
    },

    "vertical_circle_centripetal": {
        "title": "🎡 Circular Motion: Minimum Tension at Top of Vertical Loop",
        "subject": "Physics - Mechanics",
        "problem_statement": (
            "A small ball of mass m attached to a light string of length R is whirled in a vertical circle. "
            "What is the minimum speed v_top at the top of the loop so that the string does not go slack?"
        ),
        "student_concept": "Balancing Centrifugal and Centripetal Forces",
        "student_steps": (
            "Step 1: At the top of the circle, the outward centrifugal force is m*v²/R pointing upward.\n"
            "Step 2: Gravity mg pulls downward and string tension T pulls downward.\n"
            "Step 3: For the string not to be slack, tension T must be greater than zero.\n"
            "Step 4: I balanced the forces: T + mg + mv²/R = 0, which gave me negative tension, so I thought T = mg."
        ),
        "student_breakdown": (
            "I get confused about whether centripetal force points upward or downward at the top. "
            "Why do both gravity and tension point toward the center, and what provides the centripetal acceleration?"
        ),
        "canonical_concept": "Circular Dynamics & Inertial Frame Force Identification",
        "canonical_root_misconception": "Treated Centripetal Force as an Independent Third Force",
        "derailment_step": 3,
        "derailment_reason": "Conflated the net inward required force (mv²/R) with a physical applied force, leading to double-counting or wrong sign balance.",
        "student_nodes": [
            {"id": "S1", "label": "Identified downward gravity mg & downward tension T", "is_error": False},
            {"id": "S2", "label": "Added an independent outward force vector without reference frame", "is_error": True, "detail": "Double counting inertial effect as real force"},
            {"id": "S3", "label": "Mixed frame equations: T + mg + mv²/R = 0", "is_error": True, "detail": "Derailment: Incorrect force summation resulting in negative quantities"},
            {"id": "S4", "label": "Guessing T = mg", "is_error": True, "detail": "Arbitrary patch without dynamic basis"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Select Inertial Frame of Reference", "is_pivot": False},
            {"id": "R2", "label": "Identify ONLY real contact and field forces: T (down) and mg (down)", "is_pivot": False},
            {"id": "R3", "label": "💡 PIVOT: Net Real Force provides Centripetal Acceleration: Σ F_radial = m (v²/R)", "is_pivot": True, "detail": "Breakthrough: Centripetal force is the net result, not an extra force"},
            {"id": "R4", "label": "Write Equation: T + mg = m v²/R  =>  T = m(v²/R) - mg", "is_pivot": False},
            {"id": "R5", "label": "Impose Slack Condition: T ≥ 0  =>  m v²/R ≥ mg  =>  v_top ≥ √(g R)", "is_pivot": False}
        ],
        "narration_en": (
            "Notice Node 2 in your graph where you introduced an independent force alongside gravity and tension. "
            "Centripetal acceleration is the required kinematics, not an extra physical entity pushing on the ball. "
            "Look at the green remediation map at the Pivot Node: both tension and gravity point downwards, "
            "and their sum alone constitutes the net inward force providing m v squared over R."
        ),
        "narration_hi": (
            "अपने ग्राफ़ में नोड 2 को देखिए, जहाँ आपने गुरुत्वाकर्षण और तनाव के अलावा एक अलग बल जोड़ दिया। "
            "अभिकेंद्री त्वरण (centripetal acceleration) केवल गति का परिणाम है, कोई अलग से लगने वाला तीसरा बल नहीं। "
            "हरे रंग के रेमेडिएशन मैप में पिवट नोड को देखिए: शीर्ष पर तनाव और गुरुत्वाकर्षण दोनों नीचे की ओर हैं, "
            "और इन दोनों का योग ही गेंद को वृत्त में घुमाने के लिए आवश्यक नेट बल प्रदान करता है।"
        ),
        "socratic_prompt": (
            "In an inertial frame, what physical bodies are in direct contact with or exerting fields on the ball at the top? "
            "Once you sum only those real physical forces, what must their net value equal according to Newton's Second Law?"
        )
    },

    "chemistry_le_chatelier_catalyst": {
        "title": "🧪 Chemical Equilibrium: Effect of Catalyst on Yield",
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
        "derailment_reason": "Assumed catalyst alters the thermodynamic state function ΔG° or equilibrium constant K_eq, rather than lowering activation energy equally for both forward and reverse paths.",
        "student_nodes": [
            {"id": "S1", "label": "Noted catalyst speeds up reaction", "is_error": False},
            {"id": "S2", "label": "Assumed only forward reaction accelerates", "is_error": True, "detail": "Catalyst lowers activation barrier for both directions equally"},
            {"id": "S3", "label": "Invoked Le Chatelier to shift equilibrium right", "is_error": True, "detail": "Derailment: Le Chatelier responds to stress, catalyst is not a stress on equilibrium"},
            {"id": "S4", "label": "Concluded yield of NH₃ increases", "is_error": True, "detail": "Thermodynamically false"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Distinguish Kinetics (Rate) from Thermodynamics (Equilibrium Position)", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Catalyst lowers E_a by identical amount for both forward & reverse directions", "is_pivot": True, "detail": "Breakthrough: k_forward and k_reverse increase by exact same ratio"},
            {"id": "R3", "label": "Equilibrium Constant K_eq = k_f / k_r remains strictly unchanged", "is_pivot": False},
            {"id": "R4", "label": "Equilibrium composition and final yield are identical to uncatalyzed system", "is_pivot": False},
            {"id": "R5", "label": "Catalyst simply reduces the time required to reach this state", "is_pivot": False}
        ],
        "narration_en": (
            "Examine Node 2 and Node 3 in your student graph: you assumed the catalyst favors ammonia production over its decomposition. "
            "However, look at the green remediation map at the Pivot Node: a catalyst lowers the activation energy by the exact same value for both the forward and reverse reactions. "
            "Because both rate constants increase by the same factor, their ratio—the equilibrium constant K—remains identical."
        ),
        "narration_hi": (
            "अपने ग्राफ़ में नोड 2 और नोड 3 पर ध्यान दीजिए: आपने मान लिया कि उत्प्रेरक (catalyst) केवल अमोनिया बनने की गति बढ़ाता है। "
            "लेकिन हरे रंग के रेमेडिएशन मैप में पिवट नोड को देखिए: उत्प्रेरक अग्र (forward) और पश्च (reverse) दोनों अभिक्रियाओं की सक्रियण ऊर्जा (activation energy) को समान रूप से कम करता है। "
            "इसलिए साम्य स्थिरांक (K_eq) नहीं बदलता, और अंतिम उत्पाद का प्रतिशत वही रहता है।"
        ),
        "socratic_prompt": (
            "Recall the definition of the equilibrium constant K_eq = k_forward / k_backward. "
            "If a catalyst multiplies both k_forward and k_backward by 1,000, what happens to the value of K_eq?"
        )
    }
}
