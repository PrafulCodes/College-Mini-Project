"""
Debt Agent - Analyzes debt portfolio and recommends repayment strategy.

This agent evaluates outstanding debts and recommends either avalanche method
(highest interest first) or snowball method (smallest amount first) based on
available interest rate information.

Output Format:
{
    "type": "debt",
    "advice": "Actionable recommendation",
    "reason": "Explanation of the analysis",
    "metrics": {
        "total_debt": float,
        "debt_count": int,
        "high_interest_debt_flag": bool,
        "high_interest_debt_amount": float,
        "recommended_strategy": "avalanche|snowball",
        "monthly_interest_paid": float
    },
    "severity": "low|medium|high"
}
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


def analyze_debt(
    debts: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Analyze debt portfolio and recommend payoff strategy.

    Args:
        debts (List[Dict[str, Any]]): List of debt dictionaries
            Example: [
                {"name": "Credit Card", "amount": 50000, "interest_rate": 18},
                {"name": "Personal Loan", "amount": 100000, "interest_rate": 12},
                {"name": "Car Loan", "amount": 200000}
            ]
            Each debt should have: amount (required), interest_rate (optional), name (optional)

    Returns:
        Dict[str, Any]: Advisory recommendation with metrics and reasoning

    Logic:
        1. Calculate total debt amount
        2. Identify debts without interest rate information
        3. Flag high-interest debt (>15%)
        4. Recommend avalanche (if rates available) or snowball (if missing)
        5. Calculate monthly interest burden
    """
    logger.debug(f"Debt analysis: {len(debts) if debts else 0} debts")
    
    # Handle no debts case
    if not debts or len(debts) == 0:
        return {
            "type": "debt",
            "advice": "Great news! You have no recorded debts.",
            "reason": "Debt-free status is excellent for financial health.",
            "metrics": {
                "total_debt": 0,
                "debt_count": 0,
                "high_interest_debt_flag": False,
                "high_interest_debt_amount": 0,
                "recommended_strategy": "none",
                "monthly_interest_paid": 0
            },
            "severity": "low"
        }
    
    # Calculate metrics
    total_debt = 0
    debt_with_interest_rates = []
    debt_without_interest_rates = []
    high_interest_debt_amount = 0
    total_monthly_interest = 0
    high_interest_flag = False
    
    for debt in debts:
        if not isinstance(debt, dict) or "amount" not in debt:
            logger.warning(f"Invalid debt entry: {debt}")
            continue
        
        amount = debt.get("amount", 0)
        interest_rate = debt.get("interest_rate")
        name = debt.get("name", f"Debt {len(debt_with_interest_rates) + len(debt_without_interest_rates) + 1}")
        
        total_debt += amount
        
        if interest_rate is not None:
            debt_with_interest_rates.append({
                "name": name,
                "amount": amount,
                "interest_rate": interest_rate
            })
            monthly_interest = (amount * interest_rate) / 12 / 100
            total_monthly_interest += monthly_interest
            
            # Flag high-interest debt (>15%)
            if interest_rate > 15:
                high_interest_debt_amount += amount
                high_interest_flag = True
        else:
            debt_without_interest_rates.append({
                "name": name,
                "amount": amount
            })
    
    # Determine strategy
    if len(debt_with_interest_rates) > 1 or (len(debt_with_interest_rates) > 0):
        recommended_strategy = "avalanche"
        # Sort by interest rate (descending) for avalanche method
        debt_with_interest_rates.sort(key=lambda x: x["interest_rate"], reverse=True)
    else:
        recommended_strategy = "snowball"
        # Sort by amount (ascending) for snowball method
        debt_without_interest_rates.sort(key=lambda x: x["amount"])
        debt_with_interest_rates.sort(key=lambda x: x["amount"])
    
    # Determine severity and advice
    if total_debt == 0:
        severity = "low"
        advice = "Excellent! You have no recorded debts. Focus on building savings and investments."
    elif high_interest_flag:
        severity = "high"
        # Find highest interest debts for prioritization
        highest_interest_debt = debt_with_interest_rates[0] if debt_with_interest_rates else None
        advice = (
            f"Your debt portfolio (₹{total_debt:,.0f}) contains high-interest debt that needs immediate attention. "
            f"Highest priority: {highest_interest_debt['name']} (₹{highest_interest_debt['amount']:,.0f}, {highest_interest_debt['interest_rate']}%). "
            f"High-interest debt ({'>15%'}) totals ₹{high_interest_debt_amount:,.0f}. "
            f"Use the AVALANCHE method: Pay minimums on all debts, then direct extra funds to {highest_interest_debt['name']} to minimize interest. "
            f"You're paying ₹{total_monthly_interest:,.2f}/month in interest alone."
        )
    elif len(debts) > 1:
        severity = "medium"
        if debt_with_interest_rates:
            first_target = debt_with_interest_rates[0]
            strategy_desc = f"AVALANCHE method: Target {first_target['name']} first ({first_target['interest_rate']}% interest)."
        else:
            first_target = debt_without_interest_rates[0]
            strategy_desc = f"SNOWBALL method: Target {first_target['name']} first (₹{first_target['amount']:,.0f}, smallest amount)."
        
        advice = (
            f"You have {len(debts)} debts totaling ₹{total_debt:,.0f}. "
            f"Recommended payoff strategy: {strategy_desc} "
            f"After clearing the first debt, redirect that payment to the next in line. "
            f"This accelerates your path to debt freedom."
        )
    else:
        severity = "medium"
        debt = debts[0]
        amount = debt.get("amount", 0)
        rate = debt.get("interest_rate")
        advice = (
            f"You have one debt: ₹{amount:,.0f}. "
            f"{f'Interest rate: {rate}%. ' if rate else 'Create a payment plan to clear this debt. '}"
            f"Focus on paying this off systematically."
        )
    
    # Build reason
    reason_parts = []
    if total_debt > 0:
        reason_parts.append(f"Total debt: ₹{total_debt:,.0f}")
    if high_interest_flag:
        reason_parts.append(f"High-interest debt (>15%): ₹{high_interest_debt_amount:,.0f}")
    if total_monthly_interest > 0:
        reason_parts.append(f"Monthly interest: ₹{total_monthly_interest:,.2f}")
    if debt_with_interest_rates:
        reason_parts.append("Interest rates available: Using Avalanche strategy")
    if debt_without_interest_rates:
        reason_parts.append("Some debts missing interest rates: Consider Snowball strategy for those")
    
    reason = " | ".join(reason_parts) if reason_parts else "No debt data to analyze."
    
    logger.info(f"Debt analysis complete: severity={severity}, total={total_debt:,.0f}, strategy={recommended_strategy}")
    
    # Calculate impact
    impact = f"Interest savings by prioritizing high-interest debt" if high_interest_flag else "Current debt is manageable"
    if total_monthly_interest > 0:
        monthly_interest_savings = total_monthly_interest * 0.25  # Potential 25% reduction through strategy
        impact = f"Potential monthly interest savings of ₹{monthly_interest_savings:,.2f}"
    
    logger.info(f"Debt analysis complete: severity={severity}, total={total_debt:,.0f}, strategy={recommended_strategy}")
    
    return {
        "type": "debt",
        "advice": advice,
        "reason": reason,
        "impact": impact,
        "metrics": {
            "total_debt": total_debt,
            "debt_count": len(debts),
            "high_interest_debt_flag": high_interest_flag,
            "high_interest_debt_amount": high_interest_debt_amount,
            "recommended_strategy": recommended_strategy,
            "monthly_interest_paid": round(total_monthly_interest, 2),
            "debt_breakdown": {
                "with_interest_rates": len(debt_with_interest_rates),
                "without_interest_rates": len(debt_without_interest_rates)
            },
            "potential_interest_savings": round(total_monthly_interest * 0.25, 2) if total_monthly_interest > 0 else 0
        },
        "severity": severity,
        "prioritized_debts": debt_with_interest_rates + debt_without_interest_rates
    }
