import React, { useMemo } from 'react';
import katex from 'katex';

interface MathRendererProps {
  math: string;
  displayMode?: boolean;
  className?: string;
}

const STANDARD_MATH_COMMANDS = new Set([
  'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log', 'ln', 'exp', 'min', 'max', 'lim',
  'det', 'sum', 'int', 'prod', 'inf', 'sup', 'deg', 'dim', 'ker', 'hom', 'arg', 'gcd',
  'frac', 'sqrt', 'cdot', 'neq', 'times', 'approx', 'boxed', 'text', 'implies',
  'mathbf', 'mathrm', 'mathcal', 'Omega', 'theta', 'alpha', 'beta', 'gamma', 'delta', 'lambda',
  'mu', 'pi', 'rho', 'sigma', 'omega', 'Delta', 'Theta', 'Lambda', 'Sigma', 'Phi'
]);

export const MathRenderer: React.FC<MathRendererProps> = ({
  math,
  displayMode = false,
  className = '',
}) => {
  const renderedContent = useMemo(() => {
    if (!math) return { isHtml: false, text: '' };
    try {
      // Strip outer $ or $$ delimiters
      let cleanMath = math.replace(/^\$\$([\s\S]*)\$\$$/, '$1').replace(/^\$([\s\S]*)\$$/, '$1').trim();

      // If purely plain text without any LaTeX commands or math symbols, render as plain styled text
      // to avoid KaTeX stripping spaces between words
      if (!/[\\_{}^$=<>±×÷≈≠≤≥]/.test(cleanMath)) {
        return { isHtml: false, text: cleanMath };
      }

      // Repair accidental unescaped backslashes in JS literals (e.g. \neq -> \n + eq)
      cleanMath = cleanMath.replace(/\r?\n(eq|approx|in|times|le|ge|sim|circ|cdot|frac|sqrt|sin|cos|tan)/g, '\\$1');

      // Wrap bare words (3+ letters) that are separated by spaces and not LaTeX commands in \text{}
      // so KaTeX maintains proper natural spacing instead of squishing words together
      const processed = cleanMath.replace(/(?<!\\|\w)([a-zA-Z]{3,}(?:\s+[a-zA-Z]{3,})*)(?!\w)/g, (match) => {
        if (STANDARD_MATH_COMMANDS.has(match.trim().toLowerCase())) return match;
        return `\\text{${match}}`;
      });

      const html = katex.renderToString(processed, {
        throwOnError: false,
        displayMode: displayMode,
      });

      return { isHtml: true, html };
    } catch (e) {
      console.warn('KaTeX rendering error for:', math, e);
      return { isHtml: false, text: math };
    }
  }, [math, displayMode]);

  if (!math) return null;

  if (!renderedContent.isHtml) {
    return (
      <span className={`inline-block font-sans text-xs text-emerald-300 font-medium tracking-normal ${className}`}>
        {renderedContent.text}
      </span>
    );
  }

  return (
    <span
      className={`inline-block max-w-full overflow-x-auto overflow-y-hidden align-middle scrollbar-thin ${
        displayMode ? 'w-full my-1 text-center block' : ''
      } ${className}`}
      dangerouslySetInnerHTML={{ __html: renderedContent.html || '' }}
    />
  );
};
