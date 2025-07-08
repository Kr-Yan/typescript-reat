import React from "react";

interface TokenCardProps {
  symbol?: string;
  name?: string;
  price?: number;
  onClick?: () => void;
}

const TokenCard: React.FC<TokenCardProps> = ({
  symbol = "TKN",
  name = "TokenName",
  price = 0.0,
  onClick,
}) => (
  <div
    className="p-4 bg-gray-800 rounded-lg cursor-pointer hover:bg-gray-700 transition"
    onClick={onClick}
  >
    <h3 className="text-lg font-semibold">{symbol}</h3>
    <p className="text-sm text-gray-400">{name}</p>
    <p className="mt-2 text-white font-bold">${price.toFixed(2)}</p>
  </div>
);

export default TokenCard;
