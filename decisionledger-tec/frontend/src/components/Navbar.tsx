import { Activity } from 'lucide-react';

export default function Navbar() {
  return (
    <header className="bg-surface/50 backdrop-blur-xl border-b border-slate-800 h-16 flex items-center px-6 shrink-0 shadow-sm z-10 sticky top-0">
      <div className="flex items-center gap-2 group cursor-pointer">
        <Activity className="text-primary w-6 h-6 group-hover:scale-110 transition-transform duration-300 group-hover:drop-shadow-[0_0_8px_rgba(56,189,248,0.8)]" />
        <span className="text-lg font-semibold text-white tracking-wide">DecisionLedger <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary font-bold">TEC</span></span>
      </div>
    </header>
  );
}
