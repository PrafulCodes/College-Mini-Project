"""
Pydantic schemas for financial data validation
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Literal


class ExpenseItem(BaseModel):
    """Schema for expense items"""
    category: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return round(v, 2)

    class Config:
        example = {"category": "Rent", "amount": 1200.00}


class DebtItem(BaseModel):
    """Schema for debt items"""
    name: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., ge=0)
    interest_rate: float = Field(..., ge=0, le=100)

    @validator('amount', 'interest_rate')
    def validate_numbers(cls, v):
        return round(v, 2)

    class Config:
        example = {
            "name": "Credit Card",
            "amount": 3000.00,
            "interest_rate": 18.50
        }


class FinancialInputRequest(BaseModel):
    """
    Main schema for financial input
    Validates data from React frontend form
    """
    monthly_income: float = Field(..., gt=0, alias="monthlyIncome")
    expenses: List[ExpenseItem] = Field(default_factory=list)
    debts: List[DebtItem] = Field(default_factory=list)
    risk_tolerance: Literal["Low", "Medium", "High"] = Field(
        ...,
        alias="riskTolerance"
    )

    @validator('monthly_income', 'expenses')
    def validate_non_negative(cls, v):
        if isinstance(v, float) and v < 0:
            raise ValueError('Value must be non-negative')
        return v

    class Config:
        allow_population_by_field_name = True
        example = {
            "monthlyIncome": 5000,
            "expenses": [
                {"category": "Rent", "amount": 1200},
                {"category": "Groceries", "amount": 500},
            ],
            "debts": [
                {"name": "Credit Card", "amount": 3000, "interest_rate": 18.5}
            ],
            "riskTolerance": "Medium"
        }


class FinancialSummary(BaseModel):
    """Summary of financial calculations"""
    monthly_income: float
    total_expenses: float
    disposable_income: float
    total_debt: float
    savings_rate: float
    debt_to_income_ratio: float


class Recommendation(BaseModel):
    """Schema for a single recommendation"""
    id: int
    priority: Literal["High", "Medium", "Low"]
    title: str
    description: str
    action: str
    estimated_savings: str
    timeframe: str


class FinancialAnalysisResponse(BaseModel):
    """
    Response schema for financial analysis
    Sent back to React frontend
    """
    status: str = "success"
    summary: FinancialSummary
    expenses: Dict[str, float]
    debts: List[DebtItem]
    recommendations: List[Recommendation]
    risk_tolerance: str
    budget_advice: str
    savings_advice: str
    debt_advice: str
    investment_advice: str

    class Config:
        example = {
            "status": "success",
            "summary": {
                "monthly_income": 5000,
                "total_expenses": 1950,
                "disposable_income": 3050,
                "total_debt": 12000,
                "savings_rate": 0.61,
                "debt_to_income_ratio": 2.4
            },
            "expenses": {
                "Rent": 1200,
                "Groceries": 500,
                "Utilities": 150
            },
            "debts": [
                {
                    "name": "Credit Card",
                    "amount": 3000,
                    "interest_rate": 18.5
                }
            ],
            "recommendations": [
                {
                    "id": 1,
                    "priority": "High",
                    "title": "Eliminate High-Interest Debt",
                    "description": "Focus on paying off your 18.5% APR credit card.",
                    "action": "Allocate $300/month to credit card",
                    "estimated_savings": "$1,260 over 1 year",
                    "timeframe": "10-12 months"
                }
            ],
            "risk_tolerance": "Medium",
            "budget_advice": "Your budget is good...",
            "savings_advice": "Aim to save 20% of income...",
            "debt_advice": "Focus on high-interest debt first...",
            "investment_advice": "Consider investing 10% of disposable income..."
        }


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    status: str = "error"
    message: str
    errors: Optional[Dict] = None


class ActionPlan(BaseModel):
    """Schema for unified action plan"""
    plan: List[str] = Field(..., description="List of prioritized action items")
    priority_order: List[str] = Field(
        default=["debt", "savings", "budget", "investment"],
        description="Order of prioritization"
    )
    total_actions: int = Field(..., description="Total number of actions in plan")

    class Config:
        example = {
            "plan": [
                "Pay extra towards high-interest debt (Credit Card 22%)",
                "Build emergency fund with $500/month savings",
                "Reduce discretionary spending by 20%",
                "Start investing with balanced mutual funds"
            ],
            "priority_order": ["debt", "savings", "budget", "investment"],
            "total_actions": 4
        }


class ExtendedAnalysisResponse(BaseModel):
    """
    Extended response schema for financial analysis with action plan
    Includes both raw advice and synthesized plan
    """
    status: str = "success"
    summary: FinancialSummary
    expenses: Dict[str, float]
    debts: List[DebtItem]
    recommendations: List[Recommendation]
    action_plan: ActionPlan
    risk_tolerance: str
    budget_advice: str
    savings_advice: str
    debt_advice: str
    investment_advice: str

    class Config:
        example = {
            "status": "success",
            "summary": {
                "monthly_income": 5000,
                "total_expenses": 1950,
                "disposable_income": 3050,
                "total_debt": 12000,
                "savings_rate": 0.61,
                "debt_to_income_ratio": 2.4
            },
            "expenses": {"Rent": 1200, "Groceries": 500},
            "debts": [{"name": "Credit Card", "amount": 3000, "interest_rate": 18.5}],
            "recommendations": [
                {
                    "id": 1,
                    "priority": "High",
                    "title": "Eliminate High-Interest Debt",
                    "description": "Focus on paying off your 18.5% APR credit card.",
                    "action": "Allocate $300/month to credit card",
                    "estimated_savings": "$1,260 over 1 year",
                    "timeframe": "10-12 months"
                }
            ],
            "action_plan": {
                "plan": [
                    "Pay extra towards Credit Card (22% interest)",
                    "Build emergency fund with $500/month",
                    "Reduce discretionary spending by 20%"
                ],
                "priority_order": ["debt", "savings", "budget", "investment"],
                "total_actions": 3
            },
            "risk_tolerance": "Medium",
            "budget_advice": "Your budget is good...",
            "savings_advice": "Aim to save 20% of income...",
            "debt_advice": "Focus on high-interest debt first...",
            "investment_advice": "Consider investing 10% of disposable income..."
        }


class StoredPlan(BaseModel):
    """Schema for stored plan retrieval"""
    user_id: int
    plan: List[str]
    created_at: str = Field(..., description="ISO timestamp of creation")
    updated_at: str = Field(..., description="ISO timestamp of last update")

    class Config:
        example = {
            "user_id": 1,
            "plan": [
                "Pay extra towards high-interest debt",
                "Build emergency fund",
                "Reduce discretionary spending"
            ],
            "created_at": "2024-01-15T10:30:00",
            "updated_at": "2024-01-15T10:30:00"
        }


class PlanResponse(BaseModel):
    """Response schema for plan operations"""
    status: str
    user_id: int
    message: str
    plan: Optional[List[str]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class SavePlanRequest(BaseModel):
    """Request schema for saving a plan"""
    plan: List[str] = Field(..., min_items=1, max_items=20, description="List of action items")

    class Config:
        example = {
            "plan": [
                "Pay extra towards high-interest debt",
                "Build emergency fund",
                "Reduce discretionary spending"
            ]
        }
