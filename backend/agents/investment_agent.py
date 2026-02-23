"""
Investment Agent - Recommends investment strategy based on financial readiness.

This agent assesses whether the user meets prerequisites for investing and
recommends asset allocation based on risk tolerance.

Output Format:
{
    "type": "investment",
    "advice": "Actionable recommendation",
    "reason": "Explanation of the analysis",
    "metrics": {
        "investment_ready": bool,
        "investment_capacity": float,
        "emergency_fund_status": str,
        "debt_status": str,
        "risk_level": "low|medium|high",
        "recommended_allocation": {"category": percentage, ...}
    },
    "severity": "low|medium|high"
}
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


def analyze_investment(
    income: float,
    expenses: Dict[str, float],
    current_savings: float = 0,
    debts: List[Dict[str, Any]] = None,
    risk_tolerance: str = "medium"
) -> Dict[str, Any]:
    """
    Analyze investment readiness and recommend strategy.

    Args:
        income (float): Monthly income in currency units (e.g., ₹)
        expenses (Dict[str, float]): Dictionary of expense categories and amounts
        current_savings (float): Current savings balance (default: 0)
        debts (List[Dict[str, Any]]): List of debts (default: None)
        risk_tolerance (str): User's risk tolerance - "low", "medium", or "high" (default: "medium")

    Returns:
        Dict[str, Any]: Advisory recommendation with metrics and reasoning

    Logic:
        1. Check if emergency fund is built (3x monthly expenses)
        2. Check if high-interest debt exists
        3. If emergency fund insufficient or high-interest debt: avoid investing
        4. If investment ready: recommend allocation based on risk tolerance
            - Low risk: 70% Index Funds, 20% Bonds, 10% Savings
            - Medium risk: 40% Index Funds, 30% Mutual Funds, 20% ETFs, 10% Savings
            - High risk: 30% Index Funds, 30% ETFs, 25% Sectoral Funds, 15% Growth Stocks
    """
    logger.debug(f"Investment analysis: income={income}, risk_tolerance={risk_tolerance}")
    
    # Validate inputs
    if income <= 0:
        return {
            "type": "investment",
            "advice": "Invalid income provided. Cannot assess investment readiness.",
            "reason": "Income must be positive.",
            "metrics": {
                "investment_ready": False,
                "investment_capacity": 0,
                "emergency_fund_status": "unknown",
                "debt_status": "unknown",
                "risk_level": risk_tolerance,
                "recommended_allocation": {}
            },
            "severity": "high"
        }
    
    # Calculate emergency fund status
    total_expenses = sum(expenses.values()) if expenses else 0
    emergency_fund_target = total_expenses * 3
    emergency_fund_met = current_savings >= emergency_fund_target
    
    # Analyze debt situation
    total_debt = 0
    high_interest_debt_amount = 0
    if debts:
        for debt in debts:
            if isinstance(debt, dict) and "amount" in debt:
                amount = debt.get("amount", 0)
                interest_rate = debt.get("interest_rate")
                total_debt += amount
                if interest_rate and interest_rate > 15:
                    high_interest_debt_amount += amount
    
    has_high_interest_debt = high_interest_debt_amount > 0
    
    # Calculate investment capacity (20% of income, minus amounts for savings)
    monthly_savings_need = income * 0.20
    investment_capacity = max(0, monthly_savings_need * 0.75)  # 75% of savings after emergency fund contributions
    
    # Determine investment readiness
    investment_ready = emergency_fund_met and not has_high_interest_debt
    
    # Normalize risk tolerance
    risk_tolerance_lower = risk_tolerance.lower() if risk_tolerance else "medium"
    if risk_tolerance_lower not in ["low", "medium", "high"]:
        risk_tolerance_lower = "medium"
    
    # Generate allocation based on risk tolerance
    if risk_tolerance_lower == "low":
        allocation = {
            "Index Funds": 0.70,
            "Bonds": 0.20,
            "Savings Account": 0.10
        }
        allocation_description = "Conservative: Focus on stable, index-linked funds with bonds for safety."
    elif risk_tolerance_lower == "medium":
        allocation = {
            "Index Funds": 0.40,
            "Mutual Funds": 0.30,
            "ETFs": 0.20,
            "Savings Account": 0.10
        }
        allocation_description = "Balanced: Mix of growth-oriented and stable investments."
    else:  # high
        allocation = {
            "Index Funds": 0.30,
            "ETFs": 0.30,
            "Sectoral Funds": 0.25,
            "Growth Stocks": 0.15
        }
        allocation_description = "Aggressive: Higher growth potential with more volatility."
    
    # Determine severity and advice
    if not emergency_fund_met:
        severity = "high"
        months_to_emergency = (emergency_fund_target - current_savings) / (monthly_savings_need) if monthly_savings_need > 0 else 0
        advice = (
            f"NOT YET INVESTMENT READY. Your emergency fund (₹{current_savings:,.0f}) is below target (₹{emergency_fund_target:,.0f}). "
            f"Build your emergency fund first - it typically takes {months_to_emergency:.1f} months at current savings rate. "
            f"After reaching your 3-month emergency expenses buffer, you can start investing. "
            f"This is crucial financial protection."
        )
        status = "Emergency fund insufficient"
    elif has_high_interest_debt:
        severity = "high"
        advice = (
            f"HOLD ON INVESTMENTS. You have high-interest debt (₹{high_interest_debt_amount:,.0f}) that needs attention first. "
            f"Interest rates >15% will erode your investment gains. "
            f"Clear high-interest debt before investing. After that, you can deploy ₹{investment_capacity:,.0f}/month into investments."
        )
        status = "High-interest debt present"
    else:
        severity = "low"
        advice = (
            f"YOU'RE READY TO INVEST! Emergency fund is secured (₹{current_savings:,.0f}). "
            f"No high-interest debt. Current total debt: ₹{total_debt:,.0f} (manageable). "
            f"Recommended investment capacity: ₹{investment_capacity:,.0f}/month. "
            f"Investment strategy: {allocation_description} "
            f"Suggested allocation: "
        )
        for asset, pct in allocation.items():
            advice += f"{asset} {pct*100:.0f}%, "
        advice = advice.rstrip(", ")
        status = "Investment ready"
    
    reason = (
        f"Investment prerequisites: "
        f"(1) Emergency fund: {'✓' if emergency_fund_met else '✗'} "
        f"(Current: ₹{current_savings:,.0f}, Target: ₹{emergency_fund_target:,.0f}), "
        f"(2) No high-interest debt: {'✓' if not has_high_interest_debt else '✗'} "
        f"(High-interest: ₹{high_interest_debt_amount:,.0f}). "
        f"Risk tolerance: {risk_tolerance_lower}. "
        f"Monthly investment capacity: ₹{investment_capacity:,.0f}."
    )
    
    logger.info(f"Investment analysis complete: ready={investment_ready}, risk={risk_tolerance_lower}")
    
    # Calculate impact
    if investment_ready:
        annual_return_low = investment_capacity * 12 * 0.08  # Conservative 8%
        annual_return_med = investment_capacity * 12 * 0.11  # Moderate 11%
        annual_return_high = investment_capacity * 12 * 0.14  # Aggressive 14%
        
        if risk_tolerance_lower == "low":
            projected_return = annual_return_low
        elif risk_tolerance_lower == "medium":
            projected_return = annual_return_med
        else:
            projected_return = annual_return_high
        
        impact = f"Potential annual return on ₹{investment_capacity * 12:,.0f} investment: ₹{projected_return:,.0f}"
    else:
        impact = "Focus on emergency fund and debt reduction first"
        projected_return = 0
    
    logger.info(f"Investment analysis complete: ready={investment_ready}, risk={risk_tolerance_lower}")
    
    return {
        "type": "investment",
        "advice": advice,
        "reason": reason,
        "impact": impact,
        "metrics": {
            "investment_ready": investment_ready,
            "investment_capacity": round(investment_capacity, 2),
            "emergency_fund_status": f"{'Met' if emergency_fund_met else 'Not Met'} (Current: ₹{current_savings:,.0f}, Target: ₹{emergency_fund_target:,.0f})",
            "debt_status": f"Total: ₹{total_debt:,.0f}, High-interest: ₹{high_interest_debt_amount:,.0f}",
            "risk_level": risk_tolerance_lower,
            "recommended_allocation": allocation,
            "projected_annual_return": round(projected_return, 2) if investment_ready else None
        },
        "severity": severity,
        "status": status
    }
