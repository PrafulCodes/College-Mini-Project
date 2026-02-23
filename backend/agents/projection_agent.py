"""
Projection Agent - Generates 3-month financial projections.

This agent creates forward-looking scenarios showing the impact of financial
recommendations and compares current behavior vs. optimized behavior.

Output Format:
{
    "type": "projection",
    "current_behavior": {
        "savings_3m": float,
        "debt_reduction_3m": float,
        "total_available_3m": float
    },
    "optimized_behavior": {
        "savings_3m": float,
        "debt_reduction_3m": float,
        "total_available_3m": float
    },
    "impact": {
        "additional_savings": float,
        "faster_debt_payoff": float,
        "months_to_debt_free": float
    },
    "recommendations_breakdown": {
        "budget_improvement": float,
        "savings_improvement": float
    }
}
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


def generate_three_month_projection(
    income: float,
    expenses: Dict[str, float],
    current_savings: float = 0,
    debts: List[Dict[str, Any]] = None,
    savings_rate: float = 0.20,
    debt_payments: float = 0
) -> Dict[str, Any]:
    """
    Generate 3-month financial projections comparing current vs. optimized behavior.

    Args:
        income (float): Monthly income
        expenses (Dict[str, float]): Current expense categories
        current_savings (float): Current savings balance
        debts (List[Dict], optional): List of debts
        savings_rate (float): Target savings rate (default: 0.20 = 20%)
        debt_payments (float): Current monthly debt payment (default: 0)

    Returns:
        Dict[str, Any]: Projection data with current vs. optimized scenarios

    Logic:
        1. Calculate current monthly surplus (income - expenses - debt payments)
        2. Project current savings after 3 months (no optimization)
        3. Calculate optimized monthly surplus using agent recommendations
        4. Project optimized savings after 3 months
        5. Calculate impact and potential improvements
        6. Estimate months to debt-free status
    """
    logger.debug(f"Projection generation: income={income}, current_savings={current_savings}")

    if income <= 0:
        return {
            "type": "projection",
            "error": "Invalid income provided",
            "current_behavior": {},
            "optimized_behavior": {},
            "impact": {}
        }

    # Calculate total expenses and debt
    total_expenses = sum(expenses.values()) if expenses else 0
    total_debt = sum(d.get("amount", 0) for d in debts) if debts else 0

    # Current behavior scenario
    # Monthly surplus = Income - Expenses - Debt Payments
    current_monthly_surplus = income - total_expenses - debt_payments
    current_monthly_surplus = max(0, current_monthly_surplus)

    # Project 3 months of current behavior
    current_savings_3m = current_savings + (current_monthly_surplus * 3)
    current_debt_reduction_3m = debt_payments * 3

    # Optimized behavior scenario
    # Agent recommendations suggest optimizations:
    # 1. Budget reduction: If expenses > 70%, suggest 10-15% reduction
    # 2. Savings increase: Target 20% of income
    # 3. Debt payment: Increase if high-interest debt exists

    expense_ratio = total_expenses / income if income > 0 else 0
    budget_reduction = 0

    if expense_ratio > 0.85:
        # High overspending: reduce by 15%
        budget_reduction = total_expenses * 0.15
    elif expense_ratio > 0.70:
        # Moderate overspending: reduce by 10%
        budget_reduction = total_expenses * 0.10
    elif expense_ratio > 0.50:
        # Opportunity to optimize: reduce by 5%
        budget_reduction = total_expenses * 0.05

    # Optimized monthly surplus
    optimized_monthly_surplus = income - (total_expenses - budget_reduction) - debt_payments
    optimized_monthly_surplus = max(0, optimized_monthly_surplus)

    # Project 3 months of optimized behavior
    optimized_savings_3m = current_savings + (optimized_monthly_surplus * 3)
    optimized_debt_reduction_3m = debt_payments * 3  # Same debt payment for now

    # Calculate improvements
    additional_savings_3m = optimized_savings_3m - current_savings_3m
    faster_debt_payoff_3m = optimized_debt_reduction_3m - current_debt_reduction_3m

    # Estimate months to debt-free
    months_to_debt_free = 0
    if optimized_monthly_surplus > 0 and total_debt > 0:
        monthly_debt_payoff = optimized_monthly_surplus
        if total_debt > 0:
            months_to_debt_free = total_debt / monthly_debt_payoff
    elif debt_payments > 0 and total_debt > 0:
        months_to_debt_free = total_debt / debt_payments

    # Create projected emergency fund status
    emergency_fund_target = total_expenses * 3
    optimized_savings_after_3m = optimized_savings_3m

    # Determine if emergency fund goal can be met
    months_to_emergency_fund = 0
    if optimized_monthly_surplus > 0:
        emergency_fund_gap = max(0, emergency_fund_target - optimized_savings_after_3m)
        if emergency_fund_gap > 0:
            months_to_emergency_fund = emergency_fund_gap / optimized_monthly_surplus

    logger.info(
        f"Projection complete: additional_savings={additional_savings_3m:,.0f}, "
        f"months_to_debt_free={months_to_debt_free:.1f}"
    )

    return {
        "type": "projection",
        "current_behavior": {
            "monthly_surplus": round(current_monthly_surplus, 2),
            "savings_3m": round(current_savings_3m, 2),
            "debt_reduction_3m": round(current_debt_reduction_3m, 2),
            "total_available_3m": round(current_savings_3m + current_debt_reduction_3m, 2),
            "savings_after_3m": round(current_savings_3m, 2)
        },
        "optimized_behavior": {
            "monthly_surplus": round(optimized_monthly_surplus, 2),
            "savings_3m": round(optimized_savings_3m, 2),
            "debt_reduction_3m": round(optimized_debt_reduction_3m, 2),
            "total_available_3m": round(optimized_savings_3m + optimized_debt_reduction_3m, 2),
            "savings_after_3m": round(optimized_savings_after_3m, 2)
        },
        "impact": {
            "additional_savings_3m": round(additional_savings_3m, 2),
            "faster_debt_payoff_3m": round(faster_debt_payoff_3m, 2),
            "monthly_improvement": round((optimized_monthly_surplus - current_monthly_surplus), 2),
            "budget_reduction_potential": round(budget_reduction, 2),
            "months_to_debt_free": round(months_to_debt_free, 1) if months_to_debt_free > 0 else None,
            "months_to_emergency_fund": round(months_to_emergency_fund, 1) if months_to_emergency_fund > 0 else None
        },
        "summary": {
            "is_improvement_possible": additional_savings_3m > 100,
            "primary_opportunity": (
                "budget_reduction" if budget_reduction > 100 else "increase_savings"
            ),
            "urgency_level": (
                "high" if months_to_debt_free and months_to_debt_free > 120
                else "medium" if months_to_debt_free and months_to_debt_free > 60
                else "low"
            )
        }
    }


def generate_annual_projection(
    income: float,
    expenses: Dict[str, float],
    current_savings: float = 0,
    debts: List[Dict[str, Any]] = None,
    savings_rate: float = 0.20,
    debt_payments: float = 0
) -> Dict[str, Any]:
    """
    Generate 12-month financial projections.

    Args:
        income (float): Monthly income
        expenses (Dict[str, float]): Current expense categories
        current_savings (float): Current savings balance
        debts (List[Dict], optional): List of debts
        savings_rate (float): Target savings rate
        debt_payments (float): Current monthly debt payment

    Returns:
        Dict[str, Any]: Annual projection data
    """
    logger.debug(f"Annual projection generation: income={income}")

    if income <= 0:
        return {
            "type": "projection_annual",
            "error": "Invalid income provided",
            "current_behavior": {},
            "optimized_behavior": {},
            "impact": {}
        }

    # Use 3-month projection as base
    three_month = generate_three_month_projection(
        income, expenses, current_savings, debts, savings_rate, debt_payments
    )

    if "error" in three_month:
        return three_month

    # Scale to 12 months (multiply 3-month by 4)
    current_monthly = three_month["current_behavior"]["monthly_surplus"]
    optimized_monthly = three_month["optimized_behavior"]["monthly_surplus"]

    return {
        "type": "projection_annual",
        "current_behavior": {
            "monthly_surplus": current_monthly,
            "savings_12m": round(current_savings + (current_monthly * 12), 2),
            "debt_reduction_12m": round(sum(d.get("amount", 0) * 0.25 for d in debts) if debts else 0, 2)
        },
        "optimized_behavior": {
            "monthly_surplus": optimized_monthly,
            "savings_12m": round(current_savings + (optimized_monthly * 12), 2),
            "debt_reduction_12m": round(sum(d.get("amount", 0) * 0.25 for d in debts) if debts else 0, 2)
        },
        "impact": {
            "additional_savings_12m": round(
                (current_savings + (optimized_monthly * 12)) - (current_savings + (current_monthly * 12)),
                2
            ),
            "monthly_improvement": round((optimized_monthly - current_monthly), 2)
        }
    }
