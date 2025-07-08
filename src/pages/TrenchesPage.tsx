import React from "react";
import TokenCard from "../components/TokenCard";
import TrenchesToolbar from "../components/TrenchesToolbar";
const TrenchesPage: React.FC = () => {
  return (
    <div className="min-h-screen p-4 bg-black text-white">
      <TrenchesToolbar />
      <div className="min-h-screen p-4 bg-black text-white">
        <TokenCard />
        <TokenCard />
        <TokenCard />
        <TokenCard />
        <TokenCard />
        <TokenCard />
      </div>
    </div>
  );
};

export default TrenchesPage;
