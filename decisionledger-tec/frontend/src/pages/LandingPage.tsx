import { Link } from 'react-router-dom';
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
