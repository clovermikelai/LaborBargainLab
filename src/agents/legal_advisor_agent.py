"""
Legal Advisor & Compliance Agent.
Acts as an impartial statutory referee, auditing every argument under Taiwanese labor laws.
"""

from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent
from src.models.legal_checker import LegalComplianceChecker


class LegalAdvisorAgent(BaseAgent):
    def __init__(self):
        system_prompt = (
            "你是勞資談判模擬器中的獨立法律顧問與合規審查委員（Legal & Compliance Advisor）。"
            "你的職責是依據中華民國勞動四法（《勞動基準法》、《團體協約法》、《工會法》、《勞資爭議處理法》）及司法實務裁決，"
            "嚴格審查勞資雙方的每一項主張與行為，出具具備法條依據的審查意見，亮出合規警示燈號（綠燈/黃燈/紅燈），"
            "確保一切協商與爭議程序完全合法、杜絕任何違法與無權代理行為！"
        )
        super().__init__(name="獨立法律顧問 (合規把關)", role="Legal Compliance Advisor", system_prompt=system_prompt)
        self.checker = LegalComplianceChecker()

    def generate_response(self, context: Dict[str, Any], round_num: int) -> Dict[str, Any]:
        prompt = (
            f"當前協商進入第 {round_num} 回合。\n"
            f"前情摘要：{context.get('last_summary', '')}\n"
            f"勞方主張：{context.get('labor_statement', '')}\n"
            f"資方主張：{context.get('management_statement', '')}\n"
            "請以專業勞動法法律顧問身份，出具本回合各方適法性裁決備忘錄，列出法條與紅黃綠燈。"
        )

        external_resp = self.call_external_llm(prompt)
        if external_resp:
            return {
                "speaker": self.name,
                "role": self.role,
                "speech": external_resp,
                "compliance_level": "AUDITED",
                "red_flags": [],
                "statutory_references": ["勞基法第29條", "團約法第6, 8, 13條", "工會法第35條"]
            }

        # High-Fidelity Heuristic Audit for each round
        if round_num == 1:
            speech = (
                "【法律顧問合規備忘錄：程序合法性與訴求適法性審查】\n\n"
                "針對第一回合雙方陳述，本顧問出具法規合規意見如下：\n\n"
                "1. 勞方罷工程序合法性審查【綠燈（完全合法）】：\n"
                "   桃園工會已依法踐行《勞資爭議處理法》第 53 條調解程序，並於調解不成立後，"
                "   依第 54 條由全體會員進行無記名投票，以高達 99% 同意票取得合法罷工權。"
                "   該爭議權受憲法第 153 條及爭議處理法最高度保障，資方不得以任何非法手段阻撓。\n\n"
                "2. 勞方訴求二（15%稅後分潤與83個月）適法性審查【黃燈（適法但屬高階談判標的）】：\n"
                "   依《勞動基準法》第 29 條，公司年度結算有盈餘即負有法定分潤給付義務。"
                "   勞方以同業標準與精算模型提出 15% 稅後分潤，在法律上屬於正當團體協約協商標的（合法爭議事項），非違法索求。\n\n"
                "3. 資方商業機密與預算抗辯審查【黃燈警告】：\n"
                "   資方以總部財務紀律為由拒絕探討同業標準，提醒資方注意：《團體協約法》第 6 條第 1 項明定雙方負有誠信協商義務，"
                "   若一味以『總部政策』為由消極排斥實質協商，恐構成無正當理由拒絕協商之疑慮。"
            )
            red_flags = ["資方若消極拒絕實質協商有違反團約法第6條誠信義務之虞"]
            statutes = ["勞資爭議處理法第53, 54條", "勞動基準法第29條", "團體協約法第6條"]

        elif round_num == 2:
            speech = (
                "【法律顧問合規備忘錄：分潤算式與誠信協商審查】\n\n"
                "針對資方提出之『扣除預估 CAPEX + 打七折 + 100萬定錨 + 股現各半』公式，審查意見如下：\n\n"
                "1. 分潤母數扣除 CAPEX 之查核權【重大紅燈（涉嫌違反誠信協商）】：\n"
                "   依《團體協約法》第 6 條第 3 項：『拒絕提供進行協商所必要之資料者，視為無正當理由拒絕協商』。"
                "   資方若要以『下一季預估 CAPEX』作為扣除項，依法律規定，資方**必須向工會公開該預估金額之具體明細、採購合約與核算依據**！"
                "   若資方將 CAPEX 列為黑箱不予查核，致使獎金池可被單方面操弄歸零，在法律上構成欺罔性協商，無法被認定為履行誠信協商義務。\n\n"
                "2. 扣留 30% 預期外現金保留款【黃燈（欠缺法定正當理由）】：\n"
                "   在已預先提列資本支出之情況下，資方無端追加打七折，缺乏客觀財務指引支持，勞方要求剔除此重複扣除項完全合情合理合法。\n\n"
                "3. 股票鎖定一年期與裁員風險【黃燈提醒】：\n"
                "   依民法誠信原則與勞基法工資保護意旨，若協議中未明訂『非自願離職、資遣或不可抗力身心離退時，已累積之未歸屬股票應全數折現發還』，"
                "   將構成權利義務顯失公平條款（民法第 247-1 條），有被法院宣告無效之重大風險。"
            )
            red_flags = ["未提供CAPEX明細構成團約法第6條第3項違法", "股票鎖定未明訂非自願離職折現恐違反民法顯失公平"]
            statutes = ["團體協約法第6條第3項", "勞基法第26/29條", "民法第247-1條"]

        elif round_num == 3:
            audit = self.checker.audit_taichung_pact(
                signed_date="2026-10-21",
                authorized_date="2026-10-22",
                signatories_count=9,
                has_general_assembly_ratification=False,
                has_confidentiality_clause=True,
                has_peace_clause=True
            )
            speech = (
                "【法律顧問重大警示：台中 10/21 協約之效力否定與禁搭便車審查】\n\n"
                "本顧問正式就資方所提『台中已簽署協議』出具司法效力鑑定：\n\n"
                "1. 台中協議在法律上【不具團體協約效力（紅燈警示）】：\n"
                "   依《團體協約法》第 8 條第 1 項，簽訂團體協約必須經『會員大會或會員代表大會決議』或『章程規定程序』。"
                "   9 名代表受委託之授權日為 10/22，其提前於 10/21 私簽且未經全體會員大會追認，屬於民法第 170 條之**無權代理**！"
                "   勞動部亦已定調其僅為一般民事協議，非團約法之團體協約。因此：\n"
                "   (1) 該協議之『三年和平條款』對桃園工會完全不生效力；\n"
                "   (2) 台中工會全體會員有權召開大會否決並撤銷該越權協議！\n\n"
                "2. 禁搭便車條款之適法性【綠燈（完全受法律授權）】：\n"
                "   《團體協約法》第 13 條明文賦予工會約定『雇主不得將本協約所約定之勞動條件，適用於非該工會會員』之合法權限。"
                "   資方以『不能差別待遇』拒絕，在勞動法上屬於重大法律認知錯誤。禁搭便車是法定保障工會團結權的核心機制！\n\n"
                "3. 資方分化兩廠與秋後算帳風險【重度紅燈警告】：\n"
                "   資方若利用無效協議施壓桃園會員，或對罷工幹部採取任何形式之懲戒，立即構成《工會法》第 35 條第 1 項各款之不當勞動行為，"
                "   裁決委員會可命令回復原狀並處以重罰！"
            )
            red_flags = ["台中10/21協議違反團約法第8條屬無權代理", "資方反對禁搭便車違背團約法第13條", "任何秋後算帳均屬違反工會法第35條違法行為"]
            statutes = ["團體協約法第8, 13條", "工會法第35條", "民法第170條"]

        else:
            speech = (
                "【法律顧問最終結案鑑定】\n\n"
                "總結法律立場：\n"
                "1. 桃園工會罷工權完全合法，隨時可依法行使；\n"
                "2. 任何合法的終局協議，必須符合：\n"
                "   (A) 分潤公式具備查核透明度，不得設黑箱 CAPEX 條款（團約法第6條）；\n"
                "   (B) 納入法定禁搭便車機制（團約法第13條）；\n"
                "   (C) 白紙黑字明訂禁止秋後算帳罰則（工會法第35條）；\n"
                "   (D) 必須依法送交各工會全體會員（代表）大會正式決議追認（團約法第8條），方具法律約束力。"
            )
            red_flags = []
            statutes = ["團體協約法第6, 8, 13條", "工會法第35條"]

        return {
            "speaker": self.name,
            "role": self.role,
            "speech": speech,
            "compliance_level": "RED_ALERT" if red_flags else "CLEAR",
            "red_flags": red_flags,
            "statutory_references": statutes
        }
