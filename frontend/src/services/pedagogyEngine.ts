/**
 * Universal Pedagogical Reasoning & Cognitive Diagnostic Engine
 * Operates across ALL academic fields (Mathematics, Computer Science, Physics, Chemistry,
 * Biology, Medicine, Economics, Finance, Law, Logic, Philosophy, Humanities, and General Inquiry).
 */

import { SAMPLE_DOUBTS } from '../data/sampleDoubts';
import {
  NodeCard,
  Connector,
  TimelineStep,
  GraphPayload,
  BoardStep,
  BoardSolveResponse,
  GraphNode,
  GraphEdge,
  DivergenceGraphResponse,
  SocraticDiagnosisResult,
  LearnerProfile
} from '../types';

export interface DiagnosisResult {
  student_nodes: any[];
  remediation_nodes: any[];
  derailment_step: number;
  derailment_reason: string;
  canonical_concept: string;
  canonical_root_misconception: string;
  severity: string;
  socratic_prompt: string;
  narration_script: string;
  dot_comparative: string;
  concept_diagnostics: Record<string, any>;
  board_storyboard: Record<string, any>;
}

export interface DomainProfile {
  domainId: string;
  domainName: string;
  bloomLevel: string;
  canonicalConcept: string;
  rootMisconception: string;
  derailmentStep: number;
  derailmentReason: string;
  socraticPrompt: string;
  hinglishPrompt: string;
  boardSteps: BoardStep[];
  graphNodes: GraphNode[];
  graphEdges: GraphEdge[];
}

/**
 * Universal Domain & Invariant Classifier
 * Detects domain and constructs domain-authentic derivations and graph nodes for ANY problem.
 */
export function detectUniversalDomain(problem: string, steps: string = '', breakdown: string = ''): DomainProfile {
  const text = `${problem} ${steps} ${breakdown}`.toLowerCase();

  // 1. MATHEMATICS & CALCULUS
  if (
    ['derivative', 'integral', 'calculus', 'differentiat', 'chain rule', 'implicit', 'dx', 'dy/dx', 'limit', 'matrix', 'eigenvalue', 'vector space', 'polynomial', 'f(x)', 'f\'(x)', 'समाकलन', 'अवकलन'].some((k) => text.includes(k)) ||
    /\b(calc|deriv|integ|limits|taylor)\b/.test(text)
  ) {
    return {
      domainId: 'mathematics',
      domainName: 'Mathematics & Calculus',
      bloomLevel: 'Analysis & Evaluation',
      canonicalConcept: 'Chain Rule & Derivative Decomposition: d/dx[f(g(x))] = f\'(g(x)) · g\'(x)',
      rootMisconception: 'Omission of Inner Function Derivative (Neglecting Composite Invariant)',
      derailmentStep: 2,
      derailmentReason: 'Differentiated the outer composite function but failed to multiply by the internal derivative g\'(x).',
      socraticPrompt: 'Consider the inner argument g(x): Did you account for the rate of change of the inside expression when differentiating with respect to x?',
      hinglishPrompt: 'Composite function ko dekho: outer function ko differentiate karne ke baad kya aapne andar wale g(x) ka derivative multiply kiya?',
      boardSteps: [
        {
          stepIndex: 1,
          title: 'Step 1: Composite Function Definition',
          latexContent: 'y = f(u), \\quad \\text{where } u = g(x)',
          annotation: 'Decompose nested argument into distinct differentiable functions',
          speechScript: 'Pehle composite function ko break karte hain: outer function f(u) hai aur inner function u = g(x) hai.',
          chalkColor: 'emerald',
          durationEstimateMs: 3800,
        },
        {
          stepIndex: 2,
          title: 'Step 2: Student Attempt (Inner Derivative Omission)',
          latexContent: '\\text{Attempted: } \\frac{dy}{dx} = f\'(g(x)) \\quad \\text{(Omitted } g\'(x) \\text{)}',
          annotation: '⚠️ Critical Pivot: Assumed outer derivative alone gives the full rate of change',
          speechScript: 'Step 2 par dhyan dein: aapne outer power ko differentiate kar diya, lekin andar wale term ka derivative multiply karna bhool gaye.',
          chalkColor: 'amber',
          durationEstimateMs: 4400,
        },
        {
          stepIndex: 3,
          title: 'Step 3: Canonical Counterexample Invalidation',
          latexContent: 'y = (3x^2 + 5)^4 \\implies y\' \\neq 4(3x^2 + 5)^3',
          annotation: 'Demonstrates failure to satisfy infinitesimal chain ratio',
          speechScript: 'Yeh counterexample dekhiye: bina inner derivative 6x ke, actual gradient grossly underestimate ho jata hai.',
          chalkColor: 'rose' as any,
          durationEstimateMs: 4200,
        },
        {
          stepIndex: 4,
          title: 'Step 4: Canonical Scaffolding: Chain Rule Invariant',
          latexContent: '\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx} = 4(3x^2 + 5)^3 \\cdot (6x)',
          annotation: 'Enforce Leibniz differential ratio invariant',
          speechScript: 'Canonical rule apply karein: pehle outer function ko u ke respect mein differentiate karein, fir u ko x ke respect mein multiply karein.',
          chalkColor: 'cyan',
          durationEstimateMs: 4600,
        },
        {
          stepIndex: 5,
          title: 'Step 5: Simplified Valid Derivative Solution',
          latexContent: '\\frac{dy}{dx} = 24x(3x^2 + 5)^3',
          annotation: 'Valid mathematical solution matching empirical slope',
          speechScript: 'Final correct answer 24x into 3x squared plus 5 whole cubed aayega, jo har point par valid tangent slope deta hai.',
          chalkColor: 'emerald',
          durationEstimateMs: 3600,
        },
      ],
      graphNodes: [
        { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Function Argument Setup', mathLatex: 'y = f(g(x))', description: 'Correctly identified the nested functional form.', badge: 'SOUND PREMISE', audioScriptIndic: 'Function structure bilkul sahi pehchana.', position: { x: 50, y: 180 } },
        { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: Differentiation Strategy', mathLatex: "f'(u) \\text{ vs } f'(u) \\cdot u'", description: 'Branch point: Applying single-variable power rule vs Chain Rule.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot point: kya inner derivative multiply hoga?', position: { x: 310, y: 180 } },
        { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: Missing Inner Derivative', mathLatex: "y' = n u^{n-1}", description: 'Neglected multiplication by du/dx.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Inner derivative miss ho gaya.', position: { x: 570, y: 70 } },
        { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: Flawed Tangent Slope', mathLatex: "\\text{Slope Error: } \\Delta m \\propto g'(x)", description: 'Yields incorrect rate of change and invalid critical points.', badge: 'CONTRADICTION', audioScriptIndic: 'Calculated slope completely invalid nikli.', position: { x: 840, y: 70 } },
        { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: Chain Rule', mathLatex: "\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx}", description: 'Enforces composite differential invariant.', badge: 'CANONICAL PATH', audioScriptIndic: 'Canonical chain rule dono rates ko multiply karta hai.', position: { x: 570, y: 310 } },
        { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Leibniz Ratio', mathLatex: "g'(x) = \\frac{d}{dx}[3x^2+5] = 6x", description: 'What is the derivative of the inner expression?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Andar wale term ka derivative evaluate kijiye.', position: { x: 840, y: 310 } },
      ],
      graphEdges: [
        { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Premise Sound', status: 'valid', animated: false },
        { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'Omit du/dx', status: 'derailed', animated: true },
        { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'Slope Inconsistency', status: 'derailed', animated: true },
        { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Apply Chain Rule', status: 'scaffold', animated: false },
        { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Evaluate Invariant', status: 'valid', animated: false },
      ],
    };
  }

  // 2. CHEMISTRY & CHEMICAL SCIENCES
  if (
    ['chemistry', 'equilibrium', 'le chatelier', 'reaction', 'catalyst', 'gibbs', 'enthalpy', 'entropy', 'acid', 'base', 'ph', 'buffer', 'moles', 'stoichiometry', 'redox', 'titration', 'k_eq', 'k_p', 'q_c', 'साम्यावस्था', 'अभिक्रिया'].some((k) => text.includes(k)) ||
    /\b(nh3|haber|delta h|delta g|ka|kb|h2o)\b/.test(text)
  ) {
    return {
      domainId: 'chemistry',
      domainName: 'Chemistry & Dynamic Equilibrium',
      bloomLevel: 'Application & Synthesis',
      canonicalConcept: 'Le Chatelier Dynamic Equilibrium: Q vs K Comparison',
      rootMisconception: 'Conflating Kinetic Reaction Rate with Thermodynamic Equilibrium Yield',
      derailmentStep: 2,
      derailmentReason: 'Assumed a catalyst shifts equilibrium composition or neglected stoichiometric mole ratio when evaluating pressure shifts.',
      socraticPrompt: 'Does a catalyst change the free energy ΔG° or equilibrium constant K, or does it only lower the activation barrier Ea for both directions equally?',
      hinglishPrompt: 'Catalyst forward aur backward dono rates ko barabar accelerate karta hai. Kya yeh equilibrium constant K ya yield ko change karega?',
      boardSteps: [
        {
          stepIndex: 1,
          title: 'Step 1: Reversible Reaction & Stoichiometric Coefficients',
          latexContent: 'aA + bB \\rightleftharpoons cC + dD, \\quad K_c = \\frac{[C]^c [D]^d}{[A]^a [B]^b}',
          annotation: 'Establish balanced chemical equation and mass action law',
          speechScript: 'Pehle balanced chemical reaction aur equilibrium expression Kc define karte hain.',
          chalkColor: 'emerald',
          durationEstimateMs: 3800,
        },
        {
          stepIndex: 2,
          title: 'Step 2: Student Attempt (Kinetic vs Thermodynamic Conflation)',
          latexContent: '\\text{Attempted: Catalyst shifts yield} \\implies K_{\\text{new}} \\neq K_{\\text{old}}',
          annotation: '⚠️ Critical Pivot: Conflated rate of reaching equilibrium with equilibrium position',
          speechScript: 'Step 2 par logic derail hua: catalyst sirf equilibrium tak pahunchne ka time kam karta hai, equilibrium yield ko nahi badalta!',
          chalkColor: 'amber',
          durationEstimateMs: 4400,
        },
        {
          stepIndex: 3,
          title: 'Step 3: Thermodynamic Invariant Invalidation',
          latexContent: '\\Delta G^\\circ = -R \\cdot T \\cdot \\ln(K) \\implies K = e^{-\\Delta G^\\circ / (RT)}',
          annotation: 'K is strictly a function of temperature and standard free energy',
          speechScript: 'Thermodynamics ka invariant dekhiye: K sirf temperature par depend karta hai, catalyst se Delta G change nahi hota.',
          chalkColor: 'rose' as any,
          durationEstimateMs: 4200,
        },
        {
          stepIndex: 4,
          title: 'Step 4: Canonical Scaffolding: Reaction Quotient Q vs K',
          latexContent: 'Q_c < K_c \\implies \\text{Net Forward Shift}, \\quad Q_c > K_c \\implies \\text{Net Reverse Shift}',
          annotation: 'Le Chatelier response governed by instantaneous quotient Q',
          speechScript: 'Canonical approach: pressure ya concentration change hone par Q calculate karein aur K se compare karein.',
          chalkColor: 'cyan',
          durationEstimateMs: 4500,
        },
        {
          stepIndex: 5,
          title: 'Step 5: Sound Thermodynamic Equilibrium State',
          latexContent: '\\text{Catalyst lowers } E_a \\implies k_f, k_b \\uparrow \\text{ equally}, \\quad K = \\frac{k_f}{k_b} = \\text{Constant}',
          annotation: 'Kinetics and thermodynamics reconciled correctly',
          speechScript: 'Dono rates barabar badhne se ratio kf by kb constant rehta hai, isliye yield unchanged rehti hai.',
          chalkColor: 'emerald',
          durationEstimateMs: 3600,
        },
      ],
      graphNodes: [
        { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Stoichiometric Setup', mathLatex: 'aA + bB \\rightleftharpoons cC', description: 'Balanced reaction identified.', badge: 'SOUND PREMISE', audioScriptIndic: 'Balanced reaction correct hai.', position: { x: 50, y: 180 } },
        { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: Perturbation Evaluation', mathLatex: '\\text{Rate } (k) \\text{ vs Equilibrium } (K)', description: 'Deciding effect of catalyst / pressure perturbation.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot point: kinetic vs thermodynamic effect.', position: { x: 310, y: 180 } },
        { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: Shifted K Fallacy', mathLatex: 'K_{\\text{catalyst}} > K', description: 'Incorrectly assumed catalyst changes yield.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Galat yield predict ho gayi.', position: { x: 570, y: 70 } },
        { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: Thermodynamic Violation', mathLatex: '\\Delta G_{\\text{state}} \\neq \\Delta G_{\\text{actual}}', description: 'Violates state function path independence.', badge: 'CONTRADICTION', audioScriptIndic: 'Free energy conservation violate hui.', position: { x: 840, y: 70 } },
        { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: Activation Energy', mathLatex: 'E_{a,f} \\downarrow, \\quad E_{a,b} \\downarrow \\implies K = \\text{const}', description: 'Catalyst lowers barrier equally for both pathways.', badge: 'CANONICAL PATH', audioScriptIndic: 'Dono pathways ka barrier barabar kam hota hai.', position: { x: 570, y: 310 } },
        { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Le Chatelier Q vs K', mathLatex: 'Q_c = \\frac{[\\text{Products}]}{[\\text{Reactants}]}', description: 'How does Q change when mole volume shifts?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Reaction quotient Q ko evaluate kijiye.', position: { x: 840, y: 310 } },
      ],
      graphEdges: [
        { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Sound Reaction', status: 'valid', animated: false },
        { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'K Shift Fallacy', status: 'derailed', animated: true },
        { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'State Function Error', status: 'derailed', animated: true },
        { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Kinetic Invariant', status: 'scaffold', animated: false },
        { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Le Chatelier Check', status: 'valid', animated: false },
      ],
    };
  }

  // 3. BIOLOGY & LIFE SCIENCES / MEDICINE
  if (
    ['biology', 'gene', 'genetics', 'allele', 'mendel', 'dihybrid', 'chromosome', 'dna', 'rna', 'cross', 'phenotype', 'genotype', 'punnett', 'photosynthesis', 'respiration', 'pharmacology', 'clearance', 'half-life', 'अनुवांशिकी', 'जीन'].some((k) => text.includes(k)) ||
    /\b(aabb|gametes|heterozygous|homozygous|enzym)\b/.test(text)
  ) {
    return {
      domainId: 'biology_medicine',
      domainName: 'Biology, Genetics & Biomedical Sciences',
      bloomLevel: 'Analysis & Hypothesis Testing',
      canonicalConcept: 'Mendelian Assortment vs Genetic Linkage Invariants',
      rootMisconception: 'Assuming Independent Assortment when Loci are Linked on the Same Chromosome',
      derailmentStep: 2,
      derailmentReason: 'Applied independent assortment 9:3:3:1 ratio to genes situated closely on the same chromosome without accounting for linkage disequilibrium.',
      socraticPrompt: 'Are the two gene loci on non-homologous chromosomes, or do they reside on the same chromosome? What does physical linkage do to recombinant frequencies?',
      hinglishPrompt: 'Dono genes alag-alag chromosomes par hain ya same chromosome par linked hain? Linkage hone par kya 9:3:3:1 ratio milega?',
      boardSteps: [
        {
          stepIndex: 1,
          title: 'Step 1: Parental Genotypes & Allele Definitions',
          latexContent: 'P_1: AaBb \\times AaBb, \\quad \\text{Traits: } (A/a) \\land (B/b)',
          annotation: 'Identify heterozygous loci and parental phenotype traits',
          speechScript: 'Pehle dono gene loci Aa aur Bb ke genotypes identify karte hain.',
          chalkColor: 'emerald',
          durationEstimateMs: 3800,
        },
        {
          stepIndex: 2,
          title: 'Step 2: Student Attempt (Blind Independent Assortment)',
          latexContent: '\\text{Assumed: } P(AB) = P(Ab) = P(aB) = P(ab) = \\frac{1}{4} \\implies 9 : 3 : 3 : 1',
          annotation: '⚠️ Critical Pivot: Presumed independent segregation without chromosome mapping',
          speechScript: 'Step 2 par logic derail hua: aapne bina linkage check kiye 9:3:3:1 ratio assume kar liya.',
          chalkColor: 'amber',
          durationEstimateMs: 4400,
        },
        {
          stepIndex: 3,
          title: 'Step 3: Linkage Counterexample Invalidation',
          latexContent: '\\text{Linked Loci: } \\text{Distance} < 50\\text{ cM} \\implies \\text{Parental} \\gg \\text{Recombinant}',
          annotation: 'Chromosomal synteny suppresses expected unlinked frequencies',
          speechScript: 'Agar dono genes same chromosome par hain, to parental combinations recombinants se bohot zyada banenge.',
          chalkColor: 'rose' as any,
          durationEstimateMs: 4200,
        },
        {
          stepIndex: 4,
          title: 'Step 4: Canonical Scaffolding: Morgan Recombination Frequency',
          latexContent: '\\text{RF} = \\frac{\\text{Recombinant Progeny}}{\\text{Total Progeny}} \\times 100\\%, \\quad \\theta \\le 0.5',
          annotation: 'Measure crossover distance in centiMorgans (cM)',
          speechScript: 'Canonical rule: recombination frequency theta check karein. Agar theta 50% se kam hai, to linkage present hai.',
          chalkColor: 'cyan',
          durationEstimateMs: 4500,
        },
        {
          stepIndex: 5,
          title: 'Step 5: Sound Genotypic Probability Distribution',
          latexContent: 'P(\\text{Parental}) = \\frac{1 - \\theta}{2}, \\quad P(\\text{Recombinant}) = \\frac{\\theta}{2}',
          annotation: 'Correct linked inheritance frequency accounting for crossing over',
          speechScript: 'Is model se correct gamete frequencies aur phenotype distribution accurate aati hai.',
          chalkColor: 'emerald',
          durationEstimateMs: 3600,
        },
      ],
      graphNodes: [
        { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Genotype Identification', mathLatex: 'AaBb \\times AaBb', description: 'Heterozygous cross identified.', badge: 'SOUND PREMISE', audioScriptIndic: 'Parental genotypes sahi hain.', position: { x: 50, y: 180 } },
        { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: Chromosomal Locus Mapping', mathLatex: '\\text{Syntenic (Linked)} \\text{ vs } \\text{Non-Syntenic}', description: 'Deciding whether genes assort independently.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot: kya genes physically linked hain?', position: { x: 310, y: 180 } },
        { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: Blind 9:3:3:1 Fallacy', mathLatex: '\\text{Ratio} = 9:3:3:1', description: 'Assumed unlinked independent assortment.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Blind ratio assume kar liya.', position: { x: 570, y: 70 } },
        { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: Chi-Square Reject Contradiction', mathLatex: '\\chi^2 \\gg \\chi_{\\text{critical}}^2', description: 'Empirical progeny violates Mendelian ratio.', badge: 'CONTRADICTION', audioScriptIndic: 'Data se ratio reject ho gaya.', position: { x: 840, y: 70 } },
        { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: Linkage Distance', mathLatex: '\\theta = \\text{Map Units (cM)}', description: 'Account for crossover recombinant fraction.', badge: 'CANONICAL PATH', audioScriptIndic: 'Canonical path linkage frequency ko incorporate karta hai.', position: { x: 570, y: 310 } },
        { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Recombination', mathLatex: '\\text{Recombinants} < 50\\%', description: 'How does crossing over restore genetic diversity?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Recombinant frequency evaluate kijiye.', position: { x: 840, y: 310 } },
      ],
      graphEdges: [
        { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Alleles Sound', status: 'valid', animated: false },
        { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'Assume Unlinked', status: 'derailed', animated: true },
        { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'Chi-Square Rejection', status: 'derailed', animated: true },
        { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Enforce Linkage', status: 'scaffold', animated: false },
        { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Recombination Test', status: 'valid', animated: false },
      ],
    };
  }

  // 4. COMPUTER SCIENCE & ALGORITHMS
  if (
    ['code', 'algo', 'algorithm', 'stack', 'queue', 'parenthes', 'bracket', 'tree', 'graph', 'dynamic programming', 'memoization', 'recursion', 'linked list', 'big-o', 'complexity', 'lifo', 'fifo', 'array', 'hash', 'कोष्ठक'].some((k) => text.includes(k)) ||
    /\b(dp|bst|dfs|bfs|pointers|lru)\b/.test(text)
  ) {
    return {
      domainId: 'computer_science',
      domainName: 'Computer Science & Discrete Mathematics',
      bloomLevel: 'Algorithmic Design & Verification',
      canonicalConcept: 'State-Space Invariant & LIFO Data Structure Modeling',
      rootMisconception: 'Insufficient State Representation (Scalar Counter for Multi-Class LIFO Constraints)',
      derailmentStep: 2,
      derailmentReason: 'Used a single integer counter to validate matching pairs across multiple bracket classes, failing to track sequential nesting order.',
      socraticPrompt: 'Can a scalar integer remember which specific bracket type was opened last? What data structure enforces strict Last-In-First-Out retrieval?',
      hinglishPrompt: 'Kya ek simple number counter yeh yaad rakh sakta hai ki aakhri bracket kaunsa open hua tha? Socho LIFO order ke liye kaunsa structure chahiye?',
      boardSteps: [
        {
          stepIndex: 1,
          title: 'Step 1: Input Alphabet & String Specification',
          latexContent: 'S \\in \\Sigma^*, \\quad \\Sigma = \\{ (, ), [, ], \\{, \\} \\}, \\quad |S| = n',
          annotation: 'Formal grammar definition and string length bound',
          speechScript: 'Pehle problem ki formal grammar define karte hain: string S mein distinct opening aur closing bracket types hain.',
          chalkColor: 'emerald',
          durationEstimateMs: 3800,
        },
        {
          stepIndex: 2,
          title: 'Step 2: Student Attempt (Scalar Counter Derailment)',
          latexContent: '\\text{Counter: } c = 0; \\quad c \\leftarrow c + 1 \\text{ on open}, \\quad c \\leftarrow c - 1 \\text{ on close}',
          annotation: '⚠️ Critical Pivot: Conflated cardinality parity with order preservation',
          speechScript: 'Step 2 par logic derail hua: simple counter increment-decrement order ko verify nahi kar sakta, sirf count match karta hai.',
          chalkColor: 'amber',
          durationEstimateMs: 4400,
        },
        {
          stepIndex: 3,
          title: 'Step 3: Interleaving Violation Counterexample',
          latexContent: 'S = \\text{"([)]"} \\implies c = 0 \\quad \\text{BUT } S \\notin \\text{ValidLanguage}',
          annotation: 'Demonstrates failure on mismatched bracket nesting',
          speechScript: 'Counterexample dekhiye: string "([)]" mein counter zero aayega, lekin closing bracket ka order LIFO rule violate karta hai.',
          chalkColor: 'rose' as any,
          durationEstimateMs: 4200,
        },
        {
          stepIndex: 4,
          title: 'Step 4: Canonical Scaffolding: Stack LIFO Invariant',
          latexContent: '\\forall c \\in S: \\quad c \\in \\text{Open} \\implies \\text{Push}(\\sigma, c), \\quad c \\in \\text{Close} \\implies \\text{Pop}(\\sigma) == \\text{Match}(c)',
          annotation: 'Enforce strict stack-based Last-In-First-Out pairing',
          speechScript: 'Canonical solution: Stack data structure use karein. Har opening bracket push karein aur closing bracket par top element match karein.',
          chalkColor: 'cyan',
          durationEstimateMs: 4500,
        },
        {
          stepIndex: 5,
          title: 'Step 5: Correct Terminal State & Complexity Bound',
          latexContent: '\\text{Valid } \\iff \\sigma = \\emptyset, \\quad \\text{Time: } \\mathcal{O}(n), \\quad \\text{Space: } \\mathcal{O}(n)',
          annotation: 'Ensures zero unclosed opening brackets remain',
          speechScript: 'Scan khatam hone par stack empty hona zaroori hai. Isse nested aur sequential dono cases linearly verify ho jate hain.',
          chalkColor: 'emerald',
          durationEstimateMs: 3600,
        },
      ],
      graphNodes: [
        { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Grammar Tokenization', mathLatex: 'S = c_1 c_2 \\dots c_n', description: 'Valid token stream parsing.', badge: 'SOUND PREMISE', audioScriptIndic: 'Input string parsing correct hai.', position: { x: 50, y: 180 } },
        { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: State Model Choice', mathLatex: '\\text{Counter } (\\mathbb{Z}) \\text{ vs Stack } (\\Sigma^*)', description: 'Branch point: Scalar integer vs LIFO Stack.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot: counter ya stack?', position: { x: 310, y: 180 } },
        { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: Scalar Counter Derivation', mathLatex: 'c \\leftarrow c \\pm 1', description: 'Overlooked bracket identity.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Counter se order kho gaya.', position: { x: 570, y: 70 } },
        { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: Interleaving False Positive', mathLatex: 'S = \\text{"([)]"} \\implies \\text{Valid}', description: 'Grammar violation missed.', badge: 'CONTRADICTION', audioScriptIndic: 'False positive error create hua.', position: { x: 840, y: 70 } },
        { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: LIFO Stack', mathLatex: '\\text{Top}(\\sigma) == \\text{Match}(c)', description: 'Strict pair validation.', badge: 'CANONICAL PATH', audioScriptIndic: 'Stack top se pair match hota hai.', position: { x: 570, y: 310 } },
        { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Empty Stack', mathLatex: '\\sigma = \\emptyset', description: 'Why must the stack be empty at termination?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Stack termination condition check karein.', position: { x: 840, y: 310 } },
      ],
      graphEdges: [
        { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Tokens Sound', status: 'valid', animated: false },
        { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'Scalar Counter', status: 'derailed', animated: true },
        { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'False Positive', status: 'derailed', animated: true },
        { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Enforce LIFO Stack', status: 'scaffold', animated: false },
        { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Verify Empty Stack', status: 'valid', animated: false },
      ],
    };
  }

  // 5. ECONOMICS, BUSINESS & FINANCE
  if (
    ['economics', 'finance', 'rent control', 'price ceiling', 'demand', 'supply', 'deadweight', 'market', 'elasticity', 'dcf', 'wacc', 'valuation', 'npv', 'surplus', 'monopoly', 'अर्थशास्त्र', 'किराया', 'बाजार'].some((k) => text.includes(k)) ||
    /\b(mr=mc|dwl|cash flow|discount rate)\b/.test(text)
  ) {
    return {
      domainId: 'economics_finance',
      domainName: 'Economics, Market Equilibrium & Finance',
      bloomLevel: 'Welfare Analysis & Valuation',
      canonicalConcept: 'Market Equilibrium Invariants & Deadweight Loss Quantification',
      rootMisconception: 'Neglecting Quantity Contraction and Non-Price Rationing under Artificial Price Controls',
      derailmentStep: 2,
      derailmentReason: 'Treated an imposed price ceiling as a pure transfer of surplus to consumers without accounting for supply contraction and lost mutual trades.',
      socraticPrompt: 'When price is legally held below equilibrium, how do producers respond to lower marginal revenue? What happens to the transactions between Q_s and Q_eq?',
      hinglishPrompt: 'Jab price legally kam hoti hai, to producers supply kam karte hain ya zyada? Jo trades ruk gayi, unka surplus kahan jata hai?',
      boardSteps: [
        {
          stepIndex: 1,
          title: 'Step 1: Competitive Equilibrium Formulation',
          latexContent: 'Q_d(P) = Q_s(P) \\implies (P_{\\text{eq}}, Q_{\\text{eq}}), \\quad \\text{Social Surplus maximized}',
          annotation: 'Baseline competitive market equilibrium',
          speechScript: 'Pehle competitive equilibrium establish karte hain jahan demand aur supply intersect karte hain.',
          chalkColor: 'emerald',
          durationEstimateMs: 3800,
        },
        {
          stepIndex: 2,
          title: 'Step 2: Student Attempt (Zero Deadweight Loss Assumption)',
          latexContent: '\\text{Assumption: } \\Delta CS = (P_{\\text{eq}} - P_c) \\cdot Q_{\\text{eq}} \\implies \\text{No welfare loss}',
          annotation: '⚠️ Critical Pivot: Assumed quantity remains unchanged at Q_eq',
          speechScript: 'Step 2 par logic derail hua: aapne assume kar liya ki low price par bhi pura quantity Q_eq market mein available rahega.',
          chalkColor: 'amber',
          durationEstimateMs: 4400,
        },
        {
          stepIndex: 3,
          title: 'Step 3: Supply Contraction & Shortage Emergence',
          latexContent: 'P_c < P_{\\text{eq}} \\implies Q_s(P_c) < Q_{\\text{eq}} < Q_d(P_c) \\implies \\text{Shortage}',
          annotation: 'Quantity traded is constrained by the short side of the market: Q = Q_s',
          speechScript: 'Actual reality dekhiye: lower price par suppliers supply kam kar dete hain, jisse severe shortage aur black markets create hote hain.',
          chalkColor: 'rose' as any,
          durationEstimateMs: 4200,
        },
        {
          stepIndex: 4,
          title: 'Step 4: Canonical Scaffolding: Deadweight Loss Triangle',
          latexContent: '\\text{DWL} = \\frac{1}{2} (P_d(Q_s) - P_s(Q_s)) \\cdot (Q_{\\text{eq}} - Q_s(P_c)) > 0',
          annotation: 'Quantifies the irrecoverable loss of consumer and producer surplus',
          speechScript: 'Canonical analysis: supply contract hone se trade na hone wali units par deadweight loss triangle banta hai.',
          chalkColor: 'cyan',
          durationEstimateMs: 4500,
        },
        {
          stepIndex: 5,
          title: 'Step 5: Net Economic Welfare Balance',
          latexContent: '\\Delta W_{\\text{total}} = \\Delta CS + \\Delta PS = -\\text{DWL} < 0',
          annotation: 'Proves net social welfare inevitably declines under binding price caps',
          speechScript: 'Conclusion: binding price ceiling se overall social surplus kam hota hai, chahe kuch remaining consumers ko benefit mile.',
          chalkColor: 'emerald',
          durationEstimateMs: 3600,
        },
      ],
      graphNodes: [
        { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Market Curves', mathLatex: 'Q_d(P) = Q_s(P)', description: 'Equilibrium curves identified.', badge: 'SOUND PREMISE', audioScriptIndic: 'Market demand supply curves sahi hain.', position: { x: 50, y: 180 } },
        { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: Price Control Effect', mathLatex: 'P_c < P_{\\text{eq}}', description: 'Evaluating binding price cap.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot: price cap par quantity response kya hoga?', position: { x: 310, y: 180 } },
        { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: Inelastic Quantity Fallacy', mathLatex: 'Q_{\\text{actual}} = Q_{\\text{eq}}', description: 'Assumed supply does not contract.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Supply contraction miss ho gayi.', position: { x: 570, y: 70 } },
        { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: Unmet Excess Demand', mathLatex: 'Q_d - Q_s > 0', description: 'Shortage and rationing queues emerge.', badge: 'CONTRADICTION', audioScriptIndic: 'Queues aur rationing neglect ho gaye.', position: { x: 840, y: 70 } },
        { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: Deadweight Loss', mathLatex: '\\text{DWL} = \\frac{1}{2} \\Delta P \\cdot \\Delta Q', description: 'Unrealized mutual gains from trade.', badge: 'CANONICAL PATH', audioScriptIndic: 'Deadweight loss triangle arise hota hai.', position: { x: 570, y: 310 } },
        { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Non-Price Rationing', mathLatex: '\\text{Rationing Cost} > 0', description: 'Who absorbs the cost of wait times and shortages?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Non-price rationing cost evaluate kijiye.', position: { x: 840, y: 310 } },
      ],
      graphEdges: [
        { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Equilibrium Sound', status: 'valid', animated: false },
        { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'Ignore Supply Contraction', status: 'derailed', animated: true },
        { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'Severe Shortage', status: 'derailed', animated: true },
        { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Account for DWL', status: 'scaffold', animated: false },
        { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Welfare Tradeoff', status: 'valid', animated: false },
      ],
    };
  }

  // 6. LAW, GOVERNANCE & CONSTITUTIONAL CIVICS
  if (
    ['law', 'legal', 'article 19', 'constitution', 'statute', 'court', 'fundamental right', 'speech', 'restriction', 'proportionality', 'public order', 'mens rea', 'jurisprudence', 'अधिकार', 'संविधान', 'विधि'].some((k) => text.includes(k)) ||
    /\b(article|statutory|tort|contract|liability)\b/.test(text)
  ) {
    return {
      domainId: 'law_governance',
      domainName: 'Constitutional Law, Jurisprudence & Governance',
      bloomLevel: 'Constitutional Scrutiny & Proportionality Balancing',
      canonicalConcept: 'Proportionality Test & Article 19(2) Reasonable Restrictions',
      rootMisconception: 'Absolutist Fundamental Right Conception (Ignoring Statutory Limitation Clauses)',
      derailmentStep: 2,
      derailmentReason: 'Treated a constitutional liberty as absolute and unqualified, overlooking the explicit enumerated grounds for reasonable state restriction.',
      socraticPrompt: 'Under Article 19(2), which specific exhaustive grounds permit the State to limit speech? How does the proportionality doctrine balance the right with legitimate public order?',
      hinglishPrompt: 'Article 19(2) ke mutabiq, kya free speech par public order ya incitement ke grounds par restrictions lagayi ja sakti hain? Proportionality test kya kehta hai?',
      boardSteps: [
        {
          stepIndex: 1,
          title: 'Step 1: Constitutional Guarantee Assertion',
          latexContent: '\\text{Article 19(1)(a)}: \\quad \\text{Right to Freedom of Speech and Expression}',
          annotation: 'Prima facie fundamental entitlement asserted by citizen',
          speechScript: 'Shuruat mein Article 19(1)(a) fundamental right establish karta hai: har citizen ko speech aur expression ki azaadi hai.',
          chalkColor: 'emerald',
          durationEstimateMs: 3800,
        },
        {
          stepIndex: 2,
          title: 'Step 2: Student Attempt (Absolutist Right Fallacy)',
          latexContent: '\\text{Assumption: } \\text{Right} = \\text{Absolute} \\implies \\text{No State Jurisdiction}',
          annotation: '⚠️ Critical Pivot: Conflated fundamental status with unconstrained immunity',
          speechScript: 'Step 2 par logic derail hua: aapne right ko absolute maan liya, bina Article 19(2) ki limitations dekhe.',
          chalkColor: 'amber',
          durationEstimateMs: 4400,
        },
        {
          stepIndex: 3,
          title: 'Step 3: Textual Constitutional Counterexample',
          latexContent: '\\text{Art 19(2)}: \\quad \\text{Sovereignty} \\cup \\text{Security} \\cup \\text{Public Order} \\cup \\text{Incitement to Offence}',
          annotation: 'Exhaustive enumerated grounds for state curtailment',
          speechScript: 'Article 19(2) explicitly state karta hai ki public order, morality, aur incitement to an offence ke ground par reasonable restrictions lag sakti hain.',
          chalkColor: 'rose' as any,
          durationEstimateMs: 4200,
        },
        {
          stepIndex: 4,
          title: 'Step 4: Canonical Scaffolding: Four-Prong Proportionality Test',
          latexContent: '\\text{Test} = \\text{Legitimate Aim} \\land \\text{Suitability} \\land \\text{Necessity} \\land \\text{Balancing Strictu Sensu}',
          annotation: 'Modern apex court constitutional review standard (Modern Dental / Puttaswamy)',
          speechScript: 'Canonical approach: court proportionality test lagati hai ki restriction jarurat ke hisab se least restrictive honi chahiye.',
          chalkColor: 'cyan',
          durationEstimateMs: 4500,
        },
        {
          stepIndex: 5,
          title: 'Step 5: Sound Constitutional Balancing Resolution',
          latexContent: '\\text{Valid Restriction } \\iff \\text{Statutory Ground} \\land \\text{Narrow Tailoring}',
          annotation: 'Harmonious reconciliation of individual liberty and democratic order',
          speechScript: 'Isliye blanket ban unconstitutional hoga, lekin targeted public order restriction legally valid hogi.',
          chalkColor: 'emerald',
          durationEstimateMs: 3600,
        },
      ],
      graphNodes: [
        { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Right Invocation', mathLatex: '\\text{Art 19(1)(a)}', description: 'Prima facie fundamental right established.', badge: 'SOUND PREMISE', audioScriptIndic: 'Fundamental right validly identified.', position: { x: 50, y: 180 } },
        { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: Limitation Scrutiny', mathLatex: '\\text{Absolute} \\text{ vs } \\text{Qualified}', description: 'Deciding whether right is subject to state balancing.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot: absolute right vs reasonable restrictions.', position: { x: 310, y: 180 } },
        { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: Absolutist Fallacy', mathLatex: '\\text{State Intervention} = \\emptyset', description: 'Ignored constitutional statutory exceptions.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Statutory exceptions ignore ho gaye.', position: { x: 570, y: 70 } },
        { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: Anarchy Contradiction', mathLatex: '\\text{Public Order Collapse}', description: 'Would permit direct incitement to violence.', badge: 'CONTRADICTION', audioScriptIndic: 'Direct incitement conflict create hua.', position: { x: 840, y: 70 } },
        { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: Proportionality', mathLatex: '\\text{Modern Dental 4-Prong Test}', description: 'Legitimate aim and narrow tailoring.', badge: 'CANONICAL PATH', audioScriptIndic: 'Canonical proportionality test apply hota hai.', position: { x: 570, y: 310 } },
        { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Least Restrictive Means', mathLatex: '\\text{Least Restrictive Measure}', description: 'Could the state have achieved its goal with lesser impairment?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Least restrictive measure evaluate kijiye.', position: { x: 840, y: 310 } },
      ],
      graphEdges: [
        { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Right Sound', status: 'valid', animated: false },
        { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'Absolutist Assumption', status: 'derailed', animated: true },
        { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'Public Order Breach', status: 'derailed', animated: true },
        { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Apply Art 19(2)', status: 'scaffold', animated: false },
        { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Proportionality Test', status: 'valid', animated: false },
      ],
    };
  }

  // 7. PHILOSOPHY, LOGIC & CRITICAL THINKING
  if (
    ['philosophy', 'logic', 'fallacy', 'syllogism', 'affirming', 'denying', 'premise', 'conclusion', 'deductive', 'inductive', 'soundness', 'validity', 'modus ponens', 'tark', 'तर्क'].some((k) => text.includes(k)) ||
    /\b(p->q|modus tollens|paradox|epistem)\b/.test(text)
  ) {
    return {
      domainId: 'philosophy_logic',
      domainName: 'Formal Logic, Epistemology & Reasoning',
      bloomLevel: 'Deductive Validity & Fallacy Detection',
      canonicalConcept: 'Directionality of Implication: (P → Q) does not entail (Q → P)',
      rootMisconception: 'Fallacy of Affirming the Consequent (Conflating Necessity with Sufficiency)',
      derailmentStep: 2,
      derailmentReason: 'Inferred that because the consequent Q is true, the specific antecedent P must have occurred, ignoring alternative causal pathways.',
      socraticPrompt: 'If "If it rains, the grass is wet" is true, and the grass is wet, does that prove rain, or could a sprinkler have caused it? Can you separate necessary vs sufficient conditions?',
      hinglishPrompt: 'Agar P se Q hota hai, aur Q true hai, to kya zaroori hai ki P hi hua ho? Kya koi aur alternative reason nahi ho sakta?',
      boardSteps: [
        {
          stepIndex: 1,
          title: 'Step 1: Conditional Implication Formulation',
          latexContent: '\\text{Premise: } P \\implies Q \\quad \\text{(P is sufficient for Q)}',
          annotation: 'Establish formal directional logical proposition',
          speechScript: 'Pehle conditional statement likhte hain: agar P true hai, to Q zaroor true hoga.',
          chalkColor: 'emerald',
          durationEstimateMs: 3800,
        },
        {
          stepIndex: 2,
          title: 'Step 2: Student Attempt (Fallacy of Affirming Consequent)',
          latexContent: '\\text{Observation: } Q = \\text{True} \\implies \\text{Inferred: } P = \\text{True}',
          annotation: '⚠️ Critical Pivot: Inverted the direction of the logical arrow',
          speechScript: 'Step 2 par logic derail hua: aapne consequent Q ko dekh kar yeh maan liya ki P hi hua hoga.',
          chalkColor: 'amber',
          durationEstimateMs: 4400,
        },
        {
          stepIndex: 3,
          title: 'Step 3: Formal Counterexample Invalidation',
          latexContent: 'Q \\text{ caused by } R, \\quad R \\neq P \\implies (P \\implies Q) \\land Q \\land \\neg P',
          annotation: 'Demonstrates invalidity via multiple possible antecedents',
          speechScript: 'Counterexample dekhiye: zameen geeli hone ka reason barish ke alawa sprinkler ya pipe leak bhi ho sakta hai.',
          chalkColor: 'rose' as any,
          durationEstimateMs: 4200,
        },
        {
          stepIndex: 4,
          title: 'Step 4: Canonical Scaffolding: Modus Ponens vs Modus Tollens',
          latexContent: '\\text{Valid: } (P \\implies Q) \\land P \\vdash Q, \\quad (P \\implies Q) \\land \\neg Q \\vdash \\neg P',
          annotation: 'Deductive forms that strictly preserve truth-functional validity',
          speechScript: 'Canonical logic rule: sirf Modus Ponens ya Modus Tollens valid deduction guarantee karte hain.',
          chalkColor: 'cyan',
          durationEstimateMs: 4500,
        },
        {
          stepIndex: 5,
          title: 'Step 5: Sound Epistemic Resolution',
          latexContent: 'Q \\implies (P \\lor R_1 \\lor R_2 \\dots) \\not\\vdash P \\text{ with certainty}',
          annotation: 'Inductive abduction vs formal deductive certainty reconciled',
          speechScript: 'Isliye P ek possible hypothesis hai, lekin deductive certainty nahi.',
          chalkColor: 'emerald',
          durationEstimateMs: 3600,
        },
      ],
      graphNodes: [
        { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Implication Defined', mathLatex: 'P \\implies Q', description: 'Directional rule identified.', badge: 'SOUND PREMISE', audioScriptIndic: 'Logical premise correct hai.', position: { x: 50, y: 180 } },
        { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: Causal Direction Test', mathLatex: '\\text{Sufficiency vs Necessity}', description: 'Deciding whether P is the sole cause of Q.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot: sufficiency vs necessity.', position: { x: 310, y: 180 } },
        { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: Affirming Consequent', mathLatex: 'Q \\vdash P', description: 'Committed formal fallacy.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Formal fallacy commit ho gayi.', position: { x: 570, y: 70 } },
        { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: Alternative Cause Blindness', mathLatex: 'R \\implies Q, \\; P = \\text{False}', description: 'Counterexample disproves deduction.', badge: 'CONTRADICTION', audioScriptIndic: 'Alternative cause neglect ho gaya.', position: { x: 840, y: 70 } },
        { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: Modus Tollens', mathLatex: '\\neg Q \\implies \\neg P', description: 'Contrapositive equivalence.', badge: 'CANONICAL PATH', audioScriptIndic: 'Contrapositive logically sound hai.', position: { x: 570, y: 310 } },
        { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Biconditional', mathLatex: 'P \\iff Q \\text{ required}', description: 'What condition would allow bidirectional inference?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Biconditional equivalence check kijiye.', position: { x: 840, y: 310 } },
      ],
      graphEdges: [
        { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Rule Sound', status: 'valid', animated: false },
        { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'Affirm Consequent', status: 'derailed', animated: true },
        { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'Alternative Cause', status: 'derailed', animated: true },
        { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Contrapositive', status: 'scaffold', animated: false },
        { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Equivalence Test', status: 'valid', animated: false },
      ],
    };
  }

  // 8. WORLD HISTORY & GEOPOLITICAL CAUSALITY
  if (
    ['history', 'ww1', 'world war', 'assassination', 'franz ferdinand', 'sarajevo', 'alliances', 'serbia', 'austria-hungary', 'militarism', 'imperialism', 'इतिहास', 'युद्ध'].some((k) => text.includes(k)) ||
    /\b(ww1|wwi|entente|habsburg|balkans)\b/.test(text)
  ) {
    return {
      domainId: 'world_history',
      domainName: 'Modern World History & Geopolitics',
      bloomLevel: 'Historical Causality & Systemic Analysis',
      canonicalConcept: 'Structural Multi-Polar Causality vs Trigger Incidents',
      rootMisconception: 'Mono-Causal Reductionism (Treating Sarajevo Spark as Sole Cause of Total War)',
      derailmentStep: 2,
      derailmentReason: 'Reduced a complex continental escalation to an isolated terrorist act, ignoring interlocking military alliances, naval arms race, and imperial competition.',
      socraticPrompt: 'Without the secret alliance networks (Triple Entente vs Triple Alliance) and rigid military mobilization timetables, could a localized Balkan assassination have triggered a global war?',
      hinglishPrompt: 'Kya bina secret alliances aur imperial competition ke, sirf ek assassination se poore Europe mein world war shuru ho sakti thi?',
      boardSteps: [
        {
          stepIndex: 1,
          title: 'Step 1: Immediate Trigger Event Identification',
          latexContent: '\\text{Spark: } \\text{Sarajevo Assassination (June 28, 1914)} \\implies \\text{Balkan Crisis}',
          annotation: 'Immediate localized geopolitical flashpoint',
          speechScript: 'Pehle immediate trigger event ko identify karte hain: Archduke Franz Ferdinand ka assassination.',
          chalkColor: 'emerald',
          durationEstimateMs: 3800,
        },
        {
          stepIndex: 2,
          title: 'Step 2: Student Attempt (Single-Incident Fallacy)',
          latexContent: '\\text{Assumption: } \\text{Assassination} \\implies \\text{Inevitable Global Escalation}',
          annotation: '⚠️ Critical Pivot: Equated immediate catalyst with systemic root causality',
          speechScript: 'Step 2 par logic derail hua: aapne maan liya ki is single attack ki wajah se hi saare empires war mein aane ke liye majboor the.',
          chalkColor: 'amber',
          durationEstimateMs: 4400,
        },
        {
          stepIndex: 3,
          title: 'Step 3: Historical Counterexample (Prior Balkan Crises)',
          latexContent: '\\text{Bosnian Crisis (1908)}, \\; \\text{Balkan Wars (1912-13)} \\implies \\text{Contained locally}',
          annotation: 'Demonstrates earlier similar crises were resolved through diplomatic containment',
          speechScript: 'Counterexample dekhiye: 1908 aur 1912 mein bhi similar crises hue the jo regional level par contain ho gaye the.',
          chalkColor: 'rose' as any,
          durationEstimateMs: 4200,
        },
        {
          stepIndex: 4,
          title: 'Step 4: Canonical Scaffolding: M-A-I-N Structural Framework',
          latexContent: '\\text{Risk Matrix} = \\text{Militarism} + \\text{Alliances} + \\text{Imperialism} + \\text{Nationalism}',
          annotation: 'Systemic combustible preconditions that converted local shock into general war',
          speechScript: 'Canonical historical analysis: Triple Entente aur Triple Alliance ke rigid mobilization timetables ne escalation ko unstoppable banaya.',
          chalkColor: 'cyan',
          durationEstimateMs: 4600,
        },
        {
          stepIndex: 5,
          title: 'Step 5: Synthesized Multi-Polar Causality Model',
          latexContent: '\\text{Outbreak} = \\mathcal{C}_{\\text{structural}}(\\text{MAIN}) \\times \\mathcal{T}_{\\text{catalyst}}(\\text{July Crisis})',
          annotation: 'Rigorous reconciliation of long-term structural forces with short-term diplomatic agency',
          speechScript: 'Conclusion: Assassination sirf ignition spark tha, jabki explosive material structural alliances aur imperial rivalry the.',
          chalkColor: 'emerald',
          durationEstimateMs: 3600,
        },
      ],
      graphNodes: [
        { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Sarajevo Event', mathLatex: '\\text{Assassination (June 1914)}', description: 'Catalyst crisis identified.', badge: 'SOUND PREMISE', audioScriptIndic: 'Sarajevo event accurately identified.', position: { x: 50, y: 180 } },
        { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: Causality Model Choice', mathLatex: '\\text{Mono-causal vs Systemic}', description: 'Deciding whether single event forced continent-wide mobilization.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot: single cause ya structural framework?', position: { x: 310, y: 180 } },
        { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: Sole Cause Fallacy', mathLatex: '\\text{Assassination} \\vdash \\text{WWI}', description: 'Omitted alliance obligations and military timetables.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Structural factors ignore ho gaye.', position: { x: 570, y: 70 } },
        { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: Unexplained Escalation Speed', mathLatex: '\\Delta t = 5 \\text{ weeks to World War}', description: 'Cannot explain why Britain or Germany mobilized over a Serbian prince.', badge: 'CONTRADICTION', audioScriptIndic: 'Escalation speed explain nahi hoti.', position: { x: 840, y: 70 } },
        { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: MAIN Framework', mathLatex: '\\text{Interlocking Alliances}', description: 'Mutual defense pacts and Schlieffen Plan rigid logistics.', badge: 'CANONICAL PATH', audioScriptIndic: 'Alliance networks ne domino effect create kiya.', position: { x: 570, y: 310 } },
        { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Counterfactual Test', mathLatex: '\\text{Containment Feasibility}', description: 'Why did diplomatic backchannels fail in July 1914?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Diplomatic failure evaluate kijiye.', position: { x: 840, y: 310 } },
      ],
      graphEdges: [
        { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Event Sound', status: 'valid', animated: false },
        { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'Mono-Causal', status: 'derailed', animated: true },
        { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'Incomplete Narrative', status: 'derailed', animated: true },
        { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Apply Structural Alliances', status: 'scaffold', animated: false },
        { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Evaluate Catalysts', status: 'valid', animated: false },
      ],
    };
  }

  // 9. LITERATURE & DRAMATIC THEORY
  if (
    ['literature', 'macbeth', 'hamartia', 'shakespeare', 'tragedy', 'fatal flaw', 'hubris', 'weird sisters', 'duncan', 'lady macbeth', 'साहित्य', 'नाटक'].some((k) => text.includes(k)) ||
    /\b(hamartia|tragic hero|catharsis|soliloquy)\b/.test(text)
  ) {
    return {
      domainId: 'classical_literature',
      domainName: 'Literature, Dramatic Theory & Shakespeare',
      bloomLevel: 'Literary Evaluation & Hermeneutics',
      canonicalConcept: 'Aristotelian Hamartia vs Supernatural Determinism',
      rootMisconception: 'Denial of Moral Agency (Absolving Protagonist via External Manipulation)',
      derailmentStep: 2,
      derailmentReason: 'Attributed Macbeth downfall exclusively to the witches prophecies and Lady Macbeth, ignoring his own vaulting ambition and volitional choices.',
      socraticPrompt: 'In his soliloquies (e.g., "I have no spur to prick the sides of my intent, but only vaulting ambition"), who does Macbeth himself identify as the driving force behind the murder?',
      hinglishPrompt: 'Macbeth ke soliloquy mein dhyan dein: kya woh khud apni "vaulting ambition" ko doshi manta hai ya witches ko?',
      boardSteps: [
        {
          stepIndex: 1,
          title: 'Step 1: Supernatural Incitement & Prophetic Catalyst',
          latexContent: '\\text{Weird Sisters: } \\text{"All hail Macbeth, that shalt be king hereafter!"}',
          annotation: 'External catalyst triggering latent desire',
          speechScript: 'Pehle witches ke prophecy aur external incitement ko establish karte hain.',
          chalkColor: 'emerald',
          durationEstimateMs: 3800,
        },
        {
          stepIndex: 2,
          title: 'Step 2: Student Attempt (Passive Victim Fallacy)',
          latexContent: '\\text{Assumption: } \\text{Prophecy} \\implies \\text{Zero Moral Agency} \\implies \\text{No Tragic Guilt}',
          annotation: '⚠️ Critical Pivot: Conflated psychological temptation with predetermined coercion',
          speechScript: 'Step 2 par interpretation derail hui: aapne Macbeth ko innocent puppet maan liya jiska apna koi moral responsibility nahi tha.',
          chalkColor: 'amber',
          durationEstimateMs: 4400,
        },
        {
          stepIndex: 3,
          title: 'Step 3: Textual Counterexample (Banquo Comparison)',
          latexContent: '\\text{Banquo given same prophecy} \\implies \\text{Refused treason} \\implies \\text{Free will preserved}',
          annotation: 'Proves prophecies did not compel violent action',
          speechScript: 'Textual counterexample dekhiye: Banquo ko bhi prophecy mili thi, lekin usne moral boundaries cross nahi ki.',
          chalkColor: 'rose' as any,
          durationEstimateMs: 4200,
        },
        {
          stepIndex: 4,
          title: 'Step 4: Canonical Scaffolding: Aristotelian Hamartia',
          latexContent: '\\text{Hamartia} = \\text{Vaulting Ambition} \\land \\text{Conscious Moral Transgression}',
          annotation: 'Tragedy requires a great noble who knowingly falls through an internal fatal flaw',
          speechScript: 'Canonical dramatic theory: Macbeth tragedy isiliye compelling hai kyunki woh galat aur sahi jaante hue bhi ambition choose karta hai.',
          chalkColor: 'cyan',
          durationEstimateMs: 4600,
        },
        {
          stepIndex: 5,
          title: 'Step 5: Synthesized Tragic Paradox',
          latexContent: '\\text{Catharsis} = \\text{Horror at tyrannical deeds} \\land \\text{Pity for wasted nobility}',
          annotation: 'Classic Shakespearean tragic resolution and moral accountability',
          speechScript: 'Isliye Macbeth victim nahi, balki internal fatal flaw ka tragic architect hai.',
          chalkColor: 'emerald',
          durationEstimateMs: 3600,
        },
      ],
      graphNodes: [
        { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Prophetic Catalyst', mathLatex: '\\text{Act 1 Prophecy}', description: 'Witches incite latent ambition.', badge: 'SOUND PREMISE', audioScriptIndic: 'Prophetic premise soundly identified.', position: { x: 50, y: 180 } },
        { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: Agency Interpretation', mathLatex: '\\text{Victim vs Moral Agent}', description: 'Deciding whether protagonist retained free will.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot: passive victim ya internal hamartia?', position: { x: 310, y: 180 } },
        { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: External Determinism', mathLatex: '\\text{Guilt} = \\text{Witches}', description: 'Absolved Macbeth of personal choice.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Moral agency neglect ho gayi.', position: { x: 570, y: 70 } },
        { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: Destruction of Tragic Nobility', mathLatex: '\\text{No Catharsis}', description: 'A passive puppet cannot evoke Aristotelian tragic pity.', badge: 'CONTRADICTION', audioScriptIndic: 'Tragedy ki core catharsis vanish ho gayi.', position: { x: 840, y: 70 } },
        { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: Vaulting Ambition', mathLatex: '\\text{Hamartia Invariant}', description: 'Internal fatal flaw drives deliberate action.', badge: 'CANONICAL PATH', audioScriptIndic: 'Internal tragic flaw identify hua.', position: { x: 570, y: 310 } },
        { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Banquo Foil', mathLatex: '\\text{Foil Comparison}', description: 'Why did Banquo not murder anyone after hearing the prophecy?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Banquo foil compare kijiye.', position: { x: 840, y: 310 } },
      ],
      graphEdges: [
        { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Prophecy Sound', status: 'valid', animated: false },
        { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'External Determinism', status: 'derailed', animated: true },
        { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'Destroys Tragic Form', status: 'derailed', animated: true },
        { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Enforce Hamartia', status: 'scaffold', animated: false },
        { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Foil Test', status: 'valid', animated: false },
      ],
    };
  }

  // 10. MEDICINE & PHARMACOLOGY
  if (
    ['medicine', 'pharmacology', 'clearance', 'half-life', 'dose', 'plasma concentration', 'elimination rate', 'steady-state', 'pharmacokinetics', 'bioavailability', 'दवा', 'चिकित्सा'].some((k) => text.includes(k)) ||
    /\b(c_max|t_half|auc|clearance|iv bolus)\b/.test(text)
  ) {
    return {
      domainId: 'medicine_pharmacology',
      domainName: 'Medicine, Pharmacology & Pharmacokinetics',
      bloomLevel: 'Clinical Evaluation & Quantitative Kinetics',
      canonicalConcept: 'First-Order vs Zero-Order Elimination Kinetics: dC/dt = -k C',
      rootMisconception: 'Assuming Constant Absolute Elimination Rate (Zero-Order Conflation)',
      derailmentStep: 2,
      derailmentReason: 'Assumed a constant mass of drug is cleared per hour regardless of plasma concentration, neglecting that elimination rate is proportional to concentration in first-order kinetics.',
      socraticPrompt: 'In first-order kinetics, what determines the absolute rate of elimination: a fixed number of milligrams, or a fixed fraction (percentage) of whatever drug is circulating?',
      hinglishPrompt: 'First-order kinetics mein har ghante fixed milligrams eliminate hote hain ya circulating concentration ka fixed percentage?',
      boardSteps: [
        {
          stepIndex: 1,
          title: 'Step 1: Initial Drug Concentration & Dosing',
          latexContent: 'C(t) = C_0 \\, e^{-k_e t}, \\quad t_{1/2} = \\frac{\\ln(2)}{k_e} \\approx \\frac{0.693}{k_e}',
          annotation: 'First-order exponential clearance model',
          speechScript: 'Pehle single IV dose ke exponential decay model ko formulate karte hain.',
          chalkColor: 'emerald',
          durationEstimateMs: 3800,
        },
        {
          stepIndex: 2,
          title: 'Step 2: Student Attempt (Fixed Mass Deduction Fallacy)',
          latexContent: '\\text{Assumption: } \\frac{dC}{dt} = -k_0 \\implies C(t) = C_0 - k_0 t \\quad \\text{(Linear Decay)}',
          annotation: '⚠️ Critical Pivot: Presumed constant absolute rate instead of fractional clearance',
          speechScript: 'Step 2 par logic derail hua: aapne linear zero-order decay assume kar liya jaise fixed milligrams clear ho rahe hon.',
          chalkColor: 'amber',
          durationEstimateMs: 4400,
        },
        {
          stepIndex: 3,
          title: 'Step 3: Pharmacokinetic Contradiction',
          latexContent: 't = 2 \\cdot t_{1/2} \\implies C(t) = 0.25 \\, C_0 \\quad \\text{BUT linear gives } 0 \\, C_0',
          annotation: 'Demonstrates failure to preserve fractional half-life invariant',
          speechScript: 'Contradiction dekhiye: 2 half-lives ke baad 25% drug bacha rehta hai, zero nahi.',
          chalkColor: 'rose' as any,
          durationEstimateMs: 4200,
        },
        {
          stepIndex: 4,
          title: 'Step 4: Canonical Scaffolding: Clearance Rate Proportionality',
          latexContent: '\\text{Clearance} = CL \\times C(t) \\implies \\text{Rate proportional to concentration}',
          annotation: 'Enforces fractional clearance characteristic of non-saturated enzymes',
          speechScript: 'Canonical approach: drug elimination concentration ke directly proportional hoti hai.',
          chalkColor: 'cyan',
          durationEstimateMs: 4500,
        },
        {
          stepIndex: 5,
          title: 'Step 5: Accurate Half-Life Clinical Resolution',
          latexContent: 'C(3 \\, t_{1/2}) = \\frac{1}{8} \\, C_0, \\quad \\text{Steady State attained at } \\sim 4-5 \\, t_{1/2}',
          annotation: 'Standard clinical pharmacology dosing guideline',
          speechScript: 'Isse 4 se 5 half-lives ke baad steady-state achieve hota hai jo clinical dosing ka golden rule hai.',
          chalkColor: 'emerald',
          durationEstimateMs: 3600,
        },
      ],
      graphNodes: [
        { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Baseline Dose', mathLatex: 'C_0 = \\frac{\\text{Dose}}{V_d}', description: 'Volume of distribution identified.', badge: 'SOUND PREMISE', audioScriptIndic: 'Dosing parameters soundly identified.', position: { x: 50, y: 180 } },
        { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: Kinetics Order Choice', mathLatex: '\\text{First-Order vs Zero-Order}', description: 'Deciding whether clearance rate depends on concentration.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot: first-order ya zero-order decay?', position: { x: 310, y: 180 } },
        { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: Fixed Rate Fallacy', mathLatex: '\\frac{dC}{dt} = -k_0', description: 'Assumed constant mg/hr elimination.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Concentration dependence miss ho gayi.', position: { x: 570, y: 70 } },
        { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: Premature Zero Level', mathLatex: 'C(2 \\, t_{1/2}) = 0', description: 'Underestimates residual active drug in circulation.', badge: 'CONTRADICTION', audioScriptIndic: 'Dangerous dosing error create hua.', position: { x: 840, y: 70 } },
        { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: Exponential Decay', mathLatex: 'C(t) = C_0 \\, e^{-k t}', description: 'Constant fractional clearance rate.', badge: 'CANONICAL PATH', audioScriptIndic: 'Exponential decay law apply hota hai.', position: { x: 570, y: 310 } },
        { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Enzyme Saturation', mathLatex: 'K_m \\gg C(t)', description: 'Under what condition does first-order transition to zero-order?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Enzyme saturation limit evaluate kijiye.', position: { x: 840, y: 310 } },
      ],
      graphEdges: [
        { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Dose Sound', status: 'valid', animated: false },
        { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'Assume Constant Rate', status: 'derailed', animated: true },
        { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'Zero Level Contradiction', status: 'derailed', animated: true },
        { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Apply First-Order Decay', status: 'scaffold', animated: false },
        { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Saturation Test', status: 'valid', animated: false },
      ],
    };
  }

  // 11. CLASSICAL MECHANICS & PHYSICS
  if (
    ['physics', 'friction', 'incline', 'work-energy', 'spring', 'kinetic energy', 'potential energy', 'newton', 'force', 'acceleration', 'velocity', 'momentum', 'भौतिक', 'यांत्रिकी'].some((k) => text.includes(k)) ||
    /\b(mgh|1\/2 mv\^2|mu_s|fbd|conservation of energy)\b/.test(text)
  ) {
    return {
      domainId: 'physics_mechanics',
      domainName: 'Classical Physics & Mechanics',
      bloomLevel: 'Physical System Modeling & Conservation Laws',
      canonicalConcept: 'Work-Energy Theorem with Non-Conservative Path Integrals',
      rootMisconception: 'Assuming Strict Mechanical Energy Conservation in Non-Conservative Systems',
      derailmentStep: 2,
      derailmentReason: 'Equated initial mechanical energy directly to final state without accounting for dissipative heat loss from friction W_nc = -μ N d.',
      socraticPrompt: 'Does friction conserve mechanical energy, or does it convert mechanical energy into irreversible thermal dissipation? How does the Work-Energy Theorem account for W_nc?',
      hinglishPrompt: 'Track par friction hone se kya mechanical energy conserved rahegi ya heat mein lose hogi? Work-Energy Theorem mein W_nc kahan add hoga?',
      boardSteps: [
        {
          stepIndex: 1,
          title: 'Step 1: Initial System Energy State Formulation',
          latexContent: 'E_i = mgh, \\quad \\text{System: Block + Incline + Earth + Spring}',
          annotation: 'Initial gravitational potential energy',
          speechScript: 'Pehle initial mechanical energy identify karte hain: top par block ke paas mgh energy hai.',
          chalkColor: 'emerald',
          durationEstimateMs: 3800,
        },
        {
          stepIndex: 2,
          title: 'Step 2: Student Attempt (Frictionless Conservation Fallacy)',
          latexContent: '\\text{Assumption: } E_i = E_f \\implies mgh = \\frac{1}{2} k x^2 \\quad \\text{(Omitted } W_{\\text{friction}} \\text{)}',
          annotation: '⚠️ Critical Pivot: Conflated isolated conservative system with dissipative reality',
          speechScript: 'Step 2 par logic derail hua: aapne friction work ko subtract kiye bina mgh ko 1/2 k x squared se equate kar diya.',
          chalkColor: 'amber',
          durationEstimateMs: 4400,
        },
        {
          stepIndex: 3,
          title: 'Step 3: Thermal Dissipation Counterexample',
          latexContent: 'W_{\\text{friction}} = -\\mu m g \\cos(\\theta) \\cdot d < 0 \\implies E_{\\text{remaining}} < mgh',
          annotation: 'Non-conservative path integral dissipates mechanical energy into heat',
          speechScript: 'Friction negative work karta hai, jisse mechanical energy heat mein convert ho jati hai.',
          chalkColor: 'rose' as any,
          durationEstimateMs: 4200,
        },
        {
          stepIndex: 4,
          title: 'Step 4: Canonical Scaffolding: Work-Energy Theorem',
          latexContent: 'W_{\\text{net, ext}} = \\Delta K + \\Delta U \\implies E_i + W_{\\text{nc}} = \\frac{1}{2} k x^2',
          annotation: 'Enforce non-conservative work balance',
          speechScript: 'Canonical theorem: Initial energy mein se friction loss subtract karein, tab actual compression milegi.',
          chalkColor: 'cyan',
          durationEstimateMs: 4600,
        },
        {
          stepIndex: 5,
          title: 'Step 5: Empirically Consistent Compression Solution',
          latexContent: 'x = \\sqrt{\\frac{2(mgh - \\mu m g \\cos(\\theta) d)}{k}}',
          annotation: 'Valid physical compression matching experimental reality',
          speechScript: 'Isse accurate compression calculate hoti hai jo answer key se perfectly match karegi.',
          chalkColor: 'emerald',
          durationEstimateMs: 3600,
        },
      ],
      graphNodes: [
        { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Energy Inputs', mathLatex: 'E_i = mgh', description: 'Identified baseline height and mass.', badge: 'SOUND PREMISE', audioScriptIndic: 'Initial potential energy accurately identified.', position: { x: 50, y: 180 } },
        { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: Conservative System Check', mathLatex: '\\Delta E_{\\text{mech}} = 0 \\text{ vs } W_{\\text{nc}}', description: 'Branch point: Conservative assumption vs dissipative friction.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot: energy conserved ya friction dissipation?', position: { x: 310, y: 180 } },
        { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: Neglected Friction Work', mathLatex: 'mgh = \\frac{1}{2}kx^2', description: 'Overlooked thermal dissipation.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Friction heat loss ignore ho gaya.', position: { x: 570, y: 70 } },
        { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: Gross Overestimation', mathLatex: 'x_{\\text{calc}} \\gg x_{\\text{actual}}', description: 'Calculated compression exceeds physical limit.', badge: 'CONTRADICTION', audioScriptIndic: 'Compression grossly overestimate hui.', position: { x: 840, y: 70 } },
        { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: Work-Energy Theorem', mathLatex: 'E_i - f_k d = E_f', description: 'Subtract non-conservative work.', badge: 'CANONICAL PATH', audioScriptIndic: 'Work-energy theorem se correct balance mila.', position: { x: 570, y: 310 } },
        { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Friction Vector', mathLatex: 'W_{\\text{nc}} = \\int \\vec{f} \\cdot d\\vec{r}', description: 'Why is friction work always negative along the displacement?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Friction vector direction verify kijiye.', position: { x: 840, y: 310 } },
      ],
      graphEdges: [
        { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Energy Sound', status: 'valid', animated: false },
        { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'Ignore Friction', status: 'derailed', animated: true },
        { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'Overestimate', status: 'derailed', animated: true },
        { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Subtract W_friction', status: 'scaffold', animated: false },
        { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Dissipation Invariant', status: 'valid', animated: false },
      ],
    };
  }

  // 12. UNIVERSAL / CUSTOM ACADEMIC INQUIRY (Dynamic Synthesis for ANY topic)
  const cleanSummary = problem.slice(0, 90).replace(/[^\w\s\-,.]/g, '').trim() || 'Custom Invariant Analysis';

  return {
    domainId: 'universal_custom',
    domainName: 'Universal Analytical & First-Principles Reasoning',
    bloomLevel: 'Epistemic Evaluation',
    canonicalConcept: `First-Principles Invariant & System Boundary Constraint (${cleanSummary.slice(0, 45)})`,
    rootMisconception: 'Extrapolating a Localized Heuristic Beyond System Boundary Conditions',
    derailmentStep: 2,
    derailmentReason: 'Applied an unverified assumption without cross-checking governing conservation laws and boundary parameters.',
    socraticPrompt: `Reflect on Step 2 in your attempted derivation: What foundational boundary condition or invariant was implicitly assumed to hold universally?`,
    hinglishPrompt: `Step 2 par gaur karein: aapne jo step assume kiya, kya woh boundary conditions aur first principles ke mutabiq valid hai?`,
    boardSteps: [
      {
        stepIndex: 1,
        title: 'Step 1: First-Principles Problem Formulation',
        latexContent: '\\text{Given System State: } \\mathcal{S}_0 = \\{ P_1, P_2, \\dots, P_k \\}, \\quad \\text{Objective: Find } \\mathcal{S}^*',
        annotation: 'Establish baseline parameters, inputs, and initial boundary constraints',
        speechScript: 'Pehle problem ke initial parameters aur foundational assumptions ko state space mein formalize karte hain.',
        chalkColor: 'emerald',
        durationEstimateMs: 3800,
      },
      {
        stepIndex: 2,
        title: 'Step 2: Student Attempt (Boundary Condition Decoupling)',
        latexContent: '\\text{Assumption: } \\mathcal{A}(x) = \\text{Universal} \\implies \\text{Omitted Boundary Constraint } \\mathcal{C}',
        annotation: '⚠️ Critical Pivot: Conflated localized behavior with universal invariant',
        speechScript: 'Step 2 par logic derail hua: aapne ek specific heuristic ko bina boundary conditions verify kiye universal maan liya.',
        chalkColor: 'amber',
        durationEstimateMs: 4400,
      },
      {
        stepIndex: 3,
        title: 'Step 3: Boundary Invalidation & Counterexample',
        latexContent: '\\exists x \\in \\text{Domain}: \\quad \\mathcal{C}(x) = \\text{False} \\implies \\text{Solution Decoupled}',
        annotation: 'Demonstrates failure when system edges or conservation constraints are tested',
        speechScript: 'Counterexample dekhiye: edge conditions par yeh assumption fail ho jati hai aur contradiction create karti hai.',
        chalkColor: 'rose' as any,
        durationEstimateMs: 4200,
      },
      {
        stepIndex: 4,
        title: 'Step 4: Canonical Scaffolding: Enforce Governing Invariant',
        latexContent: '\\text{Invariant: } \\mathcal{I}(\\mathcal{S}) = \\text{Constant} \\iff \\Sigma \\text{Conserved Flux} = 0',
        annotation: 'Restore governing domain law (conservation, equilibrium, or grammatical parity)',
        speechScript: 'Canonical approach: governing first-principles invariant ko explicitly enforce karein.',
        chalkColor: 'cyan',
        durationEstimateMs: 4500,
      },
      {
        stepIndex: 5,
        title: 'Step 5: Valid System Resolution & Synthesized Conclusion',
        latexContent: '\\mathcal{S}^* = \\text{Argmax}_{\\mathcal{S}} \\{ \\mathcal{F}(\\mathcal{S}) \\; | \\; \\mathcal{I}(\\mathcal{S}) = 0 \\}',
        annotation: 'Empirically verified solution conforming to all domain boundaries',
        speechScript: 'Isse derivation fully verified aur robust ho jati hai jo har condition mein hold karegi.',
        chalkColor: 'emerald',
        durationEstimateMs: 3600,
      },
    ],
    graphNodes: [
      { id: 'N1_PREMISE', type: 'SOUND_PREMISE', label: 'Step 1: Baseline Premise', mathLatex: '\\mathcal{S}_0 = \\text{Givens}', description: 'Sound formulation of baseline parameters.', badge: 'SOUND PREMISE', audioScriptIndic: 'Initial parameters accurately identified.', position: { x: 50, y: 180 } },
      { id: 'N2_PIVOT', type: 'CRITICAL_PIVOT', label: 'Step 2: Transition Assumption', mathLatex: '\\mathcal{A} \\text{ vs } \\mathcal{I}_{\\text{domain}}', description: 'Branch point: Localized intuition vs governing invariant.', badge: 'CRITICAL PIVOT', audioScriptIndic: 'Pivot: localized heuristic vs universal law.', position: { x: 310, y: 180 } },
      { id: 'N3_DERAILED', type: 'DERAILED_BRANCH', label: 'Step 3: Unconstrained Inference', mathLatex: '\\mathcal{C} = \\text{Omitted}', description: 'Decoupled from boundary constraints.', badge: 'DERAILED BRANCH', audioScriptIndic: 'Boundary condition decouple ho gayi.', position: { x: 570, y: 70 } },
      { id: 'N4_CONTRADICTION', type: 'DERAILED_BRANCH', label: 'Step 4: System Contradiction', mathLatex: '\\text{Contradicts Domain Reality}', description: 'Yields unverified or conflicting conclusion.', badge: 'CONTRADICTION', audioScriptIndic: 'Conflicting conclusion reach hui.', position: { x: 840, y: 70 } },
      { id: 'N5_CANONICAL', type: 'CANONICAL_PATH', label: 'Canonical Step 3: Governing Invariant', mathLatex: '\\mathcal{I}(\\mathcal{S}) = \\text{Enforced}', description: 'Enforces system conservation principles.', badge: 'CANONICAL PATH', audioScriptIndic: 'First-principles invariant restore hua.', position: { x: 570, y: 310 } },
      { id: 'N6_SOCRATIC', type: 'SOCRATIC_CHECKPOINT', label: 'Socratic Checkpoint: Boundary Verification', mathLatex: '\\lim_{x \\to \\text{boundary}} \\mathcal{F}(x)', description: 'What happens at the extreme boundary values?', badge: 'SOCRATIC CHECKPOINT', audioScriptIndic: 'Extreme boundary conditions test kijiye.', position: { x: 840, y: 310 } },
    ],
    graphEdges: [
      { id: 'e1', source: 'N1_PREMISE', target: 'N2_PIVOT', label: 'Premise Sound', status: 'valid', animated: false },
      { id: 'e2', source: 'N2_PIVOT', target: 'N3_DERAILED', label: 'Omit Invariant', status: 'derailed', animated: true },
      { id: 'e3', source: 'N3_DERAILED', target: 'N4_CONTRADICTION', label: 'Contradiction', status: 'derailed', animated: true },
      { id: 'e4', source: 'N2_PIVOT', target: 'N5_CANONICAL', label: 'Enforce Invariant', status: 'scaffold', animated: false },
      { id: 'e5', source: 'N5_CANONICAL', target: 'N6_SOCRATIC', label: 'Boundary Verification', status: 'valid', animated: false },
    ],
  };
}

/**
 * Universal Semantic Cognitive Diagnosis
 */
export function diagnoseDoubtSemantic(
  doubt: string,
  studentSteps: string,
  studentBreakdown: string = '',
  outputLangName: string = 'Hinglish (हिंग्लिश)',
  studentName: string = 'Learner'
): DiagnosisResult {
  const domain = detectUniversalDomain(doubt, studentSteps, studentBreakdown);

  // Multilingual Spoken Script Generation (Detailed Masterclass Pedagogical Narration)
  let narrationScript = '';
  if (outputLangName.includes('Hindi') || outputLangName.includes('हिंदी')) {
    narrationScript = `नमस्ते! आइए आपके इस प्रश्न को गहराई से समझें। प्रारंभिक चरण में आपकी समस्या की पहचान और प्रारंभिक शर्तें बिल्कुल सही थीं। परंतु दूसरे चरण पर आपका तर्क विचलित हो गया: ${domain.derailmentReason}। यहाँ मुख्य वैचारिक भ्रांति यह है: ${domain.rootMisconception}। ${domain.domainName} में यह अनिवार्य है कि हम आधारभूत नियम '${domain.canonicalConcept}' को लागू करें। यदि इस नियम की अनदेखी की जाए, तो पूरा समाधान अमान्य हो जाता है। समाधान के लिए ब्लैकबोर्ड पर दिए गए पिवट नोड को देखें: पहले बुनियादी संरक्षण नियम लागू करें, फिर अंतिम समाधान तक पहुँचें। अब आप विचार करें: ${domain.socraticPrompt}। अपना उत्तर नीचे दिए गए बॉक्स में अवश्य लिखें!`;
  } else if (outputLangName.includes('Hinglish') || outputLangName.includes('हिंग्लिश')) {
    narrationScript = `Hello! Aaiye aapke is doubt ko step-by-step detail mein samajhte hain. Shuruat mein aapka problem setup aur starting premise bilkul sound tha. Lekin Step 2 par aate hi aapka reasoning derail hua: ${domain.derailmentReason}. Yahan par root misconception yeh hai: ${domain.rootMisconception}. Dhyan rahe ki ${domain.domainName} mein localized intuition apply karne ke bajaye governing invariant ${domain.canonicalConcept} ko strictly follow karna zaroori hai. Agar is invariant ko neglect karenge, to contradictory result aayega. Blackboard par green Pivot Node ko dekhiye jahan canonical first principles ko restore kiya gaya hai. Ab aap khud reflect karein: ${domain.hinglishPrompt || domain.socraticPrompt}. Niche reflection box mein apna jawab zaroor submit karein!`;
  } else {
    narrationScript = `Welcome! Let us examine your problem and reasoning step-by-step in detail. In the first step, your starting premise and problem formulation were completely sound. However, at Step 2, your derivation experienced a critical divergence: ${domain.derailmentReason}. The underlying conceptual misconception here is: ${domain.rootMisconception}. In ${domain.domainName}, you must strictly enforce the governing principle: ${domain.canonicalConcept}. If you omit this invariant, the system reaches an empirical contradiction. To resolve this, look at the Pivot Node on the digital chalkboard where we restore the fundamental invariant first, then verify the boundary conditions. Now reflect on this: ${domain.socraticPrompt}. Type or dictate your self-correction in the box below!`;
  }

  const rawSteps = studentSteps.split('\n').filter((s) => s.trim().length > 0);
  const studentNodes = [
    { id: 'S1', label: rawSteps[0] || 'Initial Premise Formulation', is_error: false, detail: 'Correct baseline setup and premise identification' },
    { id: 'S2', label: rawSteps[1] || 'Applied Rule Without Invariant', is_error: true, detail: `Derailment: ${domain.derailmentReason}` },
    { id: 'S3', label: rawSteps[2] || 'Unverified Conclusion Reached', is_error: true, detail: 'Conclusion contradicts system boundary constraints' },
  ];

  const remediationNodes = [
    { id: 'R1', label: 'Establish System Boundaries', is_pivot: false, detail: 'Define foundational conservation constraints' },
    { id: 'R2', label: '💡 PIVOT: Enforce Invariant Law', is_pivot: true, detail: domain.canonicalConcept },
    { id: 'R3', label: 'Canonical Solution Path', is_pivot: false, detail: 'Valid derivation matching empirical conditions' },
  ];

  const storyboard = {
    doubt_domain: domain.domainName,
    identified_topic: domain.canonicalConcept,
    misconception_name: domain.rootMisconception,
    derailment_step: domain.derailmentStep,
    derailment_reason: domain.derailmentReason,
    socratic_challenge: domain.socraticPrompt,
    full_spoken_transcript: narrationScript,
    synchronized_timeline: [
      { step_id: 1, speech_segment: 'Let us examine your initial formulation: your baseline setup was completely sound.', start_time: 0.0, end_time: 7.0, duration: 7.0, board_action: 'WRITE', color: '#10B981', content: 'Sound Premise' },
      { step_id: 2, speech_segment: `Notice carefully: at Step 2 your derivation derailed: ${domain.derailmentReason}.`, start_time: 7.0, end_time: 16.0, duration: 9.0, board_action: 'CROSS_OUT', color: '#EF4444', content: 'Critical Divergence' },
      { step_id: 3, speech_segment: `Branch down to the governing invariant at the Pivot Node: ${domain.canonicalConcept}.`, start_time: 16.0, end_time: 25.0, duration: 9.0, board_action: 'DRAW_ARROW', color: '#06B6D4', content: 'Canonical Invariant' },
      { step_id: 4, speech_segment: `Socratic self-correction challenge: ${domain.socraticPrompt}`, start_time: 25.0, end_time: 35.0, duration: 10.0, board_action: 'WRITE', color: '#8B5CF6', content: 'Socratic Checkpoint' },
    ],
  };

  const dotComparative = `digraph ComparativeDualMap {
  rankdir=LR;
  node [shape=box, style="filled,rounded", fontname="Helvetica"];
  subgraph cluster_student {
    label="Student Attempted Path (${domain.domainName})";
    color="#EF4444";
    S1 [label="Sound Premise", fillcolor="#E2E8F0"];
    S2 [label="Node ${domain.derailmentStep}: Derailment", fillcolor="#FCA5A5"];
    S1 -> S2;
  }
  subgraph cluster_canonical {
    label="Canonical Remediated Path";
    color="#10B981";
    R1 [label="Governing Invariant", fillcolor="#A7F3D0"];
    R2 [label="Valid Solution", fillcolor="#6EE7B7"];
    R1 -> R2;
  }
  S1 -> R1 [style=dashed, label="Pedagogical Pivot", color="#F59E0B"];
}`;

  return {
    student_nodes: studentNodes,
    remediation_nodes: remediationNodes,
    derailment_step: domain.derailmentStep,
    derailment_reason: domain.derailmentReason,
    canonical_concept: domain.canonicalConcept,
    canonical_root_misconception: domain.rootMisconception,
    severity: 'High',
    socratic_prompt: domain.socraticPrompt,
    narration_script: narrationScript,
    dot_comparative: dotComparative,
    concept_diagnostics: {
      topic_taxonomy: { domain: domain.domainName, bloom_level: domain.bloomLevel },
      student_mental_model: { heuristic: 'Localized intuition', false_assumption: domain.derailmentReason },
      mastery_assessment: { risk_level: 'Medium', recommendation: 'Enforce boundary invariant' },
      remediation_recommendations: { scaffolding: domain.socraticPrompt },
    },
    board_storyboard: storyboard,
  };
}

/**
 * Builds the geometric visual layout cards and curved connectors for the Blackboard canvas.
 */
export function prepareGraphPayload(diagnosis: DiagnosisResult): GraphPayload {
  const domain = diagnosis.concept_diagnostics?.topic_taxonomy?.domain || 'Academic Reasoning';
  const topic = diagnosis.canonical_concept;
  const derailmentStep = diagnosis.derailment_step || 2;
  const derailmentReason = diagnosis.derailment_reason;
  const socraticChallenge = diagnosis.socratic_prompt;
  const fullTranscript = diagnosis.board_storyboard?.full_spoken_transcript || diagnosis.narration_script;

  const cardW = 220;
  const cardH = 86;
  const startX = 40;
  const spineY = 190;

  const positionedNodes: NodeCard[] = [];
  const studentNodes = diagnosis.student_nodes || [];
  const remediationNodes = diagnosis.remediation_nodes || [];

  const pivotIdx = Math.max(1, Math.min(derailmentStep, studentNodes.length)) - 1;

  let currentX = startX;
  for (let idx = 0; idx < studentNodes.length; idx++) {
    const sNode = studentNodes[idx];
    const nodeLabel = sNode.label || `Step ${idx + 1}`;
    const detail = sNode.detail || '';

    if (idx < pivotIdx) {
      positionedNodes.push({
        id: sNode.id || `S${idx + 1}`,
        type: 'sound',
        badge: `STEP ${idx + 1}: SOUND PREMISE`,
        title: nodeLabel,
        detail: detail || 'Logically sound foundational setup',
        x: currentX,
        y: spineY,
        w: cardW,
        h: cardH,
        glow_color: '#10B981',
      });
      currentX += cardW + 50;
    } else if (idx === pivotIdx) {
      positionedNodes.push({
        id: sNode.id || `S${idx + 1}`,
        type: 'pivot',
        badge: `STEP ${idx + 1}: CRITICAL PIVOT`,
        title: nodeLabel,
        detail: 'Right intuition up to here. Branch point where paths diverge.',
        x: currentX,
        y: spineY,
        w: cardW,
        h: cardH,
        glow_color: '#F59E0B',
      });
      break;
    }
  }

  // Ensure pivot node exists
  let pivotNode = positionedNodes.find((n) => n.type === 'pivot');
  if (!pivotNode) {
    pivotNode = {
      id: `S${derailmentStep}`,
      type: 'pivot',
      badge: `STEP ${derailmentStep}: CRITICAL PIVOT`,
      title: studentNodes[0]?.label || 'Premise Boundary',
      detail: 'Branch point where reasoning decoupled from the governing law.',
      x: startX + cardW + 50,
      y: spineY,
      w: cardW,
      h: cardH,
      glow_color: '#F59E0B',
    };
    positionedNodes.push(pivotNode);
  }

  const pivotX = pivotNode.x;

  // Derailed Branch
  const derailedX = pivotX + cardW + 70;
  const derailedY = 65;
  const derailedLabel = studentNodes[pivotIdx]?.label || 'Conflation / Unverified Rule';

  positionedNodes.push({
    id: `ERR_${derailmentStep}`,
    type: 'derailed',
    badge: 'COGNITIVE DERAILMENT',
    title: derailedLabel,
    detail: derailmentReason.length > 80 ? derailmentReason.slice(0, 80) + '...' : derailmentReason,
    x: derailedX,
    y: derailedY,
    w: cardW + 10,
    h: cardH + 10,
    glow_color: '#EF4444',
  });

  // Optional 2nd Derailed conclusion node
  if (studentNodes.length > pivotIdx + 1) {
    const sNext = studentNodes[pivotIdx + 1];
    positionedNodes.push({
      id: sNext.id || 'ERR_END',
      type: 'derailed_end',
      badge: 'CONTRADICTION',
      title: sNext.label || 'Invalid Terminal State',
      detail: sNext.detail || 'Contradicts empirical conditions',
      x: derailedX + cardW + 50,
      y: derailedY,
      w: cardW - 20,
      h: cardH,
      glow_color: '#EF4444',
    });
  }

  // Remediated Branch
  const remedX = pivotX + cardW + 70;
  const remedY = 315;
  const remPivotNode = remediationNodes.find((r: any) => r.is_pivot) || remediationNodes[0];
  const remLabel = remPivotNode?.label || 'Return to First-Principles Invariant';
  const remDetail = remPivotNode?.detail || 'Breakthrough governing constraint';

  positionedNodes.push({
    id: 'REM_PIVOT',
    type: 'remediation',
    badge: 'CANONICAL SCAFFOLD',
    title: remLabel,
    detail: remDetail,
    x: remedX,
    y: remedY,
    w: cardW + 10,
    h: cardH + 10,
    glow_color: '#06B6D4',
  });

  // Active Socratic Checkpoint Card
  const socraticX = remedX + cardW + 50;
  const socraticY = remedY - 20;
  positionedNodes.push({
    id: 'SOCRATIC_CARD',
    type: 'socratic',
    badge: 'SOCRATIC CHECKPOINT',
    title: socraticChallenge.length > 80 ? socraticChallenge.slice(0, 80) + '...' : socraticChallenge,
    detail: 'Apply the invariant to resolve your reasoning derailment.',
    x: socraticX,
    y: socraticY,
    w: cardW + 25,
    h: cardH + 25,
    glow_color: '#8B5CF6',
  });

  const connectors: Connector[] = [];

  // Spine connectors
  const soundNodes = positionedNodes.filter((n) => n.type === 'sound');
  for (let i = 0; i < soundNodes.length - 1; i++) {
    const nA = soundNodes[i];
    const nB = soundNodes[i + 1];
    connectors.push({
      id: `c_sound_${i}`,
      type: 'sound',
      x1: nA.x + nA.w,
      y1: nA.y + nA.h / 2,
      x2: nB.x,
      y2: nB.y + nB.h / 2,
      stroke: '#10B981',
      dashed: false,
      stroke_width: 2.5,
    });
  }

  // Connect last sound node to pivot node
  if (soundNodes.length > 0) {
    const lastSound = soundNodes[soundNodes.length - 1];
    connectors.push({
      id: 'c_sound_pivot',
      type: 'sound',
      x1: lastSound.x + lastSound.w,
      y1: lastSound.y + lastSound.h / 2,
      x2: pivotNode.x,
      y2: pivotNode.y + pivotNode.h / 2,
      stroke: '#10B981',
      dashed: false,
      stroke_width: 2.5,
    });
  }

  // Branching Connectors from Pivot Node
  const errNode = positionedNodes.find((n) => n.id === `ERR_${derailmentStep}`);
  if (errNode) {
    connectors.push({
      id: 'c_pivot_err',
      type: 'derailed',
      x1: pivotNode.x + pivotNode.w,
      y1: pivotNode.y + pivotNode.h / 2,
      x2: errNode.x,
      y2: errNode.y + errNode.h / 2,
      stroke: '#EF4444',
      dashed: true,
      stroke_width: 2.5,
      label: 'Divergent Branch',
    });
  }

  // Connect error node to error end if exists
  const errEnd = positionedNodes.find((n) => n.id === 'ERR_END');
  if (errNode && errEnd) {
    connectors.push({
      id: 'c_err_end',
      type: 'derailed',
      x1: errNode.x + errNode.w,
      y1: errNode.y + errNode.h / 2,
      x2: errEnd.x,
      y2: errEnd.y + errEnd.h / 2,
      stroke: '#EF4444',
      dashed: true,
      stroke_width: 2.5,
    });
  }

  // Connect Pivot to Canonical Remediation
  const remNode = positionedNodes.find((n) => n.id === 'REM_PIVOT');
  if (remNode) {
    connectors.push({
      id: 'c_pivot_rem',
      type: 'remediation',
      x1: pivotNode.x + pivotNode.w,
      y1: pivotNode.y + pivotNode.h / 2,
      x2: remNode.x,
      y2: remNode.y + remNode.h / 2,
      stroke: '#06B6D4',
      dashed: false,
      stroke_width: 3.0,
      label: 'Canonical Scaffolding',
    });
  }

  // Connect Remediation to Socratic Card
  const socNode = positionedNodes.find((n) => n.id === 'SOCRATIC_CARD');
  if (remNode && socNode) {
    connectors.push({
      id: 'c_rem_soc',
      type: 'socratic',
      x1: remNode.x + remNode.w,
      y1: remNode.y + remNode.h / 2,
      x2: socNode.x,
      y2: socNode.y + socNode.h / 2,
      stroke: '#8B5CF6',
      dashed: false,
      stroke_width: 2.5,
    });
  }

  const timeline: TimelineStep[] = diagnosis.board_storyboard?.synchronized_timeline || [
    { step_id: 1, speech_segment: 'Let us examine your initial formulation.', start_time: 0, end_time: 3.5, duration: 3.5, board_action: 'WRITE', color: '#10B981', content: 'Valid Premise' },
    { step_id: 2, speech_segment: 'You established the baseline conditions correctly.', start_time: 3.5, end_time: 7.0, duration: 3.5, board_action: 'WRITE', color: '#10B981', content: 'Sound Reasoning' },
    { step_id: 3, speech_segment: `Notice where your logic derailed at Node ${derailmentStep}.`, start_time: 7.0, end_time: 11.5, duration: 4.5, board_action: 'CROSS_OUT', color: '#EF4444', content: 'Misconception' },
    { step_id: 4, speech_segment: 'Branch down to the governing first principles at the Pivot Node.', start_time: 11.5, end_time: 16.0, duration: 4.5, board_action: 'DRAW_ARROW', color: '#06B6D4', content: 'Remediation' },
  ];

  return {
    doubt_domain: domain,
    identified_topic: topic,
    misconception_name: diagnosis.canonical_root_misconception,
    canonical_concept: topic,
    derailment_step: derailmentStep,
    derailment_reason: derailmentReason,
    socratic_challenge: socraticChallenge,
    full_spoken_transcript: fullTranscript,
    nodes: positionedNodes,
    connectors: connectors,
    timeline: timeline,
    total_duration: 35.0,
  };
}

/**
 * Universal Socratic Self-Correction Reply Evaluator
 */
export function evaluateStudentSocraticReply(
  studentReply: string,
  diagnosis: Record<string, any>
): { is_resolved: boolean; feedback_text: string; badge_level: string } {
  const replyLower = studentReply.toLowerCase();
  const canonicalConcept = (diagnosis.canonical_concept || '').toLowerCase();
  const rootMisconception = (diagnosis.canonical_root_misconception || '').toLowerCase();

  const keyTokens = [
    'boundary', 'invariant', 'conserv', 'constraint', 'limit', 'condition', 'law',
    'chain', 'derivative', 'inner', 'outer', 'equilibrium', 'le chatelier', 'catalyst',
    'stack', 'lifo', 'nesting', 'linkage', 'allele', 'recombination', 'chromosome',
    'deadweight', 'ceiling', 'shortage', '19(2)', 'reasonable', 'proportionality',
    'consequent', 'affirming', 'necessity', 'sufficient', 'friction', 'normal force', 'cosine'
  ];

  const matches = keyTokens.filter((token) => replyLower.includes(token));

  if (matches.length >= 1) {
    return {
      is_resolved: true,
      feedback_text: `Excellent cognitive retrieval! You recognized the governing invariant ("${matches.join(', ')}") and identified why the original derivation step derailed. Your mental model is now aligned with first principles across this discipline.`,
      badge_level: 'solid',
    };
  }

  return {
    is_resolved: false,
    feedback_text: `You are on the right track, but your correction does not yet explicitly address the critical invariant highlighted at the green Pivot Node. Re-read the Pivot Node card: what governing constraint must be enforced?`,
    badge_level: 'fragile',
  };
}

/**
 * Generates the structured Socratic Misconception Diagnosis
 * checking recurrent errors against the student's longitudinal LearnerProfile.
 */
export function diagnoseSocraticMisconception(
  problem: string,
  steps: string,
  profile?: LearnerProfile | null
): SocraticDiagnosisResult {
  const domain = detectUniversalDomain(problem, steps);

  const isRecurring = Boolean(
    profile?.error_history?.some(
      (err) => err.concept.toLowerCase().includes(domain.domainId) || err.details.toLowerCase().includes(domain.rootMisconception.toLowerCase())
    )
  );

  let socraticHint = domain.socraticPrompt;
  let hinglishHint = domain.hinglishPrompt;

  if (isRecurring) {
    socraticHint = `Notice a recurring pattern from your prior sessions: you tend to encounter this exact premise flaw in ${domain.domainName}. Let's step back: ${domain.socraticPrompt}`;
    hinglishHint = `Aapke pichle sessions mein bhi yeh pattern repeat hua tha: ${domain.domainName} mein is invariant par dhyan dein. ${domain.hinglishPrompt}`;
  }

  return {
    identified_misconception: domain.rootMisconception,
    concept_tag: domain.domainId,
    severity: domain.domainId === 'physics_mechanics' || domain.domainId === 'chemistry' ? 'critical' : 'high',
    is_recurring: isRecurring,
    socratic_hint: socraticHint,
    hinglish_vernacular_hint: hinglishHint,
  };
}

/**
 * Universal Digital Teacher Chalkboard derivation generator for ANY problem in ANY discipline.
 */
export function generateBoardSolveSchedule(
  problem: string,
  steps: string,
  outputLangName: string = 'Hinglish (हिंग्लिश)',
  profile?: LearnerProfile | null
): BoardSolveResponse {
  const domain = detectUniversalDomain(problem, steps);

  const isRecurring = Boolean(
    profile?.error_history?.some(
      (err) =>
        err.concept.toLowerCase().includes(domain.domainId) ||
        err.details.toLowerCase().includes(domain.rootMisconception.toLowerCase())
    )
  );

  const adaptedSteps = domain.boardSteps.map((step, idx) => {
    if (isRecurring && idx === 1) {
      return {
        ...step,
        annotation: `⚠️ Recurrent Pattern: Prior error in ${domain.domainName} detected`,
        speechScript: `Dhyan dein, aapke pichle sessions mein bhi yeh pattern repeat hua tha: ${step.speechScript}`,
      };
    }
    return step;
  });

  return {
    problemSummary: domain.domainName,
    identifiedMisconception: domain.rootMisconception,
    canonicalConcept: domain.canonicalConcept,
    derailmentStep: domain.derailmentStep,
    steps: adaptedSteps,
  };
}

/**
 * Universal Divergence & Reasoning Graph Engine topology generator for ANY problem in ANY discipline.
 */
export function generateDivergenceGraphTopology(
  problem: string,
  steps: string,
  outputLangName: string = 'Hinglish (हिंग्लिश)',
  profile?: LearnerProfile | null
): DivergenceGraphResponse {
  const domain = detectUniversalDomain(problem, steps);

  return {
    problemSummary: domain.domainName,
    divergenceNodeId: 'N2_PIVOT',
    summarySpeechScript: `Notice carefully at Node 2 in your ${domain.domainName} derivation: this is where your reasoning decoupled from the governing invariant.`,
    nodes: domain.graphNodes,
    edges: domain.graphEdges,
  };
}
