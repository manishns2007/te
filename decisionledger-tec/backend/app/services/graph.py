from sqlalchemy.orm import Session
from app.schemas.graph_schemas import GraphResponse, GraphNode, GraphEdge
from app.models.all_models import Transaction, TelemetryData
import hashlib

class GraphService:
    @staticmethod
    def get_relationship_graph(db: Session, transaction_id: str) -> GraphResponse:
        # Fetch the root transaction
        tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not tx:
            return GraphResponse(nodes=[], edges=[])
            
        telemetry = db.query(TelemetryData).filter(TelemetryData.transaction_id == transaction_id).first()

        nodes = []
        edges = []

        # 1. Root Transaction Node
        nodes.append(GraphNode(
            id=tx.id,
            type="transaction",
            label=f"TXN: ${tx.amount:.2f}",
            risk="high" if getattr(tx, "status", "") == "FLAGGED" else "medium",
            description=f"Transaction to {tx.merchant_category}"
        ))

        # 2. Customer Node
        customer_id = f"CUST-{hashlib.md5(tx.customer_name.encode()).hexdigest()[:8]}"
        nodes.append(GraphNode(
            id=customer_id,
            type="customer",
            label=tx.customer_name,
            risk="low",
            description="Primary Account Holder"
        ))
        edges.append(GraphEdge(id=f"e_{customer_id}_{tx.id}", source=customer_id, target=tx.id, relationship="performed"))

        # 3. Account Node
        nodes.append(GraphNode(
            id=tx.account_id,
            type="account",
            label=f"ACC: {tx.account_id}",
            risk="low",
            description="Checking Account"
        ))
        edges.append(GraphEdge(id=f"e_{customer_id}_{tx.account_id}", source=customer_id, target=tx.account_id, relationship="owns"))
        edges.append(GraphEdge(id=f"e_{tx.id}_{tx.account_id}", source=tx.id, target=tx.account_id, relationship="drawn_from"))

        # 4. Merchant Node
        merchant_id = f"MERCH-{hashlib.md5(tx.merchant_category.encode()).hexdigest()[:6]}"
        nodes.append(GraphNode(
            id=merchant_id,
            type="merchant",
            label=tx.merchant_category,
            risk="medium",
            description="Merchant Category"
        ))
        edges.append(GraphEdge(id=f"e_{tx.id}_{merchant_id}", source=tx.id, target=merchant_id, relationship="paid_to"))

        # 5. Telemetry Nodes
        if telemetry:
            # Device Node
            nodes.append(GraphNode(
                id=telemetry.device_fingerprint,
                type="device",
                label=f"Device: {telemetry.device_fingerprint[:8]}",
                risk="high" if telemetry.device_trust_score < 50 else "low",
                description=f"Trust Score: {telemetry.device_trust_score}"
            ))
            edges.append(GraphEdge(id=f"e_{tx.id}_{telemetry.device_fingerprint}", source=tx.id, target=telemetry.device_fingerprint, relationship="used"))

            # IP Address Node
            nodes.append(GraphNode(
                id=telemetry.ip_address,
                type="ip",
                label=f"IP: {telemetry.ip_address}",
                risk="high" if telemetry.vpn_detected or telemetry.impossible_travel else "low",
                description=f"Reputation: {telemetry.ip_reputation}"
            ))
            edges.append(GraphEdge(id=f"e_{telemetry.device_fingerprint}_{telemetry.ip_address}", source=telemetry.device_fingerprint, target=telemetry.ip_address, relationship="connected_to"))

            # Simulated past fraudulent transaction linked by IP
            if telemetry.impossible_travel or telemetry.vpn_detected:
                past_tx_id = f"TXN-PAST-{hashlib.md5(telemetry.ip_address.encode()).hexdigest()[:6]}"
                nodes.append(GraphNode(
                    id=past_tx_id,
                    type="transaction",
                    label="Past Fraud TXN",
                    risk="high",
                    description="Known fraudulent transaction"
                ))
                edges.append(GraphEdge(id=f"e_{past_tx_id}_{telemetry.ip_address}", source=past_tx_id, target=telemetry.ip_address, relationship="shares_ip"))

                # Alert Node
                nodes.append(GraphNode(
                    id=f"ALERT-{past_tx_id}",
                    type="alert",
                    label="Fraud Ring Alert",
                    risk="high",
                    description="Shared infrastructure detected"
                ))
                edges.append(GraphEdge(id=f"e_{past_tx_id}_alert", source=past_tx_id, target=f"ALERT-{past_tx_id}", relationship="triggered"))

        return GraphResponse(nodes=nodes, edges=edges)
