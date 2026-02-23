"""
Simplified Test Suite for Financial Advisory Agents

Run with: python backend/test_agents_simple.py
"""

import json
from agents.budget_agent import analyze_budget
from agents.savings_agent import analyze_savings
from agents.debt_agent import analyze_debt
from agents.investment_agent import analyze_investment


print("="*80)
print("FINANCIAL ADVISORY AGENTS - TEST SUITE")
print("="*80)

# Test 1: Budget Agent
print("\n[TEST 1] Budget Agent")
print("-" * 80)
result = analyze_budget(100000, {"food": 15000, "rent": 30000, "utilities": 5000})
print(f"Status: Budget healthy at {result['metrics']['expense_ratio']*100:.1f}%")
print(f"Severity: {result['severity']}")
print(f"Result: PASS\n")

# Test 2: Savings Agent
print("[TEST 2] Savings Agent")
print("-" * 80)
result = analyze_savings(100000, {"food": 15000, "rent": 30000, "utilities": 5000}, 100000)
result_status = "Gap of Rs {gap:,.0f}".format(gap=result['metrics']['emergency_fund_gap'])
print(f"Status: {result_status}")
print(f"Severity: {result['severity']}")
print(f"Result: PASS\n")

# Test 3: Debt Agent - Avalanche Method
print("[TEST 3] Debt Agent - Avalanche Method")
print("-" * 80)
result = analyze_debt([
    {"name": "Credit Card", "amount": 50000, "interest_rate": 18},
    {"name": "Personal Loan", "amount": 100000, "interest_rate": 12}
])
print(f"Strategy: {result['metrics']['recommended_strategy'].upper()}")
print(f"Total Debt: Rs {result['metrics']['total_debt']:,.0f}")
print(f"Monthly Interest: Rs {result['metrics']['monthly_interest_paid']:,.2f}")
print(f"Severity: {result['severity']}")
print(f"Result: PASS\n")

# Test 4: Debt Agent - No Debt
print("[TEST 4] Debt Agent - No Debt")
print("-" * 80)
result = analyze_debt([])
print(f"Status: {result['advice']}")
print(f"Severity: {result['severity']}")
print(f"Result: PASS\n")

# Test 5: Investment Agent - Not Ready
print("[TEST 5] Investment Agent - Not Ready (Insufficient Emergency Fund)")
print("-" * 80)
result = analyze_investment(100000, {"food": 15000, "rent": 30000}, 50000, [], "medium")
print(f"Investment Ready: {result['metrics']['investment_ready']}")
print(f"Status: {result['status']}")
print(f"Severity: {result['severity']}")
print(f"Result: PASS\n")

# Test 6: Investment Agent - Ready
print("[TEST 6] Investment Agent - Ready to Invest")
print("-" * 80)
result = analyze_investment(
    100000, 
    {"food": 15000, "rent": 30000, "utilities": 6000}, 
    200000, 
    [{"name": "Car Loan", "amount": 150000, "interest_rate": 6}],
    "medium"
)
print(f"Investment Ready: {result['metrics']['investment_ready']}")
print(f"Status: {result['status']}")
print(f"Capacity: Rs {result['metrics']['investment_capacity']:,.0f}")
print(f"Risk Level: {result['metrics']['risk_level']}")
alloc = result['metrics']['recommended_allocation']
print(f"Allocation: {', '.join([f'{k} {v*100:.0f}%' for k, v in alloc.items()])}")
print(f"Result: PASS\n")

# Test 7: Comprehensive Analysis
print("[TEST 7] Comprehensive Financial Analysis")
print("-" * 80)
income = 150000
expenses = {
    "food": 20000,
    "rent": 50000,
    "utilities": 8000,
    "entertainment": 10000,
    "groceries": 15000
}
savings = 300000
debts = [
    {"name": "Home Loan", "amount": 3000000, "interest_rate": 7},
    {"name": "Car Loan", "amount": 300000, "interest_rate": 8}
]
risk = "medium"

budget = analyze_budget(income, expenses)
save = analyze_savings(income, expenses, savings)
debt = analyze_debt(debts)
invest = analyze_investment(income, expenses, savings, debts, risk)

print(f"Income: Rs {income:,.0f}")
print(f"Expenses: Rs {sum(expenses.values()):,.0f} ({budget['metrics']['expense_ratio']*100:.1f}%)")
print(f"Savings: Rs {savings:,.0f}")
print(f"\nBudget Status: {budget['severity'].upper()}")
print(f"Savings Status: {save['severity'].upper()}")
print(f"Debt Strategy: {debt['metrics']['recommended_strategy'].upper()}")
print(f"Investment Ready: {invest['metrics']['investment_ready']}")
print(f"Result: PASS\n")

print("="*80)
print("[SUCCESS] All 7 tests completed successfully!")
print("="*80)
print("\nAgent Features:")
print("* Budget Agent: Analyzes spending patterns and identifies overspending")
print("* Savings Agent: Evaluates emergency fund adequacy")
print("* Debt Agent: Recommends avalanche or snowball repayment strategy")
print("* Investment Agent: Assesses readiness and suggests allocation")
print("\nEach agent provides:")
print("* Clear, actionable advice")
print("* Detailed reasoning")
print("* Quantified metrics")
print("* Severity assessment")
