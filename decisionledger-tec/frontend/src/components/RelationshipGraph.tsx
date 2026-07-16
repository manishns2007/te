import React, { useCallback, useEffect, useState } from 'react';
import {
  ReactFlow,
  useNodesState,
  useEdgesState,
  Background,
  Controls,
  MiniMap,
  Handle,
  Position,
  MarkerType
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { User, CreditCard, Laptop, Globe, Store, AlertTriangle, FileText } from 'lucide-react';
import { PredictionService } from '../services/api';
import { LoadingSpinner } from './LoadingSpinner';

const iconMap: Record<string, React.ReactNode> = {
  customer: <User size={20} />,
  account: <CreditCard size={20} />,
  device: <Laptop size={20} />,
  ip: <Globe size={20} />,
  merchant: <Store size={20} />,
  alert: <AlertTriangle size={20} />,
  transaction: <FileText size={20} />
};

const colorMap: Record<string, string> = {
  low: 'border-risk-green bg-risk-green/20 text-risk-green',
  medium: 'border-risk-orange bg-risk-orange/20 text-risk-orange',
  high: 'border-risk-red bg-risk-red/20 text-risk-red',
};

// Custom Node Component
const EntityNode = ({ data, selected }: any) => {
  return (
    <div className={`px-4 py-2 shadow-xl rounded-md border-2 bg-slate-900 ${colorMap[data.risk] || 'border-slate-500 text-slate-300'} ${selected ? 'ring-2 ring-primary ring-offset-2 ring-offset-background scale-110' : ''} transition-all duration-200 flex items-center gap-3`}>
      <Handle type="target" position={Position.Top} className="!bg-slate-500" />
      <div className="bg-black/50 p-2 rounded-md">
        {iconMap[data.type] || <FileText size={20} />}
      </div>
      <div>
        <div className="text-xs text-slate-400 uppercase tracking-wider">{data.type}</div>
        <div className="text-sm font-bold whitespace-nowrap">{data.label}</div>
      </div>
      <Handle type="source" position={Position.Bottom} className="!bg-slate-500" />
    </div>
  );
};

const nodeTypes = { entity: EntityNode };

export const RelationshipGraph = ({ transactionId }: { transactionId: string }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedNodeData, setSelectedNodeData] = useState<any>(null);

  useEffect(() => {
    PredictionService.getRelationshipGraph(transactionId).then((data) => {
      // Circular Layout Algorithm
      const centerX = 400;
      const centerY = 300;
      const radius = 250;
      
      const formattedNodes = data.nodes.map((n: any, idx: number) => {
        // Place transaction in center, others in a circle
        const isTxn = n.type === 'transaction' && idx === 0;
        const angle = (idx / (data.nodes.length - 1)) * 2 * Math.PI;
        
        return {
          id: n.id,
          type: 'entity',
          position: {
            x: isTxn ? centerX : centerX + radius * Math.cos(angle),
            y: isTxn ? centerY : centerY + radius * Math.sin(angle),
          },
          data: n,
        };
      });

      const formattedEdges = data.edges.map((e: any) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        animated: true,
        label: e.relationship,
        labelStyle: { fill: '#94a3b8', fontSize: 12, fontWeight: 600 },
        labelBgStyle: { fill: '#0f172a' },
        style: { stroke: '#475569', strokeWidth: 2 },
        markerEnd: { type: MarkerType.ArrowClosed, color: '#475569' },
      }));

      setNodes(formattedNodes);
      setEdges(formattedEdges);
      setLoading(false);
    }).catch((err) => {
      console.error(err);
      setError("Failed to load graph data. Did you restart the backend?");
      setLoading(false);
    });
  }, [transactionId]);

  const onNodeClick = useCallback((_: any, node: any) => {
    setSelectedNodeData(node.data);
  }, []);

  const onPaneClick = useCallback(() => {
    setSelectedNodeData(null);
  }, []);

  if (loading) return <div className="h-[600px] flex items-center justify-center"><LoadingSpinner size={40} /></div>;
  if (error) return <div className="h-[600px] flex items-center justify-center text-risk-red">{error}</div>;

  return (
    <div className="flex h-[700px] w-full rounded-xl overflow-hidden border border-slate-700 bg-slate-900/50">
      <div className="flex-1 relative">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          onPaneClick={onPaneClick}
          nodeTypes={nodeTypes}
          fitView
          className="bg-background"
        >
          <Background color="#334155" gap={16} size={1} />
          <Controls className="bg-slate-800 border-slate-700 fill-white" />
          <MiniMap nodeColor="#475569" maskColor="rgba(15, 23, 42, 0.8)" className="bg-slate-900 border border-slate-700" />
        </ReactFlow>
      </div>

      {/* Right Side Inspector Panel */}
      {selectedNodeData && (
        <div className="w-80 bg-slate-900 border-l border-slate-700 p-6 flex flex-col gap-6 overflow-y-auto">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className={`p-3 rounded-lg ${colorMap[selectedNodeData.risk]} bg-opacity-20`}>
                {iconMap[selectedNodeData.type] || <FileText />}
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">{selectedNodeData.label}</h3>
                <span className="text-xs text-slate-400 uppercase tracking-wider">{selectedNodeData.type}</span>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <p className="text-xs text-slate-500 mb-1">Entity ID</p>
              <p className="text-sm font-mono text-slate-300 break-all bg-black/50 p-2 rounded">{selectedNodeData.id}</p>
            </div>
            
            <div>
              <p className="text-xs text-slate-500 mb-1">Risk Level</p>
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${selectedNodeData.risk === 'high' ? 'bg-risk-red' : selectedNodeData.risk === 'medium' ? 'bg-risk-orange' : 'bg-risk-green'}`} />
                <span className="text-sm font-medium text-slate-200 capitalize">{selectedNodeData.risk} Risk</span>
              </div>
            </div>

            {selectedNodeData.description && (
              <div>
                <p className="text-xs text-slate-500 mb-1">Description</p>
                <p className="text-sm text-slate-300">{selectedNodeData.description}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
