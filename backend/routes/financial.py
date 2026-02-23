"""
Routes for financial analysis endpoints
Handles financial input processing and returns recommendations
"""

from fastapi import APIRouter, HTTPException, Depends, Path
from typing import Dict, Any
import logging

from schemas.financial import (
    FinancialInputRequest,
    FinancialAnalysisResponse,
    ExtendedAnalysisResponse,
    FinancialSummary,
    Recommendation,
    ActionPlan,
    StoredPlan,
    PlanResponse,
    SavePlanRequest
)
from services.agent_service import FinancialAgent, create_financial_agent
from services.council_service import synthesize_plan
from services import storage

logger = logging.getLogger(__name__)

# Create router
financial_router = APIRouter(prefix="/api", tags=["financial"])


def get_financial_agent() -> FinancialAgent:
    """
    Dependency injection for financial agent
    Creates a new agent instance for each request
    """
    return create_financial_agent()


@financial_router.post("/analyze", response_model=ExtendedAnalysisResponse)
async def analyze_financial_situation(
    request: FinancialInputRequest,
    agent: FinancialAgent = Depends(get_financial_agent)
) -> ExtendedAnalysisResponse:
    """
    Analyze financial situation and return recommendations with action plan

    **Request Body:**
    - monthly_income: Monthly gross income (float)
    - expenses: List of expense items with category and amount
    - debts: List of debts with name, amount, and interest rate
    - risk_tolerance: Investment risk tolerance ("Low", "Medium", "High")

    **Response:**
    - summary: Financial summary with key metrics
    - expenses: Dictionary of expense categories and amounts
    - debts: List of debts
    - recommendations: List of prioritized recommendations
    - action_plan: Synthesized unified action plan
    - budget_advice, savings_advice, debt_advice, investment_advice: Raw agent outputs

    **Example:**
    ```json
    {
        "monthly_income": 5000,
        "expenses": [
            {"category": "Housing", "amount": 1500},
            {"category": "Food", "amount": 400}
        ],
        "debts": [
            {"name": "Credit Card", "amount": 2000, "interest_rate": 18}
        ],
        "risk_tolerance": "Medium"
    }
    ```
    """

    try:
        logger.info(
            f"Analyzing financial situation for income: ₹{request.monthly_income}"
        )


        # Run financial analysis through agent
        analysis_result = agent.analyze_financial_situation(request)

        # Extract components
        summary: FinancialSummary = analysis_result["summary"]
        expenses: Dict[str, float] = analysis_result["expenses"]
        debts = request.debts
        recommendations: list[Recommendation] = analysis_result["recommendations"]
        projection = analysis_result.get("projection", {})
        explanations = analysis_result.get("explanations", {})

        # Extract raw advice from all agents (now dicts)
        advice_dict = {
            "budget_advice": analysis_result.get("budget_advice", {}),
            "savings_advice": analysis_result.get("savings_advice", {}),
            "debt_advice": analysis_result.get("debt_advice", {}),
            "investment_advice": analysis_result.get("investment_advice", {})
        }

        # Synthesize unified action plan from agent advice (use advice text)
        plan_synthesis = synthesize_plan({
            k: v.get("advice", "") if isinstance(v, dict) else v for k, v in advice_dict.items()
        })
        action_plan = ActionPlan(
            plan=plan_synthesis["plan"],
            priority_order=plan_synthesis.get("priority_order", ["debt", "savings", "budget", "investment"]),
            total_actions=plan_synthesis.get("total_actions", 0)
        )

        logger.info(f"Synthesized action plan with {len(action_plan.plan)} items")

        # Build extended response with action plan, projection, and explanations
        response = ExtendedAnalysisResponse(
            summary=summary,
            expenses=expenses,
            debts=debts,
            recommendations=recommendations,
            action_plan=action_plan,
            risk_tolerance=request.risk_tolerance,
            budget_advice=advice_dict["budget_advice"],
            savings_advice=advice_dict["savings_advice"],
            debt_advice=advice_dict["debt_advice"],
            investment_advice=advice_dict["investment_advice"],
            projection=projection,
            explanations=explanations
        )

        logger.info(f"Analysis complete. Generated {len(recommendations)} recommendations and {len(action_plan.plan)} action items")
        return response

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred during financial analysis"
        )


@financial_router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check for financial routes
    """
    return {"status": "ok", "service": "financial-analysis"}


@financial_router.post("/validate")
async def validate_input(request: FinancialInputRequest) -> Dict[str, Any]:
    """
    Validate financial input without performing analysis
    Useful for form validation on the frontend

    Returns validation status and any errors
    """
    try:
        # If request parsing succeeds, validation passes
        return {
            "valid": True,
            "message": "Input is valid"
        }
    except ValueError as e:
        return {
            "valid": False,
            "message": str(e),
            "errors": str(e)
        }


@financial_router.get("/plan/{user_id}", response_model=StoredPlan)
async def get_plan(
    user_id: int = Path(..., gt=0, description="Unique user identifier")
) -> StoredPlan:
    """
    Retrieve a stored action plan for a user

    **Parameters:**
    - user_id (int): Unique user identifier (must be > 0)

    **Response:**
    - user_id: The user's ID
    - plan: List of action items
    - created_at: ISO timestamp of plan creation
    - updated_at: ISO timestamp of last update

    **Example:**
    ```
    GET /api/plan/1
    
    Response:
    {
        "user_id": 1,
        "plan": [
            "Pay extra towards high-interest debt",
            "Build emergency fund",
            "Reduce discretionary spending"
        ],
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:30:00"
    }
    ```
    """
    try:
        logger.info(f"Retrieving plan for user {user_id}")

        # Retrieve plan from storage
        stored_plan = storage.get_plan(user_id)

        if not stored_plan:
            logger.warning(f"Plan not found for user {user_id}")
            raise HTTPException(
                status_code=404,
                detail=f"No plan found for user {user_id}"
            )

        # Build response
        response = StoredPlan(
            user_id=stored_plan["user_id"],
            plan=stored_plan["plan"],
            created_at=stored_plan["created_at"],
            updated_at=stored_plan["updated_at"]
        )

        logger.info(f"Successfully retrieved plan for user {user_id}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving plan: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the plan"
        )


@financial_router.post("/plan/{user_id}", response_model=PlanResponse)
async def save_plan(
    user_id: int = Path(..., gt=0, description="Unique user identifier"),
    save_request: SavePlanRequest = None
) -> PlanResponse:
    """
    Save an action plan for a user

    **Parameters:**
    - user_id (int): Unique user identifier (must be > 0)

    **Request Body:**
    ```json
    {
        "plan": [
            "Action item 1",
            "Action item 2",
            "Action item 3"
        ]
    }
    ```

    **Response:**
    - status: "success" or "error"
    - user_id: The user's ID
    - message: Status message
    - plan: The saved plan
    - created_at: ISO timestamp
    - updated_at: ISO timestamp

    **Example:**
    ```
    POST /api/plan/1
    Body: {
        "plan": [
            "Pay extra towards credit card",
            "Build $1000 emergency fund"
        ]
    }

    Response:
    {
        "status": "success",
        "user_id": 1,
        "message": "Plan saved successfully",
        "plan": [...],
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:30:00"
    }
    ```
    """
    try:
        logger.info(f"Saving plan for user {user_id}")

        # Extract plan from request
        if not save_request or not save_request.plan:
            logger.warning(f"Invalid plan data for user {user_id}")
            raise HTTPException(
                status_code=400,
                detail="Plan must be a non-empty list of action items"
            )

        plan_items = save_request.plan

        # Save to storage
        stored_data = storage.save_plan(user_id, plan_items)

        logger.info(f"Successfully saved plan for user {user_id} with {len(plan_items)} items")

        return PlanResponse(
            status="success",
            user_id=user_id,
            message="Plan saved successfully",
            plan=stored_data["plan"],
            created_at=stored_data["created_at"],
            updated_at=stored_data["updated_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving plan: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while saving the plan"
        )


@financial_router.delete("/plan/{user_id}", response_model=PlanResponse)
async def delete_plan(
    user_id: int = Path(..., gt=0, description="Unique user identifier")
) -> PlanResponse:
    """
    Delete a stored action plan for a user

    **Parameters:**
    - user_id (int): Unique user identifier (must be > 0)

    **Response:**
    - status: "success" or "error"
    - user_id: The user's ID
    - message: Status message

    **Example:**
    ```
    DELETE /api/plan/1

    Response:
    {
        "status": "success",
        "user_id": 1,
        "message": "Plan deleted successfully"
    }
    ```
    """
    try:
        logger.info(f"Deleting plan for user {user_id}")

        # Delete from storage
        deleted = storage.delete_plan(user_id)

        if not deleted:
            logger.warning(f"Plan not found for user {user_id}")
            raise HTTPException(
                status_code=404,
                detail=f"No plan found for user {user_id} to delete"
            )

        logger.info(f"Successfully deleted plan for user {user_id}")

        return PlanResponse(
            status="success",
            user_id=user_id,
            message="Plan deleted successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting plan: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the plan"
        )
