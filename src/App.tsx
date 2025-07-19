import React, { useState } from "react";
import "./App.css";
import TrenchesPage from "./pages/TrenchesPage";
import CopyTradePage from "./pages/CopyTradePage";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* <Route path="/trenches" element={<TrenchesPage />} /> */}
        {/* <Route path="/trenches" element={<TrenchesPage tokens={[]} />} />

        <Route path="*" element={<Navigate to="/trenches" replace />} /> */}
        <Route path="*" element={<CopyTradePage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
