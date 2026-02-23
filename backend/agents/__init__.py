"""
Financial Advisory Agents Package

This package contains rule-based agents that analyze financial data
and provide deterministic, explainable recommendations.

Agents:
- budget_agent: Analyzes spending patterns
- savings_agent: Evaluates emergency funds and savings targets
- debt_agent: Recommends debt repayment strategy
- investment_agent: Suggests investment approach based on readiness
"""

from agents.budget_agent import analyze_budget
from agents.savings_agent import analyze_savings
from agents.debt_agent import analyze_debt
from agents.investment_agent import analyze_investment

__all__ = [
    "analyze_budget",
    "analyze_savings",
    "analyze_debt",
    "analyze_investment"
]
