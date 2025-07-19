import CopyTradeCreationPage from "./CopyTradeCreationPage";
import React, { useState } from "react";
interface CopyTradePageProps {}

const CopyTradePage: React.FC<CopyTradePageProps> = ({}) => {
  const [CopyCreation, setCopyCreation] = useState(false);

  const handleCopyCreation = () => {
    setCopyCreation(true);
  };

  if (CopyCreation) {
    return <CopyTradeCreationPage />;
  }
  return (
    <div>
      Copy Trade Page
      <div>
        <button
          onClick={() => {
            handleCopyCreation();
          }}
        >
          Create Copy Trade
        </button>
      </div>
    </div>
  );
};

export default CopyTradePage;
