// utils/preferences.js

const PREF_KEY = 'moneyCouncilPreferences';

export function savePreferences({ currency, studentMode }) {
  const prefs = { currency, studentMode };
  localStorage.setItem(PREF_KEY, JSON.stringify(prefs));
}

export function loadPreferences() {
  try {
    const raw = localStorage.getItem(PREF_KEY);
    if (!raw) return { currency: 'INR', studentMode: false };
    const prefs = JSON.parse(raw);
    return {
      currency: prefs.currency || 'INR',
      studentMode: !!prefs.studentMode
    };
  } catch {
    return { currency: 'INR', studentMode: false };
  }
}
