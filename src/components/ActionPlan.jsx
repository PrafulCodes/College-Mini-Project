
import React from 'react'
import { getPriorityColor } from '../services/mockData'
import { useCurrency } from '../contexts/CurrencyContext'
import { formatCurrency } from '../utils/currencyFormatter'
import '../styles/ActionPlan.css'


export default function ActionPlan({ recommendations }) {
  const { currency } = useCurrency ? useCurrency() : { currency: 'INR' };

  if (!recommendations || recommendations.length === 0) {
    return (
      <section className="action-plan">
        <h2>Action Plan</h2>
        <p className="no-data">No recommendations available</p>
      </section>
    )
  }

  // Try to format estimatedSavings if it looks like a number or currency
  const formatBenefit = (benefit) => {
    if (typeof benefit === 'number') return formatCurrency(benefit, currency);
    if (typeof benefit === 'string') {
      // Try to extract number from string
      const match = benefit.match(/([₹$€]?)([\d,]+(\.\d+)?)/);
      if (match) {
        const num = Number(match[2].replace(/,/g, ''));
        if (!isNaN(num)) return benefit.replace(match[0], formatCurrency(num, currency));
      }
    }
    return benefit;
  };

  return (
    <section className="action-plan">
      <h2 style={{ marginBottom: 0 }}>Personalized Action Plan</h2>
      <p className="section-subtitle" style={{ marginTop: 4, marginBottom: 16, fontWeight: 500 }}>
        Follow these <span style={{ color: '#e74c3c', fontWeight: 700 }}>priority</span> recommendations to optimize your financial health
      </p>

      <div className="recommendations-list">
        {recommendations.map((rec, index) => (
          <div
            key={rec.id}
            className="recommendation-card"
            style={rec.priority === 'High' ? { border: '2px solid #e74c3c', boxShadow: '0 0 8px #f8d7da' } : rec.priority === 'Medium' ? { border: '2px solid #f39c12', boxShadow: '0 0 8px #fff3cd' } : {}}
          >
            <div className="card-header">
              <div className="card-rank">
                <span className="rank-number">{index + 1}</span>
              </div>
              <div className="card-title-section">
                <h3>{rec.title}</h3>
                <span
                  className="priority-badge"
                  style={{ backgroundColor: getPriorityColor(rec.priority) }}
                >
                  {rec.priority} Priority
                </span>
              </div>
            </div>

            <p className="card-description">{rec.description}</p>

            <div className="card-details">
              <div className="detail-item">
                <label>Action:</label>
                <p>{rec.action}</p>
              </div>
              <div className="detail-item">
                <label>Potential Benefit:</label>
                <p>{formatBenefit(rec.estimatedSavings)}</p>
              </div>
              <div className="detail-item">
                <label>Timeframe:</label>
                <p>{rec.timeframe}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="plan-summary">
        <h3>Implementation Tips</h3>
        <ul>
          <li>Start with High Priority items first</li>
          <li>Set specific, measurable goals for each recommendation</li>
          <li>Review your progress monthly</li>
          <li>Adjust strategies as your situation changes</li>
          <li>Consider automating your savings and debt payments</li>
        </ul>
      </div>
    </section>
  )
}
