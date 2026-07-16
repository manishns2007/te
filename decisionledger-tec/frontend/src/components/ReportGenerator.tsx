import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Download, X, Bot, CheckCircle } from 'lucide-react';
import { Button } from './Button';
import type { TransactionDetail } from '../types';
import ElectricBorder from './ElectricBorder';

interface ReportGeneratorProps {
  tx: TransactionDetail;
  onClose: () => void;
}

export const ReportGenerator = ({ tx, onClose }: ReportGeneratorProps) => {
  const [isGenerating, setIsGenerating] = useState(true);
  const [displayedText, setDisplayedText] = useState('');
  
  const prob = tx.prediction ? Math.round(tx.prediction.fraud_probability * 100) : 0;
  
  const fullReport = `SUSPICIOUS ACTIVITY REPORT (SAR) - FinCEN Form 111
  
TRANSACTION ID: ${tx.id}
DATE FILED: ${new Date().toLocaleDateString()}
ACCOUNT HOLDER: ${tx.customer_name}
ACCOUNT ID: ${tx.account_id}

--- INCIDENT SUMMARY ---
On ${new Date(tx.timestamp).toLocaleString()}, a transaction of $${tx.amount.toFixed(2)} was initiated to merchant category: ${tx.merchant_category}. 
DecisionLedger TEC flagged this transaction with a High Fraud Probability of ${prob}%.

--- CYBER THREAT TELEMETRY ---
Device Trust Score: ${tx.telemetry?.device_trust_score}
IP Address: ${tx.telemetry?.ip_address}
VPN Detected: ${tx.telemetry?.vpn_detected ? 'YES' : 'NO'}
Impossible Travel: ${tx.telemetry?.impossible_travel ? 'YES' : 'NO'}

--- AI EXPLAINABILITY (SHAP) ---
The XGBoost ensemble model identified the following primary risk vectors driving the fraud prediction:
${tx.prediction?.natural_language_explanation || 'High risk of coordinated fraudulent behavior.'}

--- RECOMMENDED ACTION ---
System highly recommends immediate account freeze and step-up authentication. 
A formal investigation has been automatically queued.`;

  useEffect(() => {
    let currentIndex = 0;
    const interval = setInterval(() => {
      setDisplayedText(fullReport.slice(0, currentIndex));
      currentIndex += 5; // Speed of typing
      if (currentIndex > fullReport.length) {
        clearInterval(interval);
        setIsGenerating(false);
      }
    }, 20);
    return () => clearInterval(interval);
  }, [fullReport]);

  const handleDownload = () => {
    // In a real app, this would generate a PDF. For the demo, we trigger print dialog.
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="bg-slate-900 border border-slate-700 rounded-xl shadow-2xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[85vh]"
      >
        <ElectricBorder
          color="#38bdf8"
          speed={1}
          chaos={0.12}
          borderRadius={12}
          className="w-full h-full"
        >
          <div className="flex flex-col w-full h-full max-h-[85vh]">
            <div className="flex justify-between items-center p-4 border-b border-slate-800 bg-slate-900/50">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-primary/20 rounded-lg text-primary">
                  <Bot size={20} />
                </div>
                <div>
                  <h3 className="text-white font-medium">GenAI Investigation Copilot</h3>
                  <p className="text-xs text-slate-400">Synthesizing compliance report...</p>
                </div>
              </div>
              <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors relative z-10">
                <X size={20} />
              </button>
            </div>

            <div className="p-6 overflow-y-auto flex-1 bg-slate-950 font-mono text-sm text-slate-300 whitespace-pre-wrap leading-relaxed relative z-10">
              {displayedText}
              {isGenerating && <span className="inline-block w-2 h-4 bg-primary ml-1 animate-pulse" />}
            </div>

            <div className="p-4 border-t border-slate-800 bg-slate-900/50 flex justify-between items-center relative z-10">
              <div className="text-xs text-slate-500 flex items-center gap-2">
                {isGenerating ? (
                  <span className="flex items-center gap-2 text-primary animate-pulse">
                    Generating text...
                  </span>
                ) : (
                  <span className="flex items-center gap-2 text-risk-green">
                    <CheckCircle size={14} />
                    Report generation complete
                  </span>
                )}
              </div>
              <Button 
                onClick={handleDownload} 
                disabled={isGenerating}
                variant="primary"
                className="flex items-center gap-2 shadow-lg shadow-primary/20 relative z-20"
              >
                <Download size={16} />
                Export Official SAR
              </Button>
            </div>
          </div>
        </ElectricBorder>
      </motion.div>
    </div>
  );
};
