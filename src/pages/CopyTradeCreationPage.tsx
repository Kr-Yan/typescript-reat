import React, { useState } from "react";

import { type CopyTrader, type User } from "../types";

interface CopyTradeCreationPageProps {
  //   selectedTrader?: CopyTrader | null;
  //   user: User;
  //   onBack: () => void;
  //   onSuccess: () => void;
}

const CopyTradeCreationPage: React.FC<CopyTradeCreationPageProps> = (
  {
    //   selectedTrader,
    //   user,
    //   onBack,
    //   onSuccess,
  }
) => {
  return (
    <div>
      <h2>Copy Trade Creation</h2>
      <div>
        <strong>Trader:</strong>{" "}
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
