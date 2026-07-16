import { Card } from './Card';
import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  description?: string;
}

export function MetricCard({ title, value, icon, description }: MetricCardProps) {
  return (
    <Card className="p-6 group relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-primary/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      <div className="flex items-start justify-between relative z-10">
        <div>
          <p className="text-sm font-medium text-slate-400 group-hover:text-primary transition-colors duration-300">{title}</p>
          <p className="mt-2 text-3xl font-semibold text-white group-hover:scale-[1.02] origin-left transition-transform duration-300">{value}</p>
        </div>
        {icon && <div className="p-3 bg-slate-900/60 rounded-lg text-primary group-hover:scale-110 group-hover:shadow-glow-primary transition-all duration-300">{icon}</div>}
      </div>
      {description && <p className="mt-4 text-sm text-slate-500 relative z-10">{description}</p>}
    </Card>
  );
}
