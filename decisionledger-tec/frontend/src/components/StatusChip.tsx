import { Badge } from './Badge';

export function StatusChip({ status }: { status: string }) {
  let color = 'bg-slate-700 text-slate-300';
  if (status === 'PENDING') color = 'bg-yellow-500/20 text-yellow-500';
  if (status === 'FLAGGED') color = 'bg-orange-500/20 text-orange-500';
  if (status === 'FREEZE') color = 'bg-red-500/20 text-red-500';
  if (status === 'MONITOR') color = 'bg-blue-500/20 text-blue-500';
  
  return <Badge className={color}>{status}</Badge>;
}
