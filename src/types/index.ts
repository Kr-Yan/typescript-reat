export interface CopyTrader {
  id: string;
  name: string;
  avatar: string;
  rank: number;
  pnl: number;
  pnlPercentage: number;
  followers: number;
  winRate: number;
  isFollowing: boolean;
  balance: number;
  totalTrades: number;
  avgTradeSize: number;
  recentTrades?: TraderPosition[];
}

export interface User {
  id: string;
  email: string;
  name: string;
  walletAddress: string;
  balance: number;
  inviteCode?: string;
}

export interface TraderPosition {
  id: string;
}

export interface Transaction {
  id: string;
  type: "buy" | "sell" | "copy";
  token: string;
  amount: number;
  price: number;
  timestamp: Date;
  status: "completed" | "pending";
}

export interface Token {
  id: string;
  symbol: string;
  name: string;
  status: "completed" | "completing";
  timeAgo?: string;
  contract?: string;
  avatar?: URL;
  total_holders?: number;
  dev_migrated?: number;
  TX?: number;
  percent_status?: number;
  percent_top_hold?: number;
  percent_dev_hold?: number;
  percent_sniper?: number;
  percent_rug?: number;
}

export type TabType =
  | "trenches"
  | "new pair"
  | "trending"
  | "copytrade"
  | "monitor"
  | "follow";

export type TokenStatusFilter = "all" | "completing" | "completed";
