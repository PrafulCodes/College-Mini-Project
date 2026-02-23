import React from "react";

const CURRENCIES = [
  { code: "INR", label: "INR (₹)" },
  { code: "USD", label: "USD ($)" },
  { code: "EUR", label: "EUR (€)" },
];

export default function CurrencySelector({ currency, setCurrency }) {
  return (
    <div className="currency-selector">
      <label htmlFor="currency-select">Currency: </label>
      <select
        id="currency-select"
        value={currency}
        onChange={e => setCurrency(e.target.value)}
      >
        {CURRENCIES.map(opt => (
          <option key={opt.code} value={opt.code}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
}
