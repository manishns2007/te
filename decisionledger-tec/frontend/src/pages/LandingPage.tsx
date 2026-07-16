import { useRef } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Activity, Shield, Zap, BarChart3, Database } from 'lucide-react';
import { Card } from '../components/Card';
import { StatusChip } from '../components/StatusChip';
import VariableProximity from '../components/VariableProximity';
import Particles from '../components/Particles';
import TerminalAnimation from '../components/TerminalAnimation';

export default function LandingPage() {
  const containerRef = useRef<HTMLDivElement>(null);

  return (
    <div className="min-h-screen bg-background overflow-hidden relative" ref={containerRef}>
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <Particles
          particleColors={["#ffffff", "#38bdf8", "#a855f7"]}
          particleCount={250}
          particleSpread={10}
          speed={0.1}
          particleBaseSize={100}
          moveParticlesOnHover={false}
          alphaParticles={false}
          disableRotation={false}
          className="w-full h-full"
        />
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/5 blur-[120px] pointer-events-none" />
        <div className="absolute top-[20%] right-[-5%] w-[30%] h-[30%] rounded-full bg-secondary/5 blur-[120px] pointer-events-none" />
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
              <VariableProximity
                label="AI-Powered Banking Fraud"
                fromFontVariationSettings="'wght' 400, 'opsz' 9"
                toFontVariationSettings="'wght' 900, 'opsz' 40"
                containerRef={containerRef}
                radius={200}
                falloff="linear"
              />
              <br/>
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
              <a href="#architecture" className="px-6 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-medium transition-colors border border-slate-700">
                View Architecture
              </a>
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
             <TerminalAnimation />
          </motion.div>

        </div>
        
        <div id="architecture" className="mt-32 pb-20">
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
        
        {/* Roadmap Section */}
        <div className="mt-20 pb-32">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">Product Roadmap</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">The next generation of autonomous SOC capabilities, currently in development.</p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {[
              { title: "Automated SAR Generator", desc: "Instant, compliance-ready Suspicious Activity Report generation using Gemini." },
              { title: "AI Investigator Chat", desc: "Context-aware chatbot to query transaction telemetry and SHAP values in plain English." },
              { title: "Natural Language Rule Engine", desc: "Create complex fraud detection rules simply by typing what you want the engine to catch." },
              { title: "Smart Action Recommendations", desc: "Dynamic mitigation steps (e.g., forced password resets) based on real-time threat intelligence." }
            ].map((feature, i) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="relative group"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-secondary/20 rounded-xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <Card className="relative p-6 bg-surface/80 border-slate-800 h-full backdrop-blur-xl hover:border-slate-600 transition-colors">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-white font-medium">{feature.title}</h3>
                    <span className="text-[10px] uppercase tracking-wider bg-slate-800 text-slate-400 px-2 py-1 rounded font-semibold">Coming Soon</span>
                  </div>
                  <p className="text-slate-400 text-sm leading-relaxed">{feature.desc}</p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
