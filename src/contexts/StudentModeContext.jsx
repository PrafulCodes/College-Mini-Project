import React, { createContext, useContext, useState } from "react";

const StudentModeContext = createContext();

export function StudentModeProvider({ children }) {
  const [studentMode, setStudentMode] = useState(false);
  return (
    <StudentModeContext.Provider value={{ studentMode, setStudentMode }}>
      {children}
    </StudentModeContext.Provider>
  );
}

export function useStudentMode() {
  return useContext(StudentModeContext);
}
