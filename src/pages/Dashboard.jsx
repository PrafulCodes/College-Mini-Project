
import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Tooltip, Legend } from 'chart.js'
import { Pie, Line, Bar } from 'react-chartjs-2'
import SummaryCard from '../components/SummaryCard'
import ActionPlan from '../components/ActionPlan'
import CurrencySelector from '../components/CurrencySelector'
import StudentModeToggle from '../components/StudentModeToggle'
import { useCurrency } from '../contexts/CurrencyContext'
import { useStudentMode } from '../contexts/StudentModeContext'
import { formatCurrency } from '../utils/currencyFormatter'
import { mockAnalysisResponse, generateSavingsProjection, generateDebtTimeline } from '../services/mockData'
import '../styles/Dashboard.css'

// Register Chart.js components
ChartJS.register(ArcElement, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Tooltip, Legend)


export default function Dashboard() {
  const location = useLocation()
  const [analysisData, setAnalysisData] = useState(null)
  const [loading, setLoading] = useState(true)

  const { currency, setCurrency } = useCurrency()
  const { studentMode, setStudentMode } = useStudentMode()
  const [error, setError] = useState(null)
  const [demoMode, setDemoMode] = useState(false)

  useEffect(() => {
    // Try to get data from router state, then sessionStorage, then mock
    if (location.state?.analysisData) {
      setAnalysisData(location.state.analysisData)
      sessionStorage.setItem('dashboardData', JSON.stringify(location.state.analysisData))
    } else {
      const stored = sessionStorage.getItem('dashboardData')
      if (stored) {
        setAnalysisData(JSON.parse(stored))
      } else {
        setAnalysisData(mockAnalysisResponse)
      }
    }
    setLoading(false)
  }, [location])

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">Loading financial dashboard...</div>
      </div>
    )
  }

  if (!analysisData) {
    return (
      <div className="dashboard-container">
        <div className="error">Unable to load financial data. Please try again.</div>
      </div>
    )
  }

  const { summary, expenses, debts, recommendations, savings } = analysisData

  // ==================== EXPENSE DISTRIBUTION CHART ====================
  const expenseChartData = {
    labels: Object.keys(expenses),
    datasets: [
      {
        data: Object.values(expenses),
        backgroundColor: ['#3498db', '#e74c3c', '#f39c12', '#27ae60', '#9b59b6', '#1abc9c'],
        borderColor: '#fff',
        borderWidth: 2,
      },
    ],
  }

  const expenseChartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 15,
          font: { size: 12 },
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => `${context.label}: ${formatCurrency(context.parsed, currency)}`,
        },
      },
    },
  }

  // ==================== SAVINGS PROJECTION CHART ====================
  const savingsProjection = generateSavingsProjection(
    summary.disposableIncome * 0.5,
    summary.disposableIncome * 0.3,
    6
  )

  const savingsChartData = {
    labels: savingsProjection.labels,
    datasets: [
      {
        label: 'Projected Savings',
        data: savingsProjection.data,
        borderColor: '#27ae60',
        backgroundColor: 'rgba(39, 174, 96, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#27ae60',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
      },
    ],
  }

  const savingsChartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: true,
        labels: {
          usePointStyle: true,
          padding: 15,
          font: { size: 12 },
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => `Savings: ${formatCurrency(context.parsed.y, currency)}`,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: (value) => formatCurrency(value, currency),
        },
      },
    },
  }

  // ==================== DEBT REPAYMENT TIMELINE CHART ====================
  const debtTimeline = generateDebtTimeline(debts)

  const debtChartData = {
    labels: debtTimeline.labels,
    datasets: [
      {
        label: 'Outstanding Debt',
        data: debtTimeline.amounts,
        backgroundColor: '#e74c3c',
        borderColor: '#c0392b',
        borderWidth: 1,
      },
      {
        label: 'Monthly Payment',
        data: debtTimeline.payments,
        backgroundColor: '#3498db',
        borderColor: '#2980b9',
        borderWidth: 1,
      },
    ],
  }

  const debtChartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 15,
          font: { size: 12 },
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => `${context.dataset.label}: ${formatCurrency(context.parsed.y, currency)}`,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: (value) => formatCurrency(value, currency),
        },
      },
    },
  }

  const handleReset = () => {
    sessionStorage.removeItem('dashboardData');
    window.location.href = '/';
  };

  return (
    <div className="dashboard-container">
      {/* Header */}
      <div className="dashboard-header">
        <button
          className="reset-btn"
          style={{ position: 'absolute', right: 24, top: 24, background: '#fff', border: '1px solid #bbb', borderRadius: 6, padding: '6px 16px', fontWeight: 500, cursor: 'pointer', zIndex: 2 }}
          onClick={handleReset}
        >
          Start New Analysis
        </button>
        <h1>💰 Financial Dashboard</h1>
        <p>Your personalized financial analysis and action plan</p>
        <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
          <CurrencySelector currency={currency} setCurrency={setCurrency} />
          <StudentModeToggle studentMode={studentMode} setStudentMode={setStudentMode} />
        </div>
        {studentMode && (
          <span className="student-badge" style={{ background: '#f39c12', color: '#fff', padding: '4px 12px', borderRadius: 8, marginLeft: 12, fontWeight: 600 }}>
            🎓 Student Mode Active
          </span>
        )}
      </div>

      {/* Summary Cards */}
      <section className="summary-section">
        <h2>Financial Overview</h2>
        {studentMode && (
          <div className="student-tips" style={{ background: '#fffbe6', border: '1px solid #ffe58f', borderRadius: 8, padding: 16, marginBottom: 16 }}>
            <strong>Student Tips:</strong>
            <ul style={{ margin: 0, paddingLeft: 20 }}>
              <li>Set a savings target of 10–15% of your income.</li>
              <li>Track food delivery and subscription expenses closely.</li>
              <li>Avoid unnecessary subscriptions and impulse purchases.</li>
              <li>Look for student discounts and offers.</li>
            </ul>
          </div>
        )}
        <div className="summary-grid">
          <SummaryCard
            title="Monthly Income"
            value={summary.monthlyIncome}
            icon="💵"
            type="currency"
            currency={currency}
          />
          <SummaryCard
            title="Total Expenses"
            value={summary.totalExpenses}
            icon="💸"
            type="currency"
            currency={currency}
            subtitle={`(${((summary.totalExpenses / summary.monthlyIncome) * 100).toFixed(1)}% of income)`}
          />
          <SummaryCard
            title="Disposable Income"
            value={summary.disposableIncome}
            icon="🎯"
            type="currency"
            currency={currency}
            subtitle="Available after expenses"
          />
          <SummaryCard
            title="Total Debt"
            value={summary.totalDebt}
            icon="📊"
            type="currency"
            currency={currency}
          />
          <SummaryCard
            title="Savings Rate"
            value={studentMode ? Math.min(summary.savingsRate, 0.15) : summary.savingsRate}
            icon="📈"
            type="percentage"
            subtitle={studentMode ? "Student target: 10–15%" : "Percentage of income saved"}
          />
          <SummaryCard
            title="Debt-to-Income Ratio"
            value={summary.debtToIncomeRatio}
            icon="⚖️"
            type="number"
            subtitle="Lower is better"
          />
        </div>
      </section>

      {/* Charts Section */}
      <section className="charts-section">
        <h2>Financial Insights</h2>
        <div className="charts-grid">
          {/* Expense Distribution Pie Chart */}
          <div className="chart-card">
            <h3>Expense Distribution</h3>
            <p className="chart-subtitle">How your money is being spent</p>
            <div className="chart-container">
              <Pie data={expenseChartData} options={expenseChartOptions} />
            </div>
            <div className="chart-stats">
              {Object.entries(expenses).map(([category, amount]) => (
                <div key={category} className="stat-row">
                  <span>{category}</span>
                  <span className="stat-value">{formatCurrency(amount, currency)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Savings Projection Line Chart */}
          <div className="chart-card">
            <h3>Savings Projection (6 Months)</h3>
            <p className="chart-subtitle">Based on current income and spending</p>
            <div className="chart-container">
              <Line data={savingsChartData} options={savingsChartOptions} />
            </div>
            <div className="chart-stats">
              <div className="stat-row">
                <span>Current Estimated Savings</span>
                <span className="stat-value">{formatCurrency(summary.disposableIncome * 0.5, currency)}</span>
              </div>
              <div className="stat-row">
                <span>6-Month Projection</span>
                <span className="stat-value highlight">{formatCurrency(savingsProjection.data[6], currency)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Debt Repayment Timeline Bar Chart */}
        {debts && debts.length > 0 && (
          <div className="chart-card full-width">
            <h3>Debt Repayment Timeline</h3>
            <p className="chart-subtitle">Outstanding debt vs. monthly payments by creditor</p>
            <div className="chart-container">
              <Bar data={debtChartData} options={debtChartOptions} />
            </div>
            <div className="chart-details">
              <table className="debt-table">
                <thead>
                  <tr>
                    <th>Debt Type</th>
                    <th>Amount</th>
                    <th>Interest Rate</th>
                    <th>Monthly Payment</th>
                  </tr>
                </thead>
                <tbody>
                  {debts.map((debt) => (
                    <tr key={debt.name}>
                      <td>{debt.name}</td>
                      <td>{formatCurrency(debt.amount, currency)}</td>
                      <td>{debt.interestRate}%</td>
                      <td>{formatCurrency(debt.monthlyPayment || 50, currency)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </section>

      {/* Action Plan Section */}
      <ActionPlan recommendations={recommendations} />

      {/* Footer with Additional Info */}
      <section className="dashboard-footer">
        <div className="disclaimer">
          <h3>📌 How to Use This Dashboard</h3>
          <ul>
            <li><strong>Financial Overview:</strong> Monitor your key metrics and track changes over time</li>
            <li><strong>Expense Distribution:</strong> Identify where your money goes and find optimization opportunities</li>
            <li><strong>Savings Projection:</strong> See potential growth with consistent saving habits</li>
            <li><strong>Debt Timeline:</strong> Understand your debt obligations and repayment schedules</li>
            <li><strong>Action Plan:</strong> Follow prioritized recommendations based on your financial situation</li>
          </ul>
        </div>
        {demoMode && (
          <div className="demo-banner" style={{ background: '#e0eaff', color: '#1a237e', padding: '8px 0', textAlign: 'center', fontWeight: 600, borderRadius: 6, marginBottom: 12 }}>
            Demo Mode Active — Backend unavailable, showing sample data.
          </div>
        )}
      </section>
    </div>
  )
}

