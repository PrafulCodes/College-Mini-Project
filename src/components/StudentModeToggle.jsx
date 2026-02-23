import React from "react";

export default function StudentModeToggle({ studentMode, setStudentMode }) {
  return (
    <div className="student-mode-toggle">
      <label htmlFor="student-mode-switch">
        <input
          id="student-mode-switch"
          type="checkbox"
          checked={studentMode}
          onChange={e => setStudentMode(e.target.checked)}
        />
        <span style={{ marginLeft: 8 }}>
          Student Mode {studentMode ? "ON" : "OFF"}
        </span>
      </label>
    </div>
  );
}
