"""
Simulation Report Generator.
Exports detailed negotiation rounds and decision analysis to Markdown format.
"""

import os
from typing import List, Dict, Any
from src.engine.orchestrator import NegotiationRoundLog


class ReportGenerator:
    @staticmethod
    def generate_markdown_report(logs: List[NegotiationRoundLog], output_path: str) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        lines = [
            "# 2026 台灣美光罷工協商模擬器 — 沙盤推演與決策分析報告",
            "",
            "> 本報告由 `LaborBargainLab` 多代理人系統自動生成，模擬勞方、資方、法律顧問與中立調解人四方攻防。",
            "",
            "---",
            "",
            "## 一、 談判局勢指標走勢",
            "",
            "| 回合 | 焦點爭議 | 談判緊繃度 (Tension) | 罷工爆發機率 (Strike Prob) | 法律合規風險 (Legal Risk) |",
            "| :---: | :--- | :---: | :---: | :---: |"
        ]

        round_topics = [
            "四大訴求開場陳述與83個月定錨",
            "資方五重削弱公式 vs 勞方財務拆解",
            "台中10/21越權密約效力 vs 團約法第8/13條",
            "終局裁量、調解折衷與最後通牒"
        ]

        for i, log in enumerate(logs):
            topic = round_topics[i] if i < len(round_topics) else f"第 {log.round_number} 回合"
            lines.append(f"| 第 {log.round_number} 回合 | {topic} | {log.tension_level}% | {log.strike_probability}% | {log.legal_risk_score}% |")

        lines.extend([
            "",
            "---",
            "",
            "## 二、 逐回合四方發言與法理裁決記錄",
            ""
        ])

        for log in logs:
            lines.extend([
                f"### 第 {log.round_number} 回合攻防記錄",
                "",
                f"#### 🔴 【勞方】{log.labor_response['speaker']}",
                "",
                log.labor_response["speech"],
                "",
                f"*主要攻防點*：{', '.join(log.labor_response.get('core_points', []))}",
                f"*法規引用*：{', '.join(log.labor_response.get('statutory_references', []))}",
                "",
                f"#### 🔵 【資方】{log.management_response['speaker']}",
                "",
                log.management_response["speech"],
                "",
                f"*主要防禦點*：{', '.join(log.management_response.get('core_points', []))}",
                "",
                f"#### ⚖️ 【獨立法律顧問】{log.legal_advisor_response['speaker']}",
                "",
                log.legal_advisor_response["speech"],
                "",
                f"#### 🟢 【第三中立調解人】{log.mediator_response['speaker']}",
                "",
                log.mediator_response["speech"],
                "",
                f"*ZOPA 妥協空間評估*：{log.mediator_response.get('zopa_assessment', 'N/A')}",
                "",
                "---",
                ""
            ])

        lines.extend([
            "## 三、 勞方戰略決策支援總結",
            "",
            "1. **拆解財務黑箱**：堅決拒絕『扣除預估 CAPEX』與『打七折』，主張以會計師簽證營業利益作為公開透明分潤母數；",
            "2. **鎖死團約法第8條**：正式宣告台中 10/21 協議無權代理、自始不生效力，阻止資方利用該協議做輿論壓制；",
            "3. **落實團約法第13條**：堅持禁搭便車，保護參與 10/22 罷工與投票之 99% 會員權益；",
            "4. **防止秋後算帳**：要求於正式團約中明訂違反《工會法》第35條之高額懲罰性違約金條款。",
            ""
        ])

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return content
