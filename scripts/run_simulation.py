"""
CLI Simulation Runner for LaborBargainLab.
Executes the 4-Agent simulation, displays rich formatted terminal output, and generates reports.
"""

import sys
import os
import json
import argparse

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Ensure UTF-8 output on Windows terminal
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.engine.orchestrator import NegotiationOrchestrator
from src.engine.knowledge_extractor import KnowledgeExtractor
from src.utils.reporter import ReportGenerator


def main():
    parser = argparse.ArgumentParser(description="LaborBargainLab: 罷工談判協商模擬器")
    parser.add_argument("--rounds", type=int, default=4, help="模擬回合數 (預設: 4)")
    parser.add_argument("--report-out", type=str, default="reports/latest_simulation_report.md", help="報告輸出路徑")
    parser.add_argument("--db-out", type=str, default="data/arguments_db/rebuttals.json", help="反駁論證庫路徑")
    args = parser.parse_args()

    case_file = "data/cases/micron_taiwan_2026.json"
    if not os.path.exists(case_file):
        print(f"[錯誤] 找不到案例資料檔: {case_file}")
        sys.exit(1)

    with open(case_file, "r", encoding="utf-8") as f:
        case_data = json.load(f)

    print("=" * 70)
    print("⚖️  LaborBargainLab — 2026 台灣美光罷工協商模擬器")
    print(f"案例：{case_data['title']} ({case_data['industry']})")
    print("四大角色：勞方代表 | 資方代表 | 獨立法律顧問 | 第三中立調解人")
    print("=" * 70)

    orchestrator = NegotiationOrchestrator(case_data)
    logs = orchestrator.run_full_simulation(total_rounds=args.rounds)

    for log in logs:
        print(f"\n{'='*30} 第 {log.round_number} 回合 {'='*30}")
        print(f"🔥 緊繃度: {log.tension_level}% | ⚡ 罷工機率: {log.strike_probability}% | ⚖️ 法律風險: {log.legal_risk_score}%")
        
        print("\n🔴 【勞方主張】:")
        print(log.labor_response["speech"][:300] + "...\n")
        
        print("🔵 【資方抗辯】:")
        print(log.management_response["speech"][:300] + "...\n")
        
        print("⚖️  【法律顧問合規意見】:")
        print(log.legal_advisor_response["speech"][:300] + "...\n")
        
        print("🟢 【第三中立方斡旋】:")
        print(log.mediator_response["speech"][:300] + "...\n")

    # Extract knowledge
    extractor = KnowledgeExtractor(db_path=args.db_out)
    entries = extractor.extract_and_save(logs)
    print(f"\n[知識庫] 成功抽取並儲存 {len(entries)} 筆結構化反駁論證至 {args.db_out}")

    # Generate Report
    report_content = ReportGenerator.generate_markdown_report(logs, output_path=args.report_out)
    print(f"[分析報告] 完整沙盤推演決策報告已生成至: {args.report_out}")
    print("=" * 70)
    print("模擬推演成功結束！")


if __name__ == "__main__":
    main()
