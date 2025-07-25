import { type User } from "../types/index";

const API_BASE_URL = "http://localhost:3001/api";

export const apiService = {
  // object methods
  login: async (email: string, password: string): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (!data.success) throw new Error(data.detail);
    return data.user;
  },

  register: async (
    email: string,
    password: string,
    inviteCode: string
  ): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        password,
        inviteCode,
      }),
    });

    const data = await response.json();
    if (!data.success) throw new Error(data.detail);
    return data;
  },
};
