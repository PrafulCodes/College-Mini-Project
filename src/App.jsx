
import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import InputForm from './pages/InputForm'
import Dashboard from './pages/Dashboard'
import { CurrencyProvider } from './contexts/CurrencyContext'
import { StudentModeProvider } from './contexts/StudentModeContext'
import { loadPreferences } from './utils/preferences'
import './styles/App.css'


export default function App() {
  // Load preferences once on app start (if needed for side effects)
  // const prefs = loadPreferences(); // Not used directly here
  return (
    <CurrencyProvider>
      <StudentModeProvider>
        <Router>
          <Routes>
            <Route path="/" element={<InputForm />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </Router>
      </StudentModeProvider>
    </CurrencyProvider>
  );
}
