export interface TelemetryData {
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

export interface ErrorResponse {
  detail: string;
}

export interface GraphNode {
  id: string;
  type: string;
  label: string;
  risk: string;
  description?: string;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  relationship: string;
}

export interface GraphResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
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
