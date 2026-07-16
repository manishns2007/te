import { Card } from './Card';
import React from 'react';

interface SectionCardProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

export function SectionCard({ title, children, className = '' }: SectionCardProps) {
  return (
    <Card className={`flex flex-col ${className}`}>
      <div className="px-6 py-4 border-b border-slate-700">
        <h3 className="text-lg font-medium text-white">{title}</h3>
      </div>
      <div className="p-6 flex-1">
        {children}
      </div>
    </Card>
  );
}
