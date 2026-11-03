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
        "problem_statement_hi": (
            "एक 2 किलोग्राम का गुटका 5 मीटर लंबी ढलान पर नीचे फिसलता है, जिसमें एक खुरदरा घर्षण क्षेत्र (घर्षण गुणांक μ = 0.2, 3 मीटर तक) है। "
            "तल पर यह एक स्प्रिंग (k = 400 N/m) से टकराता है। अधिकतम संपीड़न ज्ञात कीजिए।"
        ),
        "student_concept": "Conservation of Mechanical Energy (mgh = 1/2 k x²)",
        "student_concept_hi": "यांत्रिक ऊर्जा संरक्षण (mgh = 1/2 k x²)",
        "student_steps": (
            "Step 1: Identified initial height h and spring contact.\n"
            "Step 2: Assumed that throughout the entire motion, Total Mechanical Energy is strictly conserved.\n"
            "Step 3: Equated mgh directly to 1/2 k x² without considering the rough patch.\n"
            "Step 4: Solved for compression x and obtained ~0.7 m, which is much higher than the answer key."
        ),
        "student_steps_hi": (
            "चरण 1: प्रारंभिक ऊंचाई h और स्प्रिंग संपर्क की पहचान की।\n"
            "चरण 2: मान लिया कि संपूर्ण गति के दौरान यांत्रिक ऊर्जा पूर्णतः संरक्षित है।\n"
            "चरण 3: खुरदरे भाग पर विचार किए बिना सीधे mgh = 1/2 k x² रख दिया।\n"
            "चरण 4: संपीड़न x हल किया और ~0.7 मीटर प्राप्त हुआ, जो उत्तर कुंजी से बहुत अधिक है।"
        ),
        "student_breakdown": (
            "My calculated compression is roughly 0.7 m, which is much higher than the solution key. "
            "I used conservation of energy, where did my equation derail?"
        ),
        "student_breakdown_hi": (
            "मेरा परिकलित संपीड़न लगभग 0.7 मीटर आ रहा है, जो उत्तर कुंजी से बहुत अधिक है। "
            "मैंने ऊर्जा संरक्षण लगाया था, मेरा समीकरण कहाँ गलत हुआ?"
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
        "narration_pure_hi": (
            "आपने यह बिल्कुल सही समझा कि गुरुत्वीय स्थितिज ऊर्जा स्प्रिंग की स्थितिज ऊर्जा में रूपांतरित होगी। "
            "परंतु अपने विचार मानचित्र के नोड 2 को ध्यानपूर्वक देखिए: आपने मान लिया कि संपूर्ण गति के दौरान यांत्रिक ऊर्जा पूर्णतः संरक्षित है। "
            "चूँकि ढलान पर एक खुरदरा घर्षण क्षेत्र है, इसलिए घर्षण बल ऋणात्मक कार्य करता है, जिससे यांत्रिक ऊर्जा का कुछ भाग ऊष्मा में परिवर्तित हो जाता है। "
            "समाधान मानचित्र के पिवट नोड को देखिए: स्प्रिंग ऊर्जा की तुलना करने से पूर्व घर्षण द्वारा किए गए कार्य को घटाना आवश्यक है। "
            "स्प्रिंग तक पहुँचने पर गुटके के पास वास्तव में कितनी यांत्रिक ऊर्जा शेष बचेगी?"
        ),
        "socratic_prompt": (
            "Rough patch पर friction से lost होने वाली heat energy का formula क्या होगा? "
            "क्या इसे initial energy में add करेंगे या subtract?"
        ),
        "socratic_prompt_hi": (
            "खुरदरे पथ पर घर्षण द्वारा क्षय हुई ऊष्मा ऊर्जा का सूत्र क्या होगा? "
            "क्या इसे प्रारंभिक यांत्रिक ऊर्जा में जोड़ेंगे या घटाएंगे?"
        )
    },

    "newton_third_law_horse_cart": {
        "title": "🐎 Newton's 3rd Law (Horse & Cart Paradox)",
        "subject": "Physics - Dynamics",
        "problem_statement": (
            "A horse pulls a cart forward with acceleration 1.5 m/s². "
            "Explain the forces and find net force if cart mass is 200 kg."
        ),
        "problem_statement_hi": (
            "एक घोड़ा 1.5 मीटर/सेकंड² के त्वरण से गाड़ी को आगे खींचता है। "
            "बलों की व्याख्या कीजिए और यदि गाड़ी का द्रव्यमान 200 किलोग्राम है तो परिणामी बल ज्ञात कीजिए।"
        ),
        "student_concept": "Newton's Third Law (Action and Reaction Forces)",
        "student_concept_hi": "न्यूटन का तीसरा नियम (क्रिया और प्रतिक्रिया बल)",
        "student_steps": (
            "Step 1: Horse pulls cart forward with force F.\n"
            "Step 2: By Newton's Third Law, cart pulls horse backward with equal and opposite force -F.\n"
            "Step 3: Summing the forces gives F + (-F) = 0. Forces cancel each other out.\n"
            "Step 4: Concluded that the net force is zero, so the cart can never accelerate."
        ),
        "student_steps_hi": (
            "चरण 1: घोड़ा गाड़ी को आगे F बल से खींचता है।\n"
            "चरण 2: न्यूटन के तीसरे नियम से, गाड़ी घोड़े को पीछे की ओर समान और विपरीत बल -F से खींचती है।\n"
            "चरण 3: बलों का योग F + (-F) = 0 है। बल एक-दूसरे को निरस्त कर देते हैं।\n"
            "चरण 4: निष्कर्ष निकाला कि परिणामी बल शून्य है, अतः गाड़ी कभी त्वरित नहीं हो सकती।"
        ),
        "student_breakdown": (
            "If action and reaction forces are always equal and opposite, how does the cart ever accelerate? "
            "Why don't the forces simply cancel out to zero?"
        ),
        "student_breakdown_hi": (
            "यदि क्रिया और प्रतिक्रिया बल सदैव समान और विपरीत होते हैं, तो गाड़ी कभी आगे कैसे बढ़ती है? "
            "बल एक-दूसरे को निरस्त क्यों नहीं करते?"
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
        "narration_pure_hi": (
            "आपने न्यूटन के तीसरे नियम का सही स्मरण किया कि क्रिया और प्रतिक्रिया बल परिमाण में समान और दिशा में विपरीत होते हैं। "
            "परंतु अपने विचार मानचित्र के नोड 3 को देखिए: आपने घोड़े पर लगने वाले बल को गाड़ी पर लगने वाले बल से निरस्त मान लिया। "
            "क्रिया और प्रतिक्रिया बल दो भिन्न-भिन्न पिंडों पर कार्य करते हैं, अतः वे कभी भी एक-दूसरे को निरस्त नहीं कर सकते। "
            "समाधान मानचित्र के पिवट नोड को देखिए: केवल गाड़ी का मुक्त पिंड आरेख बनाइए। गाड़ी को आगे खींचने वाला बाह्य बल कौन सा है?"
        ),
        "socratic_prompt": (
            "अगर आप सिर्फ cart को isolate करें, तो cart पर forward direction में pull करने वाला external force कौन सा है? "
            "क्या cart पर -F लग रहा है या horse पर?"
        ),
        "socratic_prompt_hi": (
            "यदि आप केवल गाड़ी को अलग करके विचार करें, तो गाड़ी पर आगे की ओर लगने वाला बाह्य बल कौन सा है? "
            "क्या गाड़ी पर -F लग रहा है या घोड़े पर?"
        )
    },

    "circular_motion_turn": {
        "title": "🏎️ Circular Motion & Centrifugal Pseudo-Force",
        "subject": "Physics - Dynamics",
        "problem_statement": (
            "A car moves around a flat circular curve of radius 50 m at 20 m/s. "
            "Find the minimum static friction coefficient needed to prevent slipping."
        ),
        "problem_statement_hi": (
            "एक कार 50 मीटर त्रिज्या वाले समतल वृत्तीय मोड़ पर 20 मीटर/सेकंड के वेग से मुड़ती है। "
            "फिसलने से बचने के लिए आवश्यक न्यूनतम स्थैतिक घर्षण गुणांक ज्ञात कीजिए।"
        ),
        "student_concept": "Balancing Centrifugal Outward Force against Friction",
        "student_concept_hi": "अपकेंद्रीय छद्म-बल को घर्षण बल से संतुलित करना",
        "student_steps": (
            "Step 1: Identified car turning with radius R = 50 m and v = 20 m/s.\n"
            "Step 2: Assumed an outward centrifugal force m v² / R acts on the car in ground frame.\n"
            "Step 3: Added forward drive force and centrifugal force via vector sum against friction.\n"
            "Step 4: Arrived at an unrealistically large friction coefficient."
        ),
        "student_steps_hi": (
            "चरण 1: कार R = 50 मीटर और v = 20 मीटर/सेकंड से मुड़ रही है।\n"
            "चरण 2: मान लिया कि जमीन के निर्देश तंत्र में बाहर की ओर अपकेंद्रीय बल m v² / R लगता है।\n"
            "चरण 3: आगे के बल और अपकेंद्रीय बल का सदिश योग घर्षण के विरुद्ध निकाला।\n"
            "चरण 4: बहुत अधिक घर्षण गुणांक प्राप्त हुआ।"
        ),
        "student_breakdown": (
            "The friction coefficient comes out unrealistically large, and I am confused about which way friction points. "
            "Why doesn't centrifugal force balance the turn?"
        ),
        "student_breakdown_hi": (
            "घर्षण गुणांक अवास्तविक रूप से बहुत अधिक आ रहा है, और मुझे समझ नहीं आ रहा कि घर्षण किस दिशा में कार्य करता है। "
            "अपकेंद्रीय बल मोड़ को संतुलित क्यों नहीं करता?"
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
        "narration_pure_hi": (
            "आपने सही पहचाना कि 50 मीटर त्रिज्या वाले मोड़ पर 20 मीटर प्रति सेकंड के वेग से कार वृत्तीय गति कर रही है। "
            "परंतु नोड 2 पर देखिए: आपने स्थिर जड़त्वीय निर्देश तंत्र में बाहर की ओर अपकेंद्रीय छद्म-बल जोड़ दिया। "
            "जमीन के निर्देश तंत्र में केवल वास्तविक संपर्क बल कार्य करते हैं। "
            "समाधान मानचित्र के पिवट नोड को देखिए: कार को केंद्र की ओर त्वरित रखने के लिए आवश्यक अभिकेंद्रीय त्वरण वास्तव में सड़क और टायर के बीच स्थित स्थैतिक घर्षण द्वारा ही प्रदान किया जाता है।"
        ),
        "socratic_prompt": (
            "Ground frame से देखने पर, car को circular path में turn कराने के लिए net static friction force किस direction में point करना चाहिए? "
            "क्या केंद्र की ओर या केंद्र से बाहर?"
        ),
        "socratic_prompt_hi": (
            "जमीन से देखने वाले जड़त्वीय प्रेक्षक के लिए कार को मोड़ने हेतु आवश्यक अभिकेंद्रीय बल कौन सा वास्तविक संपर्क बल प्रदान कर रहा है? "
            "क्या अपकेंद्रीय बल स्थिर जमीन के निर्देश तंत्र में वास्तव में अस्तित्व रखता है?"
        )
    },

    "rotational_skater_spin": {
        "title": "⛸️ Rotational Dynamics: Skater Arm Pull",
        "subject": "Physics - Rotational Mechanics",
        "problem_statement": (
            "A skater spins with initial angular velocity ω₀. Pulling arms inward cuts moment of inertia from I₀ to I₀ / 3. "
            "Compare initial and final rotational kinetic energy."
        ),
        "problem_statement_hi": (
            "एक स्केटर प्रारंभिक कोणीय वेग ω₀ से घूमती है। भुजाओं को अंदर खींचने पर उसका जड़त्व आघूर्ण I₀ से घटकर I₀ / 3 हो जाता है। "
            "प्रारंभिक और अंतिम घूर्णन गतिज ऊर्जा की तुलना कीजिए।"
        ),
        "student_concept": "Conservation of Rotational Kinetic Energy (1/2 I ω² = const)",
        "student_concept_hi": "घूर्णन गतिज ऊर्जा का संरक्षण (1/2 I ω² = नियतांक)",
        "student_steps": (
            "Step 1: Noticed that no external torque acts on the skater.\n"
            "Step 2: Assumed rotational kinetic energy must be conserved: 1/2 I₀ ω₀² = 1/2 I_f ω_f².\n"
            "Step 3: Solved for final angular velocity and found ω_f = √3 ω₀.\n"
            "Step 4: Realized this directly contradicts angular momentum conservation (L = I ω => ω_f = 3 ω₀)."
        ),
        "student_steps_hi": (
            "चरण 1: देखा कि स्केटर पर कोई बाह्य बल आघूर्ण कार्य नहीं कर रहा है।\n"
            "चरण 2: माना कि घूर्णन गतिज ऊर्जा संरक्षित रहनी चाहिए: 1/2 I₀ ω₀² = 1/2 I_f ω_f²।\n"
            "चरण 3: अंतिम कोणीय वेग निकाला और पाया कि ω_f = √3 ω₀ है।\n"
            "चरण 4: अनुभव किया कि यह कोणीय संवेग संरक्षण (L = I ω => ω_f = 3 ω₀) का खंडन करता है।"
        ),
        "student_breakdown": (
            "When I use conservation of angular momentum (L = I*ω), I get ω_f = 3*ω₀. "
            "Why are energy conservation and angular momentum conservation giving conflicting results?"
        ),
        "student_breakdown_hi": (
            "जब मैं कोणीय संवेग संरक्षण (L = I*ω) का उपयोग करता हूँ, तो मुझे ω_f = 3*ω₀ प्राप्त होता है। "
            "ऊर्जा संरक्षण और कोणीय संवेग संरक्षण परस्पर विरोधी परिणाम क्यों दे रहे हैं?"
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
        "narration_pure_hi": (
            "आपने कोणीय संवेग संरक्षण का बिल्कुल सटीक अनुप्रयोग किया कि हाथ सिकोड़ने पर जड़त्व आघूर्ण घटता है और कोणीय वेग बढ़ जाता है। "
            "परंतु नोड 2 पर देखिए: आपने मान लिया कि घूर्णन गतिज ऊर्जा भी अपरिवर्तित रहेगी। "
            "जब स्केटर अपनी भुजाओं को अंदर खींचती है, तो उसकी मांसपेशियाँ आंतरिक धनात्मक कार्य करती हैं। "
            "समाधान मानचित्र के पिवट नोड को देखिए: आंतरिक कार्य के कारण घूर्णन गतिज ऊर्जा वास्तव में बढ़ जाती है। क्या यह आंतरिक कार्य मांसपेशियों की रासायनिक ऊर्जा से नहीं आ रहा?"
        ),
        "socratic_prompt": (
            "L = I * ω conservation use करके बताइए: अगर moment of inertia one-third (I₀ / 3) हो जाता है, "
            "तो angular velocity कितने गुना बढ़ेगी? और फिर K = 1/2 I ω² का ratio क्या होगा?"
        ),
        "socratic_prompt_hi": (
            "कोणीय संवेग संरक्षण L = I * ω का उपयोग करके बताइए: यदि जड़त्व आघूर्ण एक-तिहाई (I₀ / 3) हो जाता है, "
            "तो कोणीय वेग कितने गुना बढ़ेगा? और इसके पश्चात घूर्णन गतिज ऊर्जा K = 1/2 I ω² का अनुपात क्या होगा?"
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
    },

    "economics_rent_control": {
        "title": "📉 Economics: Rent Control Price Ceiling",
        "subject": "Economics - Microeconomics & Market Policy",
        "problem_statement": (
            "A municipal government imposes a binding rent ceiling below market equilibrium to make urban housing affordable. "
            "Does this policy guarantee affordable housing for all low-income residents in the long run?"
        ),
        "problem_statement_hi": (
            "शहरी आवास को सस्ता बनाने के लिए नगर पालिका बाजार संतुलन से नीचे किराया सीमा (मूल्य नियंत्रण) लागू करती है। "
            "क्या यह नीति दीर्घावधि में सभी निम्न-आय वर्ग के नागरिकों के लिए किफायती आवास की उपलब्धता सुनिश्चित करती है?"
        ),
        "student_concept": "Price Ceilings & Inelastic Housing Supply (Demand increases while buildings stay fixed)",
        "student_concept_hi": "मूल्य सीमा और बेलोचदार आवास आपूर्ति (मकान स्थिर रहते हैं जबकि मांग बढ़ती है)",
        "student_steps": (
            "Step 1: Identified that rent is capped below equilibrium, making apartments cheaper.\n"
            "Step 2: Concluded that quantity demanded increases as more families can now afford housing.\n"
            "Step 3: Assumed housing supply remains fixed because existing apartment buildings cannot be moved or demolished easily.\n"
            "Step 4: Concluded that all low-income tenants successfully obtain cheaper housing without negative side-effects."
        ),
        "student_steps_hi": (
            "चरण 1: देखा कि किराया संतुलन से नीचे सीमित है, जिससे आवास सस्ता हो जाता है।\n"
            "चरण 2: निष्कर्ष निकाला कि मांग बढ़ेगी क्योंकि अधिक परिवार इसे वहन कर सकेंगे।\n"
            "चरण 3: मान लिया कि आवास आपूर्ति स्थिर रहेगी क्योंकि मौजूदा इमारतों को आसानी से हटाया नहीं जा सकता।\n"
            "चरण 4: निष्कर्ष निकाला कि बिना किसी दुष्प्रभाव के सभी जरूरतमंदों को सस्ता घर मिल जाएगा।"
        ),
        "student_breakdown": (
            "If buildings are already built and landlords cannot move them, why would supply decrease? "
            "Where does the economic shortage come from?"
        ),
        "student_breakdown_hi": (
            "यदि मकान पहले से बने हैं और मकान मालिक उन्हें कहीं ले नहीं जा सकते, तो आवास आपूर्ति कैसे घटेगी? "
            "दीर्घकालिक कमी क्यों उत्पन्न होती है?"
        ),
        "canonical_concept": "Price Elasticity of Supply Over Time & Deadweight Shortage",
        "canonical_root_misconception": "Conflating Immediate Fixed Housing Stock with Long-Run Supply Elasticity",
        "derailment_step": 3,
        "derailment_reason": "Treated housing supply as permanently inelastic, overlooking that landlords adjust along other margins: deferring maintenance, converting rentals to commercial/condo use, or withholding units.",
        "student_nodes": [
            {"id": "S1", "label": "Rent ceiling set below equilibrium", "is_error": False},
            {"id": "S2", "label": "Quantity demanded expands rapidly", "is_error": False},
            {"id": "S3", "label": "Assumed housing supply is permanently fixed", "is_error": True, "detail": "Derailment: Landlords disinvest in upkeep or convert units over time"},
            {"id": "S4", "label": "Concluded universal affordable housing achieved", "is_error": True, "detail": "Overlooked persistent housing shortage & informal rationing"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Map Short-Run vs Long-Run supply curves", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Supply elasticity increases over time: capital disinvests when rent < marginal maintenance", "is_pivot": True, "detail": "Breakthrough: Price ceilings create persistent excess demand (Qd > Qs) and supply contraction"},
            {"id": "R3", "label": "Identify non-price rationing mechanisms (queues, deterioration, informal premiums)", "is_pivot": False},
            {"id": "R4", "label": "Formulate targeted supply-side housing subsidies instead of static price controls", "is_pivot": False}
        ],
        "narration_en": (
            "You accurately recognized that lower rent expands tenant demand. Your basic market intuition is sound. "
            "However, look at Node 3 in your thought map: you assumed physical buildings mean housing supply never responds to prices. "
            "Over time, landlords respond by cutting maintenance, turning rentals into co-ops, or building fewer units. "
            "As shown at the green Pivot Node, long-run supply is elastic. When quantity demanded exceeds declining supply, a severe shortage emerges."
        ),
        "narration_hi": (
            "आपने बिल्कुल सही समझा कि rent कम होने से demand तेजी से बढ़ेगी। "
            "लेकिन अपने thought map के Node 3 को देखिए: आपने मान लिया कि buildings immovable हैं तो supply कभी नहीं घटेगी। "
            "Long run में landlords maintenance रोक देते हैं, units को commercial use में convert करते हैं, और नए rentals का construction रुक जाता है। "
            "Remediation map के Pivot Node को देखिए: long-run supply elastic होती है, जिससे persistent housing shortage पैदा हो जाती है।"
        ),
        "narration_pure_hi": (
            "आपने बिल्कुल सटीक पहचाना कि किराया कम होने से आवास की मांग में वृद्धि होगी। "
            "परंतु अपने विचार मानचित्र के नोड 3 को देखिए: आपने मान लिया कि इमारतों के स्थिर होने से आपूर्ति भी सदैव अपरिवर्तित रहेगी। "
            "दीर्घावधि में मकान मालिक रखरखाव कम कर देते हैं और नई इकाइयों का निर्माण रुक जाता है। "
            "समाधान मानचित्र के पिवट नोड को देखिए: समय बीतने के साथ आपूर्ति लोचदार हो जाती है, जिससे बाजार में आवास की गंभीर कमी उत्पन्न होती है।"
        ),
        "socratic_prompt": (
            "Over a 5-year horizon, if rental income does not cover building upkeep and taxes, what choices will property owners make regarding maintenance and new rental investments?"
        ),
        "socratic_prompt_hi": (
            "यदि 5 वर्षों की अवधि में किराये से होने वाली आय रखरखाव और करों को पूरा न करे, तो मकान मालिक रख-रखाव और नए आवास निर्माण के संबंध में क्या निर्णय लेंगे?"
        )
    },

    "coding_balanced_parentheses": {
        "title": "💻 Computer Science: Balanced Parentheses & Stack Invariant",
        "subject": "Computer Science - Data Structures & Algorithms",
        "problem_statement": (
            "Given a string containing parentheses '(' and ')', write an algorithm to determine if the string is balanced. "
            "The student implements a counter: increment for '(', decrement for ')', and returns True if count == 0 at the end."
        ),
        "problem_statement_hi": (
            "कोष्ठक '(' और ')' वाली स्ट्रिंग दी गई है। यह जांचने के लिए एल्गोरिदम लिखें कि क्या कोष्ठक संतुलित हैं। "
            "छात्र एक काउंटर बनाता है: '(' पर +1, ')' पर -1, और अंत में count == 0 होने पर True देता है।"
        ),
        "student_concept": "Aggregate Frequency Parity (Equal number of opening and closing brackets)",
        "student_concept_hi": "सकल संख्या समानता (खुलने और बंद होने वाले कोष्ठकों की बराबर संख्या)",
        "student_steps": (
            "Step 1: Initialized counter balance = 0.\n"
            "Step 2: Iterated through characters: +1 for '(', -1 for ')'.\n"
            "Step 3: At string end, evaluated if balance == 0.\n"
            "Step 4: Concluded string is valid whenever total open brackets equal total close brackets."
        ),
        "student_steps_hi": (
            "चरण 1: काउंटर balance = 0 प्रारंभ किया।\n"
            "चरण 2: स्ट्रिंग के प्रत्येक अक्षर के लिए: '(' पर +1, ')' पर -1 किया।\n"
            "चरण 3: स्ट्रिंग के अंत में जांचा कि क्या balance == 0 है।\n"
            "चरण 4: निष्कर्ष निकाला कि यदि कुल खुलने वाले कोष्ठक बंद होने वाले कोष्ठकों के बराबर हैं, तो स्ट्रिंग वैध है।"
        ),
        "student_breakdown": (
            "The string ')(' has one '(' and one ')', so balance == 0. "
            "Why does my code return True for a clearly broken sequence?"
        ),
        "student_breakdown_hi": (
            "स्ट्रिंग ')(' में एक '(' और एक ')' है, इसलिए balance == 0 हो जाता है। "
            "मेरा कोड गलत अनुक्रम के लिए भी True क्यों दे रहा है?"
        ),
        "canonical_concept": "Prefix Invariant & LIFO Stack State",
        "canonical_root_misconception": "Treating Sequence Validation as Commutative Frequency Equality",
        "derailment_step": 3,
        "derailment_reason": "Treated bracket validation as a global summation, failing to check the prefix invariant: balance must NEVER drop below 0 at any intermediate index.",
        "student_nodes": [
            {"id": "S1", "label": "Initialized balance counter to 0", "is_error": False},
            {"id": "S2", "label": "Incremented for '(', decremented for ')'", "is_error": False},
            {"id": "S3", "label": "Evaluated balance only at terminal boundary", "is_error": True, "detail": "Derailment: Failed to enforce prefix non-negativity constraint during scan"},
            {"id": "S4", "label": "Approved invalid sequences like ')(' and ')()('", "is_error": True, "detail": "Premature closure cannot be compensated by subsequent openers"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Define formal grammar: every closing bracket must match an unclosed predecessor", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Enforce the Prefix Stack Invariant: balance >= 0 at EVERY step during iteration", "is_pivot": True, "detail": "Breakthrough: If balance < 0 at any moment, immediately terminate and return False"},
            {"id": "R3", "label": "Demonstrate equivalence to LIFO Stack pop on empty stack condition", "is_pivot": False},
            {"id": "R4", "label": "Verify both: (1) no underflow during scan, and (2) balance == 0 at termination", "is_pivot": False}
        ],
        "narration_en": (
            "You correctly realized that balanced brackets must contain equal opening and closing counts. That is a necessary condition. "
            "But look at Node 3 in your thought map: you only checked the balance at the very end. "
            "If a string starts with a closing bracket, it is already invalid, even if an opening bracket appears later. "
            "As shown at the green Pivot Node, you must enforce that the balance never drops below zero at any point during iteration."
        ),
        "narration_hi": (
            "आपने बिल्कुल सही पहचाना कि balanced parentheses में opening और closing brackets की संख्या बराबर होनी चाहिए। "
            "लेकिन अपने thought map के Node 3 को देखिए: आपने balance सिर्फ string के end में check किया। "
            "अगर string ')(' जैसी हो, तो पहले ही step पर closing bracket आ जाता है जो किसी open bracket से match नहीं करता। "
            "Remediation map के Pivot Node को देखिए: loop के दौरान balance कभी भी 0 से कम (negative) नहीं होना चाहिए।"
        ),
        "narration_pure_hi": (
            "आपने बिल्कुल सही पहचाना कि संतुलित कोष्ठकों में खुलने और बंद होने वाले कोष्ठकों की कुल संख्या समान होनी आवश्यक है। "
            "परंतु अपने विचार मानचित्र के नोड 3 को देखिए: आपने केवल स्ट्रिंग के अंत में समानता की जांच की। "
            "यदि स्ट्रिंग ')(' से शुरू होती है, तो वह पहले ही पद पर अमान्य हो जाती है। "
            "समाधान मानचित्र के पिवट नोड को देखिए: पूरी जांच के दौरान बैलेंस का मान किसी भी समय शून्य से नीचे नहीं गिरना चाहिए।"
        ),
        "socratic_prompt": (
            "In the string ')(' what is the balance value immediately after processing the first character, and how can your loop use that to return False early?"
        ),
        "socratic_prompt_hi": (
            "स्ट्रिंग ')(' में पहले अक्षर को प्रोसेस करने के तुरंत बाद बैलेंस का मान क्या होगा, और लूप इसका उपयोग करके तुरंत False कैसे लौटा सकता है?"
        )
    },

    "law_freedom_of_speech": {
        "title": "⚖️ Constitutional Law: Free Speech & Public Order Limits",
        "subject": "Law - Constitutional Law & Fundamental Rights",
        "problem_statement": (
            "A speaker delivers a controversial socio-political speech inside a private auditorium rented by a registered club. "
            "A local administrative officer orders the arrest of the speaker under Article 19(2) citing potential public annoyance. "
            "Can the state invoke public order restrictions against speech delivered in a closed private assembly?"
        ),
        "problem_statement_hi": (
            "एक वक्ता पंजीकृत क्लब द्वारा किराए पर लिए गए निजी सभागार के भीतर विवादास्पद सामाजिक-राजनीतिक भाषण देता है। "
            "एक स्थानीय प्रशासनिक अधिकारी सार्वजनिक रोष की आशंका का हवाला देते हुए अनुच्छेद 19(2) के तहत वक्ता को गिरफ्तार करने का आदेश देता है। "
            "क्या राज्य बंद निजी सभा में दिए गए भाषण के विरुद्ध सार्वजनिक व्यवस्था प्रतिबंध लागू कर सकता है?"
        ),
        "student_concept": "State Police Power & Article 19(2) Public Order Restrictions",
        "student_concept_hi": "राज्य की पुलिस शक्ति और अनुच्छेद 19(2) सार्वजनिक व्यवस्था प्रतिबंध",
        "student_steps": (
            "Step 1: Identified that Article 19(1)(a) grants freedom of speech and expression.\n"
            "Step 2: Noted that speech is not absolute and is subject to Article 19(2) reasonable restrictions, including 'public order'.\n"
            "Step 3: Assumed that because the speech contained provocative views, it inherently poses a threat to public order.\n"
            "Step 4: Concluded that the administrative officer acted lawfully to preempt potential unrest."
        ),
        "student_steps_hi": (
            "चरण 1: पहचाना कि अनुच्छेद 19(1)(a) वाक् और अभिव्यक्ति की स्वतंत्रता प्रदान करता है।\n"
            "चरण 2: ध्यान दिया कि यह अधिकार पूर्ण नहीं है और अनुच्छेद 19(2) के तहत 'सार्वजनिक व्यवस्था' सहित उचित प्रतिबंधों के अधीन है।\n"
            "चरण 3: मान लिया कि भाषण में उत्तेजक विचार थे, अतः यह स्वाभाविक रूप से सार्वजनिक व्यवस्था के लिए खतरा है।\n"
            "चरण 4: निष्कर्ष निकाला कि अधिकारी ने संभावित अशांति को रोकने के लिए वैध कार्रवाई की।"
        ),
        "student_breakdown": (
            "If the state has power to prevent riots, why can't it stop speech that might offend public sensibilities? "
            "Where is the statutory threshold crossed?"
        ),
        "student_breakdown_hi": (
            "यदि राज्य के पास अशांति रोकने की शक्ति है, तो वह ऐसे भाषण को क्यों नहीं रोक सकता जिससे सार्वजनिक भावनाएं आहत हो सकती हैं? "
            "विधिक सीमा कहाँ लांघी गई?"
        ),
        "canonical_concept": "Doctrine of Proximity & Direct Incitement (Spark in Powder Keg Test)",
        "canonical_root_misconception": "Conflating Law and Order (or Mere Displeasure) with Serious Threat to Public Order",
        "derailment_step": 3,
        "derailment_reason": "Equated controversial speech in a closed private forum with an imminent, direct threat to 'public order'. Constitutional jurisprudence (Ram Manohar Lohia, Shreya Singhal) requires a proximate, direct nexus between speech and public disorder, not hypothetical annoyance.",
        "student_nodes": [
            {"id": "S1", "label": "Identified Article 19(1)(a) fundamental right", "is_error": False},
            {"id": "S2", "label": "Identified Article 19(2) grounds including public order", "is_error": False},
            {"id": "S3", "label": "Assumed provocative views automatically equal public disorder", "is_error": True, "detail": "Derailment: Conflated private expression with clear and present danger to public order"},
            {"id": "S4", "label": "Sanctioned preventive state suppression without proximate nexus", "is_error": True, "detail": "Violated proportionality and proximity doctrine"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Distinguish 'Law & Order' vs 'Public Order' vs 'Security of State' (Three concentric circles)", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: The Proximity Test: Speech must be like a spark in a powder keg, not a remote fear", "is_pivot": True, "detail": "Breakthrough: Closed private meetings cannot be curtailed on speculative public disorder grounds"},
            {"id": "R3", "label": "Examine procedural threshold: state must demonstrate immediate incitement to imminent violence", "is_pivot": False},
            {"id": "R4", "label": "Conclude that the officer's action was ultra vires and violated Article 19(1)(a)", "is_pivot": False}
        ],
        "narration_en": (
            "You correctly noted that free speech is subject to reasonable restrictions under Article 19(2). Your constitutional basis is sound. "
            "However, look at Node 3 in your thought map: you assumed provocative speech automatically threatens public order. "
            "Constitutional law requires a proximate, direct link between the words and imminent violence, like a spark in a powder keg. "
            "In a closed private hall, remote public annoyance does not justify state censorship. Look at the green Pivot Node to see what standard applies."
        ),
        "narration_hi": (
            "आपने बिल्कुल सही याद किया कि Article 19(1)(a) की freedom absolute नहीं है और Article 19(2) में reasonable restrictions हैं। "
            "लेकिन अपने thought map के Node 3 को देखिए: आपने controversial speech को directly public disorder मान लिया। "
            "Supreme Court के अनुसार speech और violence के बीच direct और proximate nexus होना चाहिए, जैसे बारूद में चिंगारी। "
            "एक बंद private auditorium में दूर की आशंका पर arrest lawful नहीं हो सकती। Green Pivot Node को देखिए: state को imminent violence साबित करना जरूरी क्यों है?"
        ),
        "narration_pure_hi": (
            "आपने बिल्कुल सही पहचाना कि अनुच्छेद 19(1)(a) के तहत प्राप्त वाक् स्वतंत्रता अनुच्छेद 19(2) के युक्तियुक्त निर्बंधनों के अधीन है। "
            "परंतु अपने विचार मानचित्र के नोड 3 को देखिए: आपने विवादास्पद विचारों को सीधे सार्वजनिक व्यवस्था के लिए खतरा मान लिया। "
            "संवैधानिक विधि के अनुसार, अभिव्यक्ति और हिंसा के मध्य तात्कालिक और प्रत्यक्ष संबंध होना अनिवार्य है। "
            "बंद सभागार में दिए गए भाषण के आधार पर संभावित रोष की आशंका पर रोक लगाना असंवैधानिक है।"
        ),
        "socratic_prompt": (
            "Under the landmark Supreme Court ruling in Ram Manohar Lohia, what is the crucial legal distinction between an ordinary 'law and order' issue and a grave threat to 'public order'?"
        ),
        "socratic_prompt_hi": (
            "राम मनोहर लोहिया मामले में सर्वोच्च न्यायालय के अनुसार, सामान्य 'विधि एवं व्यवस्था' (Law and Order) और गंभीर 'सार्वजनिक व्यवस्था' (Public Order) के बीच क्या मूलभूत विधिक अंतर है?"
        )
    },

    "history_ww1_causality": {
        "title": "📜 World History: Outbreak & Structural Causality of World War I",
        "subject": "History - Modern World History & International Relations",
        "problem_statement": (
            "Analyze whether the assassination of Archduke Franz Ferdinand in Sarajevo in June 1914 was the sufficient cause of World War I, "
            "or explain why major European empires rapidly mobilized into a continent-wide total war within five weeks."
        ),
        "problem_statement_hi": (
            "विश्लेषण कीजिए कि क्या जून 1914 में सारायेवो में आर्कड्यूक फ्रांज फर्डिनेंड की हत्या प्रथम विश्व युद्ध का पर्याप्त कारण थी, "
            "या स्पष्ट कीजिए कि प्रमुख यूरोपीय साम्राज्य पाँच हफ्तों के भीतर महाद्वीपीय युद्ध में इतनी तेजी से क्यों लामबंद हुए।"
        ),
        "student_concept": "Single-Incident Causality (Sarajevo Assassination as Sole Cause of WWI)",
        "student_concept_hi": "एकल-घटना कारणता (सारायेवो हत्याकांड को प्रथम विश्व युद्ध का एकमात्र कारण मानना)",
        "student_steps": (
            "Step 1: Identified the assassination of Archduke Franz Ferdinand by Gavrilo Princip in Sarajevo on June 28, 1914.\n"
            "Step 2: Noted that Austria-Hungary declared war on Serbia directly in retaliation.\n"
            "Step 3: Concluded that because of this single terrorist attack, Germany, Russia, France, and Britain had no choice but to enter a world war.\n"
            "Step 4: Deduced that without this assassination, World War I would not have occurred in early 20th century Europe."
        ),
        "student_steps_hi": (
            "चरण 1: 28 जून 1914 को सारायेवो में गैवरिलो प्रिंसिप द्वारा आर्कड्यूक फ्रांज फर्डिनेंड की हत्या की पहचान की।\n"
            "चरण 2: ध्यान दिया कि ऑस्ट्रिया-हंगरी ने बदले की कार्रवाई के रूप में सीधे सर्बिया पर युद्ध की घोषणा की।\n"
            "चरण 3: निष्कर्ष निकाला कि इस एक आतंकी हमले के कारण जर्मनी, रूस, फ्रांस और ब्रिटेन को विश्व युद्ध में शामिल होना पड़ा।\n"
            "चरण 4: अनुमान लगाया कि यदि यह हत्या न हुई होती, तो 20वीं सदी के यूरोप में प्रथम विश्व युद्ध कभी न होता।"
        ),
        "student_breakdown": (
            "My history essay was marked down for confusing the immediate trigger with underlying structural causes. "
            "Wasn't the assassination the event that started the war?"
        ),
        "student_breakdown_hi": (
            "मेरे इतिहास के निबंध में अंक काटे गए क्योंकि मैंने तात्कालिक चिंगारी (Trigger) को व्यवस्थागत कारणों (Structural Causes) के साथ मिला दिया। "
            "क्या युद्ध की शुरुआत इसी हत्याकांड से नहीं हुई थी?"
        ),
        "canonical_concept": "Distinction Between Proximate Catalysts (Spark) and Structural Tinderbox (M-A-I-N Framework)",
        "canonical_root_misconception": "Monocausal & Teleological Fallacy (Conflating the Immediate Spark with the Systemic Fuel)",
        "derailment_step": 3,
        "derailment_reason": "Equated the proximate diplomatic spark with systemic causation. The assassination lit the match, but rigid mutual defense pacts, naval arms race, imperialist friction, and Balkan nationalism created the combustible structural powder keg.",
        "student_nodes": [
            {"id": "S1", "label": "June 1914: Archduke Franz Ferdinand assassinated in Sarajevo", "is_error": False},
            {"id": "S2", "label": "Austria-Hungary issued July Ultimatum to Serbia", "is_error": False},
            {"id": "S3", "label": "Concluded single assassination forced all European empires into war", "is_error": True, "detail": "Derailment: Omitted structural alliance traps, naval arms race & imperial tensions"},
            {"id": "S4", "label": "Inferred 20th-century peace would persist without Gavrilo Princip", "is_error": True, "detail": "Fallacy: Ignored the systemic inevitability of imperial friction"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Recognize the July 1914 Crisis as the proximate diplomatic trigger", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Structural Analysis: M-A-I-N (Militarism, Alliances, Imperialism, Nationalism)", "is_pivot": True, "detail": "Breakthrough: The assassination was only the spark; the alliances provided the explosive fuel"},
            {"id": "R3", "label": "Trace mobilization domino: Russian mobilization triggered the German Schlieffen Plan through Belgium", "is_pivot": False},
            {"id": "R4", "label": "Synthesize: Without systemic reform, any diplomatic crisis would have detonated the European powder keg", "is_pivot": False}
        ],
        "narration_en": (
            "You accurately pinpointed the Sarajevo assassination as the immediate catalyst of the July Crisis. "
            "However, look at Node 3 in your historical logic: you treated this single murder as the sufficient cause of a global war. "
            "The assassination was merely the match. The true explosive fuel was decades of militarism, entangling secret alliances, and imperial friction. "
            "Examine the green Pivot Node to understand how the M-A-I-N framework explains why a localized dispute inevitably escalated."
        ),
        "narration_hi": (
            "Aapne bilkul sahi identify kiya ki Sarajevo assassination July 1914 ka immediate catalyst tha. "
            "Lekin thought map ke Node 3 par dekhein: aapne is single event ko World War I ka sole cause maan liya. "
            "Assassination sirf ek matchstick thi, lekin asli explosive fuel decades of militarism, entangling alliances, aur imperial competition the. "
            "Green Pivot Node par notice karein: M-A-I-N framework kaise explain karta hai ki localized conflict global war mein kyun convert hua."
        ),
        "narration_pure_hi": (
            "आपने 1914 के सारायेवो हत्याकांड को तात्कालिक उत्प्रेरक के रूप में सही पहचाना। "
            "परंतु अपने विचार मानचित्र के नोड 3 पर ध्यान दें: आपने इस एकल घटना को विश्व युद्ध का एकमात्र पर्याप्त कारण मान लिया। "
            "हत्या केवल एक चिंगारी थी; बारूद तो गुप्त संधियों, सैन्यवाद और साम्राज्यवादी प्रतिस्पर्धा ने दशकों से तैयार किया था। "
            "हरे पिवट नोड को देखिए: यह दर्शाता है कि बाल्कन का स्थानीय संकट यूरोपीय महायुद्ध में क्यों बदल गया।"
        ),
        "socratic_prompt": (
            "If the conflict began strictly as a dispute between Austria-Hungary and Serbia over an assassination, why did Germany invade neutral Belgium and France within five weeks? What pre-existing alliance obligations and mobilization timetables dictated this escalation?"
        ),
        "socratic_prompt_hi": (
            "यदि यह संघर्ष केवल ऑस्ट्रिया-हंगरी और सर्बिया के बीच एक हत्या का विवाद था, तो जर्मनी ने पाँच हफ्तों के भीतर तटस्थ बेल्जियम और फ्रांस पर आक्रमण क्यों किया? किन पूर्व-मौजूदा संधियों और सैन्य योजनाओं ने इस गति को निर्धारित किया?"
        )
    },

    "literature_macbeth_tragic_flaw": {
        "title": "📖 Literature: Fatal Flaw (Hamartia) vs Fate in Shakespeare's Macbeth",
        "subject": "Literature - Dramatic Theory & Shakespearean Tragedy",
        "problem_statement": (
            "In Shakespeare's tragedy Macbeth, evaluate whether Macbeth is merely a passive victim of supernatural manipulation by the Weird Sisters and psychological coercion by Lady Macbeth, "
            "or whether his downfall is driven by his own internal tragic flaw (Hamartia)."
        ),
        "problem_statement_hi": (
            "शेक्सपियर की त्रासदी 'मैकबेथ' में मूल्यांकन कीजिए कि क्या मैकबेथ केवल चुड़ैलों के अलौकिक हेरफेर और लेडी मैकबेथ के मनोवैज्ञानिक दबाव का असहाय शिकार है, "
            "या उसका पतन उसके अपने आंतरिक दुखद दोष (हमारशिया) से प्रेरित है।"
        ),
        "student_concept": "External Determinism & Denial of Protagonist Moral Agency",
        "student_concept_hi": "बाहरी नियतिवाद और नायक की नैतिक स्वतंत्र इच्छा का खंडन",
        "student_steps": (
            "Step 1: Analyzed Act 1 where the Three Witches prophesy that Macbeth will become Thane of Cawdor and King.\n"
            "Step 2: Observed Lady Macbeth ridiculing his masculinity and urging him to assassinate King Duncan.\n"
            "Step 3: Concluded that Macbeth was an innocent moral man entirely corrupted against his will by external forces.\n"
            "Step 4: Argued that without the witches and Lady Macbeth, Macbeth bears zero personal guilt or tragic responsibility."
        ),
        "student_steps_hi": (
            "चरण 1: अंक 1 का विश्लेषण किया जहाँ तीन चुड़ैलें भविष्यवाणी करती हैं कि मैकबेथ राजा बनेगा।\n"
            "चरण 2: देखा कि लेडी मैकबेथ ने उसके पौरुष पर सवाल उठाए और राजा डंकन की हत्या के लिए उकसाया।\n"
            "चरण 3: निष्कर्ष निकाला कि मैकबेथ एक निर्दोष व्यक्ति था जिसे बाहरी ताकतों ने उसकी इच्छा के विरुद्ध पूरी तरह भ्रष्ट किया।\n"
            "चरण 4: तर्क दिया कि चुड़ैलों और लेडी मैकबेथ के बिना, मैकबेथ का कोई व्यक्तिगत नैतिक दायित्व या दोष नहीं है।"
        ),
        "student_breakdown": (
            "I argued that Macbeth was forced into murder by supernatural prophecy and marital manipulation. "
            "My literature tutor noted that this destroys the play's status as an Aristotelian tragedy. Why?"
        ),
        "student_breakdown_hi": (
            "मैंने तर्क दिया कि मैकबेथ को भविष्यवाणी और लेडी मैकबेथ के दबाव ने हत्या के लिए विवश किया। "
            "मेरे शिक्षक ने कहा कि यह व्याख्या नाटक की त्रासदी के स्वरूप को नष्ट कर देती है। ऐसा क्यों?"
        ),
        "canonical_concept": "Aristotelian Tragic Flaw (Hamartia): Volitional Agency vs External Catalysts",
        "canonical_root_misconception": "Absolution of Moral Agency (Conflating External Temptation with Compulsion)",
        "derailment_step": 3,
        "derailment_reason": "Absolved Macbeth of moral agency. In dramatic theory, external catalysts (the witches, Lady Macbeth) merely illuminate and tempt the protagonist's latent flaw ('vaulting ambition'). Without volitional choice and complicity, the work becomes a tale of mere victimization rather than a tragedy.",
        "student_nodes": [
            {"id": "S1", "label": "Act 1: Witches prophesy royal ascension", "is_error": False},
            {"id": "S2", "label": "Lady Macbeth challenges his resolve to assassinate Duncan", "is_error": False},
            {"id": "S3", "label": "Concluded external manipulation stripped Macbeth of all moral agency", "is_error": True, "detail": "Derailment: Conflated external temptation with irresistible coercion"},
            {"id": "S4", "label": "Judged Macbeth as an innocent victim rather than a tragic hero", "is_error": True, "detail": "Failed Aristotelian definition of tragic hamartia"}
        ],
        "remediation_nodes": [
            {"id": "R1", "label": "Examine Act 1 Scene 3: Macbeth harbors 'murder fantastical' thoughts before meeting Lady Macbeth", "is_pivot": False},
            {"id": "R2", "label": "💡 PIVOT: Identify Internal Hamartia: 'Vaulting Ambition' (Act 1 Scene 7 soliloquy)", "is_pivot": True, "detail": "Breakthrough: The prophecy is a catalyst, but Macbeth freely chooses regicide"},
            {"id": "R3", "label": "Contrast Banquo: Heard identical prophecies yet maintained moral vigilance and rejected treason", "is_pivot": False},
            {"id": "R4", "label": "Synthesize: Tragedy requires tragic guilt; Macbeth's terror and soliloquies prove conscious complicity", "is_pivot": False}
        ],
        "narration_en": (
            "You captured the psychological intensity of the witches' prophecy and Lady Macbeth's persuasion. "
            "However, look at Node 3 in your literary analysis: you treated external temptation as irresistible force, stripping Macbeth of moral agency. "
            "In classical tragedy, external catalysts merely awaken internal desire. Macbeth himself admits his motive: 'Vaulting ambition'. "
            "Notice how Banquo hears the same witches but chooses moral restraint. Look at the green Pivot Node to see why tragic culpability requires voluntary choice."
        ),
        "narration_hi": (
            "Aapne Witches ke prophecy aur Lady Macbeth ke persuasion ko accurately observe kiya. "
            "Lekin thought map ke Node 3 par notice karein: external pressure ko absolute compulsion maan kar aapne Macbeth ki moral agency deny kar di. "
            "Classical tragedy mein external catalysts sirf internal flaw ko trigger karte hain. Macbeth khud admit karta hai ki uski drive 'vaulting ambition' thi. "
            "Banquo ne bhi same prophecies suni par moral restraint banaye rakha. Green Pivot Node par samjhein ki tragedy tabhi banti hai jab protagonist khud free choice karta hai."
        ),
        "narration_pure_hi": (
            "आपने चुड़ैलों की भविष्यवाणी और लेडी मैकबेथ के प्रभाव का सटीक अवलोकन किया। "
            "किंतु अपने विचार मानचित्र के नोड 3 पर विचार करें: बाहरी प्रलोभन को अनिवार्य दबाव मानकर आपने मैकबेथ की नैतिक स्वतंत्र इच्छा को नकार दिया। "
            "शास्त्रीय त्रासदी में बाहरी उत्प्रेरक केवल आंतरिक दोष को जागृत करते हैं। मैकबेथ स्वयं स्वीकार करता है कि उसकी 'अति-महत्वाकांक्षा' ही उसे प्रेरित करती है। "
            "बैंको ने भी वही भविष्यवाणी सुनी थी, किंतु नैतिकता नहीं छोड़ी। पिवट नोड दर्शाता है कि त्रासदी के लिए नायक का सचेत चयन आवश्यक है।"
        ),
        "socratic_prompt": (
            "In Act 1 Scene 3, Banquo listens to the same witches and hears that his descendants will be kings, yet he prays for restraint against evil thoughts. In his Act 1 Scene 7 soliloquy, Macbeth states he has no spur to prick the sides of his intent except 'Vaulting ambition'. If Macbeth were truly a powerless victim with no ambition, why did he plot murder while Banquo remained honorable?"
        ),
        "socratic_prompt_hi": (
            "अंक 1 दृश्य 3 में, बैंको भी उन्हीं चुड़ैलों से सुनता है कि उसके वंशज राजा बनेंगे, फिर भी वह संयम रखता है। मैकबेथ स्वयं स्वीकार करता है कि उसकी 'अति-महत्वाकांक्षा' ही एकमात्र प्रेरणा है। यदि मैकबेथ वास्तव में असहाय मोहरा था, तो उसने हत्या की योजना क्यों बनाई जबकि बैंको नैतिक रूप से अडिग रहा?"
        )
    }
}

# Alias for backwards compatibility
SAMPLE_DOUBTS["incline_friction_work_energy"] = SAMPLE_DOUBTS["spring_friction_energy"]
SAMPLE_DOUBTS["vertical_circle_centripetal"] = SAMPLE_DOUBTS["circular_motion_turn"]
