import React, { useState } from "react";
import { type TabType, type User } from "../types/index";
import { Search } from "lucide-react";
// - pages (trenches, newpair, trending, copytrade etc.)
// -logo
// -search bar
// -cooking: subpage
// -coin type:dropdown
// -setting:dropdown
// -deposit: dropdown
// -wallet : dropdown

interface HeaderProps {
  user: User | null;
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
}

const Header: React.FC<HeaderProps> = ({ user, activeTab, setActiveTab }) => {
  const [searchBar, setSearchBar] = useState();
  const [walletDropdown, setWalletDropdown] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <div className="bg-black px-4 pt-3 pb-4">
      <div className="flex items-center justify-between mb-6 text-white">
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

            <button className="text-gray-400 hover: text-gray-300">
              New Pair
            </button>

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

            <button className="text-gray-400 hover:text-gray-300">
              Monitor
            </button>

            <button className="text-gray-400 hover: text-gray-300">
              Follow
            </button>
          </div>
        </div>

        <div>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-gray-700/50 border border-gray-600 rounded-lg pl-10 pr-4 py-2 text-sm text-white placeholder-gray-400 w-35 focus:outline-none focus:border-gray-500"
            />
          </div>
        </div>

        <div>Cooking</div>

        <div>SOL</div>

        <div>setting</div>

        {/* two side for login */}

        <div>
          {user ? (
            <div>Wallet</div>
          ) : (
            <>
              <button className="px-3 py-2">SignUp</button>
              <button className="px-3 py-2">LogIn</button>
            </>
          )}
        </div>

        {/* <div>Wallet</div> */}
      </div>
    </div>
  );
};

export default Header;
