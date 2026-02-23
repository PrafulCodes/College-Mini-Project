"""
Explanation Service - Formats agent recommendations for user-friendly display.

This service converts technical agent outputs into clear, actionable sentences
suitable for frontend display and user communication.
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


def format_recommendations(advice_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert agent outputs into user-friendly formatted recommendations.

    Args:
        advice_list (List[Dict]): List of agent recommendation dictionaries
            Expected fields: type, advice, reason, impact, severity

    Returns:
        Dict[str, Any]: Formatted recommendations for frontend display

    Output Format:
        {
            "summary": "Brief overview of financial health",
            "priority_actions": [
                {
                    "agent": "budget",
                    "action": "Clear action statement",
                    "impact": "Expected benefit",
                    "urgency": "high|medium|low"
                }
            ],
            "detailed_explanations": {
                "budget": "Full explanation text",
                "savings": "Full explanation text",
                ...
            },
            "projections": {
                "3_month_outlook": "Human-readable projection",
                "next_steps": ["Step 1", "Step 2", ...]
            }
        }
    """
    logger.debug(f"Formatting {len(advice_list)} recommendations")

    if not advice_list:
        return {
            "summary": "No financial data provided.",
            "priority_actions": [],
            "detailed_explanations": {},
            "projections": {}
        }

    # Separate by agent type
    advice_by_type = {}
    for advice in advice_list:
        if isinstance(advice, dict):
            agent_type = advice.get("type", "unknown")
            advice_by_type[agent_type] = advice

    # Generate formatted output
    priority_actions = _extract_priority_actions(advice_by_type)
    detailed_explanations = _create_detailed_explanations(advice_by_type)
    summary = _generate_summary(advice_by_type, priority_actions)
    next_steps = _generate_next_steps(advice_by_type)

    logger.info(f"Formatted {len(priority_actions)} priority actions")

    return {
        "summary": summary,
        "priority_actions": priority_actions,
        "detailed_explanations": detailed_explanations,
        "projections": {
            "overview": _generate_projection_overview(advice_by_type),
            "next_steps": next_steps
        }
    }


def _extract_priority_actions(advice_by_type: Dict[str, Dict]) -> List[Dict[str, Any]]:
    """
    Extract high-impact actions from recommendations.

    Returns prioritized list of actionable items sorted by urgency.
    """
    actions = []

    # Budget action
    if "budget" in advice_by_type:
        budget = advice_by_type["budget"]
        if budget.get("severity") in ["high", "medium"]:
            actions.append({
                "agent": "budget",
                "action": budget.get("advice", "Optimize your spending"),
                "impact": budget.get("impact", "Savings potential"),
                "urgency": budget.get("severity", "medium"),
                "icon": "budget"
            })

    # Savings action
    if "savings" in advice_by_type:
        savings = advice_by_type["savings"]
        if savings.get("severity") in ["high", "medium"]:
            actions.append({
                "agent": "savings",
                "action": savings.get("advice", "Build your emergency fund"),
                "impact": savings.get("impact", "Financial security"),
                "urgency": savings.get("severity", "medium"),
                "icon": "savings"
            })

    # Debt action
    if "debt" in advice_by_type:
        debt = advice_by_type["debt"]
        if debt.get("severity") in ["high", "medium"]:
            strategy = debt.get("metrics", {}).get("recommended_strategy", "").upper()
            actions.append({
                "agent": "debt",
                "action": f"Use {strategy} method: {debt.get('advice', 'Optimize debt repayment')}",
                "impact": debt.get("impact", "Interest savings"),
                "urgency": debt.get("severity", "medium"),
                "icon": "debt"
            })

    # Investment action
    if "investment" in advice_by_type:
        investment = advice_by_type["investment"]
        if investment.get("metrics", {}).get("investment_ready"):
            actions.append({
                "agent": "investment",
                "action": f"Start investing: {investment.get('advice', 'Begin investment plan')}",
                "impact": investment.get("impact", "Wealth building"),
                "urgency": "low",
                "icon": "investment"
            })

    # Sort by urgency (high → medium → low)
    urgency_order = {"high": 0, "medium": 1, "low": 2}
    actions.sort(key=lambda x: urgency_order.get(x.get("urgency", "low"), 2))

    return actions


def _create_detailed_explanations(advice_by_type: Dict[str, Dict]) -> Dict[str, str]:
    """
    Create detailed, human-readable explanations for each agent.
    """
    explanations = {}

    if "budget" in advice_by_type:
        budget = advice_by_type["budget"]
        exp_ratio = budget.get("metrics", {}).get("expense_ratio", 0)
        highest_cat = budget.get("metrics", {}).get("highest_category", "")
        explanations["budget"] = (
            f"Your spending is at {exp_ratio*100:.1f}% of your income. "
            f"Your highest category is {highest_cat}. "
            f"{budget.get('advice', 'Consider optimizing your budget.')} "
            f"This could save you {budget.get('impact', 'money')} each month."
        )

    if "savings" in advice_by_type:
        savings = advice_by_type["savings"]
        gap = savings.get("metrics", {}).get("emergency_fund_gap", 0)
        target = savings.get("metrics", {}).get("emergency_fund_target", 0)
        explanations["savings"] = (
            f"Your emergency fund target is {target:,.0f} (3 months of expenses). "
            f"Currently, you have a gap of {gap:,.0f}. "
            f"{savings.get('advice', 'Focus on building your emergency fund first for financial security.')} "
            f"{savings.get('impact', 'This provides essential protection.')}"
        )

    if "debt" in advice_by_type:
        debt = advice_by_type["debt"]
        strategy = debt.get("metrics", {}).get("recommended_strategy", "").upper()
        total_debt = debt.get("metrics", {}).get("total_debt", 0)
        explanations["debt"] = (
            f"Your total debt is {total_debt:,.0f}. "
            f"Recommended strategy: {strategy} method. "
            f"{debt.get('advice', 'Prioritize high-interest debt first.')} "
            f"{debt.get('impact', 'This will reduce your interest burden.')}"
        )

    if "investment" in advice_by_type:
        investment = advice_by_type["investment"]
        ready = investment.get("metrics", {}).get("investment_ready", False)
        status = investment.get("status", "Analysis pending")
        if ready:
            explanations["investment"] = (
                f"You are ready to invest! {investment.get('advice', '')} "
                f"Risk level: {investment.get('metrics', {}).get('risk_level', 'medium')}. "
                f"{investment.get('impact', 'Start building wealth through investments.')}"
            )
        else:
            explanations["investment"] = (
                f"Investment not recommended at this time. Status: {status}. "
                f"{investment.get('advice', 'Focus on emergency fund and debt reduction first.')}"
            )

    if "projection" in advice_by_type:
        projection = advice_by_type["projection"]
        optimized = projection.get("optimized_behavior", {}).get("savings_3m", 0)
        current = projection.get("current_behavior", {}).get("savings_3m", 0)
        difference = optimized - current
        explanations["projection"] = (
            f"By following recommendations, you could save ₹{difference:,.0f} more in 3 months. "
            f"Current trajectory: ₹{current:,.0f} saved. "
            f"Optimized path: ₹{optimized:,.0f} saved."
        )

    return explanations


def _generate_summary(advice_by_type: Dict[str, Dict], actions: List[Dict]) -> str:
    """
    Generate a high-level summary of financial health.
    """
    # Determine overall health based on severities
    severities = []
    for advice in advice_by_type.values():
        severity = advice.get("severity", "low")
        if severity:
            severities.append(severity)

    high_count = severities.count("high")
    medium_count = severities.count("medium")
    low_count = severities.count("low")

    if high_count > 0:
        health_status = "needs immediate attention"
        icon = "warning"
    elif medium_count > 0:
        health_status = "moderately healthy but could improve"
        icon = "attention"
    else:
        health_status = "in good shape"
        icon = "healthy"

    action_count = len([a for a in actions if a.get("urgency") in ["high", "medium"]])

    summary = (
        f"Your financial profile {health_status}. "
        f"We found {action_count} key action(s) that could improve your finances. "
        f"Focus on the priority actions below to optimize your financial health."
    )

    return summary


def _generate_next_steps(advice_by_type: Dict[str, Dict]) -> List[str]:
    """
    Generate prioritized next steps for user action.
    """
    steps = []

    # Priority 1: Emergency fund (if savings is high severity)
    if "savings" in advice_by_type:
        savings = advice_by_type["savings"]
        if savings.get("severity") == "high":
            steps.append("Step 1: Build emergency fund (top priority for financial security)")

    # Priority 2: Reduce debt (if debt is high severity)
    if "debt" in advice_by_type:
        debt = advice_by_type["debt"]
        if debt.get("severity") == "high":
            steps.append("Step 2: Pay off high-interest debt using the recommended strategy")

    # Priority 3: Optimize budget (if budget is high severity)
    if "budget" in advice_by_type:
        budget = advice_by_type["budget"]
        if budget.get("severity") in ["high", "medium"]:
            steps.append("Step 3: Optimize your budget by reducing top expense categories")

    # Priority 4: Invest (if investment ready)
    if "investment" in advice_by_type:
        investment = advice_by_type["investment"]
        if investment.get("metrics", {}).get("investment_ready"):
            steps.append("Step 4: Start investing with recommended asset allocation")

    # Fallback steps if no high actions
    if not steps:
        steps = [
            "Review your financial goals and timeline",
            "Track your spending consistently",
            "Build your emergency fund to 3 months of expenses",
            "Consider starting a regular investment plan",
            "Monitor and adjust your budget quarterly"
        ]

    return steps[:5]  # Limit to 5 steps


def _generate_projection_overview(advice_by_type: Dict[str, Dict]) -> str:
    """
    Generate a readable overview of future projections.
    """
    if "projection" not in advice_by_type:
        return "Projection data not available."

    projection = advice_by_type["projection"]
    current_3m = projection.get("current_behavior", {}).get("savings_3m", 0)
    optimized_3m = projection.get("optimized_behavior", {}).get("savings_3m", 0)
    difference = optimized_3m - current_3m

    if difference > 0:
        overview = (
            f"Over the next 3 months, following your current plan, you would save ₹{current_3m:,.0f}. "
            f"By implementing our recommendations, you could save ₹{optimized_3m:,.0f} instead—"
            f"an additional ₹{difference:,.0f}. This is a {(difference/current_3m)*100:.0f}% improvement if you take action."
        )
    else:
        overview = (
            f"Over the next 3 months, you would save approximately ₹{current_3m:,.0f} "
            f"based on your current financial behavior."
        )

    return overview


def format_single_agent_output(agent_output: Dict[str, Any]) -> Dict[str, str]:
    """
    Format output from a single agent for display.

    Args:
        agent_output (Dict): Single agent output

    Returns:
        Dict: Formatted output with user-friendly text
    """
    agent_type = agent_output.get("type", "unknown")
    advice = agent_output.get("advice", "No advice available")
    reason = agent_output.get("reason", "No reasoning provided")
    impact = agent_output.get("impact", "No impact data")
    severity = agent_output.get("severity", "low")

    # Create user-friendly message
    severity_emoji = {
        "high": "[!] HIGH PRIORITY",
        "medium": "[*] ATTENTION NEEDED",
        "low": "[OK] HEALTHY"
    }.get(severity, "[?] INFO")

    formatted = {
        "agent": agent_type,
        "status": f"{severity_emoji}",
        "title": _get_agent_title(agent_type),
        "action": advice,
        "explanation": reason,
        "benefit": impact,
        "severity": severity
    }

    return formatted


def _get_agent_title(agent_type: str) -> str:
    """Get a friendly title for each agent type."""
    titles = {
        "budget": "Budget Health",
        "savings": "Emergency Fund Status",
        "debt": "Debt Management Strategy",
        "investment": "Investment Readiness",
        "projection": "3-Month Projection"
    }
    return titles.get(agent_type, "Financial Advice")
