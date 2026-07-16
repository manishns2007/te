import { useRef } from 'react';
import VariableProximity from './VariableProximity';

export function PageHeader({ title, subtitle }: { title: string, subtitle?: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  
  return (
    <div className="mb-8" ref={containerRef}>
      <h1 className="text-2xl font-bold text-white tracking-tight">
        <VariableProximity
          label={title}
          fromFontVariationSettings="'wght' 400, 'opsz' 9"
          toFontVariationSettings="'wght' 800, 'opsz' 40"
          containerRef={containerRef}
          radius={120}
          falloff="linear"
        />
      </h1>
      {subtitle && <p className="mt-1 text-slate-400">{subtitle}</p>}
    </div>
  );
}
