import React, { useState } from "react";
import { apiService } from "../services/auth_api";
import { type User } from "../types";

interface LoginModalProps {
  isOpen: boolean;
  onLogin: (user: User) => void;
}

const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onLogin }) => {
  if (!isOpen) return null;

  
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const user = await apiService.login(email, password);
    onLogin(user);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      // handleLogin();
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="text-white">
        <div className="font-bold">Log In</div>
        <div>Don't have account yet? Sign up</div>
        <div>Email</div>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="bg-gray-800"
        />
        <div>Password</div>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter Password"
          className="bg-gray-800"
        />

        <div>Forget Password?</div>

        <button
          onClick={handleLogin}
          className="w-full bg-green-700 font-bold rounded-lg"
        >
          Log In
        </button>

        <div className="text-center">OR</div>

        <div className="flex justify-around mb-6">
          <div>Telegram</div>
          <div>Phantom</div>
          <div>APP Scan</div>
        </div>

        <div className="text-center mt-6 ">
          <a>Terms of service</a>
          {" | "}
          <a>Private Policy</a>
        </div>
      </div>
    </div>
  );
};

export default LoginModal;
