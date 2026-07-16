import { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer, Legend } from 'recharts';
import { AlertOctagon, Activity, CheckCircle, ShieldAlert, Play, Square } from 'lucide-react';
import { DashboardService } from '../services/api';
import type { DashboardData, Transaction } from '../types';
import { PageHeader } from '../components/PageHeader';
import { MetricCard } from '../components/MetricCard';
import { SectionCard } from '../components/SectionCard';
import { StatusChip } from '../components/StatusChip';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorState } from '../components/ErrorState';
import { Button } from '../components/Button';

export default function Dashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  useEffect(() => {
    DashboardService.getDashboardData()
      .then(setData)
      .catch((e) => setError(e.message || 'Failed to load dashboard data'))
      .finally(() => setLoading(false));
  }, []);

  // Live Traffic Simulation
  useEffect(() => {
    if (!isSimulating) return;
    const interval = setInterval(() => {
      const categories = ['International Wire', 'Crypto Purchase', 'High-Value Transfer', 'B2B Payment'];
      const names = ['Acme Corp', 'John Doe', 'Global Tech', 'Jane Smith', 'Unknown Entity'];
      const newTx: Transaction = {
        id: `TXN-${Math.floor(Math.random() * 100000000)}`,
        account_id: `ACC-${Math.floor(Math.random() * 9999)}`,
        customer_name: names[Math.floor(Math.random() * names.length)],
        amount: Math.random() * 25000 + 1000,
        merchant_category: categories[Math.floor(Math.random() * categories.length)],
        status: 'PENDING',
        timestamp: new Date().toISOString()
      };
      
      setData(prev => {
        if (!prev) return prev;
        return {
          ...prev,
          kpis: {
            ...prev.kpis,
            pending_investigations: prev.kpis.pending_investigations + 1,
            high_risk_transactions: prev.kpis.high_risk_transactions + (Math.random() > 0.5 ? 1 : 0)
          },
          queue: [newTx, ...prev.queue].slice(0, 50) // Keep UI snappy
        };
      });
    }, 2500); // 2.5 seconds
    return () => clearInterval(interval);
  }, [isSimulating]);

  const riskData = useMemo(() => {
    if (!data) return [];
    const counts = data.queue.reduce((acc, tx) => {
       acc[tx.status] = (acc[tx.status] || 0) + 1;
       return acc;
    }, {} as Record<string, number>);
    return Object.entries(counts).map(([name, value]) => ({ name, value }));
  }, [data]);

  const COLORS = ['#3b82f6', '#f59e0b', '#f97316', '#ef4444', '#10b981'];

  if (loading) return <LoadingSpinner size={32} />;
  if (error) return <ErrorState message={error} />;
  if (!data) return null;

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="pb-12">
      
      <div className="flex justify-between items-start mb-6">
        <PageHeader title="Executive Dashboard" subtitle="Global transaction queue and risk analytics" />
        <Button 
          variant={isSimulating ? 'danger' : 'primary'} 
          onClick={() => setIsSimulating(!isSimulating)}
          className="shadow-lg shadow-primary/20"
        >
          {isSimulating ? <Square size={16} className="mr-2" /> : <Play size={16} className="mr-2" />}
          {isSimulating ? "Stop Live Feed" : "Simulate Live Traffic"}
        </Button>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard 
          title="High Risk Trans." 
          value={data.kpis.high_risk_transactions} 
          icon={<AlertOctagon className="text-risk-red" />} 
        />
        <MetricCard 
          title="Pending Reviews" 
          value={data.kpis.pending_investigations} 
          icon={<Activity className="text-risk-orange" />} 
        />
        <MetricCard 
          title="Avg Confidence" 
          value={`${(data.kpis.average_confidence * 100).toFixed(1)}%`} 
          icon={<CheckCircle className="text-risk-green" />} 
        />
        <MetricCard 
          title="Prevented Loss" 
          value={`$${data.kpis.estimated_prevented_loss.toLocaleString()}`} 
          icon={<ShieldAlert className="text-primary" />} 
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <SectionCard title="Transaction Status Distribution">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={riskData} innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                  {riskData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }} itemStyle={{ color: '#fff' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </SectionCard>
        
        <SectionCard title="Recent Activity">
           <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.queue.slice(0, 10).map(q => ({ name: q.customer_name.split(' ')[0], amount: q.amount }))}>
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <RechartsTooltip cursor={{fill: '#334155'}} contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }} />
                <Bar dataKey="amount" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </SectionCard>
      </div>

      {/* Table */}
      <SectionCard title="Investigation Queue">
        <div className="overflow-x-auto -mx-6 px-6">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="py-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">Transaction</th>
                <th className="py-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">Customer</th>
                <th className="py-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">Amount</th>
                <th className="py-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">Timestamp</th>
                <th className="py-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody>
              <AnimatePresence initial={false}>
                {data.queue.map((tx: Transaction) => (
                  <motion.tr 
                    layout
                    initial={{ opacity: 0, y: -20, backgroundColor: 'rgba(59, 130, 246, 0.3)' }}
                    animate={{ opacity: 1, y: 0, backgroundColor: 'transparent' }}
                    transition={{ duration: 0.5 }}
                    key={tx.id} 
                    onClick={() => navigate(`/decision/${tx.id}`)}
                    className="border-b border-slate-700/50 hover:bg-slate-700/30 cursor-pointer group"
                  >
                    <td className="py-4 text-sm font-medium text-white group-hover:text-primary transition-colors">{tx.id.substring(0,8)}...</td>
                    <td className="py-4 text-sm text-slate-300">{tx.customer_name}</td>
                    <td className="py-4 text-sm text-slate-300">${tx.amount.toFixed(2)}</td>
                    <td className="py-4 text-sm text-slate-400">{new Date(tx.timestamp).toLocaleString()}</td>
                    <td className="py-4"><StatusChip status={tx.status} /></td>
                  </motion.tr>
                ))}
              </AnimatePresence>
            </tbody>
          </table>
          {data.queue.length === 0 && (
            <div className="text-center py-8 text-slate-500">No transactions in queue.</div>
          )}
        </div>
      </SectionCard>
    </motion.div>
  );
}
