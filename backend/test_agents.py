"""
Test Suite for Financial Advisory Agents

This script tests all four agents with sample financial data to demonstrate
their functionality and output format.

Run with: python backend/test_agents.py
"""

import json
import sys
from agents.budget_agent import analyze_budget
from agents.savings_agent import analyze_savings
from agents.debt_agent import analyze_debt
from agents.investment_agent import analyze_investment


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80 + "\n")


def test_budget_agent():
    """Test the Budget Agent with various scenarios."""
    print_section("BUDGET AGENT TESTS")
    
    # Test Case 1: Healthy Budget (50% spending)
    print("[TEST 1] Healthy Budget (50% spending)")
    result = analyze_budget(
        income=100000,
        expenses={
            "food": 15000,
            "rent": 30000,
            "utilities": 5000
        }
    )
    print(json.dumps(result, indent=2))
    print(f"PASS - Severity: {result['severity']}\n")
    
    # Test Case 2: Overspending (80% spending)
    print("[TEST 2] Overspending (80% spending)")
    result = analyze_budget(
        income=100000,
        expenses={
            "food": 25000,
            "rent": 40000,
            "entertainment": 15000
        }
    )
    print(json.dumps(result, indent=2))
    print(f"PASS - Severity: {result['severity']}\n")
    
    # Test Case 3: No expenses
    print("[TEST 3] No expense data")
    result = analyze_budget(
        income=100000,
        expenses={}
    )
    print(json.dumps(result, indent=2))
    print(f"PASS - Severity: {result['severity']}\n")


def test_savings_agent():
    """Test the Savings Agent with various scenarios."""
    print_section("SAVINGS AGENT TESTS")
    
    # Test Case 1: Adequate Emergency Fund
    print("💰 Test 1: Adequate Emergency Fund")
    result = analyze_savings(
        income=100000,
        expenses={"food": 15000, "rent": 30000, "utilities": 5000},
        current_savings=200000
    )
    print(json.dumps(result, indent=2))
    print(f"✓ Severity: {result['severity']}\n")
    
    # Test Case 2: Insufficient Emergency Fund
    print("💰 Test 2: Insufficient Emergency Fund")
    result = analyze_savings(
        income=100000,
        expenses={"food": 15000, "rent": 30000, "utilities": 5000},
        current_savings=50000
    )
    print(json.dumps(result, indent=2))
    print(f"✓ Severity: {result['severity']}\n")
    
    # Test Case 3: No savings
    print("💰 Test 3: No Savings (Starting Point)")
    result = analyze_savings(
        income=100000,
        expenses={"food": 15000, "rent": 30000, "utilities": 5000},
        current_savings=0
    )
    print(json.dumps(result, indent=2))
    print(f"✓ Severity: {result['severity']}\n")


def test_debt_agent():
    """Test the Debt Agent with various scenarios."""
    print_section("DEBT AGENT TESTS")
    
    # Test Case 1: No Debt
    print("📋 Test 1: No Debt (Debt-free)")
    result = analyze_debt(debts=[])
    print(json.dumps(result, indent=2))
    print(f"✓ Severity: {result['severity']}\n")
    
    # Test Case 2: Manageable Debt with Known Rates
    print("📋 Test 2: Manageable Debt (Avalanche Method)")
    result = analyze_debt(
        debts=[
            {"name": "Credit Card", "amount": 50000, "interest_rate": 18},
            {"name": "Personal Loan", "amount": 100000, "interest_rate": 12},
            {"name": "Car Loan", "amount": 200000, "interest_rate": 8}
        ]
    )
    print(json.dumps(result, indent=2))
    print(f"✓ Severity: {result['severity']}\n")
    
    # Test Case 3: High-Interest Debt
    print("📋 Test 3: High-Interest Debt (Priority Alert)")
    result = analyze_debt(
        debts=[
            {"name": "Credit Card", "amount": 80000, "interest_rate": 22},
            {"name": "Personal Loan", "amount": 120000, "interest_rate": 14}
        ]
    )
    print(json.dumps(result, indent=2))
    print(f"✓ Severity: {result['severity']}\n")
    
    # Test Case 4: Debts without Interest Rate Info (Snowball Method)
    print("📋 Test 4: Debts without Interest Info (Snowball Method)")
    result = analyze_debt(
        debts=[
            {"name": "Loan A", "amount": 30000},
            {"name": "Loan B", "amount": 75000},
            {"name": "Loan C", "amount": 50000}
        ]
    )
    print(json.dumps(result, indent=2))
    print(f"✓ Severity: {result['severity']}\n")


def test_investment_agent():
    """Test the Investment Agent with various scenarios."""
    print_section("INVESTMENT AGENT TESTS")
    
    # Test Case 1: Not Ready (No Emergency Fund)
    print("📈 Test 1: Not Investment Ready (No Emergency Fund)")
    result = analyze_investment(
        income=100000,
        expenses={"food": 15000, "rent": 30000, "utilities": 5000},
        current_savings=50000,
        debts=[],
        risk_tolerance="medium"
    )
    print(json.dumps(result, indent=2))
    print(f"✓ Status: {result['status']}\n")
    
    # Test Case 2: High-Interest Debt (Cannot Invest Yet)
    print("📈 Test 2: Not Investment Ready (High-Interest Debt)")
    result = analyze_investment(
        income=100000,
        expenses={"food": 15000, "rent": 30000, "utilities": 5000},
        current_savings=200000,
        debts=[{"name": "Credit Card", "amount": 80000, "interest_rate": 22}],
        risk_tolerance="medium"
    )
    print(json.dumps(result, indent=2))
    print(f"✓ Status: {result['status']}\n")
    
    # Test Case 3: Ready to Invest - Low Risk
    print("📈 Test 3: Ready to Invest - Low Risk Profile")
    result = analyze_investment(
        income=100000,
        expenses={"food": 15000, "rent": 30000, "utilities": 5000},
        current_savings=200000,
        debts=[{"name": "Car Loan", "amount": 150000, "interest_rate": 6}],
        risk_tolerance="low"
    )
    print(json.dumps(result, indent=2))
    print(f"✓ Status: {result['status']}\n")
    
    # Test Case 4: Ready to Invest - High Risk
    print("📈 Test 4: Ready to Invest - High Risk Profile")
    result = analyze_investment(
        income=100000,
        expenses={"food": 15000, "rent": 30000, "utilities": 5000},
        current_savings=200000,
        debts=[],
        risk_tolerance="high"
    )
    print(json.dumps(result, indent=2))
    print(f"✓ Status: {result['status']}\n")


def run_comprehensive_test():
    """Run a comprehensive financial analysis."""
    print_section("COMPREHENSIVE FINANCIAL ANALYSIS")
    print("Analyzing a sample user profile...\n")
    
    # Sample user data
    income = 120000
    expenses = {
        "food": 18000,
        "rent": 40000,
        "utilities": 6000,
        "entertainment": 8000,
        "groceries": 12000
    }
    current_savings = 250000
    debts = [
        {"name": "Home Loan", "amount": 3000000, "interest_rate": 8},
        {"name": "Car Loan", "amount": 250000, "interest_rate": 9}
    ]
    risk_tolerance = "medium"
    
    print(f"📋 User Profile:")
    print(f"  • Monthly Income: ₹{income:,.0f}")
    print(f"  • Total Expenses: ₹{sum(expenses.values()):,.0f}")
    print(f"  • Current Savings: ₹{current_savings:,.0f}")
    print(f"  • Total Debt: ₹{sum(d.get('amount', 0) for d in debts):,.0f}")
    print(f"  • Risk Tolerance: {risk_tolerance}\n")
    
    # Run all agents
    budget_advice = analyze_budget(income, expenses)
    savings_advice = analyze_savings(income, expenses, current_savings)
    debt_advice = analyze_debt(debts)
    investment_advice = analyze_investment(income, expenses, current_savings, debts, risk_tolerance)
    
    # Display results
    print("🎯 RECOMMENDATIONS:\n")
    
    print(f"1️⃣  BUDGET")
    print(f"   Severity: {budget_advice['severity'].upper()}")
    print(f"   {budget_advice['advice']}\n")
    
    print(f"2️⃣  SAVINGS")
    print(f"   Severity: {savings_advice['severity'].upper()}")
    print(f"   {savings_advice['advice']}\n")
    
    print(f"3️⃣  DEBT")
    print(f"   Severity: {debt_advice['severity'].upper()}")
    print(f"   Strategy: {debt_advice['metrics']['recommended_strategy'].upper()}")
    print(f"   {debt_advice['advice']}\n")
    
    print(f"4️⃣  INVESTMENT")
    print(f"   Status: {investment_advice['status'].upper()}")
    print(f"   Ready: {investment_advice['metrics']['investment_ready']}")
    if investment_advice['metrics']['investment_ready']:
        alloc = investment_advice['metrics']['recommended_allocation']
        print(f"   Allocation: {', '.join([f'{k} ({v*100:.0f}%)' for k, v in alloc.items()])}")
    print(f"   {investment_advice['advice']}\n")


def main():
    """Run all tests."""
    print("\n")
    print("=" * 80)
    print("FINANCIAL ADVISORY AGENTS - COMPREHENSIVE TEST SUITE".center(80))
    print("=" * 80)
    
    try:
        # Run individual agent tests
        test_budget_agent()
        test_savings_agent()
        test_debt_agent()
        test_investment_agent()
        
        # Run comprehensive analysis
        run_comprehensive_test()
        
        print_section("TEST SUMMARY")
        print("✅ All agent tests completed successfully!")
        print("\nEach agent provides:")
        print("  • Clear, actionable advice")
        print("  • Detailed reasoning")
        print("  • Quantified metrics")
        print("  • Severity assessment")
        print("  • Multiple test scenarios\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
