"""
Financial Calculator for Labor Negotiation Simulation.
Models both the Micron Management's 5-Layer Formula and the Labor's 15% Net Profit Demand.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MicronQuarterlyInput:
    quarterly_net_profit_twd: float  # 當季稅後淨利 (新台幣)
    estimated_capex_twd: float       # 下一季預估資本支出 (新台幣)
    total_eligible_headcount: int    # 適用總人數
    union_member_count: int          # 工會會員人數
    average_monthly_wage_twd: float  # 員工平均月薪 (新台幣)
    fy26_benchmark_bonus_twd: float = 1000000.0  # 2026 一次性百萬基準
    retention_discount_rate: float = 0.70        # 扣留30% (打七折)
    cash_ratio: float = 0.50                     # 50% 現金
    stock_ratio: float = 0.50                    # 50% 股票 (一年後歸屬)


class FinancialSimulator:
    """
    Simulates negotiation math between Labor and Management.
    """

    @staticmethod
    def calculate_management_five_layer_trap(data: MicronQuarterlyInput) -> Dict[str, Any]:
        """
        資方五重削弱公式推演：
        步驟一：可動用盈餘 = 淨利 - 下一季預估 CAPEX
        步驟二：扣留 30% 現金保留款 (打七折)
        步驟三：對齊 2026 百萬定錨比例
        步驟四：50% 現金 + 50% 鎖一年股票
        步驟五：無禁搭便車，全員雨露均霑
        """
        # 步驟一：扣除 CAPEX
        net_after_capex = data.quarterly_net_profit_twd - data.estimated_capex_twd
        
        # 只要 CAPEX 超過獲利，池子直接歸零
        if net_after_capex <= 0:
            return {
                "step1_net_after_capex": net_after_capex,
                "step2_discounted_pool": 0.0,
                "total_bonus_pool_twd": 0.0,
                "per_capita_total_twd": 0.0,
                "per_capita_cash_in_hand_twd": 0.0,
                "per_capita_stock_vesting_1yr_twd": 0.0,
                "is_pool_zeroed_by_capex": True,
                "deception_analysis": "下一季預估資本支出 (CAPEX) 超過或等於獲利，獎金池直接歸零！員工實領 0 元。"
            }

        # 步驟二：打七折 (扣留 30% 預期外現金)
        discounted_pool = net_after_capex * data.retention_discount_rate

        # 步驟三：以 2026 財年一次性 100 萬作為基準比例定錨
        # 假設資方設定之上限換算係數（若當季表現等於基準季，最高不超過等比上限）
        benchmark_quarterly_cap = data.fy26_benchmark_bonus_twd * data.total_eligible_headcount / 4.0
        final_pool = min(discounted_pool, benchmark_quarterly_cap)

        # 步驟四：全員均分 (不防搭便車)
        per_capita_total = final_pool / data.total_eligible_headcount
        per_capita_cash = per_capita_total * data.cash_ratio
        per_capita_stock = per_capita_total * data.stock_ratio

        # 換算等同月薪月數
        equivalent_months_cash = per_capita_cash / data.average_monthly_wage_twd
        equivalent_months_total = per_capita_total / data.average_monthly_wage_twd

        return {
            "step1_net_after_capex": net_after_capex,
            "step2_discounted_pool": discounted_pool,
            "step3_benchmark_capped_pool": final_pool,
            "total_bonus_pool_twd": final_pool,
            "per_capita_total_twd": per_capita_total,
            "per_capita_cash_in_hand_twd": per_capita_cash,
            "per_capita_stock_vesting_1yr_twd": per_capita_stock,
            "equivalent_months_cash": equivalent_months_cash,
            "equivalent_months_total": equivalent_months_total,
            "is_pool_zeroed_by_capex": False,
            "deception_analysis": (
                f"在扣除預估 CAPEX ({data.estimated_capex_twd/1e8:.1f}億) 並打七折後，"
                f"本季員工實收現金僅 {per_capita_cash:,.0f} 元 (約 {equivalent_months_cash:.1f} 個月)，"
                f"與資方公關宣稱的年薪 200~600 萬相差甚遠。"
            )
        }

    @staticmethod
    def calculate_labor_demand_payout(
        annual_net_profit_twd: float,
        union_member_count: int,
        average_monthly_wage_twd: float,
        profit_sharing_ratio: float = 0.15,
        closed_shop: bool = True
    ) -> Dict[str, Any]:
        """
        勞方四大訴求計算模型：
        1. 稅後淨利 15% 直接提撥為分潤池 (比照台積電/同業公開透明公式，不搞黑箱扣除)
        2. 嚴格禁搭便車 (僅限工會會員分潤)
        3. 全額現金發放，不設一年鎖定期
        """
        bonus_pool = annual_net_profit_twd * profit_sharing_ratio
        
        beneficiary_count = union_member_count if closed_shop else union_member_count * 1.5

        per_capita_annual = bonus_pool / beneficiary_count
        equivalent_months = per_capita_annual / average_monthly_wage_twd

        return {
            "annual_net_profit_twd": annual_net_profit_twd,
            "profit_sharing_ratio_pct": profit_sharing_ratio * 100,
            "total_bonus_pool_twd": bonus_pool,
            "beneficiary_count": beneficiary_count,
            "per_capita_annual_twd": per_capita_annual,
            "equivalent_months": equivalent_months,
            "closed_shop_applied": closed_shop,
            "quarterly_equivalent_cash": per_capita_annual / 4.0
        }
