"""
LaborBargainLab - Streamlit Interactive Web Application.
Interactive Strike Negotiation Simulator & Decision Support System.
"""

import streamlit as st
import json
import os
import pandas as pd
import altair as alt

from src.models.financial_calculator import FinancialSimulator, MicronQuarterlyInput
from src.models.legal_checker import LegalComplianceChecker
from src.engine.orchestrator import NegotiationOrchestrator
from src.engine.knowledge_extractor import KnowledgeExtractor

st.set_page_config(
    page_title="LaborBargainLab 罷工協商模擬器",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Case Data
CASE_FILE = "data/cases/micron_taiwan_2026.json"
if os.path.exists(CASE_FILE):
    with open(CASE_FILE, "r", encoding="utf-8") as f:
        case_data = json.load(f)
else:
    case_data = {}

# Custom CSS for styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 800; color: #1e293b; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.1rem; color: #64748b; margin-bottom: 1.5rem; }
    .labor-card { border-left: 5px solid #ef4444; background-color: #fef2f2; padding: 15px; border-radius: 8px; margin-bottom: 12px; }
    .mgmt-card { border-left: 5px solid #3b82f6; background-color: #eff6ff; padding: 15px; border-radius: 8px; margin-bottom: 12px; }
    .legal-card { border-left: 5px solid #f59e0b; background-color: #fffbeb; padding: 15px; border-radius: 8px; margin-bottom: 12px; }
    .med-card { border-left: 5px solid #10b981; background-color: #ecfdf5; padding: 15px; border-radius: 8px; margin-bottom: 12px; }
    .stat-badge { font-size: 0.85rem; padding: 3px 8px; border-radius: 4px; font-weight: 600; margin-right: 5px; }
    .badge-red { background: #fee2e2; color: #991b1b; }
    .badge-blue { background: #dbeafe; color: #1e40af; }
    .badge-gold { background: #fef3c7; color: #92400e; }
    .badge-green { background: #d1fae5; color: #065f46; }
</style>
""", unsafe_allow_html=True)

# Sidebar Information
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=300&q=80", width=250)
    st.markdown("### ⚖️ LaborBargainLab")
    st.markdown("**2026 台灣美光罷工協商模擬器**")
    st.caption("四大角色沙盤推演 × 財務黑箱破解 × 勞動法理合規")
    st.divider()
    st.markdown("#### 📌 核心爭議焦點")
    st.markdown("- 4大訴求 (同業分潤/83個月/禁秋後算帳/禁搭便車)")
    st.markdown("- 桃園廠：99% 投票通過合法罷工")
    st.markdown("- 台中廠：10/21 越權秘密協約風暴")
    st.markdown("- 資方：五重削弱公式 (CAPEX/打七折/定錨/股現半)")
    st.divider()
    st.caption("專案原始碼：GitHub 開源開箱即用")

# Header
st.markdown('<div class="main-header">⚖️ LaborBargainLab — 罷工談判協商模擬器</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">真實案例沙盤推演與決策支援系統：以 2026 台灣美光工會罷工爭議為核心範本</div>', unsafe_allow_html=True)

# Navigation Tabs
tabs = st.tabs([
    "🤖 4-LLM 談判沙盤推演",
    "🧮 財務黑箱與分潤算式破解",
    "📜 法律合規與無權代理診斷",
    "📚 勞方反駁論證庫 (Rebuttals)"
])

# ----------------- TAB 1: 4-LLM SIMULATION -----------------
with tabs[0]:
    st.subheader("🤖 四代理人回合制談判推演 (Labor vs Management vs Legal vs Mediator)")
    st.write("點擊下方按鈕啟動多代理人沙盤演練，即時觀察各方論證攻防、法規警示與罷工機率演化。")

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        start_sim = st.button("🚀 啟動 4 回合全自動推演", type="primary")

    if start_sim or "sim_logs" in st.session_state:
        if start_sim:
            with st.spinner("四大代理人正在深入論辯與法理審查中..."):
                orchestrator = NegotiationOrchestrator(case_data)
                logs = orchestrator.run_full_simulation(total_rounds=4)
                st.session_state["sim_logs"] = logs
                # Save into database
                extractor = KnowledgeExtractor()
                extractor.extract_and_save(logs)
        else:
            logs = st.session_state["sim_logs"]

        st.success("✅ 推演完成！已同步更新至最新談判指標與反駁資料庫。")

        # Metric Cards
        last_log = logs[-1]
        m1, m2, m3 = st.columns(3)
        m1.metric("🔥 當前談判緊繃度", f"{last_log.tension_level} %", delta="高壓對峙", delta_color="inverse")
        m2.metric("⚡ 罷工爆發機率", f"{last_log.strike_probability} %", delta="99%投票法定背書", delta_color="inverse")
        m3.metric("⚖️ 資方法規風險等級", f"{last_log.legal_risk_score} / 100", delta="涉不當勞動行為", delta_color="inverse")

        st.divider()

        # Display Rounds
        for log in logs:
            with st.expander(f"📍 第 {log.round_number} 回合攻防紀錄 (緊繃度: {log.tension_level}% | 罷工機率: {log.strike_probability}%)", expanded=(log.round_number in [2, 3])):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f'<div class="labor-card"><span class="stat-badge badge-red">🔴 勞方發言</span><br><br>{log.labor_response["speech"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="mgmt-card"><span class="stat-badge badge-blue">🔵 資方抗辯</span><br><br>{log.management_response["speech"]}</div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="legal-card"><span class="stat-badge badge-gold">⚖️ 獨立法律顧問合規意見</span><br><br>{log.legal_advisor_response["speech"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="med-card"><span class="stat-badge badge-green">🟢 第三中立調解人斡旋</span><br><br>{log.mediator_response["speech"]}</div>', unsafe_allow_html=True)


# ----------------- TAB 2: FINANCIAL TRAP CALCULATOR -----------------
with tabs[1]:
    st.subheader("🧮 資方『五重削弱公式』vs 勞方『15%稅後分潤』精算比對")
    st.markdown("""
    資方對外宣傳「產線年薪破200萬、工程師近600萬」，但底層算式卻是：
    `獎金池 = (當季淨利 - 下季預估CAPEX) × 70% 扣留打七折 × 100萬定錨基準`，且僅發50%現金、股票鎖定一年！
    """)

    fc1, fc2 = st.columns([1, 1])

    with fc1:
        st.markdown("#### ⚙️ 模擬參數調整")
        quarterly_profit = st.slider("當季稅後淨利 (新台幣 億元)", min_value=100.0, max_value=2000.0, value=600.0, step=50.0)
        est_capex = st.slider("下一季預估資本支出 CAPEX (新台幣 億元)", min_value=0.0, max_value=1500.0, value=500.0, step=25.0)
        headcount = st.number_input("適用員工總人數", value=11000)
        union_members = st.number_input("工會會員人數 (約佔)", value=4000)
        monthly_wage = st.number_input("平均月薪 (新台幣 元)", value=65000)

        calc_input = MicronQuarterlyInput(
            quarterly_net_profit_twd=quarterly_profit * 1e8,
            estimated_capex_twd=est_capex * 1e8,
            total_eligible_headcount=int(headcount),
            union_member_count=int(union_members),
            average_monthly_wage_twd=float(monthly_wage)
        )

        mgmt_res = FinancialSimulator.calculate_management_five_layer_trap(calc_input)
        labor_res = FinancialSimulator.calculate_labor_demand_payout(
            annual_net_profit_twd=quarterly_profit * 4 * 1e8,
            union_member_count=int(union_members),
            average_monthly_wage_twd=float(monthly_wage),
            profit_sharing_ratio=0.15,
            closed_shop=True
        )

    with fc2:
        st.markdown("#### 📊 精算比對結果")
        if mgmt_res.get("is_pool_zeroed_by_capex"):
            st.error("🚨 警告：資方預估 CAPEX 吞噬或等於當季淨利，獎金池直接歸零！員工本季實領 0 元！")
        else:
            k1, k2 = st.columns(2)
            k1.metric("資方方案：本季實拿現金", f"{mgmt_res['per_capita_cash_in_hand_twd']:,.0f} 元", f"約 {mgmt_res['equivalent_months_cash']:.1f} 個月")
            k2.metric("資方方案：鎖一年股票", f"{mgmt_res['per_capita_stock_vesting_1yr_twd']:,.0f} 元", "未滿一年離職歸零")

        st.info(f"💡 【勞方四大訴求方案】（年獲利15%提撥 + 禁搭便車專屬）：\n"
                f"- 工會會員每季等同可領：**{labor_res['quarterly_equivalent_cash']:,.0f} 元**（約等同 **{labor_res['equivalent_months']/4:.1f} 個月**）！\n"
                f"- 全年等同約 **{labor_res['equivalent_months']:.1f} 個月** 實質現金回饋！")

        # Bar chart comparison
        chart_data = pd.DataFrame({
            "方案類型": ["資方實領現金 (本季)", "資方鎖一年股票", "勞方訴求分潤 (單季會員等同)"],
            "發放金額 (元)": [
                mgmt_res.get("per_capita_cash_in_hand_twd", 0),
                mgmt_res.get("per_capita_stock_vesting_1yr_twd", 0),
                labor_res.get("quarterly_equivalent_cash", 0)
            ]
        })
        c = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("方案類型", sort=None),
            y="發放金額 (元)",
            color="方案類型"
        ).properties(height=260)
        st.altair_chart(c)

        st.warning(f"🔍 財務邏輯破綻診斷：\n{mgmt_res['deception_analysis']}")


# ----------------- TAB 3: LEGAL AUDIT -----------------
with tabs[2]:
    st.subheader("📜 法律合規與爭議診斷儀表板")
    st.markdown("依據台灣勞動四法（《勞基法》、《團約法》、《工會法》、《爭議處理法》）對爭議事項進行嚴格法理審查。")

    col_l1, col_l2 = st.columns(2)

    with col_l1:
        st.markdown("#### 1. 台中 10/21 秘密協約適法性診斷器")
        sign_d = st.text_input("簽署日期", value="2026-10-21")
        auth_d = st.text_input("工會內部授權開會日期", value="2026-10-22")
        ratified = st.checkbox("是否已經會員大會或會員代表大會決議追認？", value=False)
        confidential = st.checkbox("是否包含對全體會員隱瞞的保密條款？", value=True)
        peace = st.checkbox("是否包含限制罷工的和平條款？", value=True)

        audit_res = LegalComplianceChecker.audit_taichung_pact(
            signed_date=sign_d,
            authorized_date=auth_d,
            signatories_count=9,
            has_general_assembly_ratification=ratified,
            has_confidentiality_clause=confidential,
            has_peace_clause=peace
        )

        st.metric("協約違法風險評分", f"{audit_res['risk_score']} / 100", delta="極高度無效風險", delta_color="inverse")
        st.error(f"法律定調判定：【{audit_res['legal_status']}】")
        for v in audit_res["violations"]:
            st.markdown(f"- 🔴 **[{v['statute']}]**: {v['finding']}")
        for w in audit_res["warnings"]:
            st.markdown(f"- 🟡 **[{w['statute']}]**: {w['finding']}")

    with col_l2:
        st.markdown("#### 2. 工會訴求與資方行為適法性審查")
        cshop = LegalComplianceChecker.audit_closed_shop_clause(closed_shop_demanded=True)
        st.success(f"✅ **禁搭便車訴求審查** [{cshop['statute']}]\n\n{cshop['finding']}\n\n*對資方反駁武器*：{cshop['counter_to_management']}")

        st.markdown("#### 3. 資方違法不當勞動行為即時偵測")
        issues = LegalComplianceChecker.audit_management_bargaining_conduct(
            refuse_to_provide_capex_details=True,
            threaten_reassignment_or_reprisal=True,
            bypass_union_direct_communication=True
        )
        for issue in issues:
            st.markdown(f"🚨 **{issue['violation']}** ({issue['statute']})\n> {issue['detail']}")


# ----------------- TAB 4: REBUTTALS DB -----------------
with tabs[3]:
    st.subheader("📚 勞方反駁論證資料庫 (Negotiation Talking Points)")
    st.write("已將沙盤推演精華沉澱為結構化卡片，可直接複製提供工會協商幹部作為實戰辯護武器：")

    db_path = "data/arguments_db/rebuttals.json"
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            cards = json.load(f)

        for card in cards:
            with st.container():
                st.markdown(f"### 🛡️ 【{card['category']}】")
                st.markdown(f"**資方謬誤話術**：\n> ❌ *{card['management_fallacy']}*")
                st.markdown(f"**勞方有憑有據反擊**：\n> ✅ **{card['labor_counter_argument']}**")
                st.markdown(f"🔥 **談判桌一擊必殺話術**：`{card['key_talking_point']}`")
                st.caption(f"法理依據：{card['statutory_grounds']} | 殺傷力評分：{card['effectiveness_score']} / 10")
                st.divider()
    else:
        st.info("尚未執行模擬推演，請先至第一分頁點擊『啟動推演』以累積論證資料庫。")

st.markdown("---")
st.caption("LaborBargainLab © 2026. Designed for collective bargaining empowerment and game-theoretic labor research.")
