import React, { useState, useEffect } from "react";
// import TokenCard from "../components/TokenCard";
// import TrenchesToolbar from "../components/TrenchesToolbar";
// import TokenCard from "../components/TokenCard";
// import TrenchesToolbar from "../components/TrenchesToolbar";
import type { Token, TokenStatusFilter } from "../types";
import { mockAPI } from "../services/mockAPI";
// import MarketAnalysisPage from "../pages/MarketAnalysisPage";

import {
  ChevronDown,
  Filter,
  Search,
  Zap,
  Users,
  Clock,
  Crown,
  Copy,
  Globe,
  RefreshCw,
} from "lucide-react";

interface TrenchesPageProps {
  tokens: Token[];
}

const TrenchesPage: React.FC<TrenchesPageProps> = ({}) => {
  const [tokens, setTokens] = useState<Token[]>([]);
  const [statusFilter, setStatusFilter] = useState<TokenStatusFilter>("all");
  const [isLoading, setIsLoading] = useState(false);
  const [selectedToken, setSelectedToken] = useState<Token | null>(null);
  const [showStatusDropdown, setShowStatusDropdown] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    const loadTokens = async () => {
      setIsLoading(true);
      try {
        const filteredTokens = await mockAPI.getMarketData(statusFilter);
        setTokens(filteredTokens);
      } catch (error) {
        console.error("Failed to load tokens", error);
      } finally {
        setIsLoading(false);
      }
    };
    loadTokens();
  }, [statusFilter]);

  const handleStatusFilterChange = (newFilter: TokenStatusFilter) => {
    setStatusFilter(newFilter);
    setShowStatusDropdown(false);
  };
  const handleTokenClick = (token: Token) => {
    setSelectedToken(token);
  };

  const getStatusCount = (status: TokenStatusFilter) => {
    if (status === "all") return tokens.length;
    return tokens.filter((token) => token.status === status).length;
  };

  const filteredTokens = tokens.filter(
    (token) =>
      token.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      token.symbol.toLowerCase().includes(searchTerm.toLowerCase())
  );
  const getStatusDisplayText = () => {
    switch (statusFilter) {
      case "completing":
        return "Completing";
      case "completed":
        return "Completed";
      default:
        return "New Creations";
    }
  };

  // if (selectedToken) {
  //   return <MarketAnalysisPage />;
  // }
  return (
    <div className="min-h-screen bg-black text-white">
      {/* Controls row */}
      <div className="flex items-center justify-between mb-6 px-4 py-4">
        {/* Left controls */}

        <div className="flex items-center gap-3">
          {/* Grid icon */}
          <div className="w-7 h-7 bg-gray-800 rounded flex items-center justify-center">
            <div className="grid grid-cols-2 gap-0.5">
              <div className="w-1.5 h-1.5 bg-white rounded-sm"></div>
              <div className="w-1.5 h-1.5 bg-white rounded-sm"></div>
              <div className="w-1.5 h-1.5 bg-white rounded-sm"></div>
              <div className="w-1.5 h-1.5 bg-white rounded-sm"></div>
            </div>
          </div>

          {/* Users icon */}
          <div className="w-7 h-7 bg-gray-800 rounded flex items-center justify-center">
            <Users className="h-4 w-4 text-white" />
          </div>

          {/* Filter lines icon */}
          <div className="w-7 h-7 bg-gray-800 rounded flex items-center justify-center">
            <div className="flex flex-col gap-0.5">
              <div className="w-3 h-0.5 bg-white rounded"></div>
              <div className="w-3 h-0.5 bg-white rounded"></div>
              <div className="w-3 h-0.5 bg-white rounded"></div>
            </div>
          </div>
        </div>

        {/* Right controls */}
        <div className="flex items-center gap-3">
          {/* Lightning section with colored bars */}
          <div className="bg-gray-800 rounded-lg px-3 py-1.5 flex items-center gap-2 border border-gray-600">
            <Zap className="h-4 w-4 text-green-400" />
            <div className="flex gap-1">
              <div className="w-4 h-0.5 bg-purple-500 rounded"></div>
              <div className="w-4 h-0.5 bg-blue-500 rounded"></div>
              <div className="w-4 h-0.5 bg-green-500 rounded"></div>
            </div>
            <span className="text-white text-sm font-medium">0</span>
          </div>

          {/* P1 dropdown */}
          <div className="flex items-center gap-1">
            <span className="text-white text-sm font-medium">P1</span>
            <ChevronDown className="h-3 w-3 text-gray-400" />
          </div>

          {/* Settings circle */}
          <div className="w-6 h-6 bg-gray-800 rounded-full flex items-center justify-center">
            <div className="w-3 h-3 border border-gray-400 rounded-full"></div>
          </div>
        </div>
      </div>

      {/* New Creations Header with Dropdown */}
      <div className="flex items-center justify-between px-4 py-3 bg-gray-900/30">
        <div className="flex items-center gap-3">
          <span className="text-2xl">🌱</span>
          <div className="relative">
            <button
              onClick={() => setShowStatusDropdown(!showStatusDropdown)}
              className="flex items-center gap-2 text-white font-bold text-lg"
            >
              {getStatusDisplayText()}
              <ChevronDown
                className={`h-4 w-4 text-gray-400 transition-transform ${
                  showStatusDropdown ? "rotate-180" : ""
                }`}
              />
            </button>

            {showStatusDropdown && (
              <div className="absolute top-full left-0 mt-2 bg-gray-800 rounded-lg border border-gray-600 shadow-lg z-10 min-w-48">
                <button onClick={() => handleStatusFilterChange("all")}>
                  <div className="flex justify-between items-center">
                    <span>All New Creations</span>
                    <span className="text-gray-400 text-sm">
                      ({getStatusCount("all")})
                    </span>
                  </div>
                </button>

                <button
                  onClick={() => handleStatusFilterChange("completing")}
                  className={`w-full text-left px-4 py-3 hover:bg-gray-700 ${
                    statusFilter === "completing"
                      ? "bg-gray-700 text-green-400"
                      : "text-white"
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <span>Completing</span>
                    <span>({getStatusCount("completing")})</span>
                  </div>
                  <div className="text-xs text-gray-400 mt-1">
                    Tokens in progress
                  </div>
                </button>

                <button onClick={() => handleStatusFilterChange("completed")}>
                  <div>
                    <span>Completed</span>
                    <span>({getStatusCount("completed")})</span>
                  </div>
                  <div>Fully launched tokens</div>
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search />
            <input
              type="text"
              placeholder="Search"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-gray-700/50 border border-gray-600 rounded-lg pl-10 pr-4 py-2 text-sm text-white placeholder-gray-400 w-28 focus:outline-none focus:border-gray-500"
            />
          </div>

          <button className="flex items-center gap-2 bg-gray-700/50 border border-gray-600 rounded-lg px-3 py-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <span className="text-gray-400 text-sm">Filter</span>
          </button>
        </div>
      </div>

      {/* {isLoading && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-400"></div>
        </div>
      )} */}

      {filteredTokens.length === 0 && !isLoading ? (
        <div>No Token found</div>
      ) : (
        filteredTokens.map((token) => (
          <div
            key={token.id}
            onClick={() => handleTokenClick(token)}
            className="bg-gray-900/70 rounded-lg p-3 mx-4 mb-3 border border-gray-700/50 cursor-pointer hover:bg-gray-800/70 transition-colors"
          >
            <div>
              <span>{token.symbol}</span>
            </div>

            <div>
              <span>{token.name}</span>
            </div>

            <div>
              <span></span>
            </div>

            <div>
              <span></span>
            </div>
          </div>
        ))
      )}
    </div>
  );
};
// const TrenchesPage: React.FC = () => {
//   return (
//     <div className="min-h-screen p-4 bg-black text-white">
//       <TrenchesToolbar />
//       <div className="min-h-screen p-4 bg-black text-white">
//         <TokenCard />
//         <TokenCard />
//         <TokenCard />
//         <TokenCard />
//         <TokenCard />
//         <TokenCard />
//       </div>
//     </div>
//   );
// };

export default TrenchesPage;
