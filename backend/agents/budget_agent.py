"""
Budget Agent - Analyzes spending patterns and recommends budget optimization.

This agent evaluates whether expenses are within reasonable limits relative to income
and identifies the highest expense categories for potential reduction.

Output Format:
{
    "type": "budget",
    "advice": "Actionable recommendation",
    "reason": "Explanation of the analysis",
    "metrics": {
        "total_expenses": float,
        "expense_ratio": float,
        "highest_category": str,
        "highest_category_amount": float
    },
    "severity": "low|medium|high"
}
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


def analyze_budget(
    income: float,
    expenses: Dict[str, float]
) -> Dict[str, Any]:
    """
    Analyze spending patterns and recommend budget optimization.

    Args:
        income (float): Monthly income in currency units (e.g., ₹)
        expenses (Dict[str, float]): Dictionary of expense categories and amounts
                                    Example: {"food": 5000, "rent": 20000, "utilities": 2000}

    Returns:
        Dict[str, Any]: Advisory recommendation with metrics and reasoning

    Logic:
        1. Calculate total expenses
        2. Calculate expense ratio (expenses / income)
        3. Flag if ratio > 70% (overspending)
        4. Identify highest expense category
        5. Suggest specific reduction targets
    """
    logger.debug(f"Budget analysis: income={income}, expenses={expenses}")
    
    # Validate inputs
    if not expenses:
        return {
            "type": "budget",
            "advice": "No expense data provided. Start tracking expenses to get personalized recommendations.",
            "reason": "Cannot analyze without expense information.",
            "metrics": {
                "total_expenses": 0,
                "expense_ratio": 0,
                "highest_category": None,
                "highest_category_amount": 0
            },
            "severity": "low"
        }
    
    if income <= 0:
        return {
            "type": "budget",
            "advice": "Invalid income provided. Please ensure income is greater than zero.",
            "reason": "Income must be positive to calculate expense ratios.",
            "metrics": {
                "total_expenses": sum(expenses.values()) if expenses else 0,
                "expense_ratio": None,
                "highest_category": None,
                "highest_category_amount": 0
            },
            "severity": "high"
        }
    
    # Calculate metrics
    total_expenses = sum(expenses.values())
    expense_ratio = total_expenses / income
    
    # Find highest expense category
    highest_category = max(expenses.items(), key=lambda x: x[1])
    highest_category_name = highest_category[0]
    highest_category_amount = highest_category[1]
    highest_category_ratio = highest_category_amount / income
    
    # Determine severity and advice
    if expense_ratio > 0.85:
        severity = "high"
        message = f"Your expenses ({expense_ratio*100:.1f}% of income) are significantly high. Immediate action needed."
        reduction_target = total_expenses * 0.20
        advice = (
            f"You're spending ₹{total_expenses:,.0f} against ₹{income:,.0f} income ({expense_ratio*100:.1f}%). "
            f"Reduce {highest_category_name} spending from ₹{highest_category_amount:,.0f} to ₹{highest_category_amount - reduction_target/4:,.0f}. "
            f"Target: Bring total expenses down by ₹{reduction_target:,.0f}."
        )
    elif expense_ratio > 0.70:
        severity = "medium"
        reduction_target = total_expenses * 0.10
        advice = (
            f"Your expenses ({expense_ratio*100:.1f}% of income) are on the higher side. "
            f"Highest category: {highest_category_name} (₹{highest_category_amount:,.0f}, {highest_category_ratio*100:.1f}% of income). "
            f"Consider reducing {highest_category_name} by 10-15% (₹{reduction_target/4*0.75:,.0f}) to optimize budget."
        )
    elif expense_ratio > 0.50:
        severity = "low"
        advice = (
            f"Your expense ratio ({expense_ratio*100:.1f}% of income) is healthy. "
            f"Highest category: {highest_category_name} (₹{highest_category_amount:,.0f}). "
            f"Continue monitoring and look for opportunities to optimize {highest_category_name}."
        )
    else:
        severity = "low"
        advice = (
            f"Excellent budget discipline! Your expenses ({expense_ratio*100:.1f}% of income) are well-controlled. "
            f"Maintain this spending pattern and consider increasing your savings rate."
        )
    
    reason = (
        f"Your total monthly expenses (₹{total_expenses:,.0f}) represent {expense_ratio*100:.1f}% of your income. "
        f"Healthy spending is typically 50-70% of income. "
        f"Your highest expense is {highest_category_name} at ₹{highest_category_amount:,.0f} ({highest_category_ratio*100:.1f}% of income)."
    )
    
    # Calculate potential savings impact
    if expense_ratio > 0.85:
        potential_savings = total_expenses * 0.15
    elif expense_ratio > 0.70:
        potential_savings = total_expenses * 0.10
    elif expense_ratio > 0.50:
        potential_savings = total_expenses * 0.05
    else:
        potential_savings = 0
    
    impact = f"Potential monthly savings of ₹{potential_savings:,.0f}" if potential_savings > 0 else "Maintain current healthy spending"
    
    logger.info(f"Budget analysis complete: severity={severity}, ratio={expense_ratio:.2%}")
    
    return {
        "type": "budget",
        "advice": advice,
        "reason": reason,
        "impact": impact,
        "metrics": {
            "total_expenses": total_expenses,
            "expense_ratio": round(expense_ratio, 4),
            "highest_category": highest_category_name,
            "highest_category_amount": highest_category_amount,
            "highest_category_ratio": round(highest_category_ratio, 4),
            "potential_savings": round(potential_savings, 2)
        },
        "severity": severity
    }
