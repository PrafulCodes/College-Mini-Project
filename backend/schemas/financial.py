"""
Pydantic schemas for financial data validation
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Literal, Any, Union


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
        populate_by_name = True
        json_schema_extra = {
            "example": {"category": "Rent", "amount": 1200.00}
        }


class DebtItem(BaseModel):
    """Schema for debt items"""
    name: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., ge=0)
    interest_rate: float = Field(..., ge=0, le=100, alias="interestRate")

    @validator('amount', 'interest_rate')
    def validate_numbers(cls, v):
        return round(v, 2)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Credit Card",
                "amount": 3000.00,
                "interestRate": 18.50
            }
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
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "monthlyIncome": 5000,
                "expenses": [
                    {"category": "Rent", "amount": 1200},
                    {"category": "Groceries", "amount": 500},
                ],
                "debts": [
                    {"name": "Credit Card", "amount": 3000, "interestRate": 18.5}
                ],
                "riskTolerance": "Medium"
            }
        }


class FinancialSummary(BaseModel):
    """Summary of financial calculations"""
    monthly_income: float = Field(..., alias="monthlyIncome")
    total_expenses: float = Field(..., alias="totalExpenses")
    disposable_income: float = Field(..., alias="disposableIncome")
    total_debt: float = Field(..., alias="totalDebt")
    savings_rate: float = Field(..., alias="savingsRate")
    debt_to_income_ratio: float = Field(..., alias="debtToIncomeRatio")

    class Config:
        populate_by_name = True


class Recommendation(BaseModel):
    """Schema for a single recommendation"""
    id: int
    priority: Literal["High", "Medium", "Low"]
    title: str
    description: str
    action: str
    estimated_savings: str = Field(..., alias="estimatedSavings")
    timeframe: str

    class Config:
        populate_by_name = True


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
    risk_tolerance: str = Field(..., alias="riskTolerance")
    budget_advice: Union[str, Dict[str, Any]] = Field(..., alias="budgetAdvice")
    savings_advice: Union[str, Dict[str, Any]] = Field(..., alias="savingsAdvice")
    debt_advice: Union[str, Dict[str, Any]] = Field(..., alias="debtAdvice")
    investment_advice: Union[str, Dict[str, Any]] = Field(..., alias="investmentAdvice")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "status": "success",
                "summary": {
                    "monthlyIncome": 5000,
                    "totalExpenses": 1950,
                    "disposableIncome": 3050,
                    "totalDebt": 12000,
                    "savingsRate": 0.61,
                    "debtToIncomeRatio": 2.4
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
                        "interestRate": 18.5
                    }
                ],
                "recommendations": [
                    {
                        "id": 1,
                        "priority": "High",
                        "title": "Eliminate High-Interest Debt",
                        "description": "Focus on paying off your 18.5% APR credit card.",
                        "action": "Allocate $300/month to credit card",
                        "estimatedSavings": "$1,260 over 1 year",
                        "timeframe": "10-12 months"
                    }
                ],
                "riskTolerance": "Medium",
                "budgetAdvice": "Your budget is good...",
                "savingsAdvice": "Aim to save 20% of income...",
                "debtAdvice": "Focus on high-interest debt first...",
                "investmentAdvice": "Consider investing 10% of disposable income..."
            }
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
        description="Order of prioritization",
        alias="priorityOrder"
    )
    total_actions: int = Field(..., description="Total number of actions in plan", alias="totalActions")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "plan": [
                    "Pay extra towards high-interest debt (Credit Card 22%)",
                    "Build emergency fund with $500/month savings",
                    "Reduce discretionary spending by 20%",
                    "Start investing with balanced mutual funds"
                ],
                "priorityOrder": ["debt", "savings", "budget", "investment"],
                "totalActions": 4
            }
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
    action_plan: ActionPlan = Field(..., alias="actionPlan")
    risk_tolerance: str = Field(..., alias="riskTolerance")
    budget_advice: Union[str, Dict[str, Any]] = Field(..., alias="budgetAdvice")
    savings_advice: Union[str, Dict[str, Any]] = Field(..., alias="savingsAdvice")
    debt_advice: Union[str, Dict[str, Any]] = Field(..., alias="debtAdvice")
    investment_advice: Union[str, Dict[str, Any]] = Field(..., alias="investmentAdvice")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "status": "success",
                "summary": {
                    "monthlyIncome": 5000,
                    "totalExpenses": 1950,
                    "disposableIncome": 3050,
                    "totalDebt": 12000,
                    "savingsRate": 0.61,
                    "debtToIncomeRatio": 2.4
                },
                "expenses": {"Rent": 1200, "Groceries": 500},
                "debts": [{"name": "Credit Card", "amount": 3000, "interestRate": 18.5}],
                "recommendations": [
                    {
                        "id": 1,
                        "priority": "High",
                        "title": "Eliminate High-Interest Debt",
                        "description": "Focus on paying off your 18.5% APR credit card.",
                        "action": "Allocate $300/month to credit card",
                        "estimatedSavings": "$1,260 over 1 year",
                        "timeframe": "10-12 months"
                    }
                ],
                "actionPlan": {
                    "plan": [
                        "Pay extra towards Credit Card (22% interest)",
                        "Build emergency fund with $500/month",
                        "Reduce discretionary spending by 20%"
                    ],
                    "priorityOrder": ["debt", "savings", "budget", "investment"],
                    "totalActions": 3
                },
                "riskTolerance": "Medium",
                "budgetAdvice": "Your budget is good...",
                "savingsAdvice": "Aim to save 20% of income...",
                "debtAdvice": "Focus on high-interest debt first...",
                "investmentAdvice": "Consider investing 10% of disposable income..."
            }
        }


class StoredPlan(BaseModel):
    """Schema for stored plan retrieval"""
    user_id: int = Field(..., alias="userId")
    plan: List[str]
    created_at: str = Field(..., description="ISO timestamp of creation", alias="createdAt")
    updated_at: str = Field(..., description="ISO timestamp of last update", alias="updatedAt")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "userId": 1,
                "plan": [
                    "Pay extra towards high-interest debt",
                    "Build emergency fund",
                    "Reduce discretionary spending"
                ],
                "createdAt": "2024-01-15T10:30:00",
                "updatedAt": "2024-01-15T10:30:00"
            }
        }


class PlanResponse(BaseModel):
    """Response schema for plan operations"""
    status: str
    user_id: int = Field(..., alias="userId")
    message: str
    plan: Optional[List[str]] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")

    class Config:
        populate_by_name = True


class SavePlanRequest(BaseModel):
    """Request schema for saving a plan"""
    plan: List[str] = Field(..., min_items=1, max_items=20, description="List of action items")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "plan": [
                    "Pay extra towards high-interest debt",
                    "Build emergency fund",
                    "Reduce discretionary spending"
                ]
            }
        }
