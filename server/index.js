const express = require("express");
const cors = require("cors");
const app = express();
const PORT = process.env.PORT || 3001;

let user = [
  {
    id: "1",
    email: "jojo@gmail.com",
    name: "Jojo",
    wallets: { "Main Wallet": "0x123...", "Trading Wallet": "0x456..." },
    balance: 58,
  },
];
