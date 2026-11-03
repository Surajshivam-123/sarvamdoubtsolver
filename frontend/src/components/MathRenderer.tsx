import React, { useMemo } from 'react';
import katex from 'katex';

interface MathRendererProps {
  math: string;
  displayMode?: boolean;
  className?: string;
}

export const MathRenderer: React.FC<MathRendererProps> = ({
  math,
  displayMode = false,
  className = '',
}) => {
  const html = useMemo(() => {
    if (!math) return '';
    try {
      // Strip outer $ or $$ if present
      const cleanMath = math.replace(/^\$\$([\s\S]*)\$\$$/, '$1').replace(/^\$([\s\S]*)\$$/, '$1');
      return katex.renderToString(cleanMath, {
        throwOnError: false,
        displayMode: displayMode,
      });
    } catch (e) {
      console.warn('KaTeX rendering error for:', math, e);
      return `<code class="font-mono text-emerald-300 text-xs">${math}</code>`;
    }
  }, [math, displayMode]);

  if (!math) return null;

  return (
    <span
      className={`inline-block max-w-full overflow-x-auto overflow-y-hidden align-middle scrollbar-thin ${
        displayMode ? 'w-full my-1 text-center block' : ''
      } ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
};
