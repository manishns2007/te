import { Activity } from 'lucide-react';

export default function Navbar() {
  return (
    <header className="bg-surface border-b border-slate-700 h-16 flex items-center px-6 shrink-0 shadow-sm z-10">
      <div className="flex items-center gap-2">
        <Activity className="text-primary w-6 h-6" />
        <span className="text-lg font-semibold text-white tracking-wide">DecisionLedger <span className="text-primary font-bold">TEC</span></span>
      </div>
    </header>
  );
}
