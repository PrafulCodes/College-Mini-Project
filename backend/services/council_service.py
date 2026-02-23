"""
Council service for synthesizing recommendations into a unified action plan
Orchestrates plan generation from all agent advice
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


def synthesize_plan(advice_dict: Dict[str, str]) -> Dict:
    """
    Synthesize advice from all financial agents into a unified monthly action plan.
    
    Prioritizes recommendations in the following order:
    1. Debt management (highest priority)
    2. Savings strategies
    3. Budget optimization
    4. Investment strategies (lowest priority)
    
    Args:
        advice_dict (Dict[str, str]): Dictionary containing advice from all agents
            Expected keys: "debt_advice", "savings_advice", "budget_advice", "investment_advice"
            
    Returns:
        Dict: Contains "plan" key with list of action items
        
    Example:
        input_advice = {
            "debt_advice": "Focus on paying off credit card debt at 22% interest...",
            "savings_advice": "Save $500/month in emergency fund...",
            "budget_advice": "Reduce discretionary spending by 20%...",
            "investment_advice": "Start with balanced mutual funds..."
        }
        
        output = {
            "plan": [
                "Pay extra towards high-interest debt (Credit Card 22%)",
                "Build emergency fund with $500/month savings",
                "Reduce discretionary spending by 20%",
                "Start investing with balanced funds"
            ]
        }
    """
    
    logger.info("Synthesizing unified action plan from agent advice")
    
    plan = []
    
    # Priority 1: Debt Management
    if "debt_advice" in advice_dict and advice_dict["debt_advice"]:
        debt_action = extract_primary_action(advice_dict["debt_advice"])
        if debt_action:
            plan.append(debt_action)
            logger.debug(f"Added debt action: {debt_action}")
    
    # Priority 2: Savings Strategies
    if "savings_advice" in advice_dict and advice_dict["savings_advice"]:
        savings_action = extract_primary_action(advice_dict["savings_advice"])
        if savings_action:
            plan.append(savings_action)
            logger.debug(f"Added savings action: {savings_action}")
    
    # Priority 3: Budget Optimization
    if "budget_advice" in advice_dict and advice_dict["budget_advice"]:
        budget_action = extract_primary_action(advice_dict["budget_advice"])
        if budget_action:
            plan.append(budget_action)
            logger.debug(f"Added budget action: {budget_action}")
    
    # Priority 4: Investment Strategies
    if "investment_advice" in advice_dict and advice_dict["investment_advice"]:
        investment_action = extract_primary_action(advice_dict["investment_advice"])
        if investment_action:
            plan.append(investment_action)
            logger.debug(f"Added investment action: {investment_action}")
    
    logger.info(f"Generated action plan with {len(plan)} items")
    
    return {
        "plan": plan,
        "priority_order": ["debt", "savings", "budget", "investment"],
        "total_actions": len(plan)
    }


def extract_primary_action(advice_text: str) -> str:
    """
    Extract the primary action item from agent advice text.
    
    Takes the first sentence or primary clause as the action item.
    
    Args:
        advice_text (str): Full advice text from an agent
        
    Returns:
        str: Concise action item (first sentence or primary clause)
        
    Example:
        input: "Your debt-to-income ratio is elevated. Allocate 25-30% of disposable income..."
        output: "Your debt-to-income ratio is elevated"
    """
    
    if not advice_text or not advice_text.strip():
        return ""
    
    # Get first sentence (up to period, but keep it concise)
    sentences = advice_text.split(". ")
    if sentences:
        first_sentence = sentences[0].strip()
        
        # Make it more action-oriented by reformatting if it starts with "Your"
        if first_sentence.startswith("Your "):
            # Convert passive to active where possible
            if "is" in first_sentence:
                # Already a statement, make it more concise
                action = first_sentence
            else:
                action = first_sentence
        else:
            action = first_sentence
        
        # Trim to reasonable length (max 120 chars)
        if len(action) > 120:
            action = action[:117] + "..."
        
        return action
    
    return advice_text[:120] if len(advice_text) > 120 else advice_text


def create_detailed_plan(
    plan_items: List[str],
    financial_summary: Dict,
    user_context: str = ""
) -> Dict:
    """
    Create a detailed action plan with context and metrics.
    
    Args:
        plan_items (List[str]): List of action items from synthesize_plan()
        financial_summary (Dict): Financial summary with metrics
        user_context (str): Additional context about the user (optional)
        
    Returns:
        Dict: Detailed plan with metrics and implementation guidance
        
    Example:
        detailed_plan = create_detailed_plan(
            plan_items=["Pay debt", "Save money"],
            financial_summary={
                "monthly_income": 5000,
                "disposable_income": 1000,
                "total_debt": 5000
            },
            user_context="First-time planner"
        )
    """
    
    logger.info("Creating detailed plan with context and metrics")
    
    # Calculate recommended monthly amounts
    monthly_income = financial_summary.get("monthly_income", 0)
    disposable = financial_summary.get("disposable_income", 0)
    total_debt = financial_summary.get("total_debt", 0)
    
    # Calculate debt payoff timeline (rough estimate)
    payoff_months = total_debt / max(disposable * 0.3, 100) if disposable > 0 else 0
    
    detailed_plan = {
        "summary": {
            "action_count": len(plan_items),
            "monthly_budget_available": round(disposable, 2),
            "estimated_implementation_months": round(payoff_months, 1)
        },
        "actions": plan_items,
        "recommended_allocation": {
            "debt_payment": round(disposable * 0.3, 2) if disposable > 0 else 0,
            "emergency_fund": round(disposable * 0.2, 2) if disposable > 0 else 0,
            "investment": round(disposable * 0.15, 2) if disposable > 0 else 0,
            "remaining_discretionary": round(disposable * 0.35, 2) if disposable > 0 else 0
        },
        "milestones": generate_milestones(plan_items, payoff_months),
        "user_context": user_context if user_context else "General financial planning"
    }
    
    return detailed_plan


def generate_milestones(plan_items: List[str], months_to_completion: float) -> List[Dict]:
    """
    Generate milestone checkpoints for the action plan.
    
    Args:
        plan_items (List[str]): List of action items
        months_to_completion (float): Estimated months to complete plan
        
    Returns:
        List[Dict]: Milestone checkpoints
    """
    
    if not plan_items or months_to_completion <= 0:
        return []
    
    milestones = []
    
    # Month 1: Start action
    milestones.append({
        "month": 1,
        "objective": f"Begin with: {plan_items[0]}" if plan_items else "Start financial plan",
        "metrics": ["Action initiated", "Tracking begins"]
    })
    
    # Month 3: Progress check
    if months_to_completion > 3:
        milestones.append({
            "month": 3,
            "objective": "Review progress and adjust if needed",
            "metrics": ["90-day checkpoint", "Behavior established"]
        })
    
    # Month 6: Mid-plan review
    if months_to_completion > 6:
        milestones.append({
            "month": 6,
            "objective": "Halfway progress evaluation",
            "metrics": ["Half-way milestone", "Momentum check"]
        })
    
    # Final: Plan completion
    final_month = int(months_to_completion)
    if final_month > 6:
        milestones.append({
            "month": final_month,
            "objective": "Plan completion and new goals",
            "metrics": ["Plan complete", "Next phase planning"]
        })
    
    return milestones


def validate_plan(plan: List[str]) -> Dict:
    """
    Validate the generated action plan.
    
    Args:
        plan (List[str]): Action plan to validate
        
    Returns:
        Dict: Validation result with status and issues (if any)
    """
    
    issues = []
    
    if not plan:
        issues.append("Plan is empty")
    
    if len(plan) > 10:
        issues.append("Plan has too many items (>10) - may be overwhelming")
    
    if len(plan) < 1:
        issues.append("Plan has too few items (<1) - update needed")
    
    # Check for duplicate actions
    if len(plan) != len(set(plan)):
        issues.append("Plan contains duplicate actions")
    
    # Check for very long action items
    long_items = [item for item in plan if len(item) > 150]
    if long_items:
        issues.append(f"Found {len(long_items)} action items that are too long (>150 chars)")
    
    return {
        "valid": len(issues) == 0,
        "issue_count": len(issues),
        "issues": issues,
        "action_count": len(plan)
    }
