"""
Unit tests for LaborBargainLab.
Verifies financial calculator, legal compliance checker, and orchestration engine.
Uses standard library unittest.
"""

import os
import sys
import json
import unittest

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.financial_calculator import FinancialSimulator, MicronQuarterlyInput
from src.models.legal_checker import LegalComplianceChecker
from src.engine.orchestrator import NegotiationOrchestrator
from src.engine.knowledge_extractor import KnowledgeExtractor


class TestLaborBargainLab(unittest.TestCase):
    def test_financial_calculator_capex_zeroing(self):
        inp = MicronQuarterlyInput(
            quarterly_net_profit_twd=500e8,
            estimated_capex_twd=600e8,  # CAPEX > Profit
            total_eligible_headcount=11000,
            union_member_count=4000,
            average_monthly_wage_twd=65000
        )
        res = FinancialSimulator.calculate_management_five_layer_trap(inp)
        self.assertTrue(res["is_pool_zeroed_by_capex"])
        self.assertEqual(res["total_bonus_pool_twd"], 0.0)
        self.assertEqual(res["per_capita_cash_in_hand_twd"], 0.0)

    def test_financial_calculator_retention_discount(self):
        inp = MicronQuarterlyInput(
            quarterly_net_profit_twd=1000e8,
            estimated_capex_twd=500e8,  # Remaining: 500e8
            total_eligible_headcount=11000,
            union_member_count=4000,
            average_monthly_wage_twd=65000,
            retention_discount_rate=0.70
        )
        res = FinancialSimulator.calculate_management_five_layer_trap(inp)
        self.assertFalse(res["is_pool_zeroed_by_capex"])
        self.assertEqual(res["step2_discounted_pool"], 500e8 * 0.70)
        self.assertGreater(res["per_capita_cash_in_hand_twd"], 0)

    def test_legal_compliance_taichung_audit(self):
        audit = LegalComplianceChecker.audit_taichung_pact(
            signed_date="2026-10-21",
            authorized_date="2026-10-22",
            signatories_count=9,
            has_general_assembly_ratification=False,
            has_confidentiality_clause=True,
            has_peace_clause=True
        )
        self.assertFalse(audit["is_valid_cba"])
        self.assertGreaterEqual(audit["risk_score"], 90)
        self.assertTrue(any("民法第 170 條" in v["statute"] for v in audit["violations"]))
        self.assertTrue(any("團體協約法第 8 條" in v["statute"] for v in audit["violations"]))

    def test_legal_compliance_closed_shop(self):
        audit = LegalComplianceChecker.audit_closed_shop_clause(closed_shop_demanded=True)
        self.assertEqual(audit["compliance_status"], "FULLY_LEGAL")
        self.assertIn("團體協約法第 13 條", audit["statute"])

    def test_orchestrator_simulation_flow(self):
        case_file = "data/cases/micron_taiwan_2026.json"
        with open(case_file, "r", encoding="utf-8") as f:
            case_data = json.load(f)

        orchestrator = NegotiationOrchestrator(case_data)
        logs = orchestrator.run_full_simulation(total_rounds=2)

        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[0].round_number, 1)
        self.assertIn("四大法定訴求", logs[0].labor_response["speech"])
        self.assertIn("合規意見", logs[0].legal_advisor_response["speech"])

        tmp_db = "data/arguments_db/test_rebuttals.json"
        extractor = KnowledgeExtractor(db_path=tmp_db)
        entries = extractor.extract_and_save(logs)
        self.assertGreaterEqual(len(entries), 4)
        if os.path.exists(tmp_db):
            os.remove(tmp_db)


if __name__ == "__main__":
    unittest.main()
