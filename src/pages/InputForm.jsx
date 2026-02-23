import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyzeFinancialSituation } from '../services/api'
import { mockAnalysisResponse } from '../services/mockData'
import '../styles/InputForm.css'

export default function InputForm() {
  const navigate = useNavigate()
  const [monthlyIncome, setMonthlyIncome] = useState('')
  const [expenses, setExpenses] = useState([{ category: '', amount: '' }])
  const [debts, setDebts] = useState([{ name: '', amount: '', interestRate: '' }])
  const [riskTolerance, setRiskTolerance] = useState('Medium')
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState({})

  // Validate form inputs
  const validateForm = () => {
    const newErrors = {}

    if (!monthlyIncome || monthlyIncome <= 0) {
      newErrors.monthlyIncome = 'Monthly income is required and must be greater than 0'
    }

    expenses.forEach((expense, index) => {
      if (expense.category && !expense.amount) {
        newErrors[`expense_${index}`] = 'Amount is required for all categories'
      }
      if (expense.amount && expense.amount < 0) {
        newErrors[`expense_${index}`] = 'Amount cannot be negative'
      }
    })

    debts.forEach((debt, index) => {
      if (debt.name && !debt.amount) {
        newErrors[`debt_amount_${index}`] = 'Amount is required for all debts'
      }
      if (debt.amount && debt.amount < 0) {
        newErrors[`debt_amount_${index}`] = 'Amount cannot be negative'
      }
      if (debt.interestRate && debt.interestRate < 0) {
        newErrors[`debt_rate_${index}`] = 'Interest rate cannot be negative'
      }
    })

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Handle expense row addition
  const addExpenseRow = () => {
    setExpenses([...expenses, { category: '', amount: '' }])
  }

  // Handle expense row removal
  const removeExpenseRow = (index) => {
    setExpenses(expenses.filter((_, i) => i !== index))
  }

  // Handle expense input change
  const handleExpenseChange = (index, field, value) => {
    const updatedExpenses = [...expenses]
    updatedExpenses[index][field] = value
    setExpenses(updatedExpenses)
  }

  // Handle debt row addition
  const addDebtRow = () => {
    setDebts([...debts, { name: '', amount: '', interestRate: '' }])
  }

  // Handle debt row removal
  const removeDebtRow = (index) => {
    setDebts(debts.filter((_, i) => i !== index))
  }

  // Handle debt input change
  const handleDebtChange = (index, field, value) => {
    const updatedDebts = [...debts]
    updatedDebts[index][field] = value
    setDebts(updatedDebts)
  }

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validateForm()) {
      return
    }

    setLoading(true)

    try {
      const formData = {
        monthlyIncome: parseFloat(monthlyIncome),
        expenses: expenses.filter(exp => exp.category || exp.amount),
        debts: debts.filter(d => d.name || d.amount),
        riskTolerance
      }

      console.log('Form Data Submitted:', formData)

      // Try to call API, fallback to mock data if API fails
      let analysisData
      try {
        analysisData = await analyzeFinancialSituation(formData)
        console.log('API Response:', analysisData)
      } catch (apiError) {
        console.warn('API call failed, using mock data for demonstration:', apiError)
        // Use mock data for demonstration
        analysisData = mockAnalysisResponse
      }

      // Save to sessionStorage for dashboard reloads
      sessionStorage.setItem('dashboardData', JSON.stringify(analysisData))

      // Navigate to dashboard with analysis data
      navigate('/dashboard', {
        state: { analysisData },
      })
    } catch (error) {
      console.error('Error submitting form:', error)
      alert('Failed to submit form. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="form-container">
      <div className="form-header">
        <h1>Money Council</h1>
        <p>Financial Advisory Dashboard</p>
      </div>

      <form onSubmit={handleSubmit} className="financial-form">
        {/* Monthly Income Section */}
        <section className="form-section">
          <h2>Monthly Income</h2>
          <div className="form-group">
            <label htmlFor="monthlyIncome">Monthly Income (₹)</label>
            <input
              type="number"
              id="monthlyIncome"
              value={monthlyIncome}
              onChange={(e) => setMonthlyIncome(e.target.value)}
              placeholder="Enter your monthly income"
              min="0"
              step="0.01"
              className={errors.monthlyIncome ? 'input-error' : ''}
              disabled={loading}
            />
            {errors.monthlyIncome && (
              <span className="error-message">{errors.monthlyIncome}</span>
            )}
          </div>
        </section>

        {/* Expenses Section */}
        <section className="form-section">
          <h2>Expenses</h2>
          <div className="dynamic-rows">
            {expenses.map((expense, index) => (
              <div key={index} className="row-group">
                <div className="form-group">
                  <label htmlFor={`category_${index}`}>Category</label>
                  <input
                    type="text"
                    id={`category_${index}`}
                    placeholder="e.g., Rent, Groceries, Entertainment"
                    value={expense.category}
                    onChange={(e) =>
                      handleExpenseChange(index, 'category', e.target.value)
                    }
                  />
                </div>
                <div className="form-group">
                  <label htmlFor={`expense_amount_${index}`}>Amount (₹)</label>
                  <input
                    type="number"
                    id={`expense_amount_${index}`}
                    placeholder="0.00"
                    value={expense.amount}
                    onChange={(e) =>
                      handleExpenseChange(index, 'amount', e.target.value)
                    }
                    min="0"
                    step="0.01"
                    className={errors[`expense_${index}`] ? 'input-error' : ''}
                  />
                </div>
                {expenses.length > 1 && (
                  <button
                    type="button"
                    className="btn-remove"
                    onClick={() => removeExpenseRow(index)}
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
            {errors[`expense_${expenses.length - 1}`] && (
              <span className="error-message">
                {errors[`expense_${expenses.length - 1}`]}
              </span>
            )}
          </div>
          <button
            type="button"
            className="btn-add"
            onClick={addExpenseRow}
          >
            + Add Expense
          </button>
        </section>

        {/* Debts Section */}
        <section className="form-section">
          <h2>Debts</h2>
          <div className="dynamic-rows">
            {debts.map((debt, index) => (
              <div key={index} className="row-group">
                <div className="form-group">
                  <label htmlFor={`debt_name_${index}`}>Debt Name</label>
                  <input
                    type="text"
                    id={`debt_name_${index}`}
                    placeholder="e.g., Credit Card, Student Loan"
                    value={debt.name}
                    onChange={(e) =>
                      handleDebtChange(index, 'name', e.target.value)
                    }
                  />
                </div>
                <div className="form-group">
                  <label htmlFor={`debt_amount_${index}`}>Amount (₹)</label>
                  <input
                    type="number"
                    id={`debt_amount_${index}`}
                    placeholder="0.00"
                    value={debt.amount}
                    onChange={(e) =>
                      handleDebtChange(index, 'amount', e.target.value)
                    }
                    min="0"
                    step="0.01"
                    className={errors[`debt_amount_${index}`] ? 'input-error' : ''}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor={`debt_rate_${index}`}>Interest Rate (%)</label>
                  <input
                    type="number"
                    id={`debt_rate_${index}`}
                    placeholder="0.00"
                    value={debt.interestRate}
                    onChange={(e) =>
                      handleDebtChange(index, 'interestRate', e.target.value)
                    }
                    min="0"
                    step="0.01"
                    className={errors[`debt_rate_${index}`] ? 'input-error' : ''}
                  />
                </div>
                {debts.length > 1 && (
                  <button
                    type="button"
                    className="btn-remove"
                    onClick={() => removeDebtRow(index)}
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
          </div>
          <button
            type="button"
            className="btn-add"
            onClick={addDebtRow}
          >
            + Add Debt
          </button>
        </section>

        {/* Risk Tolerance Section */}
        <section className="form-section">
          <h2>Risk Tolerance</h2>
          <div className="form-group">
            <label htmlFor="riskTolerance">Select your risk tolerance level</label>
            <select
              id="riskTolerance"
              value={riskTolerance}
              onChange={(e) => setRiskTolerance(e.target.value)}
            >
              <option value="Low">Low - Conservative, minimal risk</option>
              <option value="Medium">Medium - Balanced approach</option>
              <option value="High">High - Aggressive growth</option>
            </select>
          </div>
        </section>

        {/* Submit Button */}
        <button
          type="submit"
          className="btn-submit"
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Analyze My Finances'}
        </button>
      </form>
    </div>
  )
}
