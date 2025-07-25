import React, { useState } from "react";
import { apiService } from "../services/auth_api";

interface LoginModalProps {
  isOpen: boolean;
}

const LoginModal: React.FC<LoginModalProps> = ({ isOpen }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="text-white">please login!</div>
    </div>
  );
};

export default LoginModal;
