import { motion } from 'framer-motion';
import { Terminal } from 'lucide-react';

const logLines = [
  { text: '$ analyze-txn --id TXN-982374982', color: 'text-primary font-bold' },
  { text: 'DecisionLedger Telemetry Engine v2.4.1', color: 'text-slate-400' },
  { text: '', color: '' },
  { text: '[→] Parsing transaction parameters...', color: 'text-slate-300' },
  { text: '[✓] Transaction validated | amount=$12,450.00', color: 'text-risk-green' },
  { text: '[→] Correlating cybersecurity telemetry...', color: 'text-slate-300' },
  { text: '[✓] Telemetry loaded | sources=3', color: 'text-risk-green' },
  { text: '[→] Running XGBoost anomaly detection...', color: 'text-slate-300' },
  { text: '[!] Fraud Probability: 94.2% | Threshold: 85.0%', color: 'text-risk-orange' },
  { text: '[→] Extracting SHAP Risk Factors...', color: 'text-slate-300' },
  { text: '    - Impossible Travel (+2.45)', color: 'text-risk-red' },
  { text: '    - VPN Detected (+1.82)', color: 'text-risk-red' },
  { text: '[✓] Action: FREEZE | Prevented Loss: $12,450', color: 'text-primary font-bold' },
];

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.4,
      delayChildren: 0.5
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, x: -10 },
  show: { opacity: 1, x: 0, transition: { type: 'spring' as const, stiffness: 100 } }
};

export default function TerminalAnimation() {
  return (
    <div className="w-full rounded-xl bg-[#09090b] border border-slate-800 shadow-2xl overflow-hidden font-mono text-sm shadow-glow-primary/20">
      <div className="flex items-center justify-between px-4 py-3 bg-[#0f172a] border-b border-slate-800">
        <div className="flex gap-2">
          <div className="w-3 h-3 rounded-full bg-risk-red"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
          <div className="w-3 h-3 rounded-full bg-risk-green"></div>
        </div>
        <div className="flex items-center gap-2 text-slate-500 text-xs">
          <Terminal size={14} />
          <span>soc-analyst@decisionledger:~$</span>
        </div>
      </div>
      <motion.div 
        className="p-5 space-y-1.5"
        variants={containerVariants}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true }}
      >
        {logLines.map((line, i) => (
          <motion.div key={i} variants={itemVariants} className={`min-h-[1.25rem] ${line.color}`}>
            {line.text}
            {i === logLines.length - 1 && (
              <motion.span 
                animate={{ opacity: [1, 0] }} 
                transition={{ repeat: Infinity, duration: 0.8 }}
                className="inline-block w-2 h-4 bg-primary ml-1 align-middle"
              />
            )}
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
