"""
Negotiation Orchestrator & State Machine.
Drives the 4-Agent simulation across rounds, tracking state metrics and generating logs.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
import datetime

from src.agents.labor_agent import LaborAgent
from src.agents.management_agent import ManagementAgent
from src.agents.legal_advisor_agent import LegalAdvisorAgent
from src.agents.mediator_agent import MediatorAgent
from src.models.financial_calculator import FinancialSimulator, MicronQuarterlyInput


@dataclass
class NegotiationRoundLog:
    round_number: int
    timestamp: str
    labor_response: Dict[str, Any]
    management_response: Dict[str, Any]
    legal_advisor_response: Dict[str, Any]
    mediator_response: Dict[str, Any]
    tension_level: int       # 1 to 100
    strike_probability: int  # 0 to 100%
    legal_risk_score: int    # 0 to 100


class NegotiationOrchestrator:
    def __init__(self, case_data: Dict[str, Any]):
        self.case_data = case_data
        self.labor_agent = LaborAgent()
        self.management_agent = ManagementAgent()
        self.legal_advisor = LegalAdvisorAgent()
        self.mediator = MediatorAgent()
        
        self.round_logs: List[NegotiationRoundLog] = []
        self.current_state = {
            "tension_level": 75,
            "strike_probability": 85,
            "legal_risk_score": 60,
            "concessions_made_by_management": [],
            "concessions_made_by_labor": []
        }

    def run_full_simulation(self, total_rounds: int = 4) -> List[NegotiationRoundLog]:
        """
        Executes all rounds in sequence.
        """
        last_summary = "桃園工會合法取得99%罷工權；台中9人私簽秘密協約引爆基層怒火；談判桌正式啟動四大訴求與分潤公式攻防。"
        labor_stmt = ""
        mgmt_stmt = ""

        for r in range(1, total_rounds + 1):
            context = {
                "round_num": r,
                "last_summary": last_summary,
                "labor_statement": labor_stmt,
                "management_statement": mgmt_stmt
            }

            # 1. Labor Speaks
            labor_resp = self.labor_agent.generate_response(context, round_num=r)
            labor_stmt = labor_resp["speech"]
            context["labor_statement"] = labor_stmt

            # 2. Management Responds
            mgmt_resp = self.management_agent.generate_response(context, round_num=r)
            mgmt_stmt = mgmt_resp["speech"]
            context["management_statement"] = mgmt_stmt

            # 3. Legal Advisor Audits
            legal_resp = self.legal_advisor.generate_response(context, round_num=r)
            context["legal_opinion"] = legal_resp["speech"]

            # 4. Mediator Assesses & Synthesizes
            med_resp = self.mediator.generate_response(context, round_num=r)

            # Update State Metrics
            if r == 1:
                self.current_state["tension_level"] = 80
                self.current_state["strike_probability"] = 88
                self.current_state["legal_risk_score"] = 65
            elif r == 2:
                self.current_state["tension_level"] = 92
                self.current_state["strike_probability"] = 95
                self.current_state["legal_risk_score"] = 90  # 揭發CAPEX黑箱
            elif r == 3:
                self.current_state["tension_level"] = 96
                self.current_state["strike_probability"] = 99  # 台中密約被判定無權代理
                self.current_state["legal_risk_score"] = 95
            else:
                self.current_state["tension_level"] = 85
                self.current_state["strike_probability"] = 70  # 資方試探讓步
                self.current_state["legal_risk_score"] = 50

            log_entry = NegotiationRoundLog(
                round_number=r,
                timestamp=datetime.datetime.now().isoformat(),
                labor_response=labor_resp,
                management_response=mgmt_resp,
                legal_advisor_response=legal_resp,
                mediator_response=med_resp,
                tension_level=self.current_state["tension_level"],
                strike_probability=self.current_state["strike_probability"],
                legal_risk_score=self.current_state["legal_risk_score"]
            )
            self.round_logs.append(log_entry)

            last_summary = f"第 {r} 回合結束：調解人建議 '{med_resp.get('recommended_bridge', '')}'。"

        return self.round_logs
