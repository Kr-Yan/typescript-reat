import React from "react";
import { Users, Zap } from "lucide-react";
const TrenchesToolbar: React.FC = () => (
  <div className="flex items-center justify-between mb-6 px-4">
    {/* Left icons */}
    <div className="flex items-center gap-4">
      <div className="p-2 bg-gray-800 rounded">
        <Users className="h-5 w-5 text-white" />
      </div>
      <div className="p-2 bg-gray-800 rounded">
        <Zap className="h-5 w-5 text-green-400" />
      </div>
    </div>

    {/* Right icons */}
    <div className="flex items-center gap-4">
      <div className="p-2 bg-gray-800 rounded">Filter</div>
      <div className="p-2 bg-gray-800 rounded">Search</div>
    </div>
  </div>
);

export default TrenchesToolbar;
