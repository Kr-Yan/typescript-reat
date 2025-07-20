import React, { useState } from "react";
import { type TabType } from "../types/index";
// - pages (trenches, newpair, trending, copytrade etc.)
// -logo
// -search bar
// -cooking: subpage
// -coin type:dropdown
// -setting:dropdown
// -deposit: dropdown
// -wallet : dropdown

interface HeaderProps {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
}

const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab }) => {
  const [searchBar, setSearchBar] = useState();
  const [walletDropdown, setWalletDropdown] = useState(false);

  return (
    <div className="bg-black px-4 pt-3 pb-4">
      <div className="flex items-center justify-between mb-6">
        <div className="flex item-center gap-12">
          <div className="relative">
            <div className="w-8 h-8 bg-black flex">
              <span>🎀</span>
              <div className="text-white">GMGN</div>
            </div>
          </div>
          <div className="text-white flex gap-6">
            <button
              onClick={() => setActiveTab("trenches")}
              className={`whitespace-nowrap pb-1 transition-colors ${
                activeTab === "trenches"
                  ? "text-white"
                  : "text-gray-400 hover:text-gray-300"
              }`}
            >
              Trenches
            </button>

            {/* <button onClick={()=>setActiveTab("newpair")}>New Pair</button> */}

            <button className="text-gray-400 hover:text-gray-300">
              Trending
            </button>

            <button
              onClick={() => setActiveTab("copytrade")}
              className={`whitespace-nowrap pb-1 transition-colors ${
                activeTab === "copytrade"
                  ? "text-white font-medium border-b-2 border-green-500"
                  : "text-gray-400 hover:text-gray-300"
              }`}
            >
              CopyTrade
            </button>
          </div>
        </div>

        {/* two side for login */}
        <div className="text-white">Wallet</div>
      </div>
    </div>
  );
};

export default Header;
