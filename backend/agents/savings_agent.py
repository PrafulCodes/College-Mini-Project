"""
Savings Agent - Evaluates emergency fund and recommends savings targets.

This agent assesses whether the user has sufficient emergency reserves and
recommends savings goals based on income and expenses.

Output Format:
{
    "type": "savings",
    "advice": "Actionable recommendation",
    "reason": "Explanation of the analysis",
    "metrics": {
        "emergency_fund_target": float,
        "emergency_fund_gap": float,
        "current_savings": float,
        "monthly_savings_target": float,
        "months_to_goal": float
    },
    "severity": "low|medium|high"
}
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def analyze_savings(
    income: float,
    expenses: Dict[str, float],
    current_savings: float = 0
) -> Dict[str, Any]:
    """
    Analyze savings adequacy and recommend savings targets.

    Args:
        income (float): Monthly income in currency units (e.g., ₹)
        expenses (Dict[str, float]): Dictionary of expense categories and amounts
        current_savings (float): Current savings balance (default: 0)

    Returns:
        Dict[str, Any]: Advisory recommendation with metrics and reasoning

    Logic:
        1. Calculate total monthly expenses
        2. Calculate emergency fund target (3 × monthly expenses)
        3. Calculate funding gap
        4. Recommend 20% of income as monthly savings target
        5. Estimate months to reach emergency fund goal
    """
    logger.debug(f"Savings analysis: income={income}, current_savings={current_savings}")
    
    # Validate inputs
    if income <= 0:
        return {
            "type": "savings",
            "advice": "Invalid income provided. Please ensure income is greater than zero.",
            "reason": "Income must be positive to calculate savings targets.",
            "metrics": {
                "emergency_fund_target": 0,
                "emergency_fund_gap": 0,
                "current_savings": current_savings,
                "monthly_savings_target": 0,
                "months_to_goal": None
            },
            "severity": "high"
        }
    
    if not expenses:
        return {
            "type": "savings",
            "advice": "No expense data provided. Savings recommendations cannot be calculated.",
            "reason": "Emergency fund target depends on your monthly expenses.",
            "metrics": {
                "emergency_fund_target": 0,
                "emergency_fund_gap": 0,
                "current_savings": current_savings,
                "monthly_savings_target": income * 0.20,
                "months_to_goal": None
            },
            "severity": "medium"
        }
    
    # Calculate metrics
    total_expenses = sum(expenses.values())
    
    # Emergency fund target: 3 × monthly expenses
    # This covers 3 months of living expenses in case of emergency
    emergency_fund_target = total_expenses * 3
    
    # Calculate funding gap
    emergency_fund_gap = max(0, emergency_fund_target - current_savings)
    
    # Recommended monthly savings: 20% of income
    recommended_savings_rate = 0.20
    monthly_savings_target = income * recommended_savings_rate
    
    # Calculate months to reach goal
    if monthly_savings_target > 0 and emergency_fund_gap > 0:
        months_to_goal = emergency_fund_gap / monthly_savings_target
    else:
        months_to_goal = 0
    
    # Determine severity and advice
    if current_savings >= emergency_fund_target:
        severity = "low"
        advice = (
            f"Excellent! Your savings (₹{current_savings:,.0f}) exceed the emergency fund target (₹{emergency_fund_target:,.0f}). "
            f"You have {current_savings / total_expenses:.1f} months of expenses covered. "
            f"Consider allocating surplus to investments or additional savings goals."
        )
    elif current_savings >= emergency_fund_target * 0.75:
        severity = "low"
        remaining_gap = emergency_fund_gap
        advice = (
            f"You're close to your emergency fund goal! Current savings: ₹{current_savings:,.0f}. "
            f"Target: ₹{emergency_fund_target:,.0f}. "
            f"Save ₹{remaining_gap:,.0f} more to reach the goal. "
            f"At your recommended savings rate of ₹{monthly_savings_target:,.0f}/month, you'll reach it in ~{remaining_gap / monthly_savings_target:.1f} months."
        )
    elif current_savings >= emergency_fund_target * 0.50:
        severity = "medium"
        remaining_gap = emergency_fund_gap
        advice = (
            f"You're building good savings! Current: ₹{current_savings:,.0f} ({current_savings / total_expenses:.1f} months of expenses). "
            f"Emergency fund target: ₹{emergency_fund_target:,.0f} ({3} months of expenses). "
            f"Gap: ₹{remaining_gap:,.0f}. Prioritize saving ₹{monthly_savings_target:,.0f}/month to reach your goal in ~{remaining_gap / monthly_savings_target:.1f} months."
        )
    else:
        severity = "high"
        remaining_gap = emergency_fund_gap
        advice = (
            f"Your emergency fund is insufficient. Current: ₹{current_savings:,.0f} ({current_savings / total_expenses if total_expenses > 0 else 0:.1f} months of expenses). "
            f"Target: ₹{emergency_fund_target:,.0f} (3 months of expenses). "
            f"Prioritize building this fund immediately. Save at least ₹{monthly_savings_target:,.0f}/month (20% of income). "
            f"You'll reach your goal in approximately {remaining_gap / monthly_savings_target if monthly_savings_target > 0 else 0:.1f} months."
        )
    
    reason = (
        f"Emergency fund target is 3 months of expenses: ₹{emergency_fund_target:,.0f}. "
        f"This protects you against job loss or unexpected expenses. "
        f"Recommended savings rate: 20% of income (₹{monthly_savings_target:,.0f}/month). "
        f"Currently, you have {current_savings / total_expenses if total_expenses > 0 else 0:.1f} months of expenses saved."
    )
    
    # Calculate impact
    impact = f"Save ₹{monthly_savings_target:,.0f}/month to reach emergency fund goal in {months_to_goal:.1f} months" if months_to_goal > 0 else "Emergency fund goal achieved"
    
    logger.info(f"Savings analysis complete: severity={severity}, gap={emergency_fund_gap:,.0f}")
    
    return {
        "type": "savings",
        "advice": advice,
        "reason": reason,
        "impact": impact,
        "metrics": {
            "emergency_fund_target": emergency_fund_target,
            "emergency_fund_gap": emergency_fund_gap,
            "current_savings": current_savings,
            "monthly_savings_target": round(monthly_savings_target, 2),
            "months_to_goal": round(months_to_goal, 1) if months_to_goal > 0 else 0,
            "current_coverage_months": round(current_savings / total_expenses, 2) if total_expenses > 0 else 0,
            "potential_monthly_benefit": round(monthly_savings_target, 2)
        },
        "severity": severity
    }
