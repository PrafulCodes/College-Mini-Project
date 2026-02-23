import React, { createContext, useContext, useState, useEffect } from "react";
import { savePreferences, loadPreferences } from '../utils/preferences';

const CurrencyContext = createContext();

export function CurrencyProvider({ children }) {
  const [currency, setCurrency] = useState(() => loadPreferences().currency || "INR");

  useEffect(() => {
    savePreferences({ currency, studentMode: loadPreferences().studentMode });
  }, [currency]);

  return (
    <CurrencyContext.Provider value={{ currency, setCurrency }}>
      {children}
    </CurrencyContext.Provider>
  );
}

export function useCurrency() {
  return useContext(CurrencyContext);
}
