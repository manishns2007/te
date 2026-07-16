import { Badge } from './Badge';

export function StatusChip({ status }: { status: string }) {
  let color = 'bg-slate-700/50 text-slate-300 border border-slate-600';
  if (status === 'PENDING') color = 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/30';
  if (status === 'FLAGGED') color = 'bg-risk-orange/10 text-orange-400 border border-risk-orange/30 shadow-glow-risk-orange';
  if (status === 'FREEZE') color = 'bg-risk-red/10 text-red-400 font-bold border border-risk-red/50 shadow-[0_0_15px_rgba(239,68,68,0.3)]';
  if (status === 'MONITOR') color = 'bg-blue-500/10 text-blue-400 border border-blue-500/30';
  
  return <Badge className={`${color} px-2 py-1`}>{status}</Badge>;
}
