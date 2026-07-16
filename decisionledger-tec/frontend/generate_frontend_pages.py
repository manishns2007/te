import os

frontend_path = r"C:\Users\NEELS\Desktop\TeleFusion\decisionledger-tec\frontend\src"

files = {
    "types/index.ts": """export interface TelemetryData {
  device_fingerprint: string;
  device_trust_score: number;
  ip_address: string;
  ip_reputation: string;
  vpn_detected: boolean;
  failed_logins: number;
  impossible_travel: boolean;
  browser_changed: boolean;
  powershell_execution: boolean;
  endpoint_alert: boolean;
  known_device: boolean;
  session_risk: number;
  velocity_score: number;
}

export interface Prediction {
  fraud_probability: number;
  confidence_score: number;
  expected_prevented_loss: number;
  recommendation: string;
  shap_top_features: string;
  natural_language_explanation: string;
}

export interface InvestigationDecision {
  action_taken: string;
  notes: string;
  investigator_id: string;
  created_at: string;
}

export interface Transaction {
  id: string;
  account_id: string;
  customer_name: string;
  amount: number;
  merchant_category: string;
  status: string;
  timestamp: string;
}

export interface TransactionDetail extends Transaction {
  telemetry?: TelemetryData;
  prediction?: Prediction;
  decision?: InvestigationDecision;
}

export interface KPIMetrics {
  high_risk_transactions: number;
  pending_investigations: number;
  average_confidence: number;
  estimated_prevented_loss: number;
}

export interface DashboardData {
  kpis: KPIMetrics;
  queue: Transaction[];
}
""",
    "services/api.ts": """import axios from 'axios';
import { DashboardData, TransactionDetail, Prediction } from '../types';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const DashboardService = {
    getDashboardData: async (): Promise<DashboardData> => {
        const res = await api.get('/dashboard');
        return res.data;
    },
};

export const TransactionService = {
    getTransaction: async (id: string): Promise<TransactionDetail> => {
        const res = await api.get(/transactions/);
        return res.data;
    },
};

export const DecisionService = {
    submitDecision: async (id: string, action: string, notes: string) => {
        const res = await api.post(/transactions//decision, { action_taken: action, notes, investigator_id: 'Investigator-1' });
        return res.data;
    },
};

export const PredictionService = {
    repredict: async (id: string): Promise<Prediction> => {
        const res = await api.post(/transactions//repredict);
        return res.data;
    }
}

export default api;
""",
    "pages/LandingPage.tsx": """import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Activity, Shield, Zap, BarChart3, Database } from 'lucide-react';
import { Card } from '../components/Card';
import { StatusChip } from '../components/StatusChip';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background overflow-hidden relative">
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/10 blur-[100px]" />
        <div className="absolute top-[20%] right-[-5%] w-[30%] h-[30%] rounded-full bg-risk-red/10 blur-[100px]" />
      </div>

      <div className="container mx-auto px-6 py-20 relative z-10">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700 text-slate-300 text-sm mb-6">
              <Zap size={14} className="text-primary" />
              <span>Enterprise SOC Platform</span>
            </div>
            
            <h1 className="text-5xl lg:text-6xl font-bold text-white leading-tight mb-6 tracking-tight">
              AI-Powered Banking Fraud <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">Decision Intelligence</span>
            </h1>
            
            <p className="text-lg text-slate-400 mb-10 leading-relaxed max-w-xl">
              Correlate banking transactions with cybersecurity telemetry. 
              Explain every AI decision using XGBoost and SHAP Explainability. 
              Built for modern SOC and fraud investigation teams.
            </p>
            
            <div className="flex flex-wrap gap-4">
              <Link to="/dashboard" className="px-6 py-3 rounded-lg bg-primary hover:bg-blue-600 text-white font-medium transition-colors shadow-lg shadow-primary/20 flex items-center gap-2">
                Launch Dashboard
                <Activity size={18} />
              </Link>
              <button className="px-6 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-medium transition-colors border border-slate-700">
                View Architecture
              </button>
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
             <Card className="bg-slate-900/80 backdrop-blur-xl border-slate-700 p-6 shadow-2xl relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-risk-red to-risk-orange" />
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h3 className="text-white font-medium text-lg">Transaction Analysis</h3>
                    <p className="text-slate-400 text-sm">TXN-982374982</p>
                  </div>
                  <StatusChip status="FREEZE" />
                </div>
                
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
                    <p className="text-slate-400 text-xs mb-1">Fraud Probability</p>
                    <p className="text-3xl font-bold text-risk-red">94.2%</p>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
                    <p className="text-slate-400 text-xs mb-1">Prevented Loss</p>
                    <p className="text-3xl font-bold text-risk-green">,450</p>
                  </div>
                </div>

                <div className="space-y-3">
                  <h4 className="text-sm font-medium text-slate-300">Top Risk Factors (SHAP)</h4>
                  <div className="bg-slate-800/50 p-3 rounded border border-slate-700 flex justify-between items-center">
                    <span className="text-sm text-slate-300">Impossible Travel</span>
                    <span className="text-xs bg-risk-red/20 text-risk-red px-2 py-1 rounded">+2.45</span>
                  </div>
                  <div className="bg-slate-800/50 p-3 rounded border border-slate-700 flex justify-between items-center">
                    <span className="text-sm text-slate-300">VPN Detected</span>
                    <span className="text-xs bg-risk-red/20 text-risk-red px-2 py-1 rounded">+1.82</span>
                  </div>
                </div>
             </Card>
          </motion.div>

        </div>
        
        <div className="mt-32 pb-20">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">Enterprise Grade Telemetry</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">Unify your cybersecurity signals with transactional data to stop fraud before it happens.</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="p-6 bg-surface/50 border-slate-700/50 hover:border-primary/50 transition-colors">
              <Shield className="text-primary w-10 h-10 mb-4" />
              <h3 className="text-lg font-medium text-white mb-2">Endpoint Security</h3>
              <p className="text-slate-400 text-sm">Correlate suspicious PowerShell execution and malware alerts directly with high-value transfers.</p>
            </Card>
            <Card className="p-6 bg-surface/50 border-slate-700/50 hover:border-secondary/50 transition-colors">
              <Database className="text-secondary w-10 h-10 mb-4" />
              <h3 className="text-lg font-medium text-white mb-2">Identity & Access</h3>
              <p className="text-slate-400 text-sm">Track impossible travel, VPN usage, and credential stuffing attacks leading up to transactions.</p>
            </Card>
            <Card className="p-6 bg-surface/50 border-slate-700/50 hover:border-risk-green/50 transition-colors">
              <BarChart3 className="text-risk-green w-10 h-10 mb-4" />
              <h3 className="text-lg font-medium text-white mb-2">Explainable AI</h3>
              <p className="text-slate-400 text-sm">Every prediction is backed by SHAP values and converted into natural language for investigators.</p>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
""",
    "pages/Dashboard.tsx": """import { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer, Legend } from 'recharts';
import { AlertOctagon, Activity, CheckCircle, ShieldAlert } from 'lucide-react';
import { DashboardService } from '../services/api';
import { DashboardData, Transaction } from '../types';
import { PageHeader } from '../components/PageHeader';
import { MetricCard } from '../components/MetricCard';
import { SectionCard } from '../components/SectionCard';
import { StatusChip } from '../components/StatusChip';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorState } from '../components/ErrorState';

export default function Dashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    DashboardService.getDashboardData()
      .then(setData)
      .catch((e) => setError(e.message || 'Failed to load dashboard data'))
      .finally(() => setLoading(false));
  }, []);

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
      <PageHeader title="Executive Dashboard" subtitle="Global transaction queue and risk analytics" />

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
          value={${(data.kpis.average_confidence * 100).toFixed(1)}%} 
          icon={<CheckCircle className="text-risk-green" />} 
        />
        <MetricCard 
          title="Prevented Loss" 
          value={$} 
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
                  {riskData.map((entry, index) => (
                    <Cell key={cell-} fill={COLORS[index % COLORS.length]} />
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
              {data.queue.map((tx: Transaction) => (
                <tr 
                  key={tx.id} 
                  onClick={() => navigate(/decision/)}
                  className="border-b border-slate-700/50 hover:bg-slate-700/30 cursor-pointer transition-colors group"
                >
                  <td className="py-4 text-sm font-medium text-white group-hover:text-primary transition-colors">{tx.id.substring(0,8)}...</td>
                  <td className="py-4 text-sm text-slate-300">{tx.customer_name}</td>
                  <td className="py-4 text-sm text-slate-300"></td>
                  <td className="py-4 text-sm text-slate-400">{new Date(tx.timestamp).toLocaleString()}</td>
                  <td className="py-4"><StatusChip status={tx.status} /></td>
                </tr>
              ))}
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
""",
    "pages/DecisionConsole.tsx": """import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { TransactionService, DecisionService, PredictionService } from '../services/api';
import { TransactionDetail, Prediction } from '../types';
import { PageHeader } from '../components/PageHeader';
import { Card } from '../components/Card';
import { StatusChip } from '../components/StatusChip';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorState } from '../components/ErrorState';
import { Button } from '../components/Button';
import { ArrowLeft, RefreshCw, CheckCircle, ShieldAlert, Monitor, AlertTriangle } from 'lucide-react';

export default function DecisionConsole() {
  const { transactionId } = useParams<{ transactionId: string }>();
  const navigate = useNavigate();
  const [tx, setTx] = useState<TransactionDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [notes, setNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [repredicting, setRepredicting] = useState(false);

  useEffect(() => {
    if (!transactionId) return;
    loadData();
  }, [transactionId]);

  const loadData = () => {
    setLoading(true);
    TransactionService.getTransaction(transactionId!)
      .then(data => {
        setTx(data);
        if(data.decision) setNotes(data.decision.notes);
      })
      .catch((e) => setError(e.message || 'Failed to load transaction details'))
      .finally(() => setLoading(false));
  };

  const submitDecision = async (action: string) => {
    if (!transactionId) return;
    setSubmitting(true);
    try {
      await DecisionService.submitDecision(transactionId, action, notes);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
      loadData();
    } catch (e: any) {
      alert('Error submitting decision: ' + e.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleRepredict = async () => {
    if (!transactionId) return;
    setRepredicting(true);
    try {
      const newPrediction = await PredictionService.repredict(transactionId);
      setTx(prev => prev ? { ...prev, prediction: newPrediction } : prev);
    } catch (e: any) {
      alert('Error repredicting: ' + e.message);
    } finally {
      setRepredicting(false);
    }
  };

  if (loading) return <LoadingSpinner size={32} />;
  if (error) return <ErrorState message={error} />;
  if (!tx) return null;

  const pred = tx.prediction;
  const tel = tx.telemetry;
  const prob = pred ? Math.round(pred.fraud_probability * 100) : 0;
  
  let riskColor = 'text-risk-green';
  let riskBg = 'bg-risk-green';
  if (prob > 50) { riskColor = 'text-risk-yellow'; riskBg = 'bg-risk-yellow'; }
  if (prob > 70) { riskColor = 'text-risk-orange'; riskBg = 'bg-risk-orange'; }
  if (prob > 85) { riskColor = 'text-risk-red'; riskBg = 'bg-risk-red'; }

  const shapFeatures = pred?.shap_top_features ? JSON.parse(pred.shap_top_features) : {};
  const sortedShap = Object.entries(shapFeatures).sort((a: any, b: any) => Math.abs(b[1]) - Math.abs(a[1])).slice(0,5);

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="pb-12 relative">
      {success && (
        <div className="fixed top-6 right-6 bg-risk-green text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-2 z-50 animate-bounce">
          <CheckCircle size={20} />
          Decision submitted successfully.
        </div>
      )}

      <div className="flex items-center gap-4 mb-6">
        <button onClick={() => navigate('/dashboard')} className="p-2 hover:bg-slate-700 rounded-full transition-colors text-slate-400 hover:text-white">
          <ArrowLeft size={20} />
        </button>
        <PageHeader title={Transaction Investigation} subtitle={tx.id} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* LEFT COLUMN: Customer & TX */}
        <div className="lg:col-span-3 space-y-6">
          <Card className="p-5">
            <h3 className="text-slate-300 font-medium mb-4 uppercase text-xs tracking-wider">Customer Profile</h3>
            <div className="space-y-4">
              <div>
                <p className="text-slate-500 text-xs">Name</p>
                <p className="text-white font-medium">{tx.customer_name}</p>
              </div>
              <div>
                <p className="text-slate-500 text-xs">Account ID</p>
                <p className="text-white font-medium">{tx.account_id}</p>
              </div>
            </div>
          </Card>

          <Card className="p-5">
            <h3 className="text-slate-300 font-medium mb-4 uppercase text-xs tracking-wider">Transaction Details</h3>
            <div className="space-y-4">
              <div>
                <p className="text-slate-500 text-xs">Amount</p>
                <p className="text-2xl font-bold text-white"></p>
              </div>
              <div>
                <p className="text-slate-500 text-xs">Category</p>
                <p className="text-slate-300">{tx.merchant_category}</p>
              </div>
              <div>
                <p className="text-slate-500 text-xs">Time</p>
                <p className="text-slate-300">{new Date(tx.timestamp).toLocaleString()}</p>
              </div>
              <div>
                <p className="text-slate-500 text-xs mb-1">Status</p>
                <StatusChip status={tx.status} />
              </div>
            </div>
          </Card>
        </div>

        {/* CENTER COLUMN: AI Analysis */}
        <div className="lg:col-span-6 space-y-6">
          <Card className="p-6 relative overflow-hidden">
            <div className="absolute top-4 right-4">
              <Button variant="ghost" onClick={handleRepredict} disabled={repredicting} className="text-xs">
                <RefreshCw size={14} className={mr-2 } />
                Run AI Again
              </Button>
            </div>
            
            <h3 className="text-slate-300 font-medium mb-8 uppercase text-xs tracking-wider">AI Risk Analysis</h3>
            
            <div className="flex flex-col items-center justify-center mb-8">
              <div className="relative w-48 h-48 flex items-center justify-center">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="45" fill="none" stroke="#334155" strokeWidth="10" />
                  <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" strokeWidth="10" strokeDasharray="283" strokeDashoffset={283 - (283 * prob) / 100} className={${riskColor} transition-all duration-1000 ease-out} />
                </svg>
                <div className="absolute flex flex-col items-center justify-center">
                  <span className={	ext-4xl font-bold }>{prob}%</span>
                  <span className="text-xs text-slate-400 mt-1">Fraud Risk</span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6 text-center">
              <div className="bg-slate-800/50 p-4 rounded-lg">
                <p className="text-slate-500 text-xs mb-1">Confidence</p>
                <p className="text-lg text-white">{(pred?.confidence_score! * 100).toFixed(1)}%</p>
              </div>
              <div className="bg-slate-800/50 p-4 rounded-lg">
                <p className="text-slate-500 text-xs mb-1">Prevented Loss</p>
                <p className="text-lg text-risk-green"></p>
              </div>
            </div>

            <div className="bg-primary/10 border border-primary/20 rounded-lg p-4 mb-6">
              <p className="text-sm text-primary leading-relaxed">
                <span className="font-semibold mr-2">AI Explanation:</span>
                {pred?.natural_language_explanation || "No explanation generated."}
              </p>
            </div>

            <div>
              <h4 className="text-xs text-slate-400 uppercase tracking-wider mb-3">SHAP Feature Impact</h4>
              <div className="space-y-3">
                {sortedShap.map(([feat, val]: any) => (
                  <div key={feat} className="relative pt-1">
                    <div className="flex mb-1 items-center justify-between">
                      <span className="text-xs font-medium text-slate-300">{feat}</span>
                      <span className="text-xs font-medium text-slate-400">{val > 0 ? '+' : ''}{val.toFixed(2)}</span>
                    </div>
                    <div className="overflow-hidden h-2 text-xs flex rounded bg-slate-800">
                      <div style={{ width: ${Math.min(Math.abs(val)*20, 100)}% }} className={shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center }></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>

        {/* RIGHT COLUMN: Evidence & Action */}
        <div className="lg:col-span-3 space-y-6">
          <Card className="p-5">
            <h3 className="text-slate-300 font-medium mb-4 uppercase text-xs tracking-wider">Cyber Evidence</h3>
            {tel ? (
              <div className="space-y-3">
                <div className={p-3 rounded border flex items-start gap-3 }>
                  <AlertTriangle size={16} className="mt-0.5 shrink-0" />
                  <div>
                    <p className="text-sm font-medium">Impossible Travel</p>
                    <p className="text-xs opacity-80">{tel.impossible_travel ? 'Detected in last 24h' : 'Normal pattern'}</p>
                  </div>
                </div>
                
                <div className={p-3 rounded border flex items-start gap-3 }>
                  <ShieldAlert size={16} className="mt-0.5 shrink-0" />
                  <div>
                    <p className="text-sm font-medium">VPN/Proxy</p>
                    <p className="text-xs opacity-80">{tel.vpn_detected ? 'Anonymizer detected' : 'Clean IP'}</p>
                  </div>
                </div>

                <div className={p-3 rounded border flex items-start gap-3 }>
                  <Monitor size={16} className="mt-0.5 shrink-0" />
                  <div>
                    <p className="text-sm font-medium">Endpoint Risk</p>
                    <p className="text-xs opacity-80">{tel.powershell_execution ? 'Suspicious PowerShell' : tel.endpoint_alert ? 'Malware Alert' : 'Secure'}</p>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t border-slate-700">
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-slate-400">Device Trust</span>
                    <span className={tel.device_trust_score < 50 ? 'text-risk-red' : 'text-risk-green'}>{tel.device_trust_score}/100</span>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-sm text-slate-500">No cyber telemetry linked.</p>
            )}
          </Card>

          <Card className="p-5 border-primary/30 shadow-[0_0_15px_rgba(59,130,246,0.1)]">
            <h3 className="text-slate-300 font-medium mb-4 uppercase text-xs tracking-wider">Investigator Action</h3>
            <div className="mb-4">
              <label className="block text-xs text-slate-400 mb-2">Investigation Notes</label>
              <textarea 
                value={notes} 
                onChange={(e) => setNotes(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-primary resize-none h-24"
                placeholder="Enter investigation details..."
                disabled={tx.status !== 'PENDING' && tx.status !== 'FLAGGED'}
              />
            </div>
            
            <div className="space-y-2">
              <Button onClick={() => submitDecision('FREEZE')} disabled={submitting || (tx.status !== 'PENDING' && tx.status !== 'FLAGGED')} variant="danger" className="w-full justify-center">FREEZE ACCOUNT</Button>
              <div className="grid grid-cols-2 gap-2">
                <Button onClick={() => submitDecision('STEP_UP')} disabled={submitting || (tx.status !== 'PENDING' && tx.status !== 'FLAGGED')} variant="secondary" className="w-full justify-center text-xs">STEP-UP</Button>
                <Button onClick={() => submitDecision('MONITOR')} disabled={submitting || (tx.status !== 'PENDING' && tx.status !== 'FLAGGED')} variant="secondary" className="w-full justify-center text-xs bg-slate-800">MONITOR</Button>
              </div>
            </div>
          </Card>
        </div>
        
      </div>
    </motion.div>
  );
}
""",
    "App.tsx": """import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import DashboardLayout from './layouts/DashboardLayout';

import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import DecisionConsole from './pages/DecisionConsole';

const NotFound = () => <div className="p-8 text-center text-slate-400">404 - Page Not Found</div>;

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<LandingPage />} />
        </Route>
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/decision/:transactionId" element={<DecisionConsole />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(frontend_path, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Frontend pages generated successfully.")
