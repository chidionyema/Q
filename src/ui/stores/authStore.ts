// stores/authStore.ts

import create from 'zustand';

type AuthState = {
  token: string | null;
  user: {
    name: string;
    email: string;
  } | null;
  setToken: (token: string) => void;
  setUser: (user: { name: string; email: string }) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  setToken: (token) => set({ token }),
  setUser: (user) => set({ user }),
  logout: () => set({ token: null, user: null })
}));
