import { PageHeader } from '../components/PageHeader';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { motion } from 'framer-motion';

export default function Settings() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="pb-12">
      <PageHeader title="Platform Settings" subtitle="Configure AI thresholds and system preferences" />
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        <Card className="p-6">
          <h3 className="text-lg font-medium text-white mb-4">Risk Thresholds</h3>
          <div className="space-y-4">
            <div>
              <label className="text-sm text-slate-400 block mb-2">High Risk Threshold (%)</label>
              <input type="range" min="0" max="100" defaultValue="85" className="w-full accent-risk-red" />
              <div className="flex justify-between text-xs text-slate-500 mt-1">
                <span>0%</span><span>85%</span><span>100%</span>
              </div>
            </div>
            <div>
              <label className="text-sm text-slate-400 block mb-2">Medium Risk Threshold (%)</label>
              <input type="range" min="0" max="100" defaultValue="70" className="w-full accent-risk-orange" />
              <div className="flex justify-between text-xs text-slate-500 mt-1">
                <span>0%</span><span>70%</span><span>100%</span>
              </div>
            </div>
          </div>
        </Card>
        
        <Card className="p-6">
          <h3 className="text-lg font-medium text-white mb-4">Model Configuration</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-white">Auto-Freeze High Risk</p>
                <p className="text-xs text-slate-400">Automatically freeze accounts &gt; 95% probability</p>
              </div>
              <input type="checkbox" defaultChecked className="toggle" />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-white">SHAP Explainability</p>
                <p className="text-xs text-slate-400">Generate feature importance for all transactions</p>
              </div>
              <input type="checkbox" defaultChecked className="toggle" />
            </div>
          </div>
        </Card>
        
        <div className="md:col-span-2 flex justify-end">
          <Button variant="primary">Save Configuration</Button>
        </div>
      </div>
    </motion.div>
  );
}
