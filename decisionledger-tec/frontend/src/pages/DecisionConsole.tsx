import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { TransactionService, DecisionService, PredictionService } from '../services/api';
import type { TransactionDetail } from '../types';
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
  if (prob > 50) { riskColor = 'text-risk-yellow'; }
  if (prob > 70) { riskColor = 'text-risk-orange'; }
  if (prob > 85) { riskColor = 'text-risk-red'; }

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
        <PageHeader title="Transaction Investigation" subtitle={tx.id} />
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
                <p className="text-2xl font-bold text-white">${tx.amount.toFixed(2)}</p>
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
                <RefreshCw size={14} className={`mr-2 ${repredicting ? 'animate-spin' : ''}`} />
                Run AI Again
              </Button>
            </div>
            
            <h3 className="text-slate-300 font-medium mb-8 uppercase text-xs tracking-wider">AI Risk Analysis</h3>
            
            <div className="flex flex-col items-center justify-center mb-8">
              <div className="relative w-48 h-48 flex items-center justify-center">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="45" fill="none" stroke="#334155" strokeWidth="10" />
                  <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" strokeWidth="10" strokeDasharray="283" strokeDashoffset={283 - (283 * prob) / 100} className={`${riskColor} transition-all duration-1000 ease-out`} />
                </svg>
                <div className="absolute flex flex-col items-center justify-center">
                  <span className={`text-4xl font-bold ${riskColor}`}>{prob}%</span>
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
                <p className="text-lg text-risk-green">${pred?.expected_prevented_loss?.toLocaleString()}</p>
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
                      <div style={{ width: `${Math.min(Math.abs(val)*20, 100)}%` }} className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${val > 0 ? 'bg-risk-red' : 'bg-risk-green'}`}></div>
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
                <div className={`p-3 rounded border flex items-start gap-3 ${tel.impossible_travel ? 'bg-risk-red/10 border-risk-red/30 text-risk-red' : 'bg-slate-800/50 border-slate-700 text-slate-400'}`}>
                  <AlertTriangle size={16} className="mt-0.5 shrink-0" />
                  <div>
                    <p className="text-sm font-medium">Impossible Travel</p>
                    <p className="text-xs opacity-80">{tel.impossible_travel ? 'Detected in last 24h' : 'Normal pattern'}</p>
                  </div>
                </div>
                
                <div className={`p-3 rounded border flex items-start gap-3 ${tel.vpn_detected ? 'bg-risk-orange/10 border-risk-orange/30 text-risk-orange' : 'bg-slate-800/50 border-slate-700 text-slate-400'}`}>
                  <ShieldAlert size={16} className="mt-0.5 shrink-0" />
                  <div>
                    <p className="text-sm font-medium">VPN/Proxy</p>
                    <p className="text-xs opacity-80">{tel.vpn_detected ? 'Anonymizer detected' : 'Clean IP'}</p>
                  </div>
                </div>

                <div className={`p-3 rounded border flex items-start gap-3 ${tel.endpoint_alert || tel.powershell_execution ? 'bg-risk-red/10 border-risk-red/30 text-risk-red' : 'bg-slate-800/50 border-slate-700 text-slate-400'}`}>
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
