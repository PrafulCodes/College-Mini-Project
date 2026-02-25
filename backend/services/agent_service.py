"""
Agent service layer for financial recommendations
Contains business logic for generating financial advice
"""
from typing import Any
from typing import List, Dict, Tuple
from schemas.financial import (
    FinancialInputRequest,
    FinancialSummary,
    Recommendation,
    DebtItem
)
import logging

logger = logging.getLogger(__name__)



from agents.projection_agent import generate_three_month_projection
from services.explanation_service import format_recommendations

class FinancialAgent:
    """
    Main agent for financial analysis
    Orchestrates individual agent services
    """

    def __init__(self):
        self.budget_agent = BudgetAgent()
        self.savings_agent = SavingsAgent()
        self.debt_agent = DebtAgent()
        self.investment_agent = InvestmentAgent()

    def analyze_financial_situation(
        self,
        financial_input: FinancialInputRequest
    ) -> Dict:
        """
        Main analysis orchestrator
        Calls all agent services and compiles results
        """
        # Calculate financial summary
        summary = self._calculate_summary(financial_input)

        # Get advice from each agent (full dict outputs)
        budget_output = self.budget_agent.analyze_budget(
            financial_input.monthly_income,
            self._dict_from_expenses(financial_input.expenses)
        )
        savings_output = self.savings_agent.analyze_savings(
            financial_input.monthly_income,
            self._dict_from_expenses(financial_input.expenses),
            getattr(financial_input, 'current_savings', 0)
        )
        debt_output = self.debt_agent.analyze_debt(
            [d.dict() if hasattr(d, 'dict') else d for d in financial_input.debts]
        )
        investment_output = self.investment_agent.analyze_investment(
            financial_input.monthly_income,
            self._dict_from_expenses(financial_input.expenses),
            getattr(financial_input, 'current_savings', 0),
            [d.dict() if hasattr(d, 'dict') else d for d in financial_input.debts],
            getattr(financial_input, 'risk_tolerance', 'medium')
        )

        # Projection agent
        projection_output = generate_three_month_projection(
            income=financial_input.monthly_income,
            expenses=self._dict_from_expenses(financial_input.expenses),
            current_savings=getattr(financial_input, "current_savings", 0),
            debts=[d.dict() if hasattr(d, "dict") else d for d in financial_input.debts],
            savings_rate=summary.savings_rate
        )
        projection_output["type"] = "projection"

        # Compile all agent outputs for explanation formatter
        agent_outputs = [budget_output, savings_output, debt_output, investment_output, projection_output]
        explanations = format_recommendations(agent_outputs)

        # Compile recommendations (legacy, for backward compatibility)
        recommendations = self._compile_recommendations(
            financial_input,
            budget_output.get("advice", ""),
            savings_output.get("advice", ""),
            debt_output.get("advice", ""),
            investment_output.get("advice", "")
        )

        return {
            "summary": summary,
            "expenses": self._dict_from_expenses(financial_input.expenses),
            "debts": financial_input.debts,
            "recommendations": recommendations,
            "budget_advice": budget_output,
            "savings_advice": savings_output,
            "debt_advice": debt_output,
            "investment_advice": investment_output,
            "projection": projection_output,
            "explanations": explanations
        }

    @staticmethod
    def _calculate_summary(financial_input: FinancialInputRequest) -> FinancialSummary:
        """Calculate financial summary metrics"""
        total_expenses = sum(expense.amount for expense in financial_input.expenses)
        disposable_income = financial_input.monthly_income - total_expenses
        total_debt = sum(debt.amount for debt in financial_input.debts)
        savings_rate = (disposable_income / financial_input.monthly_income) if financial_input.monthly_income > 0 else 0
        debt_to_income = (total_debt / financial_input.monthly_income) if financial_input.monthly_income > 0 else 0

        return FinancialSummary(
            monthly_income=round(financial_input.monthly_income, 2),
            total_expenses=round(total_expenses, 2),
            disposable_income=round(disposable_income, 2),
            total_debt=round(total_debt, 2),
            savings_rate=round(savings_rate, 4),
            debt_to_income_ratio=round(debt_to_income, 4)
        )

    @staticmethod
    def _dict_from_expenses(expenses) -> Dict[str, float]:
        """Convert expense items to dictionary"""
        return {exp.category: exp.amount for exp in expenses}

    @staticmethod
    def _compile_recommendations(
        financial_input: FinancialInputRequest,
        budget_advice: str,
        savings_advice: str,
        debt_advice: str,
        investment_advice: str
    ) -> List[Recommendation]:
        """
        Compile recommendations based on agent outputs
        Prioritize based on financial situation
        """
        recommendations = []
        recommendation_id = 1

        # Determine priorities based on financial metrics
        total_debt = sum(debt.amount for debt in financial_input.debts)
        total_expenses = sum(expense.amount for expense in financial_input.expenses)
        disposable = financial_input.monthly_income - total_expenses
        debt_to_income = total_debt / financial_input.monthly_income if financial_input.monthly_income > 0 else 0

        # High priority: Debt elimination if high debt-to-income ratio
        if debt_to_income > 1.0:
            recommendations.append(Recommendation(
                id=recommendation_id,
                priority="High",
                title="Prioritize High-Interest Debt Elimination",
                description=f"Your debt-to-income ratio is {debt_to_income:.1%}, which is elevated. Focus on eliminating high-interest debt first.",
                action=debt_advice,
                estimated_savings="Significant interest savings",
                timeframe="12-24 months"
            ))
            recommendation_id += 1

        # High priority: Emergency fund if low disposable income
        if disposable < financial_input.monthly_income * 0.2:
            recommendations.append(Recommendation(
                id=recommendation_id,
                priority="High",
                title="Build Emergency Fund",
                description=f"You have limited disposable income (₹{disposable:.0f}). Start building an emergency fund equal to 3-6 months of expenses.",
                action="Set aside ₹200-300/month in savings account",
                estimated_savings="Financial security and peace of mind",
                timeframe="6-12 months"
            ))
            recommendation_id += 1

        # Medium priority: Budget optimization
        recommendations.append(Recommendation(
            id=recommendation_id,
            priority="Medium",
            title="Optimize Your Budget",
            description=budget_advice,
            action="Review expenses and identify optimization opportunities",
            estimated_savings="5-10% of current spending",
            timeframe="Immediate"
        ))
        recommendation_id += 1

        # Medium priority: Savings goals
        if disposable > 0:
            recommendations.append(Recommendation(
                id=recommendation_id,
                priority="Medium",
                title="Establish Savings Goals",
                description=savings_advice,
                action=f"Save ₹{disposable * 0.2:.0f}-₹{disposable * 0.3:.0f}/month",
                estimated_savings="Build financial cushion",
                timeframe="Ongoing"
            ))
            recommendation_id += 1

        # Low priority: Investment strategy (if applicable)
        if financial_input.risk_tolerance and disposable > 500:
            recommendations.append(Recommendation(
                id=recommendation_id,
                priority="Low",
                title="Develop Investment Strategy",
                description=investment_advice,
                action=f"Invest 10-15% of disposable income with {financial_input.risk_tolerance} risk tolerance",
                estimated_savings="Long-term wealth building",
                timeframe="After emergency fund is established"
            ))

        return recommendations


class BudgetAgent:
    """Agent for budget analysis and advice"""

    def analyze_budget(
        self,
        income: float,
        expenses: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Generate budget advice
        Returns dictionary of budget analysis
        """
        logger.info("Running budget agent")
        # Reuse logic from agents/budget_agent.py if needed, or implement here.
        # Given the orchestrator expects a dict, let's look at what agents/budget_agent.py does.
        from agents.budget_agent import analyze_budget as analyze
        return analyze(income, expenses)


class SavingsAgent:
    """Agent for savings planning and recommendations"""

    def analyze_savings(
        self,
        income: float,
        expenses: Dict[str, float],
        current_savings: float = 0
    ) -> Dict[str, Any]:
        """
        Generate savings advice
        Returns dictionary of savings analysis
        """
        logger.info("Running savings agent")
        from agents.savings_agent import analyze_savings as analyze
        return analyze(income, expenses, current_savings)


class DebtAgent:
    """Agent for debt analysis and repayment strategies"""

    def analyze_debt(
        self,
        debts: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate debt repayment advice
        Returns dictionary of debt analysis
        """
        logger.info("Running debt agent")
        from agents.debt_agent import analyze_debt as analyze
        return analyze(debts)


class InvestmentAgent:
    """Agent for investment strategy and recommendations"""

    def analyze_investment(
        self,
        income: float,
        expenses: Dict[str, float],
        current_savings: float = 0,
        debts: List[Dict[str, Any]] = None,
        risk_tolerance: str = "medium"
    ) -> Dict[str, Any]:
        """
        Generate investment advice based on risk tolerance
        Returns dictionary of investment analysis
        """
        logger.info("Running investment agent")
        from agents.investment_agent import analyze_investment as analyze
        return analyze(income, expenses, current_savings, debts, risk_tolerance)


def create_financial_agent() -> FinancialAgent:
    """
    Factory function to create financial agent
    Useful for dependency injection
    """
    return FinancialAgent()
