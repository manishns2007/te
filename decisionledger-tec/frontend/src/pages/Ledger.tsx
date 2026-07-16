import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Database, ShieldCheck, Lock } from 'lucide-react';
import { PageHeader } from '../components/PageHeader';
import { Card } from '../components/Card';
import { StatusChip } from '../components/StatusChip';
import { DashboardService } from '../services/api';

export default function Ledger() {
  const [entries, setEntries] = useState<any[]>([]);

  useEffect(() => {
    // Fetch data and generate mock cryptographic hashes for the ledger demo
    DashboardService.getDashboardData().then((data) => {
      const generated = data.queue
        .filter(tx => tx.status !== 'PENDING')
        .map(tx => ({
          ...tx,
          hash: Array.from({ length: 64 }, () => Math.floor(Math.random() * 16).toString(16)).join(''),
          blockId: `BLK-${Math.floor(Math.random() * 9000) + 1000}`
        }));
      setEntries(generated);
    });
  }, []);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="pb-12">
      <div className="flex items-center gap-3 mb-2">
        <Lock className="text-risk-green" size={24} />
        <PageHeader title="Immutable Ledger" subtitle="Cryptographically verified investigator decisions" />
      </div>

      <div className="mt-8 space-y-4">
        {entries.map((entry, idx) => (
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
            key={entry.id}
          >
            <Card className="p-5 border-l-4 border-l-risk-green border-t-slate-700 border-r-slate-700 border-b-slate-700 bg-slate-900/80">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <ShieldCheck size={16} className="text-risk-green" />
                    <span className="text-sm font-semibold text-white">Block {entry.blockId}</span>
                    <span className="text-xs text-slate-500">{new Date(entry.timestamp).toLocaleString()}</span>
                  </div>
                  <div className="font-mono text-xs text-slate-400 break-all bg-black/50 p-2 rounded border border-slate-800">
                    <span className="text-primary/70">SHA-256: </span> {entry.hash}
                  </div>
                </div>

                <div className="flex items-center gap-8">
                  <div className="text-right">
                    <p className="text-xs text-slate-500">Transaction ID</p>
                    <p className="text-sm text-slate-300 font-mono">{entry.id}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-slate-500">Decision Recorded</p>
                    <StatusChip status={entry.status} />
                  </div>
                </div>
                
              </div>
            </Card>
          </motion.div>
        ))}

        {entries.length === 0 && (
          <div className="text-center py-20 text-slate-500">
            <Database size={48} className="mx-auto mb-4 opacity-20" />
            <p>No immutable decisions recorded yet.</p>
          </div>
        )}
      </div>
    </motion.div>
  );
}
