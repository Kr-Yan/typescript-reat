import React, { useState } from "react";

interface MarketAnalysisPageProps {
  tokenData?: {
    symbol: string;
  };
  onBack: () => void;
}
export const MarketAnalysisPage: React.FC<MarketAnalysisPageProps> = ({
  tokenData = {
    symbol: "AIRBALL",
  },
  onBack,
}) => {
  const [activeTab, setActiveTab] = useState<
    "activity" | "liquidity" | "traders" | "holders" | "following"
  >("activity");
  const [activityFilter, setActivityFilter] = useState<
    "all" | "smart" | "kol" | "following" | "remarks" | "dev" | "whale"
  >("all");
  const [chartTimeframe, setChartTimeframe] = useState("1h");

  const activityData = [
    {
      id: 1,
      age: "0s",
      type: "Buy",
      amount: 84.52,
      usd: 10,
      token: "AIRBALL",
    },
    {
      id: 2,
      age: "1s",
      type: "Sell",
      amount: 68.97,
      usd: 8.5,
      token: "AIRBALL",
      isProfit: true,
    },
  ];

  const timeframes = ["1s", "15s", "30s", "1m", "5m", "15m", "1h"];
  const priceButtons = [
    "1m +56.18%",
    "5m +56.18%",
    "1h +56.18%",
    "24h +56.18%",
  ];

  return (
    <div className="bg-black text-white">
      <button onClick={onBack}></button>
    </div>
  );
};
