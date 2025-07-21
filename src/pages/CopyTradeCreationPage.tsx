import React, { useState } from "react";
import { X } from "lucide-react";

import { type CopyTrader, type User } from "../types";

interface CopyTradeCreationPageProps {
  //   selectedTrader?: CopyTrader | null;
  //   user: User;
  onBack: () => void;
  //   onSuccess: () => void;
}

const CopyTradeCreationPage: React.FC<CopyTradeCreationPageProps> = ({
  //   selectedTrader,
  //   user,
  onBack,
  //   onSuccess,
}) => {
  const [buyMethod, setBuyMethod] = useState<"max" | "fixed" | "ratio">("max");
  const [amount, setAmount] = useState(2);
  const [sellMethod, setSellMethod] = useState<"copy" | "not">("copy");
  const [advancedSetting, setAdvancedSetting] = useState(false);
  const [slippage, setSplippage] = useState<"auto" | "custom">("auto");
  const [priorityFee, setPriorityFee] = useState("0.005");
  const [antiMev, setAntiMev] = useState(false);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="flex items-center justify-between p-4 border-b border-gray-700">
        <h1 className="text-xl font-bold">CopyTrade</h1>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-gray-400">
            <span className="text-sm">🎓 Tutorial</span>
          </div>
          <button onClick={onBack}>
            <X className="h-6 w-6 text-gray-400" />
          </button>
        </div>
      </div>

      <div className="p-4">
        {/* Lightning mode toggle */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <span className="text-yellow-400">
              Lightning mode, rapid on-chain
            </span>
            <div className="w-8 h-4 bg-yellow-500 rounded-full relative">
              <div className="w-3 h-3 bg-white rounded-full absolute right-0.5 top-0.5"></div>
            </div>
          </div>
        </div>
      </div>
      {/* {selectedTrader ? selectedTrader.name : "None selected"}
      </div>

      <div>
        <strong>User: </strong>
        {user.name}
      </div>
      <button onClick={onBack}>Back</button>
      <button onClick={onSuccess}>Create Copy Trade</button> */}
    </div>
  );
};

export default CopyTradeCreationPage;
