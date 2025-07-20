import React, { useState } from "react";
import "./App.css";
import TrenchesPage from "./pages/TrenchesPage";
import { type TabType } from "./types/index";
import Header from "./components/Header";
import CopyTradePage from "./pages/CopyTradePage";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>("trenches");

  const renderActivePage = () => {
    switch (activeTab) {
      case "trenches":
        return <TrenchesPage tokens={[]} />;

      case "copytrade":
        return <CopyTradePage />;
    }
  };
  return (
    <div>
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      {renderActivePage()}
    </div>

    // <BrowserRouter>
    //   <Routes>
    //     {/* <Route path="/trenches" element={<TrenchesPage />} /> */}
    //     <Route path="/trenches" element={<TrenchesPage tokens={[]} />} />

    //     <Route path="*" element={<Navigate to="/trenches" replace />} />
    //     {/* <Route path="*" element={<CopyTradePage />} /> */}
    //   </Routes>
    // </BrowserRouter>
  );
};

export default App;
