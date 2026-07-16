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
    <Card className="p-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-400">{title}</p>
          <p className="mt-2 text-3xl font-semibold text-white">{value}</p>
        </div>
        {icon && <div className="p-3 bg-slate-800 rounded-lg text-primary">{icon}</div>}
      </div>
      {description && <p className="mt-4 text-sm text-slate-500">{description}</p>}
    </Card>
  );
}
