/**
 * Mock Data for Financial Analysis Dashboard
 * This file contains realistic mock data structures and utility functions
 * Replace with actual API response in production
 */

// Example API response structure
export const mockAnalysisResponse = {
  status: 'success',
  summary: {
    monthlyIncome: 5000,
    totalExpenses: 1950,
    disposableIncome: 3050,
    totalDebt: 12000,
    netWorth: -7000,
    savingsRate: 0.61,
    debtToIncomeRatio: 2.4,
  },
  expenses: {
    Rent: 1200,
    Groceries: 500,
    Utilities: 150,
    Transportation: 100,
  },
  debts: [
    { name: 'Credit Card', amount: 3000, interestRate: 21.0, monthlyPayment: 75 },
    { name: 'Student Loan', amount: 7000, interestRate: 4.5, monthlyPayment: 89 },
    { name: 'Car Loan', amount: 2000, interestRate: 5.0, monthlyPayment: 50 },
  ],
  riskTolerance: 'Medium',
  recommendations: [
    {
      id: 1,
      priority: 'High',
      title: 'Eliminate High-Interest Credit Card Debt',
      description:
        'Your 21% APR credit card is costing you significantly. Focus on paying this off first.',
      action: 'Allocate ₹300/month to credit card',
      estimatedSavings: '₹1,260 over 1 year',
      timeframe: '10-12 months',
    },
    {
      id: 2,
      priority: 'High',
      title: 'Build Emergency Fund',
      description:
        'You need an emergency fund equal to 3-6 months of expenses (₹5,850-₹11,700).',
      action: 'Save ₹400/month to emergency fund',
      estimatedSavings: 'Peace of mind & financial security',
      timeframe: '12-18 months',
    },
    {
      id: 3,
      priority: 'Medium',
      title: 'Optimize Student Loan Payments',
      description:
        'Your student loan has a manageable interest rate. Maintain minimum payments while building emergency fund.',
      action: 'Continue ₹89/month minimum payment',
      estimatedSavings: 'Flexibility for other priorities',
      timeframe: 'Ongoing',
    },
    {
      id: 4,
      priority: 'Medium',
      title: 'Start Investing for Retirement',
      description: 'Once emergency fund is built, consider investing 10-15% of disposable income.',
      action: 'Open a Roth IRA or 401(k)',
      estimatedSavings: 'Significant long-term wealth growth',
      timeframe: 'After 12 months',
    },
    {
      id: 5,
      priority: 'Low',
      title: 'Reduce Discretionary Spending',
      description:
        'Review transportation and discretionary spending for optimization opportunities.',
      action: 'Cut casual spending by ₹100/month',
      estimatedSavings: '₹1,200 annually',
      timeframe: 'Immediately',
    },
  ],
  savings: {
    current: 0,
    projected3months: 1350,
    projected6months: 2700,
  },
};

// Alternative mock data with different financial situation
export const mockAnalysisResponse2 = {
  status: 'success',
  summary: {
    monthlyIncome: 8000,
    totalExpenses: 3500,
    disposableIncome: 4500,
    totalDebt: 0,
    netWorth: 15000,
    savingsRate: 0.5625,
    debtToIncomeRatio: 0,
  },
  expenses: {
    Rent: 1800,
    Groceries: 800,
    Utilities: 250,
    Entertainment: 400,
    Insurance: 250,
  },
  debts: [],
  riskTolerance: 'High',
  recommendations: [
    {
      id: 1,
      priority: 'High',
      title: 'Maximize Retirement Contributions',
      description:
        'You have strong income and no debt. Focus on long-term wealth building.',
      action: 'Contribute ₹2,000/month to retirement',
      estimatedSavings: '₹24,000 annually in tax-advantaged growth',
      timeframe: 'Ongoing',
    },
    {
      id: 2,
      priority: 'High',
      title: 'Diversify Investment Portfolio',
      description: 'With your high risk tolerance, consider a diversified investment approach.',
      action: 'Invest in index funds, stocks, and bonds',
      estimatedSavings: 'Potential 7-10% annual returns',
      timeframe: 'Ongoing',
    },
    {
      id: 3,
      priority: 'Medium',
      title: 'Build Wealth Through Real Estate',
      description: 'Consider real estate investment as part of your portfolio.',
      action: 'Save for down payment on investment property',
      estimatedSavings: 'Long-term wealth appreciation',
      timeframe: '12-24 months',
    },
  ],
  savings: {
    current: 15000,
    projected3months: 28500,
    projected6months: 42000,
  },
};

/**
 * Generate savings projection data for line chart
 * @param {number} currentSavings - Starting savings amount
 * @param {number} monthlyContribution - Monthly savings amount
 * @param {number} months - Number of months to project (default: 3)
 * @returns {Object} Chart data structure
 */
export const generateSavingsProjection = (currentSavings = 0, monthlyContribution = 1000, months = 3) => {
  const labels = []
  const data = []

  for (let i = 0; i <= months; i++) {
    labels.push(`Month ${i}`)
    data.push(Math.round(currentSavings + monthlyContribution * i))
  }

  return { labels, data }
}

/**
 * Generate debt repayment timeline data for bar chart
 * @param {Array} debts - Array of debt objects
 * @returns {Object} Chart data structure
 */
export const generateDebtTimeline = (debts = []) => {
  const labels = debts.map(d => d.name)
  const amounts = debts.map(d => d.amount)
  const payments = debts.map(d => d.monthlyPayment || 50)

  return { labels, amounts, payments }
}

/**
 * Calculate debt payoff timeline
 * @param {number} amount - Debt amount
 * @param {number} monthlyPayment - Monthly payment amount
 * @param {number} interestRate - Annual interest rate (APR)
 * @returns {Object} Payoff timeline info
 */
export const calculatePayoffTimeline = (amount, monthlyPayment, interestRate) => {
  const monthlyRate = interestRate / 100 / 12
  let balance = amount
  let months = 0
  let totalInterest = 0

  if (monthlyPayment <= balance * monthlyRate) {
    return { months: Infinity, totalInterest: Infinity, feasible: false }
  }

  while (balance > 0 && months < 600) {
    const interest = balance * monthlyRate
    const principal = monthlyPayment - interest
    balance -= principal
    totalInterest += interest
    months++
  }

  return {
    months,
    years: (months / 12).toFixed(1),
    totalInterest: Math.round(totalInterest),
    feasible: true,
  }
}

/**
 * Format currency value
 * @param {number} value - Value to format
 * @returns {string} Formatted currency string
 */
export const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value)
}

/**
 * Format percentage value
 * @param {number} value - Value to format (0-1 or 0-100)
 * @param {boolean} isDecimal - If true, treats value as decimal (0-1)
 * @returns {string} Formatted percentage string
 */
export const formatPercentage = (value, isDecimal = true) => {
  const percentage = isDecimal ? value * 100 : value
  return `${percentage.toFixed(1)}%`
}

/**
 * Get color for priority level
 * @param {string} priority - Priority level (High, Medium, Low)
 * @returns {string} Color hex value
 */
export const getPriorityColor = (priority) => {
  const colors = {
    High: '#e74c3c',
    Medium: '#f39c12',
    Low: '#27ae60',
  }
  return colors[priority] || '#95a5a6'
}

/**
 * Get priority badge class
 * @param {string} priority - Priority level
 * @returns {string} CSS class name
 */
export const getPriorityClass = (priority) => {
  return `priority-${priority.toLowerCase()}`
}

// Export sample data for development
export const defaultMockData = mockAnalysisResponse
