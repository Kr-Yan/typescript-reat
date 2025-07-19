import type { Token, Transaction, CopyTrader } from "../types";

// const mockCopyTraders: CopyTrader[] =[
//     {

//     },
//     {

//     }
// ]

let mockTransactions: Transaction[] = [
  {
    id: "1",
    type: "buy",
    token: "o5JSY...xTy",
    amount: 0.418,
    price: 25.7,
    timestamp: new Date(Date.now() - 3600000),
    status: "completed",
  },
  {
    id: "2",
    type: "copy",
    token: "6cSx5...UK8",
    amount: 0,
    price: 24.8,
    timestamp: new Date(Date.now() - 7200000),
    status: "completed",
  },
];

const mockTokens: Token[] = [
  {
    id: "1",
    symbol: "WWI50...",
    name: "World War Index 500",
    status: "completed",
  },
  {
    id: "2",
    symbol: "$TRUM...",
    name: "Donald J. Trump",
    status: "completing",
  },
  { id: "3", symbol: "PEOPL...", name: "Bet on this", status: "completing" },
];

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
export const mockAPI = {
  // mockAPI.getTransactions(),
  // mockAPI.getCopyTraders(),
  // mockAPI.getMarketData(),

  getTransactions: async (): Promise<Transaction[]> => {
    await delay(500);
    return [...mockTransactions];
  },

  getMarketData: async (
    statusFilter?: "all" | "completing" | "completed"
  ): Promise<Token[]> => {
    await delay(500);
    let filteredTokens = [...mockTokens];

    if (statusFilter && statusFilter !== "all") {
      filteredTokens = mockTokens.filter(
        (token) => token.status === statusFilter
      );
    }
    return filteredTokens;
  },
};
