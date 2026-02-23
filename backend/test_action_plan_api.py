"""
Test script for Money Council Action Plan API endpoints
Run this script to verify all new endpoints are working correctly
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_response(response, title="Response"):
    print(f"{title}:")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print()

def test_analyze_endpoint():
    """Test the enhanced /analyze endpoint that includes action plan"""
    
    print_header("TEST 1: POST /api/analyze - Financial Analysis with Action Plan")
    
    payload = {
        "monthly_income": 5000,
        "expenses": [
            {"category": "Housing", "amount": 1500},
            {"category": "Food", "amount": 400},
            {"category": "Transportation", "amount": 300},
            {"category": "Entertainment", "amount": 200}
        ],
        "debts": [
            {"name": "Credit Card", "amount": 3000, "interest_rate": 22},
            {"name": "Student Loan", "amount": 15000, "interest_rate": 5}
        ],
        "risk_tolerance": "Medium"
    }
    
    print("Request Data:")
    print(json.dumps(payload, indent=2))
    print()
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        print_response(response, "Analyze Response")
        
        if response.status_code == 200:
            data = response.json()
            if "action_plan" in data:
                print("✓ Action plan found in response!")
                print(f"  Total actions: {data['action_plan']['total_actions']}")
                print("  Action items:")
                for i, item in enumerate(data['action_plan']['plan'], 1):
                    print(f"    {i}. {item}")
            else:
                print("✗ No action_plan in response!")
            
            return data
        else:
            print(f"✗ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return None

def test_save_plan(user_id, plan_items):
    """Test saving a plan for a user"""
    
    print_header(f"TEST 2: POST /api/plan/{user_id} - Save Action Plan")
    
    payload = {"plan": plan_items}
    
    print(f"Saving plan for user {user_id}")
    print(f"Plan items ({len(plan_items)}):")
    for item in plan_items:
        print(f"  - {item}")
    print()
    
    try:
        response = requests.post(f"{BASE_URL}/plan/{user_id}", json=payload)
        print_response(response, "Save Plan Response")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Plan saved successfully!")
            print(f"  Created: {data.get('created_at')}")
            print(f"  Updated: {data.get('updated_at')}")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False

def test_get_plan(user_id):
    """Test retrieving a saved plan"""
    
    print_header(f"TEST 3: GET /api/plan/{user_id} - Retrieve Saved Plan")
    
    print(f"Retrieving plan for user {user_id}\n")
    
    try:
        response = requests.get(f"{BASE_URL}/plan/{user_id}")
        print_response(response, "Get Plan Response")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Plan retrieved successfully!")
            print(f"  User ID: {data['user_id']}")
            print(f"  Created: {data['created_at']}")
            print(f"  Updated: {data['updated_at']}")
            print(f"  Actions ({len(data['plan'])}):")
            for i, item in enumerate(data['plan'], 1):
                print(f"    {i}. {item}")
            return True
        elif response.status_code == 404:
            print(f"✗ Plan not found for user {user_id}")
            return False
        else:
            print(f"✗ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False

def test_update_plan(user_id, new_plan_items):
    """Test updating an existing plan"""
    
    print_header(f"TEST 4: POST /api/plan/{user_id} - Update Existing Plan")
    
    payload = {"plan": new_plan_items}
    
    print(f"Updating plan for user {user_id}")
    print(f"New plan items ({len(new_plan_items)}):")
    for item in new_plan_items:
        print(f"  - {item}")
    print()
    
    try:
        response = requests.post(f"{BASE_URL}/plan/{user_id}", json=payload)
        print_response(response, "Update Plan Response")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Plan updated successfully!")
            print(f"  Updated timestamp: {data.get('updated_at')}")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False

def test_delete_plan(user_id):
    """Test deleting a plan"""
    
    print_header(f"TEST 5: DELETE /api/plan/{user_id} - Delete Plan")
    
    print(f"Deleting plan for user {user_id}\n")
    
    try:
        response = requests.delete(f"{BASE_URL}/plan/{user_id}")
        print_response(response, "Delete Plan Response")
        
        if response.status_code == 200:
            print(f"✓ Plan deleted successfully!")
            return True
        elif response.status_code == 404:
            print(f"✗ Plan not found for user {user_id}")
            return False
        else:
            print(f"✗ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False

def test_error_cases():
    """Test error handling"""
    
    print_header("TEST 6: Error Handling")
    
    # Test 1: Invalid user_id (non-positive)
    print("6a. Testing invalid user_id (0):\n")
    try:
        response = requests.get(f"{BASE_URL}/plan/0")
        print(f"Status: {response.status_code}")
        if response.status_code in [400, 422]:
            print("✓ Correctly rejected invalid user_id")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    print("\n" + "-"*60 + "\n")
    
    # Test 2: Empty plan
    print("6b. Testing empty plan submission:\n")
    try:
        response = requests.post(f"{BASE_URL}/plan/1", json={"plan": []})
        print(f"Status: {response.status_code}")
        if response.status_code == 400:
            print("✓ Correctly rejected empty plan")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    print("\n" + "-"*60 + "\n")
    
    # Test 3: Non-existent plan retrieval
    print("6c. Testing retrieval of non-existent plan:\n")
    try:
        response = requests.get(f"{BASE_URL}/plan/99999")
        print(f"Status: {response.status_code}")
        if response.status_code == 404:
            print("✓ Correctly returned 404 for non-existent plan")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Exception: {str(e)}")

def run_full_test_suite():
    """Run complete test suite"""
    
    print("\n")
    print("#" * 60)
    print("#  MONEY COUNCIL - ACTION PLAN API TEST SUITE")
    print("#" * 60)
    print(f"#  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("#" * 60)
    
    # Test 1: Analyze with plan generation
    analysis_data = test_analyze_endpoint()
    
    if analysis_data and "action_plan" in analysis_data:
        plan_items = analysis_data["action_plan"]["plan"]
        user_id = 1
        
        # Test 2: Save the generated plan
        test_save_plan(user_id, plan_items)
        
        # Test 3: Retrieve the saved plan
        test_get_plan(user_id)
        
        # Test 4: Update the plan
        updated_plan = [
            "Emergency debt payment ($1000/month)",
            "Build 6-month emergency fund",
            "Complete budget overhaul",
            "Max out 401k contributions"
        ]
        test_update_plan(user_id, updated_plan)
        
        # Test 5: Delete the plan
        test_delete_plan(user_id)
        
        # Test 6: Error handling
        test_error_cases()
    else:
        print("✗ Could not proceed with plan tests - analyze endpoint failed")
    
    # Final status
    print("\n")
    print("#" * 60)
    print("#  TEST SUITE COMPLETE")
    print("#" * 60)
    print(f"#  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("#" * 60)
    print("\nNote: Check Swagger UI at http://localhost:5000/docs for interactive testing")
    print()

if __name__ == "__main__":
    try:
        # Check if backend is running
        response = requests.get(f"{BASE_URL.replace('/api', '')}/health", timeout=2)
        if response.status_code == 200:
            run_full_test_suite()
        else:
            print("✗ Backend not responding correctly")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend at", BASE_URL)
        print("\nMake sure the backend is running:")
        print("  cd backend")
        print("  uvicorn main:app --reload")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
