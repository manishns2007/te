import React from 'react';
import { Inbox } from 'lucide-react';

export function EmptyState({ title, description, icon }: { title: string, description?: string, icon?: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center h-full">
      <div className="text-slate-500 mb-4">{icon || <Inbox size={48} />}</div>
      <h3 className="text-lg font-medium text-white">{title}</h3>
      {description && <p className="mt-2 text-sm text-slate-400 max-w-sm">{description}</p>}
    </div>
  );
}
