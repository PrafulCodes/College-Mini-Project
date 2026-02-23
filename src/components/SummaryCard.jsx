
import React from 'react'
import { formatCurrency } from '../utils/currencyFormatter'
import '../styles/SummaryCard.css'
import { useCurrency } from '../contexts/CurrencyContext'

export default function SummaryCard({ title, value, subtitle, icon, type = 'default', currency: propCurrency }) {
  const { currency: contextCurrency } = useCurrency ? useCurrency() : { currency: 'INR' };
  const currency = propCurrency || contextCurrency || 'INR';

  const getCardClass = () => `summary-card summary-card-${type}`;

  const displayValue = () => {
    if (type === 'currency') {
      return formatCurrency(value, currency);
    } else if (type === 'percentage') {
      return `${(value * 100).toFixed(1)}%`;
    } else if (type === 'number') {
      return value.toLocaleString();
    }
    return value;
  };

  return (
    <div className={getCardClass()}>
      <div className="card-icon">{icon}</div>
      <div className="card-content">
        <p className="card-title">{title}</p>
        <p className="card-value">{displayValue()}</p>
        {subtitle && <p className="card-subtitle">{subtitle}</p>}
      </div>
    </div>
  );
}
