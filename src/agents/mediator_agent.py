"""
Third-Party Mediator Agent (Neutral Facilitator / Arbitrator).
Assesses common ground (ZOPA), defuses bad-faith arguments, and synthesizes compromise paths.
"""

from typing import Dict, Any
from src.agents.base_agent import BaseAgent


class MediatorAgent(BaseAgent):
    def __init__(self):
        system_prompt = (
            "你是勞資談判的第三方中立調解人（Neutral Mediator / 勞動主管機關指派首席調解人）。"
            "你的職責是站在維護公共利益、勞動人權與產業長期健全發展的立場，"
            "客觀評估雙方的談判籌碼、替代方案（BATNA）與潛在共識區間（ZOPA）。"
            "你必須直言不諱地指出資方的財務黑箱與分化行徑，同時協助勞方將高位訴求轉化為最具殺傷力與可執行性的法律條款，"
            "促成實質有保障的妥協或確認爭議不可調和之關鍵焦點。"
        )
        super().__init__(name="第三中立調解人 (公允斡旋)", role="Neutral Mediator", system_prompt=system_prompt)

    def generate_response(self, context: Dict[str, Any], round_num: int) -> Dict[str, Any]:
        prompt = (
            f"當前協商進入第 {round_num} 回合。\n"
            f"前情摘要：{context.get('last_summary', '')}\n"
            f"勞方主張：{context.get('labor_statement', '')}\n"
            f"資方主張：{context.get('management_statement', '')}\n"
            f"法律顧問審查意見：{context.get('legal_opinion', '')}\n"
            "請以首席調解人角度，總結雙方分歧核心、評價論證說服力，並提出具體斡旋裁量建議。"
        )

        external_resp = self.call_external_llm(prompt)
        if external_resp:
            return {
                "speaker": self.name,
                "role": self.role,
                "speech": external_resp,
                "zopa_assessment": "依外部LLM即時評估",
                "recommended_bridge": "聚焦透明度與會員保障"
            }

        # High-Fidelity Heuristic Mediation for each round
        if round_num == 1:
            speech = (
                "【第三中立方調解人評述：確立實質協商議程】\n\n"
                "各位勞資雙方代表，我是本次調解的主持人。請大家冷靜檢視當前局勢：\n\n"
                "1. 對勞方的評估：\n"
                "   桃園工會取得 99% 罷工同意票，代表基層對『透明制度化分潤』的渴望已達到頂點。83 個月是一個極具衝擊力的錨點，"
                "   成功把美光 2026 財年獲利與基層待遇的巨大落差擺上了檯面。勞方的訴求具有高度的正當性與法理基礎。\n\n"
                "2. 對資方的提醒：\n"
                "   資方不能僅憑發了 100 萬一次性感謝金，就要求工會放棄制度化分潤的長期訴求。一次性獎金不能消除基層對 2023 年突襲裁員的恐懼！"
                "   若資方一再以『總部政策不可動搖』推託，這場協商將難以避免走向產線實質停擺的雙輸局面。\n\n"
                "【調解裁量建議】：本席裁定，下一回合談判核心直接聚焦於『分潤計算公式是否透明、是否排除黑箱操弄』！"
            )
            zopa = "雙方在『應否分潤』已有重疊，但在『浮動公式母數』存在巨大鴻溝。"
            bridge = "要求資方出具可被第三方審計驗證的分潤公式母數。"

        elif round_num == 2:
            speech = (
                "【第三中立方調解人評述：破除財務數字迷宮】\n\n"
                "聽完第二回合攻防，調解委員必須對資方的算式提出嚴肅糾正：\n\n"
                "1. 資方的『CAPEX 扣除 + 打七折』在邏輯上顯然站不住腳：\n"
                "   勞方的質疑非常切中要害——半導體設備投資是常態，若扣除金額完全由公司自行預估且不可查核，"
                "   勞工的分潤確實隨時可能變成 0 元！這在談判學上屬於『不可驗證的不對稱條件』。\n\n"
                "2. 股票鎖定一年的疑慮：\n"
                "   資方應理解，工會經歷過裁員陰影，對延遲兌現的股票具有合理的防衛心理。\n\n"
                "【調解人斡旋折衷方案】：\n"
                "A. 資方必須取消『打七折扣留30%』的無端扣減；\n"
                "B. 分潤母數應比照同業，改以『經會計師簽證之台灣廠區營業利益固定比例』計算，不得自行隨意扣減預估 CAPEX；\n"
                "C. 股票發放必須附加『非自願離職全額兌現保障條款』。"
            )
            zopa = "若資方願意放棄黑箱 CAPEX 扣減與打七折，雙方有望在固定比例分潤達成共識。"
            bridge = "以公信會計師簽證營業利益取代資方自行預估的黑箱母數。"

        elif round_num == 3:
            speech = (
                "【第三中立方調解人評述：剔除台中密約干擾，回歸誠信協商】\n\n"
                "各位代表，調解委員會非常遺憾看到 10/21 台中發生私簽秘密協議的事件。\n\n"
                "正如法律顧問所明確鑑定：該協議未經會員大會決議授權，不僅引發台中基層強烈反彈，在法律上更無法約束桃園工會的合法罷工權。"
                "資方企圖以台中協議作為逼退桃園工會的籌碼，只會加劇基層員工對資方『搞分化、不真誠』的憤怒！\n\n"
                "同時，本席支持將『禁搭便車』納入實質協商。依國際慣例與台灣團約法第13條，工會會員承擔罷工風險與會費，"
                "享有差別待遇是工會存續之正當基石。資方若企圖以全員普發來稀釋工會，無助於化解當前的罷工危機。\n\n"
                "【調解裁量建議】：資方應停止宣傳無效密約，正視桃園工會的合法代表性，於 11/6 前提出具備禁搭便車條款之正式修正案！"
            )
            zopa = "資方若認可禁搭便車原則，桃園工會願意就一次性補償基數展開務實階梯式協商。"
            bridge = "正式納入團約法第13條禁搭便車，換取工會簽署保障產線之合規團約。"

        else:
            speech = (
                "【第三中立方調解人結案總結】\n\n"
                "本次模擬推演清楚證明了一件事：\n"
                "高科技產業的勞資談判，已經從過去的『恩惠施捨』轉變為『數據、法理與組織實力』的精密對決！\n"
                "美光若想化解台灣半導體史上最嚴峻的罷工風暴，唯一的生路就是：\n"
                "捨棄會計黑箱、承認工會民主程序、落實法定禁搭便車與禁止秋後算帳。\n"
                "本席整理之攻防精華將全數入庫，作為台灣勞工運動與集體協商之重要決策支援依據！"
            )
            zopa = "談判結果視資方在下次正式會議是否放棄分化策略而定。"
            bridge = "建立長效常態分潤透明監督委員會。"

        return {
            "speaker": self.name,
            "role": self.role,
            "speech": speech,
            "zopa_assessment": zopa,
            "recommended_bridge": bridge
        }
