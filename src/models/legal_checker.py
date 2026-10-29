"""
Legal Compliance & Validity Checker for Labor Negotiation.
Verifies the statutory compliance of negotiation moves under Taiwanese labor laws.
"""

from typing import Dict, Any, List


class LegalComplianceChecker:
    """
    Checks legal validity and detects employer unfair labor practices.
    """

    @staticmethod
    def audit_taichung_pact(
        signed_date: str,
        authorized_date: str,
        signatories_count: int,
        has_general_assembly_ratification: bool,
        has_confidentiality_clause: bool,
        has_peace_clause: bool
    ) -> Dict[str, Any]:
        """
        審查台中 10/21 秘密協約之法律效力。
        依據：《團體協約法》第8條、《工會法》第26/32條、民法無權代理。
        """
        violations = []
        warnings = []
        is_legally_binding_cba = False

        # 1. 越權代理審查
        if signed_date < authorized_date:
            violations.append({
                "statute": "民法第 170 條 (無權代理) & 工會法第 26 條",
                "severity": "CRITICAL",
                "finding": f"簽署日期 ({signed_date}) 早於工會授權協商日 ({authorized_date})，9 名代表無權於事前簽字，構成越權代理。"
            })

        # 2. 團約法第8條法定成立要件審查
        if not has_general_assembly_ratification:
            violations.append({
                "statute": "團體協約法第 8 條第 1 項、第 2 項",
                "severity": "CRITICAL",
                "finding": "未經會員大會或會員代表大會決議追認，欠缺法定成立要件，在法律上『不具團體協約之法定效力』，僅屬民事一般性協議。"
            })
        else:
            is_legally_binding_cba = True

        # 3. 保密條款與受託義務審查
        if has_confidentiality_clause:
            violations.append({
                "statute": "工會法第 32 條 & 民法第 535 條 (受託人善良管理人注意義務)",
                "severity": "HIGH",
                "finding": "協約內容對委託之工會會員保密，剝奪會員知情權，構成違背工會民主與受託人義務。"
            })

        # 4. 和平條款約束力審查
        if has_peace_clause and not is_legally_binding_cba:
            warnings.append({
                "statute": "勞資爭議處理法第 53 條 & 憲法第 153 條 (勞工生存與爭議權保障)",
                "severity": "HIGH",
                "finding": "因該協議非依法成立之團體協約，其和平條款無法限制桃園工會已依法取得之合法罷工權，對反對會員亦不具法定義務拘束力。"
            })

        return {
            "is_valid_cba": is_legally_binding_cba,
            "legal_status": "一般民事協議 (非正式團體協約)" if not is_legally_binding_cba else "正式團體協約",
            "violations": violations,
            "warnings": warnings,
            "risk_score": 95 if violations else 10,
            "recommendation_for_labor": "立即由理事會或會員大會決議宣告該協議無權代理、自始不生效力，並依法向勞動部申請不當勞動行為裁決。"
        }

    @staticmethod
    def audit_closed_shop_clause(closed_shop_demanded: bool) -> Dict[str, Any]:
        """
        審查『禁搭便車』訴求之適法性。
        依據：《團體協約法》第13條。
        """
        if closed_shop_demanded:
            return {
                "statute": "團體協約法第 13 條",
                "compliance_status": "FULLY_LEGAL",
                "finding": "工會要求禁搭便車完全具備明文法律授權！法律明定雇主得約定不將協約待遇適用於非會員。",
                "counter_to_management": "資方若以『對同仁不能差別待遇』拒絕，屬法盲辯詞。團約法第13條正是為了保障工會團結權而設。"
            }
        return {"compliance_status": "OPEN", "finding": "未要求禁搭便車，將導致非會員無償坐享其成，削弱工會長期凝聚力。"}

    @staticmethod
    def audit_management_bargaining_conduct(
        refuse_to_provide_capex_details: bool,
        threaten_reassignment_or_reprisal: bool,
        bypass_union_direct_communication: bool
    ) -> List[Dict[str, Any]]:
        """
        審查資方在談判過程中的違法與不當勞動行為。
        """
        issues = []
        if refuse_to_provide_capex_details:
            issues.append({
                "statute": "團體協約法第 6 條第 3 項",
                "violation": "違反誠信協商義務",
                "detail": "資方主張分潤需扣除 CAPEX，卻拒絕提供具體資本支出查核細目，視同無正當理由拒絕協商。"
            })
        if threaten_reassignment_or_reprisal:
            issues.append({
                "statute": "工會法第 35 條第 1 項第 1 款、第 3 款",
                "violation": "違法不當勞動行為 (秋後算帳)",
                "detail": "對參與合法罷工投票或抗爭幹部施以調動、降薪或威脅考核，構成違法不當勞動行為，面臨最高法定裁罰與損害賠償。"
            })
        if bypass_union_direct_communication:
            issues.append({
                "statute": "工會法第 35 條第 1 項第 5 款",
                "violation": "支配介入工會運作",
                "detail": "資方繞過工會正常協商管道私簽協議或個別向員工施壓，構成不法支配介入。"
            })
        return issues
